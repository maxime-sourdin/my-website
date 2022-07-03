Title: Rickroller les scanneurs de sites et de serveurs
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Summary: Une redirection blagueuse des pages d'erreurs
Tags: Shitpost

Il y a juste un fichier de configuration Nginx à éditer:

	sudo nano /etc/nginx/snippets/rickroll.conf

    error_page 404 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 500 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 501 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 502 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 503 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 504 =301 https://youtu.be/dQw4w9WgXcQ?t=44;

Pensez à l'intégrer dans votre configuration Nginx:

        sudo nano /etc/nginx/snippets/monsite.conf

    include ../snippets/rickroll.conf;

Et ensuite,  Nginx doit être redémarré:

	sudo  systemctl restart nginx

