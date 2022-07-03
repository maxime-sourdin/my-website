Title: One-liner pour Trivy
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Sécurité
Summary: Scanner rapidement toutes ses images Docker
Tags: Trivy

    for image in $(docker image ls | awk '{print $1,$2}' | sed -e "s/ /:/g" | sed '/REPOSITORY:TAG/d'); do docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v caches:/root/.cache/ aquasec/trivy $image >> output ; done
