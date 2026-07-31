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
│   │   ├── models/
│   │   │   ├── __init__.py        # Imports all models
│   │   │   └── <model-name>.py
│   │   ├── admin/
│   │   │   ├── __init__.py        # Imports all admin configs
│   │   │   └── <model-name>_admin.py
│   │   ├── views/
│   │   │   ├── __init__.py        # Imports all viewsets
│   │   │   └── <model-name>_views.py
│   │   ├── serializers/
│   │   │   ├── __init__.py        # Imports all serializers
│   │   │   └── <model-name>_serializers.py
│   │   ├── apps.py
│   │   └── urls.py
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

## Graphify for Smart Code Discovery

**Use Graphify instead of raw grepping to save tokens and get better results.**

Graphify builds a knowledge graph of your codebase and answers structural questions intelligently. Always use it for code navigation and discovery instead of manual searching or asking Claude to grep.

### Common Graphify Queries

```bash
# Find where something is defined or used
graphify query "where is <symbol> defined"
graphify query "where is caching configured"
graphify query "which files reference <model-name>"

# Understand relationships between components
graphify path "User" "Permission"
graphify path "BaseViewSet" "CustomAutoSchema"

# Explore architectural concepts
graphify explain "input/output serializer pattern"
graphify explain "django-lifecycle hooks vs signals"
graphify explain "factory_boy usage in tests"

# Find implementation patterns
graphify query "show me examples of admin classes with filters"
graphify query "find all serializers with custom validation"

# Debug and troubleshoot
graphify query "where is the error handler for 404"
graphify query "how is pagination implemented"
```

### Token Savings with Graphify

Instead of:
- ❌ Asking Claude to read files and search (multiple file reads = many tokens)
- ❌ Running `grep -r` and pasting results (large result sets)
- ❌ Re-explaining the codebase structure in each session

Use:
- ✅ `graphify query` to find exact locations (1 API call)
- ✅ `graphify explain` to understand patterns (semantic understanding)
- ✅ `graphify path` to trace relationships (graph traversal)

**Each session should start with graphify queries to understand the relevant code before asking Claude to work on it.** This reduces the context Claude needs to load and speeds up iterations.

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
- **MUST** use `ClassVar` annotation or initialize list attributes in `__init__` (RUF012)
  - ❌ Bad: `list_display = ['field1', 'field2']`
  - ✅ Good: `list_display: ClassVar = ['field1', 'field2']` or initialize in `__init__`
  - This prevents ruff linting errors for mutable default values on class attributes

### Testing
- **MINIMUM** 80% code coverage
- **TARGET** 90%+ coverage

## File and Directory Naming Conventions

Each app **MUST** organize code into dedicated directories with the following structure:

```
apps/<app-name>/
├── models/
│   ├── __init__.py         # from .<model-name> import <ModelName>
│   └── <model-name>.py     # One model class per file
├── admin/
│   ├── __init__.py         # from .<model-name>_admin import <ModelName>Admin
│   └── <model-name>_admin.py
├── views/
│   ├── __init__.py         # from .<model-name>_views import <ModelName>ViewSet
│   └── <model-name>_views.py
├── serializers/
│   ├── __init__.py         # from .<model-name>_serializers import ...
│   └── <model-name>_serializers.py
├── migrations/
├── apps.py
└── urls.py
```

### Naming Rules
- **Model files**: `<model-name>.py` (snake_case, matches model name)
- **Admin files**: `<model-name>_admin.py`
- **View files**: `<model-name>_views.py`
- **Serializer files**: `<model-name>_serializers.py`
- **Directory __init__.py**: Import and re-export from submodules to enable clean imports

### Import Pattern
Instead of:
```python
from apps.users.models.user import User
from apps.users.admin.user_admin import UserAdmin
```

Use:
```python
from apps.users.models import User
from apps.users.admin import UserAdmin
```

Achieve this by populating `__init__.py` files:
```python
# apps/users/models/__init__.py
from .user import User

__all__ = ['User']
```

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

**Last Updated**: 2026-07-31  
**Latest Update**: Added Graphify for Smart Code Discovery to reduce token usage in sessions
