Title: Quelques grok patterns
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Logs
Tags: HaProxy
Summary: Grok pattern pour HaProxy et Syslog

## Grok pattern haproxy

    %{SYSLOGTIMESTAMP:timestamp}.* %{DATA:Haproxy_process}: %{IP:client_ip}.*\[%{HAPROXYDATE:accept_date}\] %{NOTSPACE:frontend_name} %{NOTSPACE:backend_name}/%{NOTSPACE:server_name} %{INT:Tq}/%{INT:Tw}/%{INT:Tc}/%{INT:Tr}/%{INT:Tt} %{DATA:http_status_code} %{NOTSPACE:bytes_read} - - ---- %{INT:actconn}/%{INT:feconn
    }/%{INT:beconn}/%{INT:srvconn}/%{NOTSPACE:retries} %{INT:srv_queue}/%{INT:backend_queue} "%{WORD:Method} %{URIPATHPARAM:request} HTTP/%{NUMBER:http_version}"

## Grok pattern syslog

    %{SYSLOGTIMESTAMP:syslog_timestamp} %{IP:server_ip} %{PROG:program}(?:\[%{POSINT:pid}\])?(?=%{GREEDYDATA:syslog_message})
