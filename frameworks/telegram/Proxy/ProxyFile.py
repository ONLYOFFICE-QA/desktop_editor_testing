# -*- coding: utf-8 -*-
from rich import print
from os.path import join, expanduser, isfile
from typing import Optional

from .Proxy import Proxy
from ..utils import File


class ProxyFile:
    """
    Manages proxy configurations from JSON files.

    Handles loading and validating proxy configurations from a default or specified JSON file path.

    :param path: Optional. Path to the JSON file containing proxy configurations.
    """

    _checked_files = {}
    _checked_paths = {}
    _default_proxy_file = join(expanduser('~'), '.telegram', 'proxy.json')

    def __init__(self, path: Optional[str] = None):
        self._proxy_file = self._get_proxy_file(path)


    def _get_proxy_file(self, path: Optional[str] = None) -> Optional[str]:
        """
        Retrieves the path to the proxy configuration JSON file.

        If a specific path is provided, it checks if the file exists. Otherwise, it defaults to a predefined location.

        :param path: Optional. Path to the JSON file containing proxy configurations.
        :return: Path to the proxy configuration file, or None if not found.
        """

        file_key = path if path else 'None'

        if file_key in self._checked_paths:
            return self._checked_paths[file_key]

        if path and isinstance(path, str) and isfile(path):
            result = path
        elif isfile(self._default_proxy_file):
            result = self._default_proxy_file
        else:
            print(f"[red]Proxy configuration file not found")
            result = None

        self._checked_paths[file_key] = result

        return result

    def get_configs(self) -> dict:
        """
        Retrieves proxy configurations from the loaded JSON file.

        Reads the JSON file, validates the configuration, and returns proxy configurations as a dictionary.

        :return: Dictionary containing proxy configurations ('http' and 'https' URLs).
        """

        result = {}
        file_key = self._proxy_file if self._proxy_file else 'None'

        if file_key in self._checked_files:
            return self._checked_files[file_key]

        if self._proxy_file:
            config = File.read_json(self._proxy_file)
            if self._check_config(config):
                proxy = Proxy(login=config['login'], password=config['password'], ip=config['ip'], port=config['port'])
                result = proxy.configs

        self._checked_files[file_key] = result

        return result

    @staticmethod
    def _check_config(config: dict) -> bool:
        """
        Validates the proxy configuration dictionary.

        Checks if the required keys ('login', 'password', 'ip', 'port') are present and not empty.

        :param config: Dictionary containing proxy configuration parameters.
        :return: True if the configuration is valid, False otherwise.
        """

        for key in ['login', 'password', 'ip', 'port']:
            if not config.get(key, None):
                print(f"[red]|ERROR| Empty parameter {key} in proxy.json file")
                return False
        return True
