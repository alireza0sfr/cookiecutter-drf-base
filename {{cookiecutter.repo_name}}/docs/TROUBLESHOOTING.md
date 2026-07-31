# Troubleshooting Guide

## Common Issues & Solutions

### Database Errors

#### "FATAL: Ident authentication failed"

**Problem**: PostgreSQL connection rejected

**Solution**:
```bash
# Check PostgreSQL is running
brew services list | grep postgres

# Start PostgreSQL if not running
brew services start postgresql@14

# Verify connection string in .env
DATABASE_URL=postgresql://user:password@localhost:5432/aghamohandes

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

#### "relation does not exist" when running migrations

**Problem**: Migration file exists but table not created

**Solution**:
```bash
# Check migration status
python manage.py showmigrations

# Run pending migrations
python manage.py migrate

# If migration is stuck
python manage.py migrate [app] [migration_number]

# Fake migration if already applied manually
python manage.py migrate [app] [migration] --fake
```

### Redis Connection Issues

#### "ConnectionRefusedError: Error 61 connecting to localhost:6379"

**Problem**: Redis not running or misconfigured

**Solution**:
```bash
# Check Redis is running
brew services list | grep redis

# Start Redis
brew services start redis

# Verify Redis connection
redis-cli ping  # Should respond with PONG

# Check Redis host/port in .env
REDIS_HOST=localhost
REDIS_PORT=6379

# Test connection
python -c "import redis; r = redis.Redis(); print(r.ping())"
```

### Test Failures

#### "ModuleNotFoundError: No module named 'apps'"

**Problem**: Virtual environment not activated or packages not installed

**Solution**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Sync dependencies
uv sync --all-groups

# Verify pytest can find modules
pytest --collect-only apps/
```

#### "django.core.exceptions.ImproperlyConfigured: Requested setting DEBUG with app registry not ready"

**Problem**: Test trying to use Django before initialization

**Solution**:
```python
# Add @pytest.mark.django_db to test methods
import pytest

@pytest.mark.django_db
def test_model_creation():
    user = UserFactory()
    assert user.id is not None
```

### Code Quality Issues

#### Ruff linting fails with "E501 line too long"

**Problem**: Line exceeds 100 character limit

**Solution**:
```bash
# Auto-fix formatting issues
ruff format .

# Check which lines are too long
ruff check . --select=E501

# Manually break long lines
# Before:
result = very_long_function_name(argument1, argument2, argument3, argument4)

# After:
result = very_long_function_name(
    argument1, argument2, argument3, argument4
)
```

#### Pre-commit hook fails

**Problem**: Code doesn't pass pre-commit checks before commit

**Solution**:
```bash
# Fix all issues automatically
ruff format .
ruff check . --fix

# Run validation script
./scripts/validate.sh

# If all checks pass, commit
git add .
git commit -m "message"
```

### API Issues

#### "HTTP 401 Unauthorized" on authenticated endpoints

**Problem**: Missing or invalid authentication token

**Solution**:
```bash
# 1. Obtain JWT token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password"}'

# 2. Use token in requests
curl http://localhost:8000/api/v1/articles/ \
  -H "Authorization: Bearer <access_token>"

# 3. Check token expiration (2 weeks)
# If expired, refresh with refresh token
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

#### "HTTP 429 Too Many Requests"

**Problem**: Rate limit exceeded

**Solution**:
```bash
# Check current rate limit
curl -i http://localhost:8000/api/v1/articles/ | grep X-RateLimit

# Wait for reset time (shown in headers)
# Or whitelist IP in settings.py
IP_WHITELIST = ['127.0.0.1', 'your-ip']

# For development, disable rate limiting
# Set throttle_classes = [] in views.py
```

#### "HTTP 500 Internal Server Error"

**Problem**: Server-side error occurred

**Solution**:
```bash
# Check server logs
tail -f logs/aghamohandes_backend-*.log

# Check Django check command
python manage.py check

# Test database connection
python manage.py dbshell

# Clear cache (might help)
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Run in debug mode (development only)
DEBUG=true python manage.py runserver
```

### Performance Issues

#### Slow API responses

**Problem**: List endpoints taking too long

**Solution**:
```python
# Use select_related for ForeignKey
articles = Article.objects.select_related('author').all()

# Use prefetch_related for ManyToMany
articles = Article.objects.prefetch_related('comments').all()

# Add db_index to frequently filtered fields
class Article(models.Model):
    is_published = models.BooleanField(db_index=True)

# Cache expensive queries
@cache_page(60 * 5)  # 5 minutes
def list(self, request):
    return super().list(request, *args, **kwargs)
```

#### High memory usage

**Problem**: Memory leaks or large query results

**Solution**:
```python
# Use values() or values_list() instead of model instances
Article.objects.all().values_list('id', 'title')  # Not Article objects

# Use iterator() for large querysets
for article in Article.objects.all().iterator(chunk_size=1000):
    process_article(article)

# Monitor task queue
celery -A aghamohandes_backend inspect active
celery -A aghamohandes_backend purge  # Clear all tasks
```

### Deployment Issues

#### "Permission denied" deploying static files

**Problem**: collectstatic can't write to static directory

**Solution**:
```bash
# Fix permissions
chmod -R 755 /var/www/aghamohandes/static/

# Or run as correct user
sudo -u www-data python manage.py collectstatic --noinput

# Verify directory is writable
touch /var/www/aghamohandes/static/test.txt
rm /var/www/aghamohandes/static/test.txt
```

#### "Connection refused" to database in production

**Problem**: Database unreachable from production server

**Solution**:
```bash
# Check database is running and accessible
psql postgresql://user:pass@db.example.com:5432/aghamohandes -c "SELECT 1"

# Check firewall rules
telnet db.example.com 5432

# Check connection string in .env
echo $DATABASE_URL

# Restart web service
systemctl restart aghamohandes
```

---

For more help, check:
- [CLAUDE.md](../CLAUDE.md) - Coding standards
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- Graphify knowledge graph: `graphify query "issue here"`
