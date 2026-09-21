#!/usr/bin/env python3
"""Render the profile README as a polished, print-ready PDF with Chromium."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


BROWSER_NAMES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
)

MAC_BROWSER_PATHS = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path.home() / "Applications/Chromium.app/Contents/MacOS/Chromium",
)


CSS = r"""
@page { size: A4; margin: 13mm 15mm 14mm; }
:root { --ink: #172033; --muted: #607086; --accent: #0b7285; --accent-dark: #075985; --line: #d9e5ea; --soft: #eef8f8; }
* { box-sizing: border-box; }
body { color: var(--ink); font-family: "Inter", "Segoe UI", Arial, sans-serif; font-size: 9.6pt; line-height: 1.38; margin: 0; }
header { border-bottom: 1px solid var(--line); margin-bottom: 13px; padding: 2px 0 10px; }
h1 { color: #102a43; font-size: 28pt; letter-spacing: -.045em; line-height: 1; margin: 0 0 5px; }
h2 { border-bottom: 2px solid var(--accent); color: var(--accent-dark); font-size: 13.5pt; letter-spacing: -.015em; margin: 16px 0 7px; padding-bottom: 3px; }
h3 { color: #164e63; font-size: 10.8pt; margin: 11px 0 1px; }
p { margin: 3px 0 7px; }
header p { color: var(--muted); margin: 3px 0; }
a { color: var(--accent-dark); text-decoration: none; }
hr { border: 0; border-top: 1px solid var(--line); margin: 11px 0; }
ul { margin: 3px 0 7px; padding-left: 17px; }
li { margin: 1.5px 0; }
code { background: var(--soft); border-radius: 3px; color: var(--accent-dark); font-family: "SFMono-Regular", Consolas, monospace; font-size: .88em; padding: 1px 4px; }
strong { color: #163b55; }
h3, h2 { break-after: avoid; }
li, p { orphans: 2; widows: 2; }
@media print { a { color: inherit; } }
"""


def inline_markdown(value: str) -> str:
    value = html.escape(value, quote=True)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    return value


def heading_id(title: str) -> str:
    title = re.sub(r"[*`]", "", title).strip().lower()
    title = "".join(character for character in title if unicodedata.category(character)[0] not in {"S", "P"})
    return re.sub(r"\s+", "-", title).rstrip("-")


def render(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = ["<!doctype html><html><head><meta charset='utf-8'>", f"<style>{CSS}</style></head><body>"]
    in_list = False
    in_header = True

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.strip()
        if not line:
            close_list()
            continue
        if line.startswith("<!--"):
            continue
        if line == "---":
            close_list()
            out.append("<hr>")
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            close_list()
            level = len(heading.group(1))
            title = re.sub(r"[*`]", "", heading.group(2)).strip()
            tag = f"h{level}"
            if level == 1:
                out.append(f"<header><{tag} id=\"{heading_id(title)}\">{inline_markdown(title)}</{tag}>")
            else:
                if in_header:
                    out.append("</header>")
                    in_header = False
                out.append(f"<{tag} id=\"{heading_id(title)}\">{inline_markdown(title)}</{tag}>")
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", line)
        if bullet:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_markdown(bullet.group(1))}</li>")
            continue
        close_list()
        out.append(f"<p>{inline_markdown(line)}</p>")

    close_list()
    if in_header:
        out.append("</header>")
    out.append("</body></html>")
    return "".join(out)


def find_browser() -> str | None:
    for name in BROWSER_NAMES:
        path = shutil.which(name)
        if path:
            return path
    for path in MAC_BROWSER_PATHS:
        if path.is_file() and path.stat().st_mode & 0o111:
            return str(path)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("README.md"), help="Markdown source file")
    parser.add_argument("--output", type=Path, default=Path("CV-Daniel-Sacco.pdf"), help="PDF destination")
    args = parser.parse_args()

    browser = find_browser()
    if not browser:
        print("No se encontró Chromium/Google Chrome. Instálalo y vuelve a ejecutar el script.", file=sys.stderr)
        return 1

    html_path = args.output.with_suffix(".html")
    html_path.write_text(render(args.input.read_text(encoding="utf-8")), encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer", f"--print-to-pdf={args.output}", html_path.resolve().as_uri()],
            check=True,
        )
    finally:
        html_path.unlink(missing_ok=True)
    print(f"PDF generado: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
