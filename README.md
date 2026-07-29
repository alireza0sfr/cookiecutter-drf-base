# Cookiecutter DRF Base

A modern Django REST Framework project template with production-ready infrastructure, comprehensive documentation, and best practices.

## Features

- **Modern DRF Stack**: Django 5.0+, DRF 3.14+, drf-spectacular
- **Package Management**: `uv` for fast, reliable dependency management
- **Admin Interface**: Django Unfold for enhanced admin panel
- **Testing**: pytest with factory_boy and 80%+ coverage targets
- **Containerization**: Multi-stage Docker builds (dev/staging/production)
- **Orchestration**: Kubernetes manifests with Kustomize overlays
- **Documentation**: Comprehensive guides and API documentation
- **Code Quality**: ruff for formatting and linting
- **Internationalization**: Django i18n with Persian locale support
- **CI/CD**: GitHub Actions ready

## Quick Start

```bash
# Install cookiecutter
pip install cookiecutter

# Generate new project
cookiecutter https://github.com/yourusername/cookiecutter-drf-base.git

# Navigate to project
cd <your-project-name>-backend

# Install dependencies
uv sync --all-groups

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

Generated projects include:

```
<project>-backend/
├── .claude/
│   └── CLAUDE.md              # Project-specific coding standards
├── deployment/
│   ├── docker/                # Dockerfile and docker-compose
│   └── kubernetes/            # K8s manifests and Kustomize overlays
├── docs/
│   ├── README.md             # Project overview
│   ├── DEVELOPMENT.md        # Setup and development
│   ├── ARCHITECTURE.md       # System design
│   ├── API.md               # REST endpoints
│   ├── TESTING.md           # Testing guide
│   ├── DEPLOYMENT.md        # Deployment guide
│   └── guides/              # Feature guides
├── apps/                      # Django feature applications
├── core/                      # Reusable utilities
├── tests/                     # Shared test utilities
├── locale/                    # Internationalization
└── pyproject.toml            # Dependencies via uv
```

## Configuration Options

The template prompts for:

- **project_name**: Human-readable project name
- **project_description**: Brief project description
- **use_drf**: Django REST Framework (default: true)
- **public_api**: Public Swagger documentation (default: false)
- **user_has_phone_number**: User phone field (default: false)
- **user_has_wallet**: User wallet support (default: false)
- **include_celery**: Celery task queue (default: false)
- **include_channels**: Django Channels (default: false)
- **primary_language**: Primary app language (default: en)

## Customization

After generating a project, customize:

1. **docs/README.md** - Project description and features
2. **.claude/CLAUDE.md** - Team coding standards
3. **pyproject.toml** - Add/remove dependencies
4. **deployment/docker/.env** - Environment variables

## License

MIT

## Support

For issues or questions about generated projects, refer to the project's documentation in `docs/` directory.
