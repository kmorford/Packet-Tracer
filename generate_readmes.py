#!/usr/bin/env python3
from __future__ import annotations
import datetime
import re
import urllib.parse
from pathlib import Path
from typing import Iterable

TARGET_DIRS = [
    "Cisco Packet Tracer",
    "Networking",
    "IoT",
]

MARKER_START = "<!-- AUTO-LIST:START -->"
MARKER_END   = "<!-- AUTO-LIST:END -->"

ROOT_INDEX_TEMPLATE = """# Packet Tracer — Labs Hub

Welcome. Use the sections below to access lab sets.

## Sections
{sections}

---

_Last updated: {today}_
"""

def encode_name(name: str) -> str:
    return urllib.parse.quote(name, safe="-._~()")

def section_links(root: Path, dirs: Iterable[str]) -> str:
    lines = []
    for d in dirs:
        p = root / d
        if p.is_dir():
            lines.append(f"- [{d}](./{encode_name(d)}/README.md)")
    return "\n".join(lines) or "_(No sections)_"

def list_pkt_markdown(folder: Path) -> str:
    pkts = sorted(
        [p for p in folder.glob("*.pkt") if p.is_file()],
        key=lambda x: x.name.lower()
    )
    if not pkts:
        return "_(No .pkt files found yet.)_"
    lines = []
    for p in pkts:
        # Title: split on _ or - and collapse spaces
        title = " ".join(re.split(r"[_-]+", p.stem)).strip()
        lines.append(f"- [{title}](./{encode_name(p.name)})")
    return "\n".join(lines)

def splice_auto_block(original: str, new_block: str) -> str:
    start_idx = original.find(MARKER_START)
    end_idx = original.find(MARKER_END)
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        end_idx += len(MARKER_END)
        before = original[:start_idx]
        after = original[end_idx:]
        return f"{before}{MARKER_START}\n{new_block}\n{MARKER_END}{after}"
    # No markers: append block
    base = original.rstrip() + "\n\n" if original.strip() else ""
    return f"{base}## Lab Index\n\n{MARKER_START}\n{new_block}\n{MARKER_END}\n"

def ensure_folder_readme(folder: Path) -> None:
    readme = folder / "README.md"
    auto_list = list_pkt_markdown(folder)
    if readme.exists():
        old = readme.read_text(encoding="utf-8")
        updated = splice_auto_block(old, auto_list)
        if updated != old:
            readme.write_text(updated, encoding="utf-8")
            print(f"[UPDATED] {readme}")
        else:
            print(f"[NO CHANGE] {readme}")
    else:
        content = (
            f"# {folder.name}\n\n"
            f"## Lab Index\n\n"
            f"{MARKER_START}\n{auto_list}\n{MARKER_END}\n"
        )
        readme.write_text(content, encoding="utf-8")
        print(f"[CREATED] {readme}")

def write_root_index(repo_root: Path) -> None:
    idx = repo_root / "index.md"
    sections = section_links(repo_root, TARGET_DIRS)
    idx.write_text(
        ROOT_INDEX_TEMPLATE.format(
            sections=sections,
            today=datetime.date.today().isoformat()
        ),
        encoding="utf-8"
    )
    print(f"[WROTE] {idx}")

def main() -> None:
    repo_root = Path(__file__).resolve().parent
    write_root_index(repo_root)
    for rel in TARGET_DIRS:
        folder = repo_root / rel
        if folder.is_dir():
            ensure_folder_readme(folder)
        else:
            print(f"[SKIP] Missing: {folder}")

if __name__ == "__main__":
    main()
