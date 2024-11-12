from win32file import LockFileEx # , UnlockFileEx
from os import open, O_RDWR, O_CREAT # , close
from win32con import LOCKFILE_FAIL_IMMEDIATELY, LOCKFILE_EXCLUSIVE_LOCK
from msvcrt import get_osfhandle
from pywintypes import OVERLAPPED

def is_file_locked(filename):
    try:
        # Open the file with exclusive access
        fd = open(filename, O_RDWR | O_CREAT)
        # Try to lock the file
        try:
            # Lock the file            
            LockFileEx(
                get_osfhandle(fd),
                (LOCKFILE_FAIL_IMMEDIATELY | LOCKFILE_EXCLUSIVE_LOCK),
                0, -0x10000, OVERLAPPED())
            return False  # File is not locked
        except Exception as e:
            print(f"Error locking file {filename}: {e}")
            return True  # File is locked
        # finally:
        #     # Unlock the file before closing it
        #     UnlockFileEx(fd, 0, 0, None)
        #     close(fd)
    except Exception as e:
        print(f"Error with file operations {filename}: {e}")
        return True  # Assume locked if any error occurs