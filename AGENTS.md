# AGENTS.md

Guidance for coding agents working in this repository.

## Repository Intent

This is a public, open-source Cloud Builder Stack reference repo for workshops, tutorials, hackathons, and live builder sessions. Keep contributions practical, source-linked, and safe for public use.

## Working Practices

- Read the existing README and docs before adding new structure.
- Keep changes small, reviewable, and focused on the requested tool, workflow, or documentation update.
- Prefer official vendor documentation as sources for tool claims.
- Avoid hype language; describe what a tool is useful for and where it fits in a builder workflow.
- Do not commit secrets, real API keys, private service-account files, exported credentials, attendee data, or local `.env` files.
- Update `.env.example` when a new integration requires configuration.
- Keep `.env.example` publish-safe with placeholders only.
- Add or update source links when tool behavior, pricing, auth, hosting, or API details are mentioned.
- Treat anything under `~/forge` with extra care: do not delete, overwrite, reset, or clean files unless the human explicitly asks for that exact action.

## Minimal Builder Pathways

For small-scope projects, hackathons, and short builder sessions, do not use the full stack by default. Pick the smallest pathway that proves the idea and keeps setup teachable.

- Start from the user path: input, backend action, visible result, and deploy command.
- Default simple UI apps to FastAPI plus either Jinja or a built frontend served from `frontend/dist`.
- For apps that only call LLM adapters or cloud REST APIs, keep the workflow to install, build, and serve commands. A `Makefile` is enough.
- Do not add Docker, compose files, Kubernetes, queues, databases, object storage, or workflow engines unless the project clearly needs isolation, persistence, orchestration, background jobs, or shared infrastructure.
- Add one integration at a time. Each integration should have a clear route, environment variable group, source link, and demo path.
- Prefer direct backend service modules before introducing n8n. Use n8n when the workflow must be visual, event-driven, editable by non-developers, or connected to many SaaS tools.
- Use Tavily only when current web retrieval or source-grounded context is part of the product behavior.
- Use Gradium only when voice is central to the interaction.
- Use Nebius only when the project needs GPU infrastructure, model hosting, object storage, serverless AI jobs, or production-style cloud resources.
- Use Base44 when prompt-built app generation or non-developer UI ownership is the point of the session.
- For short sessions, avoid adding authentication, payments, multi-tenant data models, admin dashboards, or deployment-specific config unless they are essential to the learning goal.
- If a tool is not used in the chosen pathway, mention it only as a possible extension rather than wiring it into the starter build.

## Coding Agent Commit Attribution

When a coding agent contributes to a commit, include the agent as a co-contributor in the commit message trailer after a blank line at the end of the message.

Use this format:

```text
Co-authored-by: Agent Name <agent-email@example.com>
```

Examples:

```text
Co-authored-by: Codex <codex@openai.com>
Co-authored-by: Claude <noreply@anthropic.com>
Co-authored-by: Cursor Agent <agent@cursor.sh>
```

If the agent has an official or configured no-reply email, use that exact email. If the agent email is unknown, ask the maintainer before committing rather than inventing one.

## Public Repo Safety Checklist

Before opening a PR or making a release, confirm:

- `git status` only shows intended changes.
- No `.env` file or private credential file is staged.
- New tool claims link to official or primary sources.
- Workshop instructions avoid exposing private keys during screenshots or livestreams.
- Any generated examples use fake IDs, fake domains, or clearly marked placeholders.
