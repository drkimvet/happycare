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
# We will append slides then stamp numbers by rebuilding footers — easier to build sequentially
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
# SLIDES
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
add_text(s, Inches(0.75), Inches(5.5), Inches(12), Inches(0.35), "Lecture  |  60 minutes", size=16, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(5.9), Inches(12), Inches(0.7), "Preoperative evaluation · patient and surgeon preparation · postoperative care.\nTwo real hospital cases: Willie (Cavalier, ASA III-E) and MoMo (cat, ASA IV-E — surgery cancelled).", size=14, color=WHITE)
add_text(s, Inches(0.75), Inches(6.62), Inches(12), Inches(0.32), "Required reading: Fossum, Small Animal Surgery, 5th ed. (2018)  ·  Hendrickson & Baird (2013)", size=12, color=GOLD)
notes(s, "Welcome. This hour is preoperative evaluation, patient and surgeon preparation, and postoperative care. Two real patients from the same hospital. Willie, a 6-year 11-month MN Cavalier, 13.7 kg, acute vestibular crisis plus left otitis — we sedated him. MoMo, a 6-year SF DSH, 4.25 kg, vomiting that looked like a foreign-body surgery — imaging cancelled the cut. Assign both ASA statuses. Owner identifiers stay off these slides.")

# 2 Learning objectives
s = new_content("By the end of this hour you will be able to", "Learning objectives")
items = [
    "Perform a preoperative evaluation, assign an ASA status, and decide whether to proceed, delay, or stabilize.",
    "Build a peri-operative plan: fasting, analgesia, antimicrobial prophylaxis, consent, and checklist.",
    "Prepare the patient and surgeon for aseptic surgery (clip, antiseptic prep, four-quadrant drape, gown, closed glove).",
    "Recognize and correct a break in asepsis before and after the incision is made.",
    "Write a postoperative plan, surgical report elements, and client discharge instructions — including 24-hour emergency criteria.",
]
add_bullets(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(4.6), items, size=18, spacing=12)
add_round(s, Inches(0.5), Inches(6.15), Inches(12.3), Inches(0.85), GOLD_LT)
add_text(s, Inches(0.75), Inches(6.25), Inches(11.9), Inches(0.65), "Today is judgment, asepsis, and aftercare. Poor prep cannot be rescued by elegant suture. Willie is the patient we prepare. MoMo is the patient we do not cut.", size=14, color=NAVY)
notes(s, "Read the five objectives aloud. Willie is the running surgical/sedation case. MoMo is the ASA IV-E cat whose preoperative evaluation cancelled an exploratory.")

# 3 Hour plan
s = new_content("Sixty-minute plan", "How we will spend the hour")
plan = [
    ("0–3 min", "Frame + Halsted as the through-line", NAVY),
    ("3–24 min", "I. Preoperative evaluation, ASA, both cases, the record", TEAL),
    ("24–44 min", "II. Patient and surgeon preparation — with pictures", GOLD),
    ("44–57 min", "III. Postoperative care, flowsheet, discharge", GREEN),
    ("57–60 min", "Willie vs MoMo, key points, questions", RED),
]
for i, (t, d, c) in enumerate(plan):
    y = Inches(1.25) + Inches(i * 1.05)
    add_round(s, Inches(0.55), y, Inches(12.2), Inches(0.92), WHITE)
    add_rect(s, Inches(0.55), y, Inches(0.14), Inches(0.92), c)
    add_text(s, Inches(0.95), y + Inches(0.12), Inches(2.3), Inches(0.68), t, size=18, bold=True, color=c, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(3.4), y + Inches(0.12), Inches(9.0), Inches(0.68), d, size=18, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Keep a visible timer. If discussion runs, protect Part II (prep pictures) and both cases. Skip the large-animal slide if you are behind.")

# 4 Why it matters
s = new_content("Why this hour is not optional", "Surgical site infection, harm, and professional standard")
card(s, Inches(0.5), Inches(1.2), Inches(4.0), Inches(2.35), "Most SSIs are preventable", "Hair, skin flora, hypothermia, poor hemostasis, dead space, and broken asepsis — not ‘bad luck’ — drive surgical site infection.", fill=WHITE, accent=TEAL)
card(s, Inches(4.7), Inches(1.2), Inches(4.0), Inches(2.35), "The incision is a contract", "The client trusts you with a living animal (often an elective OHE) that is going home. Operate, document, and speak as if that client is waiting in reception.", fill=WHITE, accent=GOLD)
card(s, Inches(8.9), Inches(1.2), Inches(3.9), Inches(2.35), "Postop starts in preop", "Analgesia, antibiotics, temperature, and client expectations are decided before the scalpel, not at discharge.", fill=WHITE, accent=GREEN)
add_round(s, Inches(0.5), Inches(3.75), Inches(12.3), Inches(3.2), WHITE)
add_text(s, Inches(0.75), Inches(3.9), Inches(11.8), Inches(0.4), "Three verbs for this hour — and they are all yours", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.4), Inches(11.8), Inches(2.3), [
    "Prepare the patient for a surgical procedure.",
    "Prepare yourself for a surgical procedure.",
    "Perform the surgical procedure — and a beautiful closure that bleeds or herniates in recovery is still a failed surgery. The first 24 hours count.",
], size=17, spacing=8)
notes(s, "DVM 612 will hold you to this: a beautiful closure that bleeds in recovery is a failed surgery. The first 24 hours are part of the operation.")

# 5 Halsted
s = new_content("Halsted’s principles — the through-line for today", "Every principle has a preop or postop action, not only an intraoperative one")
principles = [
    ("Gentle tissue handling", "Prep trauma, clipper burn, and crushing towel clamps are tissue handling."),
    ("Meticulous hemostasis", "Preop coagulopathy; postop hemorrhage is a 24-hour emergency."),
    ("Preserve blood supply", "Do not strangulate skin with tight bandages or poorly placed clamps."),
    ("Strict asepsis", "Patient prep, surgeon prep, draping — today’s center of gravity."),
    ("No tension", "Plan incision location and closure now, not after the fascia splits."),
    ("Accurate apposition", "Postop incision care protects the apposition you create."),
    ("Obliterate dead space", "Plan dead space now: sutures, bandage, or a drain with a written pull plan."),
]
for i, (t, d) in enumerate(principles):
    col = i % 2
    row = i // 2
    x = Inches(0.5) + Inches(col * 6.4)
    y = Inches(1.2) + Inches(row * 1.35)
    if i == 6:
        x = Inches(0.5)
        w = Inches(12.3)
    else:
        w = Inches(6.2)
    add_round(s, x, y, w, Inches(1.22), WHITE)
    add_rect(s, x, y, Inches(0.10), Inches(1.22), GOLD)
    add_text(s, x + Inches(0.28), y + Inches(0.12), w - Inches(0.4), Inches(0.38), f"{i+1}.  {t}", size=15, bold=True, color=NAVY)
    add_text(s, x + Inches(0.28), y + Inches(0.52), w - Inches(0.4), Inches(0.58), d, size=13, color=SLATE)
notes(s, "Do not spend more than 2 minutes. Point: every Halsted principle has a preop or postop action, not just an intraoperative one.")

# 6 Continuum
s = new_content("The perioperative continuum", "One patient, three rooms, one surgeon’s responsibility")
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
notes(s, "The red thread: you do not hand off responsibility at the OR door. Anesthesia gets the dog ready for surgical prep; surgery owns prep through the last skin suture; both own recovery.")

# SECTION I
s = new_section("Part I  ·  3–24 minutes", "Preoperative evaluation\nand the peri-operative plan", "History · PE · ASA · two real cases · labs · stabilize · the anesthesia record", "~21 minutes")
notes(s, "Transition. Ask: who has watched an elective surgery get cancelled at induction? That is a successful preop exam.")

# 8 Goals
s = new_content("Goals of the preoperative evaluation", "Decide: proceed  ·  delay  ·  stabilize  ·  refer")
goals = [
    ("Identify surgical disease", "Confirm the lesion, laterality, and that surgery is the right tool — not just ‘the next appointment.’"),
    ("Quantify anesthetic risk", "Assign ASA status yourself after today’s exam and labs. Do not inherit it from the appointment book."),
    ("Find problems you can fix first", "Dehydration, anemia, electrolyte disasters, uncontrolled diabetes, full bladder, pyoderma over the site."),
    ("Plan the day", "Approach, positioning, implants, blood products, ICU bed, who calls the client."),
]
for i, (t, d) in enumerate(goals):
    y = Inches(1.2) + Inches(i * 1.35)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.22), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.9), Inches(1.22), NAVY)
    add_text(s, Inches(0.5), y, Inches(0.9), Inches(1.22), f"{i+1:02d}", size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.65), y + Inches(0.18), Inches(10.8), Inches(0.4), t, size=18, bold=True, color=NAVY)
    add_text(s, Inches(1.65), y + Inches(0.58), Inches(10.8), Inches(0.5), d, size=15, color=SLATE)
notes(s, "Four jobs. Students often skip #3 and #4. Elective surgery on an unstable patient is not bravery.")

