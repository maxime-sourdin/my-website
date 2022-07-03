Title: Proxy APT
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Réseau
Tags: Proxies
Summary: Utiliser un proxy

# Pour APT

Dans **/etc/apt.conf:**

Rajouter:

	Acquire::http::Proxy "http://172.16.1.8:9999";
    Acquire::https::proxy "https://10.0.0.46:3128/";
    Acquire::ftp::proxy "ftp://10.0.0.46:3128/";

ou modifier directement les sources.list

	deb http://172.16.1.8:9999/deb.debian.org/debian/ buster main contrib non-free
	
	deb http://172.16.1.8:9999/security.debian.org/debian-security buster/updates main contrib non-free
	
	deb http://172.16.1.8:9999/deb.debian.org/debian/ buster-updates main contrib non-free

# Pour le shell

    export http_proxy="http://10.0.0.6:3128/"
    export https_proxy="http://10.0.0.6:3128/"
    export ftp_proxy="http://10.0.0.6:3128/"
    export no_proxy="127.0.0.1,localhost"
