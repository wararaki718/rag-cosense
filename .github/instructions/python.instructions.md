---
applyTo: "{src/backend/**/*.py,tests/**/*.py,*.py}"
excludeAgent: ["frontend-engineer"]
---
# Python Development Instructions

This document provides path-specific instructions for Python development in the `rag-cosense` project. These instructions apply when working on backend logic, RAG pipelines, or tests.

## 📁 Relevant Paths
- `src/backend/**/*.py`: Core backend and RAG logic.
- `tests/**/*.py`: Unit and integration tests.
- `pyproject.toml`: Dependency and tool configuration.

## 🛠 Tech Stack
- **Runtime:** Python 3.12+
- **Package Manager:** `uv` (Always use `uv run`, `uv sync`, etc.)
- **Main Libraries:** `langchain`, `langchain-openai`, `chromadb`, `httpx`
- **Quality Tools:** `ruff` (formatting/linting), `mypy` (type checking), `pytest` (testing)

## 📏 Coding Standards
- **Naming Conventions:**
  - Classes: `PascalCase`
  - Functions/Methods/Variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
- **Type Safety:** Mandatory type hints for all function signatures and public members.
- **Documentation:** Use Google-style or ReST docstrings for all modules, classes, and functions.
- **Error Handling:** Use specific exception types and provide meaningful error messages.
- **Secrets:** Never hardcode API keys. Use `python-dotenv` and access via `os.getenv`.

## 🚀 Common Commands
- **Install:** `uv sync`
- **Lint/Fix:** `uv run ruff check --fix .`
- **Format:** `uv run ruff format .`
- **Type Check:** `uv run mypy .`
- **Run Tests:** `uv run pytest`
- **Run Agent:** `uv run agent.py`
