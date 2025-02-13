# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Package(ABC):

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def install(self) -> None: ...
