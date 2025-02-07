# -*- coding: utf-8 -*-
from dataclasses import dataclass
from os.path import join, dirname, realpath

from frameworks.host_control import FileUtils, HostInfo


@dataclass
class SnapCommands:

    def __post_init__(self):
        self.commands: dict = FileUtils.read_json(join(dirname(realpath(__file__)), 'commands.json'))
        self._host = HostInfo()
        self.host_name = HostInfo().name().lower()
        self.install_commands: list = self._get_install_commands()
        self.version: str = "snap --version"

    def _get_install_commands(self) -> list:
        return self.commands.get(self._get_os_family(), [])

    def _get_os_family(self) -> str:
        _key = f"{self._host.name()} {self._host.version}"
        print(f"SnapPackage KEY: {_key}")  # TODO

        for os_family, distributions in self.commands['os_family'].items():
            if self.host_name in distributions:
                return os_family

        raise ValueError(
            f"[red]|ERROR| Can't verify os family for download desktop package.\n"
            f"host name: {self._host.name()}\n"
            f"version: {self._host.version}"
        )