# 9 History
s = new_content("History that actually changes the plan", "If you do not ask, you will discover it under the drape")
left = [
    "Signalment: species, breed, age, BCS, sex/neuter — brachycephalic, sighthound, Doberman (vWD), miniature schnauzer (hyperlipidemia).",
    "Presenting complaint vs. elective wellness: ‘just a spay’ still needs a real history.",
    "Prior anesthesia/surgery: difficult intubation, delayed recovery, bleeding, drug reactions.",
    "Medications: NSAIDs, steroids, Apoquel/Cytopoint (skin), insulin, anticonvulsants, heartworm, supplements.",
]
right = [
    "When last ate or drank — and what (including garbage, treats, coprophagia).",
    "Cough, collapse, polyuria/polydipsia, vomiting, diarrhea, heat cycle, last whelping.",
    "Bleeding tendency: petechiae, cavity bleeds, prolonged oozing from venipuncture.",
    "Environment: indoor/outdoor, other animals, zoonoses, client ability to confine postop.",
]
add_round(s, Inches(0.45), Inches(1.2), Inches(6.1), Inches(5.0), WHITE)
add_round(s, Inches(6.75), Inches(1.2), Inches(6.1), Inches(5.0), WHITE)
add_text(s, Inches(0.7), Inches(1.35), Inches(5.6), Inches(0.4), "Patient & medical", size=16, bold=True, color=TEAL)
add_text(s, Inches(7.0), Inches(1.35), Inches(5.6), Inches(0.4), "Risk, drugs, home", size=16, bold=True, color=GOLD)
add_bullets(s, Inches(0.7), Inches(1.85), Inches(5.6), Inches(4.1), left, size=14, spacing=10)
add_bullets(s, Inches(7.0), Inches(1.85), Inches(5.6), Inches(4.1), right, size=14, spacing=10)
notes(s, "Spend 2 minutes. Highlight Doberman/vWD, brachycephalics, and last meal as exam favorites. Never premedicate before you have examined the patient.")

# 10 PE
s = new_content("Physical examination — do it yourself", "Preanesthetic PE, indicated labs, interpret, then assign ASA")
add_bullets(s, Inches(0.5), Inches(1.2), Inches(7.4), Inches(5.5), [
    "Hands-on, systematic: TPR, mm, CRT, hydration, BCS, pain, mentation.",
    "Cardiopulmonary: murmurs, arrhythmias, pulse quality, lung sounds, upper airway.",
    "Surgical site: pyoderma, fleas, otitis, mammary chain, heat, pregnancy, cryptorchid.",
    "Abdomen: pain, distension, organomegaly, fluid wave — and empty the bladder if possible.",
    "Neuro/ortho if relevant: knuckling, neck pain, lameness that changes positioning.",
    "Record it. If it is not written, the next person (and the exam) will assume you skipped it.",
], size=16, spacing=10)
add_round(s, Inches(8.15), Inches(1.2), Inches(4.65), Inches(5.5), NAVY)
add_text(s, Inches(8.4), Inches(1.45), Inches(4.2), Inches(0.7), "Order of operations\nbefore any drug", size=16, bold=True, color=GOLD)
add_text(s, Inches(8.4), Inches(2.3), Inches(4.2), Inches(4.0), "1. Examine the patient\n2. Request indicated labs\n3. Interpret the results\n4. Assign ASA status\n5. Adjust the drug plan\n6. Then premedicate\n\nPremedicating before the exam is a never-event.", size=15, color=WHITE)
notes(s, "Never skip PE because the technician already did vitals. DVM 612 students share patients with anesthesia. The surgeon still owns the decision to proceed.")

# 11 ASA
s = new_content("ASA physical status — memorize this wording", "American Society of Anesthesiologists (ASA) Classification System")
rows = [
    ("1", "Normal, healthy patient", "Healthy 1-year-old OHE", GREEN),
    ("2", "Mild systemic disease, well compensated", "Obesity; asymptomatic murmur; controlled diabetes", TEAL),
    ("3", "Moderate systemic disease that is ongoing but compensated; some functional limitations exist that increase the risk of anesthesia", "Willie — vestibular + otitis, walking, compensated murmur", GOLD),
    ("4", "Severe systemic disease that is a constant threat to life, uncompensated disease, high anesthetic risk because vital body systems involved", "MoMo — rising azotemia, non-functional kidney; GDV; septic abdomen", RED),
    ("5", "Moribund patient not expected to live more than 24 hours with or without surgery", "Gastric rupture; catastrophic trauma; end-stage disease", NAVY),
]
add_rect(s, Inches(0.45), Inches(1.12), Inches(12.4), Inches(0.40), NAVY)
add_text(s, Inches(0.55), Inches(1.12), Inches(2.4), Inches(0.40), "ASA status", size=13, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3.0), Inches(1.12), Inches(6.4), Inches(0.40), "Definition — this is the wording to memorize", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(9.4), Inches(1.12), Inches(3.3), Inches(0.40), "Example", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, (asa, defn, ex, c) in enumerate(rows):
    y = Inches(1.56) + Inches(i * 0.90)
    add_round(s, Inches(0.45), y, Inches(12.4), Inches(0.84), WHITE)
    add_rect(s, Inches(0.45), y, Inches(2.35), Inches(0.84), c)
    add_text(s, Inches(0.45), y, Inches(2.35), Inches(0.84), f"Status {asa}", size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.95), y + Inches(0.06), Inches(6.35), Inches(0.72), defn, size=13, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(9.4), y + Inches(0.06), Inches(3.25), Inches(0.72), ex, size=12, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
add_round(s, Inches(0.45), Inches(6.12), Inches(12.4), Inches(0.95), GOLD_LT)
add_text(s, Inches(0.65), Inches(6.22), Inches(12.05), Inches(0.75), "E = emergency (written Status 3-E or 4-E). Willie is Status 3-E: acute, still compensated. MoMo is Status 4-E: acute, uncompensated, vital systems involved. Assign the number after today’s PE and labs, not from the appointment book.", size=14, color=NAVY)
notes(s, "Read Status 1, then 3, then 4 slowly. This is the wording to memorize. E means emergency. Next: four 60-second cases, then Willie (3-E, we sedated) and MoMo (4-E, we did not cut).")

# 12 ASA practice
s = new_content("Assign the ASA — 60-second cases", "Say the number, then whether you proceed today")
cases = [
    ("A", "Healthy 8-month Labrador for elective OHE. Normal PE, PCV/TS normal.", "ASA Status 1  ·  proceed", GREEN_LT, GREEN),
    ("B", "10-year MN Beagle, BCS 8/9, grade 2/6 murmur, no CHF, dental + mass removal.", "ASA Status 2  ·  proceed with monitoring plan", TEAL_LT, TEAL),
    ("C", "Willie: 6 y 11 mo MN Cavalier, 13.7 kg. Acute ataxia 1 h. AS otitis, TM visible/swollen. Circling left, nystagmus fast-left, right knuckling. Grade II murmur. CV stable.", "ASA Status 3-E  ·  not ‘just dirty ears’ — next slides", GOLD_LT, GOLD),
    ("D", "MoMo: 6 yo SF DSH, 4.25 kg. Acute vomiting ×2, lethargy, construction at home — possible FB. T 98.0 °F, HR 200, mm pink tacky. Mildly enlarged abdomen.", "Do not cut yet. Imaging + labs first  ·  this became ASA Status 4-E, not a surgical abdomen", RED_LT, RED),
]
for i, (let, stem, ans, fill, acc) in enumerate(cases):
    y = Inches(1.2) + Inches(i * 1.35)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.22), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.22), acc)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.22), let, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.45), y + Inches(0.12), Inches(11.0), Inches(0.5), stem, size=15, color=INK)
    add_text(s, Inches(1.45), y + Inches(0.68), Inches(11.0), Inches(0.4), ans, size=14, bold=True, color=acc)
notes(s, "Cold-call four students. C is Willie — we will unpack the sedation. D is MoMo — the preoperative evaluation cancelled the exploratory. The hyperkalemic blocked cat still appears in the knowledge check; do not lose that trap.")

# Real-world ASA III — Willie
s = new_content("Real ASA III case — Willie", "6 y 11 mo MN Cavalier King Charles Spaniel  ·  13.7 kg  ·  BCS 6/9")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.45), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.25), Inches(11.8), Inches(1.25), "Acute ataxia ~1 hour. Fell off the couch twice. Abnormal paw placement. Appetite/thirst normal. Cytopoint for allergies. No prior vestibular signs. Vitals: T 100.8 °F, HR 132, RR 52, mm pink, CRT 2 s, quiet/dull.", size=14, color=NAVY)
card(s, Inches(0.5), Inches(2.75), Inches(4.0), Inches(3.95), "Left ear (AS)", "Brown and bloody discharge. Pedal reflex at the pinna base. Canal patent. Cartilage hardened. Tympanic membrane visible but swollen.", accent=TEAL)
card(s, Inches(4.7), Inches(2.75), Inches(4.0), Inches(3.95), "Neuro exam", "Circling left. Horizontal nystagmus — fast left, slow right. Right knuckling and delayed proprioception. Wheelbarrow absent on the right. That is not a simple peripheral ear.", accent=GOLD)
card(s, Inches(8.9), Inches(2.75), Inches(3.9), Inches(3.95), "Also on PE", "Grade II/VI left systolic murmur (Cavaliers). Heavy tartar. Nasal crusts. Soft non-painful abdomen. Compensated tonight.", accent=RED)
notes(s, "This is Willie. Do not skip the murmur. Right-sided knuckling with left circling is why you cannot call this just an ear flush. Mentation was quiet/dull.")

