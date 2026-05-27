#!/usr/bin/env python3
import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


ENDPOINT = "https://www.right.codes/draw/v1/images/generations"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SAFE_PNG_CHUNKS = {b"IHDR", b"PLTE", b"tRNS", b"IDAT", b"IEND"}


def load_api_key() -> str:
    for name in ("RIGHTCODE_API_KEY", "OPENAI_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value

    roots = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        roots.append(Path(codex_home))
    roots.append(Path.home() / ".codex")

    for root in roots:
        if not root.exists():
            continue
        for auth in root.rglob("rightcode/auth.json"):
            try:
                data = json.loads(auth.read_text(encoding="utf-8"))
            except Exception:
                continue
            value = data.get("OPENAI_API_KEY") or data.get("RIGHTCODE_API_KEY")
            if value:
                return value

    raise SystemExit(
        "No API key found. Set RIGHTCODE_API_KEY or OPENAI_API_KEY, "
        "or configure an existing rightcode/auth.json under CODEX_HOME."
    )


def strip_png_metadata(raw: bytes) -> bytes:
    """Remove embedded draw.io/text metadata while preserving PNG pixels."""
    if not raw.startswith(PNG_SIGNATURE):
        return raw

    pos = len(PNG_SIGNATURE)
    chunks = [PNG_SIGNATURE]
    try:
        while pos + 8 <= len(raw):
            length = int.from_bytes(raw[pos : pos + 4], "big")
            chunk_type = raw[pos + 4 : pos + 8]
            chunk_start = pos
            chunk_end = pos + 12 + length
            if chunk_end > len(raw):
                return raw
            if chunk_type in SAFE_PNG_CHUNKS:
                chunks.append(raw[chunk_start:chunk_end])
            pos = chunk_end
            if chunk_type == b"IEND":
                break
    except Exception:
        return raw

    sanitized = b"".join(chunks)
    return sanitized if sanitized.startswith(PNG_SIGNATURE) else raw


def image_data_url(path: Path) -> str:
    raw = path.read_bytes()
    if path.suffix.lower() == ".png":
        raw = strip_png_metadata(raw)
    b64 = base64.b64encode(raw).decode("ascii")
    suffix = path.suffix.lower().lstrip(".")
    mime = "jpeg" if suffix in {"jpg", "jpeg"} else "png"
    return f"data:image/{mime};base64,{b64}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Call Right Code GPT-Image-2 image generation.")
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--input-image", action="append", default=[])
    parser.add_argument("--out", required=True)
    parser.add_argument("--response-json", required=True)
    parser.add_argument("--size", default="1536x1024")
    parser.add_argument("--model", default="gpt-image-2")
    args = parser.parse_args()

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    payload = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "response_format": "url",
    }
    if args.input_image:
        payload["image"] = [image_data_url(Path(p)) for p in args.input_image]

    api_key = load_api_key()
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {detail[:2000]}") from exc

    response_path = Path(args.response_json)
    response_path.parent.mkdir(parents=True, exist_ok=True)
    response_path.write_text(body, encoding="utf-8")

    data = json.loads(body)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    item = data["data"][0]
    if "url" in item:
        with urllib.request.urlopen(item["url"], timeout=240) as img_response:
            out.write_bytes(img_response.read())
    elif "b64_json" in item:
        out.write_bytes(base64.b64decode(item["b64_json"]))
    else:
        raise SystemExit("No url or b64_json found in image response.")

    usage = data.get("usage")
    print(f"image_path={out}")
    print(f"response_json={response_path}")
    if usage:
        print(f"usage={usage}")


if __name__ == "__main__":
    main()
