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
        self.update_os_dependencies()
        self.install_snap_dependencies()
        self.install_snapd()
        self.run_snapd_service()
        self.install_snap_core()

    def run_snapd_service(self):
        for cmd in self.cmd.run_snapd_service:
            self._run_cmd(cmd)

    def install_snapd(self):
        self._run_cmd(self.cmd.install_snapd)

    def install_snap_core(self):
        self._run_cmd(self.cmd.snap_core)

    def install_snap_dependencies(self):
        self._run_cmd(f"{self.cmd.installer} install -y sudo coreutils")

    def update_os_dependencies(self):
        self._run_cmd(f"{self.cmd.installer} update")

    def is_installed(self) -> bool:
        return self.out_snap_version() == 0

    def out_snap_version(self) -> int:
        return self._run_cmd(self.cmd.version)

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
