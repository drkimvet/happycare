#!/usr/bin/env python3
"""Build DVM 612 Week 4 lecture: Preoperative evaluation, patient preparation, postoperative care.

Lewyt College of Veterinary Medicine (LIU)
Aligned to DVM 612 course outline Week 4 and course learning objectives 4, 7, 8.
Required texts: Fossum 2018; Hendrickson & Baird 2013.
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import nsmap, qn
from pptx.util import Emu, Inches, Pt
from lxml import etree
from copy import deepcopy

ASSETS = Path(__file__).resolve().parent / "assets"

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
FOOTER = "DVM 612  |  Dr. Yujin Kim, D.V.M., Ph.D., FFCP  |  Preop · prep · postop  |  Lewyt CVM"

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
    add_rect(slide, 0, Inches(7.22), W, Inches(0.28), NAVY)
    add_text(slide, Inches(0.4), Inches(7.22), Inches(10.5), Inches(0.28), FOOTER, size=10, color=GOLD_LT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(11.4), Inches(7.22), Inches(1.5), Inches(0.28), f"{num}  /  {total}", size=10, color=WHITE, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def header_bar(slide, kicker=""):
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    add_rect(slide, 0, Inches(0.12), W, Inches(0.08), NAVY)
    if kicker:
        add_text(slide, Inches(0.5), Inches(0.28), Inches(12.3), Inches(0.28), kicker.upper(), size=11, bold=True, color=TEAL)


def content_chrome(slide, title, kicker, num, total):
    add_rect(slide, 0, 0, W, H, OFFWHITE)
    header_bar(slide, kicker)
    add_rect(slide, 0, Inches(0.12), Inches(0.12), Inches(7.1), GOLD)
    add_text(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.55), title, size=26, bold=True, color=NAVY)
    footer_bar(slide, num, total)


def card(slide, l, t, w, h, title, body, fill=WHITE, title_color=NAVY, accent=GOLD):
    add_round(slide, l, t, w, h, fill)
    add_rect(slide, l, t, Inches(0.10), h, accent)
    add_text(slide, l + Inches(0.28), t + Inches(0.12), w - Inches(0.4), Inches(0.38), title, size=15, bold=True, color=title_color)
    add_text(slide, l + Inches(0.28), t + Inches(0.48), w - Inches(0.4), h - Inches(0.58), body, size=13, color=SLATE)


def pill(slide, l, t, w, h, text, fill=GOLD, text_color=NAVY):
    add_round(slide, l, t, w, h, fill)
    add_text(slide, l, t, w, h, text, size=12, bold=True, color=text_color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# Slide registry: we first plan TOTAL then build
# Rebuild footers after all slides are created.
# and set numbers at the end.

SLIDES = []  # list of (slide, notes_text) after creation? We'll stamp at end.


def new_content(title, kicker=""):
    s = prs.slides.add_slide(BLANK)
    add_rect(s, 0, 0, W, H, OFFWHITE)
    header_bar(s, kicker)
    add_rect(s, 0, Inches(0.12), Inches(0.12), Inches(7.1), GOLD)
    add_text(s, Inches(0.5), Inches(0.50), Inches(12.3), Inches(0.52), title, size=26, bold=True, color=NAVY)
    return s


def new_section(part, title, subtitle, minutes):
    s = prs.slides.add_slide(BLANK)
    add_rect(s, 0, 0, W, H, NAVY)
    add_rect(s, 0, 0, W, Inches(0.14), GOLD)
    add_rect(s, 0, Inches(7.36), W, Inches(0.14), GOLD)
    add_text(s, Inches(0.7), Inches(2.15), Inches(12), Inches(0.4), part.upper(), size=16, bold=True, color=GOLD)
    add_text(s, Inches(0.7), Inches(2.55), Inches(12), Inches(1.1), title, size=40, bold=True, color=WHITE)
    add_text(s, Inches(0.7), Inches(3.75), Inches(12), Inches(0.7), subtitle, size=20, color=GOLD_LT)
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
            add_text(slide, Inches(11.5), Inches(7.05), Inches(1.4), Inches(0.28), f"{i}  /  {total}", size=11, color=GOLD, align=PP_ALIGN.RIGHT)
        else:
            footer_bar(slide, i, total)


# =============================================================================
# SLIDES  (38 pages)
# =============================================================================

# 1 Title
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, Inches(0), Inches(0), Inches(0.22), H, GOLD)
add_text(s, Inches(0.75), Inches(1.15), Inches(12), Inches(0.35), "LONG ISLAND UNIVERSITY  ·  LEWYT COLLEGE OF VETERINARY MEDICINE", size=13, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(1.7), Inches(12), Inches(0.4), "DVM 612  ·  PRINCIPLES OF SURGERY", size=16, bold=True, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(2.25), Inches(12), Inches(1.6), "Preoperative Evaluation,\nPatient Preparation &\nPostoperative Care", size=36, bold=True, color=WHITE)
add_text(s, Inches(0.75), Inches(5.05), Inches(12), Inches(0.45), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP", size=22, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(5.5), Inches(12), Inches(0.35), "Lecture  |  38 slides  |  60 minutes", size=16, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(5.9), Inches(12), Inches(0.7), "Preoperative evaluation · patient and surgeon preparation · postoperative care.\nTwo hospital cases: Willie (Cavalier, ASA III-E) and MoMo (cat, ASA IV-E; exploratory cancelled).", size=14, color=WHITE)
add_text(s, Inches(0.75), Inches(6.62), Inches(12), Inches(0.32), "Required reading: Fossum, Small Animal Surgery, 5th ed. (2018)  ·  Hendrickson & Baird (2013)", size=12, color=GOLD)
notes(s, "Welcome. This hour is preoperative evaluation, patient and surgeon preparation, and postoperative care. Two real patients from the same hospital. Willie, a 6-year 11-month MN Cavalier, 13.7 kg, acute vestibular crisis plus left otitis. We sedated him. MoMo, a 6-year SF DSH, 4.25 kg, vomiting that looked like a foreign-body surgery. Imaging cancelled the exploratory. Assign both ASA statuses. Owner identifiers stay off these slides. Thirty-eight slides. If discussion runs, protect antiseptics, both cases, and recovery.")

# 2 Learning objectives
s = new_content("Learning objectives", "DVM 612 Week 4  ·  38 slides")
items = [
    "Perform a preoperative evaluation, assign an ASA status, and decide whether to proceed, delay, or stabilize.",
    "Build a peri-operative plan: fasting, analgesia, antimicrobial prophylaxis, consent, and checklist.",
    "Prepare the patient and surgeon for aseptic surgery: clip, labeled antiseptic contact times, dilute 10% PVP-I 1:50 for the eye (Roberts 1986), four-quadrant drape, gown, closed glove.",
    "Recognize and correct a break in asepsis before and after the incision is made.",
    "Write a postoperative plan, surgical report elements, and client discharge instructions, including 24-hour emergency criteria.",
]
add_bullets(s, Inches(0.55), Inches(1.15), Inches(12.2), Inches(4.35), items, size=17, spacing=10)
add_round(s, Inches(0.5), Inches(5.55), Inches(12.3), Inches(1.45), GOLD_LT)
add_text(s, Inches(0.75), Inches(5.65), Inches(11.9), Inches(0.35), "Hour  ·  0–20 min preop and both cases  ·  20–40 min clip, antiseptic, drape  ·  40–57 min recovery and discharge  ·  57–60 min Willie vs MoMo", size=13, color=NAVY)
add_text(s, Inches(0.75), Inches(6.10), Inches(11.9), Inches(0.7), "Willie: examine, assign ASA Status 3-E, then sedate. MoMo: examine, image, run labs, then cancel the exploratory.", size=14, color=NAVY)
notes(s, "Read the five objectives aloud. Timer: protect Part II (prep pictures) and both cases.")

# 3 SSI
s = new_content("Surgical site infection", "Why this hour exists")
card(s, Inches(0.5), Inches(1.2), Inches(4.0), Inches(2.35), "Causes of SSI", "Hair, skin flora, hypothermia, poor hemostasis, dead space, and breaks in asepsis.", fill=WHITE, accent=TEAL)
card(s, Inches(4.7), Inches(1.2), Inches(4.0), Inches(2.35), "Client-owned patients", "Elective OHE patients go home to the owner after recovery. Documentation and the discharge conversation are part of the operation.", fill=WHITE, accent=GOLD)
card(s, Inches(8.9), Inches(1.2), Inches(3.9), Inches(2.35), "Decisions made before incision", "Analgesia, antibiotics, temperature management, and client expectations are set in the preoperative period.", fill=WHITE, accent=GREEN)
add_round(s, Inches(0.5), Inches(3.75), Inches(12.3), Inches(3.2), WHITE)
add_text(s, Inches(0.75), Inches(3.9), Inches(11.8), Inches(0.4), "Surgeon responsibilities", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.4), Inches(11.8), Inches(2.3), [
    "Prepare the patient for a surgical procedure.",
    "Prepare yourself for a surgical procedure.",
    "Perform the procedure. Then own the first 24 hours: hemorrhage or herniation in recovery is still the operation.",
], size=17, spacing=8)
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
    y = Inches(1.2) + Inches(row * 1.35)
    w = Inches(12.3) if i == 6 else Inches(6.2)
    if i == 6:
        x = Inches(0.5)
    add_round(s, x, y, w, Inches(1.22), WHITE)
    add_rect(s, x, y, Inches(0.10), Inches(1.22), GOLD)
    add_text(s, x + Inches(0.28), y + Inches(0.12), w - Inches(0.4), Inches(0.38), f"{i+1}.  {t}", size=15, bold=True, color=NAVY)
    add_text(s, x + Inches(0.28), y + Inches(0.52), w - Inches(0.4), Inches(0.58), d, size=13, color=SLATE)
notes(s, "Two minutes, then move. Every Halsted principle has a preop or postop action, not just an intraoperative one.")

# 5 Continuum
s = new_content("The perioperative continuum", "Preoperative, preparation, intraoperative, postoperative")
stages = [
    ("PRE-OP", "History, PE, ASA\nLabs, stabilize\nConsent, plan\nAnalgesia, Abx", TEAL),
    ("PREP", "Clip after induction\nDirty then sterile prep\nPosition, drape\nGown, closed glove", GOLD),
    ("INTRA-OP", "Asepsis held\nHalsted applied\nTime, temp, pain", NAVY),
    ("POST-OP", "Airway, pain, heat\nWatch 24 hours\nReport + discharge\nRecheck plan", GREEN),
]
for i, (t, b, c) in enumerate(stages):
    x = Inches(0.45) + Inches(i * 3.2)
    add_round(s, x, Inches(1.35), Inches(3.0), Inches(4.35), WHITE)
    add_rect(s, x, Inches(1.35), Inches(3.0), Inches(0.7), c)
    add_text(s, x, Inches(1.35), Inches(3.0), Inches(0.7), t, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.2), Inches(2.2), Inches(2.6), Inches(3.2), b, size=16, color=INK, align=PP_ALIGN.CENTER)
    if i < 3:
        add_text(s, x + Inches(2.7), Inches(3.2), Inches(0.55), Inches(0.4), "→", size=22, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
notes(s, "Anesthesia prepares the patient for surgical prep. Surgery owns prep through the last skin suture. Both own recovery.")

# 6 Preop evaluation
s = new_content("Preoperative evaluation", "Examine, request indicated labs, interpret, then assign ASA")
goals = [
    ("01", "Identify surgical disease", "Confirm the lesion, laterality, and that surgery is indicated."),
    ("02", "Quantify anesthetic risk", "Assign ASA after today’s examination and labs. Write that number on the record."),
    ("03", "Fix what you can first", "Dehydration, anemia, electrolyte crises, uncontrolled diabetes, full bladder, pyoderma over the site."),
    ("04", "Plan the day", "Approach, positioning, implants, blood products, ICU bed, who calls the client."),
]
for i, (n, t, d) in enumerate(goals):
    col = i % 2
    row = i // 2
    x = Inches(0.45) + Inches(col * 6.45)
    y = Inches(1.12) + Inches(row * 1.55)
    add_round(s, x, y, Inches(6.25), Inches(1.42), WHITE)
    add_rect(s, x, y, Inches(0.7), Inches(1.42), NAVY)
    add_text(s, x, y, Inches(0.7), Inches(1.42), n, size=16, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.9), y + Inches(0.12), Inches(5.15), Inches(0.4), t, size=15, bold=True, color=NAVY)
    add_text(s, x + Inches(0.9), y + Inches(0.55), Inches(5.15), Inches(0.75), d, size=13, color=SLATE)
add_round(s, Inches(0.45), Inches(4.32), Inches(8.15), Inches(2.65), WHITE)
add_text(s, Inches(0.7), Inches(4.42), Inches(7.7), Inches(0.32), "History and PE, then any drug", size=14, bold=True, color=TEAL)
add_bullets(s, Inches(0.65), Inches(4.78), Inches(7.75), Inches(2.05), [
    "Signalment, last meal, medications, prior anesthesia, bleeding tendency.",
    "TPR, mm, CRT, hydration, murmur, lungs, surgical site, abdomen, neuro if indicated.",
    "Record the examination. The next clinician reads what you wrote.",
], size=14, spacing=5)
add_round(s, Inches(8.80), Inches(4.32), Inches(3.95), Inches(2.65), NAVY)
add_text(s, Inches(9.0), Inches(4.45), Inches(3.6), Inches(0.4), "Order of operations", size=14, bold=True, color=GOLD)
add_text(s, Inches(9.0), Inches(4.95), Inches(3.6), Inches(1.85), "1. Examine the patient\n2. Request indicated labs\n3. Interpret the results\n4. Assign ASA status\n5. Adjust the drug plan\n6. Premedicate", size=13, color=WHITE)
notes(s, "Four jobs. Students often skip #3 and #4. Do your own PE, then use technician vitals as a second set of numbers. Order: examine, then premedicate.")

# 7 ASA
s = new_content("ASA physical status", "American Society of Anesthesiologists classification")
rows = [
    ("1", "Normal, healthy patient", "Healthy 1-year-old OHE", GREEN),
    ("2", "Mild systemic disease, well compensated", "Obesity; asymptomatic murmur; controlled diabetes", TEAL),
    ("3", "Moderate systemic disease that is ongoing but compensated; some functional limitations exist that increase the risk of anesthesia", "Willie: vestibular disease, otitis, walking, compensated murmur", GOLD),
    ("4", "Severe systemic disease that is a constant threat to life, uncompensated disease, high anesthetic risk because vital body systems involved", "MoMo: rising azotemia, non-functional kidney; GDV; septic abdomen", RED),
    ("5", "Moribund patient not expected to live more than 24 hours with or without surgery", "Gastric rupture; catastrophic trauma; end-stage disease", NAVY),
]
add_rect(s, Inches(0.45), Inches(1.12), Inches(12.4), Inches(0.40), NAVY)
add_text(s, Inches(0.55), Inches(1.12), Inches(2.4), Inches(0.40), "ASA status", size=13, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3.0), Inches(1.12), Inches(6.4), Inches(0.40), "Definition", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(9.4), Inches(1.12), Inches(3.3), Inches(0.40), "Example", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, (asa, defn, ex, c) in enumerate(rows):
    y = Inches(1.56) + Inches(i * 0.90)
    add_round(s, Inches(0.45), y, Inches(12.4), Inches(0.84), WHITE)
    add_rect(s, Inches(0.45), y, Inches(2.35), Inches(0.84), c)
    add_text(s, Inches(0.45), y, Inches(2.35), Inches(0.84), f"Status {asa}", size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.95), y + Inches(0.06), Inches(6.35), Inches(0.72), defn, size=13, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(9.4), y + Inches(0.06), Inches(3.25), Inches(0.72), ex, size=12, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
add_round(s, Inches(0.45), Inches(6.12), Inches(12.4), Inches(0.95), GOLD_LT)
add_text(s, Inches(0.65), Inches(6.22), Inches(12.05), Inches(0.75), "E = emergency (written Status 3-E or 4-E). Willie is Status 3-E: acute, still compensated. MoMo is Status 4-E: acute, uncompensated, vital systems involved. Assign the number after today’s PE and labs.", size=14, color=NAVY)
notes(s, "Read Status 1, then 3, then 4 slowly. E means emergency. Next: four 60-second cases, then Willie (3-E, we sedated) and MoMo (4-E, exploratory cancelled).")

# 8 ASA practice
s = new_content("ASA practice cases", "Assign status, then say whether you proceed today")
cases = [
    ("A", "Healthy 8-month Labrador for elective OHE. Normal PE, PCV/TS normal.", "ASA Status 1  ·  proceed", GREEN_LT, GREEN),
    ("B", "10-year MN Beagle, BCS 8/9, grade 2/6 murmur, no CHF, dental + mass removal.", "ASA Status 2  ·  proceed with monitoring plan", TEAL_LT, TEAL),
    ("C", "Willie: 6 y 11 mo MN Cavalier, 13.7 kg. Acute ataxia 1 h. AS otitis, TM visible/swollen. Circling left, nystagmus fast-left, right knuckling. Grade II murmur. CV stable.", "ASA Status 3-E. Proceed with a sedation plan.", GOLD_LT, GOLD),
    ("D", "MoMo: 6 yo SF DSH, 4.25 kg. Acute vomiting ×2, lethargy, construction at home; possible foreign body. T 98.0 °F, HR 200, mm pink tacky. Mildly enlarged abdomen.", "Stabilize, image, and run labs first. This became ASA Status 4-E. Medical abdomen.", RED_LT, RED),
]
for i, (let, stem, ans, fill, acc) in enumerate(cases):
    y = Inches(1.2) + Inches(i * 1.35)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.22), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.22), acc)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.22), let, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.45), y + Inches(0.12), Inches(11.0), Inches(0.5), stem, size=15, color=INK)
    add_text(s, Inches(1.45), y + Inches(0.68), Inches(11.0), Inches(0.4), ans, size=14, bold=True, color=acc)
notes(s, "Cold-call four students. C is Willie (sedation). D is MoMo (exploratory cancelled).")

# 9 Willie
s = new_content("Willie, ASA Status 3-E", "6 y 11 mo MN Cavalier King Charles Spaniel, 13.7 kg, BCS 6/9")
add_round(s, Inches(0.5), Inches(1.12), Inches(12.3), Inches(1.15), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.20), Inches(11.8), Inches(1.00), "Acute ataxia ~1 hour. Fell off the couch twice. Cytopoint for allergies. Vitals: T 100.8 °F, HR 132, RR 52, mm pink, CRT 2 s, quiet/dull. ASA III-E: compensated vestibular disease plus severe AS otitis. Still pink, walking, kidneys normal.", size=14, color=NAVY)
card(s, Inches(0.5), Inches(2.40), Inches(4.0), Inches(2.85), "Left ear (AS)", "Brown and bloody discharge. Pedal reflex at the pinna base. Canal patent. Cartilage hardened. Tympanic membrane visible but swollen.", accent=TEAL)
card(s, Inches(4.7), Inches(2.40), Inches(4.0), Inches(2.85), "Neuro exam", "Circling left. Horizontal nystagmus, fast left, slow right. Right knuckling. Treat as central vestibular disease until MRI.", accent=GOLD)
card(s, Inches(8.9), Inches(2.40), Inches(3.9), Inches(2.85), "Also on PE", "Grade II/VI left systolic murmur. Heavy tartar. Soft non-painful abdomen. Compensated tonight.", accent=RED)
add_round(s, Inches(0.5), Inches(5.40), Inches(12.3), Inches(1.55), WHITE)
add_text(s, Inches(0.75), Inches(5.50), Inches(11.8), Inches(1.35), "Plan: CBC WNL. Skip NSAID after DexSP 0.68 mL SQ. Alfaxalone sedation, deep left-ear clean, cytology/culture, 3-view films. Home: meclizine 25 mg PO BID × 5 d, Cerenia 60 mg PO SID × 4 d, confine. MRI recommended. TECA-LBO if culture-guided medical therapy fails.", size=14, color=INK)
notes(s, "Record the murmur. Right-sided knuckling with left circling: treat as central vestibular plus otitis, then sedate. Aminoglycosides are a risk if the middle ear is involved even when the drum looks present. Skip NSAID after DexSP.")

# 10 MoMo
s = new_content("MoMo, ASA Status 4-E", "6 yo SF DSH, 4.25 kg, BCS 5/9")
add_round(s, Inches(0.5), Inches(1.12), Inches(12.3), Inches(1.15), RED_LT)
add_text(s, Inches(0.75), Inches(1.20), Inches(11.8), Inches(1.00), "Acute vomiting and lethargy. Two vomits. Household construction. Possible FB. Vitals: T 98.0 °F, HR 200, RR 30, mm pink tacky, CRT <2 s, QAR. ASA IV-E: rising azotemia and a non-functional kidney. A cancelled exploratory is a successful preoperative evaluation.", size=14, color=NAVY)
card(s, Inches(0.5), Inches(2.40), Inches(4.0), Inches(2.85), "Why this looked surgical", "FB obstruction was on the list. Mildly enlarged abdomen. That is how cats get booked for an exploratory.", accent=GOLD)
card(s, Inches(4.7), Inches(2.40), Inches(4.0), Inches(2.85), "What the PE showed", "Heart/lungs normal. Ambulatory ×4. Dehydrated. The PE did not prove a foreign body.", accent=TEAL)
card(s, Inches(8.9), Inches(2.40), Inches(3.9), Inches(2.85), "Next: labs and imaging", "POCUS: abnormal kidneys, bladder intact. 3-view abdomen STAT. CBC/chem. Assign ASA after those results.", accent=RED)
add_round(s, Inches(0.5), Inches(5.40), Inches(12.3), Inches(1.55), WHITE)
add_text(s, Inches(0.75), Inches(5.50), Inches(11.8), Inches(1.35), "Work-up: IVF 1.5×, Cerenia, ondansetron, Unasyn. Creatinine 3.0 → 4.71 on fluids. AUS: right kidney fluid-filled and non-functional. Skip NSAIDs. Cancel the exploratory. Record the decision. Owner elected humane euthanasia.", size=14, color=INK)
notes(s, "MoMo is the cat whose films looked like maybe GI and were kidneys. Cold-call: who would have clipped her on history alone? Be respectful; this cat died. The teaching point is judgment.")

# 11 Diagnostics
s = new_content("Preoperative diagnostics", "Tests indicated for this patient and this procedure")
card(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(2.55), "Young, healthy, elective (ASA I)", "PCV/TS ± blood glucose and Azo stick is a defensible minimum. Many hospitals still run a preanesthetic chemistry/CBC. Know your hospital policy and be able to defend either choice.", accent=TEAL)
card(s, Inches(6.8), Inches(1.2), Inches(6.0), Inches(2.55), "Age, disease, or invasive procedure", "CBC, chemistry, UA. Add clotting (PT/PTT or BMBT) if bleeding risk. T4 in older cats. Blood pressure. ECG if arrhythmia. Imaging if it changes the approach.", accent=GOLD)
add_round(s, Inches(0.5), Inches(3.95), Inches(12.3), Inches(3.0), WHITE)
add_text(s, Inches(0.75), Inches(4.10), Inches(11.8), Inches(0.35), "How to use the tests you order", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.55), Inches(11.8), Inches(2.2), [
    "Anemia, hypoalbuminemia, azotemia, electrolyte storms, and thrombocytopenia change drugs, fluids, and whether you cut today.",
    "Abdominal surgery: image first so you know whether you are cutting a pyometra, a mass that needs a different approach, or a medical abdomen. MoMo: POCUS/AUS cancelled the cut.",
    "Repeat a value that changes the plan. MoMo: creatinine 3.0 then 4.71. Act on the rising creatinine.",
], size=15, spacing=7)
notes(s, "Request labs that change the plan. They inform the ASA number. Today’s PE writes it.")

# 12 CBC/chem
s = new_content("CBC and chemistry → ASA Status", "These bands inform Status. Today’s PE writes it.")
add_pic(s, "asa_cbc_chem.png", Inches(0.22), Inches(1.05), Inches(12.9), Inches(6.12))
notes(s, "Ninety seconds. Point at PCV, platelets, creatinine, potassium. Willie: CBC essentially Status 1. His Status 3-E is the vestibular exam. MoMo: WBC ~26 and creatinine 3.0 then 4.71.")

# 13 Apply labs
s = new_content("Applying the lab tables", "Labs inform ASA status. The physical examination assigns it.")
card(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), "Willie, laboratory results", "CBC WNL (Status 1 band).\nPhosphorus 6.0, mild increase (Status 2).\nGlucose 130, stress (Status 2 band).\nKidneys, liver, electrolytes normal.\nSkip the EPOC for this ear clean.\n\nASA Status 3-E: acute vestibular disease, severe AS otitis, murmur. An unremarkable chemistry leaves the neurologic Status 3 in place.", accent=GOLD)
card(s, Inches(6.75), Inches(1.15), Inches(6.15), Inches(5.55), "MoMo, laboratory results and EPOC", "WBC about 26K with neutrophilia (Status 3 to 4).\nPlatelets 74 K (Status 3).\nCreatinine 3.0 to 4.71; BUN 49.7 to 100 (Status 4).\nPhosphorus 8.0 (Status 3 to 4).\nEPOC pH 7.255 (Status 3); BE −7.4 (Status 2); lactate 2.05 (Status 1).\nVenous pO2 33 is venous.\nWhole-patient status is 4-E. Cancel the exploratory.", accent=RED)
notes(s, "Students want to average the columns. The worst compensated vital-system problem that is a constant threat sets the floor. MoMo’s kidneys set Status 4. Willie’s neuro exam set Status 3 even with a normal CBC.")

# 14 Stabilize
s = new_content("Stabilization before elective surgery", "When to delay, when to proceed urgently")
cols = [
    ("Fix first", GREEN, "Hypovolemia / shock\nElectrolyte crises (K+, Na+)\nSevere anemia (transfuse)\nRespiratory distress\nUncontrolled pain\nHypoglycemia\nHyperthermia / heat stroke"),
    ("Often delay elective", GOLD, "Pyoderma over the site\nAnestrus vs. heat if policy\nUnstable endocrine disease\nActive URI in cats\nRecent live vaccines (clinic policy)\nClient cannot confine / medicate\nFull-stomach elective: suction or reschedule"),
    ("May proceed urgently", RED, "GDV\nSeptic abdomen\nC-section with fetal distress\nAirway obstruction\nHemorrhage you cannot pack\nOpen fracture (after resuscitation)\nUterine rupture / pyometra shock"),
]
for i, (t, c, b) in enumerate(cols):
    x = Inches(0.45) + Inches(i * 4.25)
    add_round(s, x, Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
    add_rect(s, x, Inches(1.2), Inches(4.05), Inches(0.6), c)
    add_text(s, x, Inches(1.2), Inches(4.05), Inches(0.6), t, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.25), Inches(2.0), Inches(3.55), Inches(4.4), b, size=15, color=INK)
notes(s, "Resuscitate first, then clip. Delay elective OHE for pyoderma. Take GDV to surgery after resuscitation. MoMo: image and run labs, then cancel the exploratory.")

# 15 Fasting + consent
s = new_content("Fasting and informed consent", "2020 AAHA Anesthesia and Monitoring Guidelines; then the risk talk")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.4), "Fasting (Grubb et al. 2020 AAHA)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.65), Inches(1.78), Inches(5.75), Inches(4.7), [
    "Healthy adult dog/cat: food 4–6 h; water until premedication.",
    "Some hospitals still use 8–12 h NPO. Teach aspiration versus hypoglycemia.",
    "Neonates / <2 kg: food fast no longer than 1–2 h.",
    "Brachycephalics: shorter fast, pre-oxygenate.",
    "Ask what was eaten this morning. Clients feed ‘just a biscuit.’",
    "Diabetics: write the insulin dose and a small meal with anesthesia before drop-off.",
], size=14, spacing=6)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(5.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.4), "Consent, then file it", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.00), Inches(1.78), Inches(5.65), Inches(4.7), [
    "Procedure name in plain language, and the reason.",
    "Benefits, alternatives including medical management, and what happens if we wait.",
    "Material risks in one sentence each: anesthesia death, hemorrhage, infection, dehiscence. After OHE, name urinary incontinence.",
    "Estimate: what is included and what is not.",
    "Resuscitation code / DNR before induction.",
    "File the signed form. Then start induction.",
], size=14, spacing=6)
notes(s, "Cite Grubb et al., 2020 AAHA Anesthesia and Monitoring Guidelines: healthy adults, food 4 to 6 hours, water until premedication. Neonates and patients under 2 kg: food fast no longer than 1 to 2 hours. A 2-minute risk talk prevents a 2-hour complaint. Mention DNR.")

# 16 Checklist + analgesia
s = new_content("Pre-incision checklist and analgesia", "WHO-adapted timeout and multimodal plan")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Pre-incision checklist", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.7), Inches(4.5), [
    "Identity, procedure, site/side confirmed.",
    "Consent, estimate, DNR documented.",
    "ASA, allergies, last meal.",
    "IV catheter patent; fluids running.",
    "Airway secured; monitoring on.",
    "Antibiotics given (if indicated) 30 minutes before incision.",
    "Local block planned (incisional, testicular, TAP, splash).",
    "Instruments, suture, extra gloves, cautery, suction.",
], size=14, spacing=5)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), WHITE)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Multimodal analgesia", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.05), Inches(1.9), Inches(5.55), Inches(4.5), [
    "Opioid as part of premed or induction.",
    "NSAID if perfusion, kidneys, and GI tract allow. Often at recovery.",
    "Local/regional: the cheapest MAC-sparing tool you have.",
    "Adjuncts: ketamine CRI, dexmedetomidine CRI, gabapentin, acetaminophen (dog only).",
    "Cats: skip acetaminophen; careful NSAID choice and dose.",
    "Write the pain plan before the patient leaves the table.",
], size=14, spacing=6)
notes(s, "Checklist takes 90 seconds and prevents wrong-site and forgotten cefazolin. Locals are underused.")

# 17 Willie record
s = new_content("Anesthesia record, Willie", "Teaching form. Complete the header before the first drug.")
add_pic(s, "anesthesia_record_willie.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "Walk the header: ASA III-E is written before alfaxalone. DexSP means skip NSAID. Grid every 5 minutes while sedated. Recovery boxes are part of the same page.")

# 18 MoMo record
s = new_content("Anesthesia record, MoMo", "Preoperative evaluation documented; exploratory cancelled")
add_pic(s, "anesthesia_record_momo.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "The form is not only for patients who get clipped. Recording the cancellation is a surgical document. Say it once, respectfully, then continue.")

# 19 Abx
s = new_content("Surgical antimicrobial prophylaxis", "Frey et al. 2022 AAFP/AAHA: when. Whittem 1999 and Gonzalez 2017: how.")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), GREEN_LT)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.45), "Clean elective: skip prophylaxis", size=17, bold=True, color=GREEN)
add_text(s, Inches(0.75), Inches(1.9), Inches(5.6), Inches(4.4), "2022 AAFP/AAHA (Frey et al.):\n• Prophylaxis is a brief course started 30–60 min before the first incision.\n• Not usually needed for clean procedures.\n• Sterile technique should eliminate the need in OHE, orchiectomy, and most sterile procedures.\n• Ongoing postoperative antimicrobials are rarely required.\n\n1. Hold asepsis, Halsted, and a dry field.\n2. Skip peri-op antibiotics on these cases.\n3. After an uncomplicated clean surgery, stop at closure.", size=14, color=INK)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.45), "When indicated: timed IV, then stop", size=16, bold=True, color=RED)
add_text(s, Inches(7.1), Inches(1.9), Inches(5.5), Inches(4.4), "AAFP/AAHA 2022 does not publish a cefazolin mg/kg.\n\n1. Start 30–60 min before incision (Frey 2022).\n2. Extra-label teaching dose: cefazolin 22 mg/kg IV (Gonzalez et al. AJVR 2017 studied this dose).\n3. Whittem et al. JAVMA 1999 (orthopedic): first dose within 30 min of surgery; second dose if surgery lasted >90 min.\n4. Stop at closure unless you are treating an established infection.\nWillie’s left ear is infected: treatment, not clean prophylaxis.", size=13, color=INK)
notes(s, "Do not attribute 22 mg/kg every 90 minutes to AAHA 2022. That guideline says when: 30 to 60 minutes before incision, skip clean OHE, stop postop. Whittem 1999 timed a second dose if surgery lasted more than 90 minutes. Gonzalez 2017 used 22 mg/kg IV. Elective canine OHE: skip the 14-day cephalexin prescription.")

# 20 Sequence
s = new_content("Sequence of patient preparation", "Prep room, then operating room")
steps = [
    ("1", "Anesthetized, airway in, IV in, depth adequate"),
    ("2", "Express bladder if abdominal / caudal surgery"),
    ("3", "Clip with #40, vacuum hair, dirty antiseptic"),
    ("4", "Move to OR, position, pad, tie, final check"),
    ("5", "Sterile prep. Skin: 7.5% PVP-I ~5 min, rinse, paint 5% vet solution, dry. Eye: Roberts 1:50 of 10% stock"),
    ("6", "Four-quadrant towels → large drape"),
    ("7", "Surgeon gowns/gloves (or already gowned)"),
    ("8", "Timeout / checklist → announce incision"),
]
for i, (n, t) in enumerate(steps):
    col = i % 4
    row = i // 4
    x = Inches(0.45) + Inches(col * 3.2)
    y = Inches(1.25) + Inches(row * 2.7)
    add_round(s, x, y, Inches(3.05), Inches(2.4), WHITE)
    add_rect(s, x, y, Inches(3.05), Inches(0.7), NAVY if row == 0 else TEAL)
    add_text(s, x, y, Inches(3.05), Inches(0.7), n, size=24, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), y + Inches(0.85), Inches(2.75), Inches(1.35), t, size=15, color=INK, align=PP_ALIGN.CENTER)
notes(s, "Airway and plane before clippers. Veterinary Betadine labels: 7.5% scrub, lather about 5 minutes, rinse, paint 5% Solution Veterinary, allow to dry. Eye: Roberts 1986, 1:50 of 10% PVP-I stock, 2-minute scrub plus 2-minute soak. Do not paint 10% from the veterinary bottle; that bottle is 5%.")

# 21 Hair
s = new_content("Hair removal", "#40 clipper after induction. Field 20 cm beyond the planned incision.")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), "Too narrow. Hair remains at the margin.", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "clip_cat.jpg", Inches(0.4), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), "24 hours after OHE. Clip width was adequate.", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "spay_incision.jpg", Inches(6.75), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(0.4), Inches(5.18), Inches(12.55), Inches(1.9), WHITE)
add_text(s, Inches(0.6), Inches(5.32), Inches(12.2), Inches(1.6), "1. Airway in and a surgical plane before the clippers start.  2. #40 clipper, with the grain then against, to the skin.  3. Rectangle: xiphoid to pubis, widely lateral past the nipples, 20 cm beyond the incision. OHE, castration, and limb: clip a field the drape can cover. Orthopedic hang-prep: wrap the dirty foot, then prep from the incision toward the foot.\nPhotos: Uwe Gille, CC0; Liannadavis, CC BY-SA 4.0.", size=13, color=INK)
notes(s, "Left photo is still too narrow. Right is a real 24-hour OHE. Willie: TECA field is pinna and skull. MoMo: skip the clippers.")

# 22 Antiseptics
s = new_content("Skin antiseptics", "Read the bottle. Cite the label or the paper. Do not invent a Fossum page.")
add_round(s, Inches(0.40), Inches(1.08), Inches(12.52), Inches(1.42), GOLD_LT)
add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.42), "Human Betadine Solution = 10% PVP-I (1% available iodine).  Veterinary Betadine Solution = 5% PVP-I (0.5% available iodine).", size=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(1.52), Inches(12.2), Inches(0.88), "Roberts 1986 used 10% stock.  1 mL + 49 mL saline = 1:50 = 0.2% PVP-I.  If the bottle is veterinary 5%, 1 mL + 24 mL (1:25) matches that 0.2%.\nA 1:50 of the 5% veterinary bottle is 0.1% PVP-I, not the Roberts concentration.", size=13, color=INK, align=PP_ALIGN.CENTER)
add_round(s, Inches(0.40), Inches(2.62), Inches(4.10), Inches(4.42), WHITE)
add_rect(s, Inches(0.40), Inches(2.62), Inches(4.10), Inches(0.50), TEAL)
add_text(s, Inches(0.40), Inches(2.62), Inches(4.10), Inches(0.50), "CHG (Nolvasan label)", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(3.18), Inches(3.80), Inches(3.70), "2% chlorhexidine acetate surgical scrub.\n1. Rinse, apply 1–5 mL, wash 2 to 4 minutes, wipe foam.\n2. Avoid eyes and mucous membranes; flush if contact.\n3. Trunk and intact skin. Cornea or middle ear: dilute PVP-I.\n4. Choose one agent for the field: CHG or iodine.\n5. 70% alcohol: rinse between cycles on intact skin; allow to dry; keep off mucosa, eye, and cautery.", size=12, color=INK)
add_round(s, Inches(4.62), Inches(2.62), Inches(4.10), Inches(4.42), WHITE)
add_rect(s, Inches(4.62), Inches(2.62), Inches(4.10), Inches(0.50), GOLD)
add_text(s, Inches(4.62), Inches(2.62), Inches(4.10), Inches(0.50), "Skin (Betadine vet labels)", size=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(4.77), Inches(3.18), Inches(3.80), Inches(3.70), "1. Dirty prep first (organic matter inactivates iodine).\n2. 7.5% scrub (0.75% available iodine).\n3. After clip: wet, lather about 5 minutes, rinse with sterile water.\n4. Paint BETADINE Solution Veterinary 5% (not 10%), allow to dry, then drape.\n5. Solution is labeled full strength for skin and mucous membranes; avoid pooling.\n6. Use detergent-free SOLUTION, not 7.5% scrub, on mucosa.", size=12, color=INK)
add_round(s, Inches(8.84), Inches(2.62), Inches(4.08), Inches(4.42), WHITE)
add_rect(s, Inches(8.84), Inches(2.62), Inches(4.08), Inches(0.50), NAVY)
add_text(s, Inches(8.84), Inches(2.62), Inches(4.08), Inches(0.50), "Eye (Roberts 1986)", size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.99), Inches(3.18), Inches(3.78), Inches(3.70), "Canine ocular surface. Stock = 10% PVP-I (1% available iodine).\n1. 1:50 recommended: 2-minute scrub + 2-minute soak.\n2. 1:2, 1:10, and 1:50 all cleared culture.\n3. One instance of epithelial corneal edema at 1:2 (15 eyes).\n4. 1:100 less consistent (E. coli in 1 of 16).\nDo not put full-strength 5% or 10% on the cornea.", size=12, color=INK)
notes(s, "Write the bottle math on the board. Veterinary Betadine Solution is 5 percent, not 10 percent. Roberts 1986: 1 to 50 of 10 percent stock, 2-minute scrub plus 2-minute soak. One case of corneal edema at 1 to 2. Nolvasan: 2 percent CHG acetate, wash 2 to 4 minutes, keep out of eyes. Willie: swollen tympanum. Canal and periocular mucosa: detergent-free dilute PVP-I, not 7.5 percent scrub.")

# 23 Technique
s = new_content("Patient skin preparation technique", "Center to periphery. Dirty prep, then sterile prep.")
add_pic(s, "prep_spiral_antiseptic.png", Inches(0.4), Inches(1.15), Inches(7.4), Inches(5.9))
add_round(s, Inches(7.95), Inches(1.15), Inches(4.9), Inches(5.9), WHITE)
add_text(s, Inches(8.15), Inches(1.3), Inches(4.55), Inches(0.4), "Technique", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(8.1), Inches(1.75), Inches(4.55), Inches(5.0), [
    "1. Dirty prep in the prep room; sterile prep in the OR.",
    "2. Start at the planned incision. Spiral out. Drop each sponge after the outer ring.",
    "3. Skin: 7.5% PVP-I, lather ~5 min, rinse, paint 5% vet solution, dry (Betadine labels). Nolvasan CHG: wash 2 to 4 min. Drain pools, then drape.",
    "4. Eye: 10% PVP-I stock 1:50 (1 mL + 49 mL). 2 min scrub + 2 min soak (Roberts 1986). 5% bottle: 1:25 to match 0.2%.",
    "5. Willie: swollen tympanic membrane. Periocular and canal mucosa: detergent-free dilute PVP-I, not 7.5% scrub.",
], size=12, spacing=5)
notes(s, "Mime the spiral. Clock about 5 minutes for veterinary Betadine scrub on intact skin. Recite Roberts 1 to 50 of 10 percent stock for the eye: 2 minutes plus 2 minutes. If the bottle is 5 percent veterinary solution, 1 to 25 matches 0.2 percent.")

# 24 Position
s = new_content("Patient positioning", "Dorsal recumbency, airway, IV catheter, monitoring, V-trough")
add_pic(s, "dog_or.jpg", Inches(0.35), Inches(1.12), Inches(8.35), Inches(5.95))
add_round(s, Inches(8.85), Inches(1.12), Inches(4.1), Inches(5.95), WHITE)
add_text(s, Inches(9.05), Inches(1.28), Inches(3.75), Inches(0.45), "Visible in this photograph", size=16, bold=True, color=NAVY)
add_text(s, Inches(9.05), Inches(1.8), Inches(3.75), Inches(5.0), "• ET tube + pulse ox\n• IV catheter + fluids\n• Anesthesia machine\n• V-trough / padding\n• Ties snug, then check the pulse distal to each tie\n• Clip after a surgical plane of anesthesia\n\nKeep the hips in a neutral spread.\nLubricate the eyes. Confirm the tube is patent.\n\nPhoto: Anja, CC BY-SA 4.0.", size=14, color=INK)
notes(s, "Airway and monitoring are on before the clip. Keep hips in a neutral spread.")

# 25 Draping
s = new_content("Draping", "Four-quadrant towels, then the large drape")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), "OHE: hair visible at the drape edge", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "cherry_point_spay.jpg", Inches(0.4), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), "Sterile field: gown, glove, drape", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "hektor_drape.jpg", Inches(6.75), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(0.4), Inches(5.18), Inches(12.55), Inches(1.9), WHITE)
add_text(s, Inches(0.6), Inches(5.32), Inches(12.2), Inches(1.6), "1. Near towel first. Four towels box the field.  2. Re-clip or re-drape until the window is hair-free.  3. Large drape over towels; cuff your hands.  4. If the drape is soaked through, cover or replace it. Hands stay on the field.\nPhotos: Cpl. Samuel A. Nasso, USMC, public domain; MSgt Carlotta Holley, USAF, public domain.", size=14, color=INK)
notes(s, "Left is a real spay with hair at the window. Re-clip or re-drape. Then timeout before you cut.")

# 26 Gloving
s = new_content("Closed gloving and the anesthesia workstation", "Technique diagram and operating-room photograph")
add_pic(s, "prep_closed_gloving.png", Inches(0.35), Inches(1.12), Inches(6.3), Inches(4.15))
add_pic(s, "hektor_or.jpg", Inches(6.75), Inches(1.12), Inches(6.2), Inches(4.15))
add_round(s, Inches(0.35), Inches(5.38), Inches(12.6), Inches(1.7), WHITE)
add_text(s, Inches(0.55), Inches(5.5), Inches(12.2), Inches(1.45), "Left: closed-gloving technique (hands stay inside the gown cuffs). Right: cap, mask, ECG/SpO2/ETCO2, circle system, IV fluids, airway. Monitoring is on before the first drug. Willie needed this for an ear clean. MoMo: the record stopped at preoperative evaluation.\nPhoto: MSgt Carlotta Holley, U.S. Air Force, public domain.", size=14, color=INK)
notes(s, "Call out closed gloving. Students name SpO2, ETCO2, ECG, temp, fluids off the workstation photo.")

# 27 Asepsis + protect
s = new_content("Breaks in asepsis", "Recognize, announce, correct. Then protect the patient.")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(3.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.35), "If you contaminate", size=16, bold=True, color=TEAL)
add_text(s, Inches(0.7), Inches(1.70), Inches(5.7), Inches(2.8), "Say it immediately. Re-glove, re-gown, or re-drape. Name the break once. Fix it completely.\n\nAfter the incision is made, the same rule: notice, announce, correct. Sleeve in the abdomen, instrument off the table, hole in a glove: stop and fix it.", size=15, color=INK)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(3.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.35), "Protect the patient", size=16, bold=True, color=NAVY)
add_text(s, Inches(7.05), Inches(1.70), Inches(5.6), Inches(2.8), "1. Control significant hemorrhage.\n2. Create a secure abdominal wall closure.\n3. Achieve and maintain an aseptic field.\n4. Identify and protect adjacent organs before you clamp.\n5. Complete a sponge and instrument count before closure.", size=15, color=INK)
add_round(s, Inches(0.45), Inches(4.85), Inches(12.4), Inches(2.10), GOLD_LT)
add_text(s, Inches(0.7), Inches(5.05), Inches(11.95), Inches(1.75), "The operation is not over when the last skin suture is placed. Intra-abdominal hemorrhage from poor ligation, or herniation from a weak linea, can kill the patient after you have left the OR. That is why postoperative care is part of this lecture.", size=16, color=NAVY)
notes(s, "Praise the person who says I just contaminated my sleeve. Then re-glove. Ureter injury is a calm, well-exposed patient problem.")

# 28 Knowledge check
s = new_content("Knowledge check", "What do you do next?")
rows = [
    ("A", "When do you clip the OHE field?", "After induction, immediately before the scrub."),
    ("B", "How do you prep conjunctiva with iodine?", "Draw 10% PVP-I stock (1% available iodine). Dilute 1:50 (1 mL + 49 mL). 2 min scrub + 2 min soak (Roberts 1986). If the bottle is 5% vet solution, 1:25 matches 0.2%."),
    ("C", "A blocked cat with K+ 8.2 is booked for PU this morning. First move?", "1. Calcium, fluids, insulin/dextrose as indicated. 2. Decompress. 3. Recheck K+. 4. Then decide on anesthesia."),
    ("D", "CHG runs into the eye during a trunk scrub. Next three steps?", "1. Stop the prep. 2. Irrigate with sterile saline. 3. Reassess the cornea, then finish the field with dilute PVP-I."),
]
for i, (let, q, a) in enumerate(rows):
    y = Inches(1.15) + Inches(i * 1.4)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.28), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.28), NAVY)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.28), let, size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.4), y + Inches(0.1), Inches(11.1), Inches(0.5), q, size=15, bold=True, color=INK)
    add_text(s, Inches(1.4), y + Inches(0.65), Inches(11.1), Inches(0.5), a, size=14, color=TEAL)
notes(s, "Two minutes. B is Roberts 1986 bottle math. D is CHG off the cornea. C is the stabilize-first cat.")

# 29 Recovery
s = new_content("Immediate recovery", "Remain with the patient until airway and circulation are stable")
add_pic(s, "remus_recovery.jpg", Inches(0.35), Inches(1.12), Inches(8.15), Inches(5.95))
add_round(s, Inches(8.6), Inches(1.12), Inches(4.35), Inches(5.95), WHITE)
add_text(s, Inches(8.8), Inches(1.28), Inches(4.0), Inches(0.4), "Recovery priorities", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(8.75), Inches(1.75), Inches(4.05), Inches(5.0), [
    "Extubate when swallow/gag returns (later in brachycephalics).",
    "SpO2, mm, CRT, pulse. Pale + tachycardia after celiotomy: treat as hemorrhage, return to OR.",
    "Rewarm with a blanket or Bair Hugger. Check skin every 15 minutes.",
    "E-collar on before they can lick.",
    "Offer water when fully awake. Small meal when swallowing well.",
    "Willie: skip NSAID after DexSP.",
], size=13, spacing=5)
notes(s, "Real recovery: e-collar, IV, clipped abdomen. Pale OHE: stay at the cage, return to OR if unstable.")

# 30 Flowsheet
s = new_content("Postoperative flowsheet, first 2 hours", "Teaching form")
add_pic(s, "recovery_flowsheet.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "Students should be able to fill this after a spay. Photograph it.")

# 31 Pain + incision
s = new_content("Pain and incision care", "Score pain. Then teach the e-collar.")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.4), "Score pain and record the number", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.65), Inches(1.78), Inches(5.75), Inches(4.7), [
    "Dogs: Glasgow CMPS-SF. Cats: Feline Grimace Scale plus behavior.",
    "Re-score after intervention.",
    "Soft tissue elective: opioid ± NSAID ± local.",
    "Celiotomy / orthopedic: CRIs, extra locals, overnight monitoring.",
    "Send home the opioid + NSAID (if kidneys and GI allow) + the local you already placed. Write the dosing times.",
    "Willie already received DexSP: skip NSAID.",
], size=14, spacing=6)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(5.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.4), "Incision care", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.00), Inches(1.78), Inches(5.65), Inches(4.7), [
    "Look twice daily: swelling, discharge, gapping, smell, heat.",
    "E-collar that actually stays on.",
    "Leash walks only for 14 days. Keep the patient confined indoors otherwise.",
    "Saline if dirty. Skin sutures typically 10–14 days.",
    "Heart or kidney patients: measured fluid rate and a written stop time.",
    "Cats: start a meal the night of surgery.",
], size=14, spacing=6)
notes(s, "Licking and unsupervised running are the two discharge failures after otherwise adequate closure.")

# 32 Complications
s = new_content("Complications in the first 24 hours", "Hemorrhage, airway, hernia, dehiscence, SSI, seroma")
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
    add_text(s, x + Inches(0.35), y + Inches(0.12), Inches(5.7), Inches(0.4), t, size=16, bold=True, color=c)
    add_text(s, x + Inches(0.35), y + Inches(0.55), Inches(5.7), Inches(1.0), d, size=13, color=SLATE)
notes(s, "Hemorrhage versus seroma. Skin versus fascial dehiscence. Evisceration protocol in one breath.")

# 33 Report + discharge
s = new_content("Surgical report and discharge", "What the overnight clinician and the owner both need")
add_round(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), WHITE)
add_text(s, Inches(0.7), Inches(1.28), Inches(5.7), Inches(0.4), "Minimum report elements", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.65), Inches(1.78), Inches(5.75), Inches(4.7), [
    "Date/time, patient ID, surgeon, anesthesia, ASA.",
    "Procedure name and side. Position, clip/prep, approach.",
    "Findings in order. Ligatures, implants, samples.",
    "Suture: layer, material, size, pattern.",
    "Hemostasis, blood loss, sponge count, complications.",
    "Postop plan: fluids, pain, feeding, recheck.",
], size=14, spacing=6)
add_round(s, Inches(6.80), Inches(1.15), Inches(6.05), Inches(5.55), WHITE)
add_text(s, Inches(7.05), Inches(1.28), Inches(5.6), Inches(0.4), "Discharge, verbal and written", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.00), Inches(1.78), Inches(5.65), Inches(4.7), [
    "What we did, in one sentence.",
    "When to start food and water, and how much.",
    "Every medication: name, dose, time, with food?",
    "Incision care and 14-day leash walks.",
    "E-collar on except when directly watching.",
    "Next appointment. ER criteria. After-hours number.",
], size=14, spacing=6)
notes(s, "At 2 a.m. someone opens this record because the abdomen is swelling. They need ligatures, sponge count, linea suture, and whether the client was called.")

# 34 ER criteria
s = new_content("Emergency criteria for discharge", "The client must be able to repeat these")
crit = [
    ("Come now", "Collapse, pale gums, distended/painful abdomen, unstoppable bleeding, vomiting that prevents meds, difficulty breathing, inability to urinate, evisceration, uncontrolled pain, or you are frightened."),
    ("Call today", "Not eating by the next morning (species/procedure dependent), a few episodes of vomiting, mild incision redness, diarrhea, e-collar problems, constipation vs. straining."),
    ("Expected", "Sleepiness tonight, a small bruise near the incision, a slightly tacky incision, a reduced appetite the evening of surgery."),
]
cols_c = [RED, GOLD, GREEN]
for i, ((t, d), c) in enumerate(zip(crit, cols_c)):
    x = Inches(0.45) + Inches(i * 4.25)
    add_round(s, x, Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
    add_rect(s, x, Inches(1.2), Inches(4.05), Inches(0.7), c)
    add_text(s, x, Inches(1.2), Inches(4.05), Inches(0.7), t, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.25), Inches(2.1), Inches(3.55), Inches(4.3), d, size=15, color=INK)
notes(s, "Pale gums + distended abdomen after OHE: come now. Return to OR.")

# 35 Willie plan
s = new_content("Willie: complete perioperative plan", "ASA Status 3-E")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.45), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.28), Inches(11.8), Inches(1.20), "Willie, 6 y 11 mo MN Cavalier, 13.7 kg. Acute vestibular crisis. Severe AS otitis, TM visible/swollen. Circling left, nystagmus fast-left, right knuckling. Grade II murmur. CBC WNL. This is ASA III-E. Client-owned.", size=15, color=NAVY)
wsteps = [
    ("Pre-op", "ASA III-E. Neuro exam. Skip NSAID (DexSP already given). IVF, Cerenia, meclizine. Culture the ear. Radiographs ≠ MRI. Central until proven otherwise."),
    ("Prep", "Airway protected, monitors on, then alfaxalone to a depth that is safe to clip and flush. Periocular and canal mucosa: detergent-free dilute PVP-I (Roberts 1:50 of 10% stock for the eye). Pad him. He falls."),
    ("Intra", "Timeout. Deep clean + cytology. If you contaminate, say it and re-glove. Stay until the canal is clean."),
    ("Post", "Confine, no stairs. Watch neuro signs, vomiting, seizures. MRI next. TECA-LBO only after culture if medical therapy fails."),
]
for i, (t, d) in enumerate(wsteps):
    x = Inches(0.45) + Inches(i * 3.2)
    add_round(s, x, Inches(2.80), Inches(3.05), Inches(4.00), WHITE)
    add_rect(s, x, Inches(2.80), Inches(3.05), Inches(0.55), NAVY)
    add_text(s, x, Inches(2.80), Inches(3.05), Inches(0.55), t, size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), Inches(3.45), Inches(2.75), Inches(3.15), d, size=12, color=INK)
notes(s, "Walk Willie without questions until the end. Then one sentence on MoMo: the same hour of preoperative evaluation cancelled her exploratory.")

# 36 Willie and MoMo
s = new_content("Willie and MoMo", "Both received a preoperative evaluation. Only Willie was anesthetized.")
card(s, Inches(0.45), Inches(1.2), Inches(6.15), Inches(5.5), "Willie, ASA Status 3-E. Proceed with sedation.", "Cavalier, 13.7 kg. Acute vestibular + AS otitis + murmur. Compensated. Fill the anesthesia record. Alfaxalone, monitoring, ear clean, skip NSAID after DexSP. Own the next 24 hours. MRI / possible TECA-LBO later. Assign a new ASA status on the day of that surgery.", accent=GOLD)
card(s, Inches(6.75), Inches(1.2), Inches(6.15), Inches(5.5), "MoMo, ASA Status 4-E. Cancel the exploratory.", "DSH, 4.25 kg. Vomiting that looked like FB. Labs + POCUS + AUS: structural renal disease, creatinine 3.0 → 4.71 on fluids. Exploratory cancelled. NSAIDs contraindicated. Record the decision. Offer supportive care, referral, or euthanasia. That conversation is still surgery.", accent=RED)
notes(s, "Last content slide if time is gone. Healthy Lab OHE is only the ASA I contrast.")

# 37 Key points
s = new_content("Key points", "")
pearls = [
    "ASA is assigned after today’s PE and labs. Willie is III-E (sedate with a plan). MoMo is IV-E (image first, then cancel the exploratory).",
    "Imaging and serial creatinine can cancel a surgery. That is a successful preoperative evaluation.",
    "Elective clean OHE: skip routine postoperative antibiotics. Fill the anesthesia record and the 2-hour recovery sheet.",
    "Clip after induction, #40; spiral prep center → out; re-clip or re-drape until the window is hair-free.",
    "Skin: 7.5% PVP-I ~5 min, then 5% vet paint (Betadine labels), or Nolvasan CHG 2–4 min. Eye: 10% PVP-I 1:50, 2 min + 2 min (Roberts 1986). Cornea/middle ear: dilute PVP-I, not CHG.",
    "Pale + tachycardic after celiotomy: treat as hemorrhage, return to OR; the first 24 hours still count.",
]
for i, t in enumerate(pearls):
    y = Inches(1.15) + Inches(i * 0.9)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(0.8), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(0.8), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(0.8), str(i + 1), size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.4), y, Inches(11.1), Inches(0.8), t, size=15, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Stop here if time is gone. They should defend Willie III-E and MoMo IV-E without looking.")

# 38 Questions + references
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, 0, 0, Inches(0.22), H, GOLD)
add_text(s, Inches(0.75), Inches(0.32), Inches(12), Inches(0.32), "DVM 612  ·  PRINCIPLES OF SURGERY", size=13, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(0.62), Inches(12), Inches(0.55), "Questions", size=32, bold=True, color=WHITE)
add_text(s, Inches(0.75), Inches(1.18), Inches(12), Inches(0.70), "If there are no questions: why was Willie ASA III-E and MoMo ASA IV-E,\nand how do you dilute 10% povidone-iodine for the eye?", size=15, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(1.88), Inches(12), Inches(0.28), "Sources used in this hour. Numbers match the cited label or paper. No invented Fossum page quotes.", size=12, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(2.22), Inches(6.0), Inches(4.10),
         "Course texts\n"
         "1. Fossum TW. Small Animal Surgery. 5th ed. Elsevier; 2018. ISBN 978-0-323-44344-9. Ch. 4, 5, 6, 9. Doses and dilutions on these slides are not quoted from Fossum pages.\n"
         "2. Hendrickson DA, Baird AN. Turner and McIlwraith’s Techniques in Large Animal Surgery. 4th ed. Wiley-Blackwell; 2013. ISBN 978-1-118-27323-4.\n"
         "3. Johnston SA, Tobias KM. Veterinary Surgery: Small Animal. 2nd ed. Elsevier Saunders; 2017 (copyright 2018). ISBN 978-0-323-32065-8.\n"
         "Skin and eye numbers\n"
         "4. Roberts SM, Severin GA, Lavach JD. Am J Vet Res. 1986;47(6):1207–1210. 10% PVP-I stock (1% available iodine); 1:50 recommended; 2-min scrub + 2-min soak.\n"
         "5. BETADINE Surgical Scrub Veterinary, 7.5% PVP-I. DailyMed NDC 67618-154. Lather about 5 min, rinse, paint Solution Veterinary, dry.\n"
         "6. BETADINE Solution Veterinary, 5% PVP-I (not 10%). DailyMed NDC 67618-155.\n"
         "7. Nolvasan Surgical Scrub, 2% chlorhexidine acetate. DailyMed. Wash 2 to 4 min. Avoid eyes and mucous membranes.",
         size=11, color=WHITE)
add_text(s, Inches(6.85), Inches(2.22), Inches(5.9), Inches(4.10),
         "Fasting and antimicrobials\n"
         "8. Frey E, Costin M, Granick J, Kornya M, Weese JS. 2022 AAFP/AAHA Antimicrobial Stewardship Guidelines. J Am Anim Hosp Assoc. 2022;58(4):1–5. Start 30–60 min before incision; skip clean OHE; postop rarely required. Does not publish cefazolin mg/kg.\n"
         "9. Grubb T, Sager J, Gaynor JS, Montgomery E, Parker JA, Shafford H, Tearney C. 2020 AAHA Anesthesia and Monitoring Guidelines for Dogs and Cats. J Am Anim Hosp Assoc. 2020. Healthy adult food fast 4–6 h; water until premedication.\n"
         "10. Whittem TL, Johnson AL, Smith CW, et al. J Am Vet Med Assoc. 1999;215(2):212–216. First dose within 30 min of surgery; second dose if surgery lasted >90 min.\n"
         "11. Gonzalez OJ, Renberg WC, Roush JK, KuKanich B, Warner M. Am J Vet Res. 2017;78(6):695–701. Extra-label cefazolin 22 mg/kg IV studied in dogs.",
         size=11, color=WHITE)
add_text(s, Inches(0.75), Inches(6.42), Inches(12), Inches(0.38), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP  ·  Lewyt College of Veterinary Medicine  ·  Long Island University", size=13, color=GOLD)
notes(s, "Take questions. If none: Willie versus MoMo ASA, then iodine: Roberts 1 to 50 of 10 percent stock, 2 minutes plus 2 minutes on the eye; intact skin is the 7.5 percent scrub for about 5 minutes then 5 percent veterinary paint. Dismiss on time.")

# Stamp numbers
stamp_footers()

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
    "38 slides. Two real hospital cases: Willie (Cavalier, ASA III-E, sedated for ear clean) and MoMo (DSH, ASA IV-E, exploratory cancelled). Owner names, addresses, phones, and emails stay off slides and off this script.",
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
script_path.write_text("\n".join(script_lines), encoding="utf-8")

print(f"Saved {out}")
print(f"Copied {root_copy}")
print(f"Script {script_path}")
print(f"Slides: {len(prs.slides)}")
