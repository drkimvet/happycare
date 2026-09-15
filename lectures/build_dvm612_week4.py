#!/usr/bin/env python3
"""Build DVM 612 Week 4 lecture: Preoperative evaluation, patient preparation, postoperative care.

Lewyt College of Veterinary Medicine (LIU)
Aligned to DVM 612 course outline Week 4 and course learning objectives 4, 7, 8.
Required texts: Fossum 2018; Hendrickson & Baird 2013.
"""

from pathlib import Path
import subprocess
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import nsmap, qn
from pptx.util import Emu, Inches, Pt
from lxml import etree
from copy import deepcopy

ASSETS = Path(__file__).resolve().parent / "assets"

# Keep the teaching records in sync with the lecture (preop + recovery, large type).
subprocess.check_call([sys.executable, str(Path(__file__).resolve().parent / "make_teaching_charts.py")])

# --- Brand ---
NAVY = RGBColor(0x0B, 0x2C, 0x4A)
NAVY_DK = RGBColor(0x07, 0x1C, 0x32)
GOLD = RGBColor(0xC5, 0xA3, 0x5A)
GOLD_LT = RGBColor(0xF4, 0xEB, 0xD3)
TEAL = RGBColor(0x1B, 0x6B, 0x7A)
TEAL_LT = RGBColor(0xE4, 0xF1, 0xF3)
RED = RGBColor(0x8B, 0x2E, 0x2E)
RED_LT = RGBColor(0xF8, 0xE8, 0xE8)
GREEN = RGBColor(0x2E, 0x6B, 0x4F)
GREEN_LT = RGBColor(0xE6, 0xF3, 0xEC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFFWHITE = RGBColor(0xF6, 0xF7, 0xF9)
INK = RGBColor(0x1C, 0x1C, 0x1C)
MUTED = RGBColor(0x5B, 0x64, 0x6E)
SLATE = RGBColor(0x3D, 0x4A, 0x57)

W, H = Inches(13.333), Inches(7.5)
FOOTER = "DVM 612  |  Dr. Yujin Kim, D.V.M., Ph.D., FFCP  |  Lewyt CVM"

# Hall-readable without shouting: titles 30, body 18, cards 16, kicker 13, footer 12.
# References on the last slide may be 13 pt. Floor is 12 pt (footer).
PT_FOOTER = 12
PT_KICKER = 13
PT_TITLE = 30
PT_BODY = 18
PT_CARD = 16
PT_CARD_TITLE = 18
PT_SMALL = 14
PT_REF = 13
MIN_PT = 12

prs = Presentation()
prs.slide_width = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]


def _solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _rgb_hex(c):
    return f"{c[0]:02X}{c[1]:02X}{c[2]:02X}"


def add_rect(slide, l, t, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    _solid(sh, color)
    return sh


def add_round(slide, l, t, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    _solid(sh, color)
    # tighter corners
    try:
        sh.adjustments[0] = 0.08
    except Exception:
        pass
    return sh


def set_tf(tf, text, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT, font="Calibri", anchor=MSO_ANCHOR.TOP):
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}.get(anchor, "t"))
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    return p


