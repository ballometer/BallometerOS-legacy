import alsaaudio
import audioop

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)


while True:
    l, data = inp.read()
    if l:
        print(audioop.rms(data, 2))
