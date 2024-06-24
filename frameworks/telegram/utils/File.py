# -*- coding: utf-8 -*-
import os
import json
from os.path import join, isdir
from io import open as io_open
from codecs import open as codecs_open

from frameworks.telegram.utils import Str

from shutil import rmtree
from zipfile import ZipFile



class File:
    EXCEPTIONS = ['.DS_Store']

    @staticmethod
    def compress(path: str, archive_path: str = None, delete: bool = False, compress_type: int = 8) -> None:
        """
        :param compress_type: ZIP_STORED = 0, ZIP_DEFLATED = 8, ZIP_BZIP2 = 12, ZIP_LZMA = 14
        :param path: Path to compression files.
        :param archive_path: Path to the archive file.
        :param delete:  Deleting files after compression.
        """
        if not os.path.exists(path):
            return print(f'[bold red]|COMPRESS WARNING| Path for compression does not exist: {path}')

        _archive_path = archive_path or join(
            os.path.dirname(path) if os.path.isfile(path) else path,
            f"{os.path.basename(Str.delete_last_slash(path))}.zip"
        )

        os.makedirs(os.path.dirname(_archive_path), exist_ok=True)

        with ZipFile(_archive_path, 'w') as _zip:
            if os.path.isdir(path):
                print(f'[green]|INFO| Compressing dir: {path}')
                exceptions = File.EXCEPTIONS + [f"{os.path.basename(_archive_path)}"]

                for file in File.get_paths(path):
                    if os.path.basename(file) not in exceptions:
                        _zip.write(file, os.path.relpath(file, path), compress_type=compress_type)

                if delete:
                    File.delete([join(path, obj) for obj in os.listdir(path) if obj != os.path.basename(_archive_path)])

            else:
                print(f'[green]|INFO| Compressing file: {path}')
                _zip.write(path, os.path.basename(Str.delete_last_slash(path)), compress_type=compress_type)
                File.delete(path) if delete else ...

    @staticmethod
    def delete(path: "str | tuple | list", stdout: bool = False, stderr: bool = False) -> None:
        """
        Deletes the specified file or directory. Supports single or multiple paths.

        :param path: Path(s) to the file(s) or directory(ies) to delete. Can be a string, tuple, or list.
        :param stdout: If True, prints a message to standard output upon successful deletion. Default is False.
        :param stderr: If True, prints an error message to standard error if the path is invalid or the deletion fails. Default is False.
        :return: None
        """
        if not path:
            return print(f"[red]|DELETE ERROR| Path should be string, tuple or list not {path}") if stderr else None

        for _path in [path] if isinstance(path, str) else path:
            object_path = _path.rstrip("*")
            if not os.path.exists(object_path):
                print(f"[bold red]|DELETE WARNING| File not exist: {object_path}") if stderr else ...
                continue

            if isdir(object_path):
                rmtree(_path, ignore_errors=True)
            else:
                os.remove(object_path)

            if stderr and os.path.exists(object_path):
                print(f"[bold red]|DELETE WARNING| Is not deleted: {_path}")
            elif stdout:
                print(f'[green]|INFO| Deleted: {_path}')

    @staticmethod
    def get_paths(dir_path: str) -> list:
        """
        Retrieves all file paths within the specified directory.

        :param dir_path: Path to the directory.
        :return: A list of paths to all files within the directory.
        """
        return [os.path.join(root, filename) for root, _, files in os.walk(dir_path) for filename in files]

    @staticmethod
    def read_json(path_to_json: str, encoding: str = "utf_8_sig") -> json:
        """
        Reads a JSON file and returns its contents.

        :param path_to_json: Path to the JSON file.
        :param encoding: The encoding of the file. Default is "utf_8_sig".
        :return: The contents of the JSON file.
        """
        with codecs_open(path_to_json, mode="r", encoding=encoding) as file:
            return json.load(file)

    @staticmethod
    def read(file_path: str, encoding='utf-8') -> str:
        """
        Reads a text file and returns its contents as a string.

        :param file_path: Path to the text file.
        :param encoding: The encoding of the file. Default is 'utf-8'.
        :return: The contents of the file.
        """
        with io_open(file_path, 'r', encoding=encoding) as file:
            return file.read()
