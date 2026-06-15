# -*- coding: utf-8 -*-
import platform

import cv2
import numpy as np
from numpy.fft import fft2, ifft2
from PIL import ImageGrab

from .image import Image

_IS_ARM = platform.machine() in ('aarch64', 'arm64')


class ImageNewSystem(Image):

    @staticmethod
    def read(img_path: str) -> cv2.imread:
        return cv2.imread(img_path)

    @staticmethod
    def _match_template(image: np.ndarray, template: np.ndarray) -> "tuple[float, tuple]":
        """Platform-safe template matching. Uses numpy FFT on ARM64 (cv2.matchTemplate causes SIGILL on VBox).
        :param image: grayscale image
        :param template: grayscale template
        """
        if _IS_ARM:
            return ImageNewSystem._match_template_fft(image, template)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        return max_val, max_loc

    @staticmethod
    def _match_template_fft(image: np.ndarray, template: np.ndarray) -> "tuple[float, tuple]":
        """Fully vectorized FFT-based normalized cross-correlation using numpy.
        :param image: grayscale image (H, W)
        :param template: grayscale template (h, w)
        """
        ih, iw = image.shape[:2]
        th, tw = template.shape[:2]

        if th > ih or tw > iw:
            return 0.0, (0, 0)

        image_f = image.astype(np.float64)
        template_f = template.astype(np.float64)

        tmpl_mean = template_f.mean()
        tmpl_centered = template_f - tmpl_mean
        tmpl_energy = np.sum(tmpl_centered ** 2)

        if tmpl_energy == 0:
            return 0.0, (0, 0)

        padded_tmpl = np.zeros((ih, iw), dtype=np.float64)
        padded_tmpl[:th, :tw] = tmpl_centered
        cross_corr = np.real(ifft2(fft2(image_f) * np.conj(fft2(padded_tmpl))))

        n = th * tw
        valid_h = ih - th + 1
        valid_w = iw - tw + 1

        integral = np.cumsum(np.cumsum(image_f, axis=0), axis=1)
        integral_sq = np.cumsum(np.cumsum(image_f ** 2, axis=0), axis=1)

        br = integral[th - 1:th - 1 + valid_h, tw - 1:tw - 1 + valid_w]
        br_sq = integral_sq[th - 1:th - 1 + valid_h, tw - 1:tw - 1 + valid_w]

        patch_sum = br.copy()
        patch_sq_sum = br_sq.copy()

        if valid_h > 1:
            patch_sum[1:, :] -= integral[:valid_h - 1, tw - 1:tw - 1 + valid_w]
            patch_sq_sum[1:, :] -= integral_sq[:valid_h - 1, tw - 1:tw - 1 + valid_w]
        if valid_w > 1:
            patch_sum[:, 1:] -= integral[th - 1:th - 1 + valid_h, :valid_w - 1]
            patch_sq_sum[:, 1:] -= integral_sq[th - 1:th - 1 + valid_h, :valid_w - 1]
        if valid_h > 1 and valid_w > 1:
            patch_sum[1:, 1:] += integral[:valid_h - 1, :valid_w - 1]
            patch_sq_sum[1:, 1:] += integral_sq[:valid_h - 1, :valid_w - 1]

        patch_var = patch_sq_sum - (patch_sum ** 2) / n
        cc = cross_corr[:valid_h, :valid_w] - tmpl_mean * patch_sum

        with np.errstate(divide='ignore', invalid='ignore'):
            ncc = cc / np.sqrt(np.maximum(patch_var, 0) * tmpl_energy)
            ncc = np.where(np.isfinite(ncc), ncc, 0.0)

        max_idx = int(np.argmax(ncc))
        max_y, max_x = divmod(max_idx, valid_w)

        return max(0.0, float(ncc[max_y, max_x])), (max_x, max_y)

    @staticmethod
    def find_template_on_window(
            window_coord: tuple,
            template: str,
            threshold: "int | float" = 0.8
    ) -> "list[int, int] | None":
        window = cv2.cvtColor(ImageNewSystem.grab_coordinate(window_coord), cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(cv2.imread(template), cv2.COLOR_BGR2GRAY)
        max_val, max_loc = ImageNewSystem._match_template(window, template)
        if max_val >= threshold:
            h, w = template.shape
            center_x = max_loc[0] + w // 2 + window_coord[0]
            center_y = max_loc[1] + h // 2 + window_coord[1]
            return [center_x, center_y]
        return None

    @staticmethod
    def is_present(
            template: "str | cv2.imread",
            window_coordinates: tuple = None,
            threshold: "int | float" = 0.8
    ) -> bool:
        img = ImageNewSystem.grab_coordinate(window_coordinates)
        window = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(cv2.imread(template) if isinstance(template, str) else template, cv2.COLOR_BGR2GRAY)
        max_val, _ = ImageNewSystem._match_template(window, template)
        return max_val >= threshold

    @staticmethod
    def grab_coordinate(window_coordinates: tuple = None) -> np.array:
        """
        :param window_coordinates: (left, top, right, bottom)
        """
        if isinstance(window_coordinates, tuple):
            return np.array(ImageGrab.grab(bbox=window_coordinates))
        img = ImageGrab.grab()
        return np.array(img)

    @staticmethod
    def find_contours(img: np.ndarray):
        rgb, gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h >= 500:
                return rgb[y:y + h, x:x + w]

    @staticmethod
    def draw_differences(img_1: np.ndarray, img_2: np.ndarray, diff: np.ndarray) -> "tuple[np.ndarray, np.ndarray]":
        thresh = cv2.threshold((diff * 255).astype("uint8"), 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contur in contours[0] if len(contours) == 2 else contours[1]:
            if cv2.contourArea(contur) > 40:
                x, y, w, h = cv2.boundingRect(contur)
                cv2.rectangle(img_1, (x, y), (x + w, y + h), (0, 0, 255), 0)
                cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 0, 255), 0)
        return img_1, img_2

    @staticmethod
    def save(path: str, img: np.ndarray):
        cv2.imwrite(path, img)

    @staticmethod
    def put_text(cv2_opened_image: np.ndarray, text: str):
        cv2.putText(cv2_opened_image, text, (20, 35), cv2.FONT_HERSHEY_COMPLEX, 1, color=(0, 0, 255), thickness=2)

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
