# -*- coding: utf-8 -*-
from dataclasses import dataclass
from os import getcwd
from os.path import join


@dataclass(frozen=True)
class Paths:
    project_dir: str = getcwd()
    tmp_dir: str = join(project_dir, 'tmp')
    reports_dir: str = join(project_dir, 'reports')
    test_assets: str = join(project_dir, 'tests', 'assets')
    img_template: str = join(test_assets, 'image_template')
    bad_files_dir: str = join(test_assets, 'bad_files')
    good_files_dir: str = join(test_assets, 'good_files')
    warning_window_info: str = join(test_assets, "warning_window_info.json")
    error_img_dir: str = join(img_template, 'errors')
