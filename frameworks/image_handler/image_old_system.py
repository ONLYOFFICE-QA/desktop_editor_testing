# -*- coding: utf-8 -*-
import numpy as np
from PIL import ImageGrab

from .image import Image


class ImageOldSystem(Image):

    @staticmethod
    def read(img_path: str):
        pass

    @staticmethod
    def find_template_on_window(
            window_coord: tuple,
            template: str,
            threshold: "int | float" = 0.8
    ) -> "list[int, int] | None":
        pass

    @staticmethod
    def is_present(
            template: "str | cv2.imread",
            window_coordinates: tuple = None,
            threshold: "int | float" = 0.8
    ) -> bool:
        pass

    @staticmethod
    def grab_coordinate(window_coordinates: tuple = None) -> np.array:
        pass

    @staticmethod
    def find_contours(img: np.ndarray):
        pass

    @staticmethod
    def draw_differences(img_1: np.ndarray, img_2: np.ndarray, diff: np.ndarray) -> "tuple[np.ndarray, np.ndarray]":
        pass

    @staticmethod
    def save(path: str, img: np.ndarray):
        pass

    @staticmethod
    def put_text(cv2_opened_image: np.ndarray, text: str):
        pass

    @staticmethod
    def make_screenshot(img_path: str, window_coordinates: tuple = None) -> None:
        """
        :param img_path: Path to save an image
        :param window_coordinates: (left, top, right, bottom)
        """
        if isinstance(window_coordinates, tuple):
            ImageGrab.grab(bbox=window_coordinates).save(img_path, compression=None)
        else:
            ImageGrab.grab().save(img_path, compression=None)
