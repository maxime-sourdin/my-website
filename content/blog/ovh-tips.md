Title: OVH Tips
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Backup
Tags: OVH
Summary: Some tips on OVH


# Boot rescue mode

## The command to type

    qemu-system-x86_64 -bios /usr/share/ovmf/OVMF.fd -netdev type=user,id=mynet0 -device virtio-net-pci,netdev=mynet0 -m 8096 -localtime -enable-kvm -drive index=1,media=disk,if=virtio,file=/dev/nvme1n1 -drive index=2,media=disk,if=virtio,file=/dev/nvme0n1 -vga qxl -vnc 127.0.0.1:5900 -daemonize -drive index=0,format=raw,file=proxmox.iso -boot d


## Arguments

    qemu-system-x86_64 -bios /usr/share/ovmf/OVMF.fd -daemonize -localtime : Boot on a 64-bit system with a UEFI, in the background and with the BIOS time

    -netdev type=user,id=mynet0 -device virtio-net-pci,netdev=mynet0: Default network configuration (standard network card)

    -m 8096: 8GB RAM allocated to the VM

    -enable-kvm -vga qxl -vnc 127.0.0.1:5900: KVM activation and console access via VNC
    
    -drive index=1,media=disk,if=virtio,file=/dev/nvme1n1 -drive index=2,media=disk,if=virtio,file=/dev/nvme0n1 : Mounting the two server disks
    
    -drive index=0,format=raw,file=proxmox.iso: ISO mounting
     
    -boot d: Start the virtual machine directly after its creation 

# MTA

## Install msmtp
	
	sudo apt install -y msmtp

## Edit /etc/msmtprc

	account default
	tls_starttls off
	tls on
	tls_trust_file /etc/ssl/certs/ca-certificates.crt
	logfile        ~/.msmtp.log
	host ssl0.ovh.net
	port 465
	from postmaster@monmail.ovh
	auth on
	user postmaster@monmail.ovh
	password UnMotDePasseTresComplique

# IP Failover

## RedHat/CentOS
ifcfg-eno1

    BOOTPROTO=dhcp
    DEVICE=eno1
    HWADDR= $MAC_ADDRESS_ENO1
    ONBOOT=yes
    STARTMODE=auto
    TYPE=Ethernet
    USERCTL=no

ifcfg-eno2

    IPADDR=$IP_FAILOVER
    NETMASK=255.255.255.255
    BROADCAST=$IP_FAILOVER
    ONBOOT=yes
    TYPE=Ethernet
    PROXY_METHOD=none
    BROWSER_ONLY=none
    PREFIX=32
    DEFROST=yes
    IPV4_FAILURE_FATAL=no
    IPv6INIT=yes
    NAME="System eno2:0
    UUID=f8744e88-b2f8-de69-4797-e33eead3a435
    BOOTPROTO=none
    ZONE=web
    IPV6INIT=yes
    IPV6_AUTOCONF=no
    IPV6ADDR=$IPV6/56
    IPV6_DEFROUD=yes
    IPV6_FAILURE_FATAL=no
    IPV6_ADDR_GEN_MODE=stable-privacy
    IPV6_DEFAULTGW=$GW_IPV6
    IPV6_PEERROUTES=no

## Ubuntu

    # This file is generated from the information provided by the data source.  Changes made to this file will not affect it.
    # Changes made to this file will not persist when the instance is restarted.  To disable the network
    # network configuration capabilities, write a file
    # /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
    # network: {config: disabled}
    network:
        version: 2
        ethernets:
            eno1:
                dhcp4 : true
                match:
                    macaddress : $MAC_ADDRESS_ENO1
                set-name : eno1
                nameservers:
                    addresses: [127.0.0.1]

            eno2:
                addresses:
                    - $IP_FAILOVER/32
                optional : true
                dhcp4 : false
                match:
                    macaddress : $MAC_FAILOVER
                set-name : eno2
                nameservers :
                    addresses: [127.0.0.1]