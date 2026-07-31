# Database Schema & Migrations

## Database

- **Type**: PostgreSQL 14+
- **Driver**: psycopg2-binary
- **Connection**: Configured via `DATABASE_URL` in `.env`

## Migration Management

### Creating Migrations

```bash
# Detect changes and create migration file
python manage.py makemigrations

# Create migration with custom name
python manage.py makemigrations --name add_user_bio

# Dry run (don't apply)
python manage.py makemigrations --dry-run
```

### Applying Migrations

```bash
# Apply all pending migrations
python manage.py migrate

# Apply specific app migrations
python manage.py migrate dashboard

# Migrate to specific version
python manage.py migrate dashboard 0002

# Rollback to previous version
python manage.py migrate dashboard 0001
```

### Checking Migration Status

```bash
# List migrations and their status
python manage.py showmigrations

# Check for pending migrations
python manage.py makemigrations --check
```

## Model Design

### Base Model Pattern

All models inherit from Django's `models.Model`:

```python
class Article(models.Model):
    """Blog article model."""
    
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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
```

### Indexing Strategy

- **Single Indexes**: `db_index=True` on frequently filtered fields
- **Composite Indexes**: `Meta.indexes` for multi-field queries
- **Foreign Keys**: Always specify `on_delete` (CASCADE, SET_NULL, PROTECT)

### Timestamps

- **auto_now_add=True**: Set on creation, never changes
- **auto_now=True**: Update on every save
- **Use these instead of lifecycle hooks for timestamps**

## Lifecycle Hooks

Use `django-lifecycle` for model logic (not signals):

```python
from django_lifecycle import hook, BEFORE_SAVE, AFTER_CREATE

class Article(models.Model):
    @hook(BEFORE_SAVE)
    def set_slug_before_save(self):
        """Generate slug from title."""
        if not self.slug:
            self.slug = slugify(self.title)
    
    @hook(AFTER_CREATE)
    def invalidate_cache_after_create(self):
        """Invalidate cache."""
        cache.delete('articles_list')
```

## Common Queries

### Select Related (JOINs)

```python
# Avoid N+1 queries
articles = Article.objects.select_related('author').all()

# Multiple relations
articles = Article.objects.select_related('author', 'category').all()
```

### Prefetch Related (Separate Queries)

```python
# For reverse relations and M2M
articles = Article.objects.prefetch_related('comments').all()

# Multiple prefetches
articles = Article.objects.prefetch_related('comments', 'tags').all()
```

### Filtering

```python
# Simple filters
Article.objects.filter(is_published=True)

# Multiple conditions (AND)
Article.objects.filter(is_published=True, author_id=1)

# OR conditions
from django.db.models import Q
Article.objects.filter(Q(is_published=True) | Q(author_id=1))

# Exclude
Article.objects.exclude(is_published=False)

# Get single object
article = Article.objects.get(id=1)  # Raises DoesNotExist if not found
article = Article.objects.filter(id=1).first()  # Returns None if not found
```

### Aggregation

```python
from django.db.models import Count, Sum, Avg

# Count related objects
Article.objects.annotate(comment_count=Count('comments'))

# Sum values
Article.objects.aggregate(total_views=Sum('view_count'))

# Average
Article.objects.aggregate(avg_views=Avg('view_count'))
```

## Database Performance

### Query Optimization

1. **Use `select_related()` for ForeignKey and OneToOne**
   - Converts to single SQL JOIN

2. **Use `prefetch_related()` for ManyToMany and reverse ForeignKey**
   - Separate optimized queries

3. **Index frequently filtered fields**
   - Add `db_index=True` to model fields

4. **Use `only()` and `defer()` for large fields**
   ```python
   Article.objects.only('title', 'slug')  # Load only these fields
   Article.objects.defer('content')       # Load all except content
   ```

5. **Use `values()` or `values_list()` when you don't need model instances**
   ```python
   Article.objects.values_list('id', 'title')  # Returns tuples
   ```

### Caching Strategy

Cache invalidated via lifecycle hooks:

```python
@hook(AFTER_CREATE)
@hook(AFTER_UPDATE)
@hook(AFTER_DELETE)
def invalidate_cache(self):
    cache.delete(f'article_{self.id}')
    cache.delete('articles_list')
    cache.delete(f'articles_author_{self.author_id}')
```

## Transactions

```python
from django.db import transaction

# Atomic transaction (rolls back on exception)
@transaction.atomic
def create_article_with_tags(title, tags):
    article = Article.objects.create(title=title)
    for tag in tags:
        article.tags.add(tag)
    return article

# Manual transaction
with transaction.atomic():
    article = Article.objects.create(title='New Article')
    Comment.objects.create(article=article, content='First comment')
```

---

See [CLAUDE.md](../CLAUDE.md) for model definition patterns and best practices.
