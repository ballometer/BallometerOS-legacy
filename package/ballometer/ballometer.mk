################################################################################
#
# Ballometer
#
################################################################################

BALLOMETER_VERSION = 1.0.1
BALLOMETER_SOURCE = v$(BALLOMETER_VERSION).tar.gz
BALLOMETER_SITE = https://github.com/wipfli/ballometer/archive
BALLOMETER_LICENSE = MIT

define BALLOMETER_INSTALL_TARGET_CMDS
	mkdir $(TARGET_DIR)/root/ballometer
	cp -Rp $(@D)/* $(TARGET_DIR)/root/ballometer
endef

$(eval $(generic-package))