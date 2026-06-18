#!/usr/bin/env python3
"""Render each PDF page to a PNG for figure cropping and visual reference.

The output is one PNG per page, named ``page_NN.png`` with NN zero-padded
to a width that depends on the document's total page count. The actual
width is recorded in a ``pages.json`` sidecar so downstream scripts
(``locate_figures.py``) do not need to guess.

Backend priority:
  1. PyMuPDF (imported as ``fitz``) - preferred, no external binary.
  2. ``pdftoppm`` from Poppler - fallback if PyMuPDF is not installed.
  3. Delegate to the ``pdf`` skill's ``convert_pdf_to_images.py`` if a path
     is given via ``--delegate`` (useful in environments where PyMuPDF
     and pdftoppm are both unavailable).

Install PyMuPDF with: ``pip install pymupdf``.

Usage:
  python render_pages.py <paper.pdf> --output <pages-dir>
  python render_pages.py <paper.pdf> --output <pages-dir> --dpi 200
  python render_pages.py <paper.pdf> --output <pages-dir> --first 1 --last 8
  python render_pages.py <paper.pdf> --output <pages-dir> --delegate /path/to/convert_pdf_to_images.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def compute_width(total_pages: int) -> int:
    """Pad to at least 2 digits, more if the page count requires it."""
    return max(2, len(str(total_pages)))


def render_with_pymupdf(pdf_path: Path, output_dir: Path, dpi: int, first: int | None, last: int | None) -> tuple[int, int]:
    """Render via PyMuPDF. Returns ``(pages_rendered, width)``."""
    import fitz  # type: ignore

    output_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    with fitz.open(pdf_path) as doc:
        total = doc.page_count
        start = max(1, first or 1)
        end = min(total, last or total)
        width = compute_width(total)
        for i in range(start, end + 1):
            page = doc.load_page(i - 1)
            pix = page.get_pixmap(matrix=matrix)
            out_path = output_dir / f"page_{i:0{width}d}.png"
            pix.save(out_path)
    return end - start + 1, width


def render_with_pdftoppm(pdf_path: Path, output_dir: Path, dpi: int, first: int | None, last: int | None) -> tuple[int, int]:
    """Fallback: shell out to ``pdftoppm`` for each page. Returns ``(pages_rendered, width)``."""
    if shutil.which("pdftoppm") is None:
        raise RuntimeError(
            "Neither PyMuPDF nor pdftoppm is available, and no --delegate script was given. "
            "Install one of them: 'pip install pymupdf' or install Poppler."
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    # pdftoppm names files as <prefix>-NN.png; we want page_NN.png, so render
    # to a tmp prefix then rename.
    tmp_prefix = output_dir / "_tmp_page"
    cmd = ["pdftoppm", "-r", str(dpi), "-png", str(pdf_path), str(tmp_prefix)]
    if first is not None:
        cmd.extend(["-f", str(first)])
    if last is not None:
        cmd.extend(["-l", str(last)])
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"pdftoppm failed: {(proc.stderr or proc.stdout).strip()}")

    # Rename _tmp_page-NN.png -> page_NN.png
    rendered = sorted(output_dir.glob("_tmp_page-*.png"))
    if not rendered:
        raise RuntimeError("pdftoppm produced no files.")
    # Determine padding width from the highest page number encountered.
    max_n = 0
    for p in rendered:
        stem = p.stem  # e.g., _tmp_page-7
        m = stem.rsplit("-", 1)
        if len(m) == 2:
            try:
                max_n = max(max_n, int(m[1]))
            except ValueError:
                pass
    width = compute_width(max_n)
    count = 0
    for p in rendered:
        stem = p.stem
        m = stem.rsplit("-", 1)
        if len(m) == 2:
            try:
                n = int(m[1])
            except ValueError:
                p.unlink()
                continue
            new_name = output_dir / f"page_{n:0{width}d}.png"
            p.rename(new_name)
            count += 1
    return count, width


def render_with_delegate(
    pdf_path: Path,
    output_dir: Path,
    delegate_script: Path,
    dpi: int,
) -> int:
    """Delegate to the ``pdf`` skill's convert_pdf_to_images.py. Returns ``pages_rendered``."""
    if not delegate_script.exists():
        raise RuntimeError(f"Delegate script not found: {delegate_script}")
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(delegate_script),
        str(pdf_path),
        "--output-dir", str(output_dir),
        "--dpi", str(dpi),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Delegate failed: {(proc.stderr or proc.stdout).strip()}")
    return len(list(output_dir.glob("page_*.png"))) or len(list(output_dir.glob("*.png")))


