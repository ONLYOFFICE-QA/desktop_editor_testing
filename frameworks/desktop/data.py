# -*- coding: utf-8 -*-
from typing import NamedTuple

class Data(NamedTuple):
    version: str
    tmp_dir: str
    cache_dir: str = None
    custom_config_path: str = None
    lic_file: str = None
    debug_mode: bool = False
