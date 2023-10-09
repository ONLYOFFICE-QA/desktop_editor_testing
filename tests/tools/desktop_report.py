# -*- coding: utf-8 -*-
import csv
import re
from os.path import dirname, isfile

from frameworks.host_control import FileUtils, HostInfo
from frameworks.telegram import Telegram


class DesktopReport:
    def __init__(self, report_path: str):
        self.path = report_path
        self.dir = dirname(self.path)

    def write(self, os: str, version: str, package_name: str, exit_code: str, tg_msg: bool = False, update_from: str = None):
        self._write_titles() if not isfile(self.path) else ...
        self._writer(mode='a', message=[os, version, package_name, exit_code])
        self.send_to_telegram(exit_code, package_name, version, update_from) if tg_msg else ...

    def send_to_telegram(self, results: str, package_name: str, version: str, update_from):
        pkg_name = re.sub(r"[\s/_]", "", package_name)
        Telegram().send_media_group(
            document_paths=FileUtils.get_paths(self.dir, extension='.png'),
            media_type='photo',
            caption=f'Os: `{HostInfo().name(pretty=True)}`\n'
                    f'Version: `{(update_from + "-") if update_from else ""}{version}`\n'
                    f'Package: `{pkg_name}`\n'
                    f'Result: `{results}`'
        )

    def _writer(self, mode: str, message: list, delimiter='\t', encoding='utf-8'):
        FileUtils.create_dir(self.dir, stdout=False)
        with open(self.path, mode, newline='', encoding=encoding) as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            writer.writerow(message)

    def _write_titles(self):
        self._writer(mode='w', message=['Os', 'Version', 'Package_name', 'Exit_code'])
