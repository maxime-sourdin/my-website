Title: Configurer Unbound
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Réseau
Tags: DNS
Summary: Configuration simple d'unbound

    server:
            verbosity: 3
            interface: 192.168.1.2
            interface: ::1
            do-ip6: yes
            do-ip4: yes
            do-udp: yes
            do-tcp: yes

        access-control: 192.168.1.0/24 allow
        access-control: ::0/0 allow
        access-control: 127.0.0.0/8 allow
        access-control: ::1 allow

        hide-identity: yes
        harden-algo-downgrade: no
        harden-glue: yes
        hide-version: yes
        harden-below-nxdomain: yes
        auto-trust-anchor-file: "/var/lib/unbound/root.key"
        root-hints: "/var/lib/unbound/root.hints"
        module-config: "validator iterator"

        prefetch: yes
        prefetch-key: yes
        qname-minimisation: yes
        harden-dnssec-stripped: yes
        use-caps-for-id: yes
        cache-min-ttl: 3600
        cache-max-ttl: 86400
        prefetch: yes
        num-threads: 6
        msg-cache-slabs: 16
        rrset-cache-slabs: 16
        infra-cache-slabs: 16
        key-cache-slabs: 16
        rrset-cache-size: 256m
        msg-cache-size: 128m
        so-rcvbuf: 1m
        unwanted-reply-threshold: 10000
        do-not-query-localhost: yes
        val-clean-additional: yes
        use-syslog: yes
        logfile: /var/log/unbound.log
