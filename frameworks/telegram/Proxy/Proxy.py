# -*- coding: utf-8 -*-
from rich import print
from .ProxyChecker import ProxyChecker



class Proxy:
    def __init__(self, login: str, password: str, ip: str, port: str):
        self.login = login
        self.password = password
        self.ip = ip
        self.port = port

    @property
    def configs(self) -> dict:
        proxy_url = f"http://{self.login}:{self.password}@{self.ip}:{self.port}"
        proxies = { 'http': proxy_url, 'https': proxy_url }

        if ProxyChecker.check(proxies):
            return proxies
        print(f"[red]|ERROR| Unable to access the proxy server. Check configs.")
        return {}
