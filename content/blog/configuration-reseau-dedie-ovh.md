Title: Configuration réseau sur un serveur dédié OVH, avec une IP failover
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Réseau
Summary: Configurer "facilement" son IP failover
Tags: OVH

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
    BROWSER_ONLY=no
    PREFIX=32
    DEFROUTE=yes
    IPV4_FAILURE_FATAL=no
    IPv6INIT=yes
    NAME="System eno2:0"
    UUID=f8744e88-b2f8-de69-4797-e33eead3a435
    BOOTPROTO=none
    ZONE=web
    IPV6INIT=yes
    IPV6_AUTOCONF=no
    IPV6ADDR=$IPV6/56
    IPV6_DEFROUTE=yes
    IPV6_FAILURE_FATAL=no
    IPV6_ADDR_GEN_MODE=stable-privacy
    IPV6_DEFAULTGW=$GW_IPV6
    IPV6_PEERROUTES=no

## Ubuntu

    # This file is generated from information provided by the datasource.  Changes
    # to it will not persist across an instance reboot.  To disable cloud-init's
    # network configuration capabilities, write a file
    # /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
    # network: {config: disabled}
    network:
        version: 2
        ethernets:
            eno1:
                dhcp4: true
                match:
                    macaddress: $MAC_ADDRESS_ENO1
                set-name: eno1
                nameservers:
                    addresses: [127.0.0.1]

            eno2:
                addresses:
                    - $IP_FAILOVER/32
                optional: true
                dhcp4: false
                match:
                    macaddress: $MAC_FAILOVER
                set-name: eno2
                nameservers:
                    addresses: [127.0.0.1]
