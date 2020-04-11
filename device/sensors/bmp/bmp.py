import busio
import adafruit_bmp280

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c=busio.I2C(24, 23), address=0x76)

bmp280.seaLevelhPa = 1013.25

print("\nTemperature: %0.1f C" % bmp280.temperature)
print("Pressure: %0.3f hPa" % bmp280.pressure)
print("Altitude = %0.2f meters" % bmp280.altitude)
