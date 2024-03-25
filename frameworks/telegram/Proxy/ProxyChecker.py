# -*- coding: utf-8 -*-
from requests import post
from requests.exceptions import RequestException


class ProxyChecker:
    _checked_proxies = {}

    @staticmethod
    def check(proxies: dict) -> bool:
        proxy_key = frozenset(proxies.items())

        if proxy_key in ProxyChecker._checked_proxies:
            return ProxyChecker._checked_proxies[proxy_key]

        try:
            post('https://api.telegram.org/', proxies=proxies)
            result = True
        except RequestException:
            result = False

        ProxyChecker._checked_proxies[proxy_key] = result

        return result