def add_text(slide, l, t, w, h, text, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT, font="Calibri", anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(l, t, w, h)
    set_tf(box.text_frame, text, size=size, bold=bold, color=color, align=align, font=font, anchor=anchor)
    return box


def add_runs(slide, l, t, w, h, paragraphs, anchor=MSO_ANCHOR.TOP):
    """paragraphs: list of dicts {text, size, bold, color, align, space_after, space_before}"""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr"}.get(anchor, "t"))
    except Exception:
        pass
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = para.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(para.get("space_after", 6))
        p.space_before = Pt(para.get("space_before", 0))
        p.level = para.get("level", 0)
        run = p.add_run()
        run.text = para["text"]
        run.font.size = Pt(para.get("size", 18))
        run.font.bold = para.get("bold", False)
        run.font.color.rgb = para.get("color", INK)
        run.font.name = para.get("font", "Calibri")
        run.font.italic = para.get("italic", False)
    return box


def add_bullets(slide, l, t, w, h, items, size=18, color=INK, bullet_color=GOLD, spacing=8):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(spacing)
        p.level = 0
        # manual bullet
        run = p.add_run()
        run.text = "▸  " + item
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = "Calibri"
        run.font.bold = False
    return box


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def add_pic(slide, name, l, t, w, h):
    path = ASSETS / name
    if not path.exists():
        path = ASSETS / "real" / name
    if not path.exists():
        raise FileNotFoundError(name)
    return slide.shapes.add_picture(str(path), l, t, w, h)


def footer_bar(slide, num, total):
    add_rect(slide, 0, Inches(7.18), W, Inches(0.32), NAVY)
    add_text(slide, Inches(0.35), Inches(7.18), Inches(10.8), Inches(0.32), FOOTER, size=PT_FOOTER, color=GOLD_LT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(11.2), Inches(7.18), Inches(1.8), Inches(0.32), f"{num}  /  {total}", size=PT_FOOTER, color=WHITE, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def header_bar(slide, kicker=""):
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    add_rect(slide, 0, Inches(0.12), W, Inches(0.08), NAVY)
    if kicker:
        add_text(slide, Inches(0.5), Inches(0.22), Inches(12.3), Inches(0.32), kicker.upper(), size=PT_KICKER, bold=True, color=TEAL)


def content_chrome(slide, title, kicker, num, total):
    add_rect(slide, 0, 0, W, H, OFFWHITE)
    header_bar(slide, kicker)
    add_rect(slide, 0, Inches(0.12), Inches(0.12), Inches(7.0), GOLD)
    add_text(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.58), title, size=PT_TITLE, bold=True, color=NAVY)
    footer_bar(slide, num, total)


def card(slide, l, t, w, h, title, body, fill=WHITE, title_color=NAVY, accent=GOLD):
    add_round(slide, l, t, w, h, fill)
    add_rect(slide, l, t, Inches(0.10), h, accent)
    add_text(slide, l + Inches(0.28), t + Inches(0.12), w - Inches(0.4), Inches(0.36), title, size=PT_CARD_TITLE, bold=True, color=title_color)
    add_text(slide, l + Inches(0.28), t + Inches(0.50), w - Inches(0.4), h - Inches(0.62), body, size=PT_CARD, color=SLATE)


def pill(slide, l, t, w, h, text, fill=GOLD, text_color=NAVY):
    add_round(slide, l, t, w, h, fill)
    add_text(slide, l, t, w, h, text, size=PT_SMALL, bold=True, color=text_color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# Slide registry: we first plan TOTAL then build
# Rebuild footers after all slides are created.
# and set numbers at the end.

SLIDES = []  # list of (slide, notes_text) after creation? We'll stamp at end.


def new_content(title, kicker=""):
    s = prs.slides.add_slide(BLANK)
    add_rect(s, 0, 0, W, H, OFFWHITE)
    header_bar(s, kicker)
    add_rect(s, 0, Inches(0.12), Inches(0.12), Inches(7.0), GOLD)
    add_text(s, Inches(0.5), Inches(0.50), Inches(12.3), Inches(0.58), title, size=PT_TITLE, bold=True, color=NAVY)
    return s


def new_section(part, title, subtitle, minutes):
    s = prs.slides.add_slide(BLANK)
    add_rect(s, 0, 0, W, H, NAVY)
    add_rect(s, 0, 0, W, Inches(0.14), GOLD)
    add_rect(s, 0, Inches(7.36), W, Inches(0.14), GOLD)
    add_text(s, Inches(0.7), Inches(2.15), Inches(12), Inches(0.4), part.upper(), size=PT_SMALL, bold=True, color=GOLD)
    add_text(s, Inches(0.7), Inches(2.55), Inches(12), Inches(1.1), title, size=32, bold=True, color=WHITE)
    add_text(s, Inches(0.7), Inches(3.75), Inches(12), Inches(0.7), subtitle, size=PT_BODY, color=GOLD_LT)
    pill(s, Inches(0.7), Inches(4.7), Inches(2.4), Inches(0.42), minutes, fill=GOLD, text_color=NAVY)
    return s


def stamp_footers():
    total = len(prs.slides)
    for i, slide in enumerate(prs.slides, 1):
        dark = False
        try:
            rgb = slide.shapes[0].fill.fore_color.rgb
            dark = rgb == NAVY
        except Exception:
            dark = False
        if dark:
            add_text(slide, Inches(11.2), Inches(7.18), Inches(1.7), Inches(0.32), f"{i}  /  {total}", size=PT_FOOTER, color=GOLD, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
        else:
            footer_bar(slide, i, total)


def assert_min_font(prs, min_pt=MIN_PT):
    bad = []
    for i, slide in enumerate(prs.slides, 1):
        for sh in slide.shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if not r.text.strip() or r.font.size is None:
                        continue
                    pt = r.font.size.pt
                    if pt + 0.05 < min_pt:
                        bad.append(f"slide {i}: {pt:.0f} pt  {r.text[:50]!r}")
    if bad:
        raise SystemExit("Type below hall floor (" + str(min_pt) + " pt):\n" + "\n".join(bad))


# =============================================================================
# SLIDES  (38 pages)
# =============================================================================

# 1 Title
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, Inches(0), Inches(0), Inches(0.22), H, GOLD)
add_text(s, Inches(0.75), Inches(0.95), Inches(12), Inches(0.40), "LONG ISLAND UNIVERSITY  ·  LEWYT COLLEGE OF VETERINARY MEDICINE", size=16, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(1.45), Inches(12), Inches(0.40), "DVM 612  ·  PRINCIPLES OF SURGERY", size=20, bold=True, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(1.95), Inches(12), Inches(2.0), "Preoperative Evaluation,\nPatient Preparation &\nPostoperative Care", size=36, bold=True, color=WHITE)
add_text(s, Inches(0.75), Inches(4.15), Inches(12), Inches(0.50), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP", size=24, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(4.70), Inches(12), Inches(0.40), "Lecture  |  38 slides  |  60 minutes", size=18, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(5.20), Inches(12), Inches(0.90), "Exam, labs, ASA, then prep. Own the first 24 hours.\nTwo hospital cases are ASA examples only.", size=20, color=WHITE)
add_text(s, Inches(0.75), Inches(6.20), Inches(12), Inches(0.70), "Required: Fossum 2018; Hendrickson & Baird 2013.\nAlso used: ECFVG CPE Manual of Administration 2026, Anesthesia and Surgery.", size=16, color=GOLD)
notes(s, "Welcome. This hour is preoperative evaluation, patient and surgeon preparation, and postoperative care. The competency list is the 2026 CPE Manual of Administration, Anesthesia and Surgery chapters, taught as DVM 612, not as an exam-prep course. Two hospital patients are only ASA examples: Willie, compensated, Status 3-E, sedated for an ear clean; MoMo, uncompensated, Status 4-E, exploratory cancelled. Owner identifiers stay off these slides. Thirty-eight slides. If discussion runs, protect antiseptics, ready-for-prep, and recovery.")

# 2 Learning objectives
s = new_content("Learning objectives", "DVM 612 Week 4  ·  38 slides")
items = [
    "Assign ASA after today’s PE and labs. Correct deficits. Write premed, induction, MAC, tube, bag, and fluid rate.",
    "If albumin is low: find the cause, delay elective if you can, and do not flood with crystalloid.",
    "Prep for aseptic surgery: clip, labeled antiseptics, minimum contact time, four-quadrant drape, closed glove.",
    "Name a break in asepsis and correct it, before or after the incision. Classify the wound: clean, clean-contaminated, contaminated, or dirty.",
    "Write the postop plan, the surgical report, and 24-hour emergency criteria.",
]
add_bullets(s, Inches(0.55), Inches(1.20), Inches(12.2), Inches(3.9), items, size=20, spacing=12)
add_round(s, Inches(0.5), Inches(5.35), Inches(12.3), Inches(0.85), GOLD_LT)
add_text(s, Inches(0.75), Inches(5.45), Inches(11.9), Inches(0.65), "Exam → labs → ASA → correct deficits → premed → induce → ready for prep → clip, prep, drape → first 24 hours.", size=16, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Read the five objectives aloud. Timer: protect antiseptics, draping, and recovery. The two hospital patients are ASA practice, not the point of the hour.")

# 3 SSI
s = new_content("Prepare the patient and yourself", "Then own the first 24 hours. CPE MOA 2026 Surgery competencies.")
card(s, Inches(0.5), Inches(1.2), Inches(4.0), Inches(2.35), "Causes of SSI", "Hair, skin flora, hypothermia, poor hemostasis, dead space, and breaks in asepsis.", fill=WHITE, accent=TEAL)
card(s, Inches(4.7), Inches(1.2), Inches(4.0), Inches(2.35), "Client-owned patients", "Elective OHE patients go home to the owner after recovery. Documentation and the discharge conversation are part of the operation.", fill=WHITE, accent=GOLD)
card(s, Inches(8.9), Inches(1.2), Inches(3.9), Inches(2.35), "Set before you cut", "Analgesia, antibiotics, temperature management, and client expectations are set in the preoperative period.", fill=WHITE, accent=GREEN)
add_round(s, Inches(0.5), Inches(3.75), Inches(12.3), Inches(3.2), WHITE)
add_text(s, Inches(0.75), Inches(3.9), Inches(11.8), Inches(0.4), "Surgeon responsibilities", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.4), Inches(11.8), Inches(2.3), [
    "Prepare the patient for a surgical procedure.",
    "Prepare yourself for a surgical procedure.",
    "Perform the procedure. Then own the first 24 hours: hemorrhage from a weak ligature, or herniation from a weak linea, is still the operation (CPE MOA 2026 Surgery).",
], size=18, spacing=8)
notes(s, "A closure that hemorrhages in recovery is a failed surgery. The first 24 hours are part of the operation.")

# 4 Halsted
s = new_content("Halsted’s principles", "Each principle has a preoperative or postoperative action")
principles = [
    ("Gentle tissue handling", "Prep trauma, clipper burn, and crushing towel clamps are tissue handling."),
    ("Meticulous hemostasis", "Preop coagulopathy; postop hemorrhage is a 24-hour emergency."),
    ("Preserve blood supply", "Place clamps and bandages so skin perfusion is preserved."),
    ("Strict asepsis", "Patient preparation, surgeon preparation, and draping."),
    ("No tension", "Plan incision location and closure now, not after the fascia splits."),
    ("Accurate apposition", "Postop incision care protects the apposition you create."),
    ("Obliterate dead space", "Plan dead space now: sutures, bandage, or a drain with a written pull plan."),
]
for i, (t, d) in enumerate(principles):
    col = i % 2
    row = i // 2
    x = Inches(0.5) + Inches(col * 6.4)
    y = Inches(1.18) + Inches(row * 1.42)
    w = Inches(12.3) if i == 6 else Inches(6.2)
    if i == 6:
        x = Inches(0.5)
    add_round(s, x, y, w, Inches(1.32), WHITE)
    add_rect(s, x, y, Inches(0.10), Inches(1.32), GOLD)
    add_text(s, x + Inches(0.28), y + Inches(0.10), w - Inches(0.4), Inches(0.42), f"{i+1}.  {t}", size=18, bold=True, color=NAVY)
    add_text(s, x + Inches(0.28), y + Inches(0.54), w - Inches(0.4), Inches(0.68), d, size=16, color=SLATE)
notes(s, "Two minutes, then move. Every Halsted principle has a preop or postop action, not just an intraoperative one.")

# 5 Continuum
s = new_content("The perioperative continuum", "Two team clocks. CPE MOA 2026 Anesthesia and Surgery.")
stages = [
    ("PRE-OP", "PE, labs, ASA\nCorrect deficits\nPremed, induce, MAC\nETT, bag, fluids", TEAL),
    ("PREP", "Ready for clip:\nairway, IV, plane\nHair, skin, position\nDrape, gown, glove", GOLD),
    ("INTRA-OP", "Announce incision\nHold asepsis\nHalsted, temp, pain\nRecord every 5–10 min", NAVY),
    ("POST-OP", "Airway, pain, heat\nWatch 24 hours\nReport + discharge\nRecheck plan", GREEN),
]
for i, (t, b, c) in enumerate(stages):
    x = Inches(0.45) + Inches(i * 3.2)
    add_round(s, x, Inches(1.18), Inches(3.0), Inches(3.95), WHITE)
    add_rect(s, x, Inches(1.18), Inches(3.0), Inches(0.62), c)
    add_text(s, x, Inches(1.18), Inches(3.0), Inches(0.62), t, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.16), Inches(1.92), Inches(2.68), Inches(3.05), b, size=16, color=INK, align=PP_ALIGN.CENTER)
    if i < 3:
        add_text(s, x + Inches(2.7), Inches(2.85), Inches(0.55), Inches(0.4), "→", size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
add_round(s, Inches(0.45), Inches(5.28), Inches(6.15), Inches(1.70), TEAL_LT)
add_text(s, Inches(0.65), Inches(5.40), Inches(5.80), Inches(0.40), "Anesthesia clock  ·  ready for surgical prep", size=16, bold=True, color=TEAL)
add_text(s, Inches(0.65), Inches(5.82), Inches(5.80), Inches(1.00), "From the preoperative exam: airway in and secured, machine on, patent IV running, surgical plane, monitoring started. Then call for prep (CPE MOA 2026 Anesthesia).", size=15, color=INK)
add_round(s, Inches(6.80), Inches(5.28), Inches(6.05), Inches(1.70), GOLD_LT)
add_text(s, Inches(7.00), Inches(5.40), Inches(5.70), Inches(0.40), "Surgery clock  ·  last skin suture", size=16, bold=True, color=NAVY)
add_text(s, Inches(7.00), Inches(5.82), Inches(5.70), Inches(1.00), "From the start of patient preparation to the last skin suture, including re-gowning. Then own the first 24 hours (CPE MOA 2026 Surgery).", size=15, color=INK)
notes(s, "Do not teach this as a CPE station. Teach the clocks. Anesthesia owns exam through a patient who is ready for clippers: tube in, cuff up, machine on, IV running, surgical plane. Surgery owns clip through the last skin suture, then both own the first 24 hours. Cite ECFVG CPE Manual of Administration 2026, Anesthesia and Surgery sections.")

# 6 Preop evaluation
s = new_content("Preoperative physical examination", "CPE MOA 2026 Appendix 3: TPR, mm/CRT, then PCV, TP, BUN. Then ASA. Then premed.")
pe_boxes = [
    ("T  ·  HR  ·  RR", "Temperature, heart rate, respiratory rate. Write the numbers. Do not copy yesterday’s chart."),
    ("mm / CRT", "Mucous membrane color and capillary refill. Pink vs pale vs injected. CRT in seconds."),
    ("Heart and lungs", "Auscultate both sides. Record any murmur, arrhythmia, or crackles before you choose drugs."),
    ("Hydration + site", "Skin tent, tacky mm. Look at the surgical site: pyoderma, heat, pain. Abdomen if you might open it."),
]
for i, (t, d) in enumerate(pe_boxes):
    col = i % 2
    row = i // 2
    x = Inches(0.45) + Inches(col * 6.45)
    y = Inches(1.10) + Inches(row * 1.42)
    add_round(s, x, y, Inches(6.25), Inches(1.32), WHITE)
    add_rect(s, x, y, Inches(0.10), Inches(1.32), TEAL)
    add_text(s, x + Inches(0.28), y + Inches(0.10), Inches(5.80), Inches(0.36), t, size=18, bold=True, color=NAVY)
    add_text(s, x + Inches(0.28), y + Inches(0.50), Inches(5.80), Inches(0.72), d, size=16, color=SLATE)
add_rect(s, Inches(0.45), Inches(4.02), Inches(12.40), Inches(0.42), NAVY)
add_text(s, Inches(0.55), Inches(4.02), Inches(12.20), Inches(0.42), "Minimum labs on the anesthesia record  ·  PCV, TP, BUN  (CPE MOA 2026 Appendix 3)", size=16, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
lab_trio = [
    ("PCV", "Oxygen-carrying capacity. Anemia vs hemoconcentration. With TP: dehydration vs blood loss."),
    ("TP", "Protein / oncotic pressure. High with PCV: dehydration. Low: loss, liver, or dilution. Changes fluids and healing."),
    ("BUN", "Kidney, hydration, GI bleed. Azotemia: skip NSAIDs, rethink fluids, maybe do not cut today."),
]
for i, (t, d) in enumerate(lab_trio):
    x = Inches(0.45) + Inches(i * 4.15)
    add_round(s, x, Inches(4.52), Inches(4.00), Inches(2.55), WHITE)
    add_rect(s, x, Inches(4.52), Inches(4.00), Inches(0.48), GOLD)
    add_text(s, x, Inches(4.52), Inches(4.00), Inches(0.48), t, size=20, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), Inches(5.10), Inches(3.70), Inches(1.82), d, size=16, color=INK)
notes(s, "This is the preoperative exam the record actually holds. CPE MOA 2026 Appendix 3: heart rate, respiratory rate, mucous membranes and CRT, temperature, then PCV, TP, and BUN. Request those three. Interpret them. Then write ASA. Then premed IM or SQ. Do not premedicate before the examination. Add other labs if the PE says so. A normal CBC does not make a vestibular dog Status 1. Azotemia can cancel the cut.")

# 7 ASA
s = new_content("ASA physical status", "Grubb et al. 2020 AAHA table. CPE MOA 2026 Anesthesia Appendix 2 uses the same 1–5 scale.")
rows = [
    ("1", "Normal healthy patient", "Healthy patient for neutering", GREEN),
    ("2", "Patient with mild systemic disease", "Well compensated mild mitral degeneration", TEAL),
    ("3", "Patient with moderate systemic disease", "Cat with CKD, IRIS stage 3", GOLD),
    ("4", "Severe systemic disease; constant threat to life", "Hemoabdomen, bleeding splenic mass", RED),
    ("5", "Moribund; not expected to survive without the operation", "Hypotensive, hypothermic, obtunded septic cat", NAVY),
]
add_rect(s, Inches(0.45), Inches(1.15), Inches(12.4), Inches(0.48), NAVY)
add_text(s, Inches(0.55), Inches(1.15), Inches(2.4), Inches(0.48), "ASA status", size=16, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3.0), Inches(1.15), Inches(5.8), Inches(0.48), "Definition", size=16, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.9), Inches(1.15), Inches(3.8), Inches(0.48), "Example", size=16, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, (asa, defn, ex, c) in enumerate(rows):
    y = Inches(1.68) + Inches(i * 0.95)
    add_round(s, Inches(0.45), y, Inches(12.4), Inches(0.88), WHITE)
    add_rect(s, Inches(0.45), y, Inches(2.35), Inches(0.88), c)
    add_text(s, Inches(0.45), y, Inches(2.35), Inches(0.88), f"Status {asa}", size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.95), y + Inches(0.08), Inches(5.75), Inches(0.72), defn, size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(8.85), y + Inches(0.08), Inches(3.80), Inches(0.72), ex, size=16, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
add_round(s, Inches(0.45), Inches(6.48), Inches(12.4), Inches(0.55), GOLD_LT)
add_text(s, Inches(0.65), Inches(6.48), Inches(12.05), Inches(0.55), "E = emergency. Status 3 is compensated. Status 4 is uncompensated and a threat to life. Today’s PE writes the number.", size=16, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Read the 2020 AAHA table with MOA Appendix 2: Status 1 healthy, Status 2 mild and compensated, Status 3 moderate and compensated, Status 4 a constant threat to life, Status 5 moribund. E means emergency. Then use the two hospital patients only as practice: compensated vestibular crisis is 3-E; uncompensated azotemia that threatens life is 4-E.")

# 8 ASA practice
s = new_content("ASA practice cases", "Assign status, then say whether you proceed today")
cases = [
    ("A", "Healthy 8-month Labrador. Elective OHE. Normal PE.", "ASA Status 1  ·  proceed", GREEN_LT, GREEN),
    ("B", "10-year Beagle, BCS 8/9, grade 2/6 murmur, no CHF. Dental.", "ASA Status 2  ·  proceed with a monitoring plan", TEAL_LT, TEAL),
    ("C", "Cavalier, acute ataxia, AS otitis, murmur. CV stable.", "ASA Status 3-E. Compensated emergency. Sedation plan.", GOLD_LT, GOLD),
    ("D", "Vomiting cat. Looks like FB. T 98.0 °F, HR 200, tacky mm.", "ASA Status 4-E. Uncompensated emergency. Image and labs first. Do not cut today.", RED_LT, RED),
]
for i, (let, stem, ans, fill, acc) in enumerate(cases):
    y = Inches(1.18) + Inches(i * 1.42)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.30), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.85), Inches(1.30), acc)
    add_text(s, Inches(0.5), y, Inches(0.85), Inches(1.30), let, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.55), y + Inches(0.12), Inches(10.9), Inches(0.52), stem, size=18, color=INK)
    add_text(s, Inches(1.55), y + Inches(0.70), Inches(10.9), Inches(0.45), ans, size=18, bold=True, color=acc)
