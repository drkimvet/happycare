"""prep_legal_pdfs chunks owned books. It must not git-add PDFs."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pypdf import PdfWriter

from clinical.prep_legal_pdfs import split_pdf  # noqa: E402


class PrepLegalPdfsTests(unittest.TestCase):
    def test_splits_by_page_count(self):
        with tempfile.TemporaryDirectory() as td:
            src_dir = Path(td)
            src = src_dir / "HopperSACCM.pdf"
            writer = PdfWriter()
            for _ in range(5):
                writer.add_blank_page(width=72, height=72)
            with src.open("wb") as fh:
                writer.write(fh)
            out = src_dir / "out"
            out.mkdir()
            chunks = split_pdf(src, out, pages=2, max_mb=8)
            self.assertEqual(len(chunks), 3)
            self.assertTrue(all(p.suffix == ".pdf" for p in chunks))
            self.assertTrue(all("hopper" in p.name for p in chunks))


if __name__ == "__main__":
    unittest.main()
