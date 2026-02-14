---
applyTo: "{backend/src/ingestion/**/*.py,backend/src/vectorstore/**/*.py}"
---
# Data Management & RAG Strategy Instructions


This document defines standards for data processing, embedding, and vector store management.

## 📁 Relevant Paths
- `src/backend/ingestion/`: Scrapbox API fetching and parsing logic.
- `src/backend/vectorstore/`: ChromaDB management and retrieval logic.

## 📏 RAG Strategy
- **Chunking:**
  - Default: `RecursiveCharacterTextSplitter`.
  - Size: 500-1000 tokens (adjust based on Scrapbox page length).
  - Overlap: 10-20% to maintain context between chunks.
- **Preprocessing:**
  - Strip excessive whitespace.
  - Handle Scrapbox specific syntax (e.g., `[links]`, `[* bold]`)—either preserve for context or clean for clarity.

## 🧠 Embedding & Vector Store
- **Model:** `text-embedding-3-small` (OpenAI).
- **Vector Store:** ChromaDB.
- **Metadata Standards:** 
  - Every chunk MUST include: `source_url`, `page_title`, `project_name`, and `last_updated`.
- **Search Logic:** Use `similarity_search_with_score` or `Maximal Marginal Relevance (MMR)` to ensure diverse results.

## 🚀 Operations
- **Indexing:** Avoid re-indexing unchanged pages. Use hashes or `last_updated` timestamps to upsert.
- **Persistence:** Ensure DB files are stored in a persistent volume (defined in `compose.yml`).
