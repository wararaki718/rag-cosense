# rag-cosense

[English](#english) | [日本語](#日本語)

---

<a name="english"></a>
# rag-cosense (English)

A Retrieval-Augmented Generation (RAG) system for [Cosense](https://cosen.se/) (formerly Scrapbox) data. This project provides an AI-powered interface to query and interact with your personal or team knowledge bases.

## 🚀 Features

- **Cosense Integration**: Standalone batch process to fetch and index pages from your Cosense projects.
- **Hybrid Search**: Leverages SPLADE (sparse vectors) for high-quality semantic retrieval.
- **Local LLM**: Integrated with [Ollama](https://ollama.com/) (Gemma 3) for privacy-conscious, local inference.
- **Containerized Architecture**: Full development environment using Docker Compose.
- **Quality Focused**: Comprehensive linting (Ruff, Mypy, ESLint), type checking, and testing (Pytest, Vitest).

## 🛠 Tech Stack

- **Backend**: FastAPI (Python 3.12+), LangChain
- **Frontend**: React (Lucide Icons, Tailwind CSS)
- **Batch**: Python synchronization logic
- **Encoder**: SPLADE Service (PyTorch + Transformers)
- **Vector Database**: Elasticsearch 8.12
- **LLM Runner**: Ollama (Gemma 3)
- **Package Management**: [uv](https://github.com/astral-sh/uv) (Python), npm (Frontend)

## 🔧 Setup & Development

### Prerequisites
- Docker & Docker Compose
- `make`
- `uv` (For local Python development)

### Initial Setup

1.  **Configure Environment**:
    ```bash
    make setup
    ```
    Edit `.env` and provide your `COSENSE_PROJECT_NAME` and `COSENSE_SID`.

2.  **Start Services**:
    ```bash
    make up
    ```

3.  **Pull LLM Model**:
    ```bash
    docker compose exec ollama ollama pull gemma3
    ```

4.  **Synchronize Data**:
    ```bash
    make sync
    ```

### Service Access
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Elasticsearch**: [http://localhost:9200](http://localhost:9200)

## ✅ Validation & Testing

Run the following commands to ensure everything is working correctly:

```bash
make lint  # Linters and type checks
make test  # Run all tests
make health # Check Backend API health
```

---

<a name="日本語"></a>
# rag-cosense (日本語)

[Cosense](https://cosen.se/) (旧 Scrapbox) のデータを使用した RAG (Retrieval-Augmented Generation) システムです。個人やチームのナレッジベースに対して、AI を使用した自然言語での問い合わせを可能にします。

## 🚀 主な機能

- **Cosense 統合**: Cosense プロジェクトからページを取得し、自動的にインデックスを作成。
- **ハイブリッド検索**: SPLADE (スパースベクトル) を使用した高精度なセマンティック検索。
- **ローカル LLM**: [Ollama](https://ollama.com/) (Gemma 3) を活用し、プライバシーに配慮したローカル環境での推論を実現。
- **コンテナ化**: Docker Compose による一貫した開発・実行環境。
- **品質管理**: Ruff, Mypy, ESLint による静的解析と、Pytest, Vitest によるテスト。

## 🛠 技術スタック

- **Backend**: FastAPI (Python 3.12+), LangChain
- **Frontend**: React, Vite, Tailwind CSS
- **Batch**: Python (データ同期ロジック)
- **Encoder**: SPLADE サービス (PyTorch + Transformers)
- **Vector Database**: Elasticsearch 8.12
- **LLM Runner**: Ollama (Gemma 3)
- **パッケージ管理**: [uv](https://github.com/astral-sh/uv) (Python), npm (Frontend)

## 🔧 セットアップと開発

### 1. 環境設定
```bash
make setup
```
作成された `.env` ファイルに `COSENSE_PROJECT_NAME` と `COSENSE_SID` を設定してください。

### 2. サービスの起動
```bash
make up
```

### 3. LLM モデルの準備
```bash
docker compose exec ollama ollama pull gemma3
```

### 4. データの同期
```bash
make sync
```

## 📁 Project Structure

```text
rag-cosense/
├── backend/         # FastAPI service & RAG logic
├── batch/           # Synchronization (Cosense -> Elasticsearch)
├── frontend/        # React-based chat interface
├── encoder/         # SPLADE service for vectors
├── compose.yml      # Docker orchestration
├── Makefile         # Command shortcuts
└── architecture.md  # System architecture details
```

## 🤖 AI-Agent Friendly

This repository is optimized for AI-assisted development with specialized personas:
- **Python Engineer**: Backend & RAG logic.
- **Frontend Engineer**: UI & React development.
- **Test Engineer**: Quality assurance and automation.

Refer to [.github/copilot-instructions.md](.github/copilot-instructions.md) for global rules.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
