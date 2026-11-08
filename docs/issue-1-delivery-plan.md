# Issue 1: pathway alignment delivery plan

Source: https://github.com/knowb-ai/cloud-builder-stack/issues/1

The goal is a publishable, minimal scaffold for each agreed pathway and consistent selection in Kicklauncher. A passing prototype test is evidence for that slice, not acceptance of the whole issue. Work in disposable directories when exercising generation; do not overwrite existing project files.

## Current evidence and constraints

- `scripts/scaffold.py` generates FastAPI/Jinja, FastAPI/Vite, and frontend-only Vite. `Makefile` invokes those names directly; its setup and serve targets assume Python.
- Generation checks for existing target files before writing, with an explicit force option. Preserve that behavior and test it.
- A local interactive Kicklauncher now calls the shared generator. No separate Kicklauncher was located through accessible organization repository-name or code searches; external integration remains unverified.
- Go, Rust, Node, and Python executables are present locally. This does not establish that dependency downloads or browser/Wasm targets are available.
- The Vite scaffold pins direct dependencies and includes an npm lockfile; a clean `npm ci` and build succeeded with Node 24.

## Work packages

### 1. Contract and integration discovery

Identify the actual Kicklauncher repository, how it selects or consumes templates, and any existing interface. Define a small canonical mapping of project shape to generator pathway, preserving existing command aliases where appropriate. Define the Python prototype's minimal runnable user path and the Rust component interface and target selection based on the actual integration.

**MVT:** list the existing generator choices and trace one selection through to generated files in a temporary directory. Expected: the mapping and its consumer are identifiable. **Stop:** record the contract and unresolved Kicklauncher location; do not invent an integration. Local generator work can proceed independently.

### 2. Go backend end-to-end slice

Generate a minimal Go service with a clear handler/service boundary and no unrelated infrastructure. Provide explicit setup, build and run commands; integrate its selection with the shared pathway mapping and make entry point.

**MVT:** generate into a fresh temporary directory, start the service, and request its documented endpoint. Expected: a successful response with the documented shape. **Stop:** the request works and a repeated generation without force refuses to overwrite; terminate the disposable process.

### 3. Python prototype and FastAPI pathways

Add the smallest runnable Python learning/prototype shape, distinguishing it from the durable FastAPI selection. Align existing Jinja and bundled frontend pathways with the shared definitions and preserve their current user-facing commands. Keep backend credentials private and state the frontend/API contract; remove dependencies only where the generated behavior does not need them.

**MVT:** generate each shape in a fresh directory and run its documented user path; for the SPA build it and verify the backend serves it and its API response. Expected: each path runs without a Node backend. **Stop:** each documented route and selection works; record any unavailable dependency or environment explicitly.

### 4. Explicit Rust component

Implement an opt-in performance-critical component with a typed boundary. Require an explicit native or WebAssembly target; choose a concrete representative interaction that demonstrates the interface without claiming a performance threshold. Do not replace an application backend or imply that Rust is automatically faster for a given workload.

**MVT:** generate the explicitly selected target and exercise one typed input/output through its documented interface. Expected: native execution works for a server-side example; for WebAssembly, execute in the documented compatible host when available. **Stop:** both offered targets have evidence, or document precisely which target/host remains unverified; do not add benchmarks absent a representative workload.

### 5. Kicklauncher integration

Once its location and contract are established, connect its selection to the same pathway definitions and generator behavior. Explain the prototype/durable choice, keep Rust opt-in with explicit target, and exclude Node backend selection.

**MVT:** select one FastAPI pathway and one Go pathway via the actual Kicklauncher entry point and verify the generated shapes; check the Rust selection requires an explicit target. **Stop:** selection and generated results agree. If access or the integration contract is missing, record that exact blocker rather than claiming issue completion.

### 6. Documentation and publication verification

Update the README with the selection table, generated module boundaries, prerequisites, exact commands and deployment guidance appropriate to each implemented shape. Link primary runtime documentation for new claims. Check safe placeholders, no private files or credentials, intended changes only, and preserve any user files.

**MVT:** follow the documented command sequence from a clean disposable directory for each pathway, reusing earlier passing runs where code and inputs have not changed. Expected: generated results match the documentation. **Stop:** all issue acceptance criteria have evidence, or list the specific remaining gaps. No cloud resources, CI workload, broad benchmarks or paid services are required for this plan.

## Dependencies and completion

Packages 2–4 can proceed after the local mapping is agreed; package 5 depends on discovering and accessing Kicklauncher. Documentation evolves alongside the implementations. The issue is complete only when all four pathway choices, their generated behavior, Kicklauncher integration, focused checks, and publication review meet the issue criteria. Review readiness and release readiness are separate decisions.

## Current implementation evidence

- `go-service` returned `{"status":"ok"}` over HTTP; the generated handler also passes a Go test.
- `python-prototype` returned the same health response over HTTP.
- `rust-native` ran offline and printed `5`. The WebAssembly build used a checksum-verified official Rust target in a temporary sysroot; Node executed the exported function, including its overflow behavior.
- Both FastAPI variants returned HTTP 200 for the health and root routes with Python 3.12; the Vite production build completed. A startup error in the Vite route was fixed and its import is covered by a regression check; the Vite development proxy also returned the backend health response.
- Focused generator tests cover expected files, overwrite refusal, local Kicklauncher choices, `make init` selection, Go behavior, native and WebAssembly Rust execution, and FastAPI imports when dependencies are available. Integration with any separate Kicklauncher remains unresolved.
- The pinned frontend and lockfile passed a clean `npm ci` and production build.

- Review follow-up: generator refuses conflicting backend shapes and symbolic links; SPA fallback serves generated static files and preserves API 404s. Updated Python pins passed `pip-audit`, and the frontend lockfile passed `npm audit` on 2026-11-08. Audits reflect known advisories at the time, not a future security guarantee.
