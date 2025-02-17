# -*- coding: utf-8 -*-
from subprocess import getoutput, call

from .command import Commands
from ..decorators import retry


class FlatPakInstaller:

    def __init__(self):
        self.cmd = Commands()

    @retry(max_attempts=3, interval=2)
    def install(self):
        if self.is_installed():
            return print(f"[cyan]|INFO| FlatPak already installed")

        print('|INFO|[green] installing FlatPak...')
        for command in self.cmd.install_commands:
            self._run_cmd(command)

    def is_installed(self) -> bool:
        return self.out_flatpak_version() == 0

    def out_flatpak_version(self) -> int:
        return self._run_cmd(self.cmd.version)

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)

    @staticmethod
    def _get_output(cmd: str) -> str:
        return getoutput(cmd)
