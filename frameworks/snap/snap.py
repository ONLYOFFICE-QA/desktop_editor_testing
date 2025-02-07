# -*- coding: utf-8 -*-
from subprocess import call, getoutput
from rich import print

from .snap_commands import SnapCommands
from ..test_exceptions import TestException


class SnapException(TestException): ...

class Snap:

    def __init__(self):
        self.cmd = SnapCommands()

    def install(self):
        if self.is_installed():
            if not self.snapd_service_id_active():
                print("[cyan]|INFO| Start snapd service")
                self.start_snapd_service()

            return print(f"[cyan]|INFO| Snap already installed and running")

        print('|INFO|[green] installing snap...')
        for command in self.cmd.install_commands:
            self._run_cmd(command)

        if not self.is_installed() and not self.snapd_service_id_active():
            raise SnapException("Failed install snap..")

    def is_installed(self) -> bool:
        return self.out_snap_version() == 0

    def out_snap_version(self) -> int:
        return self._run_cmd(self.cmd.version)

    def snapd_service_id_active(self) -> bool:
        return self._get_output("systemctl is-active snapd").lower() == 'active'

    def start_snapd_service(self) -> None:
        self._run_cmd("sudo systemctl start snapd")

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)

    @staticmethod
    def _get_output(cmd: str) -> str:
        return getoutput(cmd)
