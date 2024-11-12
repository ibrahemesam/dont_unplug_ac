from os import open, O_RDONLY, O_CREAT # , close
from fcntl import flock, LOCK_EX, LOCK_NB

def is_file_locked(filename):
    fd = open(filename, O_RDONLY | O_CREAT)
    try:
        flock(fd, LOCK_EX | LOCK_NB)
        return False  # File is not locked
    except BlockingIOError:
        return True  # File is locked
    # finally:
    #     os.close(fd)