# rag-cosense

A Retrieval-Augmented Generation (RAG) system for Cosense (Scrapbox) data. This project provides a way to query your Cosense knowledge base using LLMs through a modern interface. It uses hybrid search (sparse vectors via SPLADE) and local LLMs for privacy-conscious interaction.

## 🚀 Features

- **Cosense (Scrapbox) Integration**: Automatically fetches and indexes pages from your Cosense projects.
- **Sparse Vector Search**: Uses SPLADE (encoder service) for high-quality retrieval based on semantic importance.
- **Elasticsearch Support**: Leverages Elasticsearch for efficient storage and ranking of sparse/text data.
- **Local LLM**: Integrated with [Ollama](https://ollama.com/) (Gemma 3) for private and secure document-based answering.
- **Docker Ready**: Full containerization for all services (Backend, Encoder, Elasticsearch, Ollama).
- **AI Agent-Driven Development**: Specialized instructions for various engineering roles.

## 🛠 Tech Stack

### Services & Infrastructure
- **API (Backend)**: FastAPI (Python 3.12+)
- **Encoder**: SPLADE (Transformers + PyTorch)
- **Vector Database**: Elasticsearch 8.12+
- **LLM Runner**: Ollama (Gemma 3)
- **Orchestration**: Docker Compose

### Tools
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **AI Framework**: LangChain
- **Analysis**: Ruff (Linter/Formatter), Mypy (Type Check), Pytest

## 🔧 Setup & Development

### Prerequisites
- Docker & Docker Compose
- `make` (Optional but recommended)
- `uv` (For local backend development)

### Initial Setup

1. **Environment Configuration**:
   ```bash
   make setup
   ```
   Edit the generated `.env` file and provide your `COSENSE_PROJECT_NAME` and `COSENSE_SID` (Found in your browser cookies as `connect.sid`).

2. **Start Services**:
   ```bash
   make up
   ```
   This will start the Backend, Encoder, Elasticsearch, and Ollama containers.

3. **Initialize LLM**:
   After starting the services, you need to pull the Gemma 3 model in Ollama:
   ```bash
   docker compose exec ollama ollama pull gemma3
   ```

### Running the Application

The services will be available at:
- **Backend API**: `http://localhost:8000`
- **Encoder API**: `http://localhost:8001`
- **Elasticsearch**: `http://localhost:9200`
- **Ollama**: `http://localhost:11434`

To sync your Cosense data:
```bash
curl -X POST http://localhost:8000/api/v1/index/sync
```

## ✅ Validation

### Local Development (Backend)
```bash
cd backend
uv sync
uv run ruff check .
uv run mypy .
uv run pytest
```

### Build & Infrastructure
```bash
make health  # Check if backend is alive
make ps      # List running services
make logs    # View service logs
```

## 📁 Project Structure

```text
rag-cosense/
├── backend/         # FastAPI service, RAG logic & indexing
│   ├── src/         # Source code
│   └── tests/       # Unit & integration tests
├── encoder/         # SPLADE service for sparse vectors
├── compose.yml      # Docker Compose configuration
├── Makefile         # Shortcuts for common commands
├── architecture.md  # Detailed system architecture
├── .env.example     # Environment variable template
└── README.md
```

## 🤖 AI Agents
This project uses specialized AI agents for development. Refer to [.github/copilot-instructions.md](.github/copilot-instructions.md) and [.github/agents/](.github/agents/) for more details.

This repository is optimized for AI-assisted development. Refer to the specialized personas in `.github/agents/`:
- **Python Engineer**: Backend & RAG logic.
- **Frontend Engineer**: UI & React development.
- **Test Engineer**: Quality assurance and automation.
- **Linter Engineer**: Code style and static analysis.
- **Infra Engineer**: Docker & Deployment.

## 📄 License

[MIT](LICENSE)
