import busio
import adafruit_tsl2591
import time

sensor = adafruit_tsl2591.TSL2591(busio.I2C(24, 23))
sensor.gain = adafruit_tsl2591.GAIN_LOW

print('Light: {0}lux'.format(sensor.lux))
print('Visible: {0}'.format(sensor.visible))
print('Infrared: {0}'.format(sensor.infrared))
