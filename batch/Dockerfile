# Build stage
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml .
# Sync dependencies
RUN uv sync

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy virtual environment and source code
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/

# Ensure the app user can access the app files
RUN chown -R appuser:appuser /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

USER appuser

# Entry point is main.py
CMD ["python", "src/main.py"]
