# Multi-stage build for {{ cookiecutter.project_name }}
# Stages: builder, development, production-base, staging, production

# Stage 1: Builder
FROM python:3.12-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY pyproject.toml uv.lock* ./
RUN pip install uv && uv pip install --system -e .

# Stage 2: Development
FROM python:3.12-slim as development

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBUG=True \
    ENVIRONMENT=development

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Stage 3: Production Base
FROM python:3.12-slim as production-base

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

USER appuser

EXPOSE 8000

# Stage 4: Staging
FROM production-base as staging

ENV DEBUG=True \
    ENVIRONMENT=staging

COPY deployment/docker/entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "{{ cookiecutter.__project_slug }}.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

# Stage 5: Production
FROM production-base as production

ENV DEBUG=False \
    ENVIRONMENT=production

COPY deployment/docker/entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "{{ cookiecutter.__project_slug }}.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-"]
