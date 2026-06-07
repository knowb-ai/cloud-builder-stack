#!/usr/bin/env python3
"""Generate optional Cloud Builder Stack app boilerplate."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]


def clean(content: str) -> str:
    return dedent(content).lstrip()


FILES: dict[str, dict[str, str]] = {
    "fastapi-jinja": {
        "backend/requirements.txt": clean(
            """
            fastapi==0.115.6
            uvicorn[standard]==0.34.0
            jinja2==3.1.5
            python-dotenv==1.0.1
            pydantic-settings==2.7.1
            orjson==3.10.13
            """
        ),
        "backend/requirements-dev.txt": "ruff==0.9.2\n",
        "backend/app/__init__.py": "",
        "backend/app/main.py": clean(
            '''
            from pathlib import Path

            from fastapi import FastAPI, Request
            from fastapi.responses import ORJSONResponse
            from fastapi.templating import Jinja2Templates


            TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

            app = FastAPI(default_response_class=ORJSONResponse)
            templates = Jinja2Templates(directory=TEMPLATES_DIR)


            @app.get("/api/health")
            async def health() -> dict[str, str]:
                return {"status": "ok"}


            @app.get("/", include_in_schema=False)
            async def index(request: Request):
                return templates.TemplateResponse(request, "index.html", {})
            '''
        ),
        "backend/app/templates/index.html": clean(
            """
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>Cloud Builder Stack</title>
                <style>
                  :root {
                    color-scheme: light dark;
                    font-family:
                      Inter, ui-sans-serif, system-ui, -apple-system,
                      BlinkMacSystemFont, "Segoe UI", sans-serif;
                  }

                  body {
                    min-height: 100vh;
                    margin: 0;
                    display: grid;
                    place-items: center;
                    background: #f6f7f9;
                    color: #16181d;
                  }

                  main {
                    width: min(720px, calc(100vw - 32px));
                  }

                  code {
                    background: #e9ecf1;
                    border-radius: 4px;
                    padding: 2px 5px;
                  }

                  @media (prefers-color-scheme: dark) {
                    body {
                      background: #111318;
                      color: #f4f5f7;
                    }

                    code {
                      background: #252a33;
                    }
                  }
                </style>
              </head>
              <body>
                <main>
                  <h1>Cloud Builder Stack backend is running.</h1>
                  <p>Add one route, one service module, and one visible demo path.</p>
                  <p>Health check: <a href="/api/health">/api/health</a></p>
                </main>
              </body>
            </html>
            """
        ),
    },
    "fastapi-vite": {
        "backend/requirements.txt": clean(
            """
            fastapi==0.115.6
            uvicorn[standard]==0.34.0
            jinja2==3.1.5
            python-dotenv==1.0.1
            pydantic-settings==2.7.1
            orjson==3.10.13
            """
        ),
        "backend/requirements-dev.txt": "ruff==0.9.2\n",
        "backend/app/__init__.py": "",
        "backend/app/main.py": clean(
            '''
            from pathlib import Path

            from fastapi import FastAPI, Request
            from fastapi.responses import FileResponse, ORJSONResponse, Response
            from fastapi.staticfiles import StaticFiles
            from fastapi.templating import Jinja2Templates


            ROOT_DIR = Path(__file__).resolve().parents[2]
            FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"
            FRONTEND_ASSETS = FRONTEND_DIST / "assets"
            TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

            app = FastAPI(default_response_class=ORJSONResponse)
            templates = Jinja2Templates(directory=TEMPLATES_DIR)

            if FRONTEND_ASSETS.exists():
                app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS), name="assets")


            @app.get("/api/health")
            async def health() -> dict[str, str]:
                return {"status": "ok"}


            @app.get("/{full_path:path}", include_in_schema=False)
            async def serve_frontend(request: Request, full_path: str) -> FileResponse | Response:
                if full_path.startswith("api/"):
                    return ORJSONResponse({"detail": "Not Found"}, status_code=404)

                index_path = FRONTEND_DIST / "index.html"
                if index_path.exists():
                    return FileResponse(index_path)

                return templates.TemplateResponse(
                    request,
                    "index.html",
                    {"frontend_dist": str(FRONTEND_DIST), "requested_path": full_path},
                )
            '''
        ),
        "backend/app/templates/index.html": clean(
            """
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>Cloud Builder Stack</title>
                <style>
                  :root {
                    color-scheme: light dark;
                    font-family:
                      Inter, ui-sans-serif, system-ui, -apple-system,
                      BlinkMacSystemFont, "Segoe UI", sans-serif;
                  }

                  body {
                    min-height: 100vh;
                    margin: 0;
                    display: grid;
                    place-items: center;
                    background: #f6f7f9;
                    color: #16181d;
                  }

                  main {
                    width: min(720px, calc(100vw - 32px));
                  }

                  code {
                    background: #e9ecf1;
                    border-radius: 4px;
                    padding: 2px 5px;
                  }

                  @media (prefers-color-scheme: dark) {
                    body {
                      background: #111318;
                      color: #f4f5f7;
                    }

                    code {
                      background: #252a33;
                    }
                  }
                </style>
              </head>
              <body>
                <main>
                  <h1>Cloud Builder Stack backend is running.</h1>
                  <p>
                    Build the frontend with <code>cd frontend && npm run build</code>,
                    then FastAPI will serve <code>{{ frontend_dist }}</code>.
                  </p>
                  <p>Health check: <a href="/api/health">/api/health</a></p>
                </main>
              </body>
            </html>
            """
        ),
        "frontend/index.html": clean(
            """
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Cloud Builder Stack</title>
              </head>
              <body>
                <div id="root"></div>
                <script type="module" src="/src/main.jsx"></script>
              </body>
            </html>
            """
        ),
        "frontend/package.json": clean(
            """
            {
              "name": "cloud-builder-stack-frontend",
              "version": "0.1.0",
              "private": true,
              "type": "module",
              "scripts": {
                "dev": "vite --host 0.0.0.0",
                "build": "vite build",
                "preview": "vite preview --host 0.0.0.0"
              },
              "dependencies": {
                "react": "latest",
                "react-dom": "latest"
              },
              "devDependencies": {
                "@vitejs/plugin-react": "latest",
                "vite": "latest"
              }
            }
            """
        ),
        "frontend/src/main.jsx": clean(
            """
            import React, { useEffect, useState } from "react";
            import { createRoot } from "react-dom/client";
            import "./styles.css";

            function App() {
              const [health, setHealth] = useState("checking");

              useEffect(() => {
                fetch("/api/health")
                  .then((response) => response.json())
                  .then((data) => setHealth(data.status ?? "unknown"))
                  .catch(() => setHealth("unreachable"));
              }, []);

              return (
                <main className="app-shell">
                  <section className="intro">
                    <p className="eyebrow">Cloud Builder Stack</p>
                    <h1>FastAPI backend, bundled frontend, ready to deploy.</h1>
                    <p>
                      Start small, keep secrets server-side, and ship the SPA through
                      the backend when a single-service deploy is the fastest path.
                    </p>
                  </section>

                  <section className="status-panel" aria-label="Backend status">
                    <span>Backend</span>
                    <strong>{health}</strong>
                  </section>
                </main>
              );
            }

            createRoot(document.getElementById("root")).render(<App />);
            """
        ),
        "frontend/src/styles.css": clean(
            """
            :root {
              color: #15171c;
              background: #f5f7fb;
              font-family:
                Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif;
              font-synthesis: none;
              text-rendering: optimizeLegibility;
            }

            * {
              box-sizing: border-box;
            }

            body {
              min-width: 320px;
              min-height: 100vh;
              margin: 0;
            }

            a {
              color: inherit;
            }

            .app-shell {
              min-height: 100vh;
              display: grid;
              grid-template-columns: minmax(0, 1fr) minmax(240px, 320px);
              align-items: center;
              gap: 32px;
              width: min(1080px, calc(100vw - 32px));
              margin: 0 auto;
              padding: 48px 0;
            }

            .intro {
              max-width: 700px;
            }

            .eyebrow {
              margin: 0 0 12px;
              color: #4c6f5d;
              font-size: 0.8rem;
              font-weight: 700;
              letter-spacing: 0;
              text-transform: uppercase;
            }

            h1 {
              margin: 0;
              font-size: clamp(2.25rem, 4.5rem, 5rem);
              line-height: 0.96;
              letter-spacing: 0;
            }

            .intro p:last-child {
              max-width: 620px;
              margin: 24px 0 0;
              color: #4c5563;
              font-size: 1.08rem;
              line-height: 1.6;
            }

            .status-panel {
              display: grid;
              gap: 12px;
              padding: 20px;
              border: 1px solid #dfe3ea;
              border-radius: 8px;
              background: #ffffff;
            }

            .status-panel span {
              color: #647084;
              font-size: 0.9rem;
            }

            .status-panel strong {
              font-size: 2rem;
            }

            @media (max-width: 760px) {
              .app-shell {
                grid-template-columns: 1fr;
                align-content: center;
              }

              h1 {
                font-size: clamp(2rem, 3.5rem, 3.75rem);
              }
            }
            """
        ),
        "frontend/vite.config.js": clean(
            """
            import react from "@vitejs/plugin-react";
            import { defineConfig } from "vite";

            export default defineConfig({
              plugins: [react()],
              build: {
                outDir: "dist",
                emptyOutDir: true
              }
            });
            """
        ),
    },
}

FILES["vite-frontend"] = {
    path: content
    for path, content in FILES["fastapi-vite"].items()
    if path.startswith("frontend/")
}


def write_files(pathway: str, root: Path, force: bool) -> list[Path]:
    files = FILES[pathway]
    targets = [root / relative_path for relative_path in files]
    existing = [target for target in targets if target.exists()]

    if existing and not force:
        formatted = "\n".join(f"  - {path.relative_to(root)}" for path in existing)
        raise SystemExit(
            "Refusing to overwrite existing scaffold files:\n"
            f"{formatted}\n"
            "Re-run with FORCE=1 if you intend to replace them."
        )

    for relative_path, content in files.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return targets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pathway",
        choices=sorted(FILES),
        default="fastapi-jinja",
        help="Scaffold pathway to generate.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root to write into.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = write_files(args.pathway, args.root.resolve(), args.force)
    print(f"Generated {args.pathway} scaffold:")
    for target in targets:
        print(f"  - {target.relative_to(args.root.resolve())}")


if __name__ == "__main__":
    main()
