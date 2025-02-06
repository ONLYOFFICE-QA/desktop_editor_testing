# -*- coding: utf-8 -*-
from frameworks.host_control import HostInfo
from rich import print
from ..tools import TestTools, TestData


class OpenTest:

    def __init__(self, test_data: TestData):
        self.data = test_data
        self.test_tools = TestTools(test_data=self.data)

    def run(self):
        print(f"[green]|INFO| Open test is running...")
        self.update_desktop() if self.test_tools.old_desktop else self.install_desktop()
        self.test_tools.check_installed()
        self.test_tools.check_correct_version()
        self.test_tools.desktop.set_license()
        self.test_tools.check_open_desktop()
        self.test_tools.check_open_files(self.data.path.good_files_dir)
        self.test_tools.write_results(f'Passed')
        self.test_tools.display.stop() if self.test_tools.virtual_display else ...

    def install_desktop(self):
        self.test_tools.install_package(
            self.test_tools.desktop,
            custom_installer='rpm -Uvh' if HostInfo().name().lower() in ['opensuse'] else None
        )

    def update_desktop(self):
        self.test_tools.install_package(
            self.test_tools.old_desktop,
            custom_installer='rpm -i' if HostInfo().name().lower() in ['opensuse'] else None
        )
        self.install_desktop()
