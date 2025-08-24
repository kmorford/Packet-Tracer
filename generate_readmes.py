#!/usr/bin/env python3
import os
import datetime
from pathlib import Path

# === CONFIG ===
# Folders where .pkt labs live (relative to repo root).
TARGET_DIRS = [
    "Cisco Packet Tracer",
    "Networking",
    "IoT",
]

# Section markers inside folder READMEs. Everything between them will be replaced.
MARKER_START = "<!-- AUTO-LIST:START -->"
MARKER_END   = "<!-- AUTO-LIST:END -->"

# Template for a folder README if it doesn't exist yet.
FOLDER_README_TEMPLATE = """# {title}

{blurb}

**Navigation:** [🏠 Home](../index.md){nav_links}

---

## Lab Index

{marker_start}
{auto_list}
{marker_end}

---

## Submission & Evidence (brief)
- Submit your **.pkt** plus a short write-up (PDF/MD): addressing plan, key configs, and verification output.
- Name files `LastName_FirstName_LabNN`.

"""

# Simple blurb per folder (editable).
BLURBS = {
    "Cisco Packet Tracer": "Core Packet Tracer activities used throughout the course.",
    "Networking": "Layer-2/Layer-3 fundamentals: addressing, VLANs, routing, and services.",
    "IoT": "Introductory IoT topologies using Packet Tracer’s sensors, actuators, and events.",
}

# Root index template (lightweight landing page).
ROOT_INDEX_TEMPLATE = """# Packet Tracer — Labs Hub

Welcome. Use the sections below to access lab sets.

## Sections
- [Cisco Packet Tracer](./Cisco%20Packet%20Tracer/README.md) — core PT labs & device configs
- [Networking](./Networking/README.md) — VLANs, routing, services
- [IoT](./IoT/README.md) — sensors, actuators, event logic

---

_Last updated: {today}_
"""

def list_pkt_markdown(folder: Path) -> str:
    """Return a Markdown bullet list of all .pkt files in a folder, sorted by name."""
    pkts = sorted([p for p in folder.glob("*.pkt") if p.is_file()])
    if not pkts:
        return "_(No .pkt files found yet.)_"
    lines = []
    for p in pkts:
        title = p.stem.replace("_", " ")
        # Use relative link with ./ so it works on GitHub and Pages
        lines.append(f"- [{title}](./{p.name})")
    return "\n".join(lines)

def ensure_folder_readme(folder: Path, repo_root: Path):
    """Create or update README.md in a given folder, inserting/refreshing the auto-list block."""
    readme = folder / "README.md"
    auto_list = list_pkt_markdown(folder)

    # Build nav links dynamically (links to sibling folders)
    siblings = []
    for t in TARGET_DIRS:
        if t == folder.name:
            continue
        sib_path = repo_root / t / "README.md"
        if sib_path.exists():
            rel = os.path.relpath(sib_path, folder)
            siblings.append(f"[{Path(t).name}](./{os.path.relpath(sib_path, folder).replace(os.sep,'/')})")
    nav_links = ""
    if siblings:
        nav_links = " • " + " • ".join(siblings)

    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        if MARKER_START in text and MARKER_END in text:
            # Replace existing block
            before = text.split(MARKER_START)[0]
            after = text.split(MARKER_END)[1]
            new_text = f"{before}{MARKER_START}\n{auto_list}\n{MARKER_END}{after}"
        else:
            # Append block at the end with a default header
            new_text = text.rstrip() + f"\n\n## Lab Index\n\n{MARKER_START}\n{auto_list}\n{MARKER_END}\n"
        if new_text != text:
            readme.write_text(new_text, encoding="utf-8")
            print(f"Updated: {readme}")
        else:
            print(f"No changes: {readme}")
    else:
        # Create new README using template
        title = folder.name
        blurb = BLURBS.get(title, "Labs in this section.")
        content = FOLDER_README_TEMPLATE.format(
            title=title,
            blurb=blurb,
            nav_links=nav_links,
            marker_start=MARKER_START,
            auto_list=auto_list,
            marker_end=MARKER_END,
        )
        readme.write_text(content, encoding="utf-8")
        print(f"Created: {readme}")

def write_root_index(repo
