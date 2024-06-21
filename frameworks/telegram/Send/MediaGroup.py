# -*- coding: utf-8 -*-
from os.path import basename
from json import dumps

from .Document import Document
from .Message import Message
from .Send import Send
from .tools import TelegramRequests, Caption
from ..config import Config


class MediaGroup(Send):
    """
    Handles sending media groups via Telegram.

    :param requests: An instance of TelegramRequests for making API calls.
    """
    _DEFAULT_PARSE_MOD: str = Config.DEFAULT_PARSE_MOD
    _MAX_CAPTCHA_LENGTH: int = Config.MAX_CAPTCHA_LENGTH
    _MAX_LENGTH: int = Config.MAX_MEDIA_GROUP_LENGTH

    def __init__(self, requests: TelegramRequests):
        self.requests = requests
        self.message = Message(self.requests)
        self.document = Document(self.requests)
        self.caption = Caption()

    def send(
        self,
        document_paths: list,
        caption: str = None,
        media_type: str = 'document',
        parse_mode: str = None,
        max_request_attempts: int = 10
    ) -> None:
        """
        Sends a media group. If the caption length exceeds the maximum allowed, it sends the caption as a document.

        :param document_paths: List of paths to the documents to be sent.
        :param caption: The caption for the media group. Default is None.
        :param media_type: The type of media (e.g., 'document', 'photo'). Default is 'document'.
        :param parse_mode: The parse mode for the caption (e.g., 'Markdown', 'HTML'). Default is Config.DEFAULT_PARSE_MOD.
        :param max_request_attempts: Maximum number of attempts to send the media group. Default is 10.
        :return: None
        """

        if not document_paths:
            return self.message.send(f"No files to send. {caption if caption else ''}", out_msg=True)

        if caption and len(caption) > self._MAX_CAPTCHA_LENGTH:
            document_paths.append(self.message.make_doc(caption, 'full_caption.txt'))

        for chung in self._get_group_chunks(document_paths):
            while max_request_attempts > 0:
                files, data = self._get_data(chung, media_type, caption, parse_mode or self._DEFAULT_PARSE_MOD)

                if self.requests.post('sendMediaGroup', data=data, files=files):
                    break

                max_request_attempts -= 1

    def _get_data(self, document_paths: list, media_type: str, caption: str, parse_mode: str) -> tuple:
        """
        Prepares the data and files for sending a media group.

        :param document_paths: List of paths to the documents to be sent.
        :param media_type: The type of media (e.g., 'document', 'photo').
        :param caption: The caption for the media group.
        :param parse_mode: The parse mode for the caption (e.g., 'Markdown', 'HTML').
        :return: A tuple containing the files and the data to be sent.
        """
        files, media = {}, []

        for doc_path in document_paths:
            files[basename(doc_path)] = open(self.document.prepare(doc_path), 'rb')
            media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))

        if caption:
            media[-1]['caption'] = self.caption.prepare(caption)

        media[-1]['parse_mode'] = parse_mode

        return files, {'chat_id': self.requests.auth.chat_id, 'media': dumps(media)}

    def _get_group_chunks(self, document_paths: list) -> list:
        """
        Splits the document paths into chunks of the maximum allowed size for a media group.

        :param document_paths: List of paths to the documents to be sent.
        :return: A list of document path chunks.
        """
        return [document_paths[i:i + self._MAX_LENGTH] for i in range(0, len(document_paths), self._MAX_LENGTH)]
