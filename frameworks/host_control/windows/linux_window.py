# -*- coding: utf-8 -*-
from typing import Optional

from .window import Window


class LinuxWindow(Window):

    @staticmethod
    def get_hwnd(class_name: str, text: str) -> Optional[int]:
        pass

    @staticmethod
    def get_child_window_hwnd(window_hwnd: int, child_window_title: str, child_window_text: str) -> Optional[int]:
        pass

    @staticmethod
    def click_on_button(button_hwnd: int):
        pass
