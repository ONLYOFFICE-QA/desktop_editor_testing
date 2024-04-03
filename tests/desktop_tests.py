# -*- coding: utf-8 -*-
import re
import time
from os.path import join, basename
from subprocess import Popen

from rich import print
from pyvirtualdisplay import Display

from frameworks.desktop import DesktopEditor, DesktopData, DesktopException, UrlException, PackageException
from frameworks.test_data import TestData
from frameworks.host_control import FileUtils, HostInfo
from frameworks.image_handler import Image
from tests.tools.desktop_report import DesktopReport


class TestException(Exception): ...


class DesktopTests:
    def __init__(
            self,
            version: str,
            update_from: str = None,
            custom_config: str = None,
            virtual_display: bool = True,
            telegram: bool = False,
            license_file_path: str = None,
    ):
        self.config = FileUtils.read_json(custom_config) if custom_config else TestData.config
        self.telegram_report = telegram
        self.version = version
        self.update_from = update_from
        self.virtual_display = virtual_display
        self._create_display()
        self.host_name = re.sub(r"[\s/]", "", HostInfo().name(pretty=True))
        self.report = DesktopReport(self._report_path())
        self.img_dir = TestData.img_template
        self.bad_files = TestData.bad_files_dir
        self.good_files = TestData.good_files_dir
        self.desktop = self._create_desktop(self.version, custom_config, license_file_path)
        self.old_desktop = self._create_desktop(update_from, custom_config, license_file_path) if update_from else None
        FileUtils.create_dir(self.report.dir, stdout=False)

    def open_test(self):
        if self.update_from:
            self.install_package(
                self.update_from,
                self.old_desktop,
                yum_installer=True,
                custom_installer='rpm -i' if HostInfo().name().lower() in ['opensuse'] else None
            )
        self.install_package(
            self.version,
            self.desktop,
            yum_installer=True if self.update_from else False,
            custom_installer='rpm -Uvh' if HostInfo().name().lower() in ['opensuse'] else None
        )
        self.check_installed()
        self.check_correct_version()
        self.desktop.set_license()
        self.check_open_desktop(self.desktop.open(log_out_mode=True), '[DesktopEditors]: start page loaded')
        self.check_open_files(self.good_files)
        self._write_results(f'Passed')
        self.display.stop() if self.virtual_display else ...

    def check_open_files(self, files_dir: str):
        for file in FileUtils.get_paths(files_dir):
            if basename(file) in self.config.get('exception_files', []):
                print(f"[green]|INFO| File `{basename(file)}` skipped to open.")
                continue
            print(f"[green]|INFO| Test opening file: {basename(file)}")
            self.desktop.open(file, log_out_mode=True)
            time.sleep(15)  # TODO
            self.check_error_on_screen()
            Image.make_screenshot(f"{join(self.report.dir, f'{self.version}_{self.host_name}_{basename(file)}.png')}")

    def check_open_desktop(self, stdout_process: Popen, wait_msg: str, timeout: int = 30):
        try:
            self.desktop.wait_until_open(stdout_process, wait_msg, timeout=timeout)
            time.sleep(1)  # todo
            self.check_error_on_screen()
            Image.make_screenshot(f"{join(self.report.dir, f'{self.version}_{self.host_name}_open_editor.png')}")
        except DesktopException:
            self._write_results('NOT_OPENED')
            raise TestException("[red]|ERROR| Can't open desktop editor")

    def check_installed(self):
        installed_version = self.desktop.get_version()
        if self.version != installed_version:
            self._write_results('NOT_INSTALLED')
            raise TestException(
                f"[bold red]|ERROR| Desktop not installed. "
                f"Current version: {installed_version}"
            )

    def check_correct_version(self):
        version = self.desktop.get_version()
        if len([i for i in version.split('.') if i]) != 4:
            self._write_results('INCORRECT_VERSION')
            raise TestException(f"[red]|ERROR| The version is not correct: {version}")

    def check_error_on_screen(self):
        for error_img in FileUtils.get_paths(join(self.img_dir, 'errors')):
            if Image.is_present(error_img):
                Image.make_screenshot(join(self.report.dir, f'{self.version}_{self.host_name}_error_screen.png'))
                self._write_results('ERROR')
                raise TestException(f"[red]|ERROR| An error has been detected.")

    def install_package(
            self,
            version: str,
            desktop: DesktopEditor,
            yum_installer: bool = False,
            apt_get_installer: bool = False,
            custom_installer: str = None
    ) -> None:
        if version == desktop.get_version():
            return print(f'[green]|INFO| Desktop version: {self.version} already installed[/]')
        try:
            desktop.package.get()
            desktop.package.install(
                yum_installer=yum_installer,
                apt_get_installer=apt_get_installer,
                custom_installer=custom_installer
            )
        except (UrlException, PackageException) as e:
            self._write_results('CANT_GET_PACKAGE')
            raise TestException(f"[red]|ERROR| Can't get the desktop package. Error: {e}")

    def _write_results(self, exit_code: str):
        self.report.write(
            os=HostInfo().name(pretty=True),
            version=self.version,
            package_name=self.desktop.package.name,
            exit_code=exit_code,
            tg_msg=self.telegram_report
        )

    def _create_display(self, visible: bool = False, size: tuple = (1920, 1080)):
        if self.virtual_display:
            print("[green]|INFO| The test is running on the virtual display")
            self.display = Display(visible=visible, size=size)
            self.display.start()

    @staticmethod
    def _create_desktop(version: str, custom_config: str, license_file_path: str):
        return DesktopEditor(
            DesktopData(
                version=version,
                tmp_dir=TestData.tmp_dir,
                custom_config_path=custom_config,
                lic_file=license_file_path if license_file_path else TestData.lic_file_path,
                cache_dir=TestData.cache_dir
            )
        )

    def _report_path(self):
        title = self.config.get('title', 'Undefined_title')
        return join(TestData.reports_dir, title, self.version, f"{self.version}_{title}_report.csv")
