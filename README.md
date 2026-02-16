# rag-cosense

A Retrieval-Augmented Generation (RAG) system for Cosense (Scrapbox) data. This project provides a way to query your Cosense knowledge base using LLMs through a modern interface. It uses hybrid search (sparse vectors via SPLADE) and local LLMs for privacy-conscious interaction.

## 🚀 Features

- **Cosense (Scrapbox) Integration**: Standalone batch process to fetch and index pages from your Cosense projects.
- **Sparse Vector Search**: Uses SPLADE (encoder service) for high-quality retrieval based on semantic importance.
- **Elasticsearch Support**: Leverages Elasticsearch for efficient storage and ranking of sparse/text data.
- **Local LLM**: Integrated with [Ollama](https://ollama.com/) (Gemma 3) for private and secure document-based answering.
- **Docker Ready**: Full containerization for all services (Backend, Batch, Encoder, Elasticsearch, Ollama).
- **AI Agent-Driven Development**: Specialized instructions for various engineering roles.

## 🛠 Tech Stack

### Services & Infrastructure
- **API (Backend)**: FastAPI (Python 3.12+)
- **Batch (Ingestion)**: Standalone Python 3.12+ script for data synchronization.
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
- `uv` (For local development)

### Initial Setup

1. **Environment Configuration**:
   ```bash
   make setup
   ```
   Edit the generated `.env` file and provide your `COSENSE_PROJECT_NAME` and `COSENSE_SID` (Found in your browser cookies as `connect.sid`).

2. **Start Infrastructure & API**:
   ```bash
   make up
   ```
   This will start the Backend, Frontend, Encoder, Elasticsearch, and Ollama containers.

3. **Initialize LLM**:
   After starting the services, you need to pull the Gemma 3 model in Ollama:
   ```bash
   docker compose exec ollama ollama pull gemma3
   ```

### 📥 Data Synchronization (Wait for LLM and Elasticsearch to be ready)

To fetch your data from Cosense and index it into Elasticsearch, run the manual batch sync:
```bash
make sync
```
This command runs a one-off `batch` container that processes your pages and then terminates.

### Running the Application

The services will be available at:
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **Encoder API**: `http://localhost:8001`
- **Elasticsearch**: `http://localhost:9200`
- **Ollama**: `http://localhost:11434`

## ✅ Validation

### Local Development (Backend/Batch)
```bash
cd backend # or cd batch
uv sync
uv run ruff check .
uv run mypy .
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
├── backend/         # FastAPI service & RAG logic
├── batch/           # Standalone synchronization script
├── frontend/        # React-based chat interface
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
