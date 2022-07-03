Title: Hackintosh Vostro 7590
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Mac
Tags: Hackintosh
Summary: Utilisation d'un Vostro 7590 comme Hackintosh

Retour sur l’utilisation de MacOS sur un Dell Vostro/Inspiron 7590 (hackintosh)

Ce qui fonctionne:

- HDMI
- Camera
- USB
- Usb Type C /Thunderbolt3
- Bluetooth
- Veille
- Airplay (!!)

Ce qui ne fonctionne pas:

- Wifi
- Microphone
- Lecteur de carte SD
- la GTX 1050 3Go

La clé bootable a été crée avec ce <a href="https://dortania.github.io/OpenCore-Desktop-Guide/installer-guide/winblows-install.html">guide </a>.

Dés que la clé bootable est crée, il faut accéder à la partition EFI, qui s’appelle BOOT, aller dans le dossier EFI. Il faut télécharger cette <a href="https://github.com/Pinming/Dell-Inspiron-7590-Hackintosh-Opencore/archive/master.zip">archive </a> et la décompresser dans le dossier OC, en écrasant les fichiers existants.

Après, il faut redémarrer sur la clé, et c’est le mode de récupération de Catalina qui s’affichera. Il est nécessaire d’allouer un disque entier pour Catalina. Si vous avez une connexion ADSL, l’étape suivante sera assez longue, car l’installateur télécharge ce qu’il faut pour Catalina.

Enfin, à la fin de l’installation, et au redémarrage, il faut choisir de booter sur le disque. La partition EFI du disque doit être montée.

	sudo mkdir /Volumes/efi
	sudo mount -t msdos /dev/disk0s1 /Volumes/efi

Après, il est possible d' y copier le contenu de la partition EFI de la clé USB, avec le Finder.

Pour le Wifi, ça avance, grâce à deux projets:

- <a href="https://github.com/zxystd/itlwm"> itwlm </a>

- <a href="https://github.com/AppleIntelWifi/adapter">AppleIntelWifi </a>

Niveau <a href="https://browser.geekbench.com/v5/cpu/1919290" >benchmarks </a>, c’est pas mal, ça s’approche d’un MacBookPro 16P de 2019, avec le même processeur, vendue 2700 euros (mais pas limité par le GPU intégré et qui n’a pas les dysfonctionnements du hackintosh évidemment).

Au niveau stabilité, j'ai eu quelques petits problèmes, mais ça semble inhérent à Catalina. Le boot, quant à lui est plus rapide que sur un vrai Mac, et la ventilation est mieux géré.

