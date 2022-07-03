Title: Monitoring facile avec checkup et Grafana
Date: 2021:04:23 18:00
Authors: Maxime SOURDIN
Category: Supervision
Tags: Grafana
Summary: Surveiller l'état de ses services facilement

Quelques prérequis :

- un bucket S3 (sur n'importe quel service compatible)

- Docker ou Podman

# Première étape : le déploiement de Grafana et Prometheus via docker-compose

  ## Édition du fichier docker-compose:

    version: '3'
      grafana:
        image: grafana/grafana
        container_name: grafana
        user: "UID:UID"
        restart: always
        volumes:
          - ./grafana/data:/var/lib/grafana
        networks:
          - monitoring
        healthcheck:
          test: curl -f http://127.0.0.1:3000 || exit 1
          interval: 30s
          retries: 3
     prometheus:
        image: prom/prometheus
        container_name: prometheus
        user: "UID:UID"
        restart: always
        volumes:
          - ./prometheus/config/:/etc/prometheus/
          - ./prometheus/data:/prometheus
        command:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--web.console.libraries=/etc/prometheus/console_libraries'
          - '--web.console.templates=/etc/prometheus/consoles'
          - '--storage.tsdb.retention=200h'
        networks:
          - monitoring
        healthcheck:
          test: curl -f http://127.0.0.1:9090 || exit 1
          interval: 30s
          retries: 3
    networks:
      monitoring:
        driver: bridge

Remplacer l'UID par celui qui a les droits d'exécuter Docker.

 ## Configuration prometheus (dans prometheus/config/prometheus.yml)

    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "targets.rules"
      - "host.rules"
      - "containers.rules"
    
    scrape_configs:
      - job_name: 'prometheus'
        scrape_interval: 10s
        static_configs:
          - targets: ['localhost:9090']


Ensuite, faites un docker-compose up -d et suivez la configuration pas à pas de Grafana (mot de passe administrateur·ice.)

Pour la datasource, il s'agit de prometheus, celle-ci doit donc pointer vers http://prometheus:9090. Attention, le trafic passe donc en clair.

 ## Ajout d'un nouveau type de datasource: Infinity

 Vous pouvez retrouver le code [d'Infinity ici](https://github.com/yesoreyeram/grafana-infinity-datasource).

 Pour l'installer c'est très simple:

     docker exec -ti grafana grafana-cli plugins install yesoreyeram-infinity-datasource
    docker restart grafana

# Seconde étape: compilation d'une image Docker personnalisée de Checkup

## Récupération des sources

Récupérez les sources de [checkup](https://github.com/sourcegraph/checkup) ici. Il va falloir modifier plusieurs lignes dans checkup/storage/fs/types.go:

    package fs
    //import (
    //	"fmt"
    //	"github.com/sourcegraph/checkup/types"
    //)
    const IndexName = "index.json"
    // FilenameFormatString is the format string used
    // by GenerateFilename to create a filename.
    const FilenameFormatString = ""
    //const FilenameFormatString = "latest.json"
    // GenerateFilename returns a filename that is ideal
    // for storing the results file on a storage provider
    // that relies on the filename for retrieval that is
    // sorted by date/timeframe. It returns a string pointer
    // to be used by the AWS SDK...
    func GenerateFilename() *string {
    	s:= "latest.json"
    //	s := fmt.Sprintf(FilenameFormatString, types.Timestamp())
    	return &s
    }

Au lieu de faire un fichier différent à chaque test, le fichier distant sera écrasé. Pour pouvoir faire traiter le fichier par Grafana, cela sera plus simple.

Il faut également modifier le Dockerfile:

    FROM golang:1.16.3-alpine as builder
    ENV CGO_ENABLED=0
    COPY . /app
    WORKDIR /app
    RUN apk --no-cache add make && make build
    FROM alpine:latest
    WORKDIR /app
    COPY --from=builder /app/builds/checkup /usr/local/bin/checkup
    ADD statuspage/ /app/statuspage
    RUN (echo "*/5 * * * * cd /app && checkup --store") | crontab -
    CMD /bin/sh -c "exec crond -f -L /dev/stdout && cd /app && checkup --store"

Cela permet d'automatiser les tests (toutes les 5 minutes), et également d'utiliser une image Golang plus moderne.

## Compilation de l'image

Pour un processeur x86-64 classique:

    docker buildx build --platform linux/amd64 -t monrepodocker.com/checkup --push .

Pour un Raspberry Pi Zero W (à noter que celle-ci se passe sans problème sur l'architecture M1) :

    docker buildx build --platform linux/arm/v6 -t monrepodocker.com/checkup:maison1 --push .

# Troisième étape: configuration d'un bucket S3

## Création du bucket

Créez votre bucket via l'interface ou via la cli, puis créer un utilisateur·ice avec un accès API. Notez bien l'access key et la secret key

## Stratégie IAM pour l'utilisateur·ice

Un exemple de stratégie IAM pour l'utilisateur·ice:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject"
                ],
                "Resource": [
                    "arn:aws:s3:::nombucket/*",
                    "arn:aws:s3:::nombucket/*"
                ]
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucketMultipartUploads",
                    "s3:AbortMultipartUpload",
                    "s3:ListMultipartUploadParts"
                ],
                "Resource": [
                    "arn:aws:s3:::nombucket/*",
                    "arn:aws:s3:::nombucket"
                ]
            },
            {
                "Sid": "VisualEditor2",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucketMultipartUploads",
                    "s3:AbortMultipartUpload",
                    "s3:ListMultipartUploadParts"
                ],
                "Resource": [
                    "arn:aws:s3:::nombucket/*",
                    "arn:aws:s3:::nombucket"
                ]
            }
        ]
    }
    
