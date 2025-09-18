#!/bin/bash

# Debug script for Azure VM deployment
# Run this on your Azure VM to diagnose issues

echo "🔍 Fake News Detector - Debug Information"
echo "========================================"
echo ""

# Check if we're in the right directory
echo "📍 Current Directory:"
pwd
echo ""

# Check if Docker is installed and running
echo "🐳 Docker Status:"
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed: $(docker --version)"
    if docker info &> /dev/null; then
        echo "✅ Docker daemon is running"
    else
        echo "❌ Docker daemon is not running"
        echo "Try: sudo systemctl start docker"
    fi
else
    echo "❌ Docker is not installed"
fi
echo ""

# Check if Docker Compose is installed
echo "🐙 Docker Compose Status:"
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose is installed: $(docker-compose --version)"
else
    echo "❌ Docker Compose is not installed"
fi
echo ""

# Check if repository exists
echo "📁 Repository Status:"
if [ -d ".git" ]; then
    echo "✅ Git repository found"
    echo "Current branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --oneline)"
else
    echo "❌ No git repository found"
fi
echo ""

# Check if required files exist
echo "📄 Required Files:"
files=("docker-compose.yml" "Dockerfile" "fake_news_api.py" "requirements.txt" "prometheus.yml" "nginx.conf")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done
echo ""

# Check Docker containers
echo "📦 Docker Containers:"
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "Running containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "All containers (including stopped):"
    docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
else
    echo "Cannot check containers - Docker not available"
fi
echo ""

# Check Docker images
echo "🖼️  Docker Images:"
if command -v docker &> /dev/null && docker info &> /dev/null; then
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"
else
    echo "Cannot check images - Docker not available"
fi
echo ""

# Check Docker Compose services
echo "🔧 Docker Compose Services:"
if [ -f "docker-compose.yml" ] && command -v docker-compose &> /dev/null; then
    docker-compose ps
    echo ""
    echo "Docker Compose logs (last 50 lines):"
    docker-compose logs --tail=50
else
    echo "Cannot check compose services - docker-compose.yml missing or docker-compose not installed"
fi
echo ""

# Check network connectivity
echo "🌐 Network Tests:"
if command -v curl &> /dev/null; then
    echo "Testing local services..."
    
    # Test main app
    if curl -s -f http://localhost:8000/health > /dev/null; then
        echo "✅ Main app (port 8000) is responding"
    else
        echo "❌ Main app (port 8000) not responding"
    fi
    
    # Test Prometheus
    if curl -s -f http://localhost:9090/-/ready > /dev/null; then
        echo "✅ Prometheus (port 9090) is ready"
    else
        echo "❌ Prometheus (port 9090) not ready"
    fi
    
    # Test Grafana
    if curl -s -f http://localhost:3000/api/health > /dev/null; then
        echo "✅ Grafana (port 3000) is responding"
    else
        echo "❌ Grafana (port 3000) not responding"
    fi
    
    # Test Nginx
    if curl -s -f http://localhost > /dev/null; then
        echo "✅ Nginx (port 80) is responding"
    else
        echo "❌ Nginx (port 80) not responding"
    fi
else
    echo "curl not available for testing"
fi
echo ""

# Check system resources
echo "💻 System Resources:"
echo "CPU usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory usage: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
echo "Disk usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"
echo ""

# Check firewall status
echo "🛡️  Firewall Status:"
if command -v ufw &> /dev/null; then
    echo "UFW status: $(sudo ufw status | head -1)"
    echo "Required ports:"
    sudo ufw status | grep -E "(22|80|443|3000|8000|9090|9100)" || echo "No rules found for required ports"
else
    echo "UFW not available"
fi
echo ""

# Provide suggestions
echo "🔧 Troubleshooting Suggestions:"
echo "1. If Docker is not running: sudo systemctl start docker"
echo "2. If containers are not running: docker-compose up -d"
echo "3. If services are failing: docker-compose logs [service-name]"
echo "4. If ports are blocked: sudo ufw allow [port]"
echo "5. To restart everything: docker-compose down && docker-compose up -d"
echo "6. To rebuild: docker-compose down && docker-compose up -d --build"
echo ""

echo "📊 Quick Commands:"
echo "View logs: docker-compose logs -f"
echo "Check status: docker-compose ps"
echo "Restart: docker-compose restart"
echo "Stop all: docker-compose down"
echo "Start all: docker-compose up -d"
echo ""

# Get public IP
if command -v curl &> /dev/null; then
    PUBLIC_IP=$(curl -s ifconfig.me || curl -s ipinfo.io/ip || echo "unable to determine")
    echo "🌍 Public IP: $PUBLIC_IP"
    echo "Access URLs:"
    echo "  Main App: http://$PUBLIC_IP"
    echo "  Grafana: http://$PUBLIC_IP:3000"
    echo "  Prometheus: http://$PUBLIC_IP:9090"
fi

echo ""
echo "Debug completed! ✨"
