# -*- coding: utf-8 -*-
from os import environ
from os.path import isfile, join, expanduser

from frameworks.host_control import FileUtils


class Auth:

    def __init__(self, token: str = None, chat_id: str = None):
        self._telegram_dir = join(expanduser('~'), '.telegram')
        self.token = token if token else self._get_token()
        self.chat_id = chat_id if chat_id else self._get_chat_id()

    def _get_token(self) -> "str | None":
        token_file = join(self._telegram_dir, 'token')

        if token_file and isfile(token_file):
            return FileUtils.file_reader(token_file).strip()
        elif environ.get('TELEGRAM_TOKEN', False):
            return environ.get('TELEGRAM_TOKEN')

        print(f"[cyan]|INFO| Telegram token not exists.")

    def _get_chat_id(self) -> "str | None":
        chat_id_file = join(self._telegram_dir, 'chat')

        if isfile(chat_id_file):
            return FileUtils.file_reader(chat_id_file).strip()
        elif environ.get('CHANNEL_ID', False):
            return environ.get('CHANNEL_ID')

        print(f"[cyan]|INFO| Telegram chat id not exists.")
