#!/bin/sh

set -u
set -e

cp board/ballometer/boot/cmdline-p2.txt ${O}/images/rpi-firmware/cmdline-p2.txt
cp board/ballometer/boot/cmdline-p3.txt ${O}/images/rpi-firmware/cmdline-p3.txt
cp board/ballometer/boot/config.txt ${O}/images/rpi-firmware/config.txt
cp board/ballometer/boot/select.txt ${O}/images/rpi-firmware/select.txt

rm ${O}/images/data.ext4 ${O}/images/data.ext2
${O}/host/sbin/mkfs.ext4 -d board/ballometer/data -r 1 -N 0 -m 5 -L "data" -O ^64bit ${O}/images/data.ext2 "100M"
ln -sf data.ext2 ${O}/images/data.ext4