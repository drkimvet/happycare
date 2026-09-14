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
add_text(s, Inches(0.75), Inches(5.9), Inches(12), Inches(0.7), "Preoperative evaluation · patient and surgeon preparation · postoperative care.\nTwo hospital cases: Willie (Cavalier, ASA III-E) and MoMo (cat, ASA IV-E; exploratory cancelled).", size=14, color=WHITE)
add_text(s, Inches(0.75), Inches(6.62), Inches(12), Inches(0.32), "Required reading: Fossum, Small Animal Surgery, 5th ed. (2018)  ·  Hendrickson & Baird (2013)", size=12, color=GOLD)
notes(s, "Welcome. This hour is preoperative evaluation, patient and surgeon preparation, and postoperative care. Two real patients from the same hospital. Willie, a 6-year 11-month MN Cavalier, 13.7 kg, acute vestibular crisis plus left otitis. We sedated him. MoMo, a 6-year SF DSH, 4.25 kg, vomiting that looked like a foreign-body surgery. Imaging cancelled the exploratory. Assign both ASA statuses. Owner identifiers stay off these slides.")

# 2 Learning objectives
s = new_content("Learning objectives", "DVM 612 Week 4")
items = [
    "Perform a preoperative evaluation, assign an ASA status, and decide whether to proceed, delay, or stabilize.",
    "Build a peri-operative plan: fasting, analgesia, antimicrobial prophylaxis, consent, and checklist.",
    "Prepare the patient and surgeon for aseptic surgery: clip, correct antiseptic concentrations (including povidone-iodine 1 to 20 to 1 to 50), four-quadrant drape, gown, closed glove.",
    "Recognize and correct a break in asepsis before and after the incision is made.",
    "Write a postoperative plan, surgical report elements, and client discharge instructions, including 24-hour emergency criteria.",
]
add_bullets(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(4.6), items, size=18, spacing=12)
add_round(s, Inches(0.5), Inches(6.15), Inches(12.3), Inches(0.85), GOLD_LT)
add_text(s, Inches(0.75), Inches(6.25), Inches(11.9), Inches(0.65), "Willie: examine, assign ASA Status 3-E, then sedate. MoMo: examine, image, run labs, then cancel the exploratory.", size=14, color=NAVY)
notes(s, "Read the five objectives aloud. Willie is the running surgical/sedation case. MoMo is the ASA IV-E cat whose preoperative evaluation cancelled an exploratory.")

# 3 Hour plan
s = new_content("Hour plan", "60 minutes")
plan = [
    ("0–3 min", "Introduction and Halsted’s principles", NAVY),
    ("3–24 min", "I. Preoperative evaluation, ASA, both cases, the record", TEAL),
    ("24–44 min", "II. Patient and surgeon preparation", GOLD),
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
s = new_content("Surgical site infection", "Preoperative evaluation, preparation, postoperative care")
card(s, Inches(0.5), Inches(1.2), Inches(4.0), Inches(2.35), "Causes of SSI", "Hair, skin flora, hypothermia, poor hemostasis, dead space, and breaks in asepsis.", fill=WHITE, accent=TEAL)
card(s, Inches(4.7), Inches(1.2), Inches(4.0), Inches(2.35), "Client-owned patients", "Elective OHE patients go home to the owner after recovery. Documentation and the discharge conversation are part of the operation.", fill=WHITE, accent=GOLD)
card(s, Inches(8.9), Inches(1.2), Inches(3.9), Inches(2.35), "Decisions made before incision", "Analgesia, antibiotics, temperature management, and client expectations are set in the preoperative period.", fill=WHITE, accent=GREEN)
add_round(s, Inches(0.5), Inches(3.75), Inches(12.3), Inches(3.2), WHITE)
add_text(s, Inches(0.75), Inches(3.9), Inches(11.8), Inches(0.4), "Surgeon responsibilities", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.4), Inches(11.8), Inches(2.3), [
    "Prepare the patient for a surgical procedure.",
    "Prepare yourself for a surgical procedure.",
    "Perform the procedure. Hemorrhage or herniation in recovery means the surgery failed, even if the closure looked adequate. The first 24 hours are part of the operation.",
], size=17, spacing=8)
notes(s, "A closure that hemorrhages in recovery is a failed surgery. The first 24 hours are part of the operation.")

# 5 Halsted
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
    if i == 6:
        x = Inches(0.5)
        w = Inches(12.3)
    else:
        w = Inches(6.2)
    add_round(s, x, y, w, Inches(1.22), WHITE)
    add_rect(s, x, y, Inches(0.10), Inches(1.22), GOLD)
    add_text(s, x + Inches(0.28), y + Inches(0.12), w - Inches(0.4), Inches(0.38), f"{i+1}.  {t}", size=15, bold=True, color=NAVY)
    add_text(s, x + Inches(0.28), y + Inches(0.52), w - Inches(0.4), Inches(0.58), d, size=13, color=SLATE)
notes(s, "Two minutes, then move. Every Halsted principle has a preop or postop action, not just an intraoperative one.")

# 6 Continuum
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

# SECTION I
s = new_section("Part I  ·  3–24 minutes", "Preoperative evaluation\nand the peri-operative plan", "History · PE · ASA · two real cases · labs · stabilize · the anesthesia record", "~21 minutes")
notes(s, "Transition. Ask: who has watched an elective surgery get cancelled at induction? That is a successful preop exam.")

# 8 Goals
s = new_content("Goals of the preoperative evaluation", "Proceed, delay, stabilize, or refer")
goals = [
    ("Identify surgical disease", "Confirm the lesion, laterality, and that surgery is indicated."),
    ("Quantify anesthetic risk", "Assign ASA status after today’s examination and labs. Write that number on the record."),
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
s = new_content("Preoperative history", "Signalment, medications, last meal, prior anesthesia")
left = [
    "Signalment: species, breed, age, BCS, sex/neuter. Note brachycephalic, sighthound, Doberman (vWD), miniature schnauzer (hyperlipidemia).",
    "Presenting complaint vs. elective wellness: ‘just a spay’ still needs a real history.",
    "Prior anesthesia/surgery: difficult intubation, delayed recovery, bleeding, drug reactions.",
    "Medications: NSAIDs, steroids, Apoquel/Cytopoint (skin), insulin, anticonvulsants, heartworm, supplements.",
]
right = [
    "When last ate or drank, and what (including garbage, treats, coprophagia).",
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
notes(s, "Spend 2 minutes. Highlight Doberman/vWD, brachycephalics, and last meal. Order: examine, then premedicate.")

# 10 PE
s = new_content("Physical examination", "Examine, request indicated labs, interpret, then assign ASA")
add_bullets(s, Inches(0.5), Inches(1.2), Inches(7.4), Inches(5.5), [
    "Hands-on, systematic: TPR, mm, CRT, hydration, BCS, pain, mentation.",
    "Cardiopulmonary: murmurs, arrhythmias, pulse quality, lung sounds, upper airway.",
    "Surgical site: pyoderma, fleas, otitis, mammary chain, heat, pregnancy, cryptorchid.",
    "Abdomen: pain, distension, organomegaly, fluid wave. Empty the bladder if possible.",
    "Neuro/ortho if relevant: knuckling, neck pain, lameness that changes positioning.",
    "Record the examination. The next clinician reads what you wrote.",
], size=16, spacing=10)
add_round(s, Inches(8.15), Inches(1.2), Inches(4.65), Inches(5.5), NAVY)
add_text(s, Inches(8.4), Inches(1.45), Inches(4.2), Inches(0.7), "Order of operations\nbefore any drug", size=16, bold=True, color=GOLD)
add_text(s, Inches(8.4), Inches(2.3), Inches(4.2), Inches(4.0), "1. Examine the patient\n2. Request indicated labs\n3. Interpret the results\n4. Assign ASA status\n5. Adjust the drug plan\n6. Premedicate", size=15, color=WHITE)
notes(s, "Do your own PE, then use the technician vitals as a second set of numbers. DVM 612 students share patients with anesthesia. The surgeon still owns the decision to proceed.")

# 11 ASA
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
add_text(s, Inches(0.65), Inches(6.22), Inches(12.05), Inches(0.75), "E = emergency (written Status 3-E or 4-E). Willie is Status 3-E: acute, still compensated. MoMo is Status 4-E: acute, uncompensated, vital systems involved. Assign the number after today’s PE and labs, not from the appointment book.", size=14, color=NAVY)
notes(s, "Read Status 1, then 3, then 4 slowly. This is the wording to memorize. E means emergency. Next: four 60-second cases, then Willie (3-E, we sedated) and MoMo (4-E, we did not cut).")

# 12 ASA practice
s = new_content("ASA practice cases", "Assign status, then say whether you proceed today")
cases = [
    ("A", "Healthy 8-month Labrador for elective OHE. Normal PE, PCV/TS normal.", "ASA Status 1  ·  proceed", GREEN_LT, GREEN),
    ("B", "10-year MN Beagle, BCS 8/9, grade 2/6 murmur, no CHF, dental + mass removal.", "ASA Status 2  ·  proceed with monitoring plan", TEAL_LT, TEAL),
    ("C", "Willie: 6 y 11 mo MN Cavalier, 13.7 kg. Acute ataxia 1 h. AS otitis, TM visible/swollen. Circling left, nystagmus fast-left, right knuckling. Grade II murmur. CV stable.", "ASA Status 3-E. Not an isolated otitis.", GOLD_LT, GOLD),
    ("D", "MoMo: 6 yo SF DSH, 4.25 kg. Acute vomiting ×2, lethargy, construction at home; possible foreign body. T 98.0 °F, HR 200, mm pink tacky. Mildly enlarged abdomen.", "Stabilize, image, and run labs first. This became ASA Status 4-E. Medical abdomen.", RED_LT, RED),
]
for i, (let, stem, ans, fill, acc) in enumerate(cases):
    y = Inches(1.2) + Inches(i * 1.35)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.22), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.22), acc)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.22), let, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.45), y + Inches(0.12), Inches(11.0), Inches(0.5), stem, size=15, color=INK)
    add_text(s, Inches(1.45), y + Inches(0.68), Inches(11.0), Inches(0.4), ans, size=14, bold=True, color=acc)
