# -*- coding: utf-8 -*-
from subprocess import call
from rich import print

from frameworks.snap import Snap


class SnapPackege:

    def __init__(self):
        self.snap = Snap()

    def install(self) -> None:
        self.snap.install()
        self._run_cmd(self._get_install_cmd())

    @staticmethod
    def _get_install_cmd() -> str:
        return "snap install --beta onlyoffice-desktopeditors"

    def _run_cmd(self, cmd: str) -> int:
        return call(cmd, shell=True)
