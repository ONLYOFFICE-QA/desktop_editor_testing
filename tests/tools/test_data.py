# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass, field
from os.path import join, isfile
from frameworks.host_control import FileUtils

from .paths import Paths


@dataclass
class TestData:
    version: str
    update_from: str = None
    custom_config: str = None
    virtual_display: bool = True
    telegram: bool = False
    config: json = field(init=False)
    path: Paths = Paths()
    license_file_path: str = join(path.test_assets, 'test_lic.lickey')
    snap_package: bool = False
    appimage_package: bool = False
    flatpak_package: bool = False

    def __post_init__(self):
        self.tmp_dir = self.path.tmp_dir
        self.config: json = self._read_config()
        self.cache_dir: str = self.config.get("cache_dir", None)
        self._check_package_options()

    def _read_config(self) -> json:
        if self.custom_config and isfile(self.custom_config):
            return FileUtils.read_json(self.custom_config)
        return FileUtils.read_json(join(self.path.project_dir, 'config.json'))

    def _check_package_options(self):
        if sum([self.snap_package, self.appimage_package, self.flatpak_package]) > 1:
            raise ValueError("Only one option from snap, appimage, flatpak should be enabled..")
