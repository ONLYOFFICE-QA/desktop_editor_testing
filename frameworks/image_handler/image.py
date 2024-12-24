# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import numpy as np


class Image(ABC):

    @staticmethod
    @abstractmethod
    def read(img_path: str): ...

    @staticmethod
    @abstractmethod
    def find_template_on_window(
            window_coord: tuple,
            template: str,
            threshold: "int | float" = 0.8
    ) -> "list[int, int] | None": ...

    @staticmethod
    @abstractmethod
    def is_present(
            template: "str | cv2.imread",
            window_coordinates: tuple = None,
            threshold: "int | float" = 0.8
    ) -> bool: ...

    @staticmethod
    @abstractmethod
    def grab_coordinate(window_coordinates: tuple = None) -> np.array: ...

    @staticmethod
    @abstractmethod
    def find_contours(img: np.ndarray): ...

    @staticmethod
    @abstractmethod
    def draw_differences(img_1: np.ndarray, img_2: np.ndarray, diff: np.ndarray) -> "tuple[np.ndarray, np.ndarray]": ...

    @staticmethod
    @abstractmethod
    def save(path: str, img: np.ndarray): ...

    @staticmethod
    @abstractmethod
    def put_text(cv2_opened_image: np.ndarray, text: str): ...

    @staticmethod
    @abstractmethod
    def make_screenshot(img_path: str, window_coordinates: tuple = None) -> None:
        """
        :param img_path: Path to save an image
        :param window_coordinates: (left, top, right, bottom)
        """