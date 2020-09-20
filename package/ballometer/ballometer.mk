################################################################################
#
# Ballometer
#
################################################################################

BALLOMETER_VERSION = 1.0.2
BALLOMETER_SOURCE = v$(BALLOMETER_VERSION).tar.gz
BALLOMETER_SITE = https://github.com/wipfli/ballometer/archive
BALLOMETER_LICENSE = MIT

define BALLOMETER_INSTALL_TARGET_CMDS
	rm -rf $(TARGET_DIR)/root/ballometer
	mkdir $(TARGET_DIR)/root/ballometer
	cp -Rp $(@D)/* $(TARGET_DIR)/root/ballometer
endef

$(eval $(generic-package))