# Contributing Guide

## Code of Conduct

- **Respectful**: Treat all contributors with respect
- **Collaborative**: Share knowledge and help others
- **Inclusive**: Welcome diverse perspectives and backgrounds
- **Quality**: Maintain high code quality standards

## Getting Started

### 1. Setup Development Environment

```bash
# Clone repository
git clone <your-repo-url>
cd {{ cookiecutter.repo_name }}

# Create virtual environment
uv sync --all-groups

# Setup environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

### 2. Create Feature Branch

```bash
# Create branch from main (use semantic naming)
git checkout -b feat/add-user-authentication
git checkout -b fix/cache-invalidation-bug
git checkout -b docs/update-api-guide
```

**Branch Naming Convention**:
- `feat/` - New feature
- `fix/` - Bug fix
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions
- `chore/` - Maintenance

### 3. Make Changes

Follow the [CLAUDE.md](../CLAUDE.md) standards:
- Add comprehensive docstrings
- Use proper input/output serializers
- Write tests (80%+ coverage minimum)
- Format with ruff
- Add lifecycle hooks (not signals)

### 4. Test Your Changes

```bash
# Run validation script (comprehensive checks)
./scripts/validate.sh

# Or run checks individually:

# Tests with coverage
pytest apps/ --cov=apps --cov-report=html --cov-fail-under=80

# Code quality
ruff check .
ruff format --check .

# Django validation
python manage.py check

# Migration check
python manage.py makemigrations --dry-run --check
```

### 5. Commit with Semantic Messages

Follow [Commitizen](https://commitizen-tools.github.io/commitizen/) conventions:

```bash
# Example commit messages:
git commit -m "feat(dashboard): add article publishing workflow

- Implement publish/unpublish actions
- Add published_at timestamp handling
- Update tests

Closes #123"

git commit -m "fix(core): handle missing AppContext gracefully

Previously crashed when context unavailable.
Now falls back to request object.

Fixes #456"

git commit -m "docs(testing): clarify factory_boy usage with examples"
```

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, perf, test, chore, ci

**Scopes**: core, settings, auth, dashboard, testing, translations, etc.

### 6. Create Pull Request

```bash
# Push branch
git push origin feat/add-user-authentication

# Create PR on GitHub with:
- Clear title (under 70 chars)
- Description of changes
- Link to related issues
- Screenshots (if UI changes)
```

**PR Template**:

```markdown
## Description
Brief description of changes.

## Changes
- Added user authentication module
- Integrated with JWT tokens
- Updated settings for authentication

## Testing
- [ ] Unit tests pass: `pytest apps/auth/tests/`
- [ ] Coverage 80%+: `pytest --cov=apps`
- [ ] Validation passes: `./scripts/validate.sh`
- [ ] Manual testing on dev server

## Related Issues
Closes #123
Fixes #456
```

## Review Process

### Before Review

- [ ] All checks pass locally (`./scripts/validate.sh`)
- [ ] Tests written and passing (80%+ coverage)
- [ ] No debugging code left in
- [ ] Docstrings added to new functions/classes
- [ ] Commit messages follow conventions

### Reviewer Checklist

- [ ] Code follows CLAUDE.md patterns
- [ ] Tests are comprehensive
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] No security issues

### Feedback & Iteration

1. **Fix issues** raised by reviewers
2. **Push new commits** (don't force-push)
3. **Re-request review** when ready
4. Repeat until approved

## Project Structure Reference

```
docs/                          # This documentation
├── index.md                   # Documentation home
├── ARCHITECTURE.md            # System design
├── API.md                     # REST API docs
├── DATABASE.md                # Database schema
├── DEPLOYMENT.md              # Deployment guide
├── TESTING.md                 # Testing guide
├── TROUBLESHOOTING.md         # Common issues
├── CONTRIBUTING.md            # This file
└── guides/
    ├── adding-new-feature.md
    ├── debugging.md
```

## Common Tasks

### Adding a New Feature

See [Adding a New Feature Guide](guides/adding-new-feature.md)

```bash
# 1. Create new app
./scripts/create_app.sh myfeature

# 2. Define models
# Edit apps/myfeature/models/<model-name>.py

# 3. Create serializers
# Edit apps/myfeature/serializers/<model-name>_serializers.py (input + output)

# 4. Create viewset
# Edit apps/myfeature/views/<model-name>_views.py

# 5. Register in admin
# Edit apps/myfeature/admin/<model-name>_admin.py

# 6. Add tests
# Add to apps/myfeature/tests/

# 7. Run validation
./scripts/validate.sh
```

### Fixing a Bug

1. Write a failing test that reproduces the bug
2. Fix the code to make the test pass
3. Verify all tests still pass
4. Commit with `fix:` type

### Updating Documentation

1. Make changes to relevant `.md` files
2. Update links if moving/renaming files
3. Verify documentation builds correctly
4. Commit with `docs:` type

## Issues & Discussion

### Reporting Bugs

Create an issue with:
- **Description**: What's the bug?
- **Steps to reproduce**: How to trigger it?
- **Expected behavior**: What should happen?
- **Actual behavior**: What actually happens?
- **Environment**: Python version, OS, etc.

### Suggesting Features

Create an issue with:
- **Description**: What feature to add?
- **Use case**: Why is this needed?
- **Proposed solution**: How to implement?
- **Alternatives considered**: Other approaches?

## Development Tips

### Using Graphify for Navigation

Query the codebase graph instead of raw grepping:

```bash
# Smart code discovery
graphify query "where is caching configured"

# Find relationships
graphify path "BaseViewSet" "CustomAutoSchema"

# Explore concepts
graphify explain "input/output serializer pattern"
```

### Debugging

See [Debugging Guide](guides/debugging.md)

```bash
# Use Django shell
python manage.py shell

# Use Python debugger
import pdb; pdb.set_trace()

# Use pytest with output
pytest -vvs apps/myapp/tests/test_views.py::test_name
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

---

Thank you for contributing! Your work helps make {{ cookiecutter.project_name }} better. 🙏
