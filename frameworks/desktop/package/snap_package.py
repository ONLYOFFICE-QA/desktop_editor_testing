# -*- coding: utf-8 -*-
from subprocess import call

from frameworks.snap import Snap


class SnapPackege:
    install_onlyoffice_snap_cmd = "sudo snap install --beta onlyoffice-desktopeditors"

    def __init__(self):
        self.snap = Snap()

    def install(self) -> None:
        self.snap.install()
        self.install_snap_package()

    def install_snap_package(self) -> None:
        self._run_cmd(self.install_onlyoffice_snap_cmd)

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
