Title: Créer, publier et imprimer son CV avec JsonResume
Date: 2021:04:23 18:00
Authors: Maxime SOURDIN
Category: Devops
Tags: CI/CD
Summary: Automatiser la production de son CV

Quelques prérequis:

- un bucket S3 (sur n'importe quel service compatible)
- une instance Gitlab fonctionnelle
- un [runner Gitlab](https://www.sheevaboite.fr/articles/installer-gitlab-ci-moins-5-minutes-docker/)
- Docker ou Podman
- un nom de domaine
- un compte AWS
 
# Premiére méthode: gitlab-ci

## I- Édition d'un fichier resume.json
Pour commencer il faut d'abord éditer un fichier resume.json, qui contient toutes les données de son CV, vous trouverez ici [un exemple](https://gist.github.com/ishu3101/36186df161316ec00519389b9deec690) propre.

Globalement, faites attention à la [syntaxe JSON](https://gist.github.com/mattcone/ec8057127a0ff2e0b45d2cde14355b2a) et aux alignements, et respectez le nom des catégories, pour évitez des erreurs. L'utilisation d'un vérificateur de syntaxe JSON est recommandée.

Un exemple avec mon [fichier resume.json](https://gitlab.sourdin.ovh/sitespro/website/-/raw/main/resume.json) (un peu abrégé):

    {
      "basics": {
        "name": "Maxime SOURDIN",
        "label": "21 years old, apprenticeship  at OBS (cloud specialist)",
        "picture": "profile.jpeg",
        "email": "maxime@sourdin.ovh",
        "phone": "+33630158452",
        "website": "https://maxime.sourdin.ovh",
        "location": {
          "address": "33 Rue de la Grande Fontaine",
          "postalCode": "35490",
          "city": "Romazy",
          "countryCode": "FR",
          "region": "Bretagne"
        },
        "profiles": [
          {
            "network": "Shaarli",
            "iconClass": "fa fa-shaarli-square",
            "url": "https://links.maxime.sourdin.ovh"
          }
        ]
      },
	  "work": [{
	      "position": "Apprenticeship at OBS",
	      "startDate": "2020-09",
	      "summary": "Automated test chain: Ansible, AWX, Gitlab-ci, Flexible Engine",
	      "highlights": [
	      ]
	    }
	  ],
	  "education": [
	    {
	      "institution": "CNAM & OBS",
	      "area": "Cloud specialist",
	      "startDate": "2020-09",
	      "studyType": "Engineer school"
	    }
	  ],
	  "skills": [
	    {
	      "name": "Devops",
	      "keywords": [
	        "Ansible",
	        "AWX",
	        "Gitlab",
	        "CI/CD",
	        "Docker",
	        "Podman",
	        "Docker Swarm"
	      ]
	    }
	  ],
	  "languages": [
	    {
	      "language": "English",
	      "level": "TOEIC: 620",
	      "fluency": "TOEIC: 620"
	    }
	  ]
	}

## II- Choix d'un thème JSONResume
Vous pouvez trouvez des thèmes n'importe où, [beaucoup sont installables directement](https://www.npmjs.com/search?q=jsonresume-theme) via le gestionnaire de paquets nodeJS. Sinon, beaucoup sont trouvables sur Github, et installables plutôt facilement. Dans tout les cas, ce ne sera pas un soucis pour la suite.

Dans mon cas, j'ai cloné le code du [thème "Even"](https://github.com/rbardini/jsonresume-theme-even),  dont j'ai seulement modifié les couleurs pour le rendre plus accessible aux personnes malvoyantes.

Le code est disponible [ici](https://gitlab.sourdin.ovh/sitespro/website) (oui c'est en vrac).

## III- Compilation de l'image Docker de l'export en PDF

J'ai utilisé le travail de [pinkeen](https://github.com/pinkeen/docker-html-to-pdf) et ait recompilé l'image de mon côté, en mettant à jour juste quelques dépendances ([c'est stocké sur mon gitlab](https://gitlab.sourdin.ovh/sitespro/docker-html-to-pdf)).

Vous pouvez cloner mon repository et ajuster certaines valeurs:

    git clone https://gitlab.sourdin.ovh/sitespro/docker-html-to-pdf
    cd docker-html-to-pdf
 
 Il s'agit surtout du fichier Dockerfile à modifier:

	FROM alpine:latest
	RUN apk update \
	   && apk add --no-cache \
	     chromium \
	     nodejs \
	     npm \
	     sed \
	     bash \
	     procps
	RUN npm install -g \
	     chrome-headless-render-pdf \
	     node-static
	COPY entrypoint.bash /usr/local/bin/entrypoint
	COPY chrome-wrapper.bash /usr/local/bin/chrome-wrapper
	RUN mkdir /tmp/html-to-pdf \
	   && chmod +x /usr/local/bin/*
	ARG WORKDIR="/builds/sitespro/website/public"
	ENV WORKDIR="${WORKDIR}"
	WORKDIR "${WORKDIR}"
	ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

La partie à modifier est celle-ci. C'est normalement une mauvaise pratique, vu que l'image Docker ne sera pas vraiment réutilisable, mais c'est vraiment par facilité ici.

    	ARG WORKDIR="/builds/sitespro/website/public"
   
Il suffit de suivre cette forme:

	ARG WORKDIR="/builds/$NOMUTILISATEUR·ICE ou GROUPE/$NOM DU REPO/public"

Enfin, il suffit de compiler l'image Docker qui va bien, et si vous la créez à distance, la push:

	docker build -t monrepo/htmltopdf .
	docker push monrepo/htmltopdf

Sur un Mac M1, pour la build (testé de mon côté sur un Mini M1, avec absolument aucun probléme de build) :

	docker buildx build --platform linux/amd64 -t monrepo/htmltopdf --push .

## IV- Configuration d'un bucket S3 et édition de la chaîne CI 

### A- S3
Pensez tout d'abord à créer un repository Gitlab vide. Il va falloir renseignez quelques variables (protégées et masquées) pour pouvoir stocker les fichiers sur S3, toutefois, cette méthode est discutable niveau sécurité:

- BUCKET_NAME (le nom du bucket, qui sera accessible en public)
- AWS_ACCESS_KEY_ID (l'identifiant de l'utilisateur·ice)
- AWS_DEFAULT_REGION (la région du bucket)
- AWS_SECRET_ACCESS_KEY (l'access key pour l'utilisateur·ice)
- COMPILATIONPATH (l'emplacement du code: soit   ````/builds/$NOMUTILISATEUR·ICE ou GROUPE/$NOM DU REPO/```` )
- IMAGE (le nom de l'image compilée précédemment)

Un exemple de stratégie IAM pour gérer le bucket:

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
    
Et la stratégie de bucket:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::akia42ti3uitzaacfvxq-cv/*"
            }
        ]
    }

### B- Édition de la chaîne CI
#### Code
Il faut maintenant éditer un fichier .gitlab-ci.yml

    stages:
    - html
    - pdf
    - deploy
    
    cache:
     paths:
       - /builds/$COMPILATIONPATH/node_modules/
       - /builds/$COMPILATIONPATH/public/
    
    htmlgen:
     image: node:lts-alpine3.13
     stage: html
     before_script:
      - apk add --no-cache git nodejs-npm
     artifacts:
      paths:
        - /builds/$COMPILATIONPATH/public
      expire_in: 20 minutes
     script:
      - npm init -y && npm install resume-cli@3.0.0 && npm install
      - nodejs ./node_modules/resume-cli export public/index.html --format html --theme even
    
    pdfgen:
     image:
       name: $IMAGE
       entrypoint: ["/usr/local/bin/entrypoint", "--scale 0.70 --url file:///builds/$COMPILATIONPATH/public/index.html --pdf cv.pdf"]
     stage: pdf
     script:
        - date
     artifacts:
      paths:
        - /builds/$COMPILATIONPATH/public
      expire_in: 20 minutes
     when: on_success
     dependencies:
        - htmlgen
    
    tos3:
     image: python:alpine
     stage: deploy
     before_script:
      - pip install awscli
     script:
      - aws s3 cp /builds/$COMPILATIONPATH/public/index.html s3://${BUCKET_NAME}/
      - aws s3 cp /builds/$COMPILATIONPATH/public/cv.pdf s3://${BUCKET_NAME}/
     environment:
      name: ${CI_COMMIT_REF_SLUG}
      url: https://${BUCKET_NAME}.s3-website.${AWS_DEFAULT_REGION}.amazonaws.com/
     when: on_success
     dependencies:
        - pdfgen

#### Comment se déroule cette chaîne ?

Première étape:
Tout simplement, le premier stage récupère la dernière image Docker nodejs (fonctionnant avec Alpine pour des questions de légèreté).   Enfin les dépendances sont installées (donc resume-cli) et le thème. La version de resume-cli est la 3.0.0 pour cause de bugs non résolus avec les versions suivantes (3.0.4 en avril 2021).

Si vous récupérez un thème distant, il faut remplacer ````npm init -y && npm install resume-cli@3.0.0 && npm install```` par ````npm init -y && npm install resume-cli@3.0.0 && npm install jsonresume-theme-even````.

Enfin, le CV est exporté en HTML dans le dossier public, qui est mis en cache.

Seconde étape:
Un conteneur Docker est lancé avec l'image Docker crée plus tôt, et génère une version PDF, grâce à la version cli de Chrome, toujours dans le dossier public, en se basant sur le fichier index.html de la première étape.

Troisième étape:
Un autre conteneur est lancé, sous Alpine, et installe les outils cli pour uploader directement des fichiers sur AWS.

## V- Création d'un repo de stockage du code

Si vous avez récupéré le code d'un thème, vous pouvez le gardez dans un coin, et ajouter votre fichier resume.json dedans. 
Petite astuce: ajoutez un dossier public pour permettre le stockage des fichiers généré:

    mkdir public
    touch public/.hello

Puis effacer le dossier .git, et faire un git add sur tout les fichiers nécessaires au bon fonctionnement du thème:

- resume.json
- bin/
- index.js
- .gitlab-ci.yml
- netlify.toml
- package-lock.json
- package.json
- partials/
- resume.hbs
- style.css
- tap-snapshots
- public

Ensuite, vous pouvez push le code sur votre repo Gitlab.

## VI- Lancement de la chaîne

A chaque commit, la chaîne se relancera, et recompilera votre CV en HTML et en PDF.

## VII- Publication via Cloudfront
Pour publier le site, une distribution Cloudfront doit être crée et pointer sur le bucket S3. Le [tutoriel AWS](https://aws.amazon.com/fr/premiumsupport/knowledge-center/cloudfront-serve-static-website/) sera plus clair que mes explications.

Enfin le site sera accessible publiquement, si vous ajoutez un enregistrement CNAME sur votre nom de domaine pour pointer vers la distribution CloudFront, avec évidemment un certificat SSL propre correspondant à votre nom de domaine.

Évidemment, c'est la configuration de base donc peu sécurisée et performante, mais suffisante pour proposer deux fichiers.

# docker-compose

Vous pouvez reprendre la partie I, II et III

## IV alternatif

### Compilation de l'image Docker pour utiliser jsonresume

Après avoir récupérer le code du thème, vous pouvez modifier le nom de celui-ci dans ce Dockerfile pour que cela soit cohérent:

    FROM node:current-alpine3.13
    LABEL name=jsonresume
    ENV RESUME_PUPPETEER_NO_SANDBOX=true
    WORKDIR /data
    RUN apk --no-cache add nodejs-npm git chromium
    RUN npm init -y
    RUN npm install resume-cli@3.0.0
    ADD jsonresume-theme-even /data/node_modules/jsonresume-theme-even
    WORKDIR /data/node_modules/jsonresume-theme-even
    RUN npm install
    WORKDIR /data
    ENTRYPOINT ["node", "/data/node_modules/resume-cli"]

Si c'est un thème installable directement, remplacez 

    RUN npm install resume-cli@3.0.0
    ADD jsonresume-theme-even /data/node_modules/jsonresume-theme-even

 par :
 
    RUN npm install resume-cli@3.0.0 jsonresume-theme-even

 Enfin, il faut compiler cette image et si vous la créez à distance, la push:
	
	docker build -t monrepo/jsonresume .
	docker push monrepo/jsonresume

Sur un Mac M1, (toujours testé avec succés sur Mac Mini), pour la build:

	docker buildx build --platform linux/amd64 -t monrepo/jsonresume --push .

### Fichier de configuration nginx
    user  nginx;
    error_log  stderr  warn;
    pid        /var/run/nginx.pid;
    worker_processes  auto;
    worker_rlimit_nofile 4096;
    events {
            worker_connections 4096;
            multi_accept on;
    }    
    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;
    
        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                            '$status $body_bytes_sent "$http_referer" '
                            '"$http_user_agent" "$http_x_forwarded_for"';
    
        sendfile        off;
        #tcp_nopush     on;
        keepalive_timeout           600;
        proxy_connect_timeout       600;
        server_tokens off;
        proxy_send_timeout          600;
        send_timeout                600;
        uwsgi_read_timeout          600;
        # This is the main geonode conf
        charset     utf-8;
        # max upload size
        client_max_body_size 2M;
        client_body_buffer_size 256K;
        large_client_header_buffers 4 64k;
        proxy_read_timeout 600s;
        fastcgi_hide_header Set-Cookie;

      server{
        listen 80;
        index cv.html;
        root   /var/www/html/;
    
        location /{
        rewrite ^(/.*)\.html(\?.*)?$ $1$2 permanent;
        rewrite ^/(.*)/$ /$1 permanent;
        try_files $uri/index.html $uri.html $uri/ $uri =404;
                add_header Access-Control-Allow-Methods "GET, POST";
            }
     }
        #include /etc/nginx/conf.d/*.conf;
    }

### docker-compose.yml

    services:
        webserver:
            image: nginx
            healthcheck:
                test: curl -f http://127.0.0.1:80 || exit 1
                interval: 30s
                retries: 3
            volumes:
                - cv:/var/www/html
                - ./webserver/nginx.conf:/etc/nginx/nginx.conf:ro
        generate:
            image: monrepo/jsonresume
            command: export --theme even /tmp/resume_output/cv.html
            volumes:
                -  cv:/tmp/resume_output/
                - ./files/resume.json:/data/resume.json:ro
                - ./files/profile.jpeg:/data/node_modules/jsonresume-theme-even/profile.jpeg:ro
        pdf:
            image: monrepo/html-to-pdf
            working_dir: /workspace/
            command: --url file:///workspace/cv.html --pdf cv.pdf --scale 0.72
            volumes:
                - cv:/workspace
    volumes:
      cv:

###  Utilisation finale
Il suffira juste d'utiliser un reverse proxy pour rendre accessible votre CV.