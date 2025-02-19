# -*- coding: utf-8 -*-
import os
import re
import signal
import time
from os.path import join, dirname, isfile, basename, realpath
from subprocess import Popen, PIPE

import psutil

from frameworks.host_control import HostInfo, FileUtils
from frameworks.test_exceptions import DesktopException
from rich import print
from rich.console import Console

from .package import DefaultPackage, AppImage, SnapPackage, Flatpak
from .data import Data

console = Console()

class DesktopEditor:
    def __init__(self, data: Data):
        self.data = data
        self.lic_file_path = data.license_file_path
        self.config = self._get_config(data.custom_config)
        self.package = self._get_package()
        self.os = HostInfo().os
        self.process_name = ['editors.exe'] if self.os_is_windows() else ['editors', "DesktopEditors"]
        self.debug_command = '--ascdesktop-support-debug-info'
        self.log_out_cmd = self._get_log_out_cmd()

    def open(
            self,
            file_path: str = None,
            debug_mode: bool = False,
            log_out_mode: bool = False,
            stdout: bool = True
    ) -> Popen:
        commands_parts = [
            self._generate_running_command(),
            self.log_out_cmd if log_out_mode else '',
            self.debug_command if debug_mode else '',
            file_path if file_path else ''
        ]

        command = " ".join(filter(None, commands_parts))

        if stdout:
            print(f"[green]|INFO| Open Desktop Editor via command: [cyan]{command}[/]")

        return Popen(command, stdout=PIPE, stderr=PIPE, shell=True)

    def close(self) -> None:
        print(f"[green]|INFO| Try close desktop")
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] in self.process_name:
                pid = proc.info['pid']
                if self.os_is_windows():
                    print(f"[green]|INFO| Sending close signal to {proc.info['name']} (PID: {pid}) on Windows")
                    os.system(f"taskkill /PID {pid}")
                else:
                    print(f"[green]|INFO| Sending SIGTERM to {proc.info['name']} (PID: {pid}) on Linux/macOS")
                    os.kill(pid, signal.SIGTERM)


    def wait_until_close(self, timeout: int = 20, check_interval: float = 0.5) -> bool:
        if HostInfo().name() in ["centos", "redos", "altlinux", "fedora"] and self.data.snap_package:
            # TODO
            return True

        start_time = time.time()
        print(f"[green]|INFO| Wait until close desktop")
        while time.time() - start_time < timeout:
            if not self.check_desktop_proc():
                print(f"[green]|INFO|  The {self.process_name} process has terminated")
                return True

            time.sleep(check_interval)

        print(f"[red]|ERROR| Timeout time ({timeout} sec) has expired, process {self.process_name} has not terminated")
        return False

    def check_desktop_proc(self):
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] in self.process_name:
                return True
        return False

    def wait_until_open(
            self,
            stdout_process: Popen,
            wait_msg: str = '[DesktopEditors]: start page loaded',
            timeout: int = 30
    ):
        start_time = time.time()
        with console.status('green]|INFO| Wait until desktop editor opens') as status:
            while (time.time() - start_time) < timeout:
                status.update(f'[green]|INFO| Waiting for {wait_msg}: {timeout-(time.time() - start_time):.02f} sec.')
                if self._wait_msg_is_present(wait_msg, stdout_process):
                    return
            else:
                raise DesktopException(
                    f"[red]|ERROR| The waiting time {timeout} seconds for the editor to open has expired."
                )

    def get_version(self) -> "str | None":
        version = re.findall(r"\d+\.\d+\.\d+\.\d+", FileUtils.output_cmd(self._generate_get_version_cmd()))
        return version[0] if version else None

    def _wait_msg_is_present(self, wait_msg: str, stdout_process: Popen) -> bool:
        if 'stdout' in self.log_out_cmd:
            return self._check_in_output(wait_msg, stdout_process)
        return self._check_in_log_file(wait_msg)

    def create_log_file(self):
        FileUtils.create_dir(dirname(self.log_file), stdout=False)
        FileUtils.file_writer(self.log_file, '', mode='w')

    def set_license(self):
        license_dir = self.config.get(f"lic_dir_{HostInfo().os}")
        if license_dir and isfile(self.lic_file_path):
            FileUtils.create_dir(license_dir, stdout=False)
            FileUtils.copy(self.lic_file_path, join(license_dir, basename(self.lic_file_path)))
            return print(f"[green]|INFO| Desktop activated")

    def os_is_windows(self) -> bool:
        return self.os == 'windows'

    def _generate_running_command(self):
        def raise_command_error():
            raise DesktopException(f"|ERROR| Can't get running command, key: {HostInfo().os}_run_command")

        if self.data.appimage_package:
            if self.package.path and isfile(self.package.path):
                return self.package.path

        return self.config.get(self._get_run_command_key()) or raise_command_error()

    def _get_run_command_key(self):
        return f'{HostInfo().os if self.data.is_default_package() else self.package.name.lower()}_run_command'

    def _generate_get_version_cmd(self) -> str:
        if self.os.lower() == 'windows':
            path = re.search(r"'(.*?)'", self._generate_running_command())
            return f"powershell.exe (Get-Item '{path.group(1) if path else None}').VersionInfo.FileVersion"
        return f'{self._generate_running_command()} --version'

    @staticmethod
    def _get_config(path):
        config_path = path if path and isfile(path) else join(dirname(realpath(__file__)), 'desktop_config.json')
        return FileUtils.read_json(config_path)

    def _get_log_out_cmd(self) -> str:
        if HostInfo().release in self.config.get('old_windows_system', []):
            self.log_file = FileUtils.unique_name(self.data.tmp_dir, extension='txt')
            self.create_log_file()
        else:
            self.log_file = 'stdout'

        return f'--ascdesktop-log-file="{self.log_file}"'

    @staticmethod
    def _check_in_output(wait_msg: str, stdout_process: Popen) -> bool:
        output = stdout_process.stdout.readline().decode().strip()
        if output:
            console.print(f"[cyan]|INFO| {output}")
            return wait_msg in output
        return False

    def _get_package(self):
        if self.data.flatpak_package:
            return Flatpak()
        elif self.data.snap_package:
            return SnapPackage()
        elif self.data.appimage_package:
            return AppImage(data=self.data)
        else:
            return DefaultPackage(data=self.data)

    def _check_in_log_file(self, wait_msg: str) -> bool:
        try:
            for output in [line.strip() for line in FileUtils.file_read_lines(self.log_file)]:
                if output:
                    console.print(f"[cyan]|INFO| {output}")
                    if wait_msg in output:
                        self.create_log_file()
                        return True
            return False

        except (PermissionError, FileNotFoundError):
            return False
