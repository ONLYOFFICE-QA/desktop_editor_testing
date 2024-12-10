# -*- coding: utf-8 -*-
from frameworks.host_control import HostInfo

if HostInfo().os == 'windows':
    from .windows_window import WindowsWindow as Window
else:
    from .linux_window import LinuxWindow as Window
