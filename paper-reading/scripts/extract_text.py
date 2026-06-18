#!/usr/bin/env python3
"""Extract structured text from a PDF for paper-reading.

Writes ``<output>/full.txt`` with explicit ``=== PAGE N ===`` markers between
pages, plus a small ``<output>/pages.json`` sidecar with per-page character
counts. The two output files are the contract: ``split_sections.py`` and
``locate_figures.py`` read ``full.txt`` and trust the marker format exactly.

Backend priority:
  1. PyMuPDF (imported as ``fitz``) - preferred, no external binary.
  2. ``pdftotext`` from Poppler - fallback if PyMuPDF is not installed.

Install PyMuPDF with: ``pip install pymupdf``.

Usage:
  python extract_text.py <paper.pdf> --output <text-dir>
  python extract_text.py <paper.pdf> --output <text-dir> --pages 1-5
  python extract_text.py <paper.pdf> -o <text-dir> --backend pdftotext
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def extract_with_pymupdf(pdf_path: Path) -> list[tuple[int, str]]:
    """Return a list of ``(page_number_1_indexed, page_text)`` using PyMuPDF."""
    import fitz  # type: ignore

    out: list[tuple[int, str]] = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            out.append((i, page.get_text("text")))
    return out


def extract_with_pdftotext(pdf_path: Path) -> list[tuple[int, str]]:
    """Fallback: shell out to ``pdftotext`` for each page."""
    if shutil.which("pdftotext") is None:
        raise RuntimeError(
            "Neither PyMuPDF nor pdftotext is available. "
            "Install one of them: 'pip install pymupdf' or install Poppler."
        )

    out: list[tuple[int, str]] = []
    total_pages: int | None = None
    if shutil.which("pdfinfo") is not None:
        proc = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                import re
                m = re.match(r"^Pages:\s*(\d+)\s*$", line.strip())
                if m:
                    total_pages = int(m.group(1))
                    break
    if total_pages is None:
        # Conservative upper bound; pdftotext will return empty for missing pages.
        total_pages = 200

    for i in range(1, total_pages + 1):
        proc = subprocess.run(
            ["pdftotext", "-raw", "-f", str(i), "-l", str(i), str(pdf_path), "-"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if proc.returncode != 0:
            break
        text = proc.stdout
        if not text.strip() and i > 1:
            # An empty page in the middle usually means we went past the end.
            # Continue one more page to be safe, then break.
            continue
        out.append((i, text))
    return out


def write_output(
    pages: list[tuple[int, str]],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write the concatenated text and the per-page JSON sidecar."""
    output_dir.mkdir(parents=True, exist_ok=True)
    txt_path = output_dir / "full.txt"
    json_path = output_dir / "pages.json"

    lines: list[str] = []
    char_counts: dict[str, int] = {}
    for page_num, text in pages:
        lines.append(f"=== PAGE {page_num} ===")
        lines.append(text.rstrip())
        lines.append("")
        char_counts[str(page_num)] = len(text)

    txt_path.write_text("\n".join(lines), encoding="utf-8")
    json_path.write_text(
        json.dumps({"page_count": len(pages), "char_counts": char_counts}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return txt_path, json_path


def parse_page_range(spec: str, total: int) -> list[int] | None:
    """Parse a string like ``1-5`` or ``1,3,7`` or ``2-`` into a list of page numbers.

    Returns None when ``spec`` is empty (meaning: all pages).
    """
    if not spec:
        return None
    pages: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            a_s, b_s = a.strip(), b.strip()
            start = int(a_s) if a_s else 1
            end = int(b_s) if b_s else total
            pages.update(range(start, end + 1))
        else:
            pages.add(int(chunk))
    return sorted(p for p in pages if 1 <= p <= total)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract structured text from a PDF for paper-reading."
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF.")
    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output directory. Will be created if missing.",
    )
    parser.add_argument(
        "--pages",
        default="",
        help="Page range to extract, e.g. '1-5', '1,3,7', '2-'. Default: all pages.",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "pymupdf", "pdftotext"],
        default="auto",
        help="Extraction backend. Default: auto (try PyMuPDF, then pdftotext).",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"[ERROR] PDF not found: {args.pdf}", file=sys.stderr)
        return 1

    pages: list[tuple[int, str]] = []
    backend_used = ""
    if args.backend in ("auto", "pymupdf"):
        try:
            pages = extract_with_pymupdf(args.pdf)
            backend_used = "pymupdf"
        except ImportError:
            if args.backend == "pymupdf":
                print("[ERROR] PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
                return 1
    if not pages and args.backend in ("auto", "pdftotext"):
        try:
            pages = extract_with_pdftotext(args.pdf)
            backend_used = "pdftotext"
        except RuntimeError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1

    if not pages:
        print("[ERROR] No pages extracted. Check that the PDF is valid.", file=sys.stderr)
        return 1

    selection = parse_page_range(args.pages, len(pages))
    if selection is not None:
        pages = [(n, t) for n, t in pages if n in selection]

    txt_path, json_path = write_output(pages, args.output)
    print(f"[OK] Extracted {len(pages)} page(s) using {backend_used}.")
    print(f"     Text:  {txt_path}")
    print(f"     Index: {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
