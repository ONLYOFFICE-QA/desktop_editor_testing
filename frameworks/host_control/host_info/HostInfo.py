# -*- coding: utf-8 -*-
from platform import system, machine, version
from rich import print

from frameworks.decorators.decorators import singleton
from .Unix import Unix


@singleton
class HostInfo:
    def __init__(self):
        self.__os = None
        self.__arch = None
        self.__version = None

    @property
    def os(self) -> str:
        if self.__os is None:
            self.__os = system().lower()
            if self.__os not in ['linux', 'darwin', 'windows']:
                print(f"[bold red]|ERROR| Error defining os: {self.__os}")
                self.__os = ''
        return self.__os

    @property
    def arch(self) -> str:
        if self.__arch is None:
            self.__arch = machine().lower()
        return self.__arch

    def name(self, pretty: bool = False) -> str:
        if self.os == 'windows':
            return f"{self.os} {self.version}" if pretty else self.os
        return Unix().pretty_name if pretty else Unix().id

    @property
    def version(self) -> str:
        if self.__version is None:
            if self.os == 'windows':
                self.__version = version()
            else:
                self.__version = Unix().version
        return self.__version
