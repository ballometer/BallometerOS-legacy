import busio
import adafruit_sht31d

class SHT:
    def __init__(self):
        self._sensor = adafruit_sht31d.SHT31D(i2c_bus=busio.I2C(24, 23))
        
    @property
    def temperature(self):
        '''returns the temperature in Kelvin'''
        T = self._sensor.temperature # deg C
        return T + 273.15 # K
    
    @property
    def humidity(self):
        '''returns the relative humidity in percent'''
        RH = self._sensor.relative_humidity # percent
        return RH # percent