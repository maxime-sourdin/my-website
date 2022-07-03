Title: Redimensionner un disque chiffré sous OpenMediaVault (virtualisé sous Proxmox)
Date: 2020:03:05 18:00
Authors: Maxime SOURDIN
Category: Multimédia
Tags: OpenMediaVault
Summary: Agrandissement de disques virtuels chiffrés

1- agrandir le disque virtuel sous proxmox, en cherchant dans les paramètres d'OpenMediaVault le bon disque. Il faut se baser sur le numéro alloué au port SCSI, si vous avez plusieurs disques avec un espace alloué similaire.

  
2- Il faut démonter la partition pour pouvoir l'agrandir

        sudo systemctl restart smbd
        sudo umount /srv/dev-disk-by-label-unpartage 

3- On verrouille le disque:

         sudo cryptsetup luksClose /dev/mapper/sde-crypt

4- On peut maintenant le déverouiller avec l'interface web d'OMV et le remonter (rien n'emp^êêche de le faire en ligne de commandes évidemment).


5- Enfin, il faut redimensionner le syst  me de fichiers sur le disque chiffr  :

        sudo resize2fs -p /dev/mapper/sdg-crypt
