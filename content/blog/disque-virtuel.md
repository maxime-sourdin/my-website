Title: Disque virtuel
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hyperviseur
Tags: Proxmox
Summary: Création  et utilisation d'images disques

Création d'un fichier image disque


	sudo mkdir /storage/images/999/ && sudo dd if=/dev/zero of=/storage/images/999/le.raw bs=4k count=12500


Formatage en ext4


    sudo mkfs.ext4 /storage/images/999/le.raw


Désactivation des vérifications et du contrôle au montage du disque virtuel


    sudo tune2fs -c0 -i0 /storage/images/999/le.raw


Création d'un dossier de montage et montage


    sudo mkdir /media/test && sudo mount -o loop /storage/images/999/le.raw /media/test/


Sur Proxmox:

    arch: amd64
    hostname: servpro
    memory: 4096
        mp1: storage:999/le.raw,mp=/etc/letsencrypt,acl=0,ro=1,size=50M,backup=1
    nameserver: 10.0.0.1
    net0: name=eth1,bridge=vmbr1,gw=10.0.0.10,hwaddr=1F:CD:EE:D9:14:2A,ip=10.0.0.42/24,ip6=auto,tag=42,type=veth
    onboot: 1
    ostype: debian
    rootfs: storage:106/vm-106-disk-0.raw,size=20G
    swap: 0
    unprivileged: 1