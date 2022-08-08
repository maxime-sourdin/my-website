Title: Hardening rapide
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Summary: Quelques commandes pour renforcer son serveur
Tags: Cheatsheet

## Paquets importants

    sudo apt install -y apt-listbugs apt-listchanges needrestart  debsecan debsums libpam-tmpdir chkrootkit

## CronAPT

    APTCOMMAND=/usr/bin/apt-get
    OPTIONS="-o quiet=1 -o Dir::Etc::SourceList=/etc/apt/security.sources.list"
    MAILTO="mail@mail.com"
    MAILON="always"

## Mots de passe

    apt-get install libpam-cracklib

 sudo nano  /etc/pam.d/common-password

    # here are the per-package modules (the "Primary" block)
    password        requisite                       pam_cracklib.so retry=1 minlen=32 difok=5
    password        [success=1 default=ignore]      pam_unix.so obscure use_authtok try_first_pass sha512
    # here's the fallback if no module succeeds
    password        requisite
                  pam_deny.so
    # prime the stack with a positive return value if there isn't one already;
    # this avoids us returning an error just because nothing sets a success code
    # since the modules above will each just jump around
    password        required                        pam_permit.so
    # and here are more per-package modules (the "Additional" block)
    password        optional        pam_gnome_keyring.so
    # end of pam-auth-update config

## Nmap

    for i in {1..254}; do nmap -sP --max-retries=1 --host-timeout=1500ms 192.168..1-254 | grep -Ev "Starting Nmap 7.70|Nmap done: 254 IP addresses"; done

## Fail2ban
### Jails

    [nginx-conn-limit]
    enabled = true
    filter = nginx-conn-limit
    action = iptables-multiport[name=ConnLimit, port="http,https",
    protocol=tcp]
    logpath = /var/log/nginx/*error.log
    findtime = 300 <br>
    bantime = 7200
    maxretry = 100
    
    [nginx-notilde]
    enabled = true
    filter = nginx-notilde
    action = iptables-multiport[name=ConnLimit, port="http,https",
    protocol=tcp]
    logpath = /var/log/nginx/*error.log
    findtime = 300
    bantime = 7200
    maxretry = 100
    
    [dos-http]
    enabled = true
    port = http,https
    filter = dos-http
    logpath = /var/log/nginx/*access.log
    maxretry = 300
    findtime = 300
    
    [nginx-nohome]
    enabled = false
    port = http,https
    filter = nginx-nohome
    logpath = /var/log/nginx/*access.log
    maxretry = 2
    
    [nginx-noproxy]
    enabled = false
    port = http,https
    filter = nginx-noproxy
    logpath = /var/log/nginx/*access.log
    maxretry = 25
    
    [nginx-noscript]
    enabled = true
    port = http,https
    filter = nginx-noscript
    logpath = /var/log/nginx/*access.log
    maxretry = 6
    
    [nginx-badbots]
    enabled = true
    port = http,https
    filter = nginx-badbots
    logpath = /var/log/nginx/*access.log
    maxretry = 2
    
    [nginx-botsearch]
    enabled = true
    port = http,https
    filter = nginx-botsearch
    logpath = /var/log/nginx/*access.log
    maxretry = 2

### Filters 

Par exemple, dans /etc/fail2ban/filter.d/ nginx-nohome.conf

    [Definition]
    failregex = ^<HOST> -.*GET .*/~.*
    ignoreregex =


Ou dans / etc/fail2ban/filter.d/ nginx-noproxy.conf

    [Definition]
    failregex = ^<HOST> -.*GET http.*
    ignoreregex=
    
Dans /etc/fail2ban/filter.d/nginx-noscript.conf

    [Definition]
    failregex = ^<HOST> -.*GET.*(\.php|\.asp|\.exe|\.pl|\.cgi|\.scgi)
    ignoreregex =

Dans / etc/fail2ban/filter.d/nginx-notilde.conf

    [Definition]
        failregex = ^ \[error\] \d+#\d+: \*\d+ .* client: <HOST>, server:\S+, request: "GET /.*~ HTTP
        ignoreregex =

## IPTABLES

    sudo iptables -P INPUT DROP # on bloque en entrée
    sudo iptables -P FORWARD DROP
    sudo iptables -P OUTPUT ACCEPT
    sudo iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 22 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 8118 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 80 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 443 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 139 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 631 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 53 -j ACCEPT
    sudo iptables -A INPUT -p udp -i enp0s7 --dport 53 -j ACCEPT
    sudo iptables -A INPUT -p udp -i enp0s7 --dport 1194 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 2377 -j ACCEPT
    sudo iptables -A INPUT -p tcp -i enp0s7 --dport 7946 -j ACCEPT
    sudo iptables -A INPUT -p udp -i enp0s7 --dport 4789 -j ACCEPT

## Antivirus :

Installer clamav, mettre à jour sa base de données, et lancer un scan toutes les nuits sur l’espace à protéger, puis générer un rapport :

    sudo freshclam
    sudo crontab -e :

    # m h dom mon dow command
    39 0 * * * clamscan -r /storage | grep FOUND >>
    /home/user/reports/report.txt

## Sysctl

    net.ipv6.conf.default.accept_redirects = 0
    net.ipv6.conf.all.accept_redirects = 0
    net.ipv4.conf.default.log_martians = 1
    net.ipv4.conf.default.accept_source_route = 0
    net.ipv4.conf.default.accept_redirects = 0
    net.ipv4.conf.all.send_redirects = 0
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.conf.all.log_martians = 1
    net.ipv4.conf.all.forwarding = 0
    kernel.sysrq = 0
    kernel.kptr_restrict = 2
    kernel.dmesg_restrict = 1
    fs.suid_dumpable = 0
    kernel.core_uses_pid = 1
    net.ipv4.conf.all.accept_redirects = 0

## Scan de ports

     nc -vnz -w 1 172.16.28.21 1-65535

## chkrootkit

    0 3 * * * /usr/sbin/chkrootkit 2>&1 | mail -s "chkrootkit Reports of My Server" mail@mail.com


