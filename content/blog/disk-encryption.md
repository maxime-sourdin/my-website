Title: LUKS - Disk encryption
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Tags: Encryption
Summary: Simply encrypt your disk
save_as: disk-encryption.html

# Encrypt a disk

## Dependencies
	sudo apt install -y crypsetup

## Partitioning

	fdisk /dev/sdb
	n (Create new partition)
	p (Primary partition)
	1 (Partition number)
	2048 (default Start of partition)
	+64G (Partition size 64GB)
	w (Confirm disk partitioning)

## Disk encryption

	sudo cryptsetup luksFormat -c aes -h sha256 /dev/sdb1


	WARNING!
	This action will permanently overwrite the data on /dev/sdb1.

	Are you sure? (Type uppercase yes): YES
	Enter the secret phrase for /dev/sdb1: menezdaou
	Verify the secret phrase: menezdaou

## Using encrypted disk

	sudo crypsetup luksOpen /dev/sdb1 mydisk

## Format disk

	sudo mkfs.ext4 /dev/mapper/mondisc

## Mount disk

	sudo mkdir /mnt/mount
	sudo mount /dev/mapper/mondisque /mnt/mondisque

# Expand a virtual disk encrypted by LUKS

## Enlarge disk under GUI

For example, enlarge the virtual disk under Proxmox. 
It should be based on the number allocated to the SCSI port, if you have several disks with a similar allocated space.

## Enlarge partition

### Unmount the partition 

         sudo umount /srv/dev-disk-by-label-unshare

### Lock the disk:

          sudo cryptsetup luksClose /dev/mapper/sde-crypt

### Unlock and remount

For example, you can now unlock it with the OpenMediaVault web interface and remount it (nothing prevents you from doing it on the command line of course).

### Resize the file system on the encrypted disk:

         sudo resize2fs -p /dev/mapper/sdg-crypt