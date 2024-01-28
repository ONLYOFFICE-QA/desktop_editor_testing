# -*- coding: utf-8 -*-
import json
import time
from os.path import join, getsize, basename, isdir, expanduser, isfile

import tempfile
import requests
from rich import print


from frameworks.decorators import singleton
from frameworks.host_control import FileUtils


@singleton
class Telegram:
    def __init__(self):
        self._telegram_token = self._get_token()
        self._chat_id = self._get_chat_id()
        self.tmp_dir = tempfile.gettempdir()
        self.proxies = self._get_proxies()
        FileUtils.create_dir(self.tmp_dir, stdout=False)

    @staticmethod
    def _get_token():
        path = join(expanduser('~'), '.telegram', 'token')
        if isfile(path):
            return FileUtils.file_reader(path).strip()
        print(f"[cyan]|INFO|Telegram token not exists.")

    @staticmethod
    def _get_chat_id():
        path = join(expanduser('~'), '.telegram', 'chat')
        if isfile(path):
            return FileUtils.file_reader(path).strip()
        print(f"[cyan]|INFO|Telegram chat id not exists.")

    @staticmethod
    def _get_proxies():
        proxies_config_path = join(expanduser('~'), '.telegram', 'proxy.json')
        if isfile(proxies_config_path):
            config = FileUtils.read_json(proxies_config_path)

            for check_key in ['login', 'password', 'ip', 'port']:
                if not config.get(check_key, None):
                    return {}

            proxy = f"http://{config['login']}:{config['password']}@{config['ip']}:{config['port']}"
            return {'http': proxy, 'https': proxy}

        return {}

    def send_message(self, message: str, out_msg=False) -> None:
        print(message) if out_msg else ...
        if self._access:
            if len(message) > 4096:
                document = self._make_massage_doc(message=message)
                self.send_document(document, caption=self._prepare_caption(message))
                return FileUtils.delete(document)
            self._request(
                f"https://api.telegram.org/bot{self._telegram_token}/sendMessage",
                data={"chat_id": self._chat_id, "text": message, "parse_mode": "Markdown"},
                tg_log=False
            )

    def send_document(self, document_path: str, caption: str = '') -> None:
        if self._access:
            self._request(
                f"https://api.telegram.org/bot{self._telegram_token}/sendDocument",
                data={"chat_id": self._chat_id, "caption": self._prepare_caption(caption), "parse_mode": "Markdown"},
                files={"document": open(self._prepare_documents(document_path), 'rb')}
            )

    def send_media_group(self, document_paths: list, caption: str = None, media_type: str = 'document') -> None:
        """
        :param document_paths:
        :param caption:
        :param media_type: types: 'photo', 'video', 'audio', 'document', 'voice', 'animation'
        :return:
        """
        if self._access:
            if not document_paths:
                return self.send_message(caption if caption else 'No files to send.', out_msg=True)
            if caption and len(caption)  > 200:
                document_paths.append(self._make_massage_doc(caption, 'caption.txt'))
            files, media = {}, []
            for doc_path in document_paths:
                files[basename(doc_path)] = open(self._prepare_documents(doc_path), 'rb')
                media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))
            media[-1]['caption'] = self._prepare_caption(caption) if caption is not None else ''
            media[-1]['parse_mode'] = "Markdown"
            self._request(
                f'https://api.telegram.org/bot{self._telegram_token}/sendMediaGroup',
                data={'chat_id': self._chat_id, 'media': json.dumps(media)},
                files=files
            )

    @staticmethod
    def _prepare_caption(caption: str) -> str:
        return caption[:200]

    def _request(self, url: str, data: dict, files: dict = None, tg_log: bool = True, num_tries: int = 5) -> None:
        while num_tries > 0:
            try:
                print(f"[red]|INFO| The message to Telegram will be sent via proxy") if self.proxies else ...
                response = requests.post(url, data=data, files=files, proxies=self.proxies)

                if response.status_code == 200:
                    return

                print(f"Error when sending to telegram: {response.json()}")

                if response.status_code == 429:
                    timeout = response.json().get('parameters', {}).get('retry_after', 10) + 1
                    print(f"Retry after: {timeout}")
                    time.sleep(timeout)

            except Exception as e:
                print(f"|WARNING| Impossible to send: {data}. Error: {e}\n timeout: 5 sec")
                self.send_message(f"|WARNING| Impossible to send: {data}. Error: {e}") if tg_log else ...
                time.sleep(5)

            finally:
                num_tries -= 1

    def _prepare_documents(self, doc_path: str) -> str:
        if getsize(doc_path) >= 50_000_000 or isdir(doc_path):
            FileUtils.compress_files(doc_path, join(self.tmp_dir, f'{basename(doc_path)}.zip'))
            return join(self.tmp_dir, f'{basename(doc_path)}.zip')
        return doc_path

    def _make_massage_doc(self, message: str, name: str = 'report.txt') -> str:
        doc_path = join(self.tmp_dir, name)
        with open(doc_path, "w") as file:
            file.write(message)
        return doc_path

    @property
    def _access(self) -> bool:
        if self._telegram_token and self._chat_id:
            return True
        return False
