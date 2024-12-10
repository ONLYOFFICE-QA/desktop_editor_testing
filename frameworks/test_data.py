# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from os import getcwd
from os.path import join


from frameworks.host_control import FileUtils

dataclass(frozen=True)
class TestData:
    project_dir: str = getcwd()
    tmp_dir: str = join(project_dir, 'tmp')
    reports_dir: str = join(project_dir, 'reports')
    test_assets: str = join(project_dir, 'tests', 'assets')
    img_template: str = join(test_assets, 'image_template')
    bad_files_dir: str = join(test_assets, 'bad_files')
    good_files_dir: str = join(test_assets, 'good_files')
    lic_file_path: str = join(test_assets, 'test_lic.lickey')
    config: json = FileUtils.read_json(join(project_dir, 'config.json'))
    cache_dir: str = config.get("cache_dir", None)
    warning_window_info: str = join(test_assets, "warning_window_info.json")
