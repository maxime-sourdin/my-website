Title: LUKS - Disk encryption
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Tags: Encryption
Summary: Simply encrypt your disk


------------------------------------
	sudo apt install -y crypsetup

----------------------------
Partitioning

	fdisk /dev/sdb
	n (Create new partition)
	p (Primary partition)
	1 (Partition number)
	2048 (default Start of partition)
	+64G (Partition size 64GB)
	w (Confirm disk partitioning)

----------------------------
Encryption

	sudo cryptsetup luksFormat -c aes -h sha256 /dev/sdb1


	WARNING!
	This action will permanently overwrite the data on /dev/sdb1.

	Are you sure? (Type uppercase yes): YES
	Enter the secret phrase for /dev/sdb1: menezdaou
	Verify the secret phrase: menezdaou

----------------------------
Decrypt the disk

	sudo crypsetup luksOpen /dev/sdb1 mydisk

----------------------------
Format

	sudo mkfs.ext4 /dev/mapper/mondisc

----------------------------
Mount

	sudo mkdir /mnt/mount
	sudo mount /dev/mapper/mondisque /mnt/mondisque


Translated with www.DeepL.com/Translator (free version)