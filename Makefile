PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
RUFF := $(VENV)/bin/ruff
PATHWAY ?= fastapi-jinja
FORCE ?= 0
FORCE_FLAG := $(if $(filter 1,$(FORCE)),--force,)

.PHONY: help setup setup-backend setup-frontend scaffold init scaffold-backend scaffold-frontend scaffold-app build serve dev-backend dev-frontend lint clean

help:
	@echo "Cloud Builder Stack"
	@echo ""
	@echo "Scaffold only the app shape you need:"
	@echo "  make scaffold-backend              FastAPI + Jinja starter"
	@echo "  make scaffold-frontend             Vite frontend starter"
	@echo "  make scaffold-app                  FastAPI + Vite starter"
	@echo "  make init PATHWAY=fastapi-jinja    Choose a pathway explicitly"
	@echo ""
	@echo "After scaffolding:"
	@echo "  make setup                         Install generated app dependencies"
	@echo "  make build                         Build generated frontend"
	@echo "  make serve                         Serve generated backend"

setup:
	@if [ ! -f backend/requirements.txt ] && [ ! -f frontend/package.json ]; then echo "No app scaffold found. Run 'make scaffold-backend', 'make scaffold-frontend', or 'make scaffold-app' first."; exit 1; fi
	@if [ -f backend/requirements.txt ]; then $(MAKE) setup-backend; else echo "Skipping backend setup; no backend scaffold found."; fi
	@if [ -f frontend/package.json ]; then $(MAKE) setup-frontend; else echo "Skipping frontend setup; no frontend scaffold found."; fi

setup-backend:
	@if [ ! -f backend/requirements.txt ]; then echo "No backend scaffold found. Run 'make scaffold-backend' or 'make scaffold-app' first."; exit 1; fi
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r backend/requirements.txt
	$(PIP) install -r backend/requirements-dev.txt

setup-frontend:
	@if [ ! -f frontend/package.json ]; then echo "No frontend scaffold found. Run 'make scaffold-frontend' or 'make scaffold-app' first."; exit 1; fi
	cd frontend && npm install

scaffold: init

init:
	$(PYTHON) scripts/scaffold.py --pathway $(PATHWAY) $(FORCE_FLAG)

scaffold-backend:
	$(PYTHON) scripts/scaffold.py --pathway fastapi-jinja $(FORCE_FLAG)

scaffold-frontend:
	$(PYTHON) scripts/scaffold.py --pathway vite-frontend $(FORCE_FLAG)

scaffold-app:
	$(PYTHON) scripts/scaffold.py --pathway fastapi-vite $(FORCE_FLAG)

build:
	@if [ ! -f frontend/package.json ]; then echo "No frontend scaffold found. Run 'make scaffold-frontend' or 'make scaffold-app' first."; exit 1; fi
	cd frontend && npm run build

serve:
	@if [ ! -f backend/app/main.py ]; then echo "No backend scaffold found. Run 'make scaffold-backend' or 'make scaffold-app' first."; exit 1; fi
	$(UVICORN) backend.app.main:app --host 0.0.0.0 --port $${PORT:-8000}

dev-backend:
	@if [ ! -f backend/app/main.py ]; then echo "No backend scaffold found. Run 'make scaffold-backend' or 'make scaffold-app' first."; exit 1; fi
	$(UVICORN) backend.app.main:app --reload

dev-frontend:
	@if [ ! -f frontend/package.json ]; then echo "No frontend scaffold found. Run 'make scaffold-frontend' or 'make scaffold-app' first."; exit 1; fi
	cd frontend && npm run dev

lint:
	@if [ ! -d backend/app ]; then echo "No backend scaffold found. Run 'make scaffold-backend' or 'make scaffold-app' first."; exit 1; fi
	$(RUFF) check backend

clean:
	rm -rf frontend/dist .ruff_cache .pytest_cache
