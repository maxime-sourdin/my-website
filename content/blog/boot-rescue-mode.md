Title: Boot via le rescue mode (OVH)
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Sauvegarde
Tags: OVH
Summary: Installer un systéme sur un serveur limité


# La commande 

    qemu-system-x86_64 -bios /usr/share/ovmf/OVMF.fd -netdev type=user,id=mynet0 -device virtio-net-pci,netdev=mynet0 -m 8096 -localtime -enable-kvm -drive index=1,media=disk,if=virtio,file=/dev/nvme1n1 -drive index=2,media=disk,if=virtio,file=/dev/nvme0n1 -vga qxl -vnc 127.0.0.1:5900 -daemonize -drive index=0,format=raw,file=proxmox.iso -boot d


# Explications des arguments

    qemu-system-x86_64 -bios /usr/share/ovmf/OVMF.fd -daemonize -localtime : Boot sur un système en 64 bits avec un UEFI, en arrière-plan et averc l'heure de la pile du BIOS

    -netdev type=user,id=mynet0 -device virtio-net-pci,netdev=mynet0: Configuration réseau par défaut (carte réseau standard)

    -m 8096: 8Go de RAM attribué à la VM

    -enable-kvm -vga qxl -vnc 127.0.0.1:5900: Activation du KVM et accés à la console via VNC
    
    -drive index=1,media=disk,if=virtio,file=/dev/nvme1n1 -drive index=2,media=disk,if=virtio,file=/dev/nvme0n1 : Montage des deux disques du serveurs
    
    -drive index=0,format=raw,file=proxmox.iso: Montage du fichier ISO
     
    -boot d: Démarrage de la machine virtuelle directement aprés sa création 
