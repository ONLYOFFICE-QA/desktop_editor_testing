# -*- coding: utf-8 -*-
from platform import system, machine, version
from rich import print

from frameworks.decorators.decorators import singleton
from .Unix import Unix


@singleton
class HostInfo:
    def __init__(self):
        self.os = system().lower()
        self.__arch = machine().lower()

    def name(self, pretty: bool = False) -> "str | None":
        if self.os == 'windows':
            return self.os
        return Unix().pretty_name if pretty else Unix().id

    @property
    def version(self) -> "str | None":
        return version() if self.os == 'windows' else Unix().version

    @property
    def os(self):
        return self.__os

    @property
    def arch(self):
        return self.__arch

    @os.setter
    def os(self, value):
        if value == 'linux':
            self.__os = 'linux'
        elif value == 'darwin':
            self.__os = 'mac'
        elif value == 'windows':
            self.__os = 'windows'
        else:
            print(f"[bold red]|WARNING| Error defining os: {value}")
