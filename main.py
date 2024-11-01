#!/bin/env python
"""
Plays a Beep sound when AC adapter is unplugged
so that the Laptop do NOT shutdown suddenly
cause my battery is almost dead [:
"""
from pyudev import Context, Monitor
import alsaaudio
import signal
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
mixer = __import__('pygame').mixer
alsamixer = alsaaudio.Mixer('Master')
mixer.init()
HERE = os.path.dirname(os.path.realpath(__file__))
os.chdir(HERE)


class Beep:
    def __init__(self, audio_filename):
        self.plays = mixer.Sound(audio_filename)
        self.plays.set_volume(1.0)
        self.is_playing = False
        self.__get_master_volume_status()

    def __get_master_volume_status(self):
        self.master_volume = alsamixer.getvolume()
        self.master_is_muted = 1 in alsamixer.getmute()

    def play(self):
        if self.is_playing:
            return
        self.__get_master_volume_status()
        alsamixer.setmute(0)
        os.system('pactl set-sink-volume @DEFAULT_SINK@ 150%') # set master volume to 150%
        self.is_playing = True
        self.plays.play(loops=-1)

    def stop(self):
        if not self.is_playing:
            return
        self.is_playing = False
        self.plays.stop()
        alsamixer.setmute(self.master_is_muted)
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ {r"% ".join(str(i) for i in self.master_volume)}%') # return master volume to previous


ac_online_filename = '/sys/class/power_supply/AC/online'
if not os.path.exists(ac_online_filename):
    ac_online_filename = ac_online_filename.replace('AC', 'ACAD')


def is_charger_plugged():
    with open(ac_online_filename, 'rt') as f:
        return '1' in f.read()


# init udev monitor
ctx = Context()
monitor = Monitor.from_netlink(ctx)
monitor.filter_by(subsystem='power_supply', device_type="power_supply")

# init beep
beep = Beep("./beep.mp3") # NOTE: audio file to play when AC Adapter gets unplugged


if not is_charger_plugged():
    beep.play()


def signal_handler(sig, frame):
    print('Received SIGTERM. Terminating gracefully...')
    os._exit(0)


# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)

try:
    for _, dev in monitor:
        # print(dev.device_path)
        if 'power_supply/ACAD' in dev.device_path:
            plugged = is_charger_plugged()
            if plugged:
                print('plugged')
                beep.stop()
            else:
                print('unplugeged')
                beep.play()

except KeyboardInterrupt:
    print("Monitoring stopped")

