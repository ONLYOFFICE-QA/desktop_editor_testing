# -*- coding: utf-8 -*-
from os import environ
from os.path import isfile, join, expanduser

from ..utils import File


class Auth:
    """
    Manages authentication credentials for interacting with the Telegram API.

    :param token: Telegram bot token. If not provided, attempts to retrieve from the 'token' file or environment variable 'TELEGRAM_TOKEN'.
    :param chat_id: ID of the chat or channel. If not provided, attempts to retrieve from the 'chat' file or environment variable 'CHANNEL_ID'.
    """

    def __init__(self, token: str = None, chat_id: str = None):
        self._telegram_dir = join(expanduser('~'), '.telegram')
        self.token = token if token else self._get_token()
        self.chat_id = chat_id if chat_id else self._get_chat_id()

    def _get_token(self) -> "str | None":
        """
        Retrieves the Telegram bot token from the 'token' file or environment variable 'TELEGRAM_TOKEN'.

        :return: Telegram bot token.
        """
        token_file = join(self._telegram_dir, 'token')

        if token_file and isfile(token_file):
            return File.read(token_file).strip()
        elif environ.get('TELEGRAM_TOKEN', False):
            return environ.get('TELEGRAM_TOKEN')

        print(f"[cyan]|INFO| Telegram token not exists.")

    def _get_chat_id(self) -> "str | None":
        """
        Retrieves the chat or channel ID from the 'chat' file or environment variable 'CHANNEL_ID'.

        :return: Chat ID.
        """
        chat_id_file = join(self._telegram_dir, 'chat')

        if isfile(chat_id_file):
            return File.read(chat_id_file).strip()
        elif environ.get('CHANNEL_ID', False):
            return environ.get('CHANNEL_ID')

        print(f"[cyan]|INFO| Telegram chat id not exists.")