notes(s, "Cold-call four students. C is a compensated emergency (sedation). D is uncompensated; labs cancelled the exploratory. The names on later slides are only these examples.")

# 9 Willie
s = new_content("Willie, ASA Status 3-E", "ASA example for tonight’s ear clean and for a later TECA-LBO. DexSP: skip NSAID.")
add_round(s, Inches(0.5), Inches(1.12), Inches(12.3), Inches(1.15), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.20), Inches(11.8), Inches(1.00), "Acute ataxia ~1 hour. Fell off the couch twice. Cytopoint for allergies. Vitals: T 100.8 °F, HR 132, RR 52, mm pink, CRT 2 s, quiet/dull. ASA Status 3-E: moderate systemic disease that is still compensated (acute vestibular disease plus AS otitis plus murmur). Pink, walking, kidneys normal.", size=16, color=NAVY)
card(s, Inches(0.5), Inches(2.40), Inches(4.0), Inches(2.85), "Left ear (AS)", "Brown and bloody discharge. Pedal reflex at the pinna base. Canal patent. Cartilage hardened. Tympanic membrane visible but swollen.", accent=TEAL)
card(s, Inches(4.7), Inches(2.40), Inches(4.0), Inches(2.85), "Neuro exam", "Circling left. Horizontal nystagmus, fast left, slow right. Right knuckling. Treat as central vestibular disease until MRI.", accent=GOLD)
card(s, Inches(8.9), Inches(2.40), Inches(3.9), Inches(2.85), "Also on PE", "Grade II/VI left systolic murmur. Heavy tartar. Soft non-painful abdomen. Compensated tonight.", accent=RED)
add_round(s, Inches(0.5), Inches(5.40), Inches(12.3), Inches(1.55), WHITE)
add_text(s, Inches(0.75), Inches(5.50), Inches(11.8), Inches(1.35), "Tonight: CBC WNL. DexSP already given: skip NSAID. Alfaxalone sedation, deep left-ear clean, cytology/culture, 3-view films. Confine. MRI if neurologic signs persist. If TECA-LBO is needed later, assign a new ASA that morning and re-check the murmur, steroid history, and ear class.", size=16, color=INK)
notes(s, "Willie is an ASA example, not the thesis of the hour. Tonight is a sedated ear clean. The same findings, DexSP, and murmur are what you re-score if TECA-LBO is planned later. Record the murmur. Right-sided knuckling with left circling: treat as central vestibular plus otitis. Skip NSAID after DexSP.")

# 10 MoMo
s = new_content("MoMo, ASA Status 4-E", "6 yo SF DSH, 4.25 kg, BCS 5/9. This is her, before the exploratory was cancelled.")
add_pic(s, "momo.jpg", Inches(0.40), Inches(1.12), Inches(4.42), Inches(5.90))
add_round(s, Inches(4.98), Inches(1.12), Inches(7.85), Inches(1.28), RED_LT)
add_text(s, Inches(5.18), Inches(1.20), Inches(7.50), Inches(1.12), "Acute vomiting and lethargy. Two vomits. Household construction. Possible FB. T 98.0 °F, HR 200, RR 30, mm pink tacky, CRT <2 s, QAR. ASA Status 4-E: uncompensated disease that is a constant threat to life.", size=15, color=NAVY)
card(s, Inches(4.98), Inches(2.52), Inches(7.85), Inches(1.28), "Why this looked surgical", "FB obstruction was on the list. Mildly enlarged abdomen. That is how cats get booked for an exploratory.", accent=GOLD)
card(s, Inches(4.98), Inches(3.90), Inches(7.85), Inches(1.28), "What the PE showed", "Heart/lungs normal. Ambulatory ×4. Dehydrated. Quiet and recumbent in this photograph. The PE did not prove a foreign body.", accent=TEAL)
card(s, Inches(4.98), Inches(5.28), Inches(7.85), Inches(1.74), "Image, labs, then cancel", "Right kidney fluid-filled and non-functional on AUS. Progressive azotemia on fluids (creatinine 3.0 → 4.71). Skip NSAIDs. Cancel the exploratory. Owner elected humane euthanasia. Record the decision.", accent=RED)
notes(s, "This slide is an ASA example, not the point of the hour. Pause on the photograph. Be respectful; this cat died. Cold-call: who would have clipped her on history alone? The photograph is a quiet, recumbent cat. It does not prove a foreign body. Status 3 would be compensated kidney disease. Rising creatinine, hypothermia, and a non-functional kidney made this Status 4-E.")

# 11 Diagnostics
s = new_content("Pre-anesthetic assessment", "CPE MOA 2026 Appendix 3 page 1: today’s PE, then PCV, TP, BUN. Interpret. Then circle ASA.")
add_round(s, Inches(0.40), Inches(1.08), Inches(12.55), Inches(0.70), GOLD_LT)
add_text(
    s,
    Inches(0.55),
    Inches(1.12),
    Inches(12.25),
    Inches(0.62),
    "PCV / TP: EDTA tube → spin hematocrit → read PCV → snap the capillary tube → refractometer TP.  BUN: chemistry or Azo stick.  Request, record, interpret. Then ASA. Then premed IM/SQ. Not before the exam.",
    size=16,
    color=NAVY,
    anchor=MSO_ANCHOR.MIDDLE,
)
add_pic(s, "preanesthetic_assessment_table.png", Inches(0.28), Inches(1.86), Inches(12.78), Inches(5.24))
notes(s, "This is Appendix 3 page 1 of the CPE MOA 2026 anesthesia record, taught as a table, not as the copyrighted form. The blanks are weight, HR, RR, mucous membranes and CRT, temperature, other PE findings, PCV, TP, BUN, other labs, then ASA 1 through 5. Perform and record the preoperative examination. Request, record, and interpret the minimum labs. Assign ASA. PCV and TP method: EDTA, spin, read PCV, snap the capillary tube, refractometer TP. Do not invent percentages. A normal CBC does not write Status 1. Azotemia can cancel the cut. High PCV plus high TP is dehydration. Low PCV plus low TP is blood loss. High BUN: skip NSAIDs.")

