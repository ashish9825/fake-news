#!/bin/bash

# Manual startup script for testing
# Run this script in the application directory to start services

set -e

echo "🚀 Starting Fake News Detector manually..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found. Please run this script from the application directory."
    exit 1
fi

echo "📍 Current directory: $(pwd)"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Remove old containers and volumes if they exist
echo "🧹 Cleaning up old containers..."
docker-compose rm -f || true

# Pull/build images
echo "🏗️  Building/pulling images..."
docker-compose build --no-cache

# Start services one by one for better debugging
echo "🚀 Starting Prometheus..."
docker-compose up -d prometheus
sleep 10

echo "🚀 Starting Grafana..."
docker-compose up -d grafana
sleep 10

echo "🚀 Starting Node Exporter..."
docker-compose up -d node-exporter
sleep 5

echo "🚀 Starting main application..."
docker-compose up -d fake-news-api
sleep 15

echo "🚀 Starting Nginx..."
docker-compose up -d nginx
sleep 5

# Wait for all services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check status
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "🔍 Testing services..."

# Test each service
if curl -s -f http://localhost:8000/health > /dev/null; then
    echo "✅ Main app is healthy"
else
    echo "❌ Main app health check failed"
    echo "Logs:"
    docker-compose logs --tail=20 fake-news-api
fi

if curl -s -f http://localhost:9090/-/ready > /dev/null; then
    echo "✅ Prometheus is ready"
else
    echo "❌ Prometheus not ready"
    echo "Logs:"
    docker-compose logs --tail=20 prometheus
fi

if curl -s -f http://localhost:3000/api/health > /dev/null; then
    echo "✅ Grafana is healthy"
else
    echo "❌ Grafana not ready"
    echo "Logs:"
    docker-compose logs --tail=20 grafana
fi

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me || curl -s ipinfo.io/ip || echo "localhost")

echo ""
echo "🎉 Startup completed!"
echo ""
echo "🌐 Access your services:"
echo "  Main App:    http://$PUBLIC_IP"
echo "  Main App:    http://$PUBLIC_IP:8000"
echo "  Grafana:     http://$PUBLIC_IP:3000 (admin/admin123)"
echo "  Prometheus:  http://$PUBLIC_IP:9090"
echo ""
echo "🔧 Useful commands:"
echo "  View all logs:        docker-compose logs -f"
echo "  View specific logs:   docker-compose logs -f [service-name]"
echo "  Check status:         docker-compose ps"
echo "  Stop all:            docker-compose down"
echo "  Restart service:     docker-compose restart [service-name]"
echo ""
echo "📊 Debug script:       bash debug.sh"
