---
applyTo: "{src/frontend/**/*.{ts,tsx},e2e/**/*.spec.ts}"
excludeAgent: ["python-engineer"]
---
# TypeScript/React Development Instructions

This document provides path-specific instructions for frontend development in the `rag-cosense` project. These instructions apply when working on the React UI, hooks, or E2E tests.

## 📁 Relevant Paths
- `src/frontend/**/*.{ts,tsx}`: Frontend components and logic.
- `e2e/**/*.spec.ts`: Playwright end-to-end tests.
- `package.json`: Dependency and script configuration.

## 🛠 Tech Stack
- **Framework:** React with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Package Manager:** `npm`
- **Quality Tools:** `ESLint`, `Prettier`, `Vitest` (unit), `Playwright` (E2E)

## 📏 Coding Standards
- **Naming Conventions:**
  - Components/Types/Interfaces: `PascalCase`
  - Hooks: `useCamelCase` (prefixed with `use`)
  - Functions/Variables: `camelCase`
  - Constants: `UPPER_SNAKE_CASE`
- **Strict Typing:** Avoid `any`. Use interfaces for component props and data structures.
- **Accessibility:** Ensure ARIA labels are used for interactive elements.
- **Environment Variables:** Must be prefixed with `VITE_` to be accessible in the frontend.
- **Styles:** Use Tailwind CSS utility classes. Avoid custom CSS files unless necessary.

## 🚀 Common Commands
- **Install:** `npm install`
- **Dev Server:** `npm run dev`
- **Lint:** `npm run lint`
- **Type Check:** `npm run type-check`
- **Run Unit Tests:** `npm run test`
- **Run E2E Tests:** `npx playwright test`
