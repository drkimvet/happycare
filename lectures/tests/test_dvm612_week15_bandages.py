#!/usr/bin/env python3
"""Invariants for the DVM 612 Week 15 bandage and drain lecture."""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Inches

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "assets" / "bandage" / "compose_bandage_figures.py"
BUILDER = ROOT / "build_dvm612_week15_bandages.py"
PPTX = ROOT / "DVM-612_Week15_Bandages_Drains.pptx"
SCRIPT = ROOT / "DVM-612_Week15_Instructor_Script.txt"
FOOTER = "DVM 612  |  Dr. Yujin Kim, D.V.M., Ph.D., FFCP  |  Lewyt CVM"
EXPECTED = 36
MIN_PT = 12
TITLE_PT = 30
ASSET_DIR = ROOT / "assets" / "bandage"
FIGURES = (
    "bandage_three_layers.png",
    "bandage_stirrups.png",
    "bandage_digits34.png",
    "bandage_penrose.png",
    "bandage_closed_suction.png",
    "bandage_ehmer.png",
    "bandage_velpeau.png",
)


def _runs(prs):
    for i, slide in enumerate(prs.slides, 1):
        for sh in slide.shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.text.strip() and r.font.size is not None:
                        yield i, r


class TestWeek15BandageLecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(FIG)], check=True, cwd=str(ROOT))
        subprocess.run([sys.executable, str(BUILDER)], check=True, cwd=str(ROOT))
        cls.prs = Presentation(str(PPTX))
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.blob = "\n".join(r.text for _, r in _runs(cls.prs))

    def test_slide_count_and_footer(self):
        self.assertEqual(len(self.prs.slides), EXPECTED)
        self.assertEqual(self.prs.slide_width, Inches(13.333))
        self.assertEqual(self.prs.slide_height, Inches(7.5))
        self.assertIn(FOOTER, self.blob)
        self.assertIn("WEEK 15", self.blob)

    def test_hall_type_floor(self):
        small = [(i, r.font.size.pt, r.text[:40]) for i, r in _runs(self.prs) if r.font.size.pt + 0.05 < MIN_PT]
        self.assertEqual(small, [])

    def test_no_em_dash_in_titles(self):
        bad = [
            (i, r.text)
            for i, r in _runs(self.prs)
            if r.font.size.pt >= TITLE_PT - 0.5 and "\u2014" in r.text
        ]
        self.assertEqual(bad, [])

    def test_no_teal_kicker_color_on_header_labels(self):
        teal = (0x1B, 0x6B, 0x7A)
        kickers = []
        for i, r in _runs(self.prs):
            if r.font.size.pt != 13:
                continue
            color = r.font.color.rgb
            if color and (color[0], color[1], color[2]) == teal and r.text.isupper():
                kickers.append((i, r.text))
        self.assertEqual(kickers, [])

    def test_cited_scope_and_no_owner_phi(self):
        low = self.blob.lower()
        self.assertIn("fossum", low)
        self.assertIn("merck", low)
        self.assertIn("week 15", low)
        self.assertIn("digits 3 and 4", low)
        self.assertIn("wet-to-dry", low)
        self.assertIn("never through the incision", low)
        self.assertIn("penrose", low)
        self.assertIn("ehmer", low)
        self.assertIn("velpeau", low)
        self.assertNotRegex(self.blob, r"\bMoMo\b")
        self.assertNotRegex(self.blob, r"\bWillie\b")
        self.assertNotIn("2-0 nylon", low)
        self.assertNotIn("vetrap", low)
        self.assertNotIn("elastikon", low)
        self.assertNotIn("kling", low)
        self.assertNotIn("telfa", low)
        self.assertNotIn("jackson-pratt", low)
        self.assertNotIn("jackson pratt", low)

    def test_script_keeps_vendor_homework_off_slides(self):
        self.assertIn("Vetrap", self.script)
        self.assertIn("Elastikon", self.script)
        self.assertIn("Kling", self.script)
        self.assertIn("Telfa", self.script)
        self.assertIn("Jackson-Pratt", self.script)
        self.assertNotIn("Vetrap", self.blob)
        self.assertNotIn("Elastikon", self.blob)
        self.assertNotIn("Telfa", self.blob)

    def test_original_figures_exist(self):
        missing = [name for name in FIGURES if not (ASSET_DIR / name).is_file()]
        self.assertEqual(missing, [])
        for name in FIGURES:
            self.assertGreater((ASSET_DIR / name).stat().st_size, 20_000, name)

    def test_pptx_embeds_figures(self):
        pics = [
            sh
            for slide in self.prs.slides
            for sh in slide.shapes
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE
        ]
        self.assertGreaterEqual(len(pics), 7)
        self.assertIn("Original teaching figure", self.blob)


if __name__ == "__main__":
    unittest.main()
