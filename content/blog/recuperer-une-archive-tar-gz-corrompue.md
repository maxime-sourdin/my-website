Title: Récupérer une archive tar gz corrumpue
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Archivage
Summary: Sauvetage de données archivées avec tar.gz
Tags: Sauvetage

Récupération  de gzrecover:

	git clone https://github.com/arenn/gzrt

Compilation:

	cd gzrt
	make

Installation:

	sudo cp gzrecover /usr/bin/


Utilisation:

	gzrecover lycee.tar.gz
	cpio -F lycee.tar.recovered -i -v	