# 12 CBC/chem
s = new_content("Laboratory values inform risk", "Teaching bands, not an ASA table. Grubb et al. 2020: today’s PE writes ASA.")
headers = ("Finding", "Typical healthy adult", "Repeat / stabilize first")
labrows = [
    ("PCV", "Within reference", "Anemia: use severity and chronicity (Grubb 2020)"),
    ("TP", "Within reference", "High with PCV: dehydration. Low: loss / dilution"),
    ("BUN", "Within reference", "Azotemia: skip NSAID, rethink fluids and the cut"),
    ("Potassium", "Within reference", ">6.0 mEq/L (Grubb 2020: correct first)"),
    ("Albumin", "Within reference", "<2.0 g/dL: edema, poor healing (Pardo 2024)"),
]
add_rect(s, Inches(0.45), Inches(1.18), Inches(12.4), Inches(0.55), NAVY)
add_text(s, Inches(0.55), Inches(1.18), Inches(3.5), Inches(0.55), headers[0], size=16, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(4.1), Inches(1.18), Inches(4.0), Inches(0.55), headers[1], size=16, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.2), Inches(1.18), Inches(4.4), Inches(0.55), headers[2], size=16, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, (a, b, c) in enumerate(labrows):
    y = Inches(1.80) + Inches(i * 0.92)
    add_round(s, Inches(0.45), y, Inches(12.4), Inches(0.84), WHITE)
    add_text(s, Inches(0.65), y, Inches(3.3), Inches(0.84), a, size=18, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(4.1), y, Inches(4.0), Inches(0.84), b, size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(8.2), y, Inches(4.4), Inches(0.84), c, size=16, color=RED, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(6.50), Inches(12.2), Inches(0.50), "MOA minimum is PCV, TP, BUN. A normal CBC does not assign Status 1. Azotemia can cancel the cut. Low albumin is a deficit, not an ASA number.", size=16, color=NAVY)
notes(s, "Do not call these ASA cutoffs. The anesthesia record’s minimum labs are PCV, TP, and BUN. AAHA 2020 lists K greater than 6.0 as a condition to correct before anesthesia. Pardo 2024: albumin less than 2.0 grams per deciliter is a negative prognostic indicator. Do not invent PCV cutoffs as ASA numbers.")

# 13 Premed, induction, MAC
s = new_content("Anesthetic drug protocol", "Healthy sequence, then one worked example. Write drug, concentration, dose, volume, route.")
pills = [
    (TEAL, "1. Premed after ASA", "IM or SQ. Not before the exam. Healthy: DKT or BAA. The table below is not the default."),
    (GOLD, "2. Induce IV to effect", "Alfaxalone, propofol, or ketamine + benzo. Then intubate."),
    (NAVY, "3. Iso or sevo to MAC", "Premed lowers MAC. Circle the inhalant you used."),
]
for i, (c, t, dtl) in enumerate(pills):
    x = Inches(0.40) + Inches(i * 4.28)
    add_round(s, x, Inches(1.08), Inches(4.12), Inches(1.18), WHITE)
    add_rect(s, x, Inches(1.08), Inches(4.12), Inches(0.38), c)
    add_text(s, x, Inches(1.08), Inches(4.12), Inches(0.38), t, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.12), Inches(1.50), Inches(3.88), Inches(0.68), dtl, size=14, color=INK)
add_pic(s, "anesthesia_protocol_record.png", Inches(0.28), Inches(2.32), Inches(12.78), Inches(4.80))
notes(s, "This is Appendix 3 pages 2 and 3, taught as an original record, not the copyrighted form. The three steps at the top are the general sequence. The filled table is one worked example: ear disease, DexSP already given, murmur. Healthy default is not that table. Students write drug, concentration, dose, volume, and route. Then IV fluid name and rate. Then why. Do not invent milligrams.")

# 14 Stabilize
s = new_content("Correct deficits before you cut", "Grubb et al. 2020: stabilize first. Pardo et al. 2024: albumin <2.0 g/dL.")
cols = [
    ("Correct these first", GREEN, "Grubb et al. 2020, before anesthesia:\n\nDehydration / hypovolemia\nK+ >6.0 mEq/L\npH <7.2\nGlucose <60 mg/dL\nHypothermia <99 °F\nAnemia (severity, chronicity)\nLife-threatening arrhythmia\nCHF, cyanosis, pneumothorax\nOliguria / anuria\nUncontrolled pain or anxiety"),
    ("If albumin is low", GOLD, "Find the cause: GI loss, kidney, liver, exudate, starvation.\n\nDelay elective surgery if you can treat and feed.\n\n<2.0 g/dL: edema, poor perfusion, poor wound healing (Pardo 2024).\n\nPlasma: about 20–25 mL/kg to raise albumin 0.5 g/dL. Often impractical.\n\nSpecies-specific albumin if severe and you must operate. Human albumin can cause anaphylaxis.\n\nDo not flood with crystalloid when the problem is oncotic pressure."),
    ("If you still operate", RED, "Delay elective for pyoderma over the site.\n\nEmergency: resuscitate volume, then cut. You cannot wait for albumin to normalize in GDV or septic abdomen.\n\nGentle tissue handling. Obliterate dead space. Warm the patient. Nutrition as soon as the gut allows.\n\nRising creatinine that threatens life: cancel the elective or exploratory cut."),
]
for i, (t, c, b) in enumerate(cols):
    x = Inches(0.45) + Inches(i * 4.25)
    add_round(s, x, Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
    add_rect(s, x, Inches(1.2), Inches(4.05), Inches(0.6), c)
    add_text(s, x, Inches(1.2), Inches(4.05), Inches(0.6), t, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.18), Inches(1.92), Inches(3.70), Inches(4.55), b, size=14, color=INK)
notes(s, "Read the Grubb 2020 list: correct potassium greater than 6, pH less than 7.2, glucose less than 60, hypothermia, dehydration, before you induce. Then albumin: Pardo 2024 AAHA fluids, less than 2.0 grams per deciliter is edema and poor healing. Delay elective. Treat the cause. Plasma is a poor albumin replacement, 20 to 25 milliliters per kilogram for half a gram. Do not crystalloid-flood a low-oncotic patient. Emergency: resuscitate and operate. A cancelled cut after you find uncompensated azotemia is a successful preoperative evaluation.")

# 15 Fasting + consent
s = new_content("Fasting and informed consent", "2020 AAHA Anesthesia and Monitoring Guidelines; then the risk talk")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.4), "Fasting (Grubb et al. 2020 AAHA)", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(0.65), Inches(1.78), Inches(5.75), Inches(4.7), [
    "Healthy adult dog/cat: food 4–6 h; water until premedication.",
    "Some hospitals still use 8–12 h NPO. Teach aspiration versus hypoglycemia.",
    "Neonates / <2 kg: food fast no longer than 1–2 h.",
    "Brachycephalics: same fasting as the adult or neonate row. Pre-oxygenate 3 min with 100% O2 (Grubb 2020). Extubate when they can protect the airway, not at the first swallow.",
    "Ask what was eaten this morning. Clients feed ‘just a biscuit.’",
    "Diabetics: write the insulin dose and a small meal with anesthesia before drop-off.",
], size=16, spacing=6)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(5.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.4), "Consent, then file it", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(7.00), Inches(1.78), Inches(5.65), Inches(4.7), [
    "Procedure name in plain language, and the reason.",
    "Benefits, alternatives including medical management, and what happens if we wait.",
    "Material risks in one sentence each: anesthesia death, hemorrhage, infection, dehiscence. After OHE, name urinary incontinence.",
    "Estimate: what is included and what is not.",
    "Resuscitation code / DNR before induction.",
    "File the signed form. Then start induction.",
], size=16, spacing=6)
notes(s, "Cite Grubb et al., 2020 AAHA Anesthesia and Monitoring Guidelines: healthy adults, food 4 to 6 hours, water until premedication. Neonates and patients under 2 kg: food fast no longer than 1 to 2 hours. Pre-oxygenation: 3 minutes of 100 percent oxygen gives almost 6 minutes of saturation. Brachycephalics: delay extubation until they can protect the airway. Mention DNR.")

# 16 ASA, tube, bag, fluid rate (MOA Appendix 3 fields)
s = new_content("ASA, tube, bag, and fluid rate", "CPE MOA 2026 Appendix 3: ASA, ETT size, bag, circuit, IV fluid name/rate, fresh-gas flow.")
formulas = [
    (GOLD, NAVY, "Endotracheal tube", "ID mm  =  (kg / 4)  +  3.5", "Dog start. ±0.5 mm ready. Largest through arytenoids (Grubb 2020). Cat: 3.0–4.5 mm (not the dog formula)."),
    (NAVY, GOLD, "Reservoir bag", "mL  =  kg  ×  60,  round UP", "Round up to 0.5, 1, 2, or 3 L. NRC if <3–5 kg. Circle if larger. Leak-test, then OPEN the pop-off."),
    (TEAL, WHITE, "IV fluid rate", "Dog  kg × 5   ·   cat  kg × 3–5", "mL/hr. Balanced crystalloid (Pardo 2024). Not 10 mL/kg/hr. Willie: 13.7 × 5 = 69 mL/hr."),
]
for i, (hdr, hfg, title, formula, detail) in enumerate(formulas):
    x = Inches(0.40) + Inches(i * 4.28)
    add_round(s, x, Inches(1.08), Inches(4.12), Inches(1.48), WHITE)
    add_rect(s, x, Inches(1.08), Inches(4.12), Inches(0.34), hdr)
    add_text(s, x, Inches(1.08), Inches(4.12), Inches(0.34), title, size=16, bold=True, color=hfg, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.08), Inches(1.44), Inches(3.96), Inches(0.40), formula, size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.12), Inches(1.84), Inches(3.88), Inches(0.66), detail, size=14, color=INK)
add_pic(s, "anesthesia_setup_table.png", Inches(0.28), Inches(2.62), Inches(12.78), Inches(4.50))
notes(s, "Board three formulas, then fill the table the way CPE MOA 2026 Appendix 3 is filled: circle ASA, write ETT size, bag, rebreathing versus non-rebreathing, IV fluid name and rate, fresh-gas flow. Do not project the copyrighted form. Dog tube: kilograms divided by 4, plus 3.5. A 13.7 kg dog: start 7.0 millimeter, 6.5 and 7.5 in the hand. Bag: kilograms times 60, round up. 822 milliliters is a 1 liter bag, circle. Fluids: Pardo 2024, dog 5 milliliters per kilogram per hour; write 69 milliliters per hour. Circle FGF: 2 to 3 liters per minute at induction, then 20 to 40 milliliters per kilogram per minute, minimum 500 milliliters per minute (Grubb 2020). NRC 200 to 400 milliliters per kilogram per minute. After the tube is in: inhalant to effect. Premed already lowered MAC. Then clip, sterile prep, and drape. Do not teach tube math as if a sedated ear-clean patient was intubated.")

