"""
Pytest configuration and shared fixtures for all tests.

This file is automatically loaded by pytest and provides:
- Django database setup
- API client fixtures
- Common test factories
- Test settings
"""

import os
import django
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# Ensure Django is set up
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aghamohandes_backend.settings')
django.setup()


@pytest.fixture
def api_client():
    """Provide REST API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(db, user):
    """Provide API client authenticated as a user."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(db, admin_user):
    """Provide API client authenticated as admin."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def staff_user(db):
    """Create a test staff user."""
    user = User.objects.create_user(
        username='staff',
        email='staff@example.com',
        password='staffpass123'
    )
    user.is_staff = True
    user.save()
    return user


@pytest.fixture(autouse=True)
def reset_cache(db):
    """Clear cache before each test."""
    from django.core.cache import cache
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def mock_redis(monkeypatch):
    """Mock Redis for testing without actual Redis."""
    from unittest.mock import MagicMock
    mock_cache = MagicMock()
    monkeypatch.setattr('django.core.cache.cache', mock_cache)
    return mock_cache


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with Django settings."""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'rest_framework',
                'drf_spectacular',
            ],
            MIDDLEWARE=[],
            ROOT_URLCONF='',
            SECRET_KEY='test-secret-key',
        )
        django.setup()


# Pytest markers
def pytest_configure_markers(config):
    """Register custom markers."""
    config.addinivalue_line(
        'markers', 'slow: marks tests as slow (deselect with "-m \'not slow\'")'
    )
    config.addinivalue_line(
        'markers', 'integration: marks tests as integration tests'
    )
    config.addinivalue_line(
        'markers', 'e2e: marks tests as end-to-end tests'
    )


# Test output options
def pytest_collection_modifyitems(config, items):
    """Add markers and configure test collection."""
    for item in items:
        # Mark tests in test_integration.py as integration
        if 'integration' in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Mark tests in test_e2e.py as e2e
        if 'e2e' in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


# Plugins
pytest_plugins = [
    'pytest_django',
    'pytest_cov',
]
