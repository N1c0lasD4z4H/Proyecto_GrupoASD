#!/bin/bash
set -e

# Instalar Docker
yum update -y
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Instalar Docker Compose
DOCKER_COMPOSE_VERSION=v2.27.0
curl -L "https://github.com/docker/compose/releases/download/$%7BDOCKER_COMPOSE_VERSION%7D/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Crear carpeta del proyecto
mkdir -p /home/ec2-user/app
cd /home/ec2-user/app
