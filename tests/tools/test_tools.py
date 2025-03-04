# -*- coding: utf-8 -*-
import re
import time
from os.path import basename, join
from rich import print

from pyvirtualdisplay import Display

from frameworks.desktop import DesktopException, DesktopEditor, DesktopData, UrlException
from frameworks.host_control import FileUtils, HostInfo, Window
from frameworks.image_handler import Image
from frameworks.test_exceptions import TestException, PackageException

from .desktop_report import DesktopReport
from .test_data import TestData


class TestTools:

    def __init__(self, test_data: TestData):
        self.data = test_data
        self.path = self.data.path
        self.config = self.data.config
        self.desktop = self._create_desktop()
        self.warning_window_info = FileUtils.read_json(self.path.warning_window_info)
        self.old_desktop = self._create_desktop(version=self.data.update_from) if self.data.update_from else None
        self.host_name = re.sub(r"[\s/]", "", HostInfo().name(pretty=True))
        self.desktop_version = None
        self.report = DesktopReport(self.report_path())
        self.error_images = self._get_error_images()
        self.virtual_display: bool = False
        self._create_display()

    @property
    def is_old_windows_version(self) -> bool:
        return HostInfo().release in ['vista', 'xp']

    @property
    def is_windows(self) -> bool:
        return 'windows' == HostInfo().os

    def check_open_files(self, files_dir: str):
        for file in FileUtils.get_paths(files_dir):
            if basename(file) in self.config.get('exception_files', []):
                print(f"[green]|INFO| File `{basename(file)}` skipped to open.")
                continue

            print(f"[green]|INFO| Test opening file: {basename(file)}")
            self.desktop.open(file, log_out_mode=True, stdout=False)
            time.sleep(20)  # TODO
            self._close_warning_window()
            self.check_error_on_screen()
            Image.make_screenshot(
                f"{join(self.report.dir, f'{self.data.version}_{self.host_name}_{basename(file)}.png')}")

    def check_open_desktop(self, retries: int = 5, timeout: int = 30):
        try_num = 1
        try:
            for _try in range(retries):
                process = self.desktop.open(log_out_mode=True)
                self.desktop.wait_until_open(process,'[DesktopEditors]: start page loaded',timeout=timeout)
                time.sleep(1)  # todo
                self._close_warning_window() if not self.is_old_windows_version and self.is_windows else None
                self.check_error_on_screen()
                if try_num == retries:
                    Image.make_screenshot(
                        f"{join(self.report.dir, f'{self.data.version}_{self.host_name}_open_editor_{try_num}.png')}"
                    )

                process.terminate()
                process.wait()
                self.close_desktop()
                try_num += 1

        except DesktopException:
            self.write_results(f'NOT_OPENED_ON_TRY_{try_num}')
            raise TestException(f"[red]|ERROR| Can't open desktop editor on the {try_num}th attempt")

    def close_desktop(self, retries: int = 5, timeout: int = 5):
        for _try in range(retries):
            self.desktop.close()
            if self.desktop.wait_until_close():
                return True
            time.sleep(timeout)

        self.write_results(f'CLOSE_ERROR')
        raise TestException(f"Can't close desktop")

    def check_installed(self):
        installed_version = self.desktop.get_version()
        if self.data.version != installed_version:
            self.write_results('NOT_INSTALLED')
            raise TestException(
                f"[bold red]|ERROR| Desktop not installed. "
                f"Current version: {installed_version}"
            )

    def check_correct_version(self):
        self.desktop_version = self.desktop.get_version()
        if not self.desktop_version or len([i for i in self.desktop_version.split('.') if i]) != 4:
            self.write_results('INCORRECT_VERSION')
            raise TestException(f"[red]|ERROR| The version is not correct: {self.desktop_version}")

    def check_error_on_screen(self):
        if self.is_old_windows_version:
            return print("[cyan]|INFO| OpenCv not supported on this OS")

        print(f"[green]|INFO| Check errors on screen")
        for error_img in self.error_images:
            if Image.is_present(error_img):
                Image.make_screenshot(join(self.report.dir, f'{self.data.version}_{self.host_name}_error_screen.png'))
                self.write_results('ERROR')
                raise TestException(f"[red]|ERROR| An error has been detected.")

    def install_package(
            self,
            desktop: DesktopEditor,
            custom_installer: str = None
    ) -> None:
        if desktop.package.version == desktop.get_version():
            return print(f'[green]|INFO| Desktop version: {self.data.version} already installed[/]')

        try:
            desktop.package.get()
            desktop.package.install(
                yum_installer=True if self.old_desktop else False,
                apt_get_installer=False,
                custom_installer=custom_installer
            )

        except (UrlException, PackageException) as e:
            self.write_results('CANT_GET_PACKAGE')
            raise TestException(f"[red]|ERROR| Can't get the desktop package. Error: {e}")

    def write_results(self, exit_code: str):
        self.report.write(
            os=HostInfo().name(pretty=True),
            version=self.desktop.get_version(),
            package_name=self.desktop.package.name,
            exit_code=exit_code,
            tg_msg=self.data.telegram
        )

    def _create_display(self, visible: bool = False, size: tuple = (1920, 1080)):
        if self.data.virtual_display and HostInfo().os != 'windows':
            print("[green]|INFO| The test is running on the virtual display")
            self.display = Display(visible=visible, size=size)
            self.virtual_display = True
            return self.display.start()

        self.virtual_display = False

    def _create_desktop(self, version: str = None):
        filtered_data = {k: v for k, v in  self.data.__dict__.items() if k in DesktopData.__annotations__.keys()}

        if version:
            filtered_data['version'] = version

        return DesktopEditor(DesktopData(**filtered_data))

    def report_path(self) -> str:
        title = self.config.get('title', 'Undefined_title')
        return join(self.path.reports_dir, title, self.data.version, f"{self.data.version}_{title}_report.csv")

    def _close_warning_window(self) -> None:
        window = Window()

        for info in self.warning_window_info.values():
            window_hwnd = window.get_hwnd(info.get('class_name', ''), info.get('window_text', ''))

            if not window_hwnd:
                continue

            window.close(window_hwnd)

        time.sleep(0.5)

    def _get_error_images(self) -> list:
        return [Image.read(img_path=path) for path in FileUtils.get_paths(self.path.error_img_dir)]
