# Testing Guide

Testing strategies and best practices for {{ cookiecutter.project_name }}.

## Running Tests

```bash
# Run all tests
pytest

# Run specific app
pytest apps/base/

# Run specific test file
pytest apps/base/tests/test_models.py

# Run with coverage
pytest --cov=apps --cov-report=html

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Test Structure

```
apps/feature/
  tests/
    __init__.py
    test_models.py          # Model tests
    test_serializers.py     # Serializer tests
    test_views.py           # View/API tests
    test_admin.py           # Admin tests (if applicable)
    factories.py            # Factory Boy factories
```

## Writing Tests

### Model Tests

```python
import pytest
from apps.feature.models import MyModel

@pytest.mark.django_db
class TestMyModel:
    def test_create_model(self):
        obj = MyModel.objects.create(
            field1="value1",
            field2="value2"
        )
        assert obj.pk is not None
        assert obj.field1 == "value1"
```

### Serializer Tests

```python
import pytest
from apps.feature.serializers import MySerializer

@pytest.mark.django_db
class TestMySerializer:
    def test_valid_serializer(self):
        data = {"field1": "value1", "field2": "value2"}
        serializer = MySerializer(data=data)
        assert serializer.is_valid()

    def test_invalid_serializer(self):
        data = {"field1": ""}  # Invalid
        serializer = MySerializer(data=data)
        assert not serializer.is_valid()
```

### View Tests

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestMyViewSet:
    @pytest.fixture
    def client(self):
        return APIClient()

    def test_list_endpoint(self, client):
        response = client.get('/api/resource/')
        assert response.status_code == 200
        assert 'results' in response.data

    def test_create_endpoint(self, client):
        data = {"field1": "value1"}
        response = client.post('/api/resource/', data)
        assert response.status_code == 201
```

## Using Factories

Use `factory_boy` to create test data:

```python
# apps/feature/tests/factories.py
import factory
from apps.feature.models import MyModel

class MyModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyModel

    field1 = factory.Faker('name')
    field2 = factory.Faker('email')
```

In tests:

```python
def test_with_factory(self):
    obj = MyModelFactory()
    assert obj.pk is not None
```

## Test Database

Tests use an isolated test database. Reset between test runs:

```bash
pytest --reuse-db       # Reuse test database
pytest --create-db      # Create new test database
pytest --nomigrations   # Skip migrations (faster, less reliable)
```

## Coverage Requirements

- **Minimum**: 80%
- **Target**: 90%+

View coverage report:

```bash
pytest --cov=apps --cov-report=html
open htmlcov/index.html
```

## Fixtures

Common pytest fixtures:

```python
@pytest.fixture
def authenticated_client(client, user_factory):
    user = user_factory()
    client.force_authenticate(user=user)
    return client
```

## Mocking

Use `unittest.mock` for external dependencies:

```python
from unittest.mock import patch, MagicMock

@patch('external_service.call')
def test_with_mock(self, mock_call):
    mock_call.return_value = {"result": "success"}
    # Your test
```

## Best Practices

1. ✅ **DO**:
   - Test business logic thoroughly
   - Use factories for consistent test data
   - Test edge cases and error conditions
   - Keep tests focused (one thing per test)
   - Use descriptive test names

2. ❌ **DON'T**:
   - Don't test Django internals
   - Don't use random data in tests
   - Don't test external APIs (mock them)
   - Don't skip slow tests without good reason

## Continuous Integration

Tests run automatically on every push via CI/CD. Check results before merging.

---

**Last Updated**: 2026-07-29
