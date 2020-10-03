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
            l, data = self._inp.read()
            success = not l
        return float(audioop.rms(data, 2))
