################################################################################
#
# python-pyftdi
#
################################################################################

PYTHON_PYFTDI_VERSION = 0.51.2
PYTHON_PYFTDI_SOURCE = pyftdi-$(PYTHON_PYFTDI_VERSION).tar.gz
PYTHON_PYFTDI_SITE = https://files.pythonhosted.org/packages/64/14/f502462dfd8045884a03eb3920d49f359cdaf38d97d367469bf84c0847ad
PYTHON_PYFTDI_SETUP_TYPE = setuptools
PYTHON_PYFTDI_LICENSE = BSD

$(eval $(python-package))
