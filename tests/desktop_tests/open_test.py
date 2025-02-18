# -*- coding: utf-8 -*-
from frameworks.host_control import HostInfo
from frameworks.test_exceptions import TestException, AppImageException, FlatPakException, SnapException
from rich import print
from ..tools import TestTools, TestData, DesktopReport


class OpenTest:

    def __init__(self, test_data: TestData):
        self.data = test_data
        self.test_tools = TestTools(test_data=self.data)
        self.package_name = self.test_tools.desktop.package.name
        self.is_default_package = self.test_tools.desktop.data.is_default_package()

    def run(self):
        print(f"[green]|INFO| {self.package_name} package test running...")
        self.install_desktop()
        self.test_tools.check_installed() if self.is_default_package else None
        self.test_tools.check_correct_version()
        self.test_tools.desktop.set_license() if self.is_default_package else None
        self.test_tools.check_open_desktop(retries=self.test_tools.config.open_retries)
        self.test_tools.check_open_files(self.data.path.good_files_dir)
        self.test_tools.write_results(f'Passed')
        self.test_tools.display.stop() if self.test_tools.virtual_display else None

    def install_desktop(self):
        if self.is_default_package:
            return self.test_tools.install_package(
                self.test_tools.desktop,
                custom_installer='rpm -Uvh' if HostInfo().name().lower() in ['opensuse'] else None
            )

        self._install_specific_linux_desktop()


    def _install_specific_linux_desktop(self):
        if self.test_tools.is_windows:
            raise TestException(f"Unable to install {self.package_name} package on windows")

        try:
            self.test_tools.desktop.package.install()
        except (SnapException, AppImageException, FlatPakException):
            self.test_tools.write_results(f"{self.package_name.upper()} INSTALL ERROR")

    def update_desktop(self):
        if not self.is_default_package:
            raise TestException(f"The {self.package_name} packege update is not supported")

        self.test_tools.install_package(
            self.test_tools.old_desktop,
            custom_installer='rpm -i' if HostInfo().name().lower() in ['opensuse'] else None
        )
        self.install_desktop()
