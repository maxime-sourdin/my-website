Title: Configuration réseau de relai wifi sur OpenWRT
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Réseau
Tags: Openwrt
Summary: Relai Wifi

# /etc/config/wireless

    config wifi-device 'radio0'
            option type 'mac80211'
            option hwmode '11g'
            option path 'platform/10300000.wmac'
            option htmode 'HT20'
            option disabled '0'
            option country '00'
    
         option legacy_rates '1'
            option channel '6'
    
    config wifi-iface
            option network 'wifirep'
            option ssid 'Livebox-442c'
    
    option encryption 'psk2'
            option device 'radio0'
            option mode 'sta'
            option bssid '$BSSID'
            option key ' '

# /etc/config/network

    config interface 'loopback'
            option ifname 'lo'
            option proto 'static'
            option ipaddr '127.0.0.1'
            option netmask '255.0.0.0'
    
    config globals 'globals'
            option ula_prefix 'fdee:45b4:8e97::/48'
    
    config interface 'lan'
            option type 'bridge'
            option ifname 'eth0.1'
            option proto 'static'
            option netmask '255.255.255.0'
            option ip6assign '60'
            option ipaddr '192.168.1.1'
            list dns '172.16.1.2'
            list dns '80.67.169.12'
    
    config device 'lan_dev'
            option name 'eth0.1'
            option macaddr 'c4:71:54:39:63:d2'
    
    config interface 'wan'
            option ifname 'eth0.2'
            option proto 'dhcp'
    
    config device 'wan_dev'
            option name 'eth0.2'
            option macaddr '$MAC_ADDR'
    
    config interface 'wan6'
            option ifname 'eth0.2'
            option proto 'dhcpv6'
    
    config switch
            option name 'switch0'
            option reset '1'
            option enable_vlan '1'
    
    config switch_vlan
            option device 'switch0'
    
     option vlan '1'
            option ports '1 2 3 4 6t'
    
    config switch_vlan
            option device 'switch0'
            option vlan '2'
            option ports '0
    6t'
    
    config interface 'bridge_wifi'
            option proto 'relay'
            list network 'lan'
            list network 'wifirep'
    
    config interface 'wifirep'
            option proto 'static'
            option ipaddr '172.16.14.3'
            option netmask '255.255.255.0'
            option gateway '172.16.14.254'
    
     option broadcast '172.16.14.255'
            list dns '172.16.1.2'
    
    config route
            option interface 'lan'
            option target '0.0.0.0'
            option netmask '0.0.0.0'
            option gateway '172.16.14.254'
    
    config route
            option interface 'lan'
            option target '172.16.1.0'
            option netmask '255.255.255.0'
            option gateway '172.16.14.254'
    
    config route
            option interface 'lan'
            option target '172.16.0.0'
            option netmask '255.255.255.248'
            option gateway '172.16.14.254'
    
    config route
            option interface 'lan'
            option target '172.16.15.0'
            option gateway '172.16.14.254'
            option netmask '255.255.255.0'
    
    config route
            option interface 'bridge_wifi'
            option target '0.0.0.0'
            option netmask '0.0.0.0'
            option gateway '172.16.14.254'
    
    config route
            option interface 'bridge_wifi'
    
     option target '172.16.1.0'
            option netmask '255.255.255.0'
            option gateway '172.16.1.254'
