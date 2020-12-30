################################################################################
#
# local-ui
#
################################################################################

LOCAL_UI_VERSION = 1.0.0
LOCAL_UI_SOURCE = build.tar.gz
LOCAL_UI_SITE = https://github.com/wipfli/local-ui/releases/download/v$(LOCAL_UI_VERSION)
LOCAL_UI_LICENSE = MIT

define LOCAL_UI_INSTALL_TARGET_CMDS
	rm -rf $(TARGET_DIR)/root/local-ui
	mkdir $(TARGET_DIR)/root/local-ui
	cp -Rp $(@D)/* $(TARGET_DIR)/root/local-ui
endef

$(eval $(generic-package))