notes(s, "Cold-call four students. C is Willie (sedation). D is MoMo (exploratory cancelled). The hyperkalemic blocked cat is in the knowledge check.")

# Willie, ASA Status 3-E
s = new_content("Willie, ASA Status 3-E", "6 y 11 mo MN Cavalier King Charles Spaniel, 13.7 kg, BCS 6/9")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.45), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.25), Inches(11.8), Inches(1.25), "Acute ataxia ~1 hour. Fell off the couch twice. Abnormal paw placement. Appetite/thirst normal. Cytopoint for allergies. No prior vestibular signs. Vitals: T 100.8 °F, HR 132, RR 52, mm pink, CRT 2 s, quiet/dull.", size=14, color=NAVY)
card(s, Inches(0.5), Inches(2.75), Inches(4.0), Inches(3.95), "Left ear (AS)", "Brown and bloody discharge. Pedal reflex at the pinna base. Canal patent. Cartilage hardened. Tympanic membrane visible but swollen.", accent=TEAL)
card(s, Inches(4.7), Inches(2.75), Inches(4.0), Inches(3.95), "Neuro exam", "Circling left. Horizontal nystagmus, fast left, slow right. Right knuckling and delayed proprioception. Wheelbarrow absent on the right. Treat as central vestibular disease until MRI.", accent=GOLD)
card(s, Inches(8.9), Inches(2.75), Inches(3.9), Inches(3.95), "Also on PE", "Grade II/VI left systolic murmur (Cavaliers). Heavy tartar. Nasal crusts. Soft non-painful abdomen. Compensated tonight.", accent=RED)
notes(s, "This is Willie. Record the murmur. Right-sided knuckling with left circling: treat as central vestibular disease plus otitis, then decide on sedation. Mentation was quiet/dull.")

s = new_content("Why Willie is ASA Status 3-E", "Compensated, functional limitation, acute, not a constant threat to life")
add_round(s, Inches(0.45), Inches(1.18), Inches(4.05), Inches(5.5), GREEN_LT)
add_text(s, Inches(0.65), Inches(1.35), Inches(3.7), Inches(0.45), "ASA III-E", size=18, bold=True, color=GREEN)
add_text(s, Inches(0.65), Inches(1.85), Inches(3.7), Inches(4.5), "II = murmur alone, or dirty ears without neuro signs.\n\nIII = acute vestibular disease plus severe AS otitis, still pink, walking, kidneys normal.\n\nE = started an hour ago; sedation tonight.\n\nIV = recumbent, seizing, septic, or in heart failure. He was not.", size=14, color=INK)
add_round(s, Inches(4.7), Inches(1.18), Inches(8.1), Inches(5.5), WHITE)
add_text(s, Inches(4.95), Inches(1.35), Inches(7.6), Inches(0.4), "Work-up and peri-op plan (this patient)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(4.9), Inches(1.8), Inches(7.6), Inches(4.6), [
    "CBC WNL. Phosphorus 6.0 (high), glucose 130 (stress). Kidneys, liver, electrolytes normal.",
    "IV fluids, Cerenia IV, DexSP 0.68 mL SQ. Skip NSAID after the steroid.",
    "Alfaxalone sedation: deep left-ear clean, cytology/culture, 3-view skull/spine films.",
    "Films: bullae radiographically intact, skull intact, L7–S1 discospondylosis. That does not explain acute circling.",
    "Left circling + left-fast nystagmus + right proprioceptive deficit → central until MRI says otherwise.",
    "Home: meclizine 25 mg PO BID × 5 d, Cerenia 60 mg PO SID × 4 d, confine, no stairs. MRI recommended. TECA-LBO if culture-guided medical therapy fails.",
], size=13, spacing=5)
notes(s, "The drum was seen, then ointment was infused. Aminoglycosides are a risk if the middle or inner ear is involved even when the drum looks present and swollen. Cavaliers also bring mitral valve disease and Chiari-like malformation to the vestibular list. Mention both, then return to the ear as the leading infectious cause. Skip NSAID after DexSP. Next patient: MoMo, whose evaluation cancelled surgery.")

# MoMo, ASA Status 4-E
s = new_content("MoMo, ASA Status 4-E", "6 yo SF DSH, 4.25 kg, BCS 5/9")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.45), RED_LT)
add_text(s, Inches(0.75), Inches(1.25), Inches(11.8), Inches(1.25), "Acute vomiting and lethargy this morning. Two vomits (food, then liquid). Ate normally yesterday. Household construction. Possible foreign material or toxin. Refused a favored treat. Vaccines uncertain; last wellness ~2 years. Vitals: T 98.0 °F, HR 200, RR 30, mm pink tacky, CRT <2 s, QAR.", size=14, color=NAVY)
card(s, Inches(0.5), Inches(2.75), Inches(4.0), Inches(3.95), "Why this looked surgical", "FB obstruction was on the list. Discussed IV fluids, serial imaging, and surgery if indicated. Mildly enlarged abdomen. That is how cats get booked for an exploratory.", accent=GOLD)
card(s, Inches(4.7), Inches(2.75), Inches(4.0), Inches(3.95), "What the PE actually showed", "Heart/lungs normal. No murmur. Abdomen mildly enlarged. Ambulatory ×4. No oral, ear, or neuro deficits. Dehydrated. Generalized small stature. The PE did not prove a foreign body.", accent=TEAL)
card(s, Inches(8.9), Inches(2.75), Inches(3.9), Inches(3.95), "Next: labs and imaging", "POCUS: abnormal right kidney, left kidney enlarged, bladder intact. 3-view abdomen STAT. CBC/chem. Assign ASA after those results.", accent=RED)
notes(s, "Owner identifiers stay off the slide. MoMo is the cat whose films looked like ‘maybe GI’ and were kidneys. Cold-call: who would have clipped her for an exploratory on history alone? That is the mistake this hour exists to prevent.")

