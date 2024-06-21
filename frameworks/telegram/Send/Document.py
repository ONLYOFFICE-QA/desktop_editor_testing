# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from .Send import Send
from .tools import TelegramRequests, Caption
from ..config import Config
from ..utils import File


class Document(Send):
    """
    Handles sending documents via Telegram.

    :param requests: An instance of TelegramRequests for making API calls.
    :param tmp_dir: Temporary directory for storing files. Default is system temporary directory.
    """
    _DEFAULT_PARSE_MOD: str = Config.DEFAULT_PARSE_MOD
    _MAX_DOCUMENT_SIZE: int = Config.MAX_DOCUMENT_SIZE

    def __init__(self, requests: TelegramRequests, tmp_dir: str = gettempdir()):
        self.requests = requests
        self.caption = Caption()
        self.tmp_dir = tmp_dir

    def send(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        """
        Sends a document. If the document size exceeds the maximum allowed, it compresses the document before sending.

        :param document_path: Path to the document to be sent.
        :param caption: The caption for the document. Default is an empty string.
        :param parse_mode: The parse mode for the caption (e.g., 'Markdown', 'HTML'). Default is None.
        :return: None
        """

        self.requests.post(
            'sendDocument',
            data=self._generate_data(self.caption.prepare(caption), parse_mode or self._DEFAULT_PARSE_MOD),
            files={ "document": open(self.prepare(document_path), 'rb') }
        )

    def prepare(self, doc_path: str) -> str:
        """
        Prepares the document for sending. Compresses the document if its size exceeds the maximum allowed size.

        :param doc_path: Path to the document to be prepared.
        :return: Path to the prepared document.
        """
        if not os.path.isdir(doc_path) or os.path.getsize(doc_path) <= self._MAX_DOCUMENT_SIZE:
            return doc_path

        archive_path = os.path.join(self.tmp_dir, f'{os.path.basename(doc_path)}.zip')
        File.compress(doc_path, archive_path)
        return archive_path

    def _generate_data(self, caption: str, parse_mode: str) -> dict:
        """
        Generates the data dictionary for the API call.

        :param caption: The caption for the document.
        :param parse_mode: The parse mode for the caption (e.g., 'Markdown', 'HTML').
        :return: The data dictionary for the API call.
        """
        return {
            "chat_id": self.requests.auth.chat_id,
            "caption": self.caption.prepare(caption),
            "parse_mode": parse_mode
        }
