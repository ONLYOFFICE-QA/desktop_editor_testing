# -*- coding: utf-8 -*-
from tempfile import gettempdir

from .Proxy import Proxy
from .Send import TelegramRequests, Message, MediaGroup, Document


class Telegram:
    """
    Provides methods to interact with the Telegram Bot API for sending messages, documents, and media groups.

    :param token: Telegram bot token.
    :param chat_id: ID of the chat where messages are sent.
    :param tmp_dir: Temporary directory for storing files. Default is system temporary directory.
    :param proxy: Proxy settings for HTTP connections.
    :param proxy_file: Path to a file containing proxy settings.
    :param max_request_attempts: Maximum number of attempts to send requests. Default is 10.
    :param interval: Interval between retries in seconds. Default is 5 seconds.
    """

    def __init__(
            self,
            token: str = None,
            chat_id: str = None,
            tmp_dir: str = gettempdir(),
            proxy: Proxy = None,
            proxy_file:  str = None,
            max_request_attempts: int = 10,
            interval: int = 5
    ):
        self.tmp_dir = tmp_dir
        self.max_request_attempts = max_request_attempts
        self.requests = TelegramRequests(token, chat_id, proxy, proxy_file, max_request_attempts, interval)

    def send_message(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        """
        Sends a text message to the specified chat.

        :param message: The message to send.
        :param out_msg: If True, prints the message to standard output. Default is False.
        :param parse_mode: The parse mode for the message (e.g., 'Markdown', 'HTML'). Default is None.
        :return: None
        """
        Message(self.requests, self.tmp_dir).send(message=message, out_msg=out_msg, parse_mode=parse_mode)


    def send_document(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        """
        Sends a document to the specified chat.

        :param document_path: Path to the document to send.
        :param caption: Caption for the document. Default is an empty string.
        :param parse_mode: The parse mode for the caption (e.g., 'Markdown', 'HTML'). Default is None.
        :return: None
        """
        Document(self.requests, self.tmp_dir).send(document_path, caption, parse_mode)

    def send_media_group(self,
            document_paths: list,
            caption: str = None,
            media_type: str = 'document',
            parse_mode: str = None,
    ) -> None:
        """
        Sends a media group to the specified chat.

        :param document_paths: List of paths to the media files to send.
        :param caption: Caption for the media group. Default is None.
        :param media_type: Type of media ('photo', 'video', 'audio', 'document', 'voice', 'animation'). Default is 'document'.
        :param parse_mode: The parse mode for the caption (e.g., 'Markdown', 'HTML'). Default is None.
        :param max_request_attempts: Maximum number of attempts to send the media group. Default is 10.
        :return: None
        """
        MediaGroup(self.requests).send(
            document_paths=document_paths,
            caption=caption,
            media_type=media_type,
            parse_mode=parse_mode,
            max_request_attempts=self.max_request_attempts
        )
