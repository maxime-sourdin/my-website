Title: Configuration SSH, mode hardening
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Tags: SSH
Summary: Configuration simple et solide de SSH

# Serveur

## /etc/ssh/sshd_config

	Port 2417
	ListenAddress 0.0.0.0
	HostKey "/etc/ssh/ssh_host_ed25519_key"
	KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
	Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
	MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
	LogLevel VERBOSE
	AuthenticationMethods publickey
	LoginGraceTime 5m
	PermitRootLogin no
	MaxAuthTries 2
	MaxSessions 6
	PubkeyAuthentication yes
	PermitEmptyPasswords no
	ChallengeResponseAuthentication yes
	UsePAM yes
	X11Forwarding no
	X11UseLocalhost no
	PrintMotd no
	Compression no
	AllowTcpForwarding yes
	GatewayPorts yes
	ClientAliveCountMax 2
	TCPKeepAlive no
	AllowAgentForwarding no
	AcceptEnv LANG LC_*
	Subsystem sftp /usr/lib/ssh/sftp-server -f AUTHPRIV -l INFO
	UseDNS no


# Client 

## Génération de la clé publique et de la clé privée, en utilisant l’algo ed25519, avec une clé de 4096 bits

	ssh-keygen -t ed25519 -b 4096

	Generating public/private ed25519 key pair.
	Enter file in which to save the key (/Users/pc/.ssh/id_ed25519):
	Enter passphrase (empty for no passphrase):
	Enter same passphrase again:
	Your identification has been saved in /Users/pc/.ssh/id_ed25519.
	Your public key has been saved in /Users/pc/.ssh/id_ed25519.pub.
	The key fingerprint is:
	SHA256: trucbidule pc@monpc.local
	The key's randomart image is:
	+--[ED25519 256]—+
	+----[SHA256]-----+

## On a ces deux clés, il faut désormais transférer la clé publique:

	ssh-copy-id -i .ssh/id_ed25519.pub user@monip -p 6666


	/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: ".ssh/id_ed25519.pub"
	/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
	/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
	user@monip's password:

	Number of key(s) added:        1

	Now try logging into the machine, with:   "ssh -p '6666' ‘user@monip'" and check to make sure that only the key(s) you wanted were added.

## On peut désormais se connecter avec une passphrase:

 	ssh -p '6666' ‘user@monip'
	Enter passphrase for key '/Users/pc/.ssh/id_ed25519':

## C'est bon !

	user@servssh:~$ 