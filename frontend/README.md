# Frontend

Use this directory for the app UI.

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
