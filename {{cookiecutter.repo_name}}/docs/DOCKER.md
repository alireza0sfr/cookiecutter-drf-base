# Docker & Docker Compose Guide

Complete guide to containerizing and orchestrating the Aghamohandes Backend using Docker.

## Overview

The project uses Docker for consistent development, staging, and production environments:

- **Multi-stage builds**: Separate images for development, staging, and production
- **Docker Compose**: Orchestrate services locally (dev, staging, prod configs)
- **Minimal images**: Production images optimized for size and security
- **Non-root user**: Security hardening with dedicated app user

## Quick Start

### Development Environment

```bash
# Start all services (PostgreSQL, Redis, Django, Celery, etc.)
docker-compose -f deployment/docker/docker-compose.yml up

# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web pytest

# Stop services
docker-compose down
```

Access the application at `http://localhost:8000`

### Staging Environment

```bash
# Start staging services
docker-compose -f deployment/docker/docker-compose.staging.yml up -d

# View logs
docker-compose -f docker-compose.staging.yml logs -f

# Stop staging services
docker-compose -f docker-compose.staging.yml down
```

Access at `http://localhost:80` or `https://localhost:443`

### Production Environment

```bash
# Start production services
docker-compose -f deployment/docker/docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Verify health
curl https://api.example.com/health/
```

## Directory Structure

```
deployment/docker/
├── Dockerfile                  # Multi-stage build (dev/staging/prod)
├── .dockerignore              # Files to exclude from image
├── docker-compose.yml         # Development (default)
├── docker-compose.staging.yml # Staging environment
├── docker-compose.prod.yml    # Production environment
└── nginx/
    ├── nginx-staging.conf     # Staging reverse proxy config
    └── nginx-prod.conf        # Production reverse proxy config
```

## Dockerfile Stages

### Stage 1: Builder
- Installs dependencies
- Builds Python packages
- ~500MB intermediate image (discarded)

### Stage 2: Development
- Full dev environment
- Django dev server
- Debugging tools (git, curl, psql)
- Volume mounts for live code reload
- ~1.2GB final image

### Stage 3-4: Production Base
- Minimal runtime dependencies
- Non-root user (appuser, UID 1000)
- Security hardening (read-only root, no privileges)
- ~400MB base image

### Stage 5: Staging
- Based on production-base
- Debug mode enabled
- Smaller worker pool (2 workers)
- ~410MB final image

### Stage 6: Production
- Based on production-base
- Debug disabled
- Optimized workers (4 workers)
- Health checks enabled
- ~410MB final image

## Build & Push

### Local Build

```bash
# Build for development
docker build -f deployment/docker/Dockerfile --target development -t aghamohandes:dev .

# Build for staging
docker build -f deployment/docker/Dockerfile --target staging -t aghamohandes:staging .

# Build for production
docker build -f deployment/docker/Dockerfile --target production -t aghamohandes:latest .

# Or use docker-compose (auto builds)
docker-compose build
```

### Push to Registry

```bash
# Tag image
docker tag aghamohandes:latest myregistry.azurecr.io/aghamohandes:1.0.0

# Push to Azure Container Registry
docker push myregistry.azurecr.io/aghamohandes:1.0.0

# Push to Docker Hub
docker tag aghamohandes:latest myusername/aghamohandes:1.0.0
docker push myusername/aghamohandes:1.0.0

# Push to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag aghamohandes:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/aghamohandes:1.0.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/aghamohandes:1.0.0
```

## Environment Configuration

### Development (.env)

```bash
DEBUG=true
ENVIRONMENT=development
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aghamohandes
REDIS_HOST=localhost
REDIS_PORT=6379
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Staging (.env.staging)

```bash
DEBUG=true
ENVIRONMENT=staging
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql://user:pass@db:5432/aghamohandes
REDIS_HOST=redis
REDIS_PORT=6379
ALLOWED_HOSTS=staging.example.com
CORS_ALLOWED_ORIGINS=https://staging-frontend.example.com
```

### Production (.env.prod)

```bash
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=<very-strong-random-key>
DATABASE_URL=postgresql://user:securepass@db:5432/aghamohandes
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=<strong-password>
ALLOWED_HOSTS=api.example.com,www.example.com
CORS_ALLOWED_ORIGINS=https://frontend.example.com
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=<app-password>
```

## Services

### PostgreSQL (Database)

```bash
# Connect to database
docker-compose exec db psql -U postgres -d aghamohandes

# Backup database
docker-compose exec db pg_dump -U postgres aghamohandes > backup.sql

# Restore database
docker-compose exec db psql -U postgres aghamohandes < backup.sql

# Check database size
docker-compose exec db psql -U postgres -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) FROM pg_database;"
```

### Redis (Cache & Message Broker)

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check memory usage
docker-compose exec redis redis-cli INFO memory

# Monitor Redis commands
docker-compose exec redis redis-cli MONITOR

# Clear all data
docker-compose exec redis redis-cli FLUSHALL
```

