# Claude Code Instructions for {{ cookiecutter.project_name }}

This file contains project-specific guidelines for all code modifications, features, and bugfixes.

## Project Overview

**Project**: {{ cookiecutter.project_name }}  
**Python Version**: 3.11+  
**Package Manager**: uv  
**API Documentation**: drf-spectacular (OpenAPI 3.0)  
**Admin Panel**: Django Unfold  
**Testing Framework**: pytest with factories  
**Code Quality**: ruff  

See [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) for detailed setup and commands.

## Project Structure

```
{{ cookiecutter.repo_name }}/
├── apps/                          # Django apps
│   ├── base/                      # Base/shared functionality
│   ├── dashboard/                 # Admin dashboard
│   └── [feature apps]/            # Feature-specific apps
├── core/                          # Reusable utilities
├── deployment/                    # Docker, Kubernetes
├── docs/                          # Documentation
├── locale/                        # Translations
├── tests/                         # Shared test utilities
├── manage.py                      # Django CLI
├── pyproject.toml                # Dependencies
└── CLAUDE.md                      # This file
```

## Key Standards

### Models
- **MUST** extend `django.db.models.Model`
- **MUST** use `django-lifecycle` hooks, NOT signals
- **MUST** include docstrings
- Use `auto_now` and `auto_now_add` for timestamps

### Serializers
- **MUST** use SEPARATE input and output serializers
- Include field `help_text` and docstrings

### Views
- **MUST** extend `core.views.BaseViewSet`
- **MUST** implement `get_input_serializer_class()` and `get_output_serializer_class()`
- **MUST** set `throttle_scope` for rate limiting

### Admin
- **MUST** extend `UnfoldModelAdmin` from `core.admin`

### Testing
- **MINIMUM** 80% code coverage
- **TARGET** 90%+ coverage

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
pytest --cov=apps --cov-report=html

# Code Quality
uv run ruff format .
uv run ruff check .
python manage.py check

# Docker
docker-compose -f deployment/docker/docker-compose.yml up
```

## Commit Messages

Follow Commitizen conventions:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`

---

**Last Updated**: 2026-07-29
