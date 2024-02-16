#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
from enum import Enum


class Platform(Enum):
    windows = 1
    mac = 2
    linux = 3
    others = 4


def get_platform():
    import platform
    sys_platform = platform.platform().lower()
    if "windows" in sys_platform:
        return Platform.windows
    elif "macos" in sys_platform:
        return Platform.mac
    elif "linux" in sys_platform:
        return Platform.linux
    else:
        return Platform.others


def get_base_dir():
    platform = get_platform()
    username = getpass.getuser()

    if platform == Platform.mac:
        return f"/Users/{username}/Downloads/rime_corpus"
    elif platform == Platform.linux:
        return f"/home/{username}/Downloads/rime_corpus"
    else:
        raise ValueError()
