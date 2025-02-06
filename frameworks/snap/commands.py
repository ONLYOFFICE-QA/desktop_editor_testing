# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class SnapCommands:
    snap: str = 'snap'
    snap_core: str = f'sudo {snap} install core'
    version: str = f"snap version"

    def __post_init__(self):
        self.run_snapd_service: list = self.get_snapd_service_run_cmd()
        self.installer = self._get_os_installer()
        self.install_snapd = f"{self.installer} install -y snapd"

    def _get_os_installer(self) -> str:
        return "sudo apt-get"

    def get_snapd_service_run_cmd(self):
        return  ["sudo systemctl enable --now snapd", "sudo systemctl start snapd"]
