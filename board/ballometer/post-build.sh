#!/bin/sh

set -u
set -e

# Add a console on tty1
if [ -e ${TARGET_DIR}/etc/inittab ]; then
    grep -qE '^tty1::' ${TARGET_DIR}/etc/inittab || \
	sed -i '/GENERIC_SERIAL/a\
tty1::respawn:/sbin/getty -L  tty1 0 vt100 # HDMI console' ${TARGET_DIR}/etc/inittab
fi

cp board/ballometer/boot/cmdline-p2.txt output/images/rpi-firmware/cmdline-p2.txt
cp board/ballometer/boot/cmdline-p3.txt output/images/rpi-firmware/cmdline-p3.txt
cp board/ballometer/boot/config.txt output/images/rpi-firmware/config.txt
cp board/ballometer/boot/select.txt output/images/rpi-firmware/select.txt