s = new_content("Why Willie is ASA III-E — and what we actually did", "Compensated  ·  functional limitation  ·  acute  ·  not a constant threat to life")
add_round(s, Inches(0.45), Inches(1.18), Inches(4.05), Inches(5.5), GREEN_LT)
add_text(s, Inches(0.65), Inches(1.35), Inches(3.7), Inches(0.45), "ASA III-E", size=18, bold=True, color=GREEN)
add_text(s, Inches(0.65), Inches(1.85), Inches(3.7), Inches(4.5), "II = murmur alone, or dirty ears without neuro signs.\n\nIII = acute vestibular disease plus severe AS otitis, still pink, walking, kidneys normal.\n\nE = started an hour ago; sedation tonight.\n\nIV = recumbent, seizing, septic, or in heart failure. He was not.", size=14, color=INK)
add_round(s, Inches(4.7), Inches(1.18), Inches(8.1), Inches(5.5), WHITE)
add_text(s, Inches(4.95), Inches(1.35), Inches(7.6), Inches(0.4), "Work-up and peri-op plan (this patient)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(4.9), Inches(1.8), Inches(7.6), Inches(4.6), [
    "CBC WNL. Phosphorus 6.0 (high), glucose 130 (stress). Kidneys, liver, electrolytes normal.",
    "IV fluids, Cerenia IV, DexSP 0.68 mL SQ. No NSAID after the steroid.",
    "Alfaxalone sedation: deep left-ear clean, cytology/culture, 3-view skull/spine films.",
    "Films: bullae radiographically intact, skull intact, L7–S1 discospondylosis — that does not explain acute circling.",
    "Left circling + left-fast nystagmus + right proprioceptive deficit → central until MRI says otherwise.",
    "Home: meclizine 25 mg PO BID × 5 d, Cerenia 60 mg PO SID × 4 d, confine, no stairs. MRI recommended. TECA-LBO if culture-guided medical therapy fails.",
], size=13, spacing=5)
notes(s, "The drum was seen, then ointment was infused. Aminoglycosides are a risk if the middle or inner ear is involved even when the drum looks present and swollen. Cavaliers also bring mitral valve disease and Chiari-like malformation to the vestibular list. Mention both, then return to the ear as the leading infectious cause. No NSAID after DexSP. Next patient: MoMo, the cat we did not take to surgery.")

# Real-world ASA IV — MoMo (surgery cancelled)
s = new_content("Real ASA IV-E case — MoMo", "6 yo SF DSH  ·  4.25 kg  ·  BCS 5/9  ·  same hospital, same week")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.45), RED_LT)
add_text(s, Inches(0.75), Inches(1.25), Inches(11.8), Inches(1.25), "Acute vomiting and lethargy this morning. Two vomits (food, then liquid). Ate normally yesterday. Household construction — possible foreign material or toxin. Refused a favored treat. Vaccines uncertain; last wellness ~2 years. Vitals: T 98.0 °F, HR 200, RR 30, mm pink tacky, CRT <2 s, QAR.", size=14, color=NAVY)
card(s, Inches(0.5), Inches(2.75), Inches(4.0), Inches(3.95), "Why this looked surgical", "FB obstruction was on the list. Discussed IV fluids, serial imaging, and surgery if indicated. Mildly enlarged abdomen. That is how cats get booked for an exploratory.", accent=GOLD)
card(s, Inches(4.7), Inches(2.75), Inches(4.0), Inches(3.95), "What the PE actually showed", "Heart/lungs normal. No murmur. Abdomen mildly enlarged. Ambulatory ×4. No oral, ear, or neuro deficits. Dehydrated. Generalized small stature. The PE did not prove a foreign body.", accent=TEAL)
card(s, Inches(8.9), Inches(2.75), Inches(3.9), Inches(3.95), "Do not skip labs/imaging", "POCUS: abnormal right kidney, left kidney enlarged, bladder intact. 3-view abdomen STAT. CBC/chem. This is why ‘booked for surgery’ is not an ASA.", accent=RED)
notes(s, "Owner identifiers stay off the slide. MoMo is the cat whose films looked like ‘maybe GI’ and were kidneys. Cold-call: who would have clipped her for an exploratory on history alone? That is the mistake this hour exists to prevent.")

s = new_content("Why MoMo is ASA IV-E — and why we did not cut", "Uncompensated  ·  constant threat  ·  acute  ·  not a surgical abdomen")
add_round(s, Inches(0.45), Inches(1.18), Inches(4.05), Inches(5.5), RED_LT)
add_text(s, Inches(0.65), Inches(1.35), Inches(3.7), Inches(0.45), "ASA IV-E", size=18, bold=True, color=RED)
add_text(s, Inches(0.65), Inches(1.85), Inches(3.7), Inches(4.5), "III = compensated disease you can still anesthetize with a plan.\n\nIV = severe systemic disease that is a constant threat — here, rising azotemia and a non-functional kidney.\n\nShe was QAR and walking, so not ASA V (moribund).\n\nE = acute presentation.\n\nA cancelled exploratory is a successful preoperative evaluation.", size=14, color=INK)
add_round(s, Inches(4.7), Inches(1.18), Inches(8.1), Inches(5.5), WHITE)
add_text(s, Inches(4.95), Inches(1.35), Inches(7.6), Inches(0.4), "Work-up that cancelled surgery (this patient)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(4.9), Inches(1.8), Inches(7.6), Inches(4.6), [
    "Admit: IVC, IVF 1.5× maintenance, Cerenia, ondansetron, Unasyn, aluminum hydroxide if eating.",
    "CBC: WBC ~26K with neutrophilia. Platelets variable (74 then 123). Stress glucose.",
    "Chem day 0: BUN 49.7, creatinine 3.0, phosphorus 8.0. USG 1.042 — concentrating, so this is not ‘end-stage CKD, ignore it.’",
    "Repeat on fluids: BUN 100, creatinine 4.71. Do not ignore a rising value you ordered.",
    "AUS: right kidney severely fluid-filled and non-functional; left kidney reduced corticomedullary architecture. Not an FNA target on the right.",
    "Options: IM referral (FNA left kidney) vs palliative vs euthanasia. Prognosis guarded to poor. Owner elected humane euthanasia.",
], size=13, spacing=5)
notes(s, "NSAIDs are contraindicated. Diuresis will not fix a destroyed kidney. If someone still wants to ‘just look inside,’ that is not surgery — that is harm. Be respectful; this cat died. The teaching point is judgment, not spectacle.")

# 13 Labs
s = new_content("Preoperative diagnostics — indicated, not automatic", "Request the minimum tests this patient and this procedure actually need")
card(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(2.7), "Young, healthy, elective (ASA I)", "PCV/TS ± blood glucose and Azo stick is a defensible minimum. Many hospitals still run a preanesthetic chemistry/CBC — know your hospital policy and be able to defend either choice.", accent=TEAL)
card(s, Inches(6.8), Inches(1.2), Inches(6.0), Inches(2.7), "Age, disease, or invasive procedure", "CBC, chemistry, UA. Add clotting (PT/PTT or BMBT) if bleeding risk. T4 in older cats. Blood pressure. ECG if arrhythmia. Imaging if it changes the approach.", accent=GOLD)
add_round(s, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.8), WHITE)
add_text(s, Inches(0.75), Inches(4.25), Inches(11.8), Inches(0.4), "Do not order tests you will ignore — and do not ignore tests you ordered", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.75), Inches(11.8), Inches(1.95), [
    "Anemia, hypoalbuminemia, azotemia, electrolyte storms, and thrombocytopenia change drugs, fluids, and whether you cut today.",
    "For abdominal surgery: consider imaging so you are not ‘exploring’ a pyometra you could have diagnosed, or a mass that needed a different approach. MoMo: POCUS/AUS cancelled the cut.",
    "Large animal: stall-side PCV/TS, fibrinogen, and physical exam often outweigh a full chemistry in the field — still document the risk conversation.",
], size=15, spacing=7)
notes(s, "Avoid dogma. Requesting nothing in a geriatric patient is as wrong as a $800 panel on every puppy. MoMo’s rising creatinine is the example of not ignoring a test you ordered. Next two slides: CBC/chem and EPOC numbers mapped onto ASA Status. They inform the number; they do not replace the PE.")

# CBC/chem → ASA
s = new_content("CBC and chemistry → ASA Status", "Working teaching table  ·  these bands inform Status; they do not assign it by themselves")
add_pic(s, "asa_cbc_chem.png", Inches(0.22), Inches(1.05), Inches(12.9), Inches(6.12))
notes(s, "Ninety seconds. Point at PCV, platelets, creatinine, potassium. Willie: CBC essentially Status 1, phosphorus mild up. His Status 3-E is the vestibular exam, not the chemistry. MoMo: WBC ~26 and creatinine 3.0 then 4.71 push the lab picture into Status 3–4.")

# EPOC → ASA
s = new_content("EPOC / blood gas → ASA Status", "pH, lactate, gases, bicarbonate, base excess")
add_pic(s, "asa_epoc.png", Inches(0.22), Inches(1.05), Inches(12.9), Inches(6.12))
notes(s, "MoMo’s EPOC: pH 7.255 is Status 3; base excess −7.4 is Status 2; lactate 2.05 is Status 1. Do not call a venous pO2 of 33 an arterial Status 4. Whole-patient Status was still 4-E from the kidneys. Willie did not need an EPOC for an ear clean.")

