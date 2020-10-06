import ballometer
import time

mic = ballometer.Mic()
store = ballometer.Store()

while True:
    mic_sound_level = 0
    for _ in range(10):
        mic_sound_level += mic.sound_level
        time.sleep(0.1)
    store.save(key='mic_sound_level', value=mic_sound_level)
