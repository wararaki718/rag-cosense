---
applyTo: "{backend/**/*.py,*.py}"
excludeAgent: ["frontend-engineer"]
---
# Python Development Instructions

This document provides path-specific instructions for Python development in the `rag-cosense` project. These instructions apply when working on backend logic, RAG pipelines, or tests.

## 📁 Relevant Paths
- `backend/src/**/*.py`: Core backend and RAG logic.
- `backend/tests/**/*.py`: Unit and integration tests.
- `backend/pyproject.toml`: Dependency and tool configuration.


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
  - Test Files: `test_*.py`
  - Test Functions: `test_should_*(...args)`
- **Type Safety:** Mandatory type hints for all function signatures and public members. Always use static type checking.
- **Documentation:** Use Google-style docstrings for all modules, classes, and functions.
- **Error Handling:** Use specific exception types and provide meaningful error messages.
- **Secrets:** Never hardcode API keys. Use `.env` and access via `os.getenv`.
- **Testing:** Use `pytest` with the AAA (Arrange, Act, Assert) pattern. Isolate external dependencies using `unittest.mock` or `pytest-mock`.

## 🏗 Build & Validation Flow
Before submitting backend changes, follow this sequence:
1. **Bootstrap:** `uv sync`
2. **Lint & Fix:** `uv run ruff check --fix .`
3. **Format:** `uv run ruff format .`
4. **Type Check:** `uv run mypy .`
5. **Test:** `uv run pytest`
6. **Coverage:** `uv run pytest --cov=src --cov-report=term-missing`

## 🚀 Common Commands
- **Run Agent:** `uv run agent.py`
- **Install Package:** `uv add <package>`
- **Generate API Docs:** `uv run pdoc src/ -o docs/api`

