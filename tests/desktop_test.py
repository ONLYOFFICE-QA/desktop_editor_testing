# -*- coding: utf-8 -*-
import re
import time
from os.path import join, basename
from subprocess import Popen

from rich import print
from rich.console import Console
from pyvirtualdisplay import Display

from frameworks.desktop import DesktopEditor, DesktopData
from frameworks.StaticData import StaticData
from frameworks.host_control import FileUtils, HostInfo
from frameworks.image_handler import Image
from tests.tools.desktop_report import DesktopReport
console = Console()

class TestException(Exception): ...

class DesktopTest:
    def __init__(
            self,
            version: str,
            custom_config: str = None,
            display_on: bool = True,
            telegram: bool = False,
            license_file_path: str = None
    ):
        self.config = FileUtils.read_json(custom_config) if custom_config else StaticData.config
        self.telegram_report = telegram
        self.version = version
        self.display_on = display_on
        self._create_display()
        self.report = DesktopReport(self._report_path())
        self.host_name = re.sub(r"[\s/]", "", HostInfo().name(pretty=True))
        self.img_dir = StaticData.img_template
        self.bad_files = StaticData.bad_files_dir
        self.good_files = StaticData.good_files_dir
        self.desktop = self._create_desktop(custom_config, license_file_path)
        FileUtils.create_dir(self.report.dir, stdout=False)

    def run(self):
        self._install_package()
        self.check_installed()
        self.check_correct_version()
        self.desktop.set_license()
        self.wait_until_open(self.desktop.open(), '[DesktopEditors]: start page loaded')
        self.check_open_files()
        self._write_results(f'Passed')
        self.desktop.close()
        self.display.stop() if self.display_on else ...

    def check_open_files(self):
        for file in FileUtils.get_paths(self.good_files):
            if basename(file) in self.config.get('exception_files') if self.config.get('exception_files') else []:
                print(f"[green]|INFO| File `{basename(file)}` skipped to open.")
                continue
            print(f"[green]|INFO| Test opening file: {basename(file)}")
            self.desktop.open(file)
            time.sleep(25) # TODO
            self.check_error_on_screen()
            Image.make_screenshot(f"{join(self.report.dir, f'{self.version}_{self.host_name}_{basename(file)}.png')}")

    def check_error_on_screen(self):
        for error_img in FileUtils.get_paths(join(self.img_dir, 'errors')):
            if Image.is_present(error_img):
                Image.make_screenshot(f"{join(self.report.dir, f'{self.version}_{self.host_name}_error_screen.png')}")
                self._write_results('ERROR')
                raise TestException(f"[red]|ERROR| An error has been detected.")

    def wait_until_open(self, process: Popen, wait_msg: str, timeout: int = 30):
        start_time = time.time()
        with console.status('') as status:
            while time.time() - start_time < timeout:
                status.update(f'[green]|INFO| Wait until the editor opens')
                output = process.stdout.readline().decode().strip()
                if output:
                    console.print(f"[cyan]|INFO| {output}")
                    if wait_msg in output:
                        print(f"[green]|INFO| Opened.")
                        self.check_error_on_screen()
                        break
            else:
                self._write_results('NOT_OPENED')
                raise TestException("[red]|ERROR| Can't open desktop editor")
            Image.make_screenshot(f"{join(self.report.dir, f'{self.version}_{self.host_name}_open_editor.png')}")

    def check_installed(self):
        installed_version = self.desktop.version()
        if self.version != installed_version:
            self._write_results('NOT_INSTALLED')
            raise TestException(
                f"[bold red]|ERROR| Desktop not installed. "
                f"Current version: {installed_version}"
            )

    def check_correct_version(self):
        version =  self.desktop.version()
        if len([i for i in version.split('.') if i]) != 4:
            self._write_results('INCORRECT_VERSION')
            raise TestException(f"[red]|ERROR| The version is not correct: {version}")

    def _write_results(self, exit_code: str):
        self.report.write(
            os=HostInfo().name(pretty=True),
            version=self.version,
            package_name=self.desktop.package.name,
            exit_code=exit_code,
            tg_msg=self.telegram_report
        )

    def _install_package(self):
        if self.version == self.desktop.version():
            print(f'[green]|INFO| Desktop version: {self.version} already installed[/]')
            return
        self.desktop.package.get()

    def _create_display(self, visible: bool = False, size: tuple = (1920, 1080)):
        if self.display_on:
            self.display = Display(visible=visible, size=size)
            self.display.start()
        else:
            print("[red]|INFO| Test running without virtual display")

    def _create_desktop(self, custom_config: str, license_file_path: str):
        return DesktopEditor(
            DesktopData(
                version=self.version,
                tmp_dir=StaticData.tmp_dir,
                debug_mode=True,
                custom_config_path=custom_config,
                lic_file=license_file_path if license_file_path else StaticData.lic_file_path,
                cache_dir=StaticData.cache_dir
            )
        )

    def _report_path(self):
        title = self.config.get('title')
        return join(StaticData.reports_dir, title, self.version, f"{self.version}_{title}_report.csv")
