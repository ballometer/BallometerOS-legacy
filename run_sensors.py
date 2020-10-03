import ballometer
import time

bmp = ballometer.BMP()
sht = ballometer.SHT()
tsl = ballometer.TSL()
lsm = ballometer.LSM()

store = ballometer.Store()

while True:
    store.save(key='bmp_pressure', value=bmp.pressure)
    store.save(key='bmp_temperature', value=bmp.temperature)

    store.save(key='sht_temperature', value=sht.temperature)
    store.save(key='sht_humidity', value=sht.humidity)

    store.save(key='tsl_visible', value=tsl.visible)
    store.save(key='tsl_infrared', value=tsl.infrared)

    store.save(key='lsm_accel_x', value=lsm.accel_x)
    store.save(key='lsm_accel_y', value=lsm.accel_y)
    store.save(key='lsm_accel_z', value=lsm.accel_z)

    store.save(key='lsm_mag_x', value=lsm.mag_x)
    store.save(key='lsm_mag_y', value=lsm.mag_y)
    store.save(key='lsm_mag_z', value=lsm.mag_z)

    time.sleep(1.0)
