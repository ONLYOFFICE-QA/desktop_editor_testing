# -*- coding: utf-8 -*-
from dataclasses import dataclass
from os.path import join, dirname, realpath

from frameworks.host_control import FileUtils, HostInfo


@dataclass
class SnapCommands:

    def __post_init__(self):
        self.commands: dict = FileUtils.read_json(join(dirname(realpath(__file__)), 'install_commands.json'))
        self._host = HostInfo()
        self.host_name = self._host.name().lower()
        self.version: str = "snap --version"

    @property
    def install_commands(self) -> list:
        return self.commands.get(self._get_os_family(), [])

    def _get_os_family(self) -> str:
        for os_family, distributions in self.commands['os_family'].items():
            if self.host_name in distributions:
                return os_family

        raise ValueError(
            f"[red]|ERROR| Can't verify os family for download desktop package.\n"
            f"host name: {self.host_name}\n"
            f"version: {self._host.version}"
        )
