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

## Suggested Workshop Patterns

### 1. AI Research Assistant

- Tavily retrieves current web context.
- n8n coordinates search, summarization, notifications, and logging.
- Base44 provides a quick user-facing app shell.
- Nebius can host heavier inference or batch processing if needed.

### 2. Voice-Enabled Agent

- Gradium provides speech or voice interaction.
- Tavily gives the agent current web knowledge.
- n8n routes events between voice, search, CRM, docs, and messaging tools.
- Base44 can host the demo UI or internal operator dashboard.

### 3. Hackathon Builder Platform

- Base44 accelerates participant prototypes.
- n8n gives teams reusable automation templates.
- Tavily supports grounded AI features.
- Nebius supports GPU workloads, hosted services, and shared infrastructure.
- Gradium supports voice-first bonus tracks.

## Repository Layout

```text
.
├── README.md
├── .env.example
├── .gitignore
├── LICENSE
└── docs/
    └── workshop-template.md
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

## Contributing

Contributions are welcome. Good additions include:

- new workshop-ready AI/cloud tools
- example workshop flows
- `.env.example` improvements
- security notes for public demos
- tool comparison notes with official source links

Please avoid vendor hype. Keep descriptions practical, sourced, and useful for builders.
