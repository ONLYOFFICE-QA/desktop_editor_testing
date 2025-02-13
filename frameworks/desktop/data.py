# -*- coding: utf-8 -*-
import tempfile
from dataclasses import dataclass


@dataclass
class Data:
    version: str
    tmp_dir: str = tempfile.gettempdir()
    cache_dir: str = None
    custom_config: str = None
    license_file_path: str = None
    snap_package: bool = False
    appimage_package: bool = False
    flatpak_package: bool = False

    def __post_init__(self):
        self.specific_packages: list = [self.snap_package, self.appimage_package, self.flatpak_package]
        self._check_package_options()

    def _check_package_options(self):
        if sum(self.specific_packages) > 1:
            raise ValueError("Only one option from snap, appimage, flatpak should be enabled..")

    def is_default_package(self) -> bool:
        return not any(self.specific_packages)
