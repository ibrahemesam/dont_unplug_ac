from pyudev import Context, Monitor
from threading import Thread
import os

ac_online_filename = '/sys/class/power_supply'
adapter_found = False
for i in os.listdir(ac_online_filename):
    if i.startswith('A'):
        adapter_found = i
        break
if not adapter_found:
    exit('can\'t find AC adapter filename')
ac_online_filename += '/' + adapter_found + '/online'

def is_charger_plugged():
    with open(ac_online_filename, 'rt') as f:
        return '1' in f.read()

threads_container = [] # container for theads to prevent deletion by garbage collector
def set_on_ac_adapter_state_change(on_plugged, on_unplugged):
    callback = (on_unplugged, on_plugged)
    def __monitor():
        ctx = Context()
        monitor = Monitor.from_netlink(ctx)
        monitor.filter_by(subsystem='power_supply', device_type="power_supply")
        for _, dev in monitor:
            if f'power_supply/{adapter_found}' in dev.device_path:
                # Power status has changed.
                callback[is_charger_plugged()]()
    thread = Thread(target=__monitor)
    threads_container.append(thread)
    thread.start()
    return thread

__all__ = ('is_charger_plugged', 'set_on_ac_adapter_state_change')

if __name__ == '__main__':
    import signal
    import os
    signal.signal(signal.SIGINT, lambda sig, frame: (print("^C"), os._exit(1)))
    os.system('clear')
    def on_plugged():
        print('plugged')
    def on_unplugged():
        print('unplugged')
    set_on_ac_adapter_state_change(on_plugged=on_plugged, on_unplugged=on_unplugged)
    # sleep forever
    from time import sleep
    while True:
        sleep(999999)
