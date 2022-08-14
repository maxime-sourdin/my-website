Title: Resize an encrypted disk under OpenMediaVault (virtualized under Proxmox)
Date: 2020:03:05 18:00
Author: Maxime SOURDIN
Category: Multimedia
Tags: OpenMediaVault
Summary: Expanding Encrypted Virtual Disks

1- Enlarge the virtual disk under Proxmox, by searching in the OpenMediaVault parameters for the right disk. It should be based on the number allocated to the SCSI port, if you have several disks with a similar allocated space.

  
2- You have to unmount the partition to be able to enlarge it

         sudo systemctl restart smbd
         sudo umount /srv/dev-disk-by-label-unshare

3- We lock the disk:

          sudo cryptsetup luksClose /dev/mapper/sde-crypt

4- You can now unlock it with the OMV web interface and remount it (nothing prevents you from doing it on the command line of course).


5- Finally, we must resize the file system on the encrypted disk:

         sudo resize2fs -p /dev/mapper/sdg-crypt