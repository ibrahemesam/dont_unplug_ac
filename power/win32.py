from win32con import WM_POWERBROADCAST, PBT_APMPOWERSTATUSCHANGE
from threading import Thread
import win32api, win32gui

# Get power status of the system using ctypes to call GetSystemPowerStatus
# See: https://stackoverflow.com/a/6156606/10701585
from ctypes import (
    wintypes,
    POINTER as ctypes_POINTER,
    WinError as ctypes_WinError,
    pointer as ctypes_pointer,
    windll as ctypes_windll,
    Structure as ctypes_Structure,
    )
class SYSTEM_POWER_STATUS(ctypes_Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
    ]
SYSTEM_POWER_STATUS_P = ctypes_POINTER(SYSTEM_POWER_STATUS)
GetSystemPowerStatus = ctypes_windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL
def is_charger_plugged():
    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes_pointer(status)):
        raise ctypes_WinError()
    result = status.ACLineStatus
    if result == 255:
        raise UnknownAcPowerStatusException("Unknown AC power status")
    return result

class UnknownAcPowerStatusException(Exception):
    # raised when SYSTEM_POWER_STATUS->ACLineStatus == 255
    # See: https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-system_power_status#members
    ...

threads_container = [] # container for theads to prevent deletion by garbage collector
def set_on_ac_adapter_state_change(on_plugged, on_unplugged):
    """
    Listens to Win32 `WM_POWERBROADCAST` messages
    and trigger a callback when a AC Adapter has been plugged in or out
    By creating a window for listening to messages
    See:
        https://learn.microsoft.com/en-us/windows/win32/power/wm-powerbroadcast
        https://docs.microsoft.com/en-us/windows/win32/learnwin32/creating-a-window#creating-the-window
        https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindoww
    """
    callback = (on_unplugged, on_plugged)
    def __on_message(hwnd: int, msg: int, wparam: int, lparam: int):
        if msg == WM_POWERBROADCAST and wparam == PBT_APMPOWERSTATUSCHANGE:
            # "Power status has changed."
            callback[is_charger_plugged()]()
        return 0
    def __create_window():
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = __on_message
        class_name = "Windows Partition Monitor"
        wc.lpszClassName = class_name
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        win32gui.CreateWindow(class_atom, class_name, 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None) # returns hwnd
        win32gui.PumpMessages()
    thread = Thread(target=__create_window)
    threads_container.append(thread)
    thread.start()
    return thread

__all__ = ('is_charger_plugged', 'set_on_ac_adapter_state_change')
    
if __name__ == '__main__':
    import signal
    import os
    signal.signal(signal.SIGINT, lambda sig, frame: (print("^C"), os._exit(1)))
    os.system('cls')
    def on_plugged():
        print('plugged')
    def on_unplugged():
        print('unplugged')
    set_on_ac_adapter_state_change(on_plugged=on_plugged, on_unplugged=on_unplugged)
    # sleep forever
    from time import sleep
    while True:
        sleep(999999)

