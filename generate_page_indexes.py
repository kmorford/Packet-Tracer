#!/usr/bin/env python3
from pathlib import Path
import datetime

TARGET_DIRS = ["Cisco Packet Tracer", "Networking", "IoT"]
INCLUDE_EXT = {".html", ".md"}   # list pages, not labs
EXCLUDE_NAMES = {"index.html", "index.md", "README.md"}

FOLDER_INDEX_TEMPLATE = """# {title}

## Pages
{links}
"""

ROOT_INDEX_TEMPLATE = """# Packet Tracer — Site Home

## Sections
- [Cisco Packet Tracer](./Cisco%20Packet%20Tracer/)
- [Networking](./Networking/)
- [IoT](./IoT/)

---

_Last updated: {today}_
"""

def page_list(folder: Path) -> str:
    items = []
    for p in sorted(folder.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_file():
            continue
        if p.suffix.lower() in INCLUDE_EXT and p.name not in EXCLUDE_NAMES:
            label = p.stem.replace("-", " ").replace("_", " ")
            items.append(f"- [{label}](./{p.name})")
    return "\n".join(items) or "_(No pages yet. Add .html or .md files here.)_"

def write_folder_index(folder: Path):
    idx = folder / "index.md"
    content = FOLDER_INDEX_TEMPLATE.format(
        title=folder.name,
        links=page_list(folder)
    )
    idx.write_text(content, encoding="utf-8")
    print(f"[WROTE] {idx}")

def write_root_index(root: Path):
    idx = root / "index.md"
    idx.write_text(
        ROOT_INDEX_TEMPLATE.format(today=datetime.date.today().isoformat()),
        encoding="utf-8",
    )
    print(f"[WROTE] {idx}")

def main():
    root = Path(__file__).resolve().parent
    write_root_index(root)
    for name in TARGET_DIRS:
        folder = root / name
        if folder.exists():
            write_folder_index(folder)
        else:
            print(f"[SKIP] Missing: {folder}")

if __name__ == "__main__":
    main()
