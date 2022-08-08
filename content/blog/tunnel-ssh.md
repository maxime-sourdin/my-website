Title: Mettre en place un tunnel SSH permanent
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Bidouille
Summary: Faire le lien entre deux machines
Tags: SSH

# Fichiers de configuration

## http.service:

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


sshd_config

...
    Match User tunnelshell
    PermitTunnel yes
    AllowAgentForwarding no
    AuthenticationMethods publickey
    AllowTcpForwarding yes
    ForceCommand /bin/false
    #   GatewayPorts clientspecified