# 17 Willie record
s = new_content("Willie’s perioperative record", "Page 1 of the teaching record: PE, PCV/TP/BUN, ASA. Complete before the first drug.")
add_pic(s, "anesthesia_record_willie.png", Inches(0.28), Inches(1.08), Inches(12.78), Inches(5.95))
notes(s, "Walk the large boxes: ASA Status 3-E before alfaxalone. PCV, TP, BUN WNL. Skip NSAID after DexSP. Recovery is on the same page. Drug protocol is slide 13. The intra-op chart is slide 30. Tube and bag numbers are only if you intubate.")

# 18 MoMo record
s = new_content("MoMo’s perioperative record", "Exploratory cancelled. Record the decision.")
add_pic(s, "anesthesia_record_momo.png", Inches(0.28), Inches(1.08), Inches(12.78), Inches(5.95))
notes(s, "The form is not only for patients who get clipped. Preop boxes and SURGERY CANCELLED are the document. Say it once, respectfully, then continue.")

# 19 Abx
s = new_content("Surgical wound classification", "Clean, clean-contaminated, contaminated, dirty. Then decide antibiotics. Fossum 2018; Frey et al. 2022.")
classes = [
    (GREEN, "1. Clean", "No infection. Hollow viscus not entered.\n\nElective OHE, orchiectomy, simple skin mass.\n\nSkip routine prophylaxis (Frey 2022)."),
    (TEAL, "2. Clean-contaminated", "GI, respiratory, or urinary tract entered under control. Minor break in asepsis.\n\nCystotomy. Enterotomy without spillage."),
    (GOLD, "3. Contaminated", "Fresh open trauma. Major viscus spillage. Major break in sterile technique.\n\nTime IV prophylaxis. Fix the break."),
    (RED, "4. Dirty / infected", "Pus, abscess, old trauma, perforated viscus with peritonitis.\n\nWillie’s ear. Pyometra with pus.\n\nThis is treatment, not prophylaxis."),
]
for i, (c, t, b) in enumerate(classes):
    col = i % 2
    row = i // 2
    x = Inches(0.45) + Inches(col * 6.45)
    y = Inches(1.12) + Inches(row * 2.35)
    add_round(s, x, y, Inches(6.25), Inches(2.20), WHITE)
    add_rect(s, x, y, Inches(6.25), Inches(0.48), c)
    add_text(s, x, y, Inches(6.25), Inches(0.48), t, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.22), y + Inches(0.58), Inches(5.85), Inches(1.50), b, size=16, color=INK)
add_round(s, Inches(0.45), Inches(5.90), Inches(12.40), Inches(1.18), GOLD_LT)
add_text(s, Inches(0.65), Inches(5.98), Inches(12.05), Inches(1.02), "Write the class before you draw cefazolin. Clean elective: skip. When prophylaxis is indicated: cefazolin 22 mg/kg IV 30–60 min before incision (Gonzalez 2017; Frey 2022). Second dose if surgery lasts >90 min (Whittem 1999). Stop at closure unless you are treating infection.", size=16, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Board the four National Research Council wound classes that were on the original lecture: clean, clean-contaminated, contaminated, dirty. Elective OHE is clean: skip prophylaxis, Frey 2022. Clean-contaminated: controlled entry into gut, airway, or bladder. Contaminated: fresh trauma or major spillage. Dirty: pus. Willie’s ear is dirty: treatment, not clean prophylaxis. Then say 22 milligrams per kilogram IV. Do not attribute that dose to AAHA 2022.")

# 20 Sequence
s = new_content("Sequence of patient preparation", "CPE MOA 2026 Surgery: hair, skin, position, drape. Then announce incision.")
steps = [
    ("1", "Ready for prep: ETT in, cuff to 20 cm H2O, bag on, IV running, surgical plane"),
    ("2", "Express bladder if abdominal / caudal surgery"),
    ("3", "Clip with #40, vacuum hair, dirty antiseptic"),
    ("4", "Move to OR, position, pad, tie, final check"),
    ("5", "Sterile prep. Clock minimum contact time. Skin: 7.5% ~5 min, then 5% paint. Eye: 2 min + 2 min"),
    ("6", "Four-quadrant towels → large drape"),
    ("7", "Surgeon: cap, mask, gown, closed glove"),
    ("8", "Timeout. Announce incision. Clock runs to the last skin suture."),
]
for i, (n, t) in enumerate(steps):
    col = i % 4
    row = i // 4
    x = Inches(0.45) + Inches(col * 3.2)
    y = Inches(1.25) + Inches(row * 2.7)
    add_round(s, x, y, Inches(3.05), Inches(2.4), WHITE)
    add_rect(s, x, y, Inches(3.05), Inches(0.7), NAVY if row == 0 else TEAL)
    add_text(s, x, y, Inches(3.05), Inches(0.7), n, size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), y + Inches(0.85), Inches(2.75), Inches(1.35), t, size=18, color=INK, align=PP_ALIGN.CENTER)
notes(s, "Do not clip until the patient is ready for prep: tube in, cuff holds to 20 centimeters of water, correct bag, IV running, surgical plane. CPE MOA 2026 Surgery scores hair, skin, position, and drape, then wants you to announce the incision. Veterinary Betadine labels: 7.5% scrub about 5 minutes, rinse, paint 5% Solution Veterinary, dry. Eye: Roberts 1986, 1:50 of 10% stock, 2 plus 2 minutes.")

# 21 Hair
s = new_content("Hair removal", "#40 clipper after induction. Field 20 cm beyond the planned incision.")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.50), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.50), "Too narrow. Hair at the margin.", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "clip_cat.jpg", Inches(0.4), Inches(1.62), Inches(6.2), Inches(3.40))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.50), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.50), "24 hours after OHE. Clip was wide enough.", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "spay_incision.jpg", Inches(6.75), Inches(1.62), Inches(6.2), Inches(3.40))
add_round(s, Inches(0.4), Inches(5.15), Inches(12.55), Inches(1.85), WHITE)
add_text(s, Inches(0.6), Inches(5.28), Inches(12.2), Inches(1.55), "#40 after a surgical plane. Xiphoid to pubis, past the nipples, 20 cm beyond the incision.\nPhotos: Uwe Gille, CC0; Liannadavis, CC BY-SA 4.0.", size=16, color=INK)
notes(s, "Left photo is still too narrow. Right is a real 24-hour OHE. Do not teach a TECA clip on a patient whose procedure that day was an ear clean.")

# 22 Antiseptics
s = new_content("Skin antiseptics", "Minimum contact time. Clock it. Then drape.")
add_round(s, Inches(0.40), Inches(1.12), Inches(12.52), Inches(1.20), GOLD_LT)
add_text(s, Inches(0.55), Inches(1.18), Inches(12.2), Inches(1.08), "Human Betadine Solution = 10% PVP-I.   Veterinary paint = 5%, not 10%.\nEye: 10% stock 1:50, or 5% bottle 1:25. Both = 0.2% on the cornea (Roberts 1986).", size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_round(s, Inches(0.40), Inches(2.48), Inches(4.10), Inches(2.70), WHITE)
add_rect(s, Inches(0.40), Inches(2.48), Inches(4.10), Inches(0.48), TEAL)
add_text(s, Inches(0.40), Inches(2.48), Inches(4.10), Inches(0.48), "CHG  ·  Nolvasan", size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(3.04), Inches(3.80), Inches(2.00), "2% chlorhexidine acetate\nMIN contact: 2 to 4 min\nKeep out of eyes\nTrunk / intact skin\nAlcohol: rinse, then dry", size=16, color=INK)
add_round(s, Inches(4.62), Inches(2.48), Inches(4.10), Inches(2.70), WHITE)
add_rect(s, Inches(4.62), Inches(2.48), Inches(4.10), Inches(0.48), GOLD)
add_text(s, Inches(4.62), Inches(2.48), Inches(4.10), Inches(0.48), "Skin  ·  Betadine vet", size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(4.77), Inches(3.04), Inches(3.80), Inches(2.00), "7.5% scrub\nMIN contact: about 5 min\nRinse with sterile water\nPaint 5% solution\nDry, then drape", size=16, color=INK)
add_round(s, Inches(8.84), Inches(2.48), Inches(4.08), Inches(2.70), WHITE)
add_rect(s, Inches(8.84), Inches(2.48), Inches(4.08), Inches(0.48), NAVY)
add_text(s, Inches(8.84), Inches(2.48), Inches(4.08), Inches(0.48), "Eye  ·  Roberts 1986", size=18, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.99), Inches(3.04), Inches(3.78), Inches(2.00), "Goal: 0.2% on cornea\n10% stock → dilute 1:50\n5% bottle → dilute 1:25\nMIN: 2 min + 2 min\nNot full strength", size=16, color=INK)
add_round(s, Inches(0.40), Inches(5.38), Inches(12.52), Inches(1.60), WHITE)
add_text(s, Inches(0.60), Inches(5.50), Inches(12.12), Inches(1.36), "Nolvasan Surgical Scrub: 2% chlorhexidine acetate, DailyMed NDC 54771-8701, wash 2 to 4 min, keep out of eyes.\nBETADINE Surgical Scrub Veterinary NDC 67618-154 (7.5%, lather about 5 min). BETADINE Solution Veterinary NDC 67618-155 (5% paint, not 10%).\nEye: both 1:50 of 10% and 1:25 of 5% give 0.2% on the cornea (Roberts 1986). 1:2 of 10% caused corneal edema in 1/15 eyes.", size=14, color=SLATE)
notes(s, "Write the bottle math on the board. Veterinary Betadine Solution is 5 percent, not 10 percent. Roberts 1986: 1 to 50 of 10 percent stock, 2-minute scrub plus 2-minute soak. One case of corneal edema at 1 to 2. Nolvasan: 2 percent CHG acetate, wash 2 to 4 minutes, keep out of eyes. Willie: swollen tympanum. Canal and periocular mucosa: detergent-free dilute PVP-I, not 7.5 percent scrub.")

# 23 Technique
s = new_content("Patient skin preparation technique", "Center to periphery. Dirty prep, then sterile prep.")
add_pic(s, "prep_spiral_antiseptic.png", Inches(0.4), Inches(1.15), Inches(7.4), Inches(5.9))
add_round(s, Inches(7.95), Inches(1.15), Inches(4.9), Inches(5.9), WHITE)
add_text(s, Inches(8.15), Inches(1.3), Inches(4.55), Inches(0.4), "Technique", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(8.1), Inches(1.75), Inches(4.55), Inches(5.0), [
    "Dirty prep, then sterile prep.",
    "Start at the incision. Spiral out. Drop the sponge.",
    "Clock the minimum contact time.",
    "Skin: 7.5% ~5 min, then 5% paint.",
    "Eye: 10% 1:50 or 5% 1:25. Both = 0.2% on the cornea.",
    "Willie canal: dilute PVP-I, not 7.5% scrub.",
], size=16, spacing=10)
notes(s, "Mime the spiral. Clock about 5 minutes for veterinary Betadine scrub on intact skin. Recite Roberts 1 to 50 of 10 percent stock for the eye: 2 minutes plus 2 minutes. If the bottle is 5 percent veterinary solution, 1 to 25 matches 0.2 percent.")

