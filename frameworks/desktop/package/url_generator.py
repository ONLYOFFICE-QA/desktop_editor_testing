# -*- coding: utf-8 -*-
from os.path import isfile, join, dirname, realpath
from frameworks.host_control import HostInfo, FileUtils
from frameworks.desktop.handlers.VersionHandler import VersionHandler
from ..data import Data

class UrlException(Exception): ...

class UrlGenerator:
    def __init__(self, data: Data):
        self.version = VersionHandler(data.version)
        self.host_name = HostInfo().name().lower()
        self.host_version = HostInfo().version
        self.config = self._get_config(data.custom_config_path)
        self.cef107_system: list = self.config['cef107_system'] # f"{HostInfo().name().lower()} {HostInfo().version}"
        print(f"[green]|INFO| Host Information: {self.host_name} {HostInfo().version}")

    @property
    def url(self):
        return f"{self._host}/{self._os}/{self._os_family}/{self.package_name}".strip()

    @property
    def package_name(self):
        if f"{self.host_name} {self.host_version}" in self.cef107_system:
            return self._get_package_name('package_cef107')
        return self._get_package_name('package')

    @property
    def _host(self):
        return self.config["host"]

    @property
    def _os_family(self) -> str:
        for os_family, distributions in self.config['os_family'].items():
            if self.host_name in distributions:
                return os_family
        raise UrlException(
            f"[red]|ERROR| Can't verify os family for download desktop package.\n"
            f"host name: {self.host_name}\n"
            f"version: {self.host_version}"
        )

    @property
    def _version_for_url(self):
        if self._os == 'windows':
            return self.version.version
        return f"{self.version.major}.{self.version.minor}-{self.version.build}"

    @property
    def _os(self):
        if HostInfo().os == 'windows':
            return 'win'
        return HostInfo().os

    def _get_package_name(self, key: str):
        return self.config['package_name'][self._os_family][key].replace("[version]", self._version_for_url)

    @staticmethod
    def _get_config(path: str):
        config_path = path if path and isfile(path) else join(dirname(realpath(__file__)), 'url_config.json')
        return FileUtils.read_json(config_path)
