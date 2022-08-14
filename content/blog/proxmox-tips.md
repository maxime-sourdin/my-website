Title: Useful Proxmox commands
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hypervisor
Tags: Proxmox
Summary: Some commands for pct/qm/vzdump

__Stop backup:__

	vzdump -stop

__List containers:__

	pct list

__List vm:__

	qm list

__Bridge interfaces:__

In /etc/network/interfaces:
<code>

	auto lo
	iface lo inet loopback

	auto vmbr0
	iface vmbr0 inet static
        address 172.16.0.3
        netmask 255.255.255.248
        gateway 172.16.0.1
        bridge_ports eno0
        bridge_stp off
        bridge_fd 0

	auto vmbr1
	iface vmbr1 inet static
        address 172.16.1.1
        netmask 255.255.255.0
        bridge_ports eno1
        bridge_stp off
        bridge_fd 0
</code>

__Map local folder on a container:__

	pct set 500 -mp0 /home/user,mp=/etc/letsencrypt

# Disk image file

## Creating a disk image file


	sudo mkdir /storage/images/999/ && sudo dd if=/dev/zero of=/storage/images/999/le.raw bs=4k count=12500


## Formatting in ext4


    sudo mkfs.ext4 /storage/images/999/le.raw


## Disable virtual disk mount checks and control


    sudo tune2fs -c0 -i0 /storage/images/999/le.raw


## Create a mount folder and mount


    sudo mkdir /media/test && sudo mount -o loop /storage/images/999/le.raw /media/test/


## Final container configuration on Proxmox:

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