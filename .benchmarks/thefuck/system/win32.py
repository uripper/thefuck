import os
import colorama
import msvcrt
from pathlib import Path
import win_unicode_console
from .. import const


def init_output():
    win_unicode_console.enable()
    colorama.init()


def get_key():
    ch = msvcrt.getwch()
    if ch in ('\x00', '\xe0'):  # arrow or function key prefix?
        ch = msvcrt.getwch()  # second call returns the actual key code

    if ch in const.KEY_MAPPING:
        return const.KEY_MAPPING[ch]
    if ch == 'H':
        return const.KEY_UP
    return const.KEY_DOWN if ch == 'P' else ch


def open_command(arg):
    return f'cmd /c start {arg}'

def _expanduser(self):
    return self.__class__(os.path.expanduser(str(self)))

Path.expanduser = _expanduser
