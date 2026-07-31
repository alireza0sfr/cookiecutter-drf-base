# Adding a New Feature

Step-by-step guide for implementing a new feature following project standards.

## Overview

This guide walks through adding a complete feature: models, serializers, viewsets, views, tests, and admin configuration.

**Example**: Adding an article publishing workflow.

## Step 1: Create App Structure

```bash
./scripts/create_app.sh articles
```

This creates:
```
apps/articles/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── serializers.py
├── filters.py
├── services.py
├── factories.py
├── urls.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_serializers.py
│   ├── test_views.py
│   └── test_admin.py
└── migrations/
    └── __init__.py
```

## Step 2: Define Models

Create `apps/articles/models.py`:

```python
from django.db import models
from django_lifecycle import hook, BEFORE_SAVE, AFTER_CREATE
from django.utils.text import slugify

class Article(models.Model):
    """Blog article model."""
    
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='articles')
    is_published = models.BooleanField(default=False, db_index=True)
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['author', '-published_at']),
            models.Index(fields=['is_published', '-created_at']),
        ]

    def __str__(self):
        return self.title

    @hook(BEFORE_SAVE)
    def set_slug_before_save(self):
        """Generate slug from title before saving."""
        if not self.slug:
            self.slug = slugify(self.title)

    @hook(AFTER_CREATE)
    def invalidate_list_cache_after_create(self):
        """Invalidate articles list cache after creation."""
        from django.core.cache import cache
        cache.delete('articles_list')
```

## Step 3: Create Migrations

```bash
python manage.py makemigrations articles
python manage.py migrate articles
```

## Step 4: Write Serializers

Create `apps/articles/serializers.py` with separate input/output:

```python
from rest_framework import serializers
from .models import Article

# Input Serializer (for request validation)
class ArticleInputSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating articles."""
    
    class Meta:
        model = Article
        fields = ('title', 'content', 'is_published')
    
    def validate_title(self, value):
        """Validate title length."""
        if len(value) < 5:
            raise serializers.ValidationError(
                'Title must be at least 5 characters.'
            )
        return value

# Output Serializer (for responses)
class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for article detail response."""
    
    author_name = serializers.CharField(
        source='author.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = Article
        fields = (
            'id', 'title', 'slug', 'content', 'author_name',
            'is_published', 'published_at', 'view_count',
            'created_at', 'updated_at'
        )
        read_only_fields = fields

# List Serializer (lightweight)
class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for article list response."""
    
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'slug', 'author_name', 'is_published', 'view_count', 'created_at')
        read_only_fields = fields
```

## Step 5: Create ViewSet

Create `apps/articles/views.py`:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from core.views import BaseViewSet
from core.permissions.base import IsOwnerOrReadOnly

from .models import Article
from .serializers import (
    ArticleInputSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer
)
from .filters import ArticleFilter

class ArticleViewSet(BaseViewSet):
    """ViewSet for Article CRUD operations."""
    
    queryset = Article.objects.select_related('author')
    permission_classes = [IsOwnerOrReadOnly]
    throttle_scope = 'high'
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'view_count', '-published_at']
    ordering = ['-published_at', '-created_at']
    
    def get_input_serializer_class(self):
        """Return input serializer for action."""
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleInputSerializer
        return ArticleDetailSerializer
    
    def get_output_serializer_class(self):
        """Return output serializer for action."""
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer
    
    def perform_create(self, serializer):
        """Set author on create."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], throttle_scope='crucial')
    def publish(self, request, pk=None):
        """Publish an article."""
        article = self.get_object()
        self.check_object_permissions(request, article)
        
        article.is_published = True
        article.save()
        
        serializer = self.get_serializer(article)
        return Response(serializer.data)
```

## Step 6: Register URLs

Create/update `apps/articles/urls.py`:

```python
from rest_framework.routers import SimpleRouter
from .views import ArticleViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = router.urls
```

Add to `apps/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('articles/', include('apps.articles.urls')),
]
```

## Step 7: Create Admin Interface

Create `apps/articles/admin.py`:

```python
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter
from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    """Article admin interface."""
    
    list_display = ('title', 'author', 'is_published', 'view_count', 'created_at')
    list_filter = ('is_published', ('created_at', RangeDateFilter), 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('slug', 'view_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'author')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('Stats', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def publish_articles(self, request, queryset):
        """Admin action to publish articles."""
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} articles published.')
    publish_articles.short_description = 'Publish selected articles'
```

## Step 8: Create Test Factories

Create `apps/articles/factories.py`:

```python
import factory
from django.contrib.auth.models import User
from .models import Article

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
        obj.set_password(extracted or 'password123')
        obj.save()

class ArticleFactory(factory.django.DjangoModelFactory):
    """Factory for Article model."""
    
    class Meta:
        model = Article
    
    title = factory.Faker('sentence', nb_words=6)
    content = factory.Faker('paragraph', nb_sentences=10)
    author = factory.SubFactory(UserFactory)
    is_published = False
```

## Step 9: Write Comprehensive Tests

Create `apps/articles/tests/test_models.py`:

```python
import pytest
from django.utils import timezone
from ..models import Article
from ..factories import ArticleFactory, UserFactory

@pytest.mark.django_db
class TestArticleModel:
    """Test Article model."""
    
    def test_create_article(self):
        """Test article creation."""
        article = ArticleFactory(title='Test Article')
        assert article.id is not None
        assert article.slug == 'test-article'
    
    def test_article_str(self):
        """Test string representation."""
        article = ArticleFactory(title='My Article')
        assert str(article) == 'My Article'
```

Create `apps/articles/tests/test_views.py`:

```python
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from ..factories import ArticleFactory, UserFactory

@pytest.mark.django_db
class TestArticleViewSet:
    """Test Article viewset."""
    
    @pytest.fixture
    def client(self):
        return APIClient()
    
    def test_list_articles(self, client):
        """Test listing articles."""
        ArticleFactory.create_batch(5, is_published=True)
        response = client.get('/api/v1/articles/')
        assert response.status_code == 200
        assert len(response.data['data']['results']) == 5
    
    def test_create_requires_auth(self, client):
        """Test create requires authentication."""
        data = {'title': 'New', 'content': 'Content'}
        response = client.post('/api/v1/articles/', data)
        assert response.status_code == 401
```

## Step 10: Register in Settings

Update `aghamohandes_backend/settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'apps.articles',  # Add this
]
```

## Step 11: Run Validation

```bash
# Run comprehensive checks
./scripts/validate.sh

# Or individually:
pytest apps/articles/ --cov=apps.articles --cov-fail-under=80
ruff check apps/articles/
ruff format --check apps/articles/
python manage.py check
```

## Step 12: Commit Changes

```bash
git add .
git commit -m "feat(articles): add article publishing workflow

- Create Article model with lifecycle hooks
- Implement ArticleViewSet with publish action
- Add comprehensive tests (85% coverage)
- Register in admin panel with Unfold

Closes #123"
```

## Checklist

- [ ] Models created with proper fields and indexes
- [ ] Migrations created and tested
- [ ] Input/output serializers created
- [ ] ViewSet implemented with proper permissions
- [ ] URLs registered in router
- [ ] Admin interface configured
- [ ] Test factories created
- [ ] Comprehensive tests (80%+ coverage)
- [ ] All validation checks pass
- [ ] Docstrings added
- [ ] Commit message follows conventions
- [ ] PR created with description

---

For more details, see:
- [CLAUDE.md](../../CLAUDE.md) - Coding standards
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [TESTING.md](../TESTING.md) - Testing guide
