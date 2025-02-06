# -*- coding: utf-8 -*-
from dataclasses import dataclass
from os.path import join, dirname, realpath

from frameworks.host_control import FileUtils, HostInfo


@dataclass
class SnapCommands:

    def __post_init__(self):
        self.commands: dict = FileUtils.read_json(join(dirname(realpath(__file__)), 'commands.json'))
        self._host = HostInfo()
        self.install_commands: list = self._get_install_commands()
        self.version: str = "snap --version"

    def _get_install_commands(self) -> list:
        _key = f"{self._host.name()} {self._host.version}"
        print(f"SnapPackage KEY: {_key}") #TODO
        return self.commands.get(f"{self._host.os} {self._host.release}", [])
