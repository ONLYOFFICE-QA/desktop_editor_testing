# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional


class Window(ABC):

    @staticmethod
    @abstractmethod
    def get_hwnd(class_name: str, text: str) -> Optional[int]: ...

    @staticmethod
    @abstractmethod
    def get_child_window_hwnd(window_hwnd: int, child_window_title: str, child_window_text: str) -> Optional[int]: ...

    @staticmethod
    @abstractmethod
    def click_on_button(button_hwnd: int): ...
