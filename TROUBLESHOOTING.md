# 🚨 Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. **Containers Not Starting**

#### Check Container Status
```bash
cd /opt/fake-news-detector
docker-compose ps
docker-compose logs
```

#### Common Fixes
```bash
# Stop everything and restart
docker-compose down
docker-compose up -d --build

# If build fails, try individual services
docker-compose up -d prometheus
docker-compose up -d grafana  
docker-compose up -d fake-news-api
```

### 2. **Network/Registry Issues**

If you see "registry-1.docker.io" errors:

```bash
# Check DNS
nslookup registry-1.docker.io

# Restart Docker
sudo systemctl restart docker

# Try with different DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

### 3. **Image Pull Failures**

If GitHub Container Registry pulls fail:

```bash
# Build locally instead
docker-compose build --no-cache
docker-compose up -d
```

### 4. **Port Conflicts**

Check if ports are already in use:
```bash
sudo netstat -tulpn | grep -E ":(80|3000|8000|9090|9100)"
```

### 5. **Permission Issues**

```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
# Log out and back in

# Fix directory permissions
sudo chown -R $USER:$USER /opt/fake-news-detector
```

### 6. **Firewall Issues**

```bash
# Open required ports
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 3000
sudo ufw allow 8000
sudo ufw allow 9090
sudo ufw enable
```

## Manual Deployment Steps

If CI/CD fails, deploy manually:

### Step 1: SSH into Azure VM
```bash
ssh azureuser@YOUR_VM_IP
```

### Step 2: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and back in
exit
ssh azureuser@YOUR_VM_IP
```

### Step 3: Clone Repository
```bash
sudo mkdir -p /opt/fake-news-detector
sudo chown $USER:$USER /opt/fake-news-detector
cd /opt/fake-news-detector
git clone https://github.com/ashish9825/fake-news.git .
```

### Step 4: Start Services
```bash
# Make scripts executable
chmod +x *.sh

# Run startup script
./startup.sh

# Or manually
docker-compose up -d --build
```

### Step 5: Verify Deployment
```bash
# Run debug script
./debug.sh

# Check individual services
curl http://localhost:8000/health
curl http://localhost:9090/-/ready
curl http://localhost:3000/api/health
```

## Service URLs

After successful deployment:

- **Main App**: http://YOUR_VM_IP
- **Main App Direct**: http://YOUR_VM_IP:8000
- **Grafana**: http://YOUR_VM_IP:3000 (admin/admin123)
- **Prometheus**: http://YOUR_VM_IP:9090

## Useful Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f fake-news-api
docker-compose logs -f prometheus
docker-compose logs -f grafana

# Restart specific service
docker-compose restart fake-news-api

# Stop all services
docker-compose down

# Start with fresh build
docker-compose down
docker-compose up -d --build

# Remove everything and start fresh
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## GitHub Actions Secrets Required

Set these in your GitHub repository secrets:

- `AZURE_VM_HOST`: Your Azure VM public IP
- `AZURE_VM_USERNAME`: SSH username (usually "azureuser")
- `AZURE_VM_SSH_KEY`: Your private SSH key content

## Debug Checklist

- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] Repository cloned correctly
- [ ] All required files present
- [ ] Ports not blocked by firewall
- [ ] No port conflicts
- [ ] Internet connectivity working
- [ ] DNS resolution working
- [ ] Sufficient system resources

## Emergency Recovery

If everything fails:

```bash
# Complete cleanup
cd /opt/fake-news-detector
docker-compose down -v
docker system prune -a -f
git reset --hard origin/main

# Fresh start
docker-compose up -d --build
```

## Contact & Support

If you continue having issues:

1. Run `./debug.sh` and save the output
2. Check the logs with `docker-compose logs`
3. Verify all ports are open
4. Ensure VM has sufficient resources (2+ CPU, 4+ GB RAM)

Remember: The application needs time to start up. Wait 2-3 minutes after running `docker-compose up -d` before testing.
