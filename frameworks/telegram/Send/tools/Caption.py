# -*- coding: utf-8 -*-
from ...config import Config


class Caption:
    _captcha_length: int = Config.MAX_CAPTCHA_LENGTH

    def prepare(self, caption: str) -> str:
        return caption[:self._captcha_length]
