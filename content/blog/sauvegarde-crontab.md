Title: Sauvegarde avec tar et la crontab
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Sauvegarde
Tags: OpenMediaVault
Summary: Automatisation d'une sauvegarde sous OpenMediaVault

Edition de la crontab:

	crontab -e

Ajout de deux lignes: 

	SHELL=/bin/bash
	@weekly tar cfz /srv/27374c9b-38ee-44f9-ac29-8e528c797b92/backup/mediasmaxime/$(date +"%m-%d-%y").tar.gz /srv/dev-disk-by-label-MediasMaxime/


SHELL spécifie bash comme shell (sinon la commande ne s'éxécute pas).

'tar cfz' compresse le dossier en .tar.gz, avec gunzip.


Encore mieux, des backups chiffrées (pensez à générer des clés gpg, avec une passphrase svp !!!!)

	tar -c -f - /root/scripts/* | gpg --pinentry-mode loopback --passphrase-file /root/.gpgkey  -o /mnt/data/Backup/truenas/scripts-$(date +"%m-%d-%y").tar.gz -c
