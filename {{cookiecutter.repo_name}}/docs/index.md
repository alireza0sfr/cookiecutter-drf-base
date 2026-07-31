# Aghamohandes Backend Documentation

Welcome to the Aghamohandes Backend documentation. This guide covers architecture, APIs, development, and deployment.

## Quick Start

- **New to the project?** Start with [Architecture](ARCHITECTURE.md)
- **Adding a feature?** Follow the [New Feature Guide](guides/adding-new-feature.md)
- **Deploying to production?** See [Deployment Guide](DEPLOYMENT.md)
- **Debugging an issue?** Check [Troubleshooting](TROUBLESHOOTING.md)

## Core Topics

### Development
- [Architecture](ARCHITECTURE.md) — System design and core abstractions
- [Adding a New Feature](guides/adding-new-feature.md) — Step-by-step feature development
- [Testing Guide](TESTING.md) — Test strategies and coverage requirements
- [Debugging Guide](guides/debugging.md) — Debugging techniques and tools

### API
- [API Documentation](API.md) — REST endpoints and schemas
- [Database Schema](DATABASE.md) — Models, migrations, and relationships

### Operations
- [Deployment Guide](DEPLOYMENT.md) — Environments, CI/CD, and releases
- [Docker & Docker Compose](DOCKER.md) — Containerization (dev, staging, prod)
- [Kubernetes Deployment](KUBERNETES.md) — K8s orchestration and scaling
- [Performance Tuning](guides/performance-tuning.md) — Optimization tips
- [Security Best Practices](guides/security.md) — Security guidelines

### Maintenance
- [Troubleshooting](TROUBLESHOOTING.md) — Common issues and solutions
- [Contributing Guide](CONTRIBUTING.md) — Code standards and workflows

## Project Info

- **Framework**: Django 5.0.2 + Django REST Framework 3.14.0
- **Python**: 3.11+
- **Package Manager**: uv
- **API Schema**: drf-spectacular (OpenAPI 3.0)
- **Admin Panel**: Django Unfold
- **Testing**: pytest with factory_boy
- **Code Quality**: ruff

## Key References

- [CLAUDE.md](../.claude/CLAUDE.md) — Project-specific coding standards
- [README.md](README.md) — Project overview
- [DEVELOPMENT.md](DEVELOPMENT.md) — Setup and development commands
- [CORE_ARCHITECTURE.md](CORE_ARCHITECTURE.md) — Core utilities documentation

---

**Last Updated**: 2026-07-29

For updates or questions about documentation, see [Contributing Guide](CONTRIBUTING.md).
