#!/bin/bash

# Azure VM Deployment Script for Fake News Detector
# Run this script on your Azure VM to set up the environment

set -e

echo "🚀 Starting Azure VM deployment setup..."

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create application directory
sudo mkdir -p /opt/fake-news-detector
sudo chown $USER:$USER /opt/fake-news-detector
cd /opt/fake-news-detector

# Clone repository (replace with your actual repository)
if [ ! -d ".git" ]; then
    git clone https://github.com/YOUR_USERNAME/fake-news-detector.git .
fi

# Create environment file
cat > .env << EOF
ENV=production
GRAFANA_ADMIN_PASSWORD=admin123
EOF

# Set up firewall rules
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw allow 3000    # Grafana
sudo ufw allow 9090    # Prometheus
sudo ufw --force enable

# Create systemd service for auto-start
sudo tee /etc/systemd/system/fake-news-detector.service > /dev/null <<EOF
[Unit]
Description=Fake News Detector Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/fake-news-detector
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable fake-news-detector.service

# Start the application
docker-compose up -d

echo "✅ Deployment complete!"
echo "📊 Application: http://$(curl -s ifconfig.me)"
echo "📈 Grafana: http://$(curl -s ifconfig.me):3000 (admin/admin123)"
echo "🔍 Prometheus: http://$(curl -s ifconfig.me):9090"
echo ""
echo "🔧 To manage the application:"
echo "  Start:   sudo systemctl start fake-news-detector"
echo "  Stop:    sudo systemctl stop fake-news-detector" 
echo "  Status:  sudo systemctl status fake-news-detector"
echo "  Logs:    docker-compose logs -f"
