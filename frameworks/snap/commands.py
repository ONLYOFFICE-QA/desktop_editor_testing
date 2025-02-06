# -*- coding: utf-8 -*-
from dataclasses import dataclass
from os.path import join, dirname, realpath

from frameworks.host_control import FileUtils, HostInfo


@dataclass
class SnapCommands:
    commands: dict = FileUtils.read_json(join(dirname(realpath(__file__)), 'commands.json'))

    def __post_init__(self):
        self._host = HostInfo()
        self.install_commands: list = self._get_install_commands()
        self.version: str = "snap --version"

    def _get_install_commands(self) -> list:
        return self.commands.get(f"{self._host.os} {self._host.release}", [])
