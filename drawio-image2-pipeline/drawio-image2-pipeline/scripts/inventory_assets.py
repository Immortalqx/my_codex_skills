#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
DOC_EXTS = {".pdf", ".pptx", ".md"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def image_size(path: Path) -> str:
    try:
        from PIL import Image
        with Image.open(path) as im:
            return f"{im.width}x{im.height}"
    except Exception:
        return "unknown"


def pdf_pages(path: Path) -> str:
    try:
        import fitz
        doc = fitz.open(path)
        return str(doc.page_count)
    except Exception:
        try:
            from pypdf import PdfReader
            return str(len(PdfReader(str(path)).pages))
        except Exception:
            return "unknown"


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory visual/source assets for research figure drafting.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--asset-dir", required=True)
    parser.add_argument("--copy-images", action="store_true", help="Copy discovered image files into asset-dir.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    asset_dir = Path(args.asset_dir).resolve()
    asset_dir.mkdir(parents=True, exist_ok=True)

    images = []
    docs = []
    for path in iter_files(root):
        ext = path.suffix.lower()
        if ext in IMAGE_EXTS:
            size = image_size(path)
            images.append((path, size))
            if args.copy_images:
                dest = asset_dir / path.name
                if dest.resolve() != path.resolve():
                    if dest.exists():
                        dest = asset_dir / f"{path.stem}_{abs(hash(str(path))) % 100000}{path.suffix}"
                    shutil.copy2(path, dest)
        elif ext in DOC_EXTS:
            meta = ""
            if ext == ".pdf":
                meta = f"{pdf_pages(path)} pages"
            docs.append((path, meta))

    lines = []
    lines.append("# Asset Manifest")
    lines.append("")
    lines.append(f"Root: `{root}`")
    lines.append("")
    lines.append("## Images")
    lines.append("")
    if images:
        lines.append("| Path | Size | Suggested use | Decision |")
        lines.append("| --- | --- | --- | --- |")
        for path, size in images:
            rel = path.relative_to(root) if path.is_relative_to(root) else path
            lines.append(f"| `{rel}` | {size} | method/setup/result/qualitative/other | use / reject: reason |")
    else:
        lines.append("No image files found.")
    lines.append("")
    lines.append("## Source Documents")
    lines.append("")
    if docs:
        lines.append("| Path | Info | Figure extraction decision |")
        lines.append("| --- | --- | --- |")
        for path, meta in docs:
            rel = path.relative_to(root) if path.is_relative_to(root) else path
            lines.append(f"| `{rel}` | {meta} | inspect / render pages / reject: reason |")
    else:
        lines.append("No source documents found.")
    lines.append("")
    lines.append("## Required Decision")
    lines.append("")
    lines.append("Before drawing, mark relevant assets as `use` or write a rejection reason. Do not silently ignore useful paper figures.")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"asset_manifest={out}")
    print(f"images={len(images)} docs={len(docs)}")


if __name__ == "__main__":
    main()