# 24 Position
s = new_content("Patient positioning", "Dorsal recumbency, airway, IV catheter, monitoring, V-trough")
add_pic(s, "dog_or.jpg", Inches(0.35), Inches(1.12), Inches(8.35), Inches(5.95))
add_round(s, Inches(8.85), Inches(1.12), Inches(4.1), Inches(5.95), WHITE)
add_text(s, Inches(9.05), Inches(1.28), Inches(3.75), Inches(0.45), "Visible in this photograph", size=18, bold=True, color=NAVY)
add_text(s, Inches(9.05), Inches(1.8), Inches(3.75), Inches(5.0), "• ET tube + pulse ox\n• IV catheter + fluids\n• Circle + reservoir bag\n• V-trough / padding\n• Ties snug; pulse distal to each tie\n• Clip after a surgical plane\n\nTube tip: midway larynx to thoracic inlet (Grubb 2020).\nConfirm: ETCO2, bag move, no esophageal tube.\n\nPhoto: Anja, CC BY-SA 4.0.", size=16, color=INK)
notes(s, "Name the bag size and the tube size on this photograph. Confirm placement with ETCO2. Keep hips in a neutral spread.")

# 25 Draping
s = new_content("Draping", "Four-quadrant towels, then the large drape")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.50), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.50), "OHE: hair visible at the drape edge", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "cherry_point_spay.jpg", Inches(0.4), Inches(1.62), Inches(6.2), Inches(3.40))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.50), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.50), "Sterile field: gown, glove, drape", size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "hektor_drape.jpg", Inches(6.75), Inches(1.62), Inches(6.2), Inches(3.40))
add_round(s, Inches(0.4), Inches(5.15), Inches(12.55), Inches(1.85), WHITE)
add_text(s, Inches(0.6), Inches(5.28), Inches(12.2), Inches(1.55), "Near towel first. Four towels box the field. Towel clamps on skin, not through the drape to viscera. Large drape last. Only the incision is in the window. Re-clip until the window is hair-free.\nPhotos: Cpl. Samuel A. Nasso, USMC, public domain; MSgt Carlotta Holley, USAF, public domain.", size=16, color=INK)
notes(s, "Left is a real spay with hair at the window. Re-clip or re-drape. Four-quadrant towels, then the large drape. Then timeout before you cut.")

# 26 Gloving
s = new_content("Closed gloving and the anesthesia workstation", "Technique diagram and operating-room photograph")
add_pic(s, "prep_closed_gloving.png", Inches(0.35), Inches(1.12), Inches(6.3), Inches(4.15))
add_pic(s, "hektor_or.jpg", Inches(6.75), Inches(1.12), Inches(6.2), Inches(4.15))
add_round(s, Inches(0.35), Inches(5.38), Inches(12.6), Inches(1.7), WHITE)
add_text(s, Inches(0.55), Inches(5.5), Inches(12.2), Inches(1.45), "Left: closed-gloving technique (hands stay inside the gown cuffs). Right: cap, mask, ECG, SpO2, ETCO2, circle system, IV fluids, airway. Name every monitor on the workstation before the first incision.\nPhoto: MSgt Carlotta Holley, U.S. Air Force, public domain.", size=16, color=INK)
notes(s, "Call out closed gloving. Students name SpO2, ETCO2, ECG, temp, and fluids off the workstation photo. Do not mix MAC and case names onto this slide.")

# 27 Asepsis + protect
s = new_content("Breaks in asepsis", "Say it. Correct it. After the incision, every break must be fully corrected.")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(3.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.35), "If you contaminate", size=18, bold=True, color=TEAL)
add_text(s, Inches(0.7), Inches(1.70), Inches(5.7), Inches(2.8), "Prep, gown, glove, drape: say it immediately. Re-glove, re-gown, or re-drape. Do not continue with a contaminated field.\n\nAfter the incision: notice, announce, and fully correct. Sleeve in the abdomen, instrument off the table, hole in a glove: stop and fix it.", size=16, color=INK)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(3.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.35), "Protect the patient", size=18, bold=True, color=NAVY)
add_text(s, Inches(7.05), Inches(1.70), Inches(5.6), Inches(2.8), "1. Control significant hemorrhage.\n2. Create a secure abdominal wall closure.\n3. Achieve and maintain an aseptic field.\n4. Identify and protect adjacent organs before you clamp.\n5. Complete a sponge and instrument count before closure.", size=16, color=INK)
add_round(s, Inches(0.45), Inches(4.85), Inches(12.4), Inches(2.10), GOLD_LT)
add_text(s, Inches(0.7), Inches(5.05), Inches(11.95), Inches(1.75), "The operation is not over at the last skin suture. The first 24 hours still count: intra-abdominal hemorrhage from a weak ligature, or herniation from a weak linea, is still the operation (CPE MOA 2026 Surgery).", size=16, color=NAVY)
notes(s, "Praise the person who says I just contaminated my sleeve. Then re-glove. Teach the clinical rule, not exam scoring. The 24-hour window is why recovery is in this lecture.")

# 28 Knowledge check
s = new_content("Knowledge check", "What do you do next?")
rows = [
    ("A", "When do you clip the OHE field?", "After ready for prep: tube in, IV running, surgical plane. Then sterile prep and drape."),
    ("B", "How do you prep conjunctiva with iodine?", "10% stock 1:50. MIN contact 2 min + 2 min. 5% bottle: 1:25."),
    ("C", "Albumin 1.6 g/dL, elective mass. First move?", "Delay. Find the cause. Feed. Do not crystalloid-flood. Do not cut today."),
    ("D", "13.7 kg dog. Tube, bag, and IV fluid rate if you intubate?", "7.0 mm, 1 L circle, LRS 69 mL/hr (5 mL/kg/hr). Murmur: opioid + alfaxalone."),
]
for i, (let, q, a) in enumerate(rows):
    y = Inches(1.15) + Inches(i * 1.42)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.30), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.85), Inches(1.30), NAVY)
    add_text(s, Inches(0.5), y, Inches(0.85), Inches(1.30), let, size=22, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.55), y + Inches(0.12), Inches(10.9), Inches(0.50), q, size=18, bold=True, color=INK)
    add_text(s, Inches(1.55), y + Inches(0.68), Inches(10.9), Inches(0.48), a, size=16, color=TEAL)
notes(s, "Two minutes. C is albumin: delay elective, treat the cause. D is board math for a 13.7 kg dog if you intubate: 7.0 millimeter, 1 liter circle, 69 milliliters per hour, alfaxalone if there is a murmur. B is Roberts 1986. A is airway before clippers, then sterile prep and drape.")

# 29 Recovery
s = new_content("Immediate recovery", "Remain with the patient until airway and circulation are stable")
add_pic(s, "remus_recovery.jpg", Inches(0.35), Inches(1.12), Inches(8.15), Inches(5.95))
add_round(s, Inches(8.6), Inches(1.12), Inches(4.35), Inches(5.95), WHITE)
add_text(s, Inches(8.8), Inches(1.28), Inches(4.0), Inches(0.4), "Recovery priorities", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(8.75), Inches(1.85), Inches(4.05), Inches(4.90), [
    "Extubate when swallow returns.",
    "Most anesthetic deaths are in recovery, often in the first 3 hours (Grubb 2020).",
    "Pale + tachycardic after celiotomy: return to OR.",
    "NSAID: carprofen in the dog, Onsior in the cat. Do not stack with a steroid.",
    "E-collar on before they can lick.",
], size=16, spacing=10)
notes(s, "Real recovery: e-collar, IV, clipped abdomen. Pale OHE: stay at the cage, return to OR if unstable.")

# 30 Flowsheet
s = new_content("Anesthesia chart and end of case", "Target column is the acceptable band. Time cells stay empty until a real patient. Then complications, fluids, analgesics, sign.")
add_pic(s, "anesthesia_chart_recovery.png", Inches(0.22), Inches(1.05), Inches(12.90), Inches(6.05))
notes(s, "This is Appendix 3 pages 4 and 5, taught as an original chart, not the copyrighted grid. The filled column is the acceptable anesthesia band: Grubb 2020 for monitors, Pardo 2024 for fluids. Heart rate: stay below 150 to 190 in the dog by size, below 180 in the cat. Blood pressure: SAP at least 90, MAP at least 70, DAP at least 40. ETCO2 40 to 50, start PPV if over 60. SpO2 at least 95 percent. Temperature at least 98 Fahrenheit. Circle oxygen 2 to 3 liters then 20 to 40 milliliters per kilogram per minute, minimum 500. Fluids: dog 5 milliliters per kilogram per hour, cat 3 to 5. Inhalant to effect; do not invent a MAC number. Time cells stay empty until you plot a real patient. End of case: complications or none, fluid type rate and total, recovery analgesics, signature. Do not put a hospital case into this chart.")

# 31 Pain + incision
s = new_content("Postop analgesia and incision care", "On-label NSAIDs. Dog: carprofen. Cat: Onsior. Then teach the e-collar.")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.40), "On-label NSAID", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(0.65), Inches(1.78), Inches(5.75), Inches(4.7), [
    "Score pain. Dogs: Glasgow CMPS-SF. Cats: Feline Grimace Scale. Opioid as planned.",
    "Dog: carprofen (Rimadyl) 4.4 mg/kg SQ. Dogs only. Give ~2 hours before incision so levels are on board (pre-emptive; Rimadyl label).",
    "Cat: Onsior (robenacoxib) 2 mg/kg SQ. Cats only. First dose ~30 min before incision so levels are on board. OHE, castration, orthopedic. Up to 3 days.",
    "Dog: carprofen. Cat: Onsior. Do not swap species in this course.",
    "Do not stack an NSAID with a steroid. Willie: DexSP, skip NSAID. MoMo: azotemic, skip NSAID.",
], size=16, spacing=6)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(5.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.40), "Antibiotic injection and incision", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(7.00), Inches(1.78), Inches(5.65), Inches(4.7), [
    "A postoperative antibiotic injection is treatment. Write the drug, dose, and why.",
    "Clean elective OHE: skip (Frey 2022). Do not send home 14 days of cephalexin.",
    "Dirty or infected: continue as therapy. Willie’s ear is treatment, not prophylaxis.",
    "Look twice daily: swelling, discharge, gapping, smell, heat.",
    "E-collar that stays on. Leash walks 14 days.",
    "Skin sutures typically 10–14 days.",
], size=16, spacing=6)
notes(s, "This course uses on-label NSAIDs as pre-emptive analgesia: give before incision so levels are on board. Dog: carprofen 4.4 milligrams per kilogram SQ, about 2 hours before incision. Do not use carprofen in cats. Cat: Onsior 2 milligrams per kilogram SQ, about 30 minutes before incision. Do not teach Onsior in the dog. Do not combine NSAID with DexSP. A postop antibiotic shot is not automatic. Clean spay: skip. Infected ear: treat.")

