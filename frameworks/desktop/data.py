# -*- coding: utf-8 -*-
import tempfile
from dataclasses import dataclass


@dataclass
class Data:
    version: str
    tmp_dir: str = tempfile.gettempdir()
    cache_dir: str = None
    custom_config_path: str = None
    lic_file: str = None
    snap_package: bool = False
    appimage_package: bool = False
    flatpak_package: bool = False
