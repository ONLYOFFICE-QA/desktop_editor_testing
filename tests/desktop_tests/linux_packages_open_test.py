# -*- coding: utf-8 -*-
from frameworks.snap.snap import SnapException
from frameworks.test_exceptions import TestException, AppImageException, FlatPakException
from rich import print
from ..tools import TestData, TestTools


class LinuxPackagesOpenTest:

    def __init__(self, test_data: TestData):
        self.data = test_data
        self.test_tools = TestTools(test_data=self.data)
        self.package_name = self.test_tools.desktop.package.name

    def run(self):
        print(f"[green]|INFO| {self.package_name} package test running...")
        self.install_desktop()
        self.test_tools.check_correct_version()
        self.test_tools.check_open_desktop()
        self.test_tools.check_open_files(self.data.path.good_files_dir)
        self.test_tools.write_results(f'Passed')
        self.test_tools.display.stop() if self.test_tools.virtual_display else ...

    def install_desktop(self):
        if self.test_tools.is_windows:
            raise TestException(f"Unable to install {self.package_name} package on windows")

        try:
            self.test_tools.desktop.package.install()
        except (SnapException, AppImageException, FlatPakException):
            self.test_tools.write_results(f"{self.package_name.upper()} INSTALL ERROR")

    def update_desktop(self) -> None:
        raise TestException(f"The {self.package_name} packege update is not supported")
