#!/usr/bin/env python3
"""Heuristically split extracted PDF text into named sections.

Reads the ``=== PAGE N ===`` markers written by ``extract_text.py`` and tries
to identify canonical academic-paper sections: abstract, introduction, related
work, method, experiments, conclusion, references, appendix. Output is a JSON
file mapping section name to a list of page numbers.

The heuristics are deliberately simple. They cover the common ML / CV / NLP
layout (numbered headings like "1 Introduction", "2 Related Work", ...) and
fail gracefully for papers with non-standard section ordering. The agent is
expected to inspect the output and re-assign pages if the heuristics misfire.

Usage:
  python split_sections.py <text-dir>
  python split_sections.py <text-dir> --output <text-dir>/sections.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# A section name and the regexes that should match its heading line.
# Order matters: the first match wins for a given page.
SECTION_PATTERNS: list[tuple[str, list[re.Pattern[str]]]] = [
    ("abstract", [
        re.compile(r"^\s*abstract\s*$", re.IGNORECASE),
        re.compile(r"^\s*abstract\s*[:.]", re.IGNORECASE),
    ]),
    ("introduction", [
        re.compile(r"^\s*1\.?\s+introduction\s*$", re.IGNORECASE),
        re.compile(r"^\s*1\s+introduction\s*$", re.IGNORECASE),
        re.compile(r"^\s*introduction\s*$", re.IGNORECASE),
    ]),
    ("related_work", [
        re.compile(r"^\s*2\.?\s+related\s+work", re.IGNORECASE),
        re.compile(r"^\s*related\s+work", re.IGNORECASE),
        re.compile(r"^\s*background", re.IGNORECASE),
        re.compile(r"^\s*prior\s+work", re.IGNORECASE),
    ]),
    ("method", [
        re.compile(r"^\s*3\.?\s+method", re.IGNORECASE),
        re.compile(r"^\s*3\.?\s+approach", re.IGNORECASE),
        re.compile(r"^\s*3\.?\s+model", re.IGNORECASE),
        re.compile(r"^\s*3\.?\s+framework", re.IGNORECASE),
        re.compile(r"^\s*method(s|ology)?\s*$", re.IGNORECASE),
    ]),
    ("experiments", [
        re.compile(r"^\s*4\.?\s+experiment", re.IGNORECASE),
        re.compile(r"^\s*4\.?\s+evaluation", re.IGNORECASE),
        re.compile(r"^\s*experiments?\s*$", re.IGNORECASE),
        re.compile(r"^\s*evaluation\s*$", re.IGNORECASE),
        re.compile(r"^\s*empirical\s+(evaluation|results)", re.IGNORECASE),
    ]),
    ("results", [
        re.compile(r"^\s*5\.?\s+results", re.IGNORECASE),
    ]),
    ("discussion", [
        re.compile(r"^\s*6\.?\s+discussion", re.IGNORECASE),
    ]),
    ("conclusion", [
        re.compile(r"^\s*7\.?\s+conclu", re.IGNORECASE),
        re.compile(r"^\s*conclusions?\s*$", re.IGNORECASE),
    ]),
    ("limitations", [
        re.compile(r"^\s*limitations?\s*$", re.IGNORECASE),
        re.compile(r"^\s*limitations?\s+and\s+future", re.IGNORECASE),
    ]),
    ("references", [
        re.compile(r"^\s*references\s*$", re.IGNORECASE),
        re.compile(r"^\s*bibliography\s*$", re.IGNORECASE),
    ]),
    ("appendix", [
        re.compile(r"^\s*appendix(\s+[a-z])?", re.IGNORECASE),
        re.compile(r"^\s*supplementary", re.IGNORECASE),
    ]),
]

PAGE_MARKER_RE = re.compile(r"^===\s*PAGE\s+(\d+)\s*===\s*$", re.IGNORECASE)


def split_into_pages(text: str) -> list[tuple[int, list[str]]]:
    """Group text lines by page, based on the markers written by extract_text.py."""
    pages: list[tuple[int, list[str]]] = []
    current_page: int | None = None
    current_lines: list[str] = []
    for line in text.splitlines():
        m = PAGE_MARKER_RE.match(line.strip())
        if m:
            if current_page is not None:
                pages.append((current_page, current_lines))
            current_page = int(m.group(1))
            current_lines = []
        elif current_page is not None:
            current_lines.append(line)
    if current_page is not None:
        pages.append((current_page, current_lines))
    return pages


def detect_sections(pages: list[tuple[int, list[str]]]) -> dict[str, list[int]]:
    """Walk pages in order, assign each page to the most recently detected section.

    A page is assigned to the section that began on an earlier page and has not
    been replaced by a new section heading on a later page. Pages before any
    section heading is detected are placed in the "front_matter" bucket
    (typically the abstract and the table of contents).
    """
    section_starts: list[tuple[str, int]] = []
    for page_num, lines in pages:
        for line in lines[:50]:  # only inspect the top of each page
            stripped = line.strip()
            for name, patterns in SECTION_PATTERNS:
                if any(p.match(stripped) for p in patterns):
                    section_starts.append((name, page_num))
                    break
            else:
                continue
            break

    # Deduplicate consecutive duplicates (same section repeated on a single page)
    deduped: list[tuple[str, int]] = []
    for name, page in section_starts:
        if deduped and deduped[-1][0] == name:
            continue
        deduped.append((name, page))

    # Build page->section map
    page_section: dict[int, str] = {}
    section_order = [name for name, _ in deduped]
    for page_num, _ in pages:
        active = "front_matter"
        for name, start_page in deduped:
            if start_page <= page_num:
                active = name
        page_section[page_num] = active

    # Group pages by section
    out: dict[str, list[int]] = {}
    for page_num, section in page_section.items():
        out.setdefault(section, []).append(page_num)

    # Stable order: front_matter first, then detected order, then anything else.
    final: dict[str, list[int]] = {}
    final["front_matter"] = out.pop("front_matter", [])
    for name in section_order:
        if name in out:
            final[name] = out.pop(name)
    for name, pages_list in out.items():
        final[name] = pages_list
    return final


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Heuristically split extracted PDF text into named sections."
    )
    parser.add_argument(
        "text_dir", type=Path,
        help="Directory containing full.txt (written by extract_text.py).",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help="Output JSON path. Default: <text_dir>/sections.json.",
    )
    args = parser.parse_args()

    txt_path = args.text_dir / "full.txt"
    if not txt_path.exists():
        print(f"[ERROR] Expected {txt_path} (run extract_text.py first).", file=sys.stderr)
        return 1

    text = txt_path.read_text(encoding="utf-8")
    pages = split_into_pages(text)
    if not pages:
        print(f"[ERROR] No pages found. Did extract_text.py run successfully?", file=sys.stderr)
        return 1

    sections = detect_sections(pages)
    out_path = args.output or (args.text_dir / "sections.json")
    out_path.write_text(
        json.dumps(sections, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] {len(pages)} page(s) split into {len(sections)} section(s).")
    for name, page_list in sections.items():
        rng = _format_range(page_list)
        print(f"     {name:20s} {rng}")
    print(f"     Wrote: {out_path}")
    return 0


def _format_range(pages: list[int]) -> str:
    """Render a list of page numbers as compact ranges, e.g. ``[1,2,3,5,7,8,9] -> '1-3, 5, 7-9'``."""
    if not pages:
        return "(empty)"
    pages = sorted(set(pages))
    ranges: list[str] = []
    start = pages[0]
    prev = pages[0]
    for p in pages[1:]:
        if p == prev + 1:
            prev = p
            continue
        ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
        start = p
        prev = p
    ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
    return ", ".join(ranges)


if __name__ == "__main__":
    sys.exit(main())
