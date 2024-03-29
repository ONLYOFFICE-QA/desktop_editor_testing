from subprocess import call
from rich import print
from os.path import join, isfile, getsize

from frameworks.host_control import FileUtils, HostInfo
from frameworks.decorators.decorators import highlighter

from .url_generator import UrlGenerator
from ..data import Data

class PackageException(Exception): ...

class Package:
    def __init__(self, data: Data):
        self.url_generator = UrlGenerator(data)
        self.os: str = HostInfo().name(pretty=True)
        self.url: str =  self.url_generator.url
        self.name: str = self.url_generator.package_name
        self.version: str = data.version
        self.download_dir: str = data.cache_dir if data.cache_dir else data.tmp_dir
        self.path: str = join(self.download_dir, self.name)
        FileUtils.create_dir(self.download_dir, stdout=False)

    def get(self) -> "None":
        headers = FileUtils.get_headers(self.url)
        if self.exists(headers):
            print(f"[green]|INFO| Package {self.name} already exists. Path: {self.path}")
        else:
            self.download() if headers else print(f"[red]|WARNING| Package does not exist on aws")
        self.install()

    @highlighter(color='green')
    def download(self) -> None:
        print(f"[green]|INFO| Downloading Desktop package\nVersion: {self.version}\nOS: {self.os}\nURL: {self.url}")
        FileUtils.download_file(self.url, self.download_dir)

    def exists(self, headers: "dict | None" = None) -> bool:
        if headers and isfile(self.path):
            return int(getsize(self.path)) == int(headers['Content-Length'])
        elif isfile(self.path):
            return True
        return False

    def install(self) -> None:
        print(f"[green]|INFO| Installing Desktop version: {self.version}\nPackage: {self.name}")
        if isfile(self.path):
            call(self._get_install_command(), shell=True)
        else:
            raise PackageException(f"[red]|ERROR| Package not exists.")

    def _get_install_command(self) -> str:
        if self.path.lower().endswith('.deb'):
            self._unlock_dpkg()
            return f'sudo dpkg -i {self.path}'
        elif self.path.lower().endswith('.rpm'):
            return f'sudo rpm -i {self.path}'
        else:
            raise PackageException(
                f"[red]|ERROR| Unable to generate a command to install the desktop package.\n"
                f"os: {HostInfo().name().lower()}\n"
                f"version: {HostInfo().version}\n"
                f"package path: {self.path}"
            )

    @staticmethod
    def _unlock_dpkg() -> None:
        commands = [
            "sudo rm /var/lib/apt/lists/lock",
            "sudo rm /var/cache/apt/archives/lock",
            "sudo rm /var/lib/dpkg/lock",
            "sudo rm /var/lib/dpkg/lock-frontend"
        ]
        for cmd in commands:
            FileUtils.run_command(cmd)
