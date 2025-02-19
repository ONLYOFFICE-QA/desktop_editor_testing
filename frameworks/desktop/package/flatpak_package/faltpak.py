# -*- coding: utf-8 -*-
from os.path import join, dirname, realpath
from re import search
from subprocess import call
from typing import Optional

import requests

from frameworks.flatpak import FlatPakInstaller
from frameworks.github_api import PullRequest
from frameworks.host_control import FileUtils
from frameworks.test_exceptions import FlatPakException

from ..package import Package


class Flatpak(Package):
    config = FileUtils.read_json(join(dirname(realpath(__file__)), 'flatpak_config.json'))
    find_cmd_pattern = r"flatpak install --user[^\n]*"

    def __init__(self):
        self.pr = PullRequest(repo_name=self.config['repo_name'], pull_num=self.config["pull_num"])
        self.flatpak = FlatPakInstaller()

    @property
    def name(self) -> str:
        return "Flatpak"

    def install(self) -> None:
        self.flatpak.install()
        command = self._get_last_build_install_cmd()
        if not self._check_package_exist(link=self._get_package_link(command=command)):
            raise FlatPakException(f"package not exist on {command}")

        self._run_cmd(f"{command} -y")

    @staticmethod
    def _get_package_link(command: str) -> str:
        return next((part for part in command.split() if part.startswith('http')), '')

    def _check_package_exist(self, link: str) -> bool:
        return requests.get(link).status_code == 200

    def _get_last_build_install_cmd(self) -> Optional[str]:
        newest_comment = max(self._get_filtered_comments(), key=lambda c: c["created_at"])
        command_match = search(self.find_cmd_pattern, newest_comment["body"])
        if command_match:
            return command_match.group(0)

        raise FlatPakException("Flatpak install command not found")

    def _get_filtered_comments(self) -> list:
        return  [
            comment for comment in self.pr.get_all_comments() if search(self.find_cmd_pattern, comment["body"])
        ]

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
