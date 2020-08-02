# buildroot

Builds the operating system and environment for the ballometer device.

## Overview

This fork of the buildroot project adds the following custom files:

 * A custom defconfig file in ```configs/ballometer_raspberrypi3_defconfig```
 * Custom ```post-build.sh``` and ```post-image.sh``` scripts and other files in ```board/ballometer```

## Build

```bash
git clone https://github.com/wipfli/buildroot.git
cd buildroot
make ballometer_raspberrypi3_defconfig
```

Create a file called ```./board/ballometer/wpa_supplicant.conf``` and fill it with your wifi details:
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

