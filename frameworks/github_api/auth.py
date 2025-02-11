# -*- coding: utf-8 -*-
from os.path import join, expanduser, isfile

from frameworks.decorators import singleton


@singleton
class Auth:
    default_token_dir = join(expanduser('~'), ".github")
    default_token_path = join(default_token_dir, 'token')

    def __init__(self, token: str = None, token_file_name: str = None):
        self.token = token or self._get_token(token_file_name=token_file_name)

    def _get_token(self, token_file_name: str = None) -> str:
        return self._file_read(
            join(self.default_token_dir, token_file_name) if token_file_name else self.default_token_path
        )

    @staticmethod
    def _file_read(path: str) -> str:
        """
        Read contents of a file.
        :param path: Path of the file to read.
        :return: Contents of the file.
        """
        if not isfile(path):
            raise FileNotFoundError(f"Can't found token file: {path}")

        with open(path, 'r', encoding='utf-8') as file:
            return file.read().strip()