s = new_content("Why MoMo is ASA Status 4-E", "Uncompensated, constant threat, acute; not a surgical abdomen")
add_round(s, Inches(0.45), Inches(1.18), Inches(4.05), Inches(5.5), RED_LT)
add_text(s, Inches(0.65), Inches(1.35), Inches(3.7), Inches(0.45), "ASA IV-E", size=18, bold=True, color=RED)
add_text(s, Inches(0.65), Inches(1.85), Inches(3.7), Inches(4.5), "III = compensated disease you can still anesthetize with a plan.\n\nIV = severe systemic disease that is a constant threat: rising azotemia and a non-functional kidney.\n\nShe was QAR and walking, so not ASA V (moribund).\n\nE = acute presentation.\n\nA cancelled exploratory is a successful preoperative evaluation.", size=14, color=INK)
add_round(s, Inches(4.7), Inches(1.18), Inches(8.1), Inches(5.5), WHITE)
add_text(s, Inches(4.95), Inches(1.35), Inches(7.6), Inches(0.4), "Work-up that cancelled surgery (this patient)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(4.9), Inches(1.8), Inches(7.6), Inches(4.6), [
    "Admit: IVC, IVF 1.5× maintenance, Cerenia, ondansetron, Unasyn, aluminum hydroxide if eating.",
    "CBC: WBC ~26K with neutrophilia. Platelets variable (74 then 123). Stress glucose.",
    "Chem day 0: BUN 49.7, creatinine 3.0, phosphorus 8.0. USG 1.042 (concentrating). Repeat the values on fluids.",
    "Repeat on fluids: BUN 100, creatinine 4.71. Act on the rising creatinine.",
    "AUS: right kidney severely fluid-filled and non-functional; left kidney reduced corticomedullary architecture. Not an FNA target on the right.",
    "Options: IM referral (FNA left kidney) vs palliative vs euthanasia. Prognosis guarded to poor. Owner elected humane euthanasia.",
], size=13, spacing=5)
notes(s, "NSAIDs are contraindicated. Diuresis will not fix a destroyed kidney. If someone still wants to ‘just look inside,’ that is not surgery. It is harm. Be respectful; this cat died. The teaching point is judgment, not spectacle.")

# 13 Labs
s = new_content("Preoperative diagnostics", "Tests indicated for this patient and this procedure")
card(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(2.7), "Young, healthy, elective (ASA I)", "PCV/TS ± blood glucose and Azo stick is a defensible minimum. Many hospitals still run a preanesthetic chemistry/CBC. Know your hospital policy and be able to defend either choice.", accent=TEAL)
card(s, Inches(6.8), Inches(1.2), Inches(6.0), Inches(2.7), "Age, disease, or invasive procedure", "CBC, chemistry, UA. Add clotting (PT/PTT or BMBT) if bleeding risk. T4 in older cats. Blood pressure. ECG if arrhythmia. Imaging if it changes the approach.", accent=GOLD)
add_round(s, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.8), WHITE)
add_text(s, Inches(0.75), Inches(4.25), Inches(11.8), Inches(0.4), "How to use the tests you order", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.75), Inches(4.75), Inches(11.8), Inches(1.95), [
    "Anemia, hypoalbuminemia, azotemia, electrolyte storms, and thrombocytopenia change drugs, fluids, and whether you cut today.",
    "For abdominal surgery: image first so you know whether you are cutting a pyometra, a mass that needs a different approach, or a medical abdomen. MoMo: POCUS/AUS cancelled the cut.",
    "Large animal: stall-side PCV/TS, fibrinogen, and physical exam often outweigh a full chemistry in the field. Document the risk conversation.",
], size=15, spacing=7)
notes(s, "Request labs that change the plan. MoMo’s rising creatinine is the example: repeat the value, then act. Next two slides: CBC/chem and EPOC numbers mapped onto ASA Status. They inform the number. Today’s PE writes it.")

# CBC/chem → ASA
s = new_content("CBC and chemistry → ASA Status", "These bands inform Status. Today’s PE writes it.")
add_pic(s, "asa_cbc_chem.png", Inches(0.22), Inches(1.05), Inches(12.9), Inches(6.12))
notes(s, "Ninety seconds. Point at PCV, platelets, creatinine, potassium. Willie: CBC essentially Status 1, phosphorus mild up. His Status 3-E is the vestibular exam, not the chemistry. MoMo: WBC ~26 and creatinine 3.0 then 4.71 push the lab picture into Status 3–4.")

# EPOC → ASA
s = new_content("EPOC / blood gas → ASA Status", "pH, lactate, gases, bicarbonate, base excess")
add_pic(s, "asa_epoc.png", Inches(0.22), Inches(1.05), Inches(12.9), Inches(6.12))
notes(s, "MoMo’s EPOC: pH 7.255 is Status 3; base excess −7.4 is Status 2; lactate 2.05 is Status 1. Read venous pO2 33 as venous. Whole-patient Status was still 4-E from the kidneys. Willie: skip the EPOC for this ear clean.")

# Apply tables to both cases
s = new_content("Applying the lab tables", "Labs inform ASA status. The physical examination assigns it.")
card(s, Inches(0.45), Inches(1.15), Inches(6.15), Inches(5.55), "Willie, laboratory results", "CBC WNL (Status 1 band).\nPhosphorus 6.0, mild increase (Status 2).\nGlucose 130, stress (Status 2 band).\nKidneys, liver, electrolytes normal.\nSkip the EPOC for this ear clean.\n\nASA Status 3-E: acute vestibular disease, severe AS otitis, murmur. An unremarkable chemistry leaves the neurologic Status 3 in place.", accent=GOLD)
card(s, Inches(6.75), Inches(1.15), Inches(6.15), Inches(5.55), "MoMo, laboratory results and EPOC", "WBC about 26K with neutrophilia (Status 3 to 4 inflammatory band).\nPlatelets 74 K (Status 3).\nCreatinine 3.0 to 4.71; BUN 49.7 to 100 (Status 4).\nPhosphorus 8.0 (Status 3 to 4).\nEPOC pH 7.255 (Status 3); BE −7.4 (Status 2); lactate 2.05 (Status 1).\nVenous pO2 33 is venous, not arterial hypoxemia.\nWhole-patient status is 4-E. Cancel the exploratory.", accent=RED)
notes(s, "This is the payoff slide. Students want to average the columns. Teach: the worst compensated vital-system problem that is a constant threat sets the floor. MoMo’s kidneys set Status 4. Willie’s neuro exam set Status 3 even with a normal CBC.")

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
notes(s, "One sentence: resuscitate first, then clip. Delay elective OHE for pyoderma. Take GDV to surgery after resuscitation; leave the booked dental for another day. MoMo: image and run labs, then cancel the exploratory.")

# 15 Fasting
s = new_content("Preoperative fasting", "AAHA 4 to 6 hours in healthy dogs and cats; Fossum-era 8 to 12 hours still used in some hospitals")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Working guidance (small animal)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.7), Inches(4.5), [
    "Healthy adult dog/cat: food 4–6 h; water until premedication (AAHA-aligned).",
    "Traditional/Fossum-era: often 8–12 h NPO, still used in some hospitals. Discuss aspiration versus hypoglycemia.",
    "Neonates/pediatrics: much shorter fast; offer a small meal 1–2 h prior as directed.",
    "Brachycephalics: shorter fast, careful pre-oxygenation; regurgitation risk is high either way.",
    "Ruminants: longer food withhold (often 12–24 h+) to reduce rumen fill/pressure; water 6–12 h per species/protocol.",
    "Horses: typically 8–12 h grain/hay protocols vary. Follow the hospital or field SOP.",
], size=14, spacing=7)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Why it matters", size=16, bold=True, color=RED)
add_bullets(s, Inches(7.1), Inches(1.95), Inches(5.5), Inches(4.4), [
    "Goal: less gastric volume and acidity without starving a small patient into hypoglycemia.",
    "A full stomach + recumbency + opioids = regurgitation and aspiration.",
    "Prolonged fasting increases reflux in some dogs and stress in cats.",
    "Always ask what was eaten this morning. Clients feed ‘just a biscuit.’",
    "Diabetics: write the insulin dose and a small meal with anesthesia before drop-off.",
], size=14, spacing=8)
notes(s, "Teach AAHA-style 4–6 h for healthy small animals as best practice. Older sources still say overnight NPO. Explain aspiration versus hypoglycemia. Ruminants are a different physiology, not a different lecture.")

