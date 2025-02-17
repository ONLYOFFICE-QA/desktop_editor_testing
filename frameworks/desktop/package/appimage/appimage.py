# -*- coding: utf-8 -*-
import re
from os.path import dirname, realpath, join, getsize
from subprocess import call
from typing import Optional

from rich import print

from frameworks.decorators import retry
from frameworks.desktop.data import Data
from frameworks.desktop.handlers.VersionHandler import VersionHandler
from frameworks.github_api import GitHubApi
from frameworks.host_control import FileUtils, HostInfo
from frameworks.test_exceptions import AppImageException
from ..package import Package


class AppImage(Package):
    repo_config = FileUtils.read_json(join(dirname(realpath(__file__)), "appimage_repo_config.json"))
    version_pattern = r"(\d+\.\d+\.\d+-\d+)"

    def __init__(self, data: Data):
        self.data = data
        self.api = GitHubApi(repo_owner=self.repo_config['repo_owner'], repo_name=self.repo_config['repo_name'])
        self.version_handler = VersionHandler(version=self.data.version)
        self.find_version = f"{self.version_handler.without_build}-{self.version_handler.build}"
        self.path = None

    @property
    def name(self) -> str:
        return 'AppImage'

    def install(self) -> None:
        self._install_specific_dependencies()
        archive_path = self.download_appimage(artifact=self._get_artifact())
        execute_dir = self.unpacking_appimage_archive(archive_path=archive_path)
        self.path = self.find_appimage_path(appimage_dir=execute_dir)
        self._run_cmd(f"chmod +x {self.path}")

    # TODO Bug 73165
    def _install_specific_dependencies(self):
        if f"{HostInfo().name().lower()} {HostInfo().version}" in ["pop 22.04", "ubuntu 24.04", "ubuntu 22.04"]:
            self._run_cmd("sudo apt-get install libfuse2 -y")

    @retry(max_attempts=3, interval=1)
    def download_appimage(self, artifact: dict) -> str:
        print(f"[green]|INFO| Downloading AppImage: {artifact['name']}")
        download_path = self.api.artifacts.downloads(
            artifact_url=artifact['archive_download_url'],
            output_dir=self.data.tmp_dir,
            file_name=f"{artifact['name']}.zip"
        )
        if artifact['size_in_bytes'] != getsize(download_path):
            raise AppImageException(f"Failed downloads appimage.")

        print(f"[green]|INFO| AppImage.zip downloaded to: {download_path}")
        return download_path

    def unpacking_appimage_archive(self, archive_path: str) -> str:
        execute_dir = FileUtils.unique_name(self.data.tmp_dir)
        FileUtils.create_dir(execute_dir, stdout=False)
        FileUtils.unpacking_zip(archive_path=archive_path, execute_path=execute_dir, stdout=True)
        return execute_dir

    def find_appimage_path(self, appimage_dir: str) -> str:
        for path in FileUtils.get_paths(appimage_dir, extension='AppImage'):
            if self._find_version(path) == self.find_version:
                return path

        raise AppImageException(f"|ERROR| Can't found appimage path from: {appimage_dir} ")

    def _get_artifact(self) -> Optional[dict]:
        for run in self.api.workflow.get_runs(workflow_id=self._get_workflow_id()):
            artifacts = self.api.artifacts.get(run_id=run["id"])
            for artifact in artifacts:
                if self._find_version(artifact.get('name', '')) == self.find_version:
                    return artifact

        raise AppImageException(f"|ERROR| Can't found url for version: {self.version_handler.version} ")

    def _get_workflow_id(self) -> str:
        for workflow in self.api.workflow.get():
            if workflow.get('name', '').lower() == "Build APPIMAGE package".lower():
                return workflow["id"]

        raise AppImageException(f"[bold red]|ERROR| Can't get workflow id: {self.api.host}")

    def _find_version(self, text: str) -> Optional[str]:
        match = re.search(self.version_pattern, text)
        return match.group(1) if match else None

    @staticmethod
    def _run_cmd(cmd: str) -> int:
        return call(cmd, shell=True)
