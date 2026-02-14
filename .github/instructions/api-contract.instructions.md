---
applyTo: "{backend/src/api/**/*.py,frontend/src/api/**/*.ts,shared/schemas/**/*.json}"
---
# API Contract & Communication Instructions


This document defines the standards for communication between the Python backend and the TypeScript frontend.

## 📁 Relevant Paths
- `src/backend/api/`: FastAPI/Flask routes and Pydantic models.
- `src/frontend/src/api/`: API client and type definitions.

## 📏 Contract Standards
- **Schema Naming:**
  - **Python (Pydantic):** `snake_case` (e.g., `user_query`).
  - **TypeScript:** `camelCase` (e.g., `userQuery`).
  - **Conversion:** Use a middleware or helper to automatically convert cases between Backend and Frontend.
- **Response Format:**
  - Success: `{ "status": "success", "data": { ... } }`
  - Error: `{ "status": "error", "message": "Human readable message", "code": "ERROR_CODE" }`
- **HTTP Methods:**
  - `GET`: Fetch data.
  - `POST`: Create/Trigger complex actions (like queries).
  - `DELETE`: Remove pages/indices.

## 🛠 Tooling & Validation
- **Pydantic:** Use Pydantic for all request/response validation in Python.
- **Zod:** Recommended for frontend schema validation to match API types.
- **CORS:** Strictly define allowed origins in the backend config (use environment variables).

## 🚀 Syncing
- If the backend schema changes, update the corresponding TypeScript interfaces/types immediately.
- Use a `shared/` directory or a code-generation tool if the project grows to avoid manual type duplication.
