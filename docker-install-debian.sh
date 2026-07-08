#!/bin/bash

set -e

echo "Updating packages..."
sudo apt update
sudo apt install -y ca-certificates curl gnupg

echo "Adding Docker GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/debian/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Installing Docker..."
sudo apt update

sudo apt install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

echo "Starting Docker..."
sudo systemctl enable docker
sudo systemctl start docker

echo "Configuring Docker for non-root user..."
sudo groupadd docker 2>/dev/null || true
sudo usermod -aG docker "$USER"

echo ""
echo "==========================================="
echo "Docker installation completed successfully!"
echo "==========================================="
echo ""
docker --version
docker compose version

echo ""
echo "Run ONE of the following before using Docker without sudo:"
echo ""
echo "Option 1 (recommended): Log out and log back in."
echo ""
echo "Option 2:"
echo "    newgrp docker"
echo ""
echo "Test with:"
echo "    docker run hello-world"