# Cloud Builder Stack

A public, open-source starter repo for workshops, tutorials, hackathons, and live builder sessions using practical AI/cloud tools.

The goal is to keep one clean reference place for:

- what each tool is good for
- where it fits in a builder workflow
- which secrets and configuration values a team should prepare
- how to avoid committing credentials during demos

## Tool Catalog

| Tool | Best used for | Builder-session fit | Notes |
| --- | --- | --- | --- |
| [Tavily](https://docs.tavily.com/) | Web search and retrieval for AI apps, RAG demos, source-grounded agents, research workflows | Add real-time web context to agent demos, research assistants, market scanners, and tutorial apps | Tavily Search is an API optimized for LLM consumption, with search depth controls and bearer-token authentication. |
| [n8n](https://docs.n8n.io/) | Low-code workflow automation, AI workflow orchestration, API glue, webhook demos | Build visual automation flows live, connect SaaS APIs, trigger AI steps, prototype ops workflows | n8n can run in Cloud or self-hosted modes; self-hosting exposes many environment-variable controls. |
| [Gradium](https://gradium.ai/) | Voice AI, speech-to-text, text-to-speech, voice cloning, low-latency voice interactions | Add voice interfaces to agent demos, education apps, customer-support prototypes, and interactive sessions | Gradium positions itself around audio language models for natural, expressive, low-latency voice interactions. |
| [Base44](https://docs.base44.com/) | AI-assisted website and app building from prompts, fast prototypes, app publishing | Let non-specialist builders turn ideas into working apps quickly, then discuss product flow, UX, auth, data, and integrations | Base44 handles app design, databases, signups, permissions, and hosting behind the scenes. |
| [Nebius AI Cloud](https://docs.nebius.com/) | GPU cloud infrastructure, model hosting, Kubernetes, object storage, MLflow, AI workloads | Run GPU-backed workshops, deploy models, host containers, store datasets/artifacts, and show production-style AI infrastructure | Nebius focuses on AI cloud infrastructure, including NVIDIA GPU VMs, GPU clusters, Kubernetes, object storage, and serverless AI jobs. |

## Quick Builder App Pattern

Cloud Builder Stack apps should be planned as small deployable products, even when the first version is only for a workshop or hackathon.

- Keep `backend/` and `frontend/` as top-level pathway directories with README files by default.
- Generate backend and frontend code only when the session needs it.
- Use FastAPI as the default generated backend for routing, API endpoints, webhooks, auth callbacks, server-side secrets, and static frontend serving.
- Use Jinja templates from the backend when the UI is small, mostly form-driven, or does not need a bundled JavaScript app.
- Use a bundled JavaScript frontend when the UI is an SPA, has richer client state, or benefits from a framework build step.
- Serve the frontend through FastAPI for simple single-service deploys: either render Jinja views directly or mount the built SPA assets as static files.
- Keep provider keys and private integration logic in the backend. Do not expose tool API keys in browser code.
- Plan for deployability from the start on starter-friendly platforms such as Render, Railway, or Vercel, while checking current plan limits before a public session.

### On-Demand Scaffolds

The repository does not commit frontend or backend boilerplate by default. Use `make` to generate only the shape needed for the current builder session.

```bash
make scaffold-backend
```

Generates a small FastAPI plus Jinja app.

```bash
make scaffold-frontend
```

Generates a Vite frontend only.

```bash
make scaffold-app
```

Generates FastAPI plus a Vite frontend served through the backend after build.

The generic form is also available:

```bash
make init PATHWAY=fastapi-jinja
make init PATHWAY=fastapi-vite
```

Scaffold commands refuse to overwrite existing generated files. If you intend to replace generated boilerplate, run the same command with `FORCE=1`.

### Generated Project Shapes

Default checkout:

```text
.
├── backend/
│   └── README.md
├── frontend/
│   └── README.md
├── scripts/
│   └── scaffold.py
├── README.md
├── .env.example
├── .gitignore
├── LICENSE
└── Makefile
```

`make scaffold-app` generates:

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── templates/
│   │       └── index.html
│   ├── requirements-dev.txt
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── scripts/
│   └── scaffold.py
├── README.md
├── .env.example
├── .gitignore
├── LICENSE
└── Makefile
```

### Planning Heuristics

- Choose a pathway, not the whole stack. A short session should prove one useful workflow with the fewest moving parts.
- Choose Jinja when the main workflow is a few pages, forms, server-rendered results, admin views, or internal tools.
- Choose an SPA when the app needs rich interaction, persistent client state, complex editing, dashboards, maps, voice interfaces, or multi-step user flows.
- Keep integrations thin at first: one route, one service module, one environment variable group, and one visible user path.
- For simple UI apps that call LLM adapters or cloud REST APIs, stick to install, build, and serve commands. Do not add Docker unless isolation is part of the lesson or deployment constraint.
- Add n8n when orchestration needs to be inspectable, event-driven, or editable by non-developers.
- Add Tavily when the app needs source-grounded web context.
- Add Gradium when voice is part of the primary interaction, not just a novelty.
- Add Nebius when the demo needs GPU infrastructure, model hosting, object storage, or production-style AI workloads.
- Add Base44 when the fastest path is a prompt-built application shell or when non-specialist builders need to own the UI quickly.

### Pathway Examples

| Session shape | Minimal pathway | Avoid until needed |
| --- | --- | --- |
| Simple LLM or cloud API app | FastAPI route, one service module, Jinja or SPA frontend, `make setup`, `make build`, `make serve` | Docker, queues, databases, n8n |
| Source-grounded assistant | FastAPI, Tavily service module, minimal UI, citation display | GPU hosting, workflow engine, auth |
| Visual automation demo | n8n workflow plus a small FastAPI webhook or result viewer | Custom orchestration code, Kubernetes |
| Voice-first prototype | FastAPI, Gradium integration, compact UI for controls/transcripts | Voice as an optional add-on to an unrelated app |
| Cloud infrastructure lesson | Nebius resource setup, one deployable workload, clear teardown notes | Unused services or multi-cloud abstractions |

## Local Setup

Generate the pathway needed for your demo, then install dependencies and run it.

For a small server-rendered app:

```bash
make scaffold-backend
make setup-backend
make serve
```

For a backend plus Vite app:

```bash
make scaffold-app
make setup
make build
make serve
```

Open `http://localhost:8000`.

For the generated FastAPI plus Vite pathway, the frontend build writes static assets to `frontend/dist`. The FastAPI app serves that directory when it exists, so the same backend process can serve API routes and the SPA on platforms that expect one web service.

## Deploy Shape

After generating the FastAPI plus Vite pathway, use the same build and serve sequence for simple deployments:

```bash
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build && cd ..
uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

For the FastAPI plus Jinja pathway, skip the frontend install and build command.

For split deployments, host the built frontend separately and keep FastAPI as the API backend. For single-service free-tier deploys, build the frontend during deploy and run the FastAPI serve command.

## Performance Defaults

The stack should stay easy to teach, but a few Rust-backed or speed-focused defaults are worth using:

- Use `uv` when available for faster Python environment and dependency installs; keep `pip` commands documented as the universal fallback.
- Use `ruff` for Python linting and formatting because it is fast enough to run during live builder sessions.
- Use FastAPI with Pydantic v2 and `ORJSONResponse` for quick request validation and JSON responses.
- Use Vite for frontend development and production builds.
- Keep expensive provider calls behind backend routes so responses can be cached, streamed, queued, or rate-limited without changing frontend code.

## Repository Layout

```text
.
├── README.md
├── .env.example
├── .gitignore
├── LICENSE
├── Makefile
├── scripts/
│   └── scaffold.py
├── backend/
│   └── README.md
└── frontend/
    └── README.md
```

## Environment Setup

1. Copy `.env.example` to `.env`.
2. Fill only the keys needed for your current demo.
3. Never commit `.env`, private keys, service-account files, exported n8n credentials, or workshop attendee data.
4. Use separate dev, staging, and production credentials for serious deployments.

```bash
cp .env.example .env
```

## Secret-Handling Practices

- Keep `.env.example` safe to publish: placeholders only, no real secrets.
- Prefer provider dashboards or secret managers for production secrets.
- Rotate any key that appears in a livestream, screenshot, issue, commit, or shared slide.
- Use least-privilege API tokens for hackathons and workshops.
- Disable or expire workshop credentials after the event.
- For n8n, remember that workflow source control does not sync credential values; configure credentials per environment.
- For Base44, keep third-party API keys in backend functions, project secrets, or managed connectors rather than browser-exposed frontend code.

## Source Notes

This repo summarizes vendor documentation and public product information as of 2026-05-31.

- Tavily Search API docs: https://docs.tavily.com/documentation/api-reference/endpoint/search
- n8n docs: https://docs.n8n.io/
- n8n environment variables: https://docs.n8n.io/hosting/configuration/environment-variables/
- Base44 getting started docs: https://docs.base44.com/Getting-Started/Quick-start-guide
- Base44 developer platform docs: https://docs.base44.com/developers/home
- Nebius AI Cloud docs: https://docs.nebius.com/
- Gradium homepage and launch information: https://gradium.ai/
- FastAPI docs: https://fastapi.tiangolo.com/
- FastAPI static files docs: https://fastapi.tiangolo.com/tutorial/static-files/
- Jinja templates docs: https://jinja.palletsprojects.com/
- uv docs: https://docs.astral.sh/uv/
- Ruff docs: https://docs.astral.sh/ruff/
- orjson docs: https://github.com/ijl/orjson
- Vite docs: https://vite.dev/
- Render free deploy docs: https://render.com/free
- Railway free trial docs: https://docs.railway.com/pricing/free-trial
- Vercel pricing docs: https://vercel.com/docs/pricing

## Contributing

Contributions are welcome. Good additions include:

- new workshop-ready AI/cloud tools
- example workshop flows
- `.env.example` improvements
- security notes for public demos
- tool comparison notes with official source links

Please avoid vendor hype. Keep descriptions practical, sourced, and useful for builders.
