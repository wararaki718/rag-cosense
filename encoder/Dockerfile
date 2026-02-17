# Build stage
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies if needed (fugashi might need it)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml .
# Sync dependencies
RUN uv sync --no-dev

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user with home directory
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Copy virtual environment and source code
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/

# Pre-download the model to the image (optional but recommended for speed and stability)
ENV PATH="/app/.venv/bin:$PATH" \
    HF_HOME="/app/.cache/huggingface"

RUN mkdir -p $HF_HOME && \
    python -c "from transformers import AutoTokenizer, AutoModelForMaskedLM; \
              model_id = 'aken12/splade-japanese-v3'; \
              AutoTokenizer.from_pretrained(model_id); \
              AutoModelForMaskedLM.from_pretrained(model_id)" && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8001
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
