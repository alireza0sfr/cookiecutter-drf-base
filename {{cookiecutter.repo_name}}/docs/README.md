# {{ cookiecutter.project_name }} Documentation

Welcome to {{ cookiecutter.project_name }} documentation.

## Quick Start

- **Setup**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **API**: See [API.md](API.md)
- **Testing**: See [TESTING.md](TESTING.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## Key Resources

- [Project Structure](ARCHITECTURE.md) — System design and core abstractions
- [Development Setup](DEVELOPMENT.md) — Local environment setup
- [API Documentation](API.md) — REST endpoints and schemas
- [Testing Guide](TESTING.md) — Test strategies and coverage
- [Deployment Guide](DEPLOYMENT.md) — Production deployment
- [Coding Standards](..\..\.claude\CLAUDE.md) — Code quality guidelines

## Features

{% if cookiecutter.use_drf == 'y' %}
- Django REST Framework for API development
{% endif %}
{% if cookiecutter.public_api == 'y' %}
- Public Swagger/OpenAPI documentation
{% endif %}
{% if cookiecutter.include_celery == 'y' %}
- Celery for asynchronous task processing
{% endif %}
{% if cookiecutter.include_channels == 'y' %}
- Django Channels for WebSocket support
{% endif %}

## Technology Stack

- **Framework**: Django 5.0+
- **API**: Django REST Framework 3.14+
- **Admin**: Django Unfold
- **Database**: PostgreSQL
- **Cache**: Redis
- **Testing**: pytest + factory_boy
- **Container**: Docker + Docker Compose
- **Package Manager**: uv

## Getting Help

1. Check the documentation in this directory
2. Review `.claude/CLAUDE.md` for coding standards
3. Look at example code in `apps/` directory
4. Check test files in `tests/` directory

---

**Last Updated**: 2026-07-29
