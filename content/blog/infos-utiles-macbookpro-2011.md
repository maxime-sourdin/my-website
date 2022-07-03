Title: Infos utiles à propos du MacBookPro 2011
Date: 2020:12:11 18:00
Authors: Maxime SOURDIN
Category: Mac
Tags: MacOS, Windows
Summary: Utilisation d'un MBP 2011 sous Catalina et Windows

Il est possible de passer ce mac facilement sous Catalina, grâce au patch de [dosdude](http://dosdude1.com/catalina/) , sous réserve d'avoir un ordi ou une machine virtuelle MacOS et d'avoir une clé usb de 16Go.

Pensez cependant à désactiver le SIP pour que l'installation puisse redémarrer sans problème par la suite et avoir les patches d'installés directement.

Catalina est assez gourmand donc il faut au moins 8Go de RAM, pour le reste les patches résolvent le problème de wifi, bluetooth et accélération graphique.

Depuis plus d'une semaine, cette installation fonctionne correctement, et mis à part le temps de boot (environ 45 secondes), il est plus que largement utilisable sous Catalina.

Windows 10  fonctionne dessus en dual-boot, avec quelques problèmes assez embêtants. Pensez à graver un DVD d'installation de Windows pour pouvoir commencer l'installation, le débit est peut-être largement pourri mais impossible de faire l'installation avec une clé bootable.

Voici la marche à suivre, piquée sur le [forum macg](https://forums.macg.co/threads/impossible-dintaller-windows-10-sur-la-partition-bootcamp.1286410/page-2), pour pouvoir booter correctement sur le DVD.

- Désactiver le SIP en mode recovery
- Rebooter sur macOS et ouvrir un terminal pour installer gdisk: `brew cask install gdisk`
- Exécuter cette commande pour analyser votre disque: `sudo gdisk /dev/disk0`. Récupérer le numéro de votre disque avec `diskutils list`.
- Ensuite tapez `x` `n` `w` `y` puis rebootez sur macOS.
Tout ça modifie une petite partie de la table de partitions qui permet à Windows de s'initialiser et de s'installer sans problème.
- Enfin vous pouvez rebooter sur le DVD d'installation, en appuyant sur `ALT` au boot, et choisir "Windows"

