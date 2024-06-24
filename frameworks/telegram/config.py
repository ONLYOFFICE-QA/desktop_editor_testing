# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    API_HOST: str = 'https://api.telegram.org' # Without last slash
    MAX_DOCUMENT_SIZE: int = 50_000_000
    MAX_CAPTCHA_LENGTH: int = 1000
    MAX_MESSAGE_LENGTH: int = 4096
    DEFAULT_PARSE_MOD: str = 'Markdown'
    MAX_MEDIA_GROUP_LENGTH: int = 10
