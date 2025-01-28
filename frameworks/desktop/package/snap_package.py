# -*- coding: utf-8 -*-
from subprocess import call

class SnapPackege:

    def install(self) -> None:
        call(self._get_install_cmd(), shell=True)

    @staticmethod
    def _get_install_cmd() -> str:
        return "snap install --beta onlyoffice-desktopeditors"
