# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC

class Send(ABC):
    """
    Abstract base class defining a send interface for derived classes.

    Subclasses must implement the send method.
    """

    @abstractmethod
    def send(self, *args, **kwargs) -> None:
        """
        Abstract method to send data. Must be implemented by subclasses.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: None
        """
        pass