# 16 Consent
s = new_content("Informed consent", "Procedure, risks, alternatives, estimate, resuscitation code")
add_bullets(s, Inches(0.5), Inches(1.2), Inches(7.5), Inches(5.5), [
    "Procedure name in plain language, and the reason.",
    "Benefits, alternatives (including no surgery), and what happens if we wait.",
    "Material risks, in one sentence each: anesthesia death, hemorrhage, infection, dehiscence, incomplete excision, recurrence. After OHE, name urinary incontinence (especially large-breed bitches) and give the true frequency.",
    "Estimate: professional fees vs. supplies; what is not included (histopathology, overnight, complications).",
    "Resuscitation code / DNR. Do this before induction, not in recovery.",
    "Who will call whom, and when. Write the client’s phone number on the board.",
], size=16, spacing=9)
add_round(s, Inches(8.2), Inches(1.2), Inches(4.6), Inches(5.5), NAVY)
add_text(s, Inches(8.45), Inches(1.45), Inches(4.15), Inches(0.5), "Client-owned patients", size=16, bold=True, color=GOLD)
add_text(s, Inches(8.45), Inches(2.1), Inches(4.15), Inches(4.2), "Assume every OHE is a client-owned animal going home after recovery in your hospital.\n\nOperate, document, and speak as if that client is waiting in reception.", size=15, color=WHITE)
notes(s, "Students under-consent electives. A 2-minute risk talk prevents a 2-hour complaint. Mention DNR explicitly.")

# 17 Checklist + analgesia
s = new_content("Pre-incision checklist and analgesia", "WHO-adapted timeout and multimodal plan")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Pre-incision checklist (WHO-adapted)", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.7), Inches(4.5), [
    "Identity, procedure, site/side confirmed.",
    "Consent, estimate, DNR documented.",
    "ASA, allergies, last meal.",
    "IV catheter patent; fluids running.",
    "Airway secured; monitoring on.",
    "Antibiotics given (if indicated) 30 minutes before incision.",
    "Local block planned (incisional, testicular, TAP, splash).",
    "Instruments, suture, extra gloves, cautery, suction.",
    "Image / implants in the room if needed.",
], size=14, spacing=6)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), WHITE)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Multimodal analgesia", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.05), Inches(1.9), Inches(5.55), Inches(4.5), [
    "Opioid (pure µ for most laparotomies) as part of premed or induction.",
    "NSAID if perfusion, kidneys, and GI tract allow. Often given at recovery, not during hypotensive shock.",
    "Local/regional: the cheapest, safest MAC-sparing tool you have.",
    "Adjuncts: ketamine CRI, dexmedetomidine CRI, gabapentin, acetaminophen (dog only).",
    "Cats: no acetaminophen; careful NSAID choice and dose.",
    "You must be able to discuss recovery and postoperative pain management before the dog leaves the table.",
], size=14, spacing=7)
notes(s, "Checklist takes 90 seconds and prevents wrong-site and forgotten cefazolin. Analgesia: locals are underused by students. Next slides: the kit, then the anesthesia record you actually fill.")

# What you need
s = new_content("Equipment and supplies", "Confirm before induction")
add_pic(s, "what_you_need.png", Inches(0.35), Inches(1.12), Inches(12.6), Inches(6.05))
notes(s, "Ninety seconds. Point at Pre-op, then Prep, then Post-op. Ask: what is missing in your teaching lab today? MoMo: skip the clippers; the evaluation cancelled surgery. Willie: monitors on even for an ear clean.")

# Anesthesia record, Willie
s = new_content("Anesthesia record, Willie", "Teaching form. Complete the header before the first drug.")
add_pic(s, "anesthesia_record_willie.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "Walk the header: ASA III-E is written before alfaxalone. DexSP means no NSAID. Grid every 5 minutes while sedated. Recovery boxes are part of the same page. Blank template lives with this lecture if they want to photograph it.")

# Anesthesia record, MoMo
s = new_content("Anesthesia record, MoMo", "Preoperative evaluation documented; induction cancelled")
add_pic(s, "anesthesia_record_momo.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "This is the point of the hour. The form is not only for patients who get clipped. Recording the decision not to operate is a surgical document. NSAIDs contraindicated. Rising creatinine. Owner elected euthanasia. Say it once, respectfully, then continue.")

# 18 Abx
s = new_content("Surgical antimicrobial prophylaxis", "AAHA/AAFP 2022")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), GREEN_LT)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.45), "Clean elective: skip prophylaxis", size=18, bold=True, color=GREEN)
add_text(s, Inches(0.75), Inches(1.9), Inches(5.6), Inches(4.4), "Clean procedures with excellent asepsis:\n• Elective OHE / castration\n• Most clean mass removals\n• Many short soft-tissue surgeries\n\n1. Hold asepsis, Halsted, and a dry field.\n2. Skip peri-op antibiotics on these cases.\n3. After an uncomplicated clean surgery, stop at closure.", size=15, color=INK)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.45), "Indicated: timed IV, then stop", size=18, bold=True, color=RED)
add_text(s, Inches(7.1), Inches(1.9), Inches(5.5), Inches(4.4), "1. Give IV cefazolin 22 mg/kg 30 minutes before incision.\n2. Redose every 90 minutes if the surgery is still open or blood loss is large.\n3. Write the first-dose time from the wound class:\n• Clean-contaminated / contaminated / dirty\n• Implant (orthopedic, mesh)\n• Hollow viscus entry\n• Surgery >90 minutes or a known break in asepsis\n• Patient immunocompromised\n• Infection would be catastrophic (neurologic or implant): decide from this case, then time the dose.", size=15, color=INK)
notes(s, "Elective canine OHE is a clean procedure. Skip the 14-day cephalexin prescription. Willie’s left ear is infected, so antimicrobials are treatment, not clean prophylaxis.")

# 19 Preop check
s = new_content("Knowledge check: preoperative evaluation", "")
qs = [
    ("1", "A blocked cat with K+ 8.2 is booked for perineal urethrostomy this morning. First move?", "1. Calcium, fluids, insulin/dextrose as indicated. 2. Decompress the bladder. 3. Recheck K+. 4. Then decide on anesthesia."),
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
notes(s, "Take 2 minutes. Then move.")

# SECTION II
s = new_section("Part II  ·  24–44 minutes", "Patient and surgeon\npreparation", "Clip · antiseptic · position · four-quadrant drape · scrub · gown · closed glove · asepsis", "~20 minutes")
notes(s, "This is the skill cluster for this hour: hair removal, skin prep, positioning, scrubbing/attire, gowning/gloving, draping. Lost asepsis that nobody names is how patients get SSI.")

# 21 Prep scoring map
s = new_content("Patient and surgeon preparation", "Hair, skin, positioning, scrub, gown and glove, drape")
add_text(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(0.4), "Patient preparation", size=16, bold=True, color=TEAL)
p_items = [("Hair removal", "Clipper, not razor. Adequate field. Clip to skin without clipper burn or missed patches."),
           ("Skin preparation", "Dirty then sterile. PVP-I: 5 minutes wet contact. Mucosa/eye: 1 to 20 to 1 to 50."),
           ("Patient positioning", "Secure, padded, physiologically sensible. OHE: dorsal recumbency, straight.")]
for i, (t, d) in enumerate(p_items):
    x = Inches(0.5) + Inches(i * 4.2)
    card(s, x, Inches(1.55), Inches(4.0), Inches(2.15), t, d, accent=TEAL)
add_text(s, Inches(0.5), Inches(3.85), Inches(12.3), Inches(0.35), "Surgeon preparation", size=16, bold=True, color=GOLD)
s_items = [("Scrubbing & attire", "Cap, mask, clean scrubs. Timed or brushless surgical scrub. Hands above elbows."),
           ("Gowning / gloving", "Sterile gown. Closed gloving preferred. Know open gloving for reglove."),
           ("Draping", "Four-quadrant draping is the standard. Re-clip or re-drape until the window is hair-free. Maintain the field.")]
for i, (t, d) in enumerate(s_items):
    x = Inches(0.5) + Inches(i * 4.2)
    card(s, x, Inches(4.25), Inches(4.0), Inches(2.5), t, d, accent=GOLD)
notes(s, "Read the six boxes. Students should be able to name them without mixing in the cutting steps.")

# 22 Sequence
s = new_content("Sequence of patient preparation", "Prep room, then operating room")
steps = [
    ("1", "Anesthetized, airway in, IV in, depth adequate"),
    ("2", "Express bladder if abdominal / caudal surgery"),
    ("3", "Clip with #40, vacuum hair, ‘dirty’ antiseptic"),
    ("4", "Move to OR, position, pad, tie, final check"),
    ("5", "Sterile prep (gloved). PVP-I 5 min wet contact. Mucosa/eye: 1 to 20 to 1 to 50"),
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
notes(s, "Classic fail: clipping in the OR, or sterile prep in the prep room then dragging a wet dog across a dirty corridor without a clean transfer. Another fail: starting the clip before adequate anesthetic depth. The patient wakes, contaminates, and is lacerated. Step 5: 10% PVP-I on intact skin is 5 minutes of wet contact. Lather the 7.5% scrub for 5 minutes, rinse, paint 10% solution, dry before you drape. Mucosa and eye: 1 to 20 to 1 to 50. Eye at 1:50 is a 2-minute scrub plus a 2-minute soak.")

# 23 Hair
s = new_content("Hair removal", "#40 clipper after induction. Field 20 cm beyond the planned incision.")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), "Too narrow. Hair remains at the margin.", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "clip_cat.jpg", Inches(0.4), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), "24 hours after OHE. Clip width was adequate.", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "spay_incision.jpg", Inches(6.75), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(0.4), Inches(5.18), Inches(12.55), Inches(1.9), WHITE)
add_text(s, Inches(0.6), Inches(5.32), Inches(12.2), Inches(1.6), "1. Airway in and a surgical plane before the clippers start.  2. #40 clipper, with the grain then against, to the skin.  3. Rectangle: xiphoid (or slightly cranial) to the pubis, widely lateral past the nipples, 20 cm beyond the incision.  4. Vacuum.  5. Clip after induction, immediately before the scrub.\nPhotos: Uwe Gille, CC0 (cat clip); Liannadavis, CC BY-SA 4.0 (OHE incision).", size=14, color=INK)
notes(s, "Left photo is a real clip in progress and still too narrow. That is the teaching point. Right photo is a real 24-hour OHE: the clip is the field you needed yesterday. Willie: TECA field is pinna and skull, not abdomen. MoMo: stop at imaging; skip the clippers.")

