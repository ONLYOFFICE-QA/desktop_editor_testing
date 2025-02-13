# -*- coding: utf-8 -*-
from os.path import join, dirname, realpath
from re import search
from subprocess import call
from typing import Optional

from frameworks.github_api import PullRequest
from frameworks.host_control import FileUtils
from frameworks.test_exceptions import FlatPakException


class Flatpak:
    config = FileUtils.read_json(join(dirname(realpath(__file__)), 'flatpak_config.json'))
    find_cmd_pattern = r"flatpak install --user[^\n]*"

    def __init__(self):
        self.pr = PullRequest(repo_name=self.config['repo_name'], pull_num=self.config["pull_num"])

    def install(self) -> None:
        self._run_cmd(f"{self._get_last_build_install_cmd()} -y")

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
