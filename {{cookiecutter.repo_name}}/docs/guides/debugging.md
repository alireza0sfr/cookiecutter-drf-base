# Debugging Guide

Techniques and tools for debugging Django applications.

## Python Debugger (pdb)

### Basic Usage

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Run code to breakpoint
# Then interact in Python debugger

# Commands:
# n (next) - execute next line
# s (step) - step into function
# c (continue) - continue execution
# l (list) - show current code
# p variable - print variable
# pp variable - pretty print variable
# w (where) - show stack trace
# h (help) - show help
```

### Example

```python
def calculate_total(items):
    import pdb; pdb.set_trace()  # Breakpoint here
    total = 0
    for item in items:
        total += item.price
    return total
```

### Python 3.7+ Syntax

```python
# Simpler syntax (no import needed)
breakpoint()
```

## Django Shell

Interactive Python shell with Django models loaded:

```bash
python manage.py shell
```

### Examples

```python
# Query models
from apps.articles.models import Article
articles = Article.objects.all()
print(articles.query)  # Print SQL query

# Test functions
from apps.articles.serializers import ArticleDetailSerializer
article = Article.objects.first()
serializer = ArticleDetailSerializer(article)
print(serializer.data)

# Create test data
from apps.articles.factories import ArticleFactory
article = ArticleFactory(title='Test')

# Check settings
from django.conf import settings
print(settings.DEBUG)
print(settings.DATABASES)

# Test signals/hooks
article = Article.objects.create(title='New Article')
article.refresh_from_db()  # Reload from DB
```

### Enhanced Shell

```bash
# Install django-extensions for better shell
pip install django-extensions

# Use enhanced shell
python manage.py shell_plus

# Additional features:
# - Auto-import all models
# - Print SQL queries
# - Better syntax highlighting
```

## Logging

### Configure Logging

Django logging is configured in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

### Add Logging to Code

```python
import logging
logger = logging.getLogger(__name__)

def my_function():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.exception('Exception occurred')  # With traceback
```

### View Logs

```bash
# View log file
tail -f logs/aghamohandes_backend-*.log

# Search logs
grep "ERROR" logs/aghamohandes_backend-*.log

# Follow logs from Django runserver
python manage.py runserver
# Logs appear in console
```

## Inspect Database Queries

### Print All Queries

```python
# In settings.py (development only)
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Using django-debug-toolbar

```bash
# Install
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'debug_toolbar',
    # ... other apps
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... other middleware
]

# Add to urls.py
if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

Then visit any page and click the debug toolbar in the bottom-right corner.

### Count Queries

```python
from django.test.utils import override_settings
from django.db import connection, reset_queries

@override_settings(DEBUG=True)
def test_article_list():
    reset_queries()
    articles = Article.objects.all()
    list(articles)  # Force evaluation
    
    print(f"Queries executed: {len(connection.queries)}")
    for query in connection.queries:
        print(query['sql'])
```

## Test Debugging

### Run Single Test with Output

```bash
# Show print statements and logging
pytest -vvs apps/articles/tests/test_views.py::TestArticleViewSet::test_list_articles

# Drop into debugger on failure
pytest --pdb apps/articles/tests/test_views.py

# Drop into debugger on each test
pytest --pdbcls=IPython.terminal.debugger:Pdb apps/articles/tests/
```

### Inspect Test Database

```python
import pytest
from django.core.management import call_command

@pytest.mark.django_db
def test_with_data_dump():
    article = ArticleFactory()
    
    # Dump data to fixture
    call_command('dumpdata', 'articles.Article', indent=4)
```

## Performance Profiling

### Using cProfile

```python
import cProfile
import pstats

def my_view():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Code to profile
    articles = Article.objects.all()
    result = [str(a) for a in articles]
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

### Timing Code Blocks

```python
import time

start = time.time()

# Code to time
articles = Article.objects.all()
for article in articles:
    print(article.title)

elapsed = time.time() - start
print(f"Took {elapsed:.2f} seconds")
```

## API Debugging

### Test Requests Locally

```bash
# GET request
curl http://localhost:8000/api/v1/articles/

# POST with JSON
curl -X POST http://localhost:8000/api/v1/articles/ \
  -H "Content-Type: application/json" \
  -d '{"title":"New","content":"Test"}'

# With authentication
curl http://localhost:8000/api/v1/articles/ \
  -H "Authorization: Bearer <token>"
```

### Using httpie

```bash
# Install
pip install httpie

# GET request
http GET http://localhost:8000/api/v1/articles/

# POST request
http POST http://localhost:8000/api/v1/articles/ \
  title="New Article" \
  content="Test content"

# With auth
http GET http://localhost:8000/api/v1/articles/ \
  'Authorization: Bearer <token>'

# Save request/response
http --session=debug POST http://localhost:8000/api/v1/articles/
```

### Postman/Insomnia

Use REST API client GUI:
- Import OpenAPI schema from `/api/schema/`
- Test endpoints interactively
- Save test collections
- Automate testing workflows

## Exception Handling

### Catch and Inspect Exceptions

```python
try:
    article = Article.objects.get(id=999)
except Article.DoesNotExist as e:
    print(f"Exception: {type(e).__name__}")
    print(f"Message: {str(e)}")
    import traceback
    traceback.print_exc()
```

### View Full Traceback

```bash
# In Django shell
python manage.py shell
# Then error shows full traceback

# Or use IPython
pip install ipython
python manage.py shell

# IPython shows colored tracebacks
```

## Common Debugging Scenarios

### "User not authenticated" in test

```python
@pytest.mark.django_db
def test_authenticated_endpoint(authenticated_client, user):
    # Use authenticated_client fixture
    response = authenticated_client.get('/api/v1/articles/')
    assert response.status_code == 200
```

### "Object does not exist" exception

```python
# Use .get() carefully
try:
    article = Article.objects.get(id=999)
except Article.DoesNotExist:
    # Handle missing object
    article = None

# Use .first() to avoid exception
article = Article.objects.filter(id=999).first()
if article:
    print(article.title)
```

### Slow query performance

```python
# Identify N+1 queries
articles = Article.objects.all()  # Missing select_related
for article in articles:
    print(article.author.name)  # Query per article!

# Fix with select_related
articles = Article.objects.select_related('author').all()
for article in articles:
    print(article.author.name)  # Single query
```

---

For more debugging info, see:
- [Django Documentation](https://docs.djangoproject.com/en/5.0/topics/debugging/)
- [pytest Documentation](https://docs.pytest.org/en/stable/usage.html)
