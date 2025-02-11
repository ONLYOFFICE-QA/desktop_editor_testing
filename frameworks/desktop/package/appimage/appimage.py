# -*- coding: utf-8 -*-
from os.path import dirname, realpath, join
import re
from subprocess import call

from typing_extensions import Optional

from frameworks.desktop.data import Data
from frameworks.desktop.handlers.VersionHandler import VersionHandler
from frameworks.github_api import GitHubApi
from frameworks.host_control import FileUtils
from frameworks.test_exceptions import AppImageException


class AppImage:
    repo_config = FileUtils.read_json(join(dirname(realpath(__file__)), "appimage_repo_config.json"))
    version_pattern = r"(\d+\.\d+\.\d+-\d+)"

    def __init__(self, data: Data):
        self.data = data
        self.api = GitHubApi(repo_owner=self.repo_config['repo_owner'], repo_name=self.repo_config['repo_name'])
        self.version_handler = VersionHandler(version=self.data.version)
        self.find_version = f"{self.version_handler.without_build}-{self.version_handler.build}"
        self.download_path = None

    def get(self) -> None:
        artifact = self._get_artifact()
        self.download_path = self.api.artifacts.downloads(
            artifact_url=artifact['archive_download_url'],
            output_dir=self.data.tmp_dir,
            file_name=artifact['name']
        )
        self._run_cmd(f"chmod +x {self.download_path}")

    def _get_artifact(self):
        for run in self.api.workflow.get_runs(workflow_id=self._get_workflow_id()):
            artifacts = self.api.artifacts.get(run_id=run["id"])
            for artifact in artifacts:
                if self._find_version(artifact.get('name', '')) == self.find_version:
                    return artifact

        raise AppImageException(f"|ERROR| Can't found url for version: {self.version_handler.version} ")

    def _get_workflow_id(self) -> str:
        for workflow in self.api.workflow.get():
            if workflow.get('name', '') == "Build APPIMAGE package":
                return workflow["id"]

        raise AppImageException(f"[bold red]|ERROR| Can't get workflow id: {self.api.host}")

    def _find_version(self, text: str) -> Optional[str]:
        match = re.search(self.version_pattern, text)
        return match.group(1) if match else None

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
