################################################################################
#
# python-sysv_ipc
#
################################################################################

PYTHON_SYSV_IPC_VERSION = 1.0.1
PYTHON_SYSV_IPC_SOURCE = sysv_ipc-$(PYTHON_SYSV_IPC_VERSION).tar.gz
PYTHON_SYSV_IPC_SITE = https://files.pythonhosted.org/packages/57/8a/9bbb064566320cd66c6e32c35db76d43932d7b94348f0c4c1e74d03ec261
PYTHON_SYSV_IPC_SETUP_TYPE = setuptools
PYTHON_SYSV_IPC_LICENSE = BSD
PYTHON_SYSV_IPC_LICENSE_FILES = LICENSE

$(eval $(python-package))
