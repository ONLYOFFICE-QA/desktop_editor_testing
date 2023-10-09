# -*- coding: utf-8 -*-
import re
import time
from os.path import join, dirname, isfile, basename, realpath
from subprocess import Popen, PIPE
from frameworks.host_control import HostInfo, FileUtils
from rich import print
from rich.console import Console
from .package import Package
from .data import Data

console = Console()
class DesktopException(Exception): ...

class DesktopEditor:
    def __init__(self, data: Data):
        self.lic_file_path = data.lic_file
        self.config = self._get_config(data.custom_config_path)
        self.package = Package(data)
        self.os = HostInfo().os
        self.tmp_dir = data.tmp_dir
        self.log_file = join(self.tmp_dir, "desktop.log")
        self.create_log_file()
        self.debug_command = '--ascdesktop-support-debug-info'
        self.log_out_command = f'--ascdesktop-log-file={"stdout" if HostInfo().os != "windows" else self.log_file}'

    def open(self, file_path: str = None, debug_mode: bool = False, log_out_mode: bool = False) -> Popen:
        command = (
            f"{self._generate_running_command()}"
            f"{(' ' + self.log_out_command) if log_out_mode else ''}"
            f"{(' ' + self.debug_command) if debug_mode else ''}"
            f"{(' ' + file_path) if file_path else ''}".strip()
        )
        return Popen(command, stdout=PIPE, stderr=PIPE, shell=True)

    @staticmethod
    def wait_until_open(
            stdout_process: Popen,
            wait_msg: str = '[DesktopEditors]: start page loaded',
            timeout: int = 30
    ):
        start_time = time.time()
        with console.status('green]|INFO| Wait until desktop editor opens') as status:
            while (time.time() - start_time) < timeout:
                status.update(f'[green]|INFO| Waiting for {wait_msg}: {timeout-(time.time() - start_time):.02f} sec.')
                output = stdout_process.stdout.readline().decode().strip()
                if output:
                    console.print(f"[cyan]|INFO| {output}")
                    if wait_msg in output:
                        break
            else:
                raise DesktopException(
                    f"[red]|ERROR| The waiting time {timeout} seconds for the editor to open has expired."
                )

    def version(self) -> "str | None":
        version = re.findall(
            r"\d+\.\d+\.\d+\.\d+",
            FileUtils.output_cmd(f'{self._generate_running_command()} --version')
        )
        return version[0] if version else None

    def close(self):
        # Todo
        # call('killall DesktopEditors', shell=True) -> segmentation fault in stdout
        ...

    def read_log(self, wait_msg: str):
        for line in FileUtils.file_reader(self.log_file).split('\n'):
            print(line) if line else ...
            if wait_msg == line.strip():
                self.create_log_file()
                return

    def create_log_file(self):
        FileUtils.create_dir(dirname(self.log_file), stdout=False)
        FileUtils.file_writer(self.log_file, '', mode='w')

    def set_license(self):
        license_dir = self.config.get(f"lic_dir_{HostInfo().os}")
        if license_dir and isfile(self.lic_file_path):
            FileUtils.create_dir(license_dir, stdout=False)
            FileUtils.copy(self.lic_file_path, join(license_dir, basename(self.lic_file_path)))
            return print(f"[green]|INFO| Desktop activated")

    def _generate_running_command(self):
        run_cmd = self.config.get(f'{HostInfo().os}_run_command', None)
        if run_cmd:
            return run_cmd
        raise ValueError(f"[red]|ERROR| Can't get running command, key: {HostInfo().os}_run_command")

    @staticmethod
    def _get_config(path):
        config_path = path if path and isfile(path) else join(dirname(realpath(__file__)), 'desktop_config.json')
        return FileUtils.read_json(config_path)
