# -*- coding: utf-8 -*-
from frameworks.test_exceptions import AppImageException, TestException
from ..tools import TestTools, TestData


class AppImageOpenTest:

    def __init__(self, test_data: TestData):
        self.data = test_data
        self.test_tools = TestTools(test_data=self.data)

    def run(self):
        print(f"[green]|INFO| AppImage open test is running...")
        self.install()
        self.test_tools.check_correct_version()
        self.test_tools.check_open_desktop()
        self.test_tools.check_open_files(self.data.path.good_files_dir)
        self.test_tools.write_results(f'Passed')
        self.test_tools.display.stop() if self.test_tools.virtual_display else ...

    def install(self) -> None:
        if self.test_tools.is_windows:
            raise TestException("Unable to install snap package on windows")

        try:
            self.test_tools.desktop.appimage.get()
        except AppImageException:
            self.test_tools.write_results("APPIMAGE GET ERROR")
