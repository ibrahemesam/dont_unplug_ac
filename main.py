#!/bin/env python
"""
    Plays a Beep sound when AC adapter is unplugged
    so that the Laptop do NOT shutdown suddenly
    cause my battery is almost dead [:
"""

import os, sys
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.append(APP_ROOT) # add APP_ROOT to PYTHONPATH
os.chdir(APP_ROOT) # cd into APP_ROOT

# init beep
from audio import Beep
beep = Beep("./beep.wav") # NOTE: audio file to play when AC Adapter gets unplugged
# only WAV files [PCM signed 16-bit little-endian] are supported
# to convert an audio file to into the supported WAV type:
# $ ffmpeg -i input.mp3 -acodec pcm_s16le output.wav

# check current power state
from power import is_charger_plugged
if not is_charger_plugged():
    print('already unplugged')
    beep.play()

# Register signal handler to exit on SIGINT
import signal
signal.signal(signal.SIGTERM, lambda sig, frame:\
    (print('Received SIGTERM. Terminating gracefully...'), os._exit(0)))

# init power monitor
def on_plugged():
    print('plugged')
    beep.stop()

def on_unplugged():
    print('unplugeged')
    beep.play()

from power import set_on_ac_adapter_state_change
set_on_ac_adapter_state_change(on_plugged=on_plugged, on_unplugged=on_unplugged)

# sleep forever
from time import sleep
try:
    while True:
        sleep(999999)
except KeyboardInterrupt:
    os._exit(0)
