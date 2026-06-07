# Frontend

Use this directory for frontend pathway notes by default. Generate a frontend only when the product needs a bundled JavaScript UI.

## Generate

```bash
make scaffold-frontend
```

This creates a Vite frontend only.

```bash
make scaffold-app
```

This creates a Vite frontend plus a FastAPI backend that can serve the built frontend.

Choose the smallest frontend that fits the product:

- No separate frontend build when FastAPI plus Jinja templates is enough.
- A bundled JavaScript SPA when the experience needs richer interaction, persistent client state, or framework-level tooling.

When using an SPA, build static assets that the FastAPI backend can serve for single-service deploys.

## Build

```bash
npm install
npm run build
```

The build output goes to `frontend/dist`.