# 24 Common clip fields
s = new_content("Clip fields", "OHE, castration, orthopedic, field surgery")
fields = [
    ("Canine OHE / celiotomy", "Xiphoid → pubis, widely lateral past nipples. Dorsal recumbency."),
    ("Canine castration (prescrotal)", "Scrotum ± prescrotal abdomen; some surgeons shave scrotum, some do not. Follow your hospital SOP. Clip wide enough for drape."),
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
notes(s, "One minute. Orthopedic hang-prep: wrap the dirty foot, then prep from the incision toward the foot.")

# 25 Antiseptics
s = new_content("Skin antiseptics", "Concentrations, dilution, and contact times")
add_round(s, Inches(0.40), Inches(1.08), Inches(12.52), Inches(1.42), GOLD_LT)
add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.42), "10% povidone-iodine SOLUTION  ·  mucosa, conjunctiva, prepuce  ·  dilute  1 to 20  through  1 to 50  in sterile saline", size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(1.52), Inches(12.2), Inches(0.88), "1 mL stock + 19 mL saline = 1:20 = 0.5% PVP-I        ·        1 mL stock + 49 mL saline = 1:50 = 0.2% PVP-I\nIntact skin: 5 minutes wet contact.  Eye at 1:50: 2-minute scrub + 2-minute soak.  Eye, mucosa, prepuce: 10% SOLUTION only.", size=14, color=INK, align=PP_ALIGN.CENTER)

add_round(s, Inches(0.40), Inches(2.62), Inches(4.10), Inches(4.42), WHITE)
add_rect(s, Inches(0.40), Inches(2.62), Inches(4.10), Inches(0.50), TEAL)
add_text(s, Inches(0.40), Inches(2.62), Inches(4.10), Inches(0.50), "Chlorhexidine (3 min)", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(3.22), Inches(3.80), Inches(3.65), "Intact skin: 2% or 4% CHG.\n1. Aqueous CHG: 3 minutes wet.\n2. CHG–alcohol (2%/70%): 30 s dry skin, 2 min moist.\n3. Leave residual 6 hours.\n4. Trunk and intact skin. Cornea or middle ear: switch to dilute PVP-I.\n5. Choose one agent for the field: CHG or iodine.\n6. Mix each dilution immediately before use.", size=12, color=INK)

add_round(s, Inches(4.62), Inches(2.62), Inches(4.10), Inches(4.42), WHITE)
add_rect(s, Inches(4.62), Inches(2.62), Inches(4.10), Inches(0.50), GOLD)
add_text(s, Inches(4.62), Inches(2.62), Inches(4.10), Inches(0.50), "Povidone-iodine (5 min)", size=15, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(4.77), Inches(3.22), Inches(3.80), Inches(3.65), "1. Dirty prep first (organic matter inactivates iodine).\n2. Intact skin: 7.5% scrub, lather 5 min, rinse, paint 10% solution, dry, drape.\n3. Mucosa / eye / prepuce: 10% SOLUTION, dilute 1 to 20 to 1 to 50.\n4. Eye at 1:50: 2-minute scrub + 2-minute soak.\nNot sporicidal at 5 minutes. Residual 90 minutes after dry. Hypersensitivity. Stains.", size=12, color=INK)

add_round(s, Inches(8.84), Inches(2.62), Inches(4.08), Inches(4.42), WHITE)
add_rect(s, Inches(8.84), Inches(2.62), Inches(4.08), Inches(0.50), NAVY)
add_text(s, Inches(8.84), Inches(2.62), Inches(4.08), Inches(0.50), "Alcohol (30 sec)", size=15, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.99), Inches(3.22), Inches(3.78), Inches(3.65), "1. 70% isopropyl or ethyl: 30 seconds, then dry.\n2. Keep fluid off the table and off cautery.\n3. Rinse or paint between CHG cycles on intact skin.\n4. Intact skin only. Wounds, mucosa, or eye: dilute PVP-I.\nSurgical antiseptic = CHG, PVP-I, or alcohol.", size=13, color=INK)
notes(s, "Write the numbers on the board. Intact skin, 7.5% povidone-iodine scrub: lather 5 minutes, rinse, paint 10% solution, dry before draping. Veterinary Betadine label. Mucosa, conjunctiva, prepuce: 10% SOLUTION diluted 1 to 20 to 1 to 50. Eye at 1:50: 2-minute scrub plus 2-minute soak (Roberts, AJVR 1986). Cornea: stay at 1:50; 1:2 (5%) caused corneal edema. Aqueous chlorhexidine: 3 minutes wet contact; residual 6 hours. CHG–alcohol 2%/70%: 30 seconds dry skin, 2 minutes moist skin. Alcohol 70%: 30 seconds, then dry. PVP-I is not sporicidal at 5 minutes. Willie: swollen tympanum. Canal and periocular mucosa: dilute PVP-I.")

# 26 Technique
s = new_content("Patient skin preparation technique", "Center to periphery. Dirty prep, then sterile prep.")
add_pic(s, "prep_spiral_antiseptic.png", Inches(0.4), Inches(1.15), Inches(7.4), Inches(5.9))
add_round(s, Inches(7.95), Inches(1.15), Inches(4.9), Inches(5.9), WHITE)
add_text(s, Inches(8.15), Inches(1.3), Inches(4.55), Inches(0.4), "Technique", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(8.1), Inches(1.75), Inches(4.55), Inches(5.0), [
    "1. Dirty prep in the prep room; sterile prep in the OR.",
    "2. Start at the planned incision. Spiral out. Drop each sponge after the outer ring.",
    "3. PVP-I: 5 minutes wet, rinse, paint 10%, dry. Aqueous CHG: 3 minutes. Drain pools, then drape.",
    "4. Mucosa, conjunctiva, prepuce: 10% PVP-I solution, 1 to 20 to 1 to 50. Eye at 1:50: 2-minute scrub + 2-minute soak.",
    "5. Willie: swollen tympanic membrane. Periocular and canal mucosa: dilute PVP-I.",
], size=13, spacing=6)
notes(s, "Mime the spiral. Clock 5 minutes for povidone-iodine on intact skin. Recite the 1 to 20 to 1 to 50 arithmetic. Eye: 2 minutes plus 2 minutes. No open-license spiral-prep photograph was available; this stays a diagram.")

