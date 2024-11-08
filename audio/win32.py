# control master volume in Windows
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

class MasterMixer:
    @property
    def muted(self):
        # get muted state
        return volume.GetMute()
    
    @muted.setter
    def muted(self, value):
        # set muted state
        return volume.SetMute(int(value), None)
    
    @property
    def volume(self):
        # get master volume
        return volume.GetMasterVolumeLevelScalar()
    
    @volume.setter
    def volume(self, value):
        # set master volume
        if value > 1:
            value /= 100
        volume.SetMasterVolumeLevelScalar(value, None)

    def set_volume_to_max(self):
        volume.SetMasterVolumeLevelScalar(1, None)

__all__ = ('MasterMixer',)