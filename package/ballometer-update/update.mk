################################################################################
#
# Ballometer Update
#
################################################################################

BALLOMETER_UPDATE_VERSION = 0.1.0
BALLOMETER_UPDATE_SOURCE = v$(BALLOMETER_UPDATE_VERSION).tar.gz
BALLOMETER_UPDATE_SITE = https://github.com/wipfli/update/archive
BALLOMETER_UPDATE_LICENSE = APACHE

define BALLOMETER_UPDATE_INSTALL_TARGET_CMDS
endef

$(eval $(generic-package))