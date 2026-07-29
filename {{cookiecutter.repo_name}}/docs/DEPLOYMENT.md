# Deployment Guide

Production deployment for {{ cookiecutter.project_name }}.

## Pre-Deployment Checklist

- [ ] All tests passing with 80%+ coverage
- [ ] No uncommitted changes
- [ ] Environment variables configured
- [ ] Database migrations created and tested
- [ ] Static files collected
- [ ] Security checklist completed

## Environments

### Development
- Local development with Django dev server
- Debug mode enabled
- Live reload of code changes

### Staging
- Production-like environment for testing
- Debug mode may be enabled
- Full HTTPS with self-signed cert

### Production
- Full production deployment
- Debug mode disabled
- All security features enabled
- Regular backups configured

## Docker Deployment

### Build Image

```bash
# Development
docker build -f deployment/docker/Dockerfile --target development \
  -t {{ cookiecutter.repo_name }}:dev .

# Staging
docker build -f deployment/docker/Dockerfile --target staging \
  -t {{ cookiecutter.repo_name }}:staging .

# Production
docker build -f deployment/docker/Dockerfile --target production \
  -t {{ cookiecutter.repo_name }}:1.0.0 .
```

### Run with Docker Compose

```bash
# Development
docker-compose -f deployment/docker/docker-compose.yml up

# Staging
docker-compose -f deployment/docker/docker-compose.staging.yml up -d

# Production
docker-compose -f deployment/docker/docker-compose.prod.yml up -d
```

## Environment Configuration

### Production Environment

Create `.env.prod`:

```bash
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=your-strong-random-secret-key
ALLOWED_HOSTS=api.example.com,www.example.com

DATABASE_NAME=prod_db_name
DATABASE_USER=prod_user
DATABASE_PASSWORD=prod_strong_password
DATABASE_HOST=db.example.com
DATABASE_PORT=5432

REDIS_HOST=cache.example.com
REDIS_PORT=6379

SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Database Migrations

Always test migrations locally first:

```bash
# Create migrations
python manage.py makemigrations

# Test migration
python manage.py migrate --plan
python manage.py migrate

# In production
docker-compose exec web python manage.py migrate --noinput
```

## Static Files

Collect static files before deployment:

```bash
python manage.py collectstatic --noinput
```

## Security Checklist

- [ ] `SECRET_KEY` is strong and unique
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` is configured
- [ ] HTTPS/SSL is enabled
- [ ] HSTS headers are set
- [ ] CSRF protection is enabled
- [ ] CORS is properly configured
- [ ] Database password is strong
- [ ] No secrets in `.env` (use secrets management)
- [ ] Admin user password is changed
- [ ] Dependencies are up to date

## Backup & Recovery

### Database Backup

```bash
# Backup
pg_dump -h host -U user -d database > backup.sql

# Restore
psql -h host -U user -d database < backup.sql
```

### Media Files Backup

```bash
# Backup
tar -czf media-backup.tar.gz media/

# Restore
tar -xzf media-backup.tar.gz
```

## Monitoring

Monitor production services:

- Health checks: `/health/`
- Error logs: Application logs
- Performance: Response times, errors
- Database: Connection pool, slow queries

## Rollback Procedures

### Docker

```bash
# If deployment fails, use previous image version
docker-compose -f deployment/docker/docker-compose.prod.yml down
docker tag {{ cookiecutter.repo_name }}:1.0.0-previous {{ cookiecutter.repo_name }}:latest
docker-compose -f deployment/docker/docker-compose.prod.yml up -d
```

### Database

Keep backups of all migrations. If needed:

```bash
# Reverse last migration
python manage.py migrate app_name 0001_previous

# Manually edit database if needed
psql -U user -d database
```

## Performance Optimization

### Caching

- Cache expensive queries with Redis
- Use cache decorators on views
- Set appropriate TTLs

### Database Optimization

- Add indexes on frequently queried columns
- Use `select_related()` and `prefetch_related()`
- Monitor slow queries

### Compression

- Gzip responses (enabled in Nginx)
- Minimize CSS/JS assets
- Optimize images

## Maintenance

### Regular Tasks

- Monitor disk space
- Update dependencies
- Review error logs
- Backup databases
- Test recovery procedures

---

**Last Updated**: 2026-07-29
