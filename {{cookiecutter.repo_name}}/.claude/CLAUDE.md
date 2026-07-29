# Claude Code Instructions for {{ cookiecutter.project_name }}

Project-specific coding standards and guidelines.

## Project Overview

**Project**: {{ cookiecutter.project_name }}  
**Description**: {{ cookiecutter.project_description }}
**Python Version**: 3.11+  
**Package Manager**: uv  
**Framework**: Django 5.0+ + DRF 3.14+  
**API Documentation**: drf-spectacular (OpenAPI 3.0)  
**Admin Panel**: Django Unfold  
**Testing**: pytest with factory_boy  
**Code Quality**: ruff  

## Project Structure

```
{{ cookiecutter.repo_name }}/
├── .claude/                   # Claude Code configuration
│   └── CLAUDE.md             # This file
├── deployment/               # Infrastructure & deployment
│   ├── docker/               # Docker & Docker Compose
│   └── kubernetes/           # Kubernetes manifests (optional)
├── docs/                     # Project documentation
├── apps/                     # Django apps
│   ├── base/                 # Base functionality
│   ├── dashboard/            # Admin dashboard
│   └── ...
├── core/                     # Shared utilities
├── tests/                    # Test utilities
├── locale/                   # Internationalization
└── pyproject.toml           # Dependencies
```

## Key Standards

### Models
- Extend `django.db.models.Model`
- Use `django-lifecycle` hooks, NOT signals
- Include docstrings
- Use `auto_now` and `auto_now_add` for timestamps

### Serializers
- Use SEPARATE input and output serializers
- Include `help_text` and docstrings

### Views
- Extend `rest_framework` ViewSets
- Implement proper permission classes
- Set `throttle_scope` if using rate limiting

### Admin
- Extend `UnfoldModelAdmin` for enhanced UI
- Include filters, search, and actions
- Use proper fieldsets

### Testing
- **MINIMUM** 80% code coverage
- **TARGET** 90%+ coverage
- Use factory_boy for test objects
- Test models, serializers, views, admin

### Code Quality

```bash
# Format and check
ruff format .
ruff check . --fix

# Django validation
python manage.py check

# Run tests
pytest --cov=apps --cov-report=html
```

### Commit Messages

Follow Commitizen conventions:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`

## Quick Commands

```bash
# Setup
uv sync --all-groups
source .venv/bin/activate

# Django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Tests
pytest
pytest --cov=apps --cov-report=html

# Code Quality
ruff format .
ruff check . --fix

# Docker
docker-compose -f deployment/docker/docker-compose.yml up
```

## Environment Variables

Required variables in `.env`:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (False in production)
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_HOST` and `REDIS_PORT` - Redis config
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

See `.env.example` for all available options.

## API Documentation

- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Support

For questions or issues:
1. Check `docs/` directory for documentation
2. Review existing code patterns
3. Follow the standards in this file

---

**Last Updated**: 2026-07-29  
**Framework**: Django 5.0+ + DRF 3.14+
