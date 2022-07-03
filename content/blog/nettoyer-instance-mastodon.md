Title: Nettoyage d'une instance Mastodon
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Autohébergement
Tags: Mastodon
Summary: Economiser un peu d'espace sur son instance

1- Nettoyage du cache

	RAILS_ENV=production bin/tootctl cache clear

2- Nettoyage des médias orphelins	

	RAILS_ENV=production  bin/tootctl media remove-orphans

3- Nettoyage des médias vieux de 3 mois (par défaut)

	RAILS_ENV=production  bin/tootctl media remove

4- Nettoyage des comptes inactifs

	RAILS_ENV=production  bin/tootctl accounts cull

