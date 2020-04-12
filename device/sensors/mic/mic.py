import os
import numpy as np
from scipy.io import wavfile

recordLength = 0.1 # seconds
dir = os.path.dirname(os.path.realpath(__file__))

command = 'ffmpeg -y -loglevel panic -f alsa -ac 1 -ar 48000 -i plughw:1,0 -t %1.1f %s/sample.wav' % (recordLength, dir)

os.system(command)

fs, data = wavfile.read(dir + '/sample.wav')

volumeRMS = np.sqrt(np.mean(data ** 2))

print(volumeRMS)
