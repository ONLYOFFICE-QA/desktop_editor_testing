# -*- coding: utf-8 -*-
import csv
import re
from _csv import reader
from os.path import dirname

from frameworks.host_control import FileUtils, HostInfo
from frameworks.telegram import Telegram


class DesktopReport:
    def __init__(self, report_path: str):
        self.path = report_path
        self.dir = dirname(self.path)
        FileUtils.create_dir(self.dir, stdout=False)
        self._writer(self.path, 'w', [ 'Os', 'Version', 'Package_name', 'Exit_code'])

    def write(self, os: str, version: str, package_name: str, exit_code: str, tg_msg: bool = False):
        self._writer(self.path, 'a', [os, version, package_name, exit_code])
        self.send_to_telegram(exit_code, package_name, version) if tg_msg else ...

    @staticmethod
    def read(csv_file: str, delimiter: str = "\t") -> list:
        with open(csv_file, 'r') as csvfile:
            return [row for row in reader(csvfile, delimiter=delimiter)]

    @staticmethod
    def _writer(file_path: str, mode: str, message: list, delimiter='\t', encoding='utf-8'):
        FileUtils.create_dir(dirname(file_path), stdout=False)
        with open(file_path, mode, newline='', encoding=encoding) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            writer.writerow(message)

    def send_to_telegram(self, results: str, package_name: str, version: str):
        pkg_name = re.sub(r"[\s/_]", "", package_name)
        Telegram().send_media_group(
            document_paths=self._get_report_files(),
            media_type='photo',
            caption=f'Os: `{HostInfo().name(pretty=True)}`\n'
                    f'Version: `{version}`\n'
                    f'Package: `{pkg_name}`\n'
                    f'Result: `{results if results == "Passed" else "Error"}`'
        )

    def _get_report_files(self):
        return FileUtils.get_paths(self.dir, extension='.png')
