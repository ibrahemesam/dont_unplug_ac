import sys

if sys.platform == 'win32':
    from .win32 import MasterMixer
    BUF_SIZE = 1024 # a lower BUF_SIZE to reduce latency on Windows
elif sys.platform == 'linux':
    from .linux import MasterMixer
    BUF_SIZE = 1024 * 1024 # a heigher BUF_SIZE to reduce CPU usage
else:
    raise Exception(f"Unsupported Platform: {sys.platform}")

master_mixer = MasterMixer()

from threading import Thread, Event
import pyaudio
import wave
import os



class AudioFile(Thread):
    def __init__(self, filename):
        ## Init audio stream ##
        try:
            self.wf = wave.open(filename, 'rb')
        except wave.Error:
            print(f"Unsupported audio file: {filename}")
            os._exit(0)
        # supress STDERR to prevent showing PyAudio errors (eg: ALSA errors in Linux)
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        sys.stderr.flush()
        os.dup2(devnull, 2)
        os.close(devnull)
        # ...
        self.p = pyaudio.PyAudio()
        # undo supressing STDERR
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
        # ...
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )
        ## set events and flags ##
        self.evt_playing = Event()
        self.__exit_thread = False
        ## init threading.Thread ##
        super().__init__()
        self.start()

    def run(self):
        ## Play entire file ##
        while True:
            self.evt_playing.wait()
            if self.__exit_thread:
                return
            while self.__loops:
                self.wf.setpos(0) # seek to audio start
                data = self.wf.readframes(BUF_SIZE)
                while data != b'':
                    if self.__stop_playing:
                        break
                    self.stream.write(data)
                    data = self.wf.readframes(BUF_SIZE)
                    self.evt_playing.wait()
                if self.__stop_playing:
                    break
                self.__loops -= 1

    def play(self, loops=1):
        # loops: +ve value for a <count> OR -ve for <infinity>
        self.__loops = loops
        self.__stop_playing = False
        self.evt_playing.set()
        
    def pause(self):
        self.evt_playing.clear()
    
    def stop(self):
        self.__stop_playing = True
        self.evt_playing.clear()

    def close(self):
        ## Graceful shutdown ##
        # exit thread
        self.__exit_thread = True
        self.evt_playing.set()
        # close PyAudio onject
        self.stream.close()
        self.p.terminate()
        
    __del__ = close


class Beep:
    def __init__(self, audio_filename):
        self.audio = AudioFile(audio_filename)
        self.is_playing = False
        self.__get_master_volume_status()

    def __get_master_volume_status(self):
        self.master_volume = master_mixer.volume
        self.master_is_muted = master_mixer.muted

    def play(self):
        if self.is_playing:
            return
        self.__get_master_volume_status()
        master_mixer.muted = 0
        master_mixer.set_volume_to_max() # set master volume to MAX
        self.is_playing = True
        self.audio.play(loops=-1)

    def stop(self):
        if not self.is_playing:
            return
        self.is_playing = False
        self.audio.stop()
        master_mixer.muted = self.master_is_muted
        master_mixer.volume = self.master_volume # return master volume to previous value

__all__ = ('Beep',)

if __name__ == '__main__': # or 1:
    a = AudioFile("data/me.meme.wav")
    try:
        a.play()
    except KeyboardInterrupt:
        pass
    from time import sleep
    print(1)
    sleep(5)
    print(2)
    a.close()
