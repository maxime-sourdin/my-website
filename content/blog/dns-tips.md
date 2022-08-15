Title: Some DNS Tips
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Network
Tags: Tips
Summary: Simple configuration of unbound and dnscrypt-proxy
save_as: dns-tips.html

# Unbound

## Edit /etc/unbound/unbound.conf

    server :
        verbosity : 3
        interface : 192.168.1.2
        interface : ::1
        do-ip6 : yes
        do-ip4: yes
        do-udp: yes
        do-tcp: yes

    access control: 192.168.1.0/24 allowed
    access control: ::0/0 allowed
    access control: 127.0.0.0/8 allowed
    access control : ::1 allowed

    hide-identity: yes
    harden-algo-downgrade : no
    harden-glue : yes
    hide-version : yes
    harden-below-nxdomain : yes
    auto-trust-anchor-file : "/var/lib/unbound/root.key
    root-hints: "/var/lib/unbound/root.hints
    module-config : "validation iterator".

    prefetch: yes
    prefetch-key: yes
    qname-minimization: yes
    harden-dnssec-stripped: yes
    use-caps-for-id : yes
    cache-min-ttl: 3600
    cache-max-ttl : 86400
    prefetch: yes
    num-threads : 6
    msg-cache-slabs: 16
    rrset-cache-slabs: 16
    buffers for infra caches: 16
    buffers for key cache: 16
    rrset cache size: 256m
    msg cache size: 128m
    so-rcvbuf: 1m
    unwanted-reply-threshold: 10000
    do-not-query-localhost: yes
    val-clean-additional: yes
    use-syslog : yes
    logfile : /var/log/unbound.log

## dnscrypt-proxy

### Generate DNS STAMP

