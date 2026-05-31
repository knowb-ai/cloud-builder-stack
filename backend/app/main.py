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
