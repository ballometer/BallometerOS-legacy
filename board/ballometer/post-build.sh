#!/bin/sh

set -u
set -e

cp board/ballometer/boot/cmdline-p2.txt output/images/rpi-firmware/cmdline-p2.txt
cp board/ballometer/boot/cmdline-p3.txt output/images/rpi-firmware/cmdline-p3.txt
cp board/ballometer/boot/config.txt output/images/rpi-firmware/config.txt
cp board/ballometer/boot/select.txt output/images/rpi-firmware/select.txt

rm output/images/data.ext4 output/images/data.ext2
output/host/sbin/mkfs.ext4 -d board/ballometer/data -r 1 -N 0 -m 5 -L "data" -O ^64bit output/images/data.ext2 "100M"
ln -sf data.ext2 output/images/data.ext4