- Use this site to generate the DNS STAMP of your DNS server over HTTPS](https://dnscrypt.info/stamps/)
- Note this value, it should be included at the end of the configuration file

### Edit /etc/dnscrypt-proxy/dnscrypt-proxy.toml

        ##############################################
        #                                            #
        #        dnscrypt-proxy configuration        #
        #                                            #
        ##############################################


        ##################################
        #         Global settings        #
        ##################################

        ## List of servers to use
        ##
        ## Servers from the "public-resolvers" source (see down below) can
        ## be viewed here: https://dnscrypt.info/public-servers
        ##
        ## The proxy will automatically pick working servers from this list.
        ## Note that the require_* filters do NOT apply when using this setting.
        ##
        ## By default, this list is empty and all registered servers matching the
        ## require_* filters will be used instead.
        ##
        ## Remove the leading # first to enable this; lines starting with # are ignored.

        server_names = ['sourdin']
        ## List of local addresses and ports to listen to. Can be IPv4 and/or IPv6.
        ## Example with both IPv4 and IPv6:
        ## listen_addresses = ['127.0.0.1:53', '[::1]:53']
        ##
        ## To listen to all IPv4 addresses, use `listen_addresses = ['0.0.0.0:53']`
        ## To listen to all IPv4+IPv6 addresses, use `listen_addresses = ['[::]:53']`
        listen_addresses = []
        ## Maximum number of simultaneous client connections to accept
        max_clients = 250
        ## Switch to a different system user after listening sockets have been created.
        ## Note (1): this feature is currently unsupported on Windows.
        ## Note (2): this feature is not compatible with systemd socket activation.
        ## Note (3): when using -pidfile, the PID file directory must be writable by the new user
        # user_name = 'nobody'
        ## Require servers (from remote sources) to satisfy specific properties
        # Use servers reachable over IPv4
        ipv4_servers = true
        # Use servers reachable over IPv6 -- Do not enable if you don't have IPv6 connectivity
        ipv6_servers = false
        # Use servers implementing the DNSCrypt protocol
        dnscrypt_servers = true
        # Use servers implementing the DNS-over-HTTPS protocol
        doh_servers = true
        ## Require servers defined by remote sources to satisfy specific properties
        # Server must support DNS security extensions (DNSSEC)
        require_dnssec = true
        # Server must not log user queries (declarative)
        require_nolog = true
        # Server must not enforce its own blocklist (for parental control, ads blocking...)
        require_nofilter = true
        # Server names to avoid even if they match all criteria
        disabled_server_names = []
        ## Always use TCP to connect to upstream servers.
        ## This can be useful if you need to route everything through Tor.
        ## Otherwise, leave this to `false`, as it doesn't improve security
        ## (dnscrypt-proxy will always encrypt everything even using UDP), and can
        ## only increase latency.
        force_tcp = false
        ## SOCKS proxy
        ## Uncomment the following line to route all TCP connections to a local Tor node
        ## Tor doesn't support UDP, so set `force_tcp` to `true` as well.
        # proxy = 'socks5://127.0.0.1:9050'
        ## HTTP/HTTPS proxy
        ## Only for DoH servers
        # http_proxy = 'http://127.0.0.1:8888'
        ## How long a DNS query will wait for a response, in milliseconds.
        ## If you have a network with *a lot* of latency, you may need to
        ## increase this. Startup may be slower if you do so.
        ## Don't increase it too much. 10000 is the highest reasonable value.
        timeout = 5000
        ## Keepalive for HTTP (HTTPS, HTTP/2) queries, in seconds
        keepalive = 30
        ## Add EDNS-client-subnet information to outgoing queries
        ##
        ## Multiple networks can be listed; they will be randomly chosen.
        ## These networks don't have to match your actual networks.
        # edns_client_subnet = ['0.0.0.0/0', '2001:db8::/32']
        ## Response for blocked queries. Options are `refused`, `hinfo` (default) or
        ## an IP response. To give an IP response, use the format `a:<IPv4>,aaaa:<IPv6>`.
        ## Using the `hinfo` option means that some responses will be lies.
        ## Unfortunately, the `hinfo` option appears to be required for Android 8+
        # blocked_query_response = 'refused'
        ## Load-balancing strategy: 'p2' (default), 'ph', 'p<n>', 'first' or 'random'
        ## Randomly choose 1 of the fastest 2, half, n, 1 or all live servers by latency.
        ## The response quality still depends on the server itself.
        # lb_strategy = 'p2'
        ## Set to `true` to constantly try to estimate the latency of all the resolvers
        ## and adjust the load-balancing parameters accordingly, or to `false` to disable.
        ## Default is `true` that makes 'p2' `lb_strategy` work well.
        # lb_estimator = true
        ## Log level (0-6, default: 2 - 0 is very verbose, 6 only contains fatal errors)
        # log_level = 2
        ## Log file for the application, as an alternative to sending logs to
        ## the standard system logging service (syslog/Windows event log).
        ##
        ## This file is different from other log files, and will not be
        ## automatically rotated by the application.
        # log_file = 'dnscrypt-proxy.log'
        ## When using a log file, only keep logs from the most recent launch.
        # log_file_latest = true
        ## Use the system logger (syslog on Unix, Event Log on Windows)
        # use_syslog = true
        ## Delay, in minutes, after which certificates are reloaded
        cert_refresh_delay = 240
        ## DNSCrypt: Create a new, unique key for every single DNS query
        ## This may improve privacy but can also have a significant impact on CPU usage
        ## Only enable if you don't have a lot of network load
        # dnscrypt_ephemeral_keys = false
        ## DoH: Disable TLS session tickets - increases privacy but also latency
        # tls_disable_session_tickets = false
        ## DoH: Use a specific cipher suite instead of the server preference
        ## 49199 = TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
        ## 49195 = TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
        ## 52392 = TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305
        ## 52393 = TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305
        ##  4865 = TLS_AES_128_GCM_SHA256
        ##  4867 = TLS_CHACHA20_POLY1305_SHA256
        ##
        ## On non-Intel CPUs such as MIPS routers and ARM systems (Android, Raspberry Pi...),
        ## the following suite improves performance.
        ## This may also help on Intel CPUs running 32-bit operating systems.
        ##
        ## Keep tls_cipher_suite empty if you have issues fetching sources or
        ## connecting to some DoH servers. Google and Cloudflare are fine with it.
        # tls_cipher_suite = [52392, 49199]
        ## Maximum time (in seconds) to wait for network connectivity before
        ## initializing the proxy.
        ## Useful if the proxy is automatically started at boot, and network
        ## connectivity is not guaranteed to be immediately available.
        ## Use 0 to not test for connectivity at all (not recommended),
        ## and -1 to wait as much as possible.
        netprobe_timeout = 60
        ## Address and port to try initializing a connection to, just to check
        ## if the network is up. It can be any address and any port, even if
        ## there is nothing answering these on the other side. Just don't use
        ## a local address, as the goal is to check for Internet connectivity.
        ## On Windows, a datagram with a single, nul byte will be sent, only
        ## when the system starts.
        ## On other operating systems, the connection will be initialized
        ## but nothing will be sent at all.
        netprobe_address = '9.9.9.9:53'
        ## Offline mode - Do not use any remote encrypted servers.
        ## The proxy will remain fully functional to respond to queries that
        ## plugins can handle directly (forwarding, cloaking, ...)
        # offline_mode = false
        ## Additional data to attach to outgoing queries.
        ## These strings will be added as TXT records to queries.
        ## Do not use, except on servers explicitly asking for extra data
        ## to be present.
        ## encrypted-dns-server can be configured to use this for access control
        ## in the [access_control] section
        # query_meta = ['key1:value1', 'key2:value2', 'token:MySecretToken']
        ## Automatic log files rotation
        # Maximum log files size in MB - Set to 0 for unlimited.
        log_files_max_size = 10
        # How long to keep backup files, in days
        log_files_max_age = 7
        # Maximum log files backups to keep (or 0 to keep all backups)
        log_files_max_backups = 1

        #########################
        #        Filters        #
        #########################

        ## Note: if you are using dnsmasq, disable the `dnssec` option in dnsmasq if you
        ## configure dnscrypt-proxy to do any kind of filtering (including the filters
        ## below and blocklists).
        ## You can still choose resolvers that do DNSSEC validation.

        ## Immediately respond to IPv6-related queries with an empty response
        ## This makes things faster when there is no IPv6 connectivity, but can
        ## also cause reliability issues with some stub resolvers.
        block_ipv6 = false
        ## TTL for synthetic responses sent when a request has been blocked (due to
        ## IPv6 or blocklists).

        reject_ttl = 10
        ##################################################################################
        #        Route queries for specific domains to a dedicated set of servers        #
        ##################################################################################

        ## See the `example-forwarding-rules.txt` file for an example
        # forwarding_rules = 'forwarding-rules.txt'
        ###############################
        #        Cloaking rules       #
        ###############################

        ## Cloaking returns a predefined address for a specific name.
        ## In addition to acting as a HOSTS file, it can also return the IP address
        ## of a different name. It will also do CNAME flattening.
        ## If 'cloak_ptr' is set, then PTR (reverse lookups) are enabled
        ## for cloaking rules that do not contain wild cards.
        ##
        ## See the `example-cloaking-rules.txt` file for an example
        # cloaking_rules = 'cloaking-rules.txt'
        ## TTL used when serving entries in cloaking-rules.txt
        # cloak_ttl = 600
        # cloak_ptr = false
        ###########################
        #        DNS cache        #
        ###########################
        ## Enable a DNS cache to reduce latency and outgoing traffic
        cache = true
        ## Cache size
        cache_size = 4096
        ## Minimum TTL for cached entries
        cache_min_ttl = 2400
        ## Maximum TTL for cached entries
        cache_max_ttl = 86400
        ## Minimum TTL for negatively cached entries
        cache_neg_min_ttl = 60
        ## Maximum TTL for negatively cached entries
        cache_neg_max_ttl = 600

        ###############################
        #        Query logging        #
        ###############################
        ## Log client queries to a file
        [query_log]
        ## Path to the query log file (absolute, or relative to the same directory as the config file)
        ## Can be set to /dev/stdout in order to log to the standard output.
        # file = 'query.log'
        ## Query log format (currently supported: tsv and ltsv)
        format = 'tsv'
        ## Do not log these query types, to reduce verbosity. Keep empty to log everything.
        # ignored_qtypes = ['DNSKEY', 'NS']

        ########################################
        #            Static entries            #
        ########################################
        ## Optional, local, static list of additional servers
        ## Mostly useful for testing your own servers.
        [static]
        [static.'sourdin']
        stamp = ''