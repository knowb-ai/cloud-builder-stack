PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
RUFF := $(VENV)/bin/ruff

.PHONY: setup setup-backend setup-frontend build serve dev-backend dev-frontend lint clean

setup: setup-backend setup-frontend

setup-backend:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r backend/requirements.txt
	$(PIP) install -r backend/requirements-dev.txt

setup-frontend:
	cd frontend && npm install

build:
	cd frontend && npm run build

serve:
	$(UVICORN) backend.app.main:app --host 0.0.0.0 --port $${PORT:-8000}

dev-backend:
	$(UVICORN) backend.app.main:app --reload

dev-frontend:
	cd frontend && npm run dev

lint:
	$(RUFF) check backend

clean:
	rm -rf frontend/dist .ruff_cache .pytest_cache
