.PHONY: help setup up down restart logs ps build health

# Default target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup    Copy .env.example to .env"
	@echo "  up       Start all containers in background"
	@echo "  down     Stop and remove all containers"
	@echo "  restart  Restart all containers"
	@echo "  logs     Show logs from all containers"
	@echo "  ps       List running containers"
	@echo "  build    Build or rebuild services"
	@echo "  health   Check backend health endpoint"

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created from .env.example"; \
	else \
		echo ".env already exists"; \
	fi

up:
	docker compose up -d

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
