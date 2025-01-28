# -*- coding: utf-8 -*-
from subprocess import call
from rich import print

class SnapPackege:

    def install(self) -> None:
        if not self.snap_is_installed():
            self.install_snap()

        self._run_cmd(self._get_install_cmd())

    @staticmethod
    def _get_install_cmd() -> str:
        return "snap install --beta onlyoffice-desktopeditors"

    def install_snap(self):
        print('[cyan] installing snap...')
        self.update_dependencies()
        self.install_snap_dependencies()
        self._run_cmd('sudo apt install -y snapd')
        self.run_snapd_service()
        self.install_snap_core()

    def run_snapd_service(self):
        for cmd in ["sudo systemctl enable --now snapd", "sudo systemctl start snapd"]:
            self._run_cmd(cmd)

    def install_snap_core(self):
        self._run_cmd('sudo snap install core')

    def install_snap_dependencies(self):
        self._run_cmd("sudo apt install -y sudo coreutils")

    def update_dependencies(self):
        self._run_cmd("sudo apt update")

    def _run_cmd(self, cmd: str) -> int:
        return call(cmd, shell=True)

    def snap_is_installed(self) -> bool:
        return self._run_cmd('snap version') == 0
