# -*- coding: utf-8 -*-
from ..host_control import HostInfo

if  HostInfo().release not in ['vista']:
    from .image import Image

