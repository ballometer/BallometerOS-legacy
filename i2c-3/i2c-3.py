import busio
import adafruit_bmp280
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import adafruit_sht31d
import adafruit_tsl2591

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c=busio.I2C(24, 23), address=0x76)

bmp280.seaLevelhPa = 1013.25

print("\nTemperature: %0.1f C" % bmp280.temperature)
print("Pressure: %0.3f hPa" % bmp280.pressure)
print("Altitude = %0.2f meters" % bmp280.altitude)

   
i2c = busio.I2C(24, 23)

accel = adafruit_lsm303_accel.LSM303_Accel(i2c, address=0x18)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)

i2c = busio.I2C(24, 23)
sensor = adafruit_sht31d.SHT31D(i2c)

print(sensor.temperature)

print(sensor.relative_humidity)

sensor = adafruit_tsl2591.TSL2591(busio.I2C(24, 23))
sensor.gain = adafruit_tsl2591.GAIN_LOW

print('Light: {0}lux'.format(sensor.lux))
print('Visible: {0}'.format(sensor.visible))
print('Infrared: {0}'.format(sensor.infrared))