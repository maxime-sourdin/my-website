Title: MSMTP OVH
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Mails
Tags: MTA
Summary: Configuration simple d'un MTA

Installer msmtp
	
	sudo apt install -y msmtp

Dans /etc/msmtprc

	account default
	tls_starttls off
	tls on
	tls_trust_file /etc/ssl/certs/ca-certificates.crt
	logfile        ~/.msmtp.log
	host ssl0.ovh.net
	port 465
	from postmaster@monmail.ovh
	auth on
	user postmaster@monmail.ovh
	password UnMotDePasseTresComplique
