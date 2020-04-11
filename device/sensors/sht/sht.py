import adafruit_sht31d
import busio

i2c = busio.I2C(24, 23)
sensor = adafruit_sht31d.SHT31D(i2c)

print(sensor.temperature)
