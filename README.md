# buildroot

Builds the operating system and environment for the ballometer device.

## Overview

A dual partition approad with an active and a passive rootfs allows for atomic updates of the entire operating system including installed programs.

There are four partitions:

 * mmcblk0p1 boot
 * mmcblk0p2 rootfs A
 * mmcblk0p3 rootfs B
 * mmcblk0p4 data
 
The size of partitions 2 and 3 is at least 4G. 

In the boot filesystem a file called ```select.txt``` determines which rootfs and os boot folder should be used. 
If this file content is 
```
cmdline=cmdline-p2.txt
os_prefix=os-p2/
```
then the system boots into partition mmcblk0p2 and uses the os files from boot folder os-p2. 

If the content of ```select.txt``` is
```
cmdline=cmdline-p3.txt
os_prefix=os-p3/
```
then the system boots into partition mmcblk0p3 and uses the os files from boot folder os-p3.

## Build

```bash
git clone https://github.com/wipfli/buildroot.git
cd buildroot
make ballometer_defconfig
```

Create a file called ```board/ballometer/data/wpa_supplicant.conf``` and fill it with your wifi details:
```
ctrl_interface=/var/run/wpa_supplicant
ap_scan=1
 
network={
   ssid="your-wifi-name"
   psk="your-wifi-password"
}
```

To build the whole system run
```bash
make
```

This creates a bootable image in ```output/images/sdcard.img```.

## Create Release Files

Write the tag name into a file that will appear at ```/root/release.json``` and give a tag to the latest commit with:

```bash
echo "\"v1.2.4\"" > board/ballometer/rootfs-overlay/root/release.json
git commit -m "Bump to version v1.2.4" board/ballometer/rootfs-overlay/root/release.json
git tag -a v1.2.4 -m "Add new features"
git push --follow-tags
```

A release contains the following files
 * ```rootfs.ext2.xz```
 * ```boot.tar.xz```
 * ```checksums.json```

To create ```rootfs.ext2.xz``` run:
```bash
cd output/images
xz -kv9 rootfs.ext2
```
To create ```boot.tar.xz``` run:
```bash
cd output/images/os-p2
tar -cf ../boot.tar .
cd ..
xz -kv9 boot.tar
```
The checksums file ```checksums.json``` is created by running on the ballometer device after the installation a function of the update process. These checksums are meant to check for file integrity *after* the installation.


## Resize ```/data``` partition

Plug the SD card with the full system image into a raspberry pi. Check that the devices appear with
```bash
ls /dev/sda*
# /dev/sda   /dev/sda1  /dev/sda2  /dev/sda3  /dev/sda4
```

Resize the partition with fdisk:

```bash
fdisk /dev/sda
# d (delete)
# 4 (partition 4)
# n (new)
# p (primary)
# w (write)
``` 

Resize filesystem to fill partition:

```bash
resize2fs /dev/sda4
# Resizing the filesystem on /dev/sda4 to 124123132 (1k) blocks.
# The filesystem on /dev/sda4 is now 124123132 (1k) blocks long.
```

## GitHub Actions Workflow

```bash
git commit -m "something something"
git tag -a v1.1.20 -m "version 1.1.20"
git push origin v1.1.20
```

for prereleases use ```v1.1.20-rc.1```.
