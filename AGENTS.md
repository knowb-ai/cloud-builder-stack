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
