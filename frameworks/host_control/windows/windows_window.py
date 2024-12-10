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
    def get_hwnd(class_name: str, text: str) -> Optional[int]:

        def enum_windows_callback(hwnd: int):
            if win32gui.IsWindowVisible(hwnd):
                if (
                        class_name.strip() == win32gui.GetClassName(hwnd).strip()
                        and text.strip() == win32gui.GetWindowText(hwnd).strip()
                ):
                    return hwnd

        win32gui.EnumWindows(enum_windows_callback)
        return None

    @staticmethod
    def get_child_window_hwnd(window_hwnd: int, child_window_title: str, child_window_text: str) -> Optional[int]:

        def find_button(hwnd):
            cls_name, text = win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd)
            if cls_name in child_window_title and child_window_text in text:
                return hwnd

        win32gui.EnumChildWindows(window_hwnd, find_button)
        return None

    @staticmethod
    def click_on_button(button_hwnd: int):
        try:
            win32gui.SendMessage(button_hwnd, win32con.BM_CLICK, 0, 0)
        except Exception as ex:
            print(ex)



