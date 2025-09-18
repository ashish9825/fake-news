# 🔍 AI-Powered Fake News Detector

A machine learning-powered web application that detects fake news using an ensemble of classifiers (Logistic Regression, Random Forest, and Naive Bayes). The application provides real-time news analysis using Google News API and includes comprehensive monitoring with Prometheus and Grafana.

## 🚀 Features

- **Real-time Fake News Detection**: Analyze news headlines and articles
- **Live News Feed**: Fetch and analyze latest news from Google News
- **Machine Learning Ensemble**: Uses multiple classifiers for better accuracy
- **Modern Web Interface**: Clean, responsive UI with gradient backgrounds
- **Monitoring & Metrics**: Prometheus metrics and Grafana dashboards
- **Docker Support**: Containerized application with Docker Compose
- **CI/CD Pipeline**: GitHub Actions for automated deployment
- **Azure Ready**: Scripts for Azure VM deployment

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.9
- **ML Libraries**: scikit-learn, pandas
- **News API**: GNews (Google News)
- **Monitoring**: Prometheus, Grafana
- **Web Server**: Nginx (reverse proxy)
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Cloud**: Azure VM

## 📊 Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Nginx    │────│  FastAPI    │────│  ML Model   │
│ (Port 80)   │    │ (Port 8000) │    │ (Ensemble)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                    │                 │
       │            ┌─────────────┐    ┌─────────────┐
       │            │ Prometheus  │    │   GNews     │
       │            │ (Port 9090) │    │    API      │
       │            └─────────────┘    └─────────────┘
       │                    │
┌─────────────┐    ┌─────────────┐
│   Grafana   │────│  Metrics    │
│ (Port 3000) │    │   Storage   │
└─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd fake-news-detector
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
uvicorn fake_news_api:app --reload
```

4. **Access the application**
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Access services**
- Application: http://localhost
- Grafana: http://localhost:3000 (admin/admin123)
- Prometheus: http://localhost:9090

## ☁️ Azure VM Deployment

### Prerequisites

1. **Create Azure VM**
```bash
# Create resource group
az group create --name fake-news-rg --location eastus

# Create VM
az vm create \
  --resource-group fake-news-rg \
  --name fake-news-vm \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B2s
```

2. **Configure Network Security Group**
```bash
# Open ports
az vm open-port --resource-group fake-news-rg --name fake-news-vm --port 80
az vm open-port --resource-group fake-news-rg --name fake-news-vm --port 3000
az vm open-port --resource-group fake-news-rg --name fake-news-vm --port 9090
```

### Deployment

1. **SSH into your Azure VM**
```bash
ssh azureuser@<your-vm-public-ip>
```

2. **Run deployment script**
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/fake-news-detector/main/deploy-azure.sh | bash
```

3. **Access your application**
- Application: http://\<your-vm-public-ip\>
- Grafana: http://\<your-vm-public-ip\>:3000
- Prometheus: http://\<your-vm-public-ip\>:9090

## 🔄 CI/CD Setup

### GitHub Actions Configuration

1. **Set up repository secrets**
   - `AZURE_VM_HOST`: Your Azure VM public IP
   - `AZURE_VM_USERNAME`: SSH username (e.g., azureuser)
   - `AZURE_VM_SSH_KEY`: Private SSH key for VM access

2. **Enable GitHub Container Registry**
   - Go to your repository settings
   - Enable "Packages" in the repository features

3. **Push to main branch**
   - The pipeline will automatically test, build, and deploy

### Pipeline Stages

1. **Test**: Run basic import and functionality tests
2. **Build**: Create and push Docker image to GHCR
3. **Deploy**: Deploy to Azure VM via SSH
4. **Notify**: Send deployment status notification

## 📈 Monitoring & Metrics

### Available Metrics

- `fake_news_predictions_total`: Total predictions made
- `fake_news_fake_predictions_total`: Fake news predictions
- `fake_news_real_predictions_total`: Real news predictions
- `fake_news_api_calls_total`: Total API calls
- `fake_news_uptime_seconds`: Application uptime
- `system_cpu_usage_percent`: CPU usage
- `system_memory_usage_percent`: Memory usage

### Grafana Dashboard

Import the dashboard configuration from `grafana-dashboard.json`:

1. Open Grafana (http://localhost:3000)
2. Login with admin/admin123
3. Go to "+" → Import
4. Upload `grafana-dashboard.json`

## 🛡️ Security Features

- **Non-root container execution**: Application runs as non-root user
- **Health checks**: Docker health checks for service monitoring
- **Firewall configuration**: UFW rules for Azure VM
- **Environment variables**: Sensitive data in environment files
- **SSL ready**: Nginx configuration supports HTTPS

## 🔧 API Endpoints

- `GET /`: Web interface
- `POST /predict`: Analyze text for fake news
- `GET /realtime-news`: Fetch and analyze latest news
- `GET /test-model`: Test model functionality
- `GET /metrics`: Prometheus metrics
- `GET /health`: Health check endpoint
- `GET /docs`: API documentation

## 🧪 Testing

### Manual Testing

1. **Test model prediction**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Scientists discover magical cure using unicorn tears"
```

2. **Check metrics**
```bash
curl http://localhost:8000/metrics
```

3. **Health check**
```bash
curl http://localhost:8000/health
```

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Memory issues**: Reduce model complexity or increase VM size
3. **API limits**: GNews API may have rate limits
4. **Docker permissions**: Add user to docker group

### Logs

```bash
# Application logs
docker-compose logs -f fake-news-api

# All services logs
docker-compose logs -f

# System service logs
sudo journalctl -u fake-news-detector -f
```

## 📝 Environment Variables

Create `.env` file for production:

```env
ENV=production
GRAFANA_ADMIN_PASSWORD=your-secure-password
DEBUG=false
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- scikit-learn for machine learning capabilities
- FastAPI for the modern web framework
- GNews for news data access
- Prometheus & Grafana for monitoring
- Docker for containerization
