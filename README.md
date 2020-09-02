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

In the boot filesystem a file called ```select.txt``` determines which rootfs should be used. If this file content is ```cmdline=cmdline-p2.txt```, then the system boots into mmcblk0p2 and if the content is ```cmdline=cmdline-p3.txt```, then it boots into mmcblk0p3.

## Build

```bash
git clone https://github.com/wipfli/buildroot.git
cd buildroot
make ballometer_defconfig
```

Create a file called ```./board/ballometer/data/etc/wpa_supplicant.conf``` and fill it with your wifi details:
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

