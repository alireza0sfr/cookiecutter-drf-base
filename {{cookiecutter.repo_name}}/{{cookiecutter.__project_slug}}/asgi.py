"""
ASGI config for {{ cookiecutter.__project_slug }} project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.__project_slug }}.settings')

application = get_asgi_application()
