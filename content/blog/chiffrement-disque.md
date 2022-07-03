Title: Chiffrement d'un disque avec LUKS
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Tags: Chiffrement
Summary: Chiffrer son disque simplement 

------------------------------------
	sudo apt install -y crypsetup

----------------------------
Partitionnement

	fdisk /dev/sdb
	n       (Créer nouvelle partition)
	p       (Partition primaire)
	1       (Numéro de partition)
	2048    (par défaut Début de la partition)
	+64G    (Taille de la partition 64Go)
	w       (Confirme le partitionnement du disque)

----------------------------
Chiffrement

	sudo cryptsetup luksFormat -c aes -h sha256 /dev/sdb1


	WARNING!
	Cette action écrasera définitivement les données sur /dev/sdb1.

	Are you sure? (Type uppercase yes): YES
	Saisissez la phrase secrète pour /dev/sdb1 : menezdaou
	Vérifiez la phrase secrète : menezdaou

----------------------------
Déchiffrement du disque

	sudo crypsetup luksOpen /dev/sdb1 mondisque

----------------------------
Formatage

	sudo mkfs.ext4 /dev/mapper/mondisque

----------------------------
Montage

	sudo mkdir /mnt/mondisque
	sudo mount /dev/mapper/mondisque /mnt/mondisque


