# Deployment Guide

## Environments

- **Development**: Local machine with Django dev server
- **Staging**: Pre-production clone of production
- **Production**: Live environment serving end users

## Prerequisites

- Docker & Docker Compose (recommended)
- PostgreSQL 14+
- Redis
- Python 3.11+
- Gunicorn (production WSGI server)

## Environment Configuration

### .env File

```bash
# Django
DEBUG=false
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=api.example.com,www.example.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aghamohandes

# Cache
REDIS_HOST=localhost
REDIS_PORT=6379

# Email
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=true

# Security
SITE_URL=https://api.example.com
CORS_ALLOWED_ORIGINS=https://frontend.example.com

# APM (Optional)
APM_SERVER_URL=https://apm.example.com
APM_SERVER_TOKEN=your-apm-token
```

## Deployment Steps

### 1. Prepare Code

```bash
# Pull latest code
git pull origin main

# Check for pending migrations
python manage.py makemigrations --check

# Run validation
./scripts/validate.sh
```

### 2. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (development only)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 3. Start Services

#### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: aghamohandes
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn aghamohandes_backend.wsgi:application --bind 0.0.0.0:8000
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/aghamohandes
      - REDIS_HOST=redis
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A aghamohandes_backend worker -l info
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/aghamohandes
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web
```

#### Manual Setup

```bash
# Run Gunicorn (production WSGI server)
gunicorn aghamohandes_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 30

# Run Celery worker
celery -A aghamohandes_backend worker -l info

# Run Celery beat (scheduler)
celery -A aghamohandes_backend beat -l info
```

### 4. Configure Reverse Proxy (Nginx)

```nginx
upstream django {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/aghamohandes/static/;
    }

    location /media/ {
        alias /var/www/aghamohandes/media/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

## Health Checks

### Health Endpoint

```bash
# Add to aghamohandes_backend/urls.py
path('health/', lambda request: JsonResponse({'status': 'ok'}))
```

### Monitoring

```bash
# Check service status
curl https://api.example.com/health/

# Monitor logs
tail -f /var/log/aghamohandes.log

# Check database
python manage.py dbshell

# Monitor task queue
celery -A aghamohandes_backend inspect active
```

## Backup & Recovery

### Database Backup

```bash
# Backup PostgreSQL
pg_dump -h localhost -U postgres aghamohandes > backup.sql

# Restore from backup
psql -h localhost -U postgres aghamohandes < backup.sql

# Automated backups (daily at 2 AM)
0 2 * * * pg_dump -h localhost -U postgres aghamohandes > /backups/aghamohandes-$(date +\%Y-\%m-\%d).sql
```

### Media Files Backup

```bash
# Backup media directory
tar -czf media-backup.tar.gz media/

# Restore media
tar -xzf media-backup.tar.gz
```

## Scaling

### Horizontal Scaling

```bash
# Multiple Gunicorn workers
gunicorn aghamohandes_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4                    # CPU cores * 2 + 1
    --worker-class uvicorn.workers.UvicornWorker

# Multiple Celery workers
celery -A aghamohandes_backend worker --concurrency=4
```

### Load Balancing

Use Nginx upstream or cloud load balancer:

```nginx
upstream django_cluster {
    server web1.example.com:8000;
    server web2.example.com:8000;
    server web3.example.com:8000;
}

server {
    location / {
        proxy_pass http://django_cluster;
    }
}
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: pytest --cov=apps --cov-fail-under=80

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: ssh deploy@example.com 'cd /app && git pull && ./deploy.sh'
```

## Zero-Downtime Deployment

### Blue-Green Deployment

```bash
# 1. Deploy to "green" environment (new version)
git checkout main
git pull
python manage.py migrate
python manage.py collectstatic --noinput
# Start green environment on separate port

# 2. Test green environment
curl http://localhost:8001/health/

# 3. Switch traffic to green
# Update load balancer to point to green environment

# 4. Keep blue running for quick rollback
# If issues detected, switch back to blue

# 5. After verification, shut down blue
```

---

For production security checklist, see [SECURITY.md](guides/security.md).
