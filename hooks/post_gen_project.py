#!/usr/bin/env python
"""Post-generation hooks for cookiecutter-drf-base."""

import os
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command and report status."""
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        if description:
            print(f"✓ {description}")
    except subprocess.CalledProcessError as e:
        print(f"⚠ {description}: {e.stderr.decode() if e.stderr else str(e)}")

def setup_git():
    """Initialize git repository."""
    if not os.path.exists(".git"):
        run_command("git init", "Initialize git repository")
        run_command("git add .", "Stage initial files")
        run_command(
            'git commit -m "Initial commit from cookiecutter-drf-base"',
            "Create initial commit"
        )

def setup_venv():
    """Offer to create virtual environment."""
    print("\n📦 Virtual Environment")
    print("To activate the virtual environment after uv sync:")
    print("  source .venv/bin/activate  (macOS/Linux)")
    print("  .venv\\Scripts\\activate     (Windows)")

def cleanup_optional_files():
    """Remove files for unchecked optional features."""
    use_celery = "{{ cookiecutter.include_celery|lower }}" == "y"
    use_channels = "{{ cookiecutter.include_channels|lower }}" == "y"

    optional_dirs = {
        "apps/celery": use_celery,
        "apps/channels": use_channels,
    }

    for dir_path, keep in optional_dirs.items():
        if not keep and os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"✓ Removed {dir_path} (not selected)")

def create_env_files():
    """Create environment files from templates."""
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("""# Django Settings
DEBUG=True
ENVIRONMENT=development
SECRET_KEY={{ cookiecutter.secret_key }}
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://{{ cookiecutter.postgres_user }}:{{ cookiecutter.postgres_password }}@{{ cookiecutter.postgres_host }}:{{ cookiecutter.postgres_port }}/{{ cookiecutter.postgres_db }}

# Redis
REDIS_HOST={{ cookiecutter.redis_host }}
REDIS_PORT={{ cookiecutter.redis_port }}

# Language
LANGUAGE_CODE={{ cookiecutter.primary_language }}
USE_I18N=True

# Admin
ADMIN_USERNAME={{ cookiecutter.default_user_username }}
ADMIN_PASSWORD={{ cookiecutter.default_user_password }}
ADMIN_EMAIL={{ cookiecutter.default_user_email }}
""")
        print("✓ Created .env file")

def print_next_steps():
    """Print next steps after project generation."""
    print("\n" + "=" * 60)
    print("🎉 Project '{{ cookiecutter.project_name }}' created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("\n1. Install dependencies:")
    print("   uv sync --all-groups")
    print("\n2. Activate virtual environment:")
    print("   source .venv/bin/activate")
    print("\n3. Run migrations:")
    print("   python manage.py migrate")
    print("\n4. Create superuser:")
    print("   python manage.py createsuperuser")
    print("\n5. Start development server:")
    print("   python manage.py runserver")
    print("\n6. Access the application:")
    print("   - API: http://localhost:8000/api/")
    print("   - Schema: http://localhost:8000/api/schema/")
    print("   - Admin: http://localhost:8000/admin/")
    print("\nDocumentation:")
    print("   See docs/README.md for full documentation")
    print("   See .claude/CLAUDE.md for coding standards")
    print("=" * 60)

# Main execution
if __name__ == "__main__":
    print("\n🚀 Setting up {{ cookiecutter.project_name }}...\n")

    cleanup_optional_files()
    create_env_files()
    setup_git()
    setup_venv()
    print_next_steps()
