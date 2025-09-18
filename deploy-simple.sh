#!/bin/bash

# Simple deployment script for Azure VM
# Usage: curl -fsSL https://raw.githubusercontent.com/ashish9825/fake-news/main/deploy-simple.sh | bash

set -e

echo "🚀 Starting simple deployment..."

# Variables
REPO_URL="https://github.com/ashish9825/fake-news.git"
APP_DIR="/opt/fake-news-detector"
USER=$(whoami)

# Update system
echo "📦 Updating system packages..."
sudo apt-get update

# Install Git if not present
if ! command -v git &> /dev/null; then
    echo "📦 Installing Git..."
    sudo apt-get install -y git
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "⚠️  You may need to log out and back in for Docker permissions to take effect"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR
cd $APP_DIR

# Clone repository
if [ ! -d ".git" ]; then
    echo "📥 Cloning repository..."
    git clone $REPO_URL .
else
    echo "🔄 Updating repository..."
    git fetch origin
    git reset --hard origin/main
fi

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me || curl -s ipinfo.io/ip || echo "localhost")

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Access your application:"
echo "   Main App:    http://$PUBLIC_IP"
echo "   Grafana:     http://$PUBLIC_IP:3000 (admin/admin123)"
echo "   Prometheus:  http://$PUBLIC_IP:9090"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:   docker-compose logs -f"
echo "   Stop app:    docker-compose down"
echo "   Restart:     docker-compose restart"
echo "   Update:      git pull && docker-compose up -d --build"
echo ""
echo "📊 Check application status:"
echo "   curl http://$PUBLIC_IP/health"
echo ""

# Set up firewall if UFW is available
if command -v ufw &> /dev/null; then
    echo "🛡️  Configuring firewall..."
    sudo ufw allow 22/tcp || true
    sudo ufw allow 80/tcp || true
    sudo ufw allow 443/tcp || true
    sudo ufw allow 3000/tcp || true
    sudo ufw allow 9090/tcp || true
    echo "Firewall rules added (UFW may need to be enabled manually)"
fi

echo "🎉 Setup complete!"
