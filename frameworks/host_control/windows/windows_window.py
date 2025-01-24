# -*- coding: utf-8 -*-
from typing import Optional

from .window import Window

try:
    import win32gui
    import win32con
except ImportError:
    pass


class WindowsWindow(Window):

    @staticmethod
    def get_hwnd(class_name: str, text: str) -> list:
        data = []

        def enum_windows_callback(hwnd: int, data: list):
            if win32gui.IsWindowVisible(hwnd):
                _cls_name, _text = win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd)
                if class_name.strip() == _cls_name.strip() and text.strip() == _text.strip():
                    data.append(hwnd)

        win32gui.EnumWindows(enum_windows_callback, data)
        print(data)
        return data[0] if data else None

    @staticmethod
    def get_child_window_hwnd(window_hwnd: int, child_window_title: str, child_window_text: str) -> Optional[int]:
        data = []

        def find_button(hwnd, data: list):
            cls_name, text = win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd)
            if cls_name in child_window_title and child_window_text in text:
                data.append(hwnd)

        win32gui.EnumChildWindows(window_hwnd, find_button, data)
        return data[0] if data else None

    @staticmethod
    def click_on_button(button_hwnd: int):
        try:
            win32gui.SendMessage(button_hwnd, win32con.BM_CLICK, 0, 0)
        except Exception as ex:
            print(ex)

    @staticmethod
    def close(hwnd: int) -> None:
        try:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            print(f"[red]|WARNING| Can't close the window. Exception: {e}")
