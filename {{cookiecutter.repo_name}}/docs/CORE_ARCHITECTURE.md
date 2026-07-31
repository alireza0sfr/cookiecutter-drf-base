# Core Architecture

## Overview
The `core/` directory contains reusable, domain-agnostic utilities shared across all Django apps. This replaces the clean architecture pattern (infrastructure/presentation/application layers) with a more Django-idiomatic, modular approach.

## Structure

```
core/
├── exceptions/           # Exception classes and handlers
│   ├── exceptions.py     # Custom exception hierarchy
│   └── handlers.py       # DRF exception handler
├── middleware/           # Django middleware
│   └── app_context.py    # Thread-local request/view context
├── permissions/          # DRF permission classes
│   └── base.py          # Permission hierarchy (IsSuperUser, IsAdminUser, etc.)
├── renderers/            # DRF custom renderers
│   └── camelize.py      # camelCase JSON response wrapper
├── schema/               # drf-spectacular schema customization
│   └── schema.py        # CustomAutoSchema with input/output serializer support
├── serializers/          # Base serializer fields and classes
│   └── base.py          # EnumSerializerField, KeyPairSerializer
├── throttles/            # Rate limiting
│   └── throttle.py      # CustomRateThrottle with scope-based limits
├── utils/                # Utility services
│   ├── context.py       # AppContext for thread-local storage
│   └── ip.py            # IPService for client IP extraction
├── views/                # Base view classes
│   └── base.py          # BaseViewSet, BaseAPIView
├── admin.py              # Project-wide admin customizations
├── models.py             # Project-wide base models
└── choice.py             # Reusable choice enums
```

## Usage in Apps

### Creating an App

```bash
python manage.py startapp apps/<app_name>
```

Typical structure for an app:

```
apps/account/
├── migrations/
├── models.py            # Domain models
├── serializers.py       # DRF serializers
├── views.py             # Viewsets/Views using core.views.BaseViewSet
├── urls.py              # App-specific routes
├── admin.py             # Django admin
├── permissions.py       # App-specific permissions (can extend core.permissions)
├── filters.py           # DRF filters
└── services.py          # Business logic
```

### Example ViewSet

```python
from rest_framework import viewsets
from core.views import BaseViewSet
from core.throttles.throttle import CustomRateThrottle
from core.permissions.base import IsAuthenticated

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    throttle_classes = [CustomRateThrottle]
    throttle_scope = "high"  # For CustomRateThrottle scopes
    permission_classes = [IsAuthenticated]
    
    def get_input_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_output_serializer_class(self):
        return UserDetailSerializer
```

## Key Components

### Exceptions (`core/exceptions/`)
- `BaseCustomException`: Base class with status_code, success, key, and errors fields
- `EntityNotFoundException`, `ValidationException`, `PermissionDeniedException`, etc.
- `custom_exception_handler`: DRF exception handler that wraps all responses

### Middleware (`core/middleware/`)
- `AppContextMiddleware`: Stores request in thread-local storage via `AppContext`
- Enables accessing current request anywhere without parameter threading

### Permissions (`core/permissions/`)
- `IsSuperUser`: Admin-only
- `IsAdminUser`: Admin or staff
- `IsAuthenticated`: Must be logged in
- `IsVerified`: Must have is_verified=True
- `CurrentUserOrAdmin`: User is the resource owner or admin
- `IsOwnerOrReadOnly`: Public read, private write

### Rate Limiting (`core/throttles/`)
- `CustomRateThrottle`: Scope-based rate limiting
- Scopes: `crucial` (10/hr), `high` (20/min), `medium` (25/min), `low` (35/min)

### Views (`core/views/`)
- `BaseViewSet`: Extended GenericViewSet with AppContext support
- `BaseAPIView`: Base for non-viewset APIs
- Both support `get_input_serializer_class()` and `get_output_serializer_class()`

### Serializers (`core/serializers/`)
- `EnumSerializerField`: Type-safe enum serialization
- Base fields for common patterns

### Renderers (`core/renderers/`)
- `CamelCaseJSONRenderer`: Automatic snake_case → camelCase conversion
- Matches `djangorestframework-camel-case` but with DRF integration

## Integration with Apps

Every app should:
1. Import from `core.views.BaseViewSet` for viewsets
2. Use separate input/output serializers
3. Extend `core.permissions.*` for auth
4. Set `throttle_scope` on views
5. Inherit from `core.admin.UnfoldModelAdmin` for admin

This ensures consistency and leverages shared infrastructure across the project.