# Apply tables to both cases
s = new_content("Put both patients on the lab tables", "Labs inform ASA. The physical exam still owns the number.")
card(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), "Willie — labs look quieter than the dog", "CBC WNL (Status 1 band).\nPhosphorus 6.0 — mild ↑ (Status 2).\nGlucose 130 — stress (Status 2 band).\nKidneys, liver, electrolytes normal.\nNo EPOC indicated for this ear clean.\n\nASA Status 3-E anyway: acute vestibular disease, severe AS otitis, murmur. Do not down-stage him because the chemistry is pretty.", accent=GOLD)
card(s, Inches(6.75), Inches(1.15), Inches(6.15), Inches(5.55), "MoMo — labs and EPOC support Status 4-E", "WBC ~26K with neutrophilia — Status 3–4 inflammatory band.\nPlatelets 74 K — Status 3.\nCreatinine 3.0 → 4.71; BUN 49.7 → 100 — Status 4 (severe ↑ + uremia).\nPhosphorus 8.0 — Status 3–4.\nEPOC pH 7.255 (Status 3); BE −7.4 (Status 2); lactate 2.05 (Status 1).\nVenous pO2 33 is not arterial hypoxemia.\nWhole patient = Status 4-E. Do not cut.", accent=RED)
notes(s, "This is the payoff slide. Students want to average the columns. Teach: the worst compensated vital-system problem that is a constant threat sets the floor. MoMo’s kidneys set Status 4. Willie’s neuro exam set Status 3 even with a normal CBC.")

# 14 Stabilize
s = new_content("Stabilize before you sterilize", "Elective surgery is cancelled more often by good judgment than by bad luck")
cols = [
    ("Fix first", GREEN, "Hypovolemia / shock\nElectrolyte crises (K+, Na+)\nSevere anemia (transfuse)\nRespiratory distress\nUncontrolled pain\nHypoglycemia\nHyperthermia / heat stroke"),
    ("Often delay elective", GOLD, "Pyoderma over the site\nAnestrus vs. heat if policy\nUnstable endocrine disease\nActive URI in cats\nRecent live vaccines (clinic policy)\nClient cannot confine / medicate\nNo fasting in a full-stomach elective"),
    ("May proceed urgently", RED, "GDV\nSeptic abdomen\nC-section with fetal distress\nAirway obstruction\nHemorrhage you cannot pack\nOpen fracture (after resuscitation)\nUterine rupture / pyometra shock"),
]
for i, (t, c, b) in enumerate(cols):
    x = Inches(0.45) + Inches(i * 4.25)
    add_round(s, x, Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
    add_rect(s, x, Inches(1.2), Inches(4.05), Inches(0.6), c)
    add_text(s, x, Inches(1.2), Inches(4.05), Inches(0.6), t, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.25), Inches(2.0), Inches(3.55), Inches(4.4), b, size=15, color=INK)
notes(s, "One sentence: resuscitation is not delayed for clipping. Elective OHE is delayed for pyoderma. GDV is not delayed for a dental cleaning that was also booked. MoMo is the other direction: do not take a medical kidney cat to an exploratory because FB was on the list.")

# 15 Fasting
s = new_content("Fasting — traditional teaching vs. current practice", "Know both: Fossum/traditional language and AAHA-style shorter fasts")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Working guidance (small animal)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.7), Inches(4.5), [
    "Healthy adult dog/cat: food 4–6 h; water until premedication (AAHA-aligned).",
    "Traditional/Fossum-era: often 8–12 h NPO — still appears on some exams; be able to discuss aspiration vs. hypoglycemia.",
    "Neonates/pediatrics: much shorter fast; offer a small meal 1–2 h prior as directed.",
    "Brachycephalics: shorter fast, careful pre-oxygenation; regurgitation risk is high either way.",
    "Ruminants: longer food withhold (often 12–24 h+) to reduce rumen fill/pressure; water 6–12 h per species/protocol.",
    "Horses: typically 8–12 h grain/hay protocols vary — follow hospital/field SOP.",
], size=14, spacing=7)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Why it matters", size=16, bold=True, color=RED)
add_bullets(s, Inches(7.1), Inches(1.95), Inches(5.5), Inches(4.4), [
    "Goal: less gastric volume and acidity without starving a small patient into hypoglycemia.",
    "A full stomach + recumbency + opioids = regurgitation and aspiration.",
    "Prolonged fasting increases reflux in some dogs and stress in cats.",
    "Always ask what was eaten this morning. Clients feed ‘just a biscuit.’",
    "Diabetics: coordinate insulin and a small meal with anesthesia — do not improvise.",
], size=14, spacing=8)
notes(s, "Teach AAHA-style 4–6 h for healthy small animals as best practice. Older sources still say overnight NPO — explain aspiration vs hypoglycemia. Ruminants are a different physiology, not a different lecture.")

# 16 Consent
s = new_content("Informed consent is a surgical skill", "If you did not say it, you did not consent")
add_bullets(s, Inches(0.5), Inches(1.2), Inches(7.5), Inches(5.5), [
    "Procedure name in plain language, and the reason.",
    "Benefits, alternatives (including no surgery), and what happens if we wait.",
    "Material risks: anesthesia death (rare but real), hemorrhage, infection, dehiscence, incomplete excision, recurrence, incontinence (OHE myth vs. data — be honest).",
    "Estimate: professional fees vs. supplies; what is not included (histopathology, overnight, complications).",
    "Resuscitation code / DNR. Do this before induction, not in recovery.",
    "Who will call whom, and when. Write the client’s phone number on the board.",
], size=16, spacing=9)
add_round(s, Inches(8.2), Inches(1.2), Inches(4.6), Inches(5.5), NAVY)
add_text(s, Inches(8.45), Inches(1.45), Inches(4.15), Inches(0.5), "Client in the lobby", size=16, bold=True, color=GOLD)
add_text(s, Inches(8.45), Inches(2.1), Inches(4.15), Inches(4.2), "Assume every OHE is a client-owned animal going home after recovery in your hospital.\n\nOperate, document, and speak as if that client is waiting in reception — because they are.", size=15, color=WHITE)
notes(s, "Students under-consent electives. A 2-minute risk talk prevents a 2-hour complaint. Mention DNR explicitly.")

# 17 Checklist + analgesia
s = new_content("Checklist and the analgesia plan belong in preop", "Pain is not a postoperative surprise")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Pre-incision checklist (WHO-adapted)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.7), Inches(4.5), [
    "Identity, procedure, site/side confirmed.",
    "Consent, estimate, DNR documented.",
    "ASA, allergies, last meal.",
    "IV catheter patent; fluids running.",
    "Airway secured; monitoring on.",
    "Antibiotics given (if indicated) 30–60 min before incision.",
    "Local block planned (incisional, testicular, TAP, splash).",
    "Instruments, suture, extra gloves, cautery, suction.",
    "Image / implants in the room if needed.",
], size=14, spacing=6)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), WHITE)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Multimodal analgesia — plan it now", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.05), Inches(1.9), Inches(5.55), Inches(4.5), [
    "Opioid (pure µ for most laparotomies) as part of premed or induction.",
    "NSAID if perfusion and kidneys/GI allow — often at recovery, not in hypotensive shock.",
    "Local/regional: the cheapest, safest MAC-sparing tool you have.",
    "Adjuncts: ketamine CRI, dexmedetomidine CRI, gabapentin, acetaminophen (dog only).",
    "Cats: no acetaminophen; careful NSAID choice and dose.",
    "You must be able to discuss recovery and postoperative pain management before the dog leaves the table.",
], size=14, spacing=7)
notes(s, "Checklist takes 90 seconds and prevents wrong-site and forgotten cefazolin. Analgesia: locals are underused by students. Next slides: the kit, then the anesthesia record you actually fill.")

# What you need
s = new_content("What must be in the room", "If it is not here before induction, you are not ready")
add_pic(s, "what_you_need.png", Inches(0.35), Inches(1.12), Inches(12.6), Inches(6.05))
notes(s, "Ninety seconds. Point at Pre-op, then Prep, then Post-op. Ask: what is missing in your teaching lab today? MoMo never needed the clippers. Willie needed monitoring even for an ear clean.")

