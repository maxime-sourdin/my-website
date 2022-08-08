Title: Configuration de différents serveurs Web
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Réseau
Summary: Configuration httpd (openbsd)/Nginx/HaProxy
Tags: ServeursWeb

## Conf httpd (openbsd)

    types { include "/usr/share/misc/mime.types" }
    
    
    server "undomaine.com" {
        listen on * port 8080
        block return 301 "https://"
    }
    
    server undomaine.com {
        listen on * tls port 443
       root "/htdocs"
        directory index index.php
    
        hsts
        tls {
            certificate "/etc/letsencrypt/archive/undomaine.com/fullchain1.pem"
     key "/etc/letsencrypt/archive/undomaine.com/privkey1.pem"
        }
    location "*.php" {
                    fastcgi socket "/run/php-fpm.sock"
            }
            directory { index "index.php"}
    
            }
    
    server "www.undomaine.com" {
        listen on * port 8080
        block return 301 "https://"
    }
    
    server www.undomaine.com {
        listen on * tls port 443
        root "/htdocs"
        directory index index.php
        log access "root.log"
    
        hsts
        tls {
            certificate "/etc/letsencrypt/live/www.undomaine.com/fullchain.pem"
            key "/etc/letsencrypt/live/www.undomaine.com/privkey.pem"
        }
    
        location "*.php*" {
            fastcgi socket "/run/php-fpm.sock"
        }
         directory { index "index.php" }
    
        }
    
    
    
    server "blog.undomaine.com" {
        listen on * port 8080
        block return 301 "https://"
    }
    
    server blog.undomaine.com {
        listen on * tls port 443
        root "/htdocs/blog/"
        log access "root.log"
        hsts
        tls {
            certificate "/etc/letsencrypt/live/blog.undomaine.com/fullchain.pem"
            key "/etc/letsencrypt/live/blog.undomaine.com/privkey.pem"}
            location "*.php" {
                    fastcgi socket "/run/php-fpm.sock"
            }
            directory { index "index.php"}
    
        }
    
    
    server "chat.undomaine.com" {
        listen on * port 8080
     block return 301 "https://"
    }
    
    server chat.undomaine.com {
        listen on * tls port 443
        root "/htdocs/chat/"
    log access "root.log"
    hsts
        tls {
            certificate "/etc/letsencrypt/live/chat.undomaine.com/fullchain.pem"
            key "/etc/letsencrypt/live/chat.undomaine.com/privkey.pem"
        }
    location "*.php" {
                    fastcgi socket "/run/php-fpm.sock"
            }
            directory { index "index.php"}
    }
    
    
    server "bin.undomaine.com" {
        listen on * port 8080
        block return 301 "https://"
    }
    
    server bin.undomaine.com {
        listen on * tls port 443
        root "/htdocs/privatebin/"
        log access "root.log"
        hsts
        tls {
            certificate "/etc/letsencrypt/live/bin.undomaine.com/fullchain.pem"
            key "/etc/letsencrypt/live/bin.undomaine.com/privkey.pem"
        }
    location "*.php" {
                    fastcgi socket "/run/php-fpm.sock"
            }
            directory { index "index.php"}
    
     }