# 32 Complications
s = new_content("Complications in the first 24 hours", "The operation is not over at the last skin suture. Hemorrhage, hernia, dehiscence.")
rows = [
    ("Hemorrhage", "Pale mm, tachycardia, distending abdomen, drip from incision, collapsing. Stabilize and return to OR.", RED),
    ("Airway / aspiration", "Stertor, crackles, regurg on the pillow. Especially brachycephalics and after opioids.", TEAL),
    ("Hernia / evisceration", "Linea failure. Emergency. Protect viscera with sterile moist towels, opioids, OR now.", NAVY),
    ("Dehiscence (later)", "Often day 3–5. Skin versus fascia: fascial dehiscence is the emergency.", GOLD),
    ("SSI", "Redness, pain, discharge, fever, usually after day 3. Culture. Open, lavage, and treat the organism you grow.", GREEN),
    ("Seroma / self-trauma", "Dead space + motion. Restrict activity. Bandage if needed. Leave the fluid unless it is infected.", TEAL),
]
for i, (t, d, c) in enumerate(rows):
    col = i % 2
    row = i // 2
    x = Inches(0.45) + Inches(col * 6.45)
    y = Inches(1.18) + Inches(row * 1.85)
    add_round(s, x, y, Inches(6.25), Inches(1.7), WHITE)
    add_rect(s, x, y, Inches(0.12), Inches(1.7), c)
    add_text(s, x + Inches(0.35), y + Inches(0.12), Inches(5.7), Inches(0.4), t, size=18, bold=True, color=c)
    add_text(s, x + Inches(0.35), y + Inches(0.55), Inches(5.7), Inches(1.0), d, size=16, color=SLATE)
notes(s, "Hemorrhage versus seroma. Skin versus fascial dehiscence. Evisceration protocol in one breath.")

# 33 Report + discharge
s = new_content("Surgical report and discharge", "What the overnight clinician and the owner both need")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.4), "Minimum report elements", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(0.65), Inches(1.78), Inches(5.75), Inches(4.7), [
    "Date/time, patient ID, surgeon, anesthesia, ASA.",
    "Procedure name and side. Position, clip/prep, approach.",
    "Findings in order. Ligatures, implants, samples.",
    "Suture: layer, material, size, pattern.",
    "Hemostasis, blood loss, sponge count, complications.",
    "Postop plan: fluids, pain, feeding, recheck.",
], size=16, spacing=6)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(5.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.4), "Discharge, verbal and written", size=18, bold=True, color=NAVY)
add_bullets(s, Inches(7.00), Inches(1.78), Inches(5.65), Inches(4.7), [
    "What we did, in one sentence.",
    "When to start food and water, and how much.",
    "Every medication: name, dose, time, with food?",
    "Incision care and 14-day leash walks.",
    "E-collar on except when directly watching.",
    "Next appointment. ER criteria. After-hours number.",
], size=16, spacing=6)
notes(s, "At 2 a.m. someone opens this record because the abdomen is swelling. They need ligatures, sponge count, linea suture, and whether the client was called.")

# 34 ER criteria
s = new_content("Emergency criteria for discharge", "The client must be able to repeat these")
crit = [
    ("Come now", "Collapse. Pale gums. Distended abdomen. Unstoppable bleeding. Can’t breathe. Can’t urinate. Evisceration. Uncontrolled pain."),
    ("Call today", "Not eating by morning. A few vomits. Mild incision redness. Diarrhea. E-collar problems."),
    ("Expected", "Sleepy tonight. Small bruise. Slightly tacky incision. Reduced appetite this evening."),
]
cols_c = [RED, GOLD, GREEN]
for i, ((t, d), c) in enumerate(zip(crit, cols_c)):
    x = Inches(0.45) + Inches(i * 4.25)
    add_round(s, x, Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
    add_rect(s, x, Inches(1.2), Inches(4.05), Inches(0.7), c)
    add_text(s, x, Inches(1.2), Inches(4.05), Inches(0.7), t, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.25), Inches(2.1), Inches(3.55), Inches(4.3), d, size=18, color=INK)
notes(s, "Pale gums + distended abdomen after OHE: come now. Return to OR.")

# 35 Willie plan
s = new_content("Willie: complete perioperative plan", "ASA example: ear disease + DexSP. Re-assign ASA on the day of any later TECA-LBO.")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(0.80), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.22), Inches(11.8), Inches(0.70), "Willie  ·  Cavalier  ·  13.7 kg  ·  ASA Status 3-E  ·  vestibular + AS otitis  ·  skip NSAID", size=18, color=NAVY)
wsteps = [
    ("Pre-op", "Neuro exam. ASA 3-E. Exam before any drug. Skip NSAID after DexSP. Premed path: opioid + alfaxalone."),
    ("Sedation", "Alfaxalone for an ear clean. Tube, bag, and 69 mL/hr only if you intubate a 13.7 kg dog. Canal: dilute PVP-I, not 7.5% scrub."),
    ("Intra", "Timeout. Deep clean + cytology. If you contaminate, say it and re-glove."),
    ("Post", "No stairs. Watch neuro signs. MRI if signs persist. If TECA-LBO later: new ASA that morning."),
]
for i, (t, d) in enumerate(wsteps):
    x = Inches(0.45) + Inches(i * 3.2)
    add_round(s, x, Inches(2.10), Inches(3.05), Inches(4.80), WHITE)
    add_rect(s, x, Inches(2.10), Inches(3.05), Inches(0.65), NAVY)
    add_text(s, x, Inches(2.10), Inches(3.05), Inches(0.65), t, size=18, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), Inches(2.90), Inches(2.75), Inches(3.80), d, size=16, color=INK)
notes(s, "Walk this as an ASA example, not as the lecture thesis. One sentence on the other example: the same preoperative evaluation cancelled an exploratory when the disease was uncompensated.")

# 36 Willie and MoMo
s = new_content("Willie and MoMo", "ASA examples. Both received a preoperative evaluation. Only Willie was sedated.")
card(s, Inches(0.45), Inches(1.2), Inches(6.15), Inches(5.5), "Willie, ASA Status 3-E", "Proceed with sedation. Cavalier, 13.7 kg. Acute vestibular + AS otitis + murmur. Compensated. Fill the anesthesia record. Alfaxalone, ear clean, skip NSAID after DexSP. If TECA-LBO is needed later, assign a new ASA that morning.", accent=GOLD)
card(s, Inches(6.75), Inches(1.2), Inches(6.15), Inches(5.5), "MoMo, ASA Status 4-E", "Cancel the exploratory. DSH, 4.25 kg. Vomiting that looked like FB. Right kidney fluid-filled and non-functional on AUS. Progressive azotemia on fluids (creatinine 3.0 → 4.71). NSAIDs contraindicated. Record the decision. Offer supportive care, referral, or euthanasia.", accent=RED)
notes(s, "Last content slide if time is gone. These two patients are ASA examples only. Healthy Lab OHE is the ASA Status 1 contrast.")

# 37 Key points
s = new_content("Key points", "CPE MOA 2026 Appendix 3 and Surgery competencies")
pearls = [
    "Pre-anesthetic assessment: TPR, mm/CRT, then PCV, TP, BUN. Interpret. Circle ASA. Then IM or SQ premed.",
    "Write drug, concentration, dose, volume, and route. Then IV fluid name and rate, ETT size, circuit, and fresh-gas flow.",
    "Ready for surgical prep: airway secured, machine on, patent IV running, surgical plane, monitoring started.",
    "Patient: hair, skin, position, drape. Surgeon: attire, gown, closed glove. Announce incision.",
    "Fill the chart: HR, RR, BP, inhalant, O2, ETCO2, SpO2, temp, fluids. Then complications, recovery analgesics, and sign.",
    "First 24 hours still count: hemorrhage from a weak ligature, or hernia from a weak linea.",
]
for i, t in enumerate(pearls):
    y = Inches(1.15) + Inches(i * 0.92)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(0.84), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.85), Inches(0.84), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.85), Inches(0.84), str(i + 1), size=20, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.55), y, Inches(10.9), Inches(0.84), t, size=18, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "These six lines are the Appendix 3 record and the Surgery competencies: assessment and ASA, drug protocol and equipment, ready for prep, hair-skin-position-drape, the chart and signature, then the first 24 hours. Do not recap the hospital patients here.")

