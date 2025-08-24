#!/usr/bin/env python3
import os
import datetime
from pathlib import Path

# === CONFIG ===
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
- [Cisco Packet Tracer](./Cisco%20Packet%20Tracer/README.md)
- [Networking](./Networking/README.md)
- [IoT](./IoT/README.md)

---

_Last updated: {today}_
"""

def list_pkt_markdown(folder: Path) -> str:
    pkts = sorted([p for p in folder.glob("*.pkt") if p.is_file()])
    if not pkts:
        return "_(No .pkt files found yet.)_"
    lines = []
    for p in pkts:
        title = p.stem.replace("_", " ")
        lines.append(f"- [{title}](./{p.name})")
    return "\n".join(lines)

def ensure_folder_readme(folder: Path):
    readme = folder / "README.md"
    auto_list = list_pkt_markdown(folder)

    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        if MARKER_START in text and MARKER_END in text:
            before = text.split(MARKER_START)[0]
            after = text.split(MARKER_END)[1]
            new_text = f"{before}{MARKER_START}\n{auto_list}\n{MARKER_END}{after}"
        else:
            new_text = text.rstrip() + f"\n\n## Lab Index\n\n{MARKER_START}\n{auto_list}\n{MARKER_END}\n"
        if new_text != text:
            readme.write_text(new_text, encoding="utf-8")
            print(f"Updated: {readme}")
    else:
        content = f"# {folder.name}\n\n## Lab Index\n\n{MARKER_START}\n{auto_list}\n{MARKER_END}\n"
        readme.write_text(content, encoding="utf-8")
        print(f"Created: {readme}")

def write_root_index(repo_root: Path):
    index_md = r_

        readme.write_text(content, encoding="utf-8")
        print(f"Created: {readme}")

def write_root_index(repo
