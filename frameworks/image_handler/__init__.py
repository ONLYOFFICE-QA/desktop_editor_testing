# -*- coding: utf-8 -*-
from frameworks.host_control import HostInfo

if  HostInfo().release in ['vista', 'xp']:
    from .image_old_system import ImageOldSystem as Image
else:
    from .image_new_system import ImageNewSystem as Image
