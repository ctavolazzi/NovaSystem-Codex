#!/bin/bash

# NovaSystem Production Deployment Script
# This script deploys NovaSystem to production using Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE="env.prod"
BACKUP_DIR="./backups"
LOG_DIR="./logs"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file $ENV_FILE not found. Please create it from env.template."
        exit 1
    fi

    log_success "Prerequisites check passed"
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."

    mkdir -p "$BACKUP_DIR"
    mkdir -p "$LOG_DIR"
    mkdir -p "./data"
    mkdir -p "./cache"
    mkdir -p "./nginx/ssl"
    mkdir -p "./monitoring/grafana/dashboards"
    mkdir -p "./monitoring/grafana/datasources"

    log_success "Directories created"
}

# Backup existing data
backup_data() {
    if [ -d "./data" ] && [ "$(ls -A ./data)" ]; then
        log_info "Backing up existing data..."

        BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
        tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" ./data

        log_success "Data backed up to $BACKUP_DIR/$BACKUP_NAME.tar.gz"
    fi
}

# Pull latest images
pull_images() {
    log_info "Pulling latest Docker images..."

    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull

    log_success "Images pulled successfully"
}

# Build custom images
build_images() {
    log_info "Building custom images..."

    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --no-cache

    log_success "Images built successfully"
}

# Deploy services
deploy_services() {
    log_info "Deploying services..."

    # Stop existing services
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down

    # Start services
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d

    log_success "Services deployed successfully"
}

# Wait for services to be healthy
wait_for_health() {
    log_info "Waiting for services to be healthy..."

    # Wait for API service
    log_info "Waiting for API service..."
    timeout 300 bash -c 'until curl -f http://localhost:8000/health; do sleep 5; done'

    # Wait for Web service
    log_info "Waiting for Web service..."
    timeout 300 bash -c 'until curl -f http://localhost:5000/health; do sleep 5; done'

    # Wait for Gradio service
    log_info "Waiting for Gradio service..."
    timeout 300 bash -c 'until curl -f http://localhost:7860/health; do sleep 5; done'

    log_success "All services are healthy"
}

# Show deployment status
show_status() {
    log_info "Deployment Status:"
    echo ""

    # Show running containers
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps

    echo ""
    log_info "Service URLs:"
    echo "  API Server:     http://localhost:8000"
    echo "  Web Interface:  http://localhost:5000"
    echo "  Gradio Interface: http://localhost:7860"
    echo "  Prometheus:     http://localhost:9090"
    echo "  Grafana:        http://localhost:3000"
    echo ""

    log_info "Useful commands:"
    echo "  View logs:      docker-compose -f $COMPOSE_FILE logs -f"
    echo "  Stop services:  docker-compose -f $COMPOSE_FILE down"
    echo "  Restart:        docker-compose -f $COMPOSE_FILE restart"
    echo "  Update:         ./deploy.sh --update"
}

# Update deployment
update_deployment() {
    log_info "Updating deployment..."

    # Pull latest images
    pull_images

    # Rebuild custom images
    build_images

    # Restart services
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d --force-recreate

    # Wait for health
    wait_for_health

    log_success "Deployment updated successfully"
}

# Cleanup old resources
cleanup() {
    log_info "Cleaning up old resources..."

    # Remove unused images
    docker image prune -f

    # Remove unused volumes
    docker volume prune -f

    # Remove old backups (keep last 7 days)
    find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

    log_success "Cleanup completed"
}

# Main deployment function
main() {
    log_info "Starting NovaSystem production deployment..."

    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            create_directories
            backup_data
            pull_images
            build_images
            deploy_services
            wait_for_health
            show_status
            ;;
        "update")
            check_prerequisites
            update_deployment
            show_status
            ;;
        "stop")
            log_info "Stopping services..."
            docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down
            log_success "Services stopped"
            ;;
        "restart")
            log_info "Restarting services..."
            docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" restart
            wait_for_health
            show_status
            ;;
        "logs")
            docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" logs -f
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        *)
            echo "Usage: $0 {deploy|update|stop|restart|logs|status|cleanup}"
            echo ""
            echo "Commands:"
            echo "  deploy   - Deploy NovaSystem to production"
            echo "  update   - Update existing deployment"
            echo "  stop     - Stop all services"
            echo "  restart  - Restart all services"
            echo "  logs     - View service logs"
            echo "  status   - Show deployment status"
            echo "  cleanup  - Clean up old resources"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