# 27 Position
s = new_content("Patient positioning", "Dorsal recumbency, airway, IV catheter, monitoring, V-trough")
add_pic(s, "dog_or.jpg", Inches(0.35), Inches(1.12), Inches(8.35), Inches(5.95))
add_round(s, Inches(8.85), Inches(1.12), Inches(4.1), Inches(5.95), WHITE)
add_text(s, Inches(9.05), Inches(1.28), Inches(3.75), Inches(0.45), "Visible in this photograph", size=16, bold=True, color=NAVY)
add_text(s, Inches(9.05), Inches(1.8), Inches(3.75), Inches(5.0), "• ET tube + pulse ox\n• IV catheter + fluids\n• Anesthesia machine\n• V-trough / padding\n• Ties snug, then check the pulse distal to each tie\n• Clip after a surgical plane of anesthesia\n\nKeep the hips in a neutral spread.\nLubricate the eyes. Confirm the tube is patent.\n\nPhoto: Anja, CC BY-SA 4.0.", size=14, color=INK)
notes(s, "This is a real dog in dorsal recumbency. Point: airway and monitoring are on before the clip. Over-splitting femurs is a student habit. GDV positioning can worsen caval compression.")

# 28 Draping
s = new_content("Draping", "Four-quadrant towels, then the large drape. Hair must not show at the edge.")
add_round(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), RED)
add_text(s, Inches(0.4), Inches(1.10), Inches(6.2), Inches(0.38), "OHE: hair visible at the drape edge", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "cherry_point_spay.jpg", Inches(0.4), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), GREEN)
add_text(s, Inches(6.75), Inches(1.10), Inches(6.2), Inches(0.38), "Sterile field: gown, glove, drape", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_pic(s, "hektor_drape.jpg", Inches(6.75), Inches(1.50), Inches(6.2), Inches(3.55))
add_round(s, Inches(0.4), Inches(5.18), Inches(12.55), Inches(1.9), WHITE)
add_text(s, Inches(0.6), Inches(5.32), Inches(12.2), Inches(1.6), "Four towels box the field (near towel first). Hair must not show at any edge. Re-clip or re-drape. Large drape over towels; cuff your hands. Wet-through is contaminated. Hands stay on the field.\nPhotos: Cpl. Samuel A. Nasso, U.S. Marine Corps, public domain (left); MSgt Carlotta Holley, U.S. Air Force, public domain (right).", size=14, color=INK)
notes(s, "Left is a real spay: gown/mask/drape are present, but hair is still at the window. The clip is inadequate. Right is a real sterile field. Then timeout before you cut.")

# 29 Surgeon
s = new_content("Closed gloving and the anesthesia workstation", "Technique diagram and operating-room photograph")
add_pic(s, "prep_closed_gloving.png", Inches(0.35), Inches(1.12), Inches(6.3), Inches(4.15))
add_pic(s, "hektor_or.jpg", Inches(6.75), Inches(1.12), Inches(6.2), Inches(4.15))
add_round(s, Inches(0.35), Inches(5.38), Inches(12.6), Inches(1.7), WHITE)
add_text(s, Inches(0.55), Inches(5.5), Inches(12.2), Inches(1.45), "Left: closed-gloving technique diagram (hands stay inside the gown cuffs). Right: working K9 anesthesia: cap, mask, ECG/SpO2/ETCO2 monitors, circle system, IV fluids, airway. Monitoring is on before the first drug. Willie needed this for an ear clean. MoMo: the record stopped at preoperative evaluation.\nPhoto: MSgt Carlotta Holley, U.S. Air Force, public domain.", size=14, color=INK)
notes(s, "Call out the inset as closed gloving. Students name SpO2, ETCO2, ECG, temp, fluids off the real workstation photo.")

# 30 Asepsis breaks
s = new_content("Breaks in asepsis", "Recognize, announce, and correct")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Before the incision (prep / drape)", size=16, bold=True, color=TEAL)
add_text(s, Inches(0.75), Inches(1.95), Inches(5.6), Inches(4.4), "If you contaminate yourself or the field: say it immediately and correct it. Re-glove, re-gown, or re-drape.\n\nName the break once. Fix it completely.\n\nA second unrecognized break means you cannot maintain an aseptic field. Stop.\n\nThis is how we protect a client-owned animal.", size=15, color=INK)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), RED_LT)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "After the incision is made", size=16, bold=True, color=RED)
add_text(s, Inches(7.1), Inches(1.95), Inches(5.5), Inches(4.4), "Once the incision is made, contamination must still be noticed, announced, and corrected.\n\nIncomplete correction puts the animal at risk.\n\nExamples: sleeve in the abdomen, instrument off the table used again, hole in glove ignored, dripping sweat onto the field.", size=15, color=INK)
notes(s, "Culture in lab: praise the person who says I just contaminated my sleeve. Then re-glove.")

# 31 Protect the patient
s = new_content("Protect the patient", "DVM 612 professional standard")
ev = [
    "1. Control significant hemorrhage.",
    "2. Create a secure abdominal wall closure.",
    "3. Achieve and maintain an aseptic field (patient and surgeon preparation included).",
    "4. Identify and protect adjacent organs (ureter, cervix) before you clamp or ligate.",
    "5. Complete a sponge and instrument count before closure.",
]
add_bullets(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(4.2), ev, size=18, spacing=12)
add_round(s, Inches(0.5), Inches(5.6), Inches(12.3), Inches(1.35), GOLD_LT)
add_text(s, Inches(0.75), Inches(5.75), Inches(11.8), Inches(1.05), "The operation is not over when the last skin suture is placed. Intra-abdominal hemorrhage from poor ligation, or herniation from a weak linea, can kill the patient after you have left the OR. That is why postoperative care is part of this lecture.", size=15, color=NAVY)
notes(s, "Connect hemorrhage, closure, and asepsis to this hour. Ureter injury is a calm, well-prepped, well-exposed patient problem.")

# 32 Prep check
s = new_content("Knowledge check: preparation", "")
rows = [
    ("A", "When do you clip the OHE field?", "After induction, immediately before the scrub."),
    ("B", "How do you take hair down to the skin at the incision?", "#40 clipper, with the grain then against. Clippers, not razors."),
    ("C", "CHG runs into the eye during a trunk scrub. Next three steps?", "1. Stop the prep. 2. Irrigate with sterile saline. 3. Reassess the cornea, then finish the field with dilute PVP-I."),
    ("D", "How do you prep conjunctiva or a prepuce with iodine?", "Draw 10% SOLUTION. Dilute 1 to 20 to 1 to 50. Intact skin: 5 min wet. Eye: 2 min scrub + 2 min soak."),
]
for i, (let, q, a) in enumerate(rows):
    y = Inches(1.15) + Inches(i * 1.4)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.28), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(1.28), NAVY)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(1.28), let, size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.4), y + Inches(0.1), Inches(11.1), Inches(0.5), q, size=15, bold=True, color=INK)
    add_text(s, Inches(1.4), y + Inches(0.65), Inches(11.1), Inches(0.5), a, size=14, color=TEAL)
notes(s, "C is the safety slide. D: 1 to 20 to 1 to 50, 5 minutes wet on intact skin, 2 minutes plus 2 minutes on the eye. Hair at the drape edge: re-clip or re-drape until the window is hair-free.")

# SECTION III
s = new_section("Part III  ·  44–57 minutes", "Postoperative care", "Recovery · pain · warmth · wound · 24-hour complications · report · discharge", "~13 minutes")
notes(s, "Shift energy. Students think postop is ‘the techs’ job.’ It is not.")

