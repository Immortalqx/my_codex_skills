#!/usr/bin/env python3
import argparse
from pathlib import Path


def parse_pages(spec: str):
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = [int(x) for x in part.split("-", 1)]
            pages.extend(range(a, b + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def main() -> None:
    parser = argparse.ArgumentParser(description="Render selected PDF pages to PNG assets.")
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--pages", required=True, help="1-based pages, e.g. 1,3,5-7")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--dpi", type=int, default=200)
    args = parser.parse_args()

    try:
        import fitz
    except Exception as exc:
        raise SystemExit("PyMuPDF/fitz is required to render PDF pages.") from exc

    pdf = Path(args.pdf).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    zoom = args.dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    for page_num in parse_pages(args.pages):
        if page_num < 1 or page_num > doc.page_count:
            raise SystemExit(f"Page out of range: {page_num}")
        page = doc[page_num - 1]
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = out_dir / f"{pdf.stem}_page_{page_num:03d}.png"
        pix.save(out)
        print(out)


if __name__ == "__main__":
    main()
