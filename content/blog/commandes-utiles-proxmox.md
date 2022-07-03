Title: Commandes utiles Proxmox
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hyperviseur
Tags: Proxmox
Summary: Quelques commandes utiles sur Proxmox

__Stopper une sauvegarde:__

	vzdump -stop

__Lister conteneurs:__

	pct list

__Lister vm:__

	qm list

__Bridger des interfaces:__

dans /etc/network/interfaces:
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

__Mapper un dossier local de l'hyperviseur sur un container (nécessite un arrêt du conteneur):__

	pct set 500 -mp0 /home/user,mp=/etc/letsencrypt

