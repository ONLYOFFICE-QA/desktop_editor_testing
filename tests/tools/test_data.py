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
    snap: bool = False
    appimage: bool = False

    def __post_init__(self):
        self.config: json = self._read_config()
        self.cache_dir: str = self.config.get("cache_dir", None)

    def _read_config(self) -> json:
        if self.custom_config and isfile(self.custom_config):
            return FileUtils.read_json(self.custom_config)
        return FileUtils.read_json(join(self.path.project_dir, 'config.json'))
