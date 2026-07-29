# Architecture

System design and core abstractions for {{ cookiecutter.project_name }}.

## Project Structure

```
{{ cookiecutter.repo_name }}/
├── apps/                          # Django apps
│   ├── base/                      # Base/shared functionality
│   ├── dashboard/                 # Admin dashboard
│   └── [feature apps]/            # Feature-specific apps
├── core/                          # Reusable utilities
│   ├── exceptions/                # Exception classes
│   ├── middleware/                # Custom middleware
│   ├── permissions/               # DRF permissions
│   ├── serializers/               # Base serializers
│   ├── views/                     # Base views
│   └── models.py                  # Base model
├── deployment/
│   └── docker/                    # Docker configuration
├── docs/                          # Documentation
├── locale/                        # Translations
├── tests/                         # Shared test utilities
└── pyproject.toml                # Dependencies
```

## Core Concepts

### Apps
- Each feature is a Django app in `apps/`
- Typical structure: models.py, serializers.py, views.py, urls.py, tests/
- Follow Django conventions for app organization

### Serializers Pattern
- **Input Serializers**: Validate request data
- **Output Serializers**: Format response data
- Keep them separate for clarity

### Views Pattern
- Extend `rest_framework.viewsets.ViewSet` or `ModelViewSet`
- Implement `get_input_serializer_class()` and `get_output_serializer_class()`
- Set appropriate permission and throttle classes

### Models
- Always extend `django.db.models.Model`
- Use `django-lifecycle` for hooks instead of signals
- Include proper `Meta` options and docstrings

## Design Patterns

### Request-Response Flow

```
Request → URL Router → Viewset → Serializer (Input) → Model Logic
                                                          ↓
Response ← Serializer (Output) ← Model Data ← Database Query
```

### Error Handling

- Use custom exception classes from `core.exceptions`
- DRF handles serialization and HTTP status codes
- Include meaningful error messages and codes

### Authentication & Permissions

- Session-based authentication for admin
- Token-based for API (optional)
- Permission classes on ViewSets

## Database Design

### Migrations
- Use Django's built-in migration system
- Create meaningful migration names
- Test migrations locally before deploying

### Relationships
- Use ForeignKey for 1-to-N relationships
- Use ManyToManyField for M-to-N
- Use OneToOneField for 1-to-1

## API Design

### Endpoint Structure

```
/api/v1/
  /resource/              # List, create
  /resource/{id}/         # Retrieve, update, delete
  /resource/{id}/action/  # Custom action
```

### Status Codes
- `200 OK`: Successful GET/PUT/PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: No permission
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Testing Strategy

### Test Organization
```
apps/feature/
  tests/
    __init__.py
    test_models.py
    test_serializers.py
    test_views.py
```

### Test Levels
- **Unit Tests**: Models and utilities
- **Integration Tests**: Serializer and view combinations
- **API Tests**: Full endpoint testing

### Minimum Coverage
- **Minimum**: 80%
- **Target**: 90%+

## Deployment Architecture

### Environments
- **Development**: Local with Django dev server
- **Staging**: Staging-like production with debug enabled
- **Production**: Full production with all security features

### Docker
- Multi-stage build optimizes image size
- Separate images for development vs production
- Docker Compose for local orchestration

## Configuration Management

### Environment Variables
- Stored in `.env` file (never committed)
- Loaded by Django settings
- Override in production via deployment platform

### Secrets
- Database credentials
- API keys
- Secret key
- Should never be in git

---

**Last Updated**: 2026-07-29