# Anesthesia record — Willie
s = new_content("Anesthesia / sedation record — Willie", "Fill it before the first drug  ·  this is a teaching form, not a hospital original")
add_pic(s, "anesthesia_record_willie.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "Walk the header: ASA III-E is written before alfaxalone. DexSP means no NSAID. Grid every 5 minutes while sedated. Recovery boxes are part of the same page. Blank template lives with this lecture if they want to photograph it.")

# Anesthesia record — MoMo
s = new_content("The same record — MoMo", "A completed preoperative evaluation can end with do not induce")
add_pic(s, "anesthesia_record_momo.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "This is the point of the hour. The form is not only for patients who get clipped. Recording the decision not to operate is a surgical document. NSAIDs contraindicated. Rising creatinine. Owner elected euthanasia — say it once, respectfully, then move.")

# 18 Abx
s = new_content("Surgical antimicrobial prophylaxis — stewardship, not ritual", "AAHA/AAFP 2022")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), GREEN_LT)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.45), "Usually NO prophylaxis", size=18, bold=True, color=GREEN)
add_text(s, Inches(0.75), Inches(1.9), Inches(5.6), Inches(4.4), "Clean procedures with excellent asepsis:\n• Elective OHE / castration\n• Most clean mass removals\n• Many short soft-tissue surgeries\n\nAntibiotics are not a substitute for sterile technique, Halsted, or a dry field.\n\nOngoing postoperative antibiotics are rarely required after an uncomplicated clean surgery.", size=15, color=INK)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.45), "YES — timed IV, then stop", size=18, bold=True, color=RED)
add_text(s, Inches(7.1), Inches(1.9), Inches(5.5), Inches(4.4), "Give 30–60 min before incision; redose (e.g. cefazolin ~q90 min) if surgery is long or blood loss is large.\n\nConsider if:\n• Clean-contaminated / contaminated / dirty\n• Implant (orthopedic, mesh)\n• Hollow viscus entry\n• Prolonged surgery or known break in asepsis\n• Patient immunocompromised\n• Infection would be catastrophic (some neuro/implant cases — still think, don’t reflex)", size=15, color=INK)
notes(s, "Elective canine OHE is a clean procedure — do not invent a 14-day cephalexin prescription. Willie’s left ear is infected, so antimicrobials are treatment, not clean prophylaxis.")

# 19 Preop check
s = new_content("Knowledge check — preoperative", "Answer before we walk to the prep room")
qs = [
    ("1", "A blocked cat with K+ 8.2 is booked for perineal urethrostomy this morning. First move?", "Stabilize (calcium, fluids, insulin/dextrose as indicated, decompress). Do not induce an ASA IV-E hyperkalemic cat ‘because surgery is on the board.’"),
    ("2", "Healthy 1-year-old OHE. Client asks for ‘antibiotics just in case.’", "Decline routine prophylaxis. Explain asepsis + short clean procedure. Offer a written SSI-watch list instead."),
    ("3", "You assigned ASA I yesterday. Today the dog has a productive cough and fever.", "Reassign ASA, delay elective surgery, work up respiratory disease. ASA is a live assessment."),
]
for i, (n, q, a) in enumerate(qs):
    y = Inches(1.2) + Inches(i * 1.8)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.65), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.65), TEAL)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.65), n, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.45), y + Inches(0.15), Inches(11.0), Inches(0.55), q, size=16, bold=True, color=NAVY)
    add_text(s, Inches(1.45), y + Inches(0.75), Inches(11.0), Inches(0.7), a, size=14, color=SLATE)
notes(s, "Take 2 minutes. Then move. Do not let this become a 10-minute debate.")

# SECTION II
s = new_section("Part II  ·  24–44 minutes", "Patient and surgeon\npreparation", "Clip · antiseptic · position · four-quadrant drape · scrub · gown · closed glove · asepsis", "~20 minutes")
notes(s, "This is the skill cluster for this hour: hair removal, skin prep, positioning, scrubbing/attire, gowning/gloving, draping. Lost asepsis that nobody names is how patients get SSI.")

# 21 Prep scoring map
s = new_content("What we actually check in patient and surgeon prep", "The same six boxes every time you take a patient to surgery")
add_text(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(0.4), "Patient preparation", size=16, bold=True, color=TEAL)
p_items = [("Hair removal", "Clipper, not razor. Adequate field. No clipper burn / missed patches in the field."),
           ("Skin preparation", "Dirty prep then sterile prep. Contact time. Center → periphery. No pooling / wicking."),
           ("Patient positioning", "Secure, padded, physiologically sensible. OHE: dorsal recumbency, straight.")]
for i, (t, d) in enumerate(p_items):
    x = Inches(0.5) + Inches(i * 4.2)
    card(s, x, Inches(1.55), Inches(4.0), Inches(2.15), t, d, accent=TEAL)
add_text(s, Inches(0.5), Inches(3.85), Inches(12.3), Inches(0.35), "Surgeon preparation", size=16, bold=True, color=GOLD)
s_items = [("Scrubbing & attire", "Cap, mask, clean scrubs. Timed or brushless surgical scrub. Hands above elbows."),
           ("Gowning / gloving", "Sterile gown. Closed gloving preferred. Know open gloving for reglove."),
           ("Draping", "Four-quadrant draping is the standard. Hair must not show at the drape edge. Maintain the field.")]
for i, (t, d) in enumerate(s_items):
    x = Inches(0.5) + Inches(i * 4.2)
    card(s, x, Inches(4.25), Inches(4.0), Inches(2.5), t, d, accent=GOLD)
notes(s, "Read the six boxes. Students should be able to name them without mixing in the cutting steps.")

# 22 Sequence
s = new_content("Sequence — do not invert the rooms", "Prep room is dirty. OR is sterile. The dog moves once.")
steps = [
    ("1", "Anesthetized, airway in, IV in, depth adequate"),
    ("2", "Express bladder if abdominal / caudal surgery"),
    ("3", "Clip with #40, vacuum hair, ‘dirty’ antiseptic"),
    ("4", "Move to OR, position, pad, tie, final check"),
    ("5", "Sterile prep (gloved), contact time honored"),
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
notes(s, "Classic fail: clipping in the OR, or sterile prep in the prep room then dragging a wet dog across a dirty corridor without a clean transfer. Another fail: starting the clip before a surgical plane — patient wakes, contaminates, gets clipper lacerations.")

# 23 Hair
s = new_content("Hair removal — clip after induction, not last night", "Real clinic photographs  ·  #40 clipper, not razor  ·  field wide enough to extend")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), "Too narrow — hair still at the margin", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "clip_cat.jpg", Inches(0.4), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), "24 h after OHE — this is the clip you needed", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "spay_incision.jpg", Inches(6.75), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(0.4), Inches(5.18), Inches(12.55), Inches(1.9), WHITE)
add_text(s, Inches(0.6), Inches(5.32), Inches(12.2), Inches(1.6), "Xiphoid (or slightly cranial) to pubis, widely lateral past the nipples — a rectangle, not a bikini strip. Clip with the grain, then against, to the skin. Vacuum. ~20 cm beyond the planned incision. Do not clip the night before. Razor = micro-nicks = higher SSI. Airway in and depth adequate BEFORE the clippers start.\nPhotos: Uwe Gille, CC0 (cat clip); Liannadavis, CC BY-SA 4.0 (OHE incision).", size=14, color=INK)
notes(s, "Left photo is a real clip in progress and still too narrow — that is the teaching point. Right photo is a real 24-hour OHE: the clip is the field you needed yesterday. Willie: TECA field is pinna and skull, not abdomen. MoMo never reached clippers.")

# 24 Common clip fields
s = new_content("Know the field before you pick up the clippers", "If you cannot describe the field, you are not ready to cut")
fields = [
    ("Canine OHE / celiotomy", "Xiphoid → pubis, widely lateral past nipples. Dorsal recumbency."),
    ("Canine castration (prescrotal)", "Scrotum ± prescrotal abdomen; some surgeons shave scrotum, some don’t — follow your hospital SOP. Clip wide enough for drape."),
    ("Feline castration", "Pluck or clip scrotum per SOP. Still aseptic skin prep."),
    ("Canine castration (scrotal ablation)", "Wider perineal/scrotal field; purse-string anus if needed."),
    ("Limb / orthopedic", "Joint above to joint below; hang limb; stirrup; circumferential prep (‘around the world’)."),
    ("Field LA surgery", "Clip still matters. Dirt and fecal contamination are the enemy; sterile-drape ideals are adapted, not abandoned."),
]
for i, (t, d) in enumerate(fields):
    col = i % 3
    row = i // 3
    x = Inches(0.45) + Inches(col * 4.25)
    y = Inches(1.2) + Inches(row * 2.75)
    card(s, x, y, Inches(4.05), Inches(2.55), t, d, accent=TEAL if row == 0 else GOLD)
notes(s, "One minute. Orthopedic hang-prep is the concept they need: the foot is dirty, wrapped, and you prep from incision toward the foot, never reverse.")

# 25 Antiseptics
s = new_content("Skin antiseptics — choose with anatomy, not loyalty", "No single agent is perfect; technique and contact time beat brand")
# table-like cards
add_round(s, Inches(0.45), Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
add_rect(s, Inches(0.45), Inches(1.2), Inches(4.05), Inches(0.7), TEAL)
add_text(s, Inches(0.45), Inches(1.2), Inches(4.05), Inches(0.7), "Chlorhexidine", size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.7), Inches(2.05), Inches(3.6), Inches(4.4), "Broad Gram+ / Gram−, residual 24 h on skin.\nBest with alcohol (CHG–alcohol).\nInactivated by organic debris if too dilute.\nTOXIC to cornea. Ototoxic in the middle ear. Not for peritoneum, bladder, joints, meninges.\nDo not store homemade dilute jugs.", size=14, color=INK)

add_round(s, Inches(4.65), Inches(1.2), Inches(4.05), Inches(5.5), WHITE)
add_rect(s, Inches(4.65), Inches(1.2), Inches(4.05), Inches(0.7), GOLD)
add_text(s, Inches(4.65), Inches(1.2), Inches(4.05), Inches(0.7), "Povidone-iodine", size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(4.9), Inches(2.05), Inches(3.6), Inches(4.4), "Broad spectrum including spores at right conc./time.\nBetter near mucous membranes / some ocular protocols (dilute, veterinarian-directed).\nInactivated by organic matter and alcohol in some sequences.\nSkin/thyroid/iodine sensitivity. Stains.\nMust dry / contact time to work.", size=14, color=INK)

