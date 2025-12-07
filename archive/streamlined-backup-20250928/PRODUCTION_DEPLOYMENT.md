# NovaSystem Production Deployment Guide

This guide covers deploying NovaSystem to production using Docker Compose with monitoring, caching, and high availability.

## 🏗️ Architecture Overview

The production deployment includes:

- **NovaSystem API Server**: Core API with FastAPI
- **NovaSystem Web Interface**: Flask-based web UI
- **NovaSystem Gradio Interface**: Interactive Gradio interface
- **Ollama Service**: Local LLM inference engine
- **Redis**: Caching and session management
- **Nginx**: Reverse proxy and load balancer
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization

## 📋 Prerequisites

### System Requirements

- **CPU**: 8+ cores recommended
- **RAM**: 32GB+ recommended (16GB minimum)
- **Storage**: 100GB+ SSD recommended
- **OS**: Linux (Ubuntu 20.04+ recommended)

### Software Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Git
- curl

### Model Requirements

- Ollama installed and running
- At least one model downloaded (e.g., `ollama pull phi3`)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd NovaSystem-Streamlined
```

### 2. Configure Environment

```bash
# Copy and edit production environment file
cp env.prod .env.prod
nano .env.prod
```

**Important**: Update these values in `.env.prod`:
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: Generate a secure secret key
- `GRAFANA_PASSWORD`: Set a secure password
- `ALLOWED_HOSTS`: Add your domain names

### 3. Deploy

```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy to production
./deploy.sh deploy
```

### 4. Verify Deployment

```bash
# Check status
./deploy.sh status

# View logs
./deploy.sh logs
```

## 🔧 Configuration

### Environment Variables

Key configuration options in `env.prod`:

#### API Configuration
```bash
API_HOST=0.0.0.0
API_PORT=8000
MAX_WORKERS=4
REQUEST_TIMEOUT=60
```

#### Model Configuration
```bash
DEFAULT_MODEL=ollama:phi3
MODEL_CACHE_SIZE=5
MAX_MEMORY_MB=16384
CACHE_TTL_HOURS=24
```

#### Performance Configuration
```bash
MAX_CONCURRENT_REQUESTS=10
ENABLE_METRICS=true
ENABLE_CACHING=true
```

#### Security Configuration
```bash
SECRET_KEY=your-secure-secret-key
CORS_ORIGINS=*
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
```

### Docker Compose Configuration

The `docker-compose.prod.yml` file configures:

- **Resource limits**: CPU and memory limits for each service
- **Health checks**: Automatic health monitoring
- **Restart policies**: Automatic restart on failure
- **Volume mounts**: Persistent data storage
- **Network configuration**: Service communication

### Nginx Configuration

The `nginx/nginx.conf` file provides:

- **Reverse proxy**: Routes requests to appropriate services
- **Rate limiting**: Prevents abuse
- **SSL termination**: HTTPS support (configure certificates)
- **Compression**: Gzip compression for better performance
- **Security headers**: Enhanced security

## 📊 Monitoring

### Prometheus Metrics

Access Prometheus at `http://localhost:9090` to view:

- API request metrics
- Model performance metrics
- System resource usage
- Cache hit rates
- Error rates

### Grafana Dashboards

Access Grafana at `http://localhost:3000` (admin/admin by default) to view:

- System overview dashboard
- API performance dashboard
- Model usage dashboard
- Resource utilization dashboard

### Log Management

Logs are stored in `./logs/` directory:

- `novasystem.log`: Application logs
- `nginx/`: Nginx access and error logs
- `docker/`: Container logs

View logs:
```bash
# Application logs
tail -f logs/novasystem.log

# All service logs
./deploy.sh logs

# Specific service logs
docker-compose -f docker-compose.prod.yml logs -f novasystem-api
```

## 🔄 Maintenance

### Updating Deployment

```bash
# Update to latest version
./deploy.sh update
```

### Backup and Restore

```bash
# Manual backup
./deploy.sh backup

# Restore from backup
./deploy.sh restore backup_20240101_120000.tar.gz
```

### Scaling Services

To scale specific services:

```bash
# Scale API servers
docker-compose -f docker-compose.prod.yml up -d --scale novasystem-api=3

# Scale web servers
docker-compose -f docker-compose.prod.yml up -d --scale novasystem-web=2
```

### Health Checks

```bash
# Check service health
curl http://localhost:8000/health
curl http://localhost:5000/health
curl http://localhost:7860/health

# Check all services
./deploy.sh status
```

## 🔒 Security

### SSL/TLS Configuration

1. Obtain SSL certificates
2. Place certificates in `nginx/ssl/`
3. Update `nginx/nginx.conf` to enable SSL
4. Set `SSL_ENABLED=true` in environment

### Firewall Configuration

```bash
# Allow only necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

### Access Control

- Use strong passwords for Grafana
- Restrict API access with rate limiting
- Monitor access logs regularly
- Keep Docker and system updated

## 🚨 Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check logs
./deploy.sh logs

# Check resource usage
docker stats

# Restart services
./deploy.sh restart
```

#### High Memory Usage
```bash
# Check memory usage
docker stats

# Reduce cache size in env.prod
MODEL_CACHE_SIZE=3
MAX_MEMORY_MB=8192

# Restart services
./deploy.sh restart
```

#### Slow Performance
```bash
# Check metrics
curl http://localhost:9090

# Optimize model cache
./deploy.sh cache status

# Check system resources
htop
```

### Performance Tuning

#### For High Load
- Increase `MAX_WORKERS` to 8-16
- Increase `MAX_CONCURRENT_REQUESTS`
- Use multiple API server instances
- Enable Redis clustering

#### For Large Models
- Increase `MAX_MEMORY_MB` to 32GB+
- Use SSD storage for model cache
- Preload frequently used models
- Monitor memory usage closely

## 📈 Scaling

### Horizontal Scaling

1. **Load Balancer**: Use external load balancer (HAProxy, AWS ALB)
2. **Multiple Instances**: Run multiple API servers
3. **Database**: Use external Redis cluster
4. **Storage**: Use shared storage (NFS, EFS)

### Vertical Scaling

1. **CPU**: Increase CPU cores
2. **Memory**: Increase RAM for larger models
3. **Storage**: Use faster SSDs
4. **Network**: Use faster network interfaces

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          ./deploy.sh update
```

### Automated Backups

```bash
# Add to crontab for daily backups
0 2 * * * /path/to/NovaSystem-Streamlined/deploy.sh backup
```

## 📞 Support

For production support:

1. Check logs first: `./deploy.sh logs`
2. Check metrics: `http://localhost:9090`
3. Review this documentation
4. Check GitHub issues
5. Contact support team

## 📝 Changelog

- **v2.0.0**: Initial production deployment configuration
- Added Docker Compose production setup
- Added monitoring with Prometheus/Grafana
- Added Nginx reverse proxy
- Added automated deployment scripts
