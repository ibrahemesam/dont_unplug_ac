# control master volume in Linux
from os import system as os_system
import alsaaudio

alsamixer = alsaaudio.Mixer('Master')

class MasterMixer:
    @property
    def muted(self):
        # get muted state
        return 1 in alsamixer.getmute()
    
    @muted.setter
    def muted(self, value):
        # set muted state
        return alsamixer.setmute(int(value))
    
    @property
    def volume(self):
        # get master volume
        return alsamixer.getvolume()
    
    @volume.setter
    def volume(self, value):
        # set master volume
        os_system(f'pactl set-sink-volume @DEFAULT_SINK@ {r"% ".join(str(i) for i in value)}%') # assuming PulseAudio is used
        
    def set_volume_to_max(self):
        os_system('pactl set-sink-volume @DEFAULT_SINK@ 150%') # assuming PulseAudio is used

__all__ = ('MasterMixer',)
