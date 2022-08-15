Title: Quick Hardening
Date: 2019:21:10 18:00
Author: Maxime SOURDIN
Category: Hardening
Summary: A few commands to strengthen your server
Tags: Tips

## Important Packages

    sudo apt install -y apt-listbugs apt-listchanges needrestart debsecan debsums libpam-tmpdir chkrootkit

## CronAPT

    APTCOMMAND=/usr/bin/apt-get
    OPTIONS="-o quiet=1 -o Dir::Etc::SourceList=/etc/apt/security.sources.list"
    MAILTO="mail@mail.com"
    LINK="always"

## Passwords

    apt-get install libpam-cracklib

 sudo nano /etc/pam.d/common-password

    # here are the per-package modules (the "Primary" block)
    password requirement pam_cracklib.so retry=1 minlen=32 difok=5
    password [success=1 default=ignore] pam_unix.so obscure use_authtok try_first_pass sha512
    # here's the fallback if no module succeeds
    password requirement
                  pam_deny.so
    # prime the stack with a positive return value if there isn't one already;
    # this avoids us returning an error just because nothing sets a success code
    # since the modules above will each just jump around
    password required pam_permit.so
    # and here are more per-package modules (the "Additional" block)
    password optional pam_gnome_keyring.so
    # end of pam-auth-update config

## Nmap

    for i in {1..254}; do nmap -sp --max-retries=1 --host-timeout=1500ms 192.168..1-254 | grep -Ev "Starting Nmap 7.70|Nmap done: 254 IP addresses"; done

## Nginx

### Rickroll bots

#### Edit /etc/nginx/snippets/rickroll.conf

    error_page 404 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 500 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 501 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 502 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 503 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 504 =301 https://youtu.be/dQw4w9WgXcQ?t=44;

#### Edit /etc/nginx/snippets/monsite.conf

    include ../snippets/rickroll.conf;

#### Restart Nginx

	sudo systemctl restart nginx


## Fail2ban
### Jails

    [nginx-conn-limit]
    enabled = true
    filter=nginx-conn-limit
    action = iptables-multiport[name=ConnLimit, port="http,https",
    protocol=tcp]
    logpath = /var/log/nginx/*error.log
    findtime=300 <br>
    bantime = 7200
    maxretry = 100
    
    [nginx-notilde]
    enabled = true
    filter=nginx-notilde
    action = iptables-multiport[name=ConnLimit, port="http,https",
    protocol=tcp]
    logpath = /var/log/nginx/*error.log
    findtime = 300
    bantime = 7200
    maxretry = 100
    
    [back-http]
    enabled = true
    port=http,https
    filter=dos-http
    logpath = /var/log/nginx/*access.log
    maxretry = 300
    findtime = 300
    
    [nginx-nohome]
    enabled = false
    port=http,https
    filter=nginx-nohome
    logpath = /var/log/nginx/*access.log
    maxretry = 2
    
    [nginx-noproxy]
    enabled = false
    port=http,https
    filter=nginx-noproxy
    logpath = /var/log/nginx/*access.log
    maxretry = 25
    
    [nginx-noscript]
    enabled = true
    port=http,https
    filter=nginx-noscript
    logpath = /var/log/nginx/*access.log
    maxretry = 6
    
    [nginx-badbots]
    enabled = true
    port=http,https
    filter=nginx-badbots
    logpath = /var/log/nginx/*access.log
    maxretry = 2
    
    [nginx-botsearch]
    enabled = true
    port=http,https
    filter=nginx-botsearch
    logpath = /var/log/nginx/*access.log
    maxretry = 2

### Filters

For example, in /etc/fail2ban/filter.d/nginx-nohome.conf

    [Definition]
    failregex = ^<HOST> -.*GET .*/~.*
    ignoreregex=


Or in /etc/fail2ban/filter.d/nginx-noproxy.conf

    [Definition]
    failregex = ^<HOST> -.*GET http.*
    ignoreregex=
    
In /etc/fail2ban/filter.d/nginx-noscript.conf

    [Definition]
    failregex = ^<HOST>-.*GET.*(\.php|\.asp|\.exe|\.pl|\.cgi|\.scgi)
    ignoreregex =

In /etc/fail2ban/filter.d/nginx-notilde.conf

    [Definition]
        failregex = ^ \[error\] \d+#\d+: \*\d+ .* client: <HOST>, server:\S+, request: "GET /.*~ HTTP
        ignoreregex =

##IPTABLES

    sudo iptables -P INPUT DROP # block input
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

## Anti-virus :

Install clamav, update its database, and run a scan every night on the space to be protected, then generate a report:

    sudo fresh clam
    sudo crontab -e :

    # m h dom my dow command
    39 0 * * * clamscan -r /storage | grep FOUND >>
    /home/user/reports/report.txt

## Sysctl

    net.ipv6.conf.default.accept_redirects=0
    net.ipv6.conf.all.accept_redirects=0
    net.ipv4.conf.default.log_martians=1
    net.ipv4.conf.default.accept_source_route = 0
    net.ipv4.conf.default.accept_redirects=0
    net.ipv4.conf.all.send_redirects=0
    net.ipv4.conf.all.rp_filter=1
    net.ipv4.conf.all.log_martians=1
    net.ipv4.conf.all.forwarding=0
    kernel.sysrq = 0
    kernel.kptr_restrict = 2
    kernel.dmesg_restrict = 1
    fs.suid_dumpable = 0
    kernel.core_uses_pid = 1
    net.ipv4.conf.all.accept_redirects=0

## Port Scan

     nc -vnz -w 1 172.16.28.21 1-65535

## chkrootkit

    0 3 * * * /usr/sbin/chkrootkit 2>&1 | mail -s "chkrootkit Reports of My Server" mail@mail.com

## SSH

### Server

#### /etc/ssh/sshd_config

    Port 2417
    Listening address 0.0.0.0
    Host key "/etc/ssh/ssh_host_ed25519_key".
    KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
    Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
    Macs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
    VERBOSE log level
    Authentication methods Publickey
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
    sftp subsystem /usr/lib/ssh/sftp-server -f AUTHPRIV -l INFO
    UseDNS no

### Client

#### Generation of the public and private key, using the algo ed25519, with a 4096 bit key

ssh-keygen -t ed25519 -b 4096

Generation of the public/private key pair ed25519.
Enter the file where you want to save the key (/Users/pc/.ssh/id_ed25519):
Enter the passphrase (empty for no passphrase):
Enter the same passphrase again:
Your identification has been saved in /Users/pc/.ssh/id_ed25519.
Your public key has been saved in /Users/pc/.ssh/id_ed25519.pub.
The key fingerprint is:
SHA256: thingbidule pc@mypc.local
The random image of the key is:
+--[ED25519 256]-+
+----[SHA256]-----+

#### We have these two keys, now we have to transfer the public key:

ssh-copy-id -i .ssh/id_ed25519.pub user@monip -p 6666


/usr/bin/ssh-copy-id: INFO: Source of the key(s) to install: ".ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempt to connect with the new key(s), to filter out those already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now, it is to install the new keys
the user password@monip:

Number of key(s) added: 1

Now try to connect to the machine, with: "ssh -p '6666' 'user@monip'" and check that only the keys you wanted were added.

#### We can now connect with a passphrase:

 ssh -p '6666' 'user@myp' (user@myp)
Enter the passphrase for the key '/Users/pc/.ssh/id_ed25519':

#### That's it!

user@servssh:~$

