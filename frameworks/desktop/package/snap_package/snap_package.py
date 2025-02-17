# -*- coding: utf-8 -*-
from os.path import dirname, realpath, join
from subprocess import call

from frameworks.host_control import FileUtils
from frameworks.snap import Snap
from ..package import Package


class SnapPackage(Package):
    config = FileUtils.read_json(join(dirname(realpath(__file__)), "snap_config.json"))

    def __init__(self):
        self.snap = Snap()

    @property
    def name(self) -> str:
        return "Snap"

    def install(self) -> None:
        self.snap.install()
        self.install_snap_package()

    def install_snap_package(self) -> None:
        self._run_cmd(self.config["install_snap_cmd"])

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
