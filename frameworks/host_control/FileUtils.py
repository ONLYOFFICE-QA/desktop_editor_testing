# -*- coding: utf-8 -*-
import json
from os import makedirs, walk
from os.path import isfile, isdir, join, basename, getsize, exists
from random import randint
from shutil import copyfile
from subprocess import getoutput, Popen, PIPE
from codecs import open as codecs_open

from requests import get, head
from rich import print
from rich.progress import track

class FileUtils:

    @staticmethod
    def read_json(path_to_json: str, encoding: str = "utf_8_sig") -> json:
        with codecs_open(path_to_json, mode="r", encoding=encoding) as file:
            return json.load(file)

    @staticmethod
    def delete_last_slash(path):
        return path.rstrip(path[-1]) if path[-1] in ['/', '\\'] else path

    @staticmethod
    def create_dir(dir_path: "str | tuple | list", stdout: bool = True, stderr: bool = True) -> None:
        for _dir_path in [dir_path] if isinstance(dir_path, str) else dir_path:
            if not isdir(_dir_path):
                makedirs(_dir_path, exist_ok=True)

                if isdir(_dir_path):
                    print(f'[green]|INFO| Folder Created: {_dir_path}') if stdout else ...
                    continue

                print(f'[bold red]|WARNING| Create folder warning. Folder not created: {_dir_path}') if stderr else ...
                continue

            print(f'[green]|INFO| Folder exists: {_dir_path}') if stdout else ...

    @staticmethod
    def get_headers(url: str, stderr: bool = False):
        """
        Retrieve headers from a given URL.

        :param url: The URL from which to retrieve headers.
        :param stderr: (Optional) If True, prints a warning message when unable to retrieve headers. Defaults to False.
        :return: A dictionary containing the headers if the request is successful, None otherwise.
        """
        status = head(url)

        if status.status_code == 200:
            return status.headers

        print(f"[bold red]|WARNING| Can't get headers\nURL:{url}\nResponse: {status.status_code}") if stderr else None
        return None


    @staticmethod
    def copy(
            path_from: str,
            path_to: str,
            stderr: bool = True,
    ) -> None:
        if not exists(path_from):
            return print(f"[red]|WARNING| Path not exist: {path_from}") if stderr else None

        if isfile(path_from):
            copyfile(path_from, path_to)
        else:
            return print(f"[red] Cant copy dir: {path_from}")

    @staticmethod
    def download(
            url: str,
            dir_path: str,
            name: str = None,
            process_bar: bool = True,
            stdout: bool = True,
            stderr: bool = True,
            chunk_size: int = 1024 * 1024
    ) -> None:
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

        with get(url, stream=True) as request:
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


    @staticmethod
    def file_reader(file_path, mode='r'):
        with open(file_path, mode) as file:
            return file.read()

    @staticmethod
    def file_read_lines(file_path, mode='r') -> list:
        with open(file_path, mode) as file:
            return file.readlines()

    @staticmethod
    def file_writer(file_path, text, mode='w'):
        with open(file_path, mode) as file:
            file.write(text)

    @staticmethod
    def output_cmd(command):
        return getoutput(command)

    @staticmethod
    def run_command(command):
        popen = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = popen.communicate()
        popen.wait()
        stdout = stdout.strip().decode('utf-8', errors='ignore')
        stderr = stderr.strip().decode('utf-8', errors='ignore')
        popen.stdout.close(), popen.stderr.close()
        return stdout, stderr

    @staticmethod
    def unique_name(path: str, extension: str = None) -> str:
        """
        Generate a unique filename in a given directory.

        :param path: The directory path in which to generate the unique filename.
        :param extension: (Optional) The extension for the filename. If provided, it should not contain a leading period.
        :return: A unique filename with an optional extension.
        """
        _ext = extension.replace(".", "") if extension else None
        while True:
            random_path = join(path, f"{randint(500, 50000)}{('.' + _ext) if _ext else ''}".strip())
            if not exists(random_path):
                return random_path

    @staticmethod
    def get_paths(dir_path: str, extension: "tuple | str" = None) -> list:
        """
        Retrieves all file paths within the specified directory.

        :param dir_path: Path to the directory.
        :param extension: (Optional) The extension(s) of the files to include. Can be a string or a tuple of strings. Defaults to None.
        :return: A list of paths to all files within the directory.
        """
        file_paths = []

        if extension:
            extension = tuple(ext.lower() for ext in extension) if isinstance(extension, tuple) else extension.lower()

        for root, dirs, files in walk(dir_path):
            for filename in files:

                if extension and not filename.lower().endswith(extension):
                    continue

                file_paths.append(join(root, filename))

        return file_paths
