# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from os import getcwd
from os.path import join


from frameworks.host_control import FileUtils

dataclass(frozen=True)
class StaticData:
    project_dir: str = getcwd()
    tmp_dir: str = join(project_dir, 'tmp')
    reports_dir: str = join(project_dir, 'reports')
    img_template: str = join(project_dir, 'tests', 'assets', 'image_template')
    bad_files_dir: str = join(project_dir, 'tests', 'assets', 'bad_files')
    good_files_dir: str = join(project_dir, 'tests', 'assets', 'good_files')
    lic_file_path: str = join(project_dir, 'tests', 'assets', 'test_lic.lickey')
    config: json = FileUtils.read_json(join(project_dir, 'config.json'))
    cache_dir: str = config.get("cache_dir", None)
