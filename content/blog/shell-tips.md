Title: Exploiting Trivy
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Security
Summary: Some Trivy tips
Tags: Trivy


# One liner Trivy
    for image in $(docker image ls | awk '{print $1,$2}' | sed -e "s/ /:/g" | sed '/REPOSITORY:TAG/d'); do docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v caches:/root/.cache/ aquasec/trivy $image >> output ; done

# A light minecraft server

    java -server -XX:+UnlockExperimentalVMOptions -XX:CompileThreshold=752253 -XX:+TieredCompilatnion -XX:+UseStringCache -XX:+OptimizeStringConcat, -XX:+UseBiansedLocking, -Xnoclassgc, -XX:+UseFastAccessorMethods, -XX:+UseConmpressedOops, -XX:+UseG1GC, -XX:NewSize=624m, -XX:MaxNewSize=624nm, -XX:MaxGCPauseMillis=5, -XX:G1HeapRegionSize=128k, -XX:G1HeapnWastePercent=8, -XX:InitiatingHeapOccupancyPercent=69, -XX:Survin

    java -server, -XX:+UnlockExperimentalVMOptions -XX:+UseStringCache -XX:+OptimizeStringConcat -XX:+UseBiasedLocking -Xnoclassgc -XX+UseFastAccessorMethods -XX:+UseCompressedOops -XX:ParallelGCThreads=20 -Xms3000m -Xmx5000m -XX:PermSize=304m

# Crontab backup

## Edit crontab:

	crontab -e

	SHELL=/bin/bash
	@weekly tar cfz /srv/27374c9b-38ee-44f9-ac29-8e528c797b92/backup/mediasmaxime/$(date +"%m-%d-%y").tar.gz /srv/dev-disk-by-label-MediasMaxime/


SHELL variable specifies bash as the shell (otherwise the command does not run).

tar cfz' compresses the folder to .tar.gz, with gunzip.

## Encrypted backups

Even better, encrypted backups (remember to generate gpg keys, with a passphrase please !!!!)

	tar -c -f - /root/scripts/* | gpg --pinentry-mode loopback --passphrase-file /root/.gpgkey  -o /mnt/data/Backup/truenas/scripts-$(date +"%m-%d-%y").tar.gz -c

# Recover corrupted tar.gz archive

## Download gzrecover:

	git clone https://github.com/arenn/gzrt

## Compile !:

	cd gzrt
	make

## Install binary:

	sudo cp gzrecover /usr/local/bin/

# Usage:

	gzrecover lycee.tar.gz
	cpio -F lycee.tar.recovered -i -v	

# SSH Tunnel

## Edit http.service:

    [Unit]
    Description=http
    After=network.target

    [Service]
    ExecStart=/usr/bin/ssh -NT -i /home/fedora/.ssh/autovm -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L $IPDISTANTE:80:$IPVM1DUSERVEUR:80 ubuntu@$IPVM1DUSERVEUR
    User=fedora
    # Restart every >2 seconds to avoid StartLimitInterval failure
    RestartSec=5
    Restart=always

    [Install]
    WantedBy=multi-user.target


## Edit sshd_config

...
    Match User tunnelshell
    PermitTunnel yes
    AllowAgentForwarding no
    AuthenticationMethods publickey
    AllowTcpForwarding yes
    ForceCommand /bin/false
    #   GatewayPorts clientspecified

# Proxies

## APT

### Edit **/etc/apt.conf:**

Add :

	Acquire::http::Proxy "http://172.16.1.8:9999";
    Acquire::https::proxy "https://10.0.0.46:3128/";
    Acquire::ftp::proxy "ftp://10.0.0.46:3128/" ;

or directly modify the sources.list

	deb http://172.16.1.8:9999/deb.debian.org/debian/ buster main contrib non-free
	
	deb http://172.16.1.8:9999/security.debian.org/debian-security buster/updates main contrib non-free
	
	deb http://172.16.1.8:9999/deb.debian.org/debian/ buster-updates main contrib non-free

## Shell

    export http_proxy="http://10.0.0.6:3128/"
    export https_proxy="http://10.0.0.6:3128/"
    export ftp_proxy="http://10.0.0.6:3128/"
    export no_proxy="127.0.0.1,localhost"