# 38 Questions + references
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, 0, 0, Inches(0.22), H, GOLD)
add_text(s, Inches(0.55), Inches(0.26), Inches(12.2), Inches(0.28), "DVM 612  ·  PRINCIPLES OF SURGERY", size=14, bold=True, color=GOLD)
add_text(s, Inches(0.55), Inches(0.52), Inches(12.2), Inches(0.48), "Questions", size=28, bold=True, color=WHITE)
add_text(s, Inches(0.55), Inches(1.02), Inches(12.2), Inches(0.70), "When is the patient ready for clippers?\nWhat do you write before the first IM or SQ premed?", size=16, color=GOLD_LT)
add_text(s, Inches(0.55), Inches(1.78), Inches(12.2), Inches(0.32), "References  (course texts, guidelines, labels, and papers used in this hour)", size=14, bold=True, color=GOLD)
left_refs = (
    "1. Fossum TW. Small Animal Surgery. 5th ed. Elsevier; 2018. ISBN 978-0-323-44344-9. Ch. 4, 5, 6, 9.\n\n"
    "2. Hendrickson DA, Baird AN. Turner and McIlwraith’s Techniques in Large Animal Surgery. 4th ed. Wiley-Blackwell; 2013. ISBN 978-1-118-27323-4.\n\n"
    "3. Johnston SA, Tobias KM. Veterinary Surgery: Small Animal. 2nd ed. Elsevier Saunders; 2017. ISBN 978-0-323-32065-8.\n\n"
    "4. Grubb T, Sager J, Gaynor JS, Montgomery E, Parker JA, Shafford H, Tearney C. 2020 AAHA Anesthesia and Monitoring Guidelines for Dogs and Cats. J Am Anim Hosp Assoc. 2020;56(2):59–82.\n\n"
    "5. Frey E, Costin M, Granick J, Kornya M, Weese JS. 2022 AAFP/AAHA Antimicrobial Stewardship Guidelines. J Am Anim Hosp Assoc. 2022;58(4):1–5.\n\n"
    "6. Roberts SM, Severin GA, Lavach JD. Am J Vet Res. 1986;47(6):1207–1210."
)
right_refs = (
    "7. Whittem TL, Johnson AL, Smith CW, et al. J Am Vet Med Assoc. 1999;215(2):212–216.\n\n"
    "8. Gonzalez OJ, Renberg WC, Roush JK, KuKanich B, Warner M. Am J Vet Res. 2017;78(6):695–701.\n\n"
    "9. BETADINE Surgical Scrub Veterinary. 7.5% povidone-iodine. DailyMed NDC 67618-154. Lather about 5 min, rinse, paint Solution Veterinary, dry.\n\n"
    "10. BETADINE Solution Veterinary. 5% povidone-iodine (not 10%). DailyMed NDC 67618-155.\n\n"
    "11. Nolvasan Surgical Scrub. 2% chlorhexidine acetate. DailyMed NDC 54771-8701.\n\n"
    "12. ECFVG. CPE Manual of Administration. 2026 ed. Anesthesia; Surgery.\n\n"
    "13. Pardo et al. 2024 AAHA Fluid Therapy. JAAHA. 2024;60:131–163."
)
add_text(s, Inches(0.55), Inches(2.12), Inches(6.05), Inches(4.55), left_refs, size=PT_REF, color=WHITE)
add_text(s, Inches(6.75), Inches(2.12), Inches(6.05), Inches(4.55), right_refs, size=PT_REF, color=WHITE)
add_text(s, Inches(0.55), Inches(6.72), Inches(12.2), Inches(0.32), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP  ·  Lewyt CVM  ·  Long Island University", size=14, color=GOLD)
notes(s, "Take questions. If none: ready for clippers means airway secured, machine on, patent IV running, surgical plane, monitoring started. Before the first premed: today’s PE, PCV, TP, BUN, and ASA. Dismiss on time.")

# Stamp numbers
stamp_footers()

assert_min_font(prs)

if len(prs.slides) != 38:
    raise SystemExit(f"Expected 38 slides, built {len(prs.slides)}")

out = Path("/workspace/lectures/DVM-612_Week4_Preop_PatientPrep_Postop.pptx")
prs.save(str(out))
root_copy = Path("/workspace/DVM-612_Week4_Preop_PatientPrep_Postop.pptx")
root_copy.write_bytes(out.read_bytes())

script_lines = [
    "DVM 612 Week 4 instructor script",
    "Instructor: Dr. Yujin Kim, D.V.M., Ph.D., FFCP",
    "",
    "38 slides. Two hospital patients are ASA examples only: Willie (Cavalier, ASA Status 3-E, sedated for ear clean) and MoMo (DSH, ASA Status 4-E, exploratory cancelled). Owner names, addresses, phones, and emails stay off slides and off this script.",
    "",
]
for i, slide in enumerate(prs.slides, 1):
    title = ""
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text.strip().split("\n")[0].strip()
        if 8 <= len(t) <= 90 and not t.startswith("DVM 612  |"):
            title = t
            break
    try:
        speak = slide.notes_slide.notes_text_frame.text.strip()
    except Exception:
        speak = ""
    script_lines.append(f"SLIDE {i}. {title or '(visual)'}")
    if speak:
        script_lines.append(f"    SPEAK: {speak}")
    script_lines.append("")
script_path = Path("/workspace/lectures/DVM-612_Week4_Instructor_Script.txt")
script_path.write_text("\n".join(script_lines) + """

APPENDIX  ·  FULL REFERENCES
1. Fossum TW. Small Animal Surgery. 5th ed. Elsevier; 2018. ISBN 978-0-323-44344-9. Ch. 4, 5, 6, 9. Doses and dilutions on the slides are not quoted from Fossum pages.
2. Hendrickson DA, Baird AN. Turner and McIlwraith's Techniques in Large Animal Surgery. 4th ed. Wiley-Blackwell; 2013. ISBN 978-1-118-27323-4.
3. Johnston SA, Tobias KM. Veterinary Surgery: Small Animal. 2nd ed. Elsevier Saunders; 2017 (copyright 2018). ISBN 978-0-323-32065-8.
4. Grubb T, Sager J, Gaynor JS, Montgomery E, Parker JA, Shafford H, Tearney C. 2020 AAHA Anesthesia and Monitoring Guidelines for Dogs and Cats. J Am Anim Hosp Assoc. 2020;56(2):59-82. doi:10.5326/JAAHA-MS-7055. ASA companion table; healthy adult food 4-6 h; water until premedication; neonates/<2 kg food fast no longer than 1-2 h; correct K+ >6.0 mEq/L before anesthesia. NRC O2 ~200-400 mL/kg/min, inspired CO2 <5 mm Hg. Circle: 2-3 L/min when rapid depth change is needed, then typically 20-40 mL/kg/min with a minimum 500 mL/min.
5. Frey E, Costin M, Granick J, Kornya M, Weese JS. 2022 AAFP/AAHA Antimicrobial Stewardship Guidelines. J Am Anim Hosp Assoc. 2022;58(4):1-5. Start 30-60 min before incision; skip clean OHE/orchiectomy; postop rarely required. Does not publish cefazolin mg/kg.
6. Roberts SM, Severin GA, Lavach JD. Am J Vet Res. 1986;47(6):1207-1210. 10% PVP-I stock (1% available iodine); 1:50 recommended; 2-min scrub + 2-min soak; 1:2 corneal edema in 1/15 eyes.
7. BETADINE Surgical Scrub Veterinary, 7.5% PVP-I. DailyMed NDC 67618-154. Lather about 5 min, rinse, paint Solution Veterinary, dry.
8. BETADINE Solution Veterinary, 5% PVP-I (not 10%). DailyMed NDC 67618-155. If this bottle is used for a Roberts 0.2% field, dilute 1:25 (1 mL + 24 mL).
9. Nolvasan Surgical Scrub, 2% chlorhexidine acetate. DailyMed NDC 54771-8701; setid 4a2567ca-26b9-4078-b3e3-4695f50899b4. Wash 2 to 4 min. Avoid eyes and mucous membranes.
10. Whittem TL, Johnson AL, Smith CW, et al. J Am Vet Med Assoc. 1999;215(2):212-216. First dose within 30 min of surgery; second dose if surgery lasted >90 min. Abstract does not print mg/kg.
11. Gonzalez OJ, Renberg WC, Roush JK, KuKanich B, Warner M. Am J Vet Res. 2017;78(6):695-701. Extra-label 22 mg/kg IV studied in dogs. Interstitial fluid >4 ug/mL for about 4 h after IV. Does not say q90 min.
12. ONSIOR (robenacoxib) injection. DailyMed. Cats: 2 mg/kg SQ once daily up to 3 days for orthopedic surgery, OHE, and castration. First dose about 30 min before surgery. Do not combine with another NSAID or a corticosteroid. This lecture does not teach Onsior in the dog.
13. RIMADYL (carprofen) sterile injectable. DailyMed NDC 54771-8507. Dogs only. Do not use in cats. 4.4 mg/kg SQ daily; postoperative dose about 2 hours before the procedure.
14. ECFVG. Clinical Proficiency Examination Manual of Administration. 2026 ed. American Veterinary Medical Association. https://www.avma.org/sites/default/files/2025-11/ECFVG-2026_MOA.pdf. Anesthesia section: preoperative examination before IM/SQ premedication; request labs; assign ASA (Appendix 2); select ETT, breathing system, and reservoir bag; calculate fresh-gas flow; leak-test; cuff holds to 20 cm H2O; ready for surgical prep means airway secured, machine on, patent IV running, surgical plane, monitoring started. Surgery section: hair, skin, position, drape, gown/glove; announce incision; one unrecognized asepsis break before incision, none after; last skin suture ends the clock; first 24 hours still count (hemorrhage, hernia). Used as the competency list for this DVM 612 hour, not as CPE exam-prep.
15. Pardo M, Spencer E, Odunayo A, Ramirez ML, Rudloff E, Shafford H, Weil A, Wolff E. 2024 AAHA Fluid Therapy Guidelines for Dogs and Cats. J Am Anim Hosp Assoc. 2024;60:131-163. doi:10.5326/JAAHA-MS-7444. Anesthesia crystalloid: dogs 5 mL/kg/hr, cats 3-5 mL/kg/hr; the old 10 mL/kg/hr rate lacked evidence. Albumin <2.0 g/dL: negative prognostic indicator, edema, poor wound healing. Plasma ~20-25 mL/kg to raise albumin 0.5 g/dL. Species-specific albumin preferred if severe. Human albumin: allergic reactions.

TEACHING NAMES (no mg/kg invented on the slides): DKT = dexmedetomidine + ketamine + butorphanol. BAA = butorphanol + acepromazine + atropine. MAC = minimum alveolar concentration.
ANESTHESIA SEQUENCE FOR THIS HOUR: examine, labs, ASA, correct deficits, IM/SQ premed, IV induction to effect, intubate, inhalant to MAC (premed lowers MAC), then clip / sterile prep / drape.
TUBE, BAG, AND FLUIDS (board math): dog ETT starting estimate ID mm = (kg / 4) + 3.5, then confirm largest that passes the arytenoids without trauma (Grubb 2020). Bag: kg × 60 mL, round UP to 0.5/1/2/3 L. Anesthesia IVF (Pardo 2024): dog 5 mL/kg/hr, cat 3-5 mL/kg/hr. Circle FGF (Grubb 2020): 2-3 L/min at induction, then 20-40 mL/kg/min, minimum 500 mL/min. NRC: 200-400 mL/kg/min. A 13.7 kg dog if intubated: 7.0 mm, 1 L circle, LRS 69 mL/hr, FGF 2-3 L/min then ≥0.5 L/min. Teaching table on slide 16 uses CPE MOA 2026 Appendix 3 fields (ASA, ETT, bag, circuit, IV name/rate, FGF); do not dump the copyrighted form.

TYPE: titles 30 pt, body 18 pt, cards 16 pt, kicker 13 pt, footer 12 pt, references 13 pt.
""", encoding="utf-8")

print(f"Saved {out}")
print(f"Copied {root_copy}")
print(f"Script {script_path}")
print(f"Slides: {len(prs.slides)}")
