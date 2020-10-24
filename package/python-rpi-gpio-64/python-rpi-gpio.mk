################################################################################
#
# python-rpi-gpio-64
#
################################################################################

PYTHON_RPI_GPIO_64_VERSION = 0.7.0
PYTHON_RPI_GPIO_64_SOURCE = RPi.GPIO-$(PYTHON_RPI_GPIO_64_VERSION).tar.gz
PYTHON_RPI_GPIO_64_SITE = https://sourceforge.net/projects/raspberry-gpio-python/files
PYTHON_RPI_GPIO_64_LICENSE = MIT
PYTHON_RPI_GPIO_64_LICENSE_FILES = LICENCE.txt
PYTHON_RPI_GPIO_64_SETUP_TYPE = distutils

$(eval $(python-package))