### Django Web Server

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Run tests
docker-compose exec web pytest
```

### Celery Worker & Beat

```bash
# View Celery logs
docker-compose logs -f celery celery-beat

# Inspect active tasks
docker-compose exec celery celery -A aghamohandes_backend inspect active

# Purge all tasks
docker-compose exec celery celery -A aghamohandes_backend purge

# Check worker statistics
docker-compose exec celery celery -A aghamohandes_backend inspect stats
```

## Health Checks

### Development
- Web: `http://localhost:8000/health/`
- Redis: Auto-configured in docker-compose
- PostgreSQL: Auto-configured in docker-compose

### Staging
- Web: `http://localhost:8001/health/`
- Nginx: `http://localhost/health/`
- All services have health checks defined

### Production
- Web: `https://api.example.com/health/`
- Nginx: Auto-configured
- Kubernetes: Health checks in deployment manifest

## Nginx Configuration

### Staging
- HTTP → HTTPS redirect
- Self-signed SSL (or Let's Encrypt)
- Compression enabled
- Cache headers for static files
- Security headers

### Production
- HTTP → HTTPS redirect (Let's Encrypt)
- Rate limiting per endpoint
- CORS configuration
- Gzip compression
- OCSP stapling
- Static file caching (365 days)
- API caching (7 days)

## Common Tasks

### Restart Services

```bash
# Restart web server
docker-compose restart web

# Restart all services
docker-compose restart

# Soft restart (SIGHUP)
docker-compose kill -s SIGHUP web
```

### View Logs

```bash
# Follow web logs
docker-compose logs -f web

# View last 100 lines
docker-compose logs --tail=100 web

# Filter by service
docker-compose logs celery

# Combine services
docker-compose logs -f web celery redis
```

### Database Management

```bash
# Create database backup
docker-compose exec db pg_dump -U postgres aghamohandes > backup-$(date +%Y%m%d).sql

# Create media backup
docker-compose exec web tar -czf /app/media-backup.tar.gz /app/media/

# Copy file from container
docker cp aghamohandes-web-dev:/app/media/file.pdf .

# Copy file to container
docker cp local-file.pdf aghamohandes-web-dev:/app/media/
```

### Performance Monitoring

```bash
# CPU and memory usage
docker stats

# Container details
docker-compose ps

# Image disk usage
docker images --digests

# Disk usage by layers
docker history aghamohandes:latest

# Inspect container
docker inspect aghamohandes-web-dev
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Inspect container
docker-compose inspect web

# Rebuild image
docker-compose build --no-cache web

# Start with verbose output
docker-compose up --verbose web
```

### Database Connection Failed

```bash
# Check database service
docker-compose ps db

# Test database connection
docker-compose exec web psql $DATABASE_URL -c "SELECT 1"

# Check environment variables
docker-compose exec web env | grep DATABASE
```

### Out of Disk Space

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove containers
docker container prune
```

### Performance Issues

```bash
# Check resource limits
docker stats --no-stream

# Increase limits (edit docker-compose.yml)
# resources:
#   limits:
#     cpus: '2'
#     memory: 2G

# Enable Docker BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build .
```

## Production Deployment

### Using Docker Compose

```bash
# Pull latest code
git pull origin main

# Build new image
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f deployment/docker/docker-compose.prod.yml up -d

# Verify services are running
docker-compose -f deployment/docker/docker-compose.prod.yml ps

# Monitor logs
docker-compose -f deployment/docker/docker-compose.prod.yml logs -f
```

### Blue-Green Deployment

```bash
# 1. Start new version (green)
docker-compose -f deployment/docker/docker-compose.prod.yml -f deployment/docker/docker-compose.green.yml up -d

# 2. Verify green version
curl https://api-green.example.com/health/

# 3. Switch Nginx to green
docker-compose exec nginx nginx -s reload

# 4. Keep blue running for rollback
# 5. After verification, shut down blue
docker-compose -f deployment/docker/docker-compose.prod.yml down
```

## Security Best Practices

✅ DO:
- Use official base images (python:3.11-slim)
- Run as non-root user (appuser:1000)
- Minimize image layers
- Use multi-stage builds
- Set resource limits
- Use .dockerignore to exclude files
- Scan images for vulnerabilities
- Keep dependencies updated

❌ DON'T:
- Commit secrets to git
- Run as root
- Use `latest` tag in production
- Disable security contexts
- Use insecure registries
- Include build tools in production
- Mount sensitive host directories
- Trust untrusted images

## Resource Limits

### Development
- Memory: Unlimited (developer machines)
- CPU: Unlimited

### Staging
- Web: 512Mi request, 1Gi limit
- Celery: 256Mi request, 512Mi limit
- Database: 1Gi request, 2Gi limit

### Production
- Web: 512Mi request, 1Gi limit
- Celery: 256Mi request, 512Mi limit
- Database: 2Gi request, 4Gi limit
- Redis: 512Mi request, 1Gi limit

---

See also:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [KUBERNETES.md](KUBERNETES.md) - Kubernetes orchestration
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