# 34 Recovery
s = new_content("Immediate recovery", "Remain with the patient until airway and circulation are stable")
add_pic(s, "remus_recovery.jpg", Inches(0.35), Inches(1.12), Inches(8.15), Inches(5.95))
add_round(s, Inches(8.6), Inches(1.12), Inches(4.35), Inches(5.95), WHITE)
add_text(s, Inches(8.8), Inches(1.28), Inches(4.0), Inches(0.4), "Recovery priorities", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(8.75), Inches(1.75), Inches(4.05), Inches(4.4), [
    "Extubate when swallow/gag returns (later in brachycephalics).",
    "SpO2, mm, CRT, pulse. Pale + tachycardia after celiotomy = hemorrhage until proven otherwise.",
    "Rewarm with a blanket or Bair Hugger. Check skin every 15 minutes.",
    "E-collar on before they can lick.",
    "Willie: no NSAID after DexSP.",
], size=13, spacing=6)
add_text(s, Inches(8.8), Inches(6.35), Inches(4.0), Inches(0.55), "Photo: Anja, CC BY-SA 4.0.", size=11, color=MUTED)
notes(s, "Real recovery: e-collar, IV, clipped abdomen. Pale OHE: treat as hemorrhage, stay at the cage, return to OR if unstable.")

# Recovery flowsheet
s = new_content("Postoperative flowsheet, first 2 hours", "Teaching form")
add_pic(s, "recovery_flowsheet.png", Inches(0.28), Inches(1.08), Inches(12.75), Inches(6.1))
notes(s, "Students should be able to fill this after a spay. Call-the-surgeon line at the bottom is the discharge talk they will repeat to clients. Photograph it.")

# 35 Pain
s = new_content("Pain assessment", "Glasgow CMPS-SF, Feline Grimace Scale, CSU scales")
add_round(s, Inches(0.5), Inches(1.2), Inches(6.1), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.6), Inches(0.4), "Score pain and record the number", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.95), Inches(5.7), Inches(4.5), [
    "Dogs: Glasgow Composite Measure Pain Scale (short form) is a common teaching standard.",
    "Cats: Feline Grimace Scale + behavior (hide, hunched, no groom).",
    "Colorado State University scales are also widely used in teaching hospitals.",
    "Re-score after intervention. A single ‘looks comfortable’ at 10 pm is not a plan.",
    "Large animals: species-specific (horse: pawing, flank watching, reduced appetite; cattle: isolation, bruxism).",
], size=15, spacing=8)
add_round(s, Inches(6.85), Inches(1.2), Inches(5.95), Inches(5.5), WHITE)
add_text(s, Inches(7.1), Inches(1.4), Inches(5.5), Inches(0.4), "Match analgesia to the procedure", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.05), Inches(1.95), Inches(5.55), Inches(4.5), [
    "Soft tissue elective: opioid ± NSAID ± local is often enough.",
    "Celiotomy / orthopedic: expect more: CRIs, additional local blocks, overnight monitoring.",
    "Send home the opioid + NSAID (if kidneys and GI allow) + the local you already placed. Write the dosing times.",
    "Client: how to give meds, what sedation vs. pain looks like, when to call.",
    "Dysphoria ≠ pain, but treat pain first if unsure.",
], size=15, spacing=8)
notes(s, "Score pain. NSAIDs: not in hypovolemia, kidney injury, GI ulcer, or concurrent steroids. Willie already received DexSP.")

# 36 Wound
s = new_content("Incision care", "24-hour OHE photograph")
add_pic(s, "spay_incision.jpg", Inches(0.4), Inches(1.12), Inches(6.4), Inches(5.95))
add_round(s, Inches(6.95), Inches(1.12), Inches(5.95), Inches(5.95), WHITE)
add_text(s, Inches(7.15), Inches(1.28), Inches(5.55), Inches(0.4), "Incision care", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(7.1), Inches(1.75), Inches(5.6), Inches(4.7), [
    "Look twice daily: swelling, discharge, gapping, smell, heat.",
    "E-collar that actually stays on. Licking is the most common cause of dehiscence after otherwise adequate closure.",
    "Leash walks only for 14 days. Keep the patient confined indoors otherwise.",
    "Usually no daily CHG scrub. Saline if dirty.",
    "Skin sutures typically 10–14 days if healing is routine.",
    "Photo: Liannadavis, CC BY-SA 4.0.",
], size=14, spacing=7)
notes(s, "Real 24-hour OHE. Licking and unsupervised running are the two discharge failures I see after otherwise adequate closure. Be concrete: no off-leash activity for 14 days.")

