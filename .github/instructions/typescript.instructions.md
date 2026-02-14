---
applyTo: "{frontend/**/*.{ts,tsx},e2e/**/*.spec.ts}"
excludeAgent: ["python-engineer"]
---
# TypeScript/React Development Instructions

This document provides path-specific instructions for frontend development in the `rag-cosense` project. These instructions apply when working on the React UI, hooks, or E2E tests.

## 📁 Relevant Paths
- `frontend/src/**/*.{ts,tsx}`: Frontend components and logic.
- `frontend/tests/**/*.{ts,tsx}`: Frontend unit and component tests.
- `e2e/**/*.spec.ts`: Playwright end-to-end tests.
- `frontend/package.json`: Dependency and script configuration.


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
  - Test Files: `*.test.ts/tsx` or `*.spec.ts` (for E2E)
- **Strict Typing:** Avoid `any`. Use interfaces for component props and data structures. Use `tsc` for validation.
- **Accessibility:** Ensure ARIA labels are used for interactive elements.
- **Environment Variables:** Must be prefixed with `VITE_` to be accessible in the frontend.
- **Styles:** Use Tailwind CSS utility classes. Avoid custom CSS files unless necessary.
- **Testing:** Use `Vitest` and `React Testing Library`. Follow the AAA pattern.

## 🏗 Build & Validation Flow
Before submitting frontend changes, follow this sequence:
1. **Bootstrap:** `npm install`
2. **Lint:** `npm run lint`
3. **Type Check:** `npm run type-check`
4. **Test:** `npm run test`
5. **Coverage:** `npm run test:coverage`

## 🚀 Common Commands
- **Dev Server:** `npm run dev`
- **E2E Tests:** `npx playwright test`
- **E2E Debug:** `npx playwright test --debug`
- **Format:** `npm run format`
- **Generate API Docs:** `npm run docs:generate`


