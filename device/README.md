# Device

This folder contains code and instructions for setting up a ballometer device on a raspberry pi. 

## Raspbian

Download the <a href="http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2020-02-14/2020-02-13-raspbian-buster-lite.zip">raspbian buster light 2020-02-14 image</a>.

Write the image to an SD card with <a href="https://sourceforge.net/projects/win32diskimager/">win32diskimager</a>.

If there was already a raspbian installation on the SD card use DISKPART on windows to delete the partitions and create a new primary one.

Then mount the SD card in your computer and in the boot folder write a file called ```ssh```. This will enable SSH access by default. 

Allow the raspberry pi to connect to wifi by writing into ```wpa_supplicant.conf``` in the boot folder the following content:

```conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
        ssid="your-hotspot-name"
        psk="your-hotspot-password"
}
```

Put the SD card in the pi, turn it on, and ssh into it with ```ssh pi@raspberrypi.local``` password is ```raspberry```.

To enable root ssh login which we will use with ansible, edit on the pi

```bash
$ sudo nano /etc/ssh/sshd_config
```

and change the line 

```
#PermitRootLogin prohibit-password
```  

to 

```
PermitRootLogin yes
```

Set the root password to ```ballometer``` with

```bash
$ sudo passwd root
```

and then reboot with

```bash
$ sudo reboot
```

SSH into the pi again now with ```ssh root@raspberrypi.local``` and delete the default ```pi``` user with

```
# userdel -r pi
```

Then change the hostname from ```raspberrypi``` to ```ballometer``` in

```
# nano /etc/hosts
```

and in

```
# nano /etc/hostname
```

Then reboot with

```
# reboot
```

Copy the ssh keys of your computer to the pi with:

```bash
ssh-copy-id root@ballometer.local
```