add_round(s, Inches(8.85), Inches(1.2), Inches(4.0), Inches(5.5), WHITE)
add_rect(s, Inches(8.85), Inches(1.2), Inches(4.0), Inches(0.7), NAVY)
add_text(s, Inches(8.85), Inches(1.2), Inches(4.0), Inches(0.7), "Alcohol & others", size=18, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(9.1), Inches(2.05), Inches(3.55), Inches(4.4), "Isopropyl/ethyl alcohol: rapid, no residual, flammable — no pooling near cautery.\nOften the ‘paint’ between CHG scrubs.\nDo not use alcohol on open wounds, mucous membranes, or laser/cautery pools.\nHydrogen peroxide is not a surgical prep.", size=14, color=INK)
notes(s, "CHG–alcohol is a common choice for trunk skin when not contraindicated. Willie’s left ear is exactly where CHG and aminoglycosides can harm a swollen drum and middle ear.")

# 26 Technique
s = new_content("How to scrub the patient", "Technique diagram  ·  center → periphery  ·  real photos are on the clip and drape slides")
add_pic(s, "prep_spiral_antiseptic.png", Inches(0.4), Inches(1.15), Inches(7.4), Inches(5.9))
add_round(s, Inches(7.95), Inches(1.15), Inches(4.9), Inches(5.9), WHITE)
add_text(s, Inches(8.15), Inches(1.3), Inches(4.55), Inches(0.4), "Technique", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(8.1), Inches(1.75), Inches(4.55), Inches(5.0), [
    "Dirty prep in the prep room; sterile prep in the OR.",
    "Start at the planned incision. Spiral out. Never bring a dirty sponge back to the center.",
    "Typical teaching: timed 3–5 min or product cycles, then a final paint.",
    "Damp-to-dry, not a lake.",
    "CHG off the cornea and out of the middle ear — Willie’s swollen drum.",
    "This spiral is a diagram. The clip and drape slides are real clinic photographs.",
], size=13, spacing=6)
notes(s, "Mime the spiral. No open-license spiral-prep photograph was available; this stays a diagram. Real clip, drape, anesthesia, and recovery photos are adjacent.")

# 27 Position
s = new_content("Positioning is physiology, not just ‘on its back’", "Real OR photograph  ·  dorsal recumbency, airway, IV, monitoring, V-trough")
add_pic(s, "dog_or.jpg", Inches(0.35), Inches(1.12), Inches(8.35), Inches(5.95))
add_round(s, Inches(8.85), Inches(1.12), Inches(4.1), Inches(5.95), WHITE)
add_text(s, Inches(9.05), Inches(1.28), Inches(3.75), Inches(0.45), "Name what you see", size=16, bold=True, color=NAVY)
add_text(s, Inches(9.05), Inches(1.8), Inches(3.75), Inches(5.0), "• ET tube + pulse ox\n• IV catheter + fluids\n• Anesthesia machine\n• V-trough / padding\n• Ties that are not tourniquets\n• Abdomen not yet clipped — that is next, after a surgical plane\n\nDo not over-split the hips.\nEyes lubricated. Tube not kinked.\n\nPhoto: Anja, CC BY-SA 4.0.", size=14, color=INK)
notes(s, "This is a real dog in dorsal recumbency. Point: airway and monitoring are on before the clip. Over-splitting femurs is a student habit. GDV positioning can worsen caval compression.")

# 28 Draping
s = new_content("Draping — hair at the edge fails the prep", "Real clinic photographs  ·  gown, glove, box the field, then the large drape")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), "Real OHE — hair still at the drape", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "cherry_point_spay.jpg", Inches(0.4), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), "Real sterile field — gown, glove, drape", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "hektor_drape.jpg", Inches(6.75), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(0.4), Inches(5.18), Inches(12.55), Inches(1.9), WHITE)
add_text(s, Inches(0.6), Inches(5.32), Inches(12.2), Inches(1.6), "Four towels box the field (near towel first). Hair must not show at any edge — re-clip or re-drape. Large drape over towels; cuff your hands. Wet-through is contaminated. Hands stay on the field.\nPhotos: Cpl. Samuel A. Nasso, U.S. Marine Corps, public domain (left); MSgt Carlotta Holley, U.S. Air Force, public domain (right).", size=14, color=INK)
notes(s, "Left is a real spay: gown/mask/drape are present, but hair is still at the window — that is the fail. Right is a real sterile field. Then timeout before you cut.")

# 29 Surgeon
s = new_content("Closed gloving and a real anesthesia workstation", "Diagram for the glove  ·  photograph for the machine")
add_pic(s, "prep_closed_gloving.png", Inches(0.35), Inches(1.12), Inches(6.3), Inches(4.15))
add_pic(s, "hektor_or.jpg", Inches(6.75), Inches(1.12), Inches(6.2), Inches(4.15))
add_round(s, Inches(0.35), Inches(5.38), Inches(12.6), Inches(1.7), WHITE)
add_text(s, Inches(0.55), Inches(5.5), Inches(12.2), Inches(1.45), "Left: closed-gloving technique diagram (hands stay inside the gown cuffs). Right: real K9 anesthesia — cap, mask, ECG/SpO2/ETCO2 monitors, circle system, IV fluids, airway. Monitoring is on before the first drug. Willie needed this for an ear clean. MoMo never reached induction.\nPhoto: MSgt Carlotta Holley, U.S. Air Force, public domain.", size=14, color=INK)
notes(s, "Call out the inset as closed gloving. Students name SpO2, ETCO2, ECG, temp, fluids off the real workstation photo.")

# 30 Asepsis breaks
s = new_content("Breaks in asepsis — recognize, announce, fix", "If you contaminate and stay silent, the patient pays")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Before the incision (prep / drape)", size=16, bold=True, color=TEAL)
add_text(s, Inches(0.75), Inches(1.95), Inches(5.6), Inches(4.4), "If YOU contaminate yourself or the field: say it immediately and correct (re-glove, re-gown, re-drape).\n\nName it once, fix it completely.\n\nA second unrecognized break means you cannot maintain an aseptic field — stop.\n\nThis is how we protect a client-owned animal, not a game of gotcha.", size=15, color=INK)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "After the incision is made", size=16, bold=True, color=RED)
add_text(s, Inches(7.1), Inches(1.95), Inches(5.5), Inches(4.4), "Once the incision is made, there is no free pass.\n\nYou must notice, announce, and completely correct.\n\nIf you do not, or if you correct incompletely, you have put the animal at risk.\n\nExamples: sleeve in the abdomen, instrument off the table used again, hole in glove ignored, dripping sweat onto the field.", size=15, color=INK)
notes(s, "Culture in lab: we praise people who say I just contaminated my sleeve. We do not praise silent heroics.")

# 31 Never-events
s = new_content("Never-events — these stop the surgery", "DVM 612 professional standard  ·  patient safety, not a trivia list")
ev = [
    "1. Fail to control significant hemorrhage.",
    "2. Fail to create a secure abdominal wall closure.",
    "3. Unable to achieve and maintain an aseptic field (patient and surgeon preparation included).",
    "4. Significant damage to other organs (e.g., ureter in a clamp or ligature; removing cervix inappropriately).",
    "5. Any other behavior that puts the animal’s life at risk (retained sponge/instrument is the classic example).",
]
add_bullets(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(4.2), ev, size=18, spacing=12)
add_round(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(1.35), GOLD_LT)
add_text(s, Inches(0.75), Inches(5.75), Inches(11.8), Inches(1.05), "The operation is not over when the last skin suture is placed. Intra-abdominal hemorrhage from poor ligation, or herniation from a weak linea, can kill the patient after you have left the OR. That is why postoperative care is part of this lecture.", size=15, color=NAVY)
notes(s, "Connect hemorrhage, closure, and asepsis to this hour. Ureter injury is a calm, well-prepped, well-exposed patient problem.")

# 32 Prep check
s = new_content("Knowledge check — preparation", "Which of these is acceptable?")
rows = [
    ("A", "Clip the OHE field the night before to save time at induction.", "No. Increases bacterial load and clipper injury."),
    ("B", "Razor the incision line for a ‘closer shave.’", "No. Micro-nicks, higher SSI."),
    ("C", "CHG scrub, then a drop of CHG runs into the eye — rinse and continue.", "Emergency for the eye. CHG is corneal-toxic. Irrigate immediately; do not ‘continue.’"),
    ("D", "Hair visible at the drape edge; you add another towel to cover it.", "Yes — if the added drape is sterile and the field is truly covered. Best is an adequate clip."),
]
for i, (let, q, a) in enumerate(rows):
    y = Inches(1.15) + Inches(i * 1.4)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.28), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.28), NAVY)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.28), let, size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.4), y + Inches(0.1), Inches(11.1), Inches(0.5), q, size=15, bold=True, color=INK)
    add_text(s, Inches(1.4), y + Inches(0.65), Inches(11.1), Inches(0.5), a, size=14, color=TEAL)
notes(s, "C is the safety slide. D is the nuanced yes.")

