try:
    import alsaaudio
    import audioop
except ImportError:
    pass


class Mic:
    def __init__(self):
        self._inp = alsaaudio.PCM(
            alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

    @property
    def sound_level(self):
        success = False
        while not success:
            success, data = self._inp.read()
        return float(audioop.rms(data, 2))
