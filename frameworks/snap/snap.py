# -*- coding: utf-8 -*-
from subprocess import call
from rich import print

from .commands import SnapCommands


class Snap:

    def __init__(self):
        self.cmd = SnapCommands()

    def install(self):
        if self.is_installed():
            return print(f"[cyan]|INFO| Snap already installed")

        print('[cyan] installing snap...')
        for command in self.cmd.install_commands:
            self._run_cmd(command)

    def is_installed(self) -> bool:
        return self.out_snap_version() == 0

    def out_snap_version(self) -> int:
        return self._run_cmd(self.cmd.version)

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
