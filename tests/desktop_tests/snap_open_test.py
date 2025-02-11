# -*- coding: utf-8 -*-
from frameworks.snap.snap import SnapException
from frameworks.test_exceptions import TestException
from rich import print
from ..tools import TestData, TestTools


class SnapOpenTest:

    def __init__(self, test_data: TestData):
        self.data = test_data
        self.test_tools = TestTools(test_data=self.data)

    def run(self):
        print(f"[green]|INFO| Snap package test running...")
        self.install_desktop()
        self.test_tools.check_correct_version()
        self.test_tools.check_open_desktop()
        self.test_tools.check_open_files(self.data.path.good_files_dir)
        self.test_tools.write_results(f'Passed')
        self.test_tools.display.stop() if self.test_tools.virtual_display else ...

    def install_desktop(self):
        if self.test_tools.is_windows:
            raise TestException("Unable to install snap package on windows")

        try:
            self.test_tools.desktop.snap_package.install()
        except SnapException:
            self.test_tools.write_results("SNAP INSTALL ERROR")

    def update_desktop(self) -> None:
        raise TestException("The snap packege update is not supported")
