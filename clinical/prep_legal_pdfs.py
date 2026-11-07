#!/usr/bin/env python3
"""Split legal PDFs on the attending's computer so the phone does not have to.

Cloud agents cannot see the laptop disk unless `cursor worker start` is running
on that machine. Cursor Desktop file access is a different session. Phone
uploads also fail around ~46 MB (the whole Plunkett file). This script chunks
a folder of owned PDFs into `textbooks/` (gitignored). It does not buy books,
fetch mirrors, or git-add PDFs.

  python3 clinical/prep_legal_pdfs.py --in ~/Books --out textbooks
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

DEFAULT_PAGES = 40
DEFAULT_MAX_MB = 8.0


def _slug(name: str) -> str:
    stem = Path(name).stem
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return slug[:60] or "book"


def split_pdf(src: Path, out_dir: Path, pages: int, max_mb: float) -> list[Path]:
    reader = PdfReader(str(src))
    n = len(reader.pages)
    if n == 0:
        return []
    written: list[Path] = []
    slug = _slug(src.name)
    start = 0
    max_bytes = int(max_mb * 1024 * 1024)
    pages_now = pages
    while start < n:
        writer = PdfWriter()
        end = min(start + pages_now, n)
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        dest = out_dir / f"{slug}-p{start + 1:04d}-{end:04d}.pdf"
        tmp = dest.with_suffix(".pdf.tmp")
        with tmp.open("wb") as fh:
            writer.write(fh)
        if tmp.stat().st_size > max_bytes and (end - start) > 1:
            tmp.unlink()
            pages_now = max(1, (end - start) // 2)
            continue
        tmp.replace(dest)
        written.append(dest)
        start = end
        pages_now = pages
    return written


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Chunk legal PDFs for cloud-agent study. Never commits them.")
    p.add_argument("--in", dest="src", required=True, help="Folder of owned PDFs, or one PDF")
    p.add_argument("--out", dest="out", default="textbooks", help="Gitignored output folder")
    p.add_argument("--pages", type=int, default=DEFAULT_PAGES)
    p.add_argument("--max-mb", type=float, default=DEFAULT_MAX_MB)
    args = p.parse_args(argv)
    src = Path(args.src).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        files = [src]
    elif src.is_dir():
        files = sorted(src.glob("*.pdf"))
    else:
        print(f"not found: {src}", file=sys.stderr)
        return 2
    if not files:
        print("no PDFs in input", file=sys.stderr)
        return 2
    total = 0
    for pdf in files:
        chunks = split_pdf(pdf, out, args.pages, args.max_mb)
        total += len(chunks)
        print(f"{pdf.name}: {len(chunks)} chunk(s)")
        for c in chunks:
            print(f"  {c.name}  {c.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"done: {total} files in {out}")
    print("Do not git add textbooks/. Attach chunks here, or leave them for a desktop/self-hosted agent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
