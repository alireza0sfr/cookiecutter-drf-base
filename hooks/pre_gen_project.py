#!/usr/bin/env python
"""Pre-generation hooks for cookiecutter-drf-base."""

import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
REPO_MODULE_REGEX = r"^[-a-zA-Z][-a-zA-Z0-9]+$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

module_name = "{{ cookiecutter.__project_slug }}"
repo_name = "{{ cookiecutter.repo_name }}"
author_email = "{{ cookiecutter.author_email }}"
primary_language = "{{ cookiecutter.primary_language }}"
supported_languages = "{{ cookiecutter.supported_languages }}"

# Validate module name
if not re.match(MODULE_REGEX, module_name):
    print(
        f"ERROR: Project slug '{module_name}' is not a valid Python module name. "
        "Use only letters, numbers, and underscores (starting with letter or underscore)."
    )
    sys.exit(1)

# Validate repository name
if not re.match(REPO_MODULE_REGEX, repo_name):
    print(
        f"ERROR: Repository name '{repo_name}' is not valid. "
        "Use only letters, numbers, and hyphens (starting with letter)."
    )
    sys.exit(1)

# Validate email format
if author_email and not re.match(EMAIL_REGEX, author_email):
    print(
        f"ERROR: Email '{author_email}' is not a valid email address."
    )
    sys.exit(1)

# Validate language codes
valid_lang_codes = primary_language.split(",")
supported_lang_codes = [lang.strip() for lang in supported_languages.split(",")]

for lang in valid_lang_codes:
    if len(lang.strip()) != 2:
        print(f"WARNING: Language code '{lang}' should be 2 characters (e.g., 'en', 'fa')")

# Ensure primary language is in supported languages
if primary_language not in supported_lang_codes:
    print(
        f"WARNING: Primary language '{primary_language}' not in supported languages. "
        f"Adding it to the list."
    )
    supported_lang_codes.append(primary_language)

print("✓ Project configuration is valid")
print(f"  Module: {module_name}")
print(f"  Repository: {repo_name}")
print(f"  Primary Language: {primary_language}")
print(f"  Supported Languages: {', '.join(supported_lang_codes)}")