# 37 Complications
s = new_content("Complications in the first 24 hours", "Hemorrhage, airway, hernia, dehiscence, SSI, seroma")
rows = [
    ("Hemorrhage", "Pale mm, tachycardia, distending abdomen, drip from incision, collapsing. Stabilize and return to OR.", RED),
    ("Airway / aspiration", "Stertor, crackles, regurg on the pillow. Especially brachycephalics and after opioids.", TEAL),
    ("Hernia / evisceration", "Linea failure. Emergency. Protect viscera with sterile moist towels, opioids, OR now.", NAVY),
    ("Dehiscence (later)", "Often day 3–5 as inflammation peaks and the patient licks. Skin versus fascia: fascial dehiscence is the emergency.", GOLD),
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
notes(s, "Spend time on hemorrhage vs. seroma (students confuse them) and skin vs. fascial dehiscence. Evisceration protocol in one breath.")

# 38 Report
s = new_content("Surgical report", "Required elements")
left = [
    "Date/time, patient ID, surgeon, assistant, anesthesia.",
    "Preop diagnosis and ASA.",
    "Procedure name (and side).",
    "Position, clip/prep, approach.",
    "Findings in order of encounter.",
    "What was done: ligatures, implants, samples.",
    "Suture: layer, material, size, pattern.",
    "Hemostasis, estimated blood loss, complications.",
    "Specimens to pathology / culture.",
    "Postop plan: fluids, pain, feeding, urinary, recheck.",
]
add_round(s, Inches(0.5), Inches(1.2), Inches(6.3), Inches(5.5), WHITE)
add_text(s, Inches(0.75), Inches(1.4), Inches(5.8), Inches(0.4), "Minimum elements", size=16, bold=True, color=NAVY)
add_bullets(s, Inches(0.7), Inches(1.9), Inches(5.9), Inches(4.5), left, size=15, spacing=5)
add_round(s, Inches(7.05), Inches(1.2), Inches(5.75), Inches(5.5), NAVY)
add_text(s, Inches(7.3), Inches(1.45), Inches(5.3), Inches(0.4), "What the overnight clinician needs", size=16, bold=True, color=GOLD)
add_text(s, Inches(7.3), Inches(2.05), Inches(5.3), Inches(4.3), "At 2 a.m. someone will open this record because the abdomen is swelling.\n\nThey need how the pedicles were ligated, whether a sponge count was complete, what suture is in the linea, and whether the client was already called.", size=16, color=WHITE)
notes(s, "For Willie: neuro exam, ASA III-E, TM visible but swollen, DexSP given, no NSAID, murmur, films, MRI plan.")

# 39 Discharge
s = new_content("Discharge instructions", "Verbal and written. Teach-back. One caregiver demonstrates the e-collar.")
must = [
    "What we did, in one sentence.",
    "When to start food and water, and how much.",
    "Every medication: name, dose, time, with food?, what if a dose is missed.",
    "Incision care and activity restriction. Specify duration (example: 14 days leash only).",
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

# 41 Nutrition fluids
s = new_content("Fluids, feeding, and other systems", "")
card(s, Inches(0.5), Inches(1.2), Inches(4.0), Inches(5.5), "Fluids", "Continue until eating/drinking and not hypotensive. Match losses (vomiting, drains). Heart or kidney patients: measured rate and a written stop time. Recheck PCV/TS if hemorrhage is suspected.", accent=TEAL)
card(s, Inches(4.7), Inches(1.2), Inches(4.0), Inches(5.5), "Nutrition", "1. Offer water when fully awake. 2. Small bland or usual meal (procedure-dependent). 3. GI surgery: follow the surgeon’s timeline. 4. Cats: start a meal the night of surgery. Add mirtazapine or capromorelin if intake is low.", accent=GOLD)
card(s, Inches(8.9), Inches(1.2), Inches(3.9), Inches(5.5), "Other systems", "Walk the dog out. Confirm a urination. Lubricate the eyes. Recheck glucose in diabetics. Bowel movements after laparotomy may lag. Confirm the crate actually confines.", accent=GREEN)
notes(s, "Cats and food. Diabetics and insulin. Short.")

# 42 LA teaser
s = new_content("Large animal surgery", "Clip, gloves, and a drape still apply in the field")
add_bullets(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(5.5), [
    "Field surgery can be aseptic, not ‘sterile theater.’ Clip, wash, sterile gloves/instruments, and a drape still prevent SSI in a castration or displaced abomasum.",
    "Standing sedation vs. general anesthesia changes aspiration, padding, and recovery risk (especially horses).",
    "Tetanus prophylaxis is part of equine/farm-animal postop planning, not an afterthought.",
    "Recovery in a stall: protect the head and eyes, assist to standing, then trailer after the horse is stable.",
    "Antimicrobial use in food animals: write milk and slaughter withhold, then time the dose.",
    "Discharge is often a producer conversation: milk withhold, slaughter withhold, when the animal can rejoin the group.",
], size=17, spacing=10)
notes(s, "One minute. Halsted travels to the barn. Then get back to Willie.")

# Willie: complete plan
s = new_content("Willie: complete perioperative plan", "ASA Status 3-E")
add_round(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(1.55), GOLD_LT)
add_text(s, Inches(0.75), Inches(1.3), Inches(11.8), Inches(1.25), "Willie, 6 y 11 mo MN Cavalier, 13.7 kg. Acute vestibular crisis. Severe AS otitis, TM visible/swollen. Circling left, nystagmus fast-left, right knuckling. Grade II murmur. CBC WNL. This is ASA III-E. Client-owned.", size=15, color=NAVY)
steps = [
    ("Pre-op", "ASA III-E. Neuro exam. Skip NSAID (DexSP already given). IVF, Cerenia, meclizine. Culture the ear. Radiographs ≠ MRI. Central until proven otherwise."),
    ("Prep", "Airway protected, monitors on, then alfaxalone to a depth that is safe to clip and flush. Periocular and canal mucosa: 10% PVP-I 1 to 20 to 1 to 50; eye 2 min scrub + 2 min soak. Pad him. He falls."),
    ("Intra", "Timeout. Deep clean + cytology. If you contaminate, say it and re-glove. Stay until the canal is clean."),
    ("Post", "Confine, no stairs. Watch neuro signs, vomiting, seizures. MRI next. TECA-LBO only after culture if medical therapy fails."),
]
for i, (t, d) in enumerate(steps):
    x = Inches(0.45) + Inches(i * 3.2)
    add_round(s, x, Inches(2.9), Inches(3.05), Inches(3.85), WHITE)
    add_rect(s, x, Inches(2.9), Inches(3.05), Inches(0.55), NAVY)
    add_text(s, x, Inches(2.9), Inches(3.05), Inches(0.55), t, size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.15), Inches(3.55), Inches(2.75), Inches(3.0), d, size=12, color=INK)
notes(s, "Walk Willie without questions until the end. Then one sentence on MoMo: the same hour of preoperative evaluation cancelled her exploratory. A healthy Lab OHE is ASA I: skip routine antibiotics. Willie is III-E. MoMo is IV-E: medical abdomen.")

# MoMo vs Willie close
s = new_content("Willie and MoMo", "Both received a preoperative evaluation. Only Willie was anesthetized.")
card(s, Inches(0.45), Inches(1.2), Inches(6.15), Inches(5.5), "Willie, ASA Status 3-E. Proceed with sedation.", "Cavalier, 13.7 kg. Acute vestibular + AS otitis + murmur. Compensated. Fill the anesthesia record. Alfaxalone, monitoring, ear clean, skip NSAID after DexSP. Own the next 24 hours. MRI / possible TECA-LBO later. Assign a new ASA status on the day of that surgery.", accent=GOLD)
card(s, Inches(6.75), Inches(1.2), Inches(6.15), Inches(5.5), "MoMo, ASA Status 4-E. Cancel the exploratory.", "DSH, 4.25 kg. Vomiting that looked like FB. Labs + POCUS + AUS: structural renal disease, creatinine 3.0 → 4.71 on fluids. Exploratory cancelled. NSAIDs contraindicated. Record the decision. Offer supportive care, referral, or euthanasia. That conversation is still surgery.", accent=RED)
notes(s, "This is the last content slide if time is gone. Healthy Lab OHE is only the ASA I contrast.")

# 44 Key points
s = new_content("Key points", "")
pearls = [
    "ASA is assigned after today’s PE and labs. Willie is III-E (sedate with a plan). MoMo is IV-E (image first, then cancel the exploratory).",
    "Imaging and serial creatinine can cancel a surgery. That is a successful preoperative evaluation.",
    "Elective clean OHE: skip routine postoperative antibiotics. Fill the anesthesia record and the 2-hour recovery sheet.",
    "Clip after induction, #40, not razor; spiral prep center → out; hair in the drape window fails the prep.",
    "Intact skin: PVP-I 5 minutes wet (then paint and dry), or aqueous CHG 3 minutes. Mucosa/eye: 10% PVP-I 1 to 20 to 1 to 50; eye 2 min + 2 min. Cornea and middle ear: dilute PVP-I.",
    "Pale + tachycardic after celiotomy: treat as hemorrhage, return to OR; the first 24 hours still count.",
]
for i, t in enumerate(pearls):
    y = Inches(1.15) + Inches(i * 0.9)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(0.8), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.7), Inches(0.8), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.7), Inches(0.8), str(i + 1), size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.4), y, Inches(11.1), Inches(0.8), t, size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Stop here if time is gone. They should defend Willie III-E and MoMo IV-E without looking.")

# 45 Summary
s = new_content("Summary", "")
add_round(s, Inches(0.5), Inches(1.25), Inches(12.3), Inches(5.4), WHITE)
add_text(s, Inches(0.85), Inches(1.6), Inches(11.6), Inches(4.8), "Preoperative evaluation is a decision to proceed, delay, stabilize, or not to operate.\n\nPatient and surgeon preparation prevents surgical site infection.\n\nPostoperative care includes pain, temperature, the incision, the record, and the client conversation.\n\nHalsted’s principles apply through the first 24 hours.", size=20, color=NAVY)
notes(s, "Close the loop to slide 1.")

# 46 References
s = new_content("References", "")
add_bullets(s, Inches(0.5), Inches(1.15), Inches(12.2), Inches(5.6), [
    "Fossum T.W. Small Animal Surgery. 5th ed. Elsevier; 2018. Preoperative evaluation, patient preparation, postoperative care.",
    "Johnston S.A., Tobias K.M. Veterinary Surgery: Small Animal. 2nd ed. Elsevier; 2017.",
    "Hendrickson D.A., Baird A.N. Turner and McIlwraith’s Techniques in Large Animal Surgery. 4th ed. Wiley-Blackwell; 2013.",
    "Roberts S.M., Severin G.A., Lavach J.D. Am J Vet Res. 1986;47(6):1207–1210. Canine ocular 1:50 (0.2%): 2-minute scrub + 2-minute soak. 1:2 (5%) caused corneal edema.",
    "Betadine Surgical Scrub (povidone-iodine 7.5%), veterinary label: lather 5 minutes, rinse, paint 10% solution, dry.  ·  AAHA/AAFP Antimicrobial Stewardship 2022: cefazolin 22 mg/kg IV 30 minutes before incision; redose every 90 minutes.",
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
add_text(s, Inches(0.75), Inches(4.3), Inches(12), Inches(1.2), "If there are no questions: why was Willie ASA III-E and MoMo ASA IV-E,\nand how do you dilute 10% povidone-iodine for conjunctiva or prepuce?", size=18, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(6.3), Inches(12), Inches(0.4), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP  ·  Lewyt College of Veterinary Medicine  ·  Long Island University", size=14, color=GOLD)
notes(s, "Take questions. If none: Willie vs MoMo ASA, then iodine: 1 to 20 to 1 to 50, 5 minutes wet on intact skin, 2 minutes plus 2 minutes on the eye. Dismiss on time.")

# Stamp numbers
stamp_footers()

out = Path("/workspace/lectures/DVM-612_Week4_Preop_PatientPrep_Postop.pptx")
prs.save(str(out))
# Convenience copy at repo root for download
root_copy = Path("/workspace/DVM-612_Week4_Preop_PatientPrep_Postop.pptx")
root_copy.write_bytes(out.read_bytes())

# Instructor script from speaker notes so it cannot drift
script_lines = [
    "DVM 612 Week 4 instructor script",
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
