################################################################################
#
# python-adafruit-circuitpython-lsm303-accel
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_VERSION = 1.1.2
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_SOURCE = adafruit-circuitpython-lsm303-accel-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_SITE = https://files.pythonhosted.org/packages/a2/05/5986b1e1394950ca9f534d62ca655238243bdced161285bf42d4e3228e9f
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303_ACCEL_LICENSE_FILES = LICENSE

$(eval $(python-package))
