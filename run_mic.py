import ballometer


mic = ballometer.Mic()
store = ballometer.Store()

while True:
    store.save(key='mic_sound_level_1s', value=mic.sound_level_1s)
