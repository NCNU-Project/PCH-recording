#!/bin/bash

if ! [ -x "$(command -v docker)" ]; then
    echo "docker not installed, run the 'curl -L get.docker.com | sudo sh' to install"
    exit 1
fi

# chean up environments
docker compose -f ./setup/docker-compose.yml down
# create new containers
docker compose -f ./setup/docker-compose.yml up
