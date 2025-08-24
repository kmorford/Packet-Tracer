#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import datetime
import urllib.parse
from typing import Iterable

TARGET_DIRS = ["Cisco Packet Tracer", "Networking", "IoT"]
INCLUDE_EXT = {".html", ".md"}   # list pages, not labs
EXCLUDE_NAMES = {"index.html", "index.md", "README.md"}

FOLDER_INDEX_TEMPLATE = """# {title}

## Pages
{links}
"""

ROOT_INDEX_TEMPLATE = """# Packet Tracer — Site Home

## Sections
{sections}

---

_Last updated: {today}_
"""

def encode_segment(name: str) -> str:
    return urllib.parse.quote(name, safe="-._~()")

def encode_filename(name: str) -> str:
    # Encode spaces & special chars but keep dot before extension
    return urllib.parse.quote(name, safe="-._~()")

def list_section_links(existing: Iterable[Path]) -> str:
    lines = []
    for folder in existing:
        enc = encode_segment(folder.name)
        lines.append(f"- [{folder.name}](./{enc}/)")
    return "\n".join(lines) or "_(No sections present)_"

def page_list(folder: Path) -> str:
    items: list[str] = []
    for p in sorted(folder.iterdir(), key=lambda x: x.name.lower()):
        if p.name.startswith("."):
            continue
        if not p.is_file():
            continue
        if p.suffix.lower() in INCLUDE_EXT and p.name not in EXCLUDE_NAMES:
            label = " ".join(p.stem.replace("-", " ").replace("_", " ").split())
            items.append(f"- [{label}](./{encode_filename(p.name)})")
    return "\n".join(items) or "_(No pages yet. Add .html or .md files here.)_"

def write_folder_index(folder: Path) -> None:
    idx = folder / "index.md"
    content = FOLDER_INDEX_TEMPLATE.format(
        title=folder.name,
        links=page_list(folder)
    )
    idx.write_text(content + "\n", encoding="utf-8")
    print(f"[WROTE] {idx}")

def write_root_index(root: Path, existing_dirs: list[Path]) -> None:
    idx = root / "index.md"
    idx.write_text(
        ROOT_INDEX_TEMPLATE.format(
            sections=list_section_links(existing_dirs),
            today=datetime.date.today().isoformat()
        ) + "\n",
        encoding="utf-8",
    )
    print(f"[WROTE] {idx}")

def main() -> None:
    root = Path(__file__).resolve().parent
    existing = []
    for name in TARGET_DIRS:
        folder = root / name
        if folder.exists() and folder.is_dir():
            existing.append(folder)
        else:
            print(f"[SKIP] Missing: {folder}")
    write_root_index(root, existing)
    for folder in existing:
        write_folder_index(folder)

if __name__ == "__main__":
    main()
