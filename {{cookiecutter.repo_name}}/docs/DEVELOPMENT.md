# Development Setup

Setup and development commands for {{ cookiecutter.project_name }}.

## Prerequisites

- Python 3.11 or later
- PostgreSQL 12+
- Redis 6+
- `uv` package manager ([install uv](https://docs.astral.sh/uv/getting-started/installation/))

## Quick Start

### 1. Install dependencies

```bash
# Install all dependencies (production + dev)
uv sync --all-groups

# Activate virtual environment
source .venv/bin/activate
```

### 2. Setup environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Setup database

```bash
# Create database (if using local PostgreSQL)
createdb {{ cookiecutter.postgres_db }}

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Start development server

```bash
python manage.py runserver
```

Access at:
- API: http://localhost:8000/api/
- Schema: http://localhost:8000/api/schema/swagger/
- Admin: http://localhost:8000/admin/

## Common Commands

### Dependency Management

```bash
# Add a new package
uv pip install package-name

# Add to dev dependencies
uv pip install --group dev package-name

# Update lock file
uv lock --upgrade
```

### Django Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Django shell
python manage.py shell
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test
pytest apps/base/tests/
```

### Docker Development

```bash
# Start services
docker-compose -f deployment/docker/docker-compose.yml up

# View logs
docker-compose logs -f web

# Run migrations in Docker
docker-compose exec web python manage.py migrate

# Stop services
docker-compose down
```

## Environment Setup

Key variables in `.env`:

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_NAME={{ cookiecutter.postgres_db }}
DATABASE_USER={{ cookiecutter.postgres_user }}
DATABASE_PASSWORD={{ cookiecutter.postgres_password }}
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Language
LANGUAGE_CODE={{ cookiecutter.primary_language }}
```

See `.env.example` for all available options.

## Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [uv Documentation](https://docs.astral.sh/uv/)

---

**Last Updated**: 2026-07-29