# SECTION III
s = new_section("Part III  ·  44–57 minutes", "Postoperative care", "Recovery · pain · warmth · wound · 24-hour complications · report · discharge", "~13 minutes")
notes(s, "Shift energy. Students think postop is ‘the techs’ job.’ It is not.")

# 34 Recovery
s = new_content("Immediate recovery — stay with the patient", "Real clinic photograph  ·  e-collar, IV, clipped abdomen, not left alone")
add_pic(s, "remus_recovery.jpg", Inches(0.35), Inches(1.12), Inches(8.15), Inches(5.95))
add_round(s, Inches(8.6), Inches(1.12), Inches(4.35), Inches(5.95), WHITE)
add_text(s, Inches(8.8), Inches(1.28), Inches(4.0), Inches(0.4), "Do not leave", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(8.75), Inches(1.75), Inches(4.05), Inches(4.4), [
    "Extubate when swallow/gag returns (later in brachycephalics).",
    "SpO2, mm, CRT, pulse. Pale + tachycardia after celiotomy = hemorrhage until proven otherwise.",
    "Rewarm; do not burn.",
    "E-collar on before they can lick.",
    "Willie: no NSAID after DexSP.",
], size=13, spacing=6)
add_text(s, Inches(8.8), Inches(6.35), Inches(4.0), Inches(0.55), "Photo: Anja, CC BY-SA 4.0.", size=11, color=MUTED)
notes(s, "Real recovery: e-collar, IV, clipped abdomen. Do not send a pale OHE to the kennel because she looks groggy.")

# Recovery flowsheet
s = new_content("Postoperative flowsheet — first 2 hours", "If it is not written, it was not done  ·  teaching form")
add_pic(s, "recovery_flowsheet.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "Students should be able to fill this after a spay. Call-the-surgeon line at the bottom is the discharge talk they will repeat to clients. Photograph it.")

# 35 Pain
s = new_content("Pain assessment is a vital sign", "If you do not score it, you will not treat it")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Use a scale. Write the number.", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.95), Inches(5.7), Inches(4.5), [
    "Dogs: Glasgow Composite Measure Pain Scale (short form) is a common teaching standard.",
    "Cats: Feline Grimace Scale + behavior (hide, hunched, no groom).",
    "Colorado State University scales are also widely used in teaching hospitals.",
    "Re-score after intervention. A single ‘looks comfortable’ at 10 pm is not a plan.",
    "Large animals: species-specific (horse: pawing, flank watching, reduced appetite; cattle: isolation, bruxism).",
], size=15, spacing=8)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), WHITE)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Treat to the surgery you did", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.05), Inches(1.95), Inches(5.55), Inches(4.5), [
    "Soft tissue elective: opioid ± NSAID ± local is often enough.",
    "Celiotomy / orthopedic: expect more — CRIs, additional locals, overnight monitoring.",
    "Do not send home only tramadol and hope (dogs: weak evidence).",
    "Client: how to give meds, what sedation vs. pain looks like, when to call.",
    "Dysphoria ≠ pain, but treat pain first if unsure.",
], size=15, spacing=8)
notes(s, "Score pain. NSAIDs: not in hypovolemia, kidney injury, GI ulcer, or concurrent steroids — Willie already received DexSP.")

# 36 Wound
s = new_content("The incision after you leave it", "Real 24-hour OHE photograph  ·  protect the apposition you just created")
add_pic(s, "spay_incision.jpg", Inches(0.4), Inches(1.12), Inches(6.4), Inches(5.95))
add_round(s, Inches(6.95), Inches(1.12), Inches(5.95), Inches(5.95), WHITE)
add_text(s, Inches(7.15), Inches(1.28), Inches(5.55), Inches(0.4), "Protect it", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.1), Inches(1.75), Inches(5.6), Inches(4.7), [
    "Look twice daily: swelling, discharge, gapping, smell, heat.",
    "E-collar that actually stays on. Licking is the leading student dehiscence.",
    "Leash only. No running, jumping, wrestling, unsupervised stairs.",
    "Usually no daily CHG scrub. Saline if dirty.",
    "Skin sutures typically 10–14 days if healing is routine.",
    "Photo: Liannadavis, CC BY-SA 4.0.",
], size=14, spacing=7)
notes(s, "Real 24-hour OHE. Licking and basketball-with-the-dog are the two discharge failures. Be concrete: no off-leash for 14 days.")

# 37 Complications
s = new_content("The first 24 hours — what fails a surgery after the OR", "Hemorrhage, hernia, and dehiscence show up after you have gone home")
rows = [
    ("Hemorrhage", "Pale mm, tachycardia, distending abdomen, drip from incision, collapsing. Return to OR. Do not ‘watch overnight’ if unstable.", RED),
    ("Airway / aspiration", "Stertor, crackles, regurg on the pillow. Especially brachycephalics and after opioids.", TEAL),
    ("Hernia / evisceration", "Linea failure. Emergency. Protect viscera with sterile moist towels, opioids, OR now.", NAVY),
    ("Dehiscence (later)", "Often day 3–5 as inflammation peaks and the patient licks. Skin vs. fascia — fascia is the emergency.", GOLD),
    ("SSI", "Redness, pain, discharge, fever, usually after day 3. Culture if indicated. Open, lavage, do not just add a random antibiotic.", GREEN),
    ("Seroma / self-trauma", "Dead space + motion. Usually not an emergency. Restrict, bandage sometimes. Do not drain casually.", TEAL),
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
notes(s, "Spend time on hemorrhage vs. seroma (students confuse them) and skin vs. fascial dehiscence. Evisceration protocol in one breath.")

# 38 Report
s = new_content("Surgical report — if it is not written, it was not done", "The next doctor at 2 a.m. is your audience")
left = [
    "Date/time, patient ID, surgeon, assistant, anesthesia.",
    "Preop diagnosis and ASA.",
    "Procedure name (and side).",
    "Position, clip/prep, approach.",
    "Findings in order of encounter.",
    "What was done — ligatures, implants, samples.",
    "Suture: layer, material, size, pattern.",
    "Hemostasis, estimated blood loss, complications.",
    "Specimens to pathology / culture.",
    "Postop plan: fluids, pain, feeding, urinary, recheck.",
]
add_round(s, Inches(0.5), Inches(1.2), Inches(6.3), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.8), Inches(0.4), "Minimum elements", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.9), Inches(4.5), left, size=15, spacing=5)
add_round(s, Inches(7.05), Inches(1.2), Inches(5.75), Inches(5.5), NAVY)
add_text(s, Inches(7.3), Inches(1.45), Inches(5.3), Inches(0.4), "Why the next doctor cares", size=16, bold=True, color=GOLD)
add_text(s, Inches(7.3), Inches(2.05), Inches(5.3), Inches(4.3), "At 2 a.m. someone will open this record because the abdomen is swelling.\n\nThey need: how the pedicles were ligated, whether a sponge count was complete, what suture is in the linea, and whether the client was already called.\n\nOperate as if that night-call is tonight.", size=16, color=WHITE)
notes(s, "For Willie: neuro exam, ASA III-E, TM visible but swollen, DexSP given, no NSAID, murmur, films, MRI plan.")

