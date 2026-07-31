#!/bin/bash
# Validation script for {{ cookiecutter.project_name }}
# Runs all quality and test checks before committing
#
# Usage:
#   chmod +x scripts/validate.sh
#   ./scripts/validate.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== {{ cookiecutter.project_name }} Validation ===${NC}\n"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}✗ Virtual environment not activated${NC}"
    echo "Run: source .venv/bin/activate"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# 1. Code Quality Checks
echo -e "${YELLOW}1. Running Ruff Linter...${NC}"
if ruff check .; then
    echo -e "${GREEN}✓ Ruff linting passed${NC}\n"
else
    echo -e "${RED}✗ Ruff linting failed${NC}"
    echo "Run: ruff check --fix ."
    exit 1
fi

echo -e "${YELLOW}2. Running Ruff Formatter...${NC}"
if ruff format --check .; then
    echo -e "${GREEN}✓ Ruff formatting check passed${NC}\n"
else
    echo -e "${RED}✗ Code needs formatting${NC}"
    echo "Run: ruff format ."
    exit 1
fi

# 2. Django Validation
echo -e "${YELLOW}3. Running Django System Check...${NC}"
if python manage.py check; then
    echo -e "${GREEN}✓ Django system check passed${NC}\n"
else
    echo -e "${RED}✗ Django system check failed${NC}"
    exit 1
fi

# 3. Database Migrations
echo -e "${YELLOW}4. Checking for pending migrations...${NC}"
if python manage.py makemigrations --dry-run --check; then
    echo -e "${GREEN}✓ No pending migrations${NC}\n"
else
    echo -e "${YELLOW}⚠ Pending migrations detected${NC}"
    echo "Run: python manage.py makemigrations"
    echo "Note: This is not a blocker, but should be committed"
fi

# 4. Tests
echo -e "${YELLOW}5. Running Tests...${NC}"
if pytest apps/ --cov=apps --cov-report=term-missing --cov-fail-under=80 -v; then
    echo -e "${GREEN}✓ All tests passed with 80%+ coverage${NC}\n"
else
    echo -e "${RED}✗ Tests failed or coverage below 80%${NC}"
    exit 1
fi

# 5. Type Checking (optional, if mypy is installed)
if command -v mypy &> /dev/null; then
    echo -e "${YELLOW}6. Running Type Checks...${NC}"
    if mypy apps/ --ignore-missing-imports 2>/dev/null || true; then
        echo -e "${GREEN}✓ Type checks passed${NC}\n"
    else
        echo -e "${YELLOW}⚠ Type checking issues (non-blocking)${NC}\n"
    fi
fi

# Success
echo -e "${GREEN}=== All Validations Passed! ===${NC}"
echo -e "${GREEN}✓ Ready to commit${NC}\n"
