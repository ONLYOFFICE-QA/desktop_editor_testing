# -*- coding: utf-8 -*-


def delete_last_slash(path: str) -> str:
    """
    Removes the trailing slash or backslash from the given path, if present.

    :param path: The file or directory path.
    :return: The path without the trailing slash or backslash.
    """
    return path.rstrip(path[-1]) if path[-1] in ['/', '\\'] else path