## Stratégie pour le bucket

    {
        "Version": "2012-10-17",
        "Id": "S3PolicyId1",
        "Statement": [
            {
                "Sid": "IPAllow",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "ARN BUCKET/*",
                "Condition": {
                    "IpAddress": {
                        "aws:SourceIp": "IP DE GRAFANA"
                    }
                }
            }
        ]
    }

Remplacer les valeurs en majuscule (dans Resource et aws:SourceIp) et votre bucket sera prêt.

# Quatrième étape: édition des tests et des notifications

## Édition de la configuration: checkup.json

Un fichier checkup.json complet:

        {"storage":{"type":"s3","access_key_id":"ACCESS KEY ID S3","secret_access_key":"SECRET ACCESS KEY S3","region":"eu-west-3","bucket":"BUCKET S3","check_expiry":604800000000000},
        "notifiers":[{"type": "mail","from": "POSTMASTER@EXAMPLE.COM","to": [ "DESTINATAIRE@EXAMPLE.ORG" ],"subject": "Status Alert","smtp": {"server": "SERVEUR MAIL","port": 587,"username": "POSTMASTER@EXAMPLE.COM","password": "MOT DE PASSE POSTMASTER"}},
        {"type": "slack","username": "Status Bot (maison1)","channel": "#système","webhook": "WEBHOOK DISCORD"/slack"}],
        "checkers":[{"type":"tcp","endpoint_name":"Livebox","endpoint_url":"172.16.0.1:443","threshold_rtt":500000000,"attempts":5},
       {"type":"tcp","endpoint_name":"wifi1","endpoint_url":"192.168.1.1:80","threshold_rtt":500000000,"attempts":5},
    {"type":"tcp","endpoint_name":"FreeNAS","endpoint_url":"172.16.0.3:443","threshold_rtt":500000000,"attempts":5},
        {"type": "tcp","endpoint_name": "FreeNAS SMB","endpoint_url": "172.16.0.3:445"},  
        {"type": "tcp","endpoint_name": "Plex","endpoint_url": "172.16.0.6:32400"} ],
        "timestamp":"0001-01-01T00:00:00Z"}

En décomposant un peu, on a :

### La configuration pour le bucket S3

        {"storage":{"type":"s3","access_key_id":"ACCESS KEY ID S3","secret_access_key":"SECRET ACCESS KEY S3","region":"REGION","bucket":"BUCKET S3","check_expiry":604800000000000}
Remplacer les valeurs en majuscule par celles obtenues précédemment, pour permettre la connexion au bucket.

### La configuration des notifications mails et Discord

        "notifiers":[{"type": "mail","from": "POSTMASTER@EXAMPLE.COM","to": [ "DESTINATAIRE@EXAMPLE.ORG" ],"subject": "Status Alert","smtp": {"server": "SERVEUR MAIL","port": 587,"username": "POSTMASTER@EXAMPLE.COM","password": "MOT DE PASSE POSTMASTER"}}, {"type": "slack","username": "Status Bot (maison1)","channel": "#système","webhook": "WEBHOOK DISCORD"/slack"}],
Ici, c'est encore plus simple (il est toujours question de remplacer les valeurs en majuscule), évidemment pensez à créer un compte mail dédié pour limiter les risques.

Pour la partie Discord, je vous renvoie vers la documentation [Discord](https://support.discord.com/hc/fr/articles/228383668-Utiliser-les-Webhooks).
Remplacer 'WEBHOOK DISCORD" par l'URL de votre webhook, et gardez le /slack à la fin. C'est un mode de compatibilité particulièrement utile.

### La configuration des tests

[La documentation est particulièrement claire](https://github.com/sourcegraph/checkup/blob/master/README.md) :

        #### HTTP Checker
    
    {
        "type": "http",
        "endpoint_name": "Example HTTP",
        "endpoint_url": "http://www.example.com"
    }
    
    #### TCP Checker
        
    {
        "type": "tcp",
        "endpoint_name": "Example TCP",
        "endpoint_url": "example.com:80"
    }
    
    #### DNS Checkers
    
    {
        "type": "dns",
        "endpoint_name": "Example of endpoint_url looking up host.example.com",
        "endpoint_url": "ns.example.com:53",
        "hostname_fqdn": "host.example.com"
    }
    
    #### TLS Checkers:     
    {
        "type": "tls",
        "endpoint_name": "Example TLS Protocol Check",
        "endpoint_url": "www.example.com:443"
    }

Dans mon cas, je teste seulement si les hôtes sont joignables, via un petit ping sur les ports censés répondre.

    "checkers":[{"type":"tcp","endpoint_name":"Livebox","endpoint_url":"172.16.0.1:443","threshold_rtt":500000000,"attempts":5}, {"type":"tcp","endpoint_name":"wifi1","endpoint_url":"192.168.1.1:80","threshold_rtt":500000000,"attempts":5}, {"type":"tcp","endpoint_name":"FreeNAS","endpoint_url":"172.16.0.3:443","threshold_rtt":500000000,"attempts":5},
    {"type": "tcp","endpoint_name": "FreeNAS SMB","endpoint_url": "172.16.0.3:445"},
    {"type": "tcp","endpoint_name": "Plex","endpoint_url": "172.16.0.6:32400"}],

Ci-dessous, le test de mon Shaarli. Attention, les tests HTTP sont sensibles aux redirections, en cas de retour d'un code HTTP 302, le service est considéré comme DOWN.

    {"type":"http","endpoint_name":"Shaarli","endpoint_url":"https://links.maxime.sourdin.ovh","threshold_rtt":500000000,"attempts":5}

### Le format pour l'horodatage
    "timestamp":"0001-01-01T00:00:00Z"}

## Sécurisation du fichier checkup.json

Etant donné que le conteneur est exécuté avec l'utilisateur·ice courant·e, pensez à appliquer les bonnes autorisations au fichier, vu qu'il contient de quoi accéder à un bucket et de quoi accéder à une boite mail:

    chmod 600 checkup.json

En cas de soucis avec le bucket, le peu d'informations qui pourront être retirées sont des ports pour se connecter et des URL, par exemple :

    [{"title":"Livebox","endpoint":"172.16.0.1:443","timestamp":1620243308993278950,"times":[{"rtt":20929892},{"rtt":48361749},{"rtt":23045881},{"rtt":35709815},{"rtt":36920809}],"threshold":500000000,"healthy":true},{"title":"wifi1","endpoint":"192.168.1.1:80","timestamp":1620243308994907941,"times":[{"rtt":27225859},{"rtt":34943819},{"rtt":39484795},{"rtt":30538842},{"rtt":29570846}],"threshold":500000000,"healthy":true},{"title":"FreeNAS","endpoint":"172.16.0.3:443","timestamp":1620243308996989931,"times":[{"rtt":51494733},{"rtt":38261802},{"rtt":23417879},{"rtt":37854803},{"rtt":13516930}],"threshold":500000000,"healthy":true},{"title":"FreeNAS SMB","endpoint":"172.16.0.3:445","timestamp":1620243309000877911,"times":[{"rtt":38250802}],"healthy":true},{"title":"Plex","endpoint":"172.16.0.6:32400","timestamp":1620243308975109044,"times":[{"rtt":61374682}],"healthy":true}]

# Cinquième étape : utilisation dans Grafana

## Configuration de la datasource

Dans Paramétres/Datasources, sélectionnez "Infinity".
Donnez lui un nom, et pour l'URL, il suffit d'indiquer celle du bucket (sans mot de passe, ni nom de fichier à la fin de celle-ci).

Après avoir cliqué sur "Save & Test", cette source sera disponible.

## Ajout d'un panel

Sur un nouveau dashboard, ou un existant, ajoutez un panel, et sélectionnez la datasource créée précédemment.

Dans l'URL, indiquez le nom de votre fichier (comme latest.json par exemple), normalement le passage en mode table de l'affichage sera proposé. Il ne restera plus qu'à sélectionner les colonnes intéressantes, et à les renommer, en se servant de ce que Grafana permet.

![Panel Grafana, où l'affichage des données récupérées est paramétré : chaque colonne est renommée correctement (Service, Value et URL au lieu de title, endpoint, timestamp, times, thresold, healthy)]({static}/medias/checkup-grafana-2.png)

## Exemple de dashboard

### JSON

    {
    "annotations": {
        "list": [
        {
            "builtIn": 1,
            "datasource": "-- Grafana --",
            "enable": true,
            "hide": true,
            "iconColor": "rgba(0, 211, 255, 1)",
            "name": "Annotations & Alerts",
            "type": "dashboard"
        }
        ]
    },
    "editable": true,
    "gnetId": null,
    "graphTooltip": 0,
    "id": 18,
    "links": [],
    "panels": [
        {
        "datasource": "statuspage",
        "description": "",
        "fieldConfig": {
            "defaults": {
            "color": {
                "mode": "thresholds"
            },
            "custom": {
                "align": null,
                "displayMode": "color-text",
                "filterable": false
            },
            "mappings": [],
            "noValue": "KO",
            "thresholds": {
                "mode": "absolute",
                "steps": [
                {
                    "color": "red",
                    "value": null
                }
                ]
            }
            },
            "overrides": []
        },
        "gridPos": {
            "h": 20,
            "w": 12,
            "x": 0,
            "y": 0
        },
        "id": 3,
        "options": {
            "showHeader": true,
            "sortBy": [
            {
                "desc": false,
                "displayName": "Service"
            }
            ]
        },
        "pluginVersion": "7.5.5",
        "targets": [
            {
            "columns": [
                {
                "selector": "title",
                "text": "Service",
                "type": "string"
                },
                {
                "selector": "healthy",
                "text": "Value",
                "type": "string"
                },
                {
                "selector": "endpoint",
                "text": "URL",
                "type": "string"
                }
            ],
            "data": "",
            "filters": [
                {
                "field": "Value",
                "operator": "in",
                "value": [
                    ""
                ]
                }
            ],
            "format": "table",
            "global_query_id": "",
            "hide": false,
            "query_mode": "standard",
            "refId": "A",
            "root_selector": "",
            "source": "url",
            "type": "json",
            "url": "latest.json",
            "url_options": {
                "data": "",
                "method": "GET"
            }
            }
        ],
        "title": "Services KO",
        "transformations": [
            {
            "id": "organize",
            "options": {
                "excludeByName": {
                "Value": true,
                "endpoint": true,
                "threshold": true,
                "times": true,
                "timestamp": true
                },
                "indexByName": {},
                "renameByName": {
                "endpoint": "URL",
                "healthy": "Statut",
                "title": "Service"
                }
            }
            }
        ],
        "type": "table"
        },
        {
        "datasource": "statuspage",
        "description": "",
        "fieldConfig": {
            "defaults": {
            "color": {
                "mode": "thresholds"
            },
            "custom": {
                "align": null,
                "displayMode": "color-text",
                "filterable": false
            },
            "mappings": [],
            "noValue": "KO",
            "thresholds": {
                "mode": "absolute",
                "steps": [
                {
                    "color": "red",
                    "value": null
                }
                ]
            }
            },
            "overrides": []
        },
        "gridPos": {
            "h": 20,
            "w": 12,
            "x": 12,
            "y": 0
        },
        "id": 5,
        "options": {
            "showHeader": true,
            "sortBy": [
            {
                "desc": false,
                "displayName": "Service"
            }
            ]
        },
        "pluginVersion": "7.5.5",
        "targets": [
            {
            "columns": [
                {
                "selector": "title",
                "text": "Service",
                "type": "string"
                },
                {
                "selector": "healthy",
                "text": "Value",
                "type": "string"
                },
                {
                "selector": "endpoint",
                "text": "URL",
                "type": "string"
                }
            ],
            "data": "",
            "filters": [
                {
                "field": "Value",
                "operator": "in",
                "value": [
                    ""
                ]
                }
            ],
            "format": "table",
            "global_query_id": "",
            "hide": false,
            "query_mode": "standard",
            "refId": "A",
            "root_selector": "",
            "source": "url",
            "type": "json",
            "url": "maison.json",
            "url_options": {
                "data": "",
                "method": "GET"
            }
            }
        ],
        "title": "Maison KO",
        "transformations": [
            {
            "id": "organize",
            "options": {
                "excludeByName": {
                "Value": true,
                "endpoint": true,
                "threshold": true,
                "times": true,
                "timestamp": true
                },
                "indexByName": {},
                "renameByName": {
                "endpoint": "URL",
                "healthy": "Statut",
                "title": "Service"
                }
            }
            }
        ],
        "type": "table"
        },
        {
        "collapsed": true,
        "datasource": null,
        "gridPos": {
            "h": 1,
            "w": 24,
            "x": 0,
            "y": 20
        },
        "id": 7,
        "panels": [
            {
            "datasource": "statuspage",
            "description": "",
            "fieldConfig": {
                "defaults": {
                "color": {
                    "mode": "thresholds"
                },
                "custom": {
                    "align": null,
                    "displayMode": "color-text",
                    "filterable": false
                },
                "mappings": [],
                "noValue": "KO",
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                    {
                        "color": "green",
                        "value": null
                    }
                    ]
                }
                },
                "overrides": [
                {
                    "matcher": {
                    "id": "byName",
                    "options": "Service"
                    },
                    "properties": [
                    {
                        "id": "custom.width",
                        "value": 175
                    }
                    ]
                }
                ]
            },
            "gridPos": {
                "h": 22,
                "w": 12,
                "x": 0,
                "y": 21
            },
            "id": 2,
            "options": {
                "showHeader": true,
                "sortBy": [
                {
                    "desc": false,
                    "displayName": "Service"
                }
                ]
            },
            "pluginVersion": "7.5.5",
            "targets": [
                {
                "columns": [
                    {
                    "selector": "title",
                    "text": "Service",
                    "type": "string"
                    },
                    {
                    "selector": "healthy",
                    "text": "Value",
                    "type": "string"
                    },
                    {
                    "selector": "endpoint",
                    "text": "URL",
                    "type": "string"
                    }
                ],
                "data": "",
                "filters": [
                    {
                    "field": "Value",
                    "operator": "notin",
                    "value": [
                        ""
                    ]
                    }
                ],
                "format": "table",
                "global_query_id": "",
                "hide": false,
                "query_mode": "standard",
                "refId": "A",
                "root_selector": "",
                "source": "url",
                "type": "json",
                "url": "latest.json",
                "url_options": {
                    "data": "",
                    "method": "GET"
                }
                }
            ],
            "title": "Services OK",
            "transformations": [
                {
                "id": "organize",
                "options": {
                    "excludeByName": {
                    "Value": true,
                    "endpoint": true,
                    "threshold": true,
                    "times": true,
                    "timestamp": true
                    },
                    "indexByName": {},
                    "renameByName": {
                    "endpoint": "URL",
                    "healthy": "Statut",
                    "title": "Service"
                    }
                }
                }
            ],
            "type": "table"
            },
            {
            "datasource": "statuspage",
            "description": "",
            "fieldConfig": {
                "defaults": {
                "color": {
                    "mode": "thresholds"
                },
                "custom": {
                    "align": null,
                    "displayMode": "color-text",
                    "filterable": false
                },
                "mappings": [],
                "noValue": "KO",
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                    {
                        "color": "green",
                        "value": null
                    }
                    ]
                }
                },
                "overrides": [
                {
                    "matcher": {
                    "id": "byName",
                    "options": "Service"
                    },
                    "properties": [
                    {
                        "id": "custom.width",
                        "value": 175
                    }
                    ]
                }
                ]
            },
            "gridPos": {
                "h": 22,
                "w": 12,
                "x": 12,
                "y": 21
            },
            "id": 4,
            "options": {
                "showHeader": true,
                "sortBy": [
                {
                    "desc": false,
                    "displayName": "Service"
                }
                ]
            },
            "pluginVersion": "7.5.5",
            "targets": [
                {
                "columns": [
                    {
                    "selector": "title",
                    "text": "Service",
                    "type": "string"
                    },
                    {
                    "selector": "healthy",
                    "text": "Value",
                    "type": "string"
                    },
                    {
                    "selector": "endpoint",
                    "text": "URL",
                    "type": "string"
                    }
                ],
                "data": "",
                "filters": [
                    {
                    "field": "Value",
                    "operator": "notin",
                    "value": [
                        ""
                    ]
                    }
                ],
                "format": "table",
                "global_query_id": "",
                "hide": false,
                "query_mode": "standard",
                "refId": "A",
                "root_selector": "",
                "source": "url",
                "type": "json",
                "url": "maison.json",
                "url_options": {
                    "data": "",
                    "method": "GET"
                }
                }
            ],
            "title": "Maison OK",
            "transformations": [
                {
                "id": "organize",
                "options": {
                    "excludeByName": {
                    "Value": true,
                    "endpoint": true,
                    "threshold": true,
                    "times": true,
                    "timestamp": true
                    },
                    "indexByName": {},
                    "renameByName": {
                    "endpoint": "URL",
                    "healthy": "Statut",
                    "title": "Service"
                    }
                }
                }
            ],
            "type": "table"
            }
        ],
        "title": "OK",
        "type": "row"
        }
    ],
    "schemaVersion": 27,
    "style": "dark",
    "tags": [],
    "templating": {
        "list": []
    },
    "time": {
        "from": "now-5m",
        "to": "now"
    },
    "timepicker": {},
    "timezone": "",
    "title": "Status Page",
    "uid": "IERYjr9Mk",
    "version": 12
    }

### Capture d'écran du dashboard final

![Dashboard Grafana, où il y a quatre panels : deux sont vides, et remontent les services KO, et deux autres sont pleins, et donnent la liste des services fonctionnant correctement]({static}/medias/checkup-grafana-1.png)

### Capture d'écran d'un mail d'alerte

![Mail d'alerte : "Checkup has detected the following issues: Autoblog - Status degraded, Kanboard - Status degraded, Notes - Status degraded, Wallabag - Status degraded ]({static}/medias/checkup-grafana-3.png)

### Capture d'écran d'une alerte sur Discord

![Messages Discord : Notes (Status DEGRADED) et Wallabag (Status DEGRADED)]({static}/medias/checkup-grafana-4.png)

# Fichier docker-compose final

    version: '3'
      grafana:
        image: grafana/grafana
        container_name: grafana
        user: "UID:UID"
        restart: always
        volumes:
          - ./grafana/data:/var/lib/grafana
        networks:
          - monitoring
        healthcheck:
          test: curl -f http://127.0.0.1:3000 || exit 1
          interval: 30s
          retries: 3
     prometheus:
        image: prom/prometheus
        container_name: prometheus
        user: "UID:UID"
        restart: always
        volumes:
          - ./prometheus/config/:/etc/prometheus/
          - ./prometheus/data:/prometheus
        command:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--web.console.libraries=/etc/prometheus/console_libraries'
          - '--web.console.templates=/etc/prometheus/consoles'
          - '--storage.tsdb.retention=200h'
        networks:
          - monitoring
        healthcheck:
          test: curl -f http://127.0.0.1:9090 || exit 1
          interval: 30s
          retries: 3
     checkup:
        hostname: checkup
        image: monrepodocker.com/checkup:latest
        user: "UID:UID"
        volumes:
         - ./checkup/checkup.json:/app/checkup.json:ro
         - ./checkup/checks:/app/checks
        restart: always
    networks:
      monitoring:
        driver: bridge
