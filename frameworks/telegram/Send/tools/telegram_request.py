# -*- coding: utf-8 -*-
import time
import requests
from rich import print

from functools import wraps
from urllib3 import HTTPSConnectionPool
from urllib3.exceptions import NewConnectionError

from ...utils import Str
from ...Proxy import Proxy, ProxyFile
from ...Auth import Auth
from ...config import Config


def with_token_only(func):
    @wraps(func)
    def _check(self, *args, **kwargs):
        if self.auth.token:
            return func(self, *args, **kwargs)
        print('pls check token')

    return _check

def with_chat_id_only(func):
    @wraps(func)
    def _check(self, *args, **kwargs):
        if self.auth.chat_id:
            return func(self, *args, **kwargs)
        print('pls check token')

    return _check

class TelegramRequests:
    _API_HOST = Config.API_HOST

    def __init__(
            self,
            token: str = None,
            chat_id: str = None,
            proxy: Proxy = None,
            proxy_file: str = None,
            max_request_attempts: int = 10,
            interval: int = 5
        ):
        self.auth = Auth(token=token, chat_id=chat_id)
        self.interval = interval
        self.max_request_attempts = max_request_attempts
        self.tg_host = Str.delete_last_slash(self._API_HOST)
        self.proxies: dict = self._get_proxies(proxy, proxy_file)

    @with_chat_id_only
    @with_token_only
    def post(self, mode: str, data: dict, files: dict = None) -> bool:
        _max_attempts = self.max_request_attempts
        while _max_attempts > 0:
            try:
                print(f"[red]|INFO| The message to Telegram will be sent via proxy") if self.proxies else ...
                response = requests.post(self._get_url(mode), data=data, files=files, proxies=self.proxies)

                if response.status_code == 200:
                    return True

                print(f"Error when sending to telegram: {response.json()}")

                if response.status_code == 429:
                    timeout = response.json().get('parameters', {}).get('retry_after', 10) + 2
                    print(f"Retry after: {timeout}")
                    time.sleep(timeout)
                    return False

                if response.status_code == 400:
                    if response.json().get('description') == 'Bad Request: file must be non-empty':
                        return False
                else:
                    time.sleep(self.interval)

            except (HTTPSConnectionPool, NewConnectionError) as e:
                print(f"|WARNING| Impossible to send: {data}. Error: {e}\n timeout: 20 sec")
                time.sleep(self.interval)
                return False

            finally:
                _max_attempts -= 1

    def _get_url(self, mode: str) -> str:
        return f"{self.tg_host}/bot{self.auth.token}/{mode}"

    @staticmethod
    def _get_proxies(proxy: Proxy = None, proxy_file: "True | str" = None) -> dict:
        if isinstance(proxy, Proxy):
            return proxy.configs
        return ProxyFile(proxy_file).get_configs()
