import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scaffold.py"


class ScaffoldTest(unittest.TestCase):
    def test_pathways_and_overwrite_protection(self):
        expected = {
            "python-prototype": ["backend/main.py"],
            "go-service": ["backend/go.mod", "backend/main.go"],
            "fastapi-jinja": ["backend/app/main.py", "backend/app/templates/index.html"],
            "fastapi-vite": ["backend/app/main.py", "frontend/package.json"],
            "vite-frontend": ["frontend/package.json"],
            "rust-native": ["component/Cargo.toml", "component/src/main.rs"],
            "rust-wasm": ["component/Cargo.toml", "component/src/lib.rs"],
        }
        for pathway, paths in expected.items():
            with self.subTest(pathway=pathway), tempfile.TemporaryDirectory() as directory:
                command = [sys.executable, str(SCRIPT), "--pathway", pathway, "--root", directory]
                subprocess.run(command, check=True, capture_output=True)
                for path in paths:
                    self.assertTrue((Path(directory) / path).is_file(), path)
                original = (Path(directory) / paths[0]).read_bytes()
                repeat = subprocess.run(command, capture_output=True)
                self.assertNotEqual(repeat.returncode, 0)
                self.assertIn(b"Refusing to overwrite", repeat.stderr)
                self.assertEqual((Path(directory) / paths[0]).read_bytes(), original)


    @unittest.skipUnless(all(importlib.util.find_spec(name) for name in ("fastapi", "jinja2", "orjson")), "FastAPI dependencies are not installed")
    def test_fastapi_apps_load(self):
        for pathway in ("fastapi-jinja", "fastapi-vite"):
            with self.subTest(pathway=pathway), tempfile.TemporaryDirectory() as directory:
                subprocess.run([sys.executable, str(SCRIPT), "--pathway", pathway, "--root", directory], check=True, capture_output=True)
                subprocess.run([sys.executable, "-c", "import backend.app.main"], cwd=directory, check=True, capture_output=True)

    def test_rejects_conflicting_backends_and_symlinks(self):
        for old, new in (("python-prototype", "go-service"), ("go-service", "fastapi-jinja"), ("fastapi-vite", "python-prototype")):
            with self.subTest(old=old, new=new), tempfile.TemporaryDirectory() as directory:
                def command(pathway):
                    return [sys.executable, str(SCRIPT), "--pathway", pathway, "--root", directory]
                subprocess.run(command(old), check=True, capture_output=True)
                before = {p.relative_to(directory): p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()}
                result = subprocess.run(command(new) + ["--force"], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(b"Conflicting backend", result.stderr)
                self.assertEqual(before, {p.relative_to(directory): p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()})
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            (Path(directory) / "backend").symlink_to(outside, target_is_directory=True)
            result = subprocess.run([sys.executable, str(SCRIPT), "--pathway", "go-service", "--root", directory, "--force"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"symlink", result.stderr)
            self.assertFalse(list(Path(outside).iterdir()))
        with tempfile.TemporaryDirectory() as directory:
            backend = Path(directory) / "backend"
            backend.mkdir()
            (backend / "go.mod").symlink_to(Path(directory) / "missing")
            result = subprocess.run([sys.executable, str(SCRIPT), "--pathway", "go-service", "--root", directory], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"symlink", result.stderr)
            self.assertFalse((backend / "main.go").exists())

    @unittest.skipUnless(all(importlib.util.find_spec(name) for name in ("fastapi", "jinja2", "orjson")), "FastAPI dependencies are not installed")
    def test_spa_static_file_and_api_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run([sys.executable, str(SCRIPT), "--pathway", "fastapi-vite", "--root", directory], check=True, capture_output=True)
            dist = root / "frontend" / "dist"
            dist.mkdir(parents=True)
            (dist / "index.html").write_text("index")
            (dist / "manifest.webmanifest").write_text("manifest")
            code = '''
import asyncio
from backend.app.main import serve_frontend
async def check():
    manifest = await serve_frontend(None, "manifest.webmanifest")
    assert manifest.path.name == "manifest.webmanifest"
    route = await serve_frontend(None, "dashboard")
    assert route.path.name == "index.html"
    api = await serve_frontend(None, "api")
    assert api.status_code == 404
    nested_api = await serve_frontend(None, "api/missing")
    assert nested_api.status_code == 404
asyncio.run(check())
'''
            subprocess.run([sys.executable, "-c", code], cwd=root, check=True, capture_output=True)

    def test_kicklauncher_selection(self):
        launcher = SCRIPT.parent / "kicklauncher.py"
        for choices, expected in (("1\n", "backend/main.py"), ("2\n1\n", "backend/app/main.py"), ("2\n2\n", "frontend/package.json"), ("3\n", "backend/go.mod"), ("4\n1\n", "component/src/main.rs"), ("4\n2\n", "component/src/lib.rs")):
            with self.subTest(choices=choices), tempfile.TemporaryDirectory() as directory:
                command = [sys.executable, str(launcher), "--root", directory]
                subprocess.run(command, input=choices, text=True, check=True, capture_output=True)
                self.assertTrue((Path(directory) / expected).is_file())
                repeat = subprocess.run(command, input=choices, text=True, capture_output=True)
                self.assertNotEqual(repeat.returncode, 0)
                self.assertIn("Refusing to overwrite", repeat.stderr)
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(launcher), "--root", directory], input="4\n", text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(list(Path(directory).iterdir()))

    @unittest.skipUnless(shutil.which("cargo") and shutil.which("node") and os.environ.get("CBS_WASM_SYSROOT"), "Wasm target sysroot and Node are required")
    def test_wasm_component_in_node(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run([sys.executable, str(SCRIPT), "--pathway", "rust-wasm", "--root", directory], check=True, capture_output=True)
            env = {**os.environ, "CARGO_HOME": str(root / "cargo-home"), "RUSTFLAGS": "--sysroot " + os.environ["CBS_WASM_SYSROOT"]}
            subprocess.run(["cargo", "build", "--offline", "--release", "--target", "wasm32-unknown-unknown"], cwd=root / "component", env=env, check=True)
            wasm = root / "component/target/wasm32-unknown-unknown/release/example_component.wasm"
            js = 'WebAssembly.instantiate(require("fs").readFileSync(process.argv[1])).then(({instance}) => {const f=instance.exports.component_add; if(f(2,3)!==5 || (f(-1,1)>>>0)!==4294967295) process.exit(1);}).catch(() => process.exit(1))'
            subprocess.run(["node", "-e", js, str(wasm)], check=True, capture_output=True)

    @unittest.skipUnless(shutil.which("make"), "Make is not installed")
    def test_make_init_selects_go(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            shutil.copy(SCRIPT, root / "scripts" / "scaffold.py")
            shutil.copytree(SCRIPT.parent.parent / "templates", root / "templates")
            shutil.copy(SCRIPT.parent.parent / "Makefile", root / "Makefile")
            subprocess.run(["make", "init", "PATHWAY=go-service"], cwd=root, check=True, capture_output=True)
            self.assertTrue((root / "backend" / "go.mod").is_file())

    @unittest.skipUnless(shutil.which("go"), "Go is not installed")
    def test_go_service_build_and_health_handler(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run([sys.executable, str(SCRIPT), "--pathway", "go-service", "--root", directory], check=True, capture_output=True)
            (root / "backend" / "main_test.go").write_text(r'''
package main
import ("net/http/httptest"; "testing")
func TestHealth(t *testing.T) {
    w := httptest.NewRecorder()
    healthHandler(w, httptest.NewRequest("GET", "/api/health", nil))
    if w.Code != 200 || w.Body.String() != "{\"status\":\"ok\"}\n" { t.Fatalf("unexpected response: %d %q", w.Code, w.Body.String()) }
    w = httptest.NewRecorder()
    healthHandler(w, httptest.NewRequest("POST", "/api/health", nil))
    if w.Code != 405 || w.Header().Get("Allow") != "GET" { t.Fatalf("unexpected method response: %d", w.Code) }
}
''')
            env = {**os.environ, "GOCACHE": str(root / "go-cache"), "GOPROXY": "off"}
            subprocess.run(["go", "test", "./..."], cwd=root / "backend", env=env, check=True, capture_output=True)

    @unittest.skipUnless(shutil.which("cargo"), "Cargo is not installed")
    def test_native_rust_command(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run([sys.executable, str(SCRIPT), "--pathway", "rust-native", "--root", directory], check=True, capture_output=True)
            env = {**os.environ, "CARGO_HOME": str(Path(directory) / "cargo-home")}
            result = subprocess.run(["cargo", "run", "--offline", "--quiet"], cwd=Path(directory) / "component", env=env, check=True, stdout=subprocess.PIPE, text=True)
            self.assertEqual(result.stdout.strip(), "5")


if __name__ == "__main__":
    unittest.main()
