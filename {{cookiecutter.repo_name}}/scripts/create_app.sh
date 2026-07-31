#!/bin/bash
# Script to create a new Django app with all required files following project patterns
#
# Usage:
#   chmod +x scripts/create_app.sh
#   ./scripts/create_app.sh <app_name>
#
# Example:
#   ./scripts/create_app.sh articles

if [ -z "$1" ]; then
    echo "Usage: ./scripts/create_app.sh <app_name>"
    echo "Example: ./scripts/create_app.sh articles"
    exit 1
fi

APP_NAME=$1
APP_PATH="apps/$APP_NAME"

# Check if app already exists
if [ -d "$APP_PATH" ]; then
    echo "Error: App '$APP_NAME' already exists at $APP_PATH"
    exit 1
fi

echo "Creating new Django app: $APP_NAME"
echo "Location: $APP_PATH"

# Create the app using Django
python manage.py startapp "$APP_NAME" "$APP_PATH"

# Create additional directories
mkdir -p "$APP_PATH/models"
mkdir -p "$APP_PATH/admin"
mkdir -p "$APP_PATH/views"
mkdir -p "$APP_PATH/serializers"
mkdir -p "$APP_PATH/tests"
mkdir -p "$APP_PATH/migrations"

# Create __init__.py files for directory imports
cat > "$APP_PATH/models/__init__.py" << 'EOF'
"""Models for the app."""
EOF

cat > "$APP_PATH/admin/__init__.py" << 'EOF'
"""Admin configuration for the app."""
EOF

cat > "$APP_PATH/views/__init__.py" << 'EOF'
"""Views and viewsets for the app."""
EOF

cat > "$APP_PATH/serializers/__init__.py" << 'EOF'
"""Serializers for the app."""
EOF

# Create test files
cat > "$APP_PATH/tests/__init__.py" << 'EOF'
"""Tests for the app."""
EOF

cat > "$APP_PATH/tests/test_models.py" << 'EOF'
"""Tests for models."""
import pytest


@pytest.mark.django_db
class TestModels:
    """Test model creation and validation."""

    def test_placeholder(self):
        """Placeholder test."""
        assert True
EOF

cat > "$APP_PATH/tests/test_serializers.py" << 'EOF'
"""Tests for serializers."""
import pytest


@pytest.mark.django_db
class TestSerializers:
    """Test serializer validation and serialization."""

    def test_placeholder(self):
        """Placeholder test."""
        assert True
EOF

cat > "$APP_PATH/tests/test_views.py" << 'EOF'
"""Tests for views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestViews:
    """Test API endpoints."""

    @pytest.fixture
    def client(self):
        """Provide API client."""
        return APIClient()

    def test_placeholder(self, client):
        """Placeholder test."""
        assert True
EOF

cat > "$APP_PATH/tests/test_admin.py" << 'EOF'
"""Tests for admin configuration."""
import pytest


@pytest.mark.django_db
class TestAdmin:
    """Test Django admin configuration."""

    def test_placeholder(self):
        """Placeholder test."""
        assert True
EOF

# Create factories file
cat > "$APP_PATH/factories.py" << 'EOF'
"""Test factories for models."""
import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password('defaultpass123')
        obj.save()
EOF

# Create services file
cat > "$APP_PATH/services.py" << 'EOF'
"""Business logic for the app."""


class BaseService:
    """Base service class for business logic."""

    def __init__(self):
        pass
EOF

# Create filters file
cat > "$APP_PATH/filters.py" << 'EOF'
"""DRF filters for querysets."""
from django_filters import FilterSet, CharFilter


class BaseFilter(FilterSet):
    """Base filter class."""

    class Meta:
        model = None
        fields = []
EOF

# Create permissions file
cat > "$APP_PATH/permissions.py" << 'EOF'
"""DRF permissions for API endpoints."""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Permission to check if user is the object owner."""

    def has_object_permission(self, request, view, obj):
        """Check if user owns the object."""
        return obj.owner == request.user
EOF

# Remove auto-generated models.py and replace with directory structure
rm "$APP_PATH/models.py"

cat > "$APP_PATH/models/__init__.py" << EOF
"""Models for the $APP_NAME app.

Import your models here to enable clean imports:
    from apps.$APP_NAME.models import MyModel

Example:
    Create a file: apps/$APP_NAME/models/my_model.py
    Add content and import here:
        from .my_model import MyModel
"""
EOF

# Remove auto-generated admin.py
rm "$APP_PATH/admin.py"

cat > "$APP_PATH/admin/__init__.py" << EOF
"""Admin configuration for the app.

Import your admin classes here to register them:
    from apps.$APP_NAME.admin import MyModelAdmin

Example:
    Create a file: apps/$APP_NAME/admin/my_model_admin.py
    Add admin config and import here.
"""
EOF

# Remove auto-generated views.py
rm "$APP_PATH/views.py"

cat > "$APP_PATH/views/__init__.py" << EOF
"""Views and viewsets for the app.

Import your viewsets here to enable clean imports:
    from apps.$APP_NAME.views import MyModelViewSet

Example:
    Create a file: apps/$APP_NAME/views/my_model_views.py
    Add viewset and import here.
"""
EOF

# Create serializers/__init__.py if it doesn't exist
if [ ! -f "$APP_PATH/serializers.py" ]; then
    cat > "$APP_PATH/serializers/__init__.py" << EOF
"""Serializers for API endpoints.

Import your serializers here to enable clean imports:
    from apps.$APP_NAME.serializers import MyModelSerializer

Example:
    Create a file: apps/$APP_NAME/serializers/my_model_serializers.py
    Add serializers and import here.

Remember to create SEPARATE input and output serializers for proper request/response handling:
    class MyModelInputSerializer(serializers.Serializer):
        # For request validation
        pass

    class MyModelOutputSerializer(serializers.ModelSerializer):
        # For response formatting
        class Meta:
            model = MyModel
            fields = '__all__'
EOF
fi

# Update apps.py with proper docstring
cat > "$APP_PATH/apps.py" << EOF
"""App configuration."""
from django.apps import AppConfig


class ${APP_NAME^}Config(AppConfig):
    """Configuration for the $APP_NAME app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.$APP_NAME'
    verbose_name = '$(python -c "print('${APP_NAME}'.replace('_', ' ').title())")'
EOF

echo "✓ App structure created at $APP_PATH"
echo ""
echo "Next steps:"
echo "1. Define your models in $APP_PATH/models/<model-name>.py"
echo "2. Create serializers in $APP_PATH/serializers/<model-name>_serializers.py"
echo "3. Create viewsets in $APP_PATH/views/<model-name>_views.py"
echo "4. Create admin config in $APP_PATH/admin/<model-name>_admin.py"
echo "5. Add tests to $APP_PATH/tests/"
echo "6. Update __init__.py files to import your classes"
echo "7. Register in settings.py INSTALLED_APPS"
echo "8. Include URLs in your project's urls.py file"
echo ""
echo "Remember to follow the CLAUDE.md guidelines!"
