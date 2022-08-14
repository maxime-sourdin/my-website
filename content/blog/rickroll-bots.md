Title: Rickroll bots and vulnerabilities scanners (Nginx)
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Hardening
Summary: Jopping redirection
Tags: Nginx

# Edit /etc/nginx/snippets/rickroll.conf

    error_page 404 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 500 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 501 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 502 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 503 =301 https://youtu.be/dQw4w9WgXcQ?t=44;
    error_page 504 =301 https://youtu.be/dQw4w9WgXcQ?t=44;

# Edit /etc/nginx/snippets/monsite.conf

    include ../snippets/rickroll.conf;

# Restart Nginx

	sudo systemctl restart nginx
