# -*- coding: utf-8 -*-
from os.path import basename, join, getsize, isfile

from requests import get
from rich import print
from rich.progress import track

from frameworks.host_control import FileUtils
from frameworks.decorators import singleton
from .auth import Auth


@singleton
class ApiReqeust:

    def __init__(self):
        self.auth = Auth()
        self.headers =  {"Authorization": f"Bearer {self.auth.token}"}

    def get(self, url: str) -> dict:
        response = get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        print(f"Error: {response.status_code} - {response.text}")
        return {}

    def download(
            self,
            url: str,
            dir_path: str,
            name: str = None,
            process_bar: bool = True,
            stdout: bool = True,
            stderr: bool = True,
            chunk_size: int = 1024 * 1024
    ) -> str:
        """
        :param chunk_size:
        :param url: download link
        :param dir_path: download folder
        :param name: download filename
        :param process_bar: Enables/disables the file upload status bar display,
        only 1 status bar can be displayed at a time.
        :param stdout: Enable/disable display of successful download messages
        :param stderr: Enable/disable display of error messages
        """

        FileUtils.create_dir(dir_path, stdout=False)

        _name = name if name else basename(url)
        _path = join(dir_path, _name)

        with get(url,  headers=self.headers, stream=True) as request:
            request.raise_for_status()
            with open(_path, 'wb') as file:
                _iter = request.iter_content(chunk_size=chunk_size)
                for chunk in track(_iter, description=f'[red] Downloading: {_name}') if process_bar else _iter:
                    if chunk:
                        file.write(chunk)

        if stdout:
            print(f"[bold green]|INFO| File Saved to: {_path}" if isfile(_path) else f"[red]|WARNING| Not exist")

        if stderr and int(getsize(_path)) != int(request.headers['Content-Length']):
            print(f"[red]|WARNING| Size different\nFile:{getsize(_path)}\nServer:{request.headers['Content-Length']}")

        return _path
