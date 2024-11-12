# exit app if one instance of it is already running
# exit if a lock file is locked


import sys

if sys.platform == 'linux':
    from .linux import is_file_locked
elif sys.platform == 'win32':
    from .win32 import is_file_locked

from os import _exit
from os.path import join, realpath, dirname

try:
    from __main__ import __file__
except ImportError:
    __file__ = sys.executable

if is_file_locked(join(dirname(realpath(__file__)), ".app.lock")):
    print("App Already Running")
    _exit(1)