def write_pages_sidecar(output_dir: Path, width: int, rendered_pages: list[int], total_pages: int) -> Path:
    """Write a sidecar JSON describing the render output. Downstream scripts read this."""
    sidecar_path = output_dir / "pages.json"
    sidecar = {
        "total_pages": total_pages,
        "width": width,
        "rendered_pages": rendered_pages,
    }
    sidecar_path.write_text(
        json.dumps(sidecar, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return sidecar_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render each PDF page to a PNG for figure cropping."
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF.")
    parser.add_argument(
        "--output", "-o", type=Path, required=True,
        help="Output directory for page_NN.png files. Will be created if missing.",
    )
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="Render DPI. Default: 150. Use 200-300 for figures with small text.",
    )
    parser.add_argument(
        "--first", type=int, default=None,
        help="First page to render (1-indexed). Default: 1.",
    )
    parser.add_argument(
        "--last", type=int, default=None,
        help="Last page to render (1-indexed). Default: last page of the PDF.",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "pymupdf", "pdftoppm", "delegate"],
        default="auto",
        help="Rendering backend. Default: auto (try PyMuPDF, then pdftoppm).",
    )
    parser.add_argument(
        "--delegate", type=Path, default=None,
        help="Path to a renderer script (e.g., the pdf skill's convert_pdf_to_images.py). "
             "Used only when --backend is 'delegate' or when all local backends fail.",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"[ERROR] PDF not found: {args.pdf}", file=sys.stderr)
        return 1
    if args.dpi < 72 or args.dpi > 600:
        print(f"[WARN] DPI {args.dpi} is outside the typical 72-600 range.", file=sys.stderr)

    backend_used = ""
    count = 0
    width = 0
    total_pages = 0
    if args.backend in ("auto", "pymupdf"):
        try:
            import fitz  # type: ignore
            with fitz.open(args.pdf) as doc:
                total_pages = doc.page_count
            count, width = render_with_pymupdf(args.pdf, args.output, args.dpi, args.first, args.last)
            backend_used = "pymupdf"
        except ImportError:
            if args.backend == "pymupdf":
                print("[ERROR] PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
                return 1
    if not count and args.backend in ("auto", "pdftoppm"):
        try:
            count, width = render_with_pdftoppm(args.pdf, args.output, args.dpi, args.first, args.last)
            backend_used = "pdftoppm"
        except RuntimeError:
            if args.backend == "pdftoppm":
                return 1
    if not count and args.delegate is not None:
        try:
            count = render_with_delegate(args.pdf, args.output, args.delegate, args.dpi)
            # When delegating, infer width from the actual rendered files
            rendered = sorted(args.output.glob("page_*.png"))
            if rendered:
                # The widest number we have
                max_n = max(int(p.stem.split("_")[1]) for p in rendered if p.stem.split("_")[1].isdigit())
                width = compute_width(max_n)
                if not total_pages:
                    total_pages = max_n
            backend_used = f"delegate:{args.delegate}"
        except RuntimeError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
    if not count:
        print("[ERROR] No pages rendered. Install pymupdf or poppler, or pass --delegate.", file=sys.stderr)
        return 1

    # Determine which pages were rendered (for the sidecar)
    rendered_pages = sorted(int(p.stem.split("_")[1]) for p in args.output.glob("page_*.png") if p.stem.split("_")[1].isdigit())
    if not total_pages:
        total_pages = max(rendered_pages) if rendered_pages else 0

    sidecar_path = write_pages_sidecar(args.output, width, rendered_pages, total_pages)
    print(f"[OK] Rendered {count} page(s) using {backend_used} at {args.dpi} DPI (width={width}).")
    print(f"     Output:   {args.output}")
    print(f"     Sidecar:  {sidecar_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
