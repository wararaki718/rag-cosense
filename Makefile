.PHONY: help setup up down restart logs ps build health sync lint test

# Default target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup    Copy .env.example to .env"
	@echo "  up       Start all containers in background"
	@echo "  sync     Run batch synchronization (manual)"
	@echo "  down     Stop and remove all containers"
	@echo "  restart  Restart all containers"
	@echo "  logs     Show logs from all containers"
	@echo "  ps       List running containers"
	@echo "  build    Build or rebuild services"
	@echo "  health   Check backend health endpoint"
	@echo "  lint     Run linting and type checking for all components"
	@echo "  test     Run unit tests for all components"

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created from .env.example"; \
	else \
		echo ".env already exists"; \
	fi

up:
	docker compose up -d

sync:
	docker compose --profile manual run --rm batch

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

build:
	docker compose build

health:
	curl http://localhost:8000/api/v1/health

lint:
	cd backend && uv run ruff check . && uv run mypy .
	cd batch && uv run ruff check . && uv run mypy .
	cd encoder && uv run ruff check . && uv run mypy .
	cd frontend && npm run lint && npm run type-check

test:
	cd backend && uv run pytest
	cd batch && uv run pytest
	cd encoder && uv run pytest
	cd frontend && npm test -- --run
