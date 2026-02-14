---
applyTo: "{compose.yml,Dockerfile,Dockerfile.*,docker/**/*.conf}"
---
# Docker & Container Orchestration Instructions

This document provides instructions for containerization and infrastructure management using Docker and Docker Compose in the `rag-cosense` project.

## 📁 Relevant Paths
- `compose.yml`: Main orchestration file for development and production.
- `Dockerfile`: Multi-stage build definitions for backend/frontend.
- `docker/`: Custom configuration files (e.g., Nginx, ChromaDB tweaks).

## 🛠 Tech Stack
- **Docker Engine:** 25.0+ recommended.
- **Docker Compose:** V2 (Preferred command: `docker compose`).
- **Base Images:** 
  - Python: `python:3.12-slim`
  - Frontend: `node:20-alpine` (building), `nginx:alpine` (serving).
- **Service Stack:** Backend (Python Agent), Frontend (React SPA), Vector Store (ChromaDB).

## 📏 Standards & Best Practices
- **Multi-stage Builds:** Always use multi-stage Dockerfiles to minimize image size and improve security.
- **Non-root Users:** Run processes as a non-privileged user inside containers.
- **Environment Variables:** Use `.env` file integration via `env_file` in `compose.yml`. Never hardcode secrets in Dockerfiles.
- **Volume Persistence:** Ensure data persistence for ChromaDB using named volumes (e.g., `chroma_data:/path/to/data`).
- **Health Checks:** Implement `healthcheck` in `compose.yml` for critical services like the vector store.
- **Networking:** Use a dedicated bridge network for internal communication between services.

## 🚀 Common Commands
- **Start All:** `docker compose up -d`
- **Rebuild & Start:** `docker compose up -d --build`
- **Stop & Remove:** `docker compose down`
- **View Logs:** `docker compose logs -f`
- **Inside Container:** `docker compose exec backend bash`

## ⚠️ Security
- Use `.dockerignore` to exclude `node_modules`, `__pycache__`, `.env`, and git history.
- Pin image versions (use `python:3.12-slim` instead of `python:latest`).
