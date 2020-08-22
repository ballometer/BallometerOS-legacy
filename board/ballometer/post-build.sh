#!/bin/sh

set -u
set -e

cp board/ballometer/boot/cmdline-p2.txt output/images/rpi-firmware/cmdline-p2.txt
cp board/ballometer/boot/cmdline-p3.txt output/images/rpi-firmware/cmdline-p3.txt
cp board/ballometer/boot/config.txt output/images/rpi-firmware/config.txt
cp board/ballometer/boot/select.txt output/images/rpi-firmware/select.txt