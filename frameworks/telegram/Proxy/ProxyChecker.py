# -*- coding: utf-8 -*-
from requests import post
from requests.exceptions import RequestException

from ..utils import Str
from ..config import Config


class ProxyChecker:
    """
    Utility class to check the validity of HTTP proxies.

    Uses a caching mechanism to store previously checked proxies.

    :param proxies: Dictionary containing 'http' and 'https' URLs of the proxy server.
    :return: True if the proxy is reachable, False otherwise.
    """
    _checked_proxies = {}

    @staticmethod
    def check(proxies: dict) -> bool:
        """
        Checks if the specified proxy server is reachable.

        :param proxies: Dictionary containing 'http' and 'https' URLs of the proxy server.
        :return: True if the proxy is reachable, False otherwise.
        """
        proxy_key = frozenset(proxies.items())

        if proxy_key in ProxyChecker._checked_proxies:
            return ProxyChecker._checked_proxies[proxy_key]

        try:
            post(f"{Str.delete_last_slash(Config.API_HOST)}/", proxies=proxies)
            result = True
        except RequestException:
            result = False

        ProxyChecker._checked_proxies[proxy_key] = result
        return result