# 39 Discharge
s = new_content("Discharge instructions — in the client’s language", "Verbal + written. Teach-back. One caregiver demonstrates the e-collar.")
must = [
    "What we did, in one sentence.",
    "When to start food and water, and how much.",
    "Every medication: name, dose, time, with food?, what if a dose is missed.",
    "Incision care and activity restriction — specific, timed (e.g., 14 days leash-only).",
    "E-collar on except when directly watching.",
    "Next appointment (recheck / suture removal / histopath call).",
    "ER criteria (next slide) with a phone number that answers.",
    "Your name. The hospital number. After-hours number.",
]
for i, t in enumerate(must):
    col = i % 2
    row = i // 2
    x = Inches(0.45) + Inches(col * 6.45)
    y = Inches(1.2) + Inches(row * 1.35)
    add_round(s, x, y, Inches(6.25), Inches(1.22), WHITE)
    add_rect(s, x, y, Inches(0.12), Inches(1.22), GOLD)
    add_text(s, x + Inches(0.4), y, Inches(5.7), Inches(1.22), t, size=15, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Role-play one sentence: ‘If the incision opens and you see fat or intestine, cover with a clean wet towel and come now.’ Students write too much physiology and too few phone numbers.")

# 40 ER criteria
s = new_content("When to come back tonight — teach this verbatim", "If the client cannot repeat these, you did not discharge")
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
notes(s, "Pale gums + distended abdomen after OHE is never ‘wait until morning.’")

# 41 Nutrition fluids
s = new_content("Fluids, feeding, and the rest of the animal", "Surgery is a whole-patient event")
card(s, Inches(0.5), Inches(1.2), Inches(4.0), Inches(5.5), "Fluids", "Continue until eating/drinking and not hypotensive. Match losses (vomiting, drains). Do not fluid-overload heart or kidney patients. Recheck PCV/TS if hemorrhage suspected.", accent=TEAL)
card(s, Inches(4.7), Inches(1.2), Inches(4.0), Inches(5.5), "Nutrition", "Offer water, then a small bland or usual meal when fully awake (procedure-dependent). GI surgery: surgeon specifies. Cats: prevent hepatic lipidosis — do not ‘wait and see’ for days. Consider mirtazapine/capromorelin as directed.", accent=GOLD)
card(s, Inches(8.9), Inches(1.2), Inches(3.9), Inches(5.5), "Other systems", "Urinate before discharge. Bowel movements after laparotomy may lag. Eyes: lubrication after anesthesia. Recheck glucose in diabetics. Walk the dog out — do not assume the crate is fine.", accent=GREEN)
notes(s, "Cats and food. Diabetics and insulin. Short.")

# 42 LA teaser
s = new_content("Large animal — same principles, different dirt", "Field surgery is still Halsted; it is not an excuse to skip clip, gloves, and a drape")
add_bullets(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(5.5), [
    "Field surgery can be aseptic, not ‘sterile theater.’ Clip, wash, sterile gloves/instruments, and a drape still prevent SSI in a castration or displaced abomasum.",
    "Standing sedation vs. general anesthesia changes aspiration, padding, and recovery risk (especially horses).",
    "Tetanus prophylaxis is part of equine/farm-animal postop planning, not an afterthought.",
    "Recovery in a stall: head/eye protection, assist, do not rush to trailering.",
    "Antimicrobial use in food animals has residue and regulatory obligations — prophylaxis is not a default pour-on.",
    "Discharge is often a producer conversation: milk withhold, slaughter withhold, when the animal can rejoin the group.",
], size=17, spacing=10)
notes(s, "One minute. Halsted travels to the barn. Then get back to Willie.")

# 43 Integrated case — Willie
s = new_content("Walk Willie through the whole hour", "You are the surgeon. The owner is in reception.")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.55), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.3), Inches(11.8), Inches(1.25), "Willie, 6 y 11 mo MN Cavalier, 13.7 kg. Acute vestibular crisis. Severe AS otitis, TM visible/swollen. Circling left, nystagmus fast-left, right knuckling. Grade II murmur. CBC WNL. This is ASA III-E. Client-owned.", size=15, color=NAVY)
steps = [
    ("Pre-op", "ASA III-E. Neuro exam. No NSAID (DexSP). IVF, Cerenia, meclizine. Culture the ear. Radiographs ≠ MRI. Central until proven otherwise."),
    ("Prep", "Alfaxalone only after a surgical plane. Clip/prep the ear if you flush. CHG off the eye and drum. Pad him — he falls. Maintain the airway."),
    ("Intra", "Deep clean + cytology. Timeout. If you contaminate, say it. Do not treat this like a 20-minute spay."),
    ("Post", "Confine, no stairs. Watch neuro signs, vomiting, seizures. MRI next. TECA-LBO only after culture if medical therapy fails. You own hour 23."),
]
for i, (t, d) in enumerate(steps):
    x = Inches(0.45) + Inches(i * 3.2)
    add_round(s, x, Inches(2.9), Inches(3.05), Inches(3.85), WHITE)
    add_rect(s, x, Inches(2.9), Inches(3.05), Inches(0.55), NAVY)
    add_text(s, x, Inches(2.9), Inches(3.05), Inches(0.55), t, size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), Inches(3.55), Inches(2.75), Inches(3.0), d, size=12, color=INK)
notes(s, "Walk Willie without questions until the end. Then one sentence on MoMo: the same hour of preoperative evaluation decided not to clip her. A healthy Lab OHE is ASA I and gets no routine antibiotics. Willie is III-E. MoMo is IV-E and not a surgical abdomen.")

# MoMo vs Willie close
s = new_content("Same hour, opposite decisions", "Both are preoperative evaluation  ·  only one reaches the clippers")
card(s, Inches(0.45), Inches(1.2), Inches(6.15), Inches(5.5), "Willie — ASA III-E — proceed (sedation)", "Cavalier, 13.7 kg. Acute vestibular + AS otitis + murmur. Compensated. Fill the anesthesia record. Alfaxalone, monitoring, ear clean, no NSAID after DexSP. Own the next 24 hours. MRI / possible TECA-LBO later — that future surgery still needs a new ASA that day.", accent=GOLD)
card(s, Inches(6.75), Inches(1.2), Inches(6.15), Inches(5.5), "MoMo — ASA IV-E — do not induce", "DSH, 4.25 kg. Vomiting that looked like FB. Labs + POCUS + AUS: structural renal disease, creatinine 3.0 → 4.71 on fluids. Exploratory cancelled. NSAIDs contraindicated. Record the decision. Supportive care vs referral vs euthanasia is still a surgical conversation — you just do not cut.", accent=RED)
notes(s, "This is the last content slide if time is gone. Healthy Lab OHE is only the ASA I contrast.")

# 44 Key points
s = new_content("Key points from this hour", "If you remember six things, remember these")
pearls = [
    "ASA is assigned after today’s PE and labs. Willie is III-E (sedate with a plan). MoMo is IV-E (do not explore).",
    "Imaging and serial creatinine can cancel a surgery. That is a successful preoperative evaluation.",
    "Elective clean OHE: no routine postoperative antibiotics. Fill the anesthesia record and the 2-hour recovery sheet.",
    "Clip after induction, #40, not razor; spiral prep center → out; hair in the drape window fails the prep.",
    "Closed glove; CHG off the cornea and out of the middle ear; announce contamination.",
    "Pale + tachycardic after celiotomy = hemorrhage until proven otherwise; the first 24 hours still count.",
]
for i, t in enumerate(pearls):
    y = Inches(1.15) + Inches(i * 0.9)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(0.8), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(0.8), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(0.8), str(i + 1), size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.4), y, Inches(11.1), Inches(0.8), t, size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Stop here if time is gone. They should defend Willie III-E and MoMo IV-E without looking.")

# 45 Summary
s = new_content("Take-home", "Prepare the patient. Prepare yourself. Own the next 24 hours.")
add_round(s, Inches(0.5), Inches(1.25), Inches(12.3), Inches(5.4), WHITE)
add_text(s, Inches(0.85), Inches(1.6), Inches(11.6), Inches(4.8), "Preoperative evaluation is a decision to proceed, delay, stabilize, refer — or not to operate.\n\nPatient and surgeon preparation is teachable and unforgiving — technique, not luck, prevents SSI.\n\nPostoperative care is part of the operation: pain, warmth, the incision, the record, and the client.\n\nHalsted does not stop when the last throw is buried.", size=20, color=NAVY)
notes(s, "Close the loop to slide 1.")

# 46 References
s = new_content("References", "Sources used in this lecture")
add_bullets(s, Inches(0.5), Inches(1.15), Inches(12.2), Inches(5.6), [
    "Fossum T.W. Small Animal Surgery. 5th ed. Elsevier; 2018. Preoperative evaluation, patient preparation, postoperative care.",
    "Hendrickson D.A., Baird A.N. Turner and McIlwraith’s Techniques in Large Animal Surgery. 4th ed. Wiley-Blackwell; 2013.",
    "Johnston S.A., Tobias K.M. Veterinary Surgery: Small Animal. 2nd ed. Elsevier; 2017.",
    "AAHA/AAFP Antimicrobial Stewardship Guidelines, 2022 — surgical prophylaxis.",
    "AAHA Anesthesia and Monitoring Guidelines (current edition) — fasting, PE, monitoring, recovery.",
    "Clinical photographs (open license or U.S. government work): Uwe Gille (CC0); Anja (CC BY-SA 4.0); Liannadavis (CC BY-SA 4.0); Cpl. Samuel A. Nasso, USMC (public domain); MSgt Carlotta Holley, USAF (public domain). Closed-gloving and spiral-prep figures are technique diagrams, not clinic photographs.",
], size=14, spacing=7)
notes(s, "Fossum is the text behind this hour.")

# 47 Questions
s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, 0, 0, Inches(0.22), H, GOLD)
add_text(s, Inches(0.75), Inches(2.3), Inches(12), Inches(0.5), "DVM 612  ·  PRINCIPLES OF SURGERY", size=16, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(2.85), Inches(12), Inches(1.2), "Questions", size=54, bold=True, color=WHITE)
add_text(s, Inches(0.75), Inches(4.3), Inches(12), Inches(1.2), "If there are no questions: why was Willie ASA III-E and MoMo ASA IV-E —\nand why did only one of them get anesthetized?", size=18, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(6.3), Inches(12), Inches(0.4), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP  ·  Lewyt College of Veterinary Medicine  ·  Long Island University", size=14, color=GOLD)
notes(s, "Take questions. If none: Willie vs MoMo ASA and why only Willie was anesthetized. Dismiss on time.")

# Stamp numbers
stamp_footers()

out = Path("/workspace/lectures/DVM-612_Week4_Preop_PatientPrep_Postop.pptx")
prs.save(str(out))
# Convenience copy at repo root for download
root_copy = Path("/workspace/DVM-612_Week4_Preop_PatientPrep_Postop.pptx")
root_copy.write_bytes(out.read_bytes())

# Instructor script from speaker notes so it cannot drift
script_lines = [
    "DVM 612 — Week 4 instructor script",
    "Instructor: Dr. Yujin Kim, D.V.M., Ph.D., FFCP",
    "",
    "Two real hospital cases: Willie (Cavalier, ASA III-E, sedated for ear clean) and MoMo (DSH, ASA IV-E, exploratory cancelled). Owner names, addresses, phones, and emails stay off slides and off this script.",
    "Skip the large-animal slide if the hour is tight.",
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
