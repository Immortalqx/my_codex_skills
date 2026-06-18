#!/usr/bin/env python3
"""Locate figure captions in a paper and crop the figure body from the page.

Pipeline:

  1. Read the ``=== PAGE N ===`` markers in ``text/full.txt`` (written by
     ``extract_text.py``) and find lines matching ``Figure N: ...``
     (also ``Fig. N:``, ``Figure N.``, and ``Table N``).
  2. For each match, identify the page number from the marker.
  3. Read ``pages/pages.json`` (written by ``render_pages.py``) for the actual
     page-number width used in the render output.
  4. Open the corresponding ``page_NN.png`` from the pages directory.
  5. Crop the figure body using one of two strategies:
     a. ``--bbox "x,y,w,h"`` - manual crop, in pixels relative to the page PNG.
     b. ``--bbox-mode auto-top`` - locate the caption via PyMuPDF, then crop
        from the page top down to just above the caption.
  6. Write ``figures/figure_N.png`` and ``figures/figure_N.meta.json`` with
     the page number, caption text, and crop region so the agent can
     visually QA the crop.

The agent must visually QA every crop. The script tries to do the right
thing automatically but a wrong crop is common (caption included,
neighbouring figure included, figure clipped). Re-run with a manual
``--bbox`` if the auto-crop is wrong.

Install PyMuPDF with: ``pip install pymupdf``.
Install Pillow with: ``pip install pillow``.

Usage:
  python locate_figures.py <paper.pdf> --text-dir <text-dir> --pages-dir <pages-dir> --output <figures-dir>
  python locate_figures.py <paper.pdf> --text-dir <text-dir> --pages-dir <pages-dir> --output <figures-dir> --figure 3
  python locate_figures.py <paper.pdf> --text-dir <text-dir> --pages-dir <pages-dir> --output <figures-dir> --figure 2 --bbox 80,90,400,300
  python locate_figures.py <paper.pdf> --text-dir <text-dir> --pages-dir <pages-dir> --output <figures-dir> --list
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CAPTION_PATTERNS = [
    re.compile(r"^\s*figure\s+(\d+)[\s.:]", re.IGNORECASE),
    re.compile(r"^\s*fig\.\s*(\d+)[\s.:]", re.IGNORECASE),
    re.compile(r"^\s*table\s+(\d+)[\s.:]", re.IGNORECASE),
]

PAGE_MARKER_RE = re.compile(r"^===\s*PAGE\s+(\d+)\s*===\s*$", re.IGNORECASE)


def find_captions(full_text_path: Path) -> list[dict[str, object]]:
    """Return a list of ``{number, kind, caption, page, line_idx}`` for every figure or table caption.

    Walks ``full.txt`` and records every line that starts a caption.
    """
    if not full_text_path.exists():
        raise FileNotFoundError(f"Expected {full_text_path} (run extract_text.py first).")
    text = full_text_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    current_page: int | None = None
    out: list[dict[str, object]] = []
    for idx, line in enumerate(lines):
        m_page = PAGE_MARKER_RE.match(line.strip())
        if m_page:
            current_page = int(m_page.group(1))
            continue
        for pat in CAPTION_PATTERNS:
            m = pat.match(line)
            if m and current_page is not None:
                out.append({
                    "number": int(m.group(1)),
                    "kind": "table" if pat.pattern.startswith(r"^\s*table") else "figure",
                    "caption": line.strip(),
                    "page": current_page,
                    "line_idx": idx,
                })
                break
    return out


def read_pages_sidecar(pages_dir: Path) -> int:
    """Return the page-number width recorded in ``pages/pages.json``. Defaults to 3 if the sidecar is missing."""
    sidecar = pages_dir / "pages.json"
    if not sidecar.exists():
        return 3
    try:
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        return int(data.get("width", 3))
    except (json.JSONDecodeError, ValueError, TypeError):
        return 3


def locate_caption_bbox_pdf(
    pdf_path: Path,
    page_num: int,
    caption_substring: str,
) -> tuple[float, float, float, float] | None:
    """Return the ``(x0, y0, x1, y1)`` PDF-point bbox of the caption text block on a page.

    Returns None if PyMuPDF is unavailable or the caption cannot be located.
    """
    try:
        import fitz  # type: ignore
    except ImportError:
        return None
    with fitz.open(pdf_path) as doc:
        if page_num < 1 or page_num > doc.page_count:
            return None
        page = doc.load_page(page_num - 1)
        needle = caption_substring[:30].lower()
        for block in page.get_text("blocks"):
            # block = (x0, y0, x1, y1, text, block_no, block_type)
            if len(block) < 5:
                continue
            text = (block[4] or "").lower()
            if needle in text:
                return (float(block[0]), float(block[1]), float(block[2]), float(block[3]))
    return None


def find_figure_region(
    page_png: Path,
    page_num: int,
    caption_bbox: tuple[float, float, float, float] | None,
    pdf_path: Path,
) -> tuple[int, int, int, int]:
    """Return a ``(x, y, w, h)`` crop in PNG pixels of the figure body.

    Strategy:
      - If a caption bbox is given, crop from the page top to just above
        the caption (with a small margin to avoid clipping the figure).
      - Fall back to the upper 60% of the page if the caption cannot be
        located precisely.
    """
    from PIL import Image  # type: ignore

    img = Image.open(page_png)
    page_w, page_h = img.size

    if caption_bbox is None:
        # Default: top 60% of the page.
        return (0, 0, page_w, int(page_h * 0.6))

    # Convert PDF-point bbox to pixel bbox.
    try:
        import fitz  # type: ignore
    except ImportError:
        return (0, 0, page_w, int(page_h * 0.6))

    with fitz.open(pdf_path) as doc:
        page = doc.load_page(page_num - 1)
        zoom = img.size[1] / page.rect.height
    cap_x0, cap_y0, cap_x1, cap_y1 = caption_bbox
    cap_y0_px = int(cap_y0 * zoom)
    cap_x0_px = int(cap_x0 * zoom)
    cap_x1_px = int(cap_x1 * zoom)

    # The figure body sits above the caption. Crop from page top to caption
    # top, full width if the caption spans the page, or column width if the
    # caption is in a single column.
    page_x0 = 0
    page_x1 = page_w
    # If the caption is in a single column, restrict width to that column.
    if cap_x0_px > page_w * 0.1:
        page_x0 = max(0, cap_x0_px - 10)
    if cap_x1_px < page_w * 0.9:
        page_x1 = min(page_w, cap_x1_px + 10)

    crop_y0 = 0
    crop_y1 = max(1, cap_y0_px - 5)  # 5px margin above the caption
    return (page_x0, crop_y0, page_x1 - page_x0, crop_y1 - crop_y0)


def render_one(
    pdf_path: Path,
    text_dir: Path,
    pages_dir: Path,
    output_dir: Path,
    figure_number: int,
    bbox: tuple[int, int, int, int] | None,
) -> dict[str, object] | None:
    """Locate one figure and write the crop + meta JSON. Returns the meta dict or None."""
    captions = find_captions(text_dir / "full.txt")
    target = [c for c in captions if c["kind"] == "figure" and c["number"] == figure_number]
    if not target:
        print(f"[ERROR] No figure {figure_number} caption found in {text_dir / 'full.txt'}.", file=sys.stderr)
        return None
    # If the same figure is captioned on multiple pages (rare), use the first occurrence.
    cap = target[0]
    page_num = int(cap["page"])
    width = read_pages_sidecar(pages_dir)
    page_png = pages_dir / f"page_{page_num:0{width}d}.png"
    if not page_png.exists():
        print(f"[ERROR] Page render for page {page_num} not found in {pages_dir}.", file=sys.stderr)
        return None

    from PIL import Image  # type: ignore

    output_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(page_png)
    out_path = output_dir / f"figure_{figure_number}.png"
    meta: dict[str, object] = {
        "figure_number": figure_number,
        "caption": cap["caption"],
        "page": page_num,
        "page_png": str(page_png),
    }

    if bbox is not None:
        x, y, w, h = bbox
        x = max(0, min(x, img.size[0] - 1))
        y = max(0, min(y, img.size[1] - 1))
        w = max(1, min(w, img.size[0] - x))
        h = max(1, min(h, img.size[1] - y))
        meta["crop"] = {"x": x, "y": y, "w": w, "h": h, "mode": "manual"}
        img.crop((x, y, x + w, y + h)).save(out_path)
    else:
        cap_bbox = locate_caption_bbox_pdf(pdf_path, page_num, str(cap["caption"]))
        crop = find_figure_region(page_png, page_num, cap_bbox, pdf_path)
        meta["crop"] = {"x": crop[0], "y": crop[1], "w": crop[2], "h": crop[3], "mode": "auto-top"}
        if cap_bbox is not None:
            meta["caption_bbox_pdf_points"] = {
                "x0": cap_bbox[0], "y0": cap_bbox[1], "x1": cap_bbox[2], "y1": cap_bbox[3],
            }
        img.crop(crop).save(out_path)

    meta_path = output_dir / f"figure_{figure_number}.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Wrote {out_path}")
    print(f"     Caption: {cap['caption'][:80]}{'...' if len(str(cap['caption'])) > 80 else ''}")
    print(f"     Page:    {page_num}")
    print(f"     Crop:    {meta['crop']}")
    return meta


def list_figures(text_dir: Path) -> list[dict[str, object]]:
    """Print every figure / table caption found in ``full.txt``. Does not crop anything."""
    captions = find_captions(text_dir / "full.txt")
    if not captions:
        print(f"[ERROR] No captions found in {text_dir / 'full.txt'}.", file=sys.stderr)
        return []
    print(f"Found {len(captions)} caption(s):")
    for c in captions:
        print(f"  {c['kind']:6s} {c['number']:>3}  page {c['page']:>3}  {str(c['caption'])[:80]}")
    return captions


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Locate figure captions in a paper and crop the figure body from the page."
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF.")
    parser.add_argument(
        "--text-dir", type=Path, required=True,
        help="Directory containing full.txt (from extract_text.py).",
    )
    parser.add_argument(
        "--pages-dir", type=Path, required=True,
        help="Directory containing page_NN.png renders and pages.json sidecar (from render_pages.py).",
    )
    parser.add_argument(
        "--output", "-o", type=Path, required=True,
        help="Output directory for figure_N.png and figure_N.meta.json.",
    )
    parser.add_argument(
        "--figure", type=int, default=None,
        help="Figure number to locate (e.g. 3 for 'Figure 3'). If omitted, lists all captions.",
    )
    parser.add_argument(
        "--bbox", default=None,
        help="Manual crop box 'x,y,w,h' in PNG pixels. Overrides auto-locate.",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List every figure / table caption found, then exit. Does not write crops.",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"[ERROR] PDF not found: {args.pdf}", file=sys.stderr)
        return 1

    if args.list:
        captions = list_figures(args.text_dir)
        return 0 if captions else 1

    if args.figure is None:
        print("[ERROR] Pass --figure N to crop figure N, or --list to enumerate captions.", file=sys.stderr)
        return 1

    bbox: tuple[int, int, int, int] | None = None
    if args.bbox is not None:
        try:
            parts = [int(p.strip()) for p in args.bbox.split(",")]
            if len(parts) != 4:
                raise ValueError
            bbox = (parts[0], parts[1], parts[2], parts[3])
        except ValueError:
            print("[ERROR] --bbox must be 'x,y,w,h' with four integers.", file=sys.stderr)
            return 1

    meta = render_one(
        args.pdf, args.text_dir, args.pages_dir, args.output,
        args.figure, bbox,
    )
    if meta is None:
        return 1
    print()
    print("Visual QA required: open the cropped figure and confirm it shows the")
    print("intended content. Re-run with --bbox if the crop is wrong.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
