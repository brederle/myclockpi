### Raspian (MacOS):
> dd if=<raspian>.imd of=/dev/rdsik<diskid> bs=1m conv=sync

### Setup:
> sudo raspi-config

Locale: de_DE.UTF-8
Timezone
Keyboard locale (do before passwd change!)
Change passwd
- Enable I2C (for sensors)
- Enable SPI (for LCD)
- Enable ssh

### Replace pi user:
https://www.raspberrypi.org/documentation/configuration/security.md

> sudo useradd -m myuser -G sudo -G video -G input -s /bin/bash
> sudo passwd myuser
# login as myuser,check
> sudo visudo
> sudo deluser -remove-home pi

UPDATE firmware:
> sudo rpi-update

### WLAN connection:
https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

Generate config entry:
> wpa_passphrase "testing" "testingPassword" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf

Remove clear test password and unused/obsolete entries:
> sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
> wpa_cli -i wlan0 reconfigure

### Install kivy:
https://kivy.org/docs/installation/installation-rpi.html#change-the-default-screen-to-use

Python3:
> sudo apt-get update
> sudo apt-get python3 python3-pip

> sudo apt-get update && apt-get upgrade

*** From package (non-working)
> sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python3-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-tools python3-dev libmt-dev\
   xclip xsel git
> sudo apt-get remove python2.7
#> sudo apt autoremove
> sudo pip3 install -U Cython>=0.28.2
> sudo pip3 install --upgrade --force-reinstall git+https://github.com/kivy/kivy.git@master
###> sudo apt-get install python-kivy python3-kivy


(6) Configure USB soundcard
https://blog.fh-kaernten.at/ingmarsretro/tag/raspberry-pi-usb-soundkarte/
> sudo install pulseaudio
> sudo nano /etc/modprobe.d/alsa-base.conf

options snd_usb_audio index=0
options snd_bcm2835 index=1
options snd slots=snd-usb-audio,snd-bcm2835

Add user to use audio diectly:
> sudo adduser myuser audio 

(6) Configure SDL2/direct framebuffer:
export SDL_FBDEV=/dev/fb1


(7) Add touch support:

In ~/.kivy/config.ini and go to the [input] section:

[graphics]
width=480
height=320

[input]
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput


git clone export https://github.com/AndrewFromMelbourne/raspi2fb

export SDL_MOUSEDRV=TSLIB
export SDL_MOUSEDEV=/dev/input/touchscreen


(8) I2C for Gyro - detection of 
> sudo raspi-config
Enable I2C

> sudo vi /etc/modules
i2c-bcm2708
i2c-dev

> sudo apt-get install i2c-tools
> sudo i2cdetect -y 1

> sudo pip3 install smbus2
> sudo adduser myuser i2c

(9) GPIO usage:

GPIO
for Python:
> sudo pip3 install rpi.gpio
> sudo adduser myuser gpio

NOTE: /dev/gpiomem is needed to make this working. This may requires rpi-update to create the device.  

(10) Streaming player
> sudo apt-get install libavcodec  libavdevice libavfilter libavformat libavutil libswscale libswresample libpostproc
> sudo pip3 install ffpyplayer

FAQ:

Problem with root account
Cannot open access to console, root account is locked

Reason:
It comes from fsck detecting a problem after a forced reboot.
It prompts for a repair during boot but gets no access to console.

Solution:
Add to cmdline.txt
fsck.repair=yes


Problem with vim and copy by mouse
Solution:
> sudo vi /etc/vim/vimrc

Add
set mouse=c

Problem: rotate display with new GL driver

Solution:
/boot/config.txt

display_hdmi_rotate=3
0 - no rotation
1 - rotate 90 degrees clockwise
2 - rotate 180 degrees clockwise
3 - rotate 270 degrees clockwise
0x10000 horizontal flip
0x20000 vertical flip









# myclockpi

# Register as service
> sudo cp service/myclockpi.service /etc/systemd/system/
> sudo systemctl enable myclockpi

