# -*- coding: utf-8 -*-
from os.path import isfile, join, dirname, realpath
from rich import print

from frameworks.host_control import HostInfo, FileUtils
from frameworks.desktop.handlers.VersionHandler import VersionHandler

from ...data import Data

class UrlException(Exception):
    """Exception raised when URL generation fails."""
    ...

class UrlGenerator:
    """Generates download URLs for desktop packages based on system configuration."""

    def __init__(self, data: Data):
        """Initialize UrlGenerator with configuration data.

        :param data: Configuration data containing version and custom config information
        """
        self.version = VersionHandler(data.version)
        self.host_name = HostInfo().name().lower()
        self.host_version = HostInfo().version
        self.config = self._get_config(data.custom_config)
        self.__arch = None
        print(f"[green]|INFO| Host Information: {self.host_name} {HostInfo().version}")

    @property
    def arch(self) -> str:
        """Get the architecture identifier for the current system.

        :return: Architecture name ('arm64' or 'amd64')
        """
        if self.__arch is None:
            if HostInfo().arch in ['aarch64', 'arm64']:
                self.__arch = 'arm64'
            else:
                self.__arch = 'amd64'
        return self.__arch

    @property
    def url(self):
        """Generate the complete download URL for the desktop package.

        :return: Full URL to download the package
        """
        return f"{self._host}/{self._os}/{self._os_family}/{self.package_name}".strip()

    @property
    def package_name(self):
        """Determine the appropriate package name based on system requirements.

        :return: Package name with version information
        """
        if f"{self.host_name} {self.host_version}" in self._get_cef107_system():
            package_key = 'package_cef107'
        elif self.host_name == 'windows' and HostInfo().release in self._get_xp_system():
            package_key = 'package_xp'
        else:
            package_key = 'package'

        return self._get_package_name(package_key)

    @property
    def _host(self):
        """Get the base host URL from configuration.

        :return: Base URL of the download host
        """
        return self.config["host"]

    @property
    def _os_family(self) -> str:
        """Determine the OS family for the current system.

        :return: OS family identifier
        :raises UrlException: If OS family cannot be determined
        """
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
        """Format version string appropriately for URL construction.

        :return: Formatted version string
        """
        if HostInfo().os == 'windows':
            return self.version.version
        return f"{self.version.major}.{self.version.minor}-{self.version.build}"

    @property
    def _os(self):
        """Get the OS identifier for URL construction.

        :return: OS name for URL
        """
        if HostInfo().os == 'windows':
            return 'win'
        return HostInfo().os

    def _get_package_name(self, key: str):
        """Get the package name template and substitute version.

        :param key: Configuration key for the package type
        :return: Package name with version substituted
        """
        package_name = self.config['package_name'][self._os_family][self.arch][key]
        return package_name.replace("[version]", self._version_for_url)

    @staticmethod
    def _get_config(path: str):
        """Load configuration from JSON file.

        :param path: Custom configuration file path, or None to use default
        :return: Configuration dictionary
        """
        config_path = path if path and isfile(path) else join(dirname(realpath(__file__)), 'url_config.json')
        return FileUtils.read_json(config_path)

    def _get_cef107_system(self) -> list:
        """Get list of systems that require CEF107 package version.

        From [f"{HostInfo().name().lower()} {HostInfo().version}"]
        :return: List of system identifiers requiring CEF107
        """
        return self.config['cef107_system']

    def _get_xp_system(self) -> list:
        """Get list of Windows XP compatible system releases.
        From ["HostInfo().release"]
        :return: List of XP system identifiers
        """
        return self.config['xp_system']
