#!/usr/bin/env python3
"""Choose a minimal pathway and generate it with the shared scaffold generator."""

import argparse
from pathlib import Path

from scaffold import ROOT, write_files


def choose(prompt: str, options: dict[str, tuple[str, str]]) -> str:
    print(prompt)
    for key, (label, _) in options.items():
        print(f"  {key}. {label}")
    while True:
        value = input("Choice: ").strip()
        if value in options:
            return options[value][1]
        print("Choose one of: " + ", ".join(options))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Directory to generate into")
    args = parser.parse_args()
    shape = choose("Choose the project shape:", {
        "1": ("Python learning prototype", "python-prototype"),
        "2": ("UI with backend behavior (FastAPI)", "fastapi"),
        "3": ("Backend service (Go)", "go-service"),
        "4": ("Opt-in Rust performance component", "rust"),
    })
    if shape == "fastapi":
        shape = choose("Choose the frontend:", {
            "1": ("Server-rendered Jinja", "fastapi-jinja"),
            "2": ("Bundled Vite frontend", "fastapi-vite"),
        })
    elif shape == "rust":
        shape = choose("Choose the component target explicitly:", {
            "1": ("Native server-side component", "rust-native"),
            "2": ("WebAssembly for a compatible host", "rust-wasm"),
        })
    root = args.root.resolve()
    targets = write_files(shape, root, force=False)
    print(f"Generated {shape} scaffold:")
    for target in targets:
        print(f"  - {target.relative_to(root)}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit("Selection cancelled; no files generated.")
