Title: Hackintosh Vostro 7590
Date: 2019:21:10 18:00
Author: Maxime SOURDIN
Category: Mac
Tags: Hackintosh
Summary: Using a Vostro 7590 as Hackintosh

Feedback on using MacOS on a Dell Vostro/Inspiron 7590 (hackintosh)

What works:

-HDMI
-Camera
-USB
- USB Type-C / Thunderbolt3
-Bluetooth
- Standby
- Airplay (!!)

What doesn't work:

- Wireless
- Microphone
- SD card reader
- the GTX 1050 3GB

The bootable key was created with this <a href="https://dortania.github.io/OpenCore-Desktop-Guide/installer-guide/winblows-install.html">guide</a>.

As soon as the bootable key is created, you must access the EFI partition, which is called BOOT, go to the EFI folder. You have to download this <a href="https://github.com/Pinming/Dell-Inspiron-7590-Hackintosh-Opencore/archive/master.zip">archive </a> and unzip it in the OC folder, overwriting existing files.

Afterwards, you have to restart on the key, and it is the Catalina recovery mode that will be displayed. It is necessary to allocate an entire disk for Catalina. If you have an ADSL connection, the next step will be quite long, because the installer downloads what is needed for Catalina.

Finally, at the end of the installation, and at the restart, you must choose to boot from the disk. The disk's EFI partition must be mounted.

sudo mkdir /Volumes/efi
sudo mount -t msdos /dev/disk0s1 /Volumes/efi

Afterwards, it is possible to copy the contents of the EFI partition of the USB key there, with the Finder.

For Wifi, things are progressing, thanks to two projects:

- <a href="https://github.com/zxystd/itlwm">itwlm</a>

- <a href="https://github.com/AppleIntelWifi/adapter">AppleIntelWifi</a>

Level <a href="https://browser.geekbench.com/v5/cpu/1919290" >benchmarks </a>, it's not bad, it's approaching a MacBookPro 16P from 2019, with the same processor, sold for 2700 euros (but not limited by the integrated GPU and which obviously does not have the hackintosh malfunctions).

At the stability level, I had some small problems, but it seems inherent to Catalina. The boot, meanwhile, is faster than on a real Mac, and the ventilation is better managed.