# buildroot

Builds the operating system and environment for the ballometer device.

## Overview

This fork of the buildroot project adds the following custom files:

 * A custom defconfig file in ```configs/ballometer_raspberrypi3_defconfig```
 * Custom ```post-build.sh``` and ```post-image.sh``` scripts in ```board/ballometer```

## Installation

```bash
git clone https://github.com/wipfli/buildroot.git
cd buildroot
make ballometer_raspberrypi3_defconfig
make
```

This creates a bootable image in ```output/images/sdcard.img```.

