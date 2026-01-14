# -*- coding: utf-8 -*-
from os.path import isfile, join, dirname, realpath
from rich import print

from frameworks.host_control import HostInfo, FileUtils
from frameworks.desktop.handlers.VersionHandler import VersionHandler

from ...data import Data

class UrlException(Exception): ...

class UrlGenerator:
    def __init__(self, data: Data):
        self.version = VersionHandler(data.version)
        self.host_name = HostInfo().name().lower()
        self.host_version = HostInfo().version
        self.config = self._get_config(data.custom_config)
        self.__arch = None
        print(f"[green]|INFO| Host Information: {self.host_name} {HostInfo().version}")

    @property
    def arch(self) -> str:
        if self.__arch is None:
            if HostInfo().arch == 'aarch64':
                self.__arch = 'arm64'
            else:
                self.__arch = 'amd64'
        return self.__arch

    @property
    def url(self):
        return f"{self._host}/{self._os}/{self._os_family}/{self.package_name}".strip()

    @property
    def package_name(self):
        if f"{self.host_name} {self.host_version}" in self._get_cef107_system():
            package_key = 'package_cef107'
        elif self.host_name == 'windows' and HostInfo().release in self._get_xp_system():
            package_key = 'package_xp'
        else:
            package_key = 'package'

        return self._get_package_name(package_key)

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
        if HostInfo().os == 'windows':
            return self.version.version
        return f"{self.version.major}.{self.version.minor}-{self.version.build}"

    @property
    def _os(self):
        if HostInfo().os == 'windows':
            return 'win'
        return HostInfo().os

    def _get_package_name(self, key: str):
        package_name = self.config['package_name'][self._os_family][self.arch][key]
        return package_name.replace("[version]", self._version_for_url)

    @staticmethod
    def _get_config(path: str):
        config_path = path if path and isfile(path) else join(dirname(realpath(__file__)), 'url_config.json')
        return FileUtils.read_json(config_path)

    def _get_cef107_system(self) -> list:
        # [f"{HostInfo().name().lower()} {HostInfo().version}"]
        return self.config['cef107_system']

    def _get_xp_system(self) -> list:
        # ["HostInfo().release"]
        return self.config['xp_system']
