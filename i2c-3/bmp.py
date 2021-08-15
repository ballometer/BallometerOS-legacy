import busio
import adafruit_bmp280

class BMP:
    def __init__(self):
        self._sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c=busio.I2C(24, 23), address=0x76)
    
    @property
    def temperature(self):
        '''returns the temperature in Kelvin'''
        T = self._sensor.temperature # deg C
        return T + 273.15 # K
    
    @property
    def pressure(self):
        '''returns the pressure in Pa'''
        p = self._sensor.pressure # hPa
        return p * 1e2 # Pa

   