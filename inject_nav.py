#!/usr/bin/env python3
"""
inject_nav.py — Add a site-wide Bootstrap nav bar to all .html files.

Usage (from repo root):
  python inject_nav.py --root . --base /Packet-Tracer --dry-run
  python inject_nav.py --root . --base /Packet-Tracer
  python inject_nav.py --root ./docs --base /Packet-Tracer --include-index

Key options:
  --root PATH           Top folder to scan (default: .)
  --base URL_PATH       Absolute base path for GitHub Pages, e.g. /Packet-Tracer
  --dry-run             Show files that would be changed without writing
  --include-index       Include files named index.html (default: included; keep for completeness)
  --exclude GLOB        Exclude pattern(s), can repeat (e.g., --exclude "vendor/*" --exclude "archive/*")
  --only GLOB           Only include files that match (can repeat)

The script is idempotent: it checks for a marker and won't inject twice.
It also writes timestamped backups, e.g., file.html.bak.2025-08-24T15-07-00
"""

import argparse, fnmatch, os, re, sys, shutil, datetime
from pathlib import Path

MARKER_START = "<!-- NAVBAR-INJECT START -->"
MARKER_END   = "<!-- NAVBAR-INJECT END -->"

BOOTSTRAP_CSS = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">'
BOOTSTRAP_JS  = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'

NAV_TEMPLATE = f"""{MARKER_START}
<!-- Injected by inject_nav.py -->
<nav class=\"navbar navbar-expand-lg navbar-dark bg-dark\">
  <div class=\"container-fluid\">
    <a class=\"navbar-brand\" href=\"{{base}}/index.html\">Packet Tracer Labs</a>
    <button class=\"navbar-toggler\" type=\"button\" data-bs-toggle=\"collapse\" data-bs-target=\"#navbarNav\">
      <span class=\"navbar-toggler-icon\"></span>
    </button>
    <div class=\"collapse navbar-collapse\" id=\"navbarNav\">
      <ul class=\"navbar-nav\">
        <li class=\"nav-item\"><a class=\"nav-link\" href=\"{{base}}/index.html\">Home</a></li>
        <li class=\"nav-item\"><a class=\"nav-link\" href=\"{{base}}/Cisco-Packet-Tracer/index.html\">Cisco Labs</a></li>
        <li class=\"nav-item\"><a class=\"nav-link\" href=\"{{base}}/Networking/index.html\">Networking</a></li>
        <li class=\"nav-item\"><a class=\"nav-link\" href=\"{{base}}/IoT/index.html\">IoT</a></li>
      </ul>
    </div>
  </div>
</nav>
{MARKER_END}"""

def should_skip(path: Path, includes, excludes, include_index):
    rel = str(path).replace("\\", "/")

    # Glob filters
    if includes:
        if not any(fnmatch.fnmatch(rel, pat) for pat in includes):
            return True
    if excludes and any(fnmatch.fnmatch(rel, pat) for pat in excludes):
        return True

    # Keep index.html by default (so condition is noop unless future change)
    if not include_index and path.name.lower() == "index.html":
        return True

    return False

def has_marker(html: str) -> bool:
    return (MARKER_START in html) and (MARKER_END in html)

def ensure_bootstrap_head(html: str) -> str:
    # Insert CSS before </head> if not present
    if BOOTSTRAP_CSS not in html:
        html = re.sub(r"</head>", f"  {BOOTSTRAP_CSS}\n</head>", html, count=1, flags=re.IGNORECASE)
    return html


def ensure_bootstrap_body_end(html: str) -> str:
    # Insert JS before </body> if not present
    if BOOTSTRAP_JS not in html:
        html = re.sub(r"</body>", f"  {BOOTSTRAP_JS}\n</body>", html, count=1, flags=re.IGNORECASE)
    return html

def inject_nav(html: str, base: str) -> str:
    # Idempotency
    if has_marker(html):
        return html

    # Find <body ...> tag and insert right after it
    m = re.search(r"<body[^>]*>", html, flags=re.IGNORECASE)
    if not m:
        return html  # no body tag, skip

    nav_html = NAV_TEMPLATE.replace("{MARKER_START}", MARKER_START).replace("{MARKER_END}", MARKER_END).replace("{{base}}", base)
    insert_pos = m.end()
    new_html = html[:insert_pos] + "\n" + nav_html + "\n" + html[insert_pos:]
    return new_html

def process_file(path: Path, base: str, dry_run: bool) -> bool:
    orig = path.read_text(encoding="utf-8", errors="ignore")
    html = orig

    html = ensure_bootstrap_head(html)
    html = inject_nav(html, base)
    html = ensure_bootstrap_body_end(html)

    changed = (html != orig)
    if changed and not dry_run:
        # Backup
        ts = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        backup = path.with_suffix(path.suffix + f".bak.{ts}")
        backup.write_text(orig, encoding="utf-8", errors="ignore")
        path.write_text(html, encoding="utf-8")

    return changed

def main():
    import argparse, fnmatch
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".", help="Top folder to scan")
    p.add_argument("--base", required=True, help="Absolute base path for links, e.g. /Packet-Tracer")
    p.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    p.add_argument("--include-index", action="store_true", help="Include files named index.html (default: included)")
    p.add_argument("--exclude", action="append", default=[], help="Glob to exclude (can repeat)")
    p.add_argument("--only", action="append", default=[], help="Glob to include (can repeat)")
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[!] Root not found: {root}", file=sys.stderr)
        sys.exit(1)

    edited = []
    scanned = 0
    for path in root.rglob("*.html"):
        scanned += 1
        if should_skip(path, args.only, args.exclude, args.include_index):
            continue
        changed = process_file(path, args.base.rstrip("/"), args.dry_run)
        if changed:
            edited.append(str(path))

    if args.dry_run:
        print(f"Dry run complete. {len(edited)} file(s) would be modified:")
    else:
        print(f"Done. Modified {len(edited)} file(s). Backups created next to originals.")
    for e in edited:
        print("-", e)

if __name__ == "__main__":
    main()
