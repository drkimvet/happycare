#!/usr/bin/env python3
"""Build DVM 612 Week 15 lecture: drains and bandages.

Lewyt College of Veterinary Medicine (LIU)
Aligned to the public DVM 612 outline (Week 15) and course LO 5.
Required text: Fossum 2018 (named only). Week 9 owns wound-healing stages.
Merck Winkler Jul 2023 / Sept 2024 for bandage layers and drains.
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

NAVY = RGBColor(0x0B, 0x2C, 0x4A)
GOLD = RGBColor(0xC5, 0xA3, 0x5A)
GOLD_LT = RGBColor(0xF4, 0xEB, 0xD3)
RED = RGBColor(0x8B, 0x2E, 0x2E)
RED_LT = RGBColor(0xF8, 0xE8, 0xE8)
GREEN = RGBColor(0x2E, 0x6B, 0x4F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFFWHITE = RGBColor(0xF6, 0xF7, 0xF9)
INK = RGBColor(0x1C, 0x1C, 0x1C)
SLATE = RGBColor(0x3D, 0x4A, 0x57)

W, H = Inches(13.333), Inches(7.5)
FOOTER = "DVM 612  |  Dr. Yujin Kim, D.V.M., Ph.D., FFCP  |  Lewyt CVM"
EXPECTED_SLIDES = 36

PT_FOOTER = 12
PT_TITLE = 30
PT_BODY = 18
PT_CARD = 16
PT_CARD_TITLE = 18
PT_SMALL = 14
PT_REF = 13
MIN_PT = 12

OUT_DIR = Path(__file__).resolve().parent
PPTX = OUT_DIR / "DVM-612_Week15_Bandages_Drains.pptx"
ASSET_DIR = OUT_DIR / "assets" / "bandage"

prs = Presentation()
prs.slide_width = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]


def _solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_rect(slide, l, t, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    _solid(sh, color)
    return sh


def add_round(slide, l, t, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    _solid(sh, color)
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
        tf._txBody.bodyPr.set(
            "anchor",
            {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}.get(anchor, "t"),
        )
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


def add_bullets(slide, l, t, w, h, items, size=18, spacing=8):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(spacing)
        run = p.add_run()
        run.text = "▸  " + item
        run.font.size = Pt(size)
        run.font.color.rgb = INK
        run.font.name = "Calibri"
    return box


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def header_bar(slide):
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    add_rect(slide, 0, Inches(0.12), W, Inches(0.08), NAVY)


def card(slide, l, t, w, h, title, body, fill=WHITE, title_color=NAVY, accent=GOLD):
    add_round(slide, l, t, w, h, fill)
    add_rect(slide, l, t, Inches(0.10), h, accent)
    add_text(slide, l + Inches(0.28), t + Inches(0.12), w - Inches(0.4), Inches(0.36), title, size=PT_CARD_TITLE, bold=True, color=title_color)
    add_text(slide, l + Inches(0.28), t + Inches(0.50), w - Inches(0.4), h - Inches(0.62), body, size=PT_CARD, color=SLATE)


def pill(slide, l, t, w, h, text, fill=GOLD, text_color=NAVY):
    add_round(slide, l, t, w, h, fill)
    add_text(slide, l, t, w, h, text, size=PT_SMALL, bold=True, color=text_color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def new_content(title):
    s = prs.slides.add_slide(BLANK)
    add_rect(s, 0, 0, W, H, OFFWHITE)
    header_bar(s)
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


def add_pic(slide, path, l, t, w, h):
    return slide.shapes.add_picture(str(path), l, t, w, h)


def figure_panel(slide, l, t, w, h, image_name, caption="Original teaching figure"):
    path = ASSET_DIR / image_name
    if not path.exists():
        raise SystemExit(f"Missing figure: {path}")
    add_round(slide, l, t, w, h, WHITE)
    add_rect(slide, l, t, w, Inches(0.40), NAVY)
    add_text(slide, l, t, w, Inches(0.40), caption, size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box_w = w - Inches(0.28)
    box_h = h - Inches(0.64)
    pic_l = l + Inches(0.14)
    pic_t = t + Inches(0.50)
    add_pic(slide, path, pic_l, pic_t, box_w, box_h)


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
            add_text(
                slide,
                Inches(11.2),
                Inches(7.18),
                Inches(1.7),
                Inches(0.32),
                f"{i}  /  {total}",
                size=PT_FOOTER,
                color=GOLD,
                align=PP_ALIGN.RIGHT,
                anchor=MSO_ANCHOR.MIDDLE,
            )
            continue
        add_rect(slide, 0, Inches(7.18), W, Inches(0.32), NAVY)
        add_text(
            slide,
            Inches(0.35),
            Inches(7.18),
            Inches(10.8),
            Inches(0.32),
            FOOTER,
            size=PT_FOOTER,
            color=GOLD_LT,
            anchor=MSO_ANCHOR.MIDDLE,
        )
        add_text(
            slide,
            Inches(11.2),
            Inches(7.18),
            Inches(1.8),
            Inches(0.32),
            f"{i}  /  {total}",
            size=PT_FOOTER,
            color=WHITE,
            align=PP_ALIGN.RIGHT,
            anchor=MSO_ANCHOR.MIDDLE,
        )


# =============================================================================
# SLIDES
# =============================================================================

s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, 0, 0, Inches(0.22), H, GOLD)
add_text(s, Inches(0.75), Inches(0.95), Inches(12), Inches(0.40), "LONG ISLAND UNIVERSITY  ·  LEWYT COLLEGE OF VETERINARY MEDICINE", size=16, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(1.45), Inches(12), Inches(0.40), "DVM 612  ·  PRINCIPLES OF SURGERY  ·  WEEK 15", size=20, bold=True, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(2.05), Inches(12), Inches(1.6), "Drains and Bandages", size=40, bold=True, color=WHITE)
add_text(s, Inches(0.75), Inches(3.85), Inches(12), Inches(0.50), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP", size=24, bold=True, color=GOLD)
add_text(s, Inches(0.75), Inches(4.40), Inches(12), Inches(0.40), "Lecture  |  36 slides  |  50 minutes  |  OSCE skills tonight", size=18, color=GOLD_LT)
add_text(s, Inches(0.75), Inches(5.10), Inches(12), Inches(0.90), "Name the wound, the exudate, and the load. Then pick the contact layer, the wrap, or the drain.", size=20, color=WHITE)
add_text(s, Inches(0.75), Inches(6.10), Inches(12), Inches(0.60), "Required: Fossum 2018. Week 9 owns healing stages. This hour is the wrap and the drain.", size=16, color=GOLD)
notes(s, "Welcome. Public DVM 612 outline Week 15: drains and bandages, OSCE. Course LO 5. Do not dump a brand catalog. Do not invent a change-interval table. Vendor names stay in this script: conforming gauze, elastic wrap, nonadherent pad. Kling, Vetrap, Elastikon, Telfa stay off the student slide.")

s = new_content("Learning objectives")
add_bullets(s, Inches(0.55), Inches(1.20), Inches(12.2), Inches(4.3), [
    "Name why a bandage exists: pressure, protection, absorption, immobilization, or a vehicle for a dressing (course LO 5).",
    "Build three layers. Primary touches the wound. Secondary pads. Tertiary holds.",
    "Match the contact layer to exudate and granulation. Wet-to-dry is short-term debridement, not the default moist-wound plan.",
    "Apply distal to proximal, even tension, about 50 percent overlap, stirrups, tips of digits 3 and 4 visible.",
    "Name Robert Jones, modified Robert Jones, Spica, Velpeau, and Ehmer by job, not by brand.",
    "Place a drain to kill dead space. Never through the incision. Remove it when it is no longer useful.",
], size=18, spacing=8)
add_round(s, Inches(0.5), Inches(5.70), Inches(12.3), Inches(1.20), GOLD_LT)
add_text(s, Inches(0.75), Inches(5.85), Inches(11.9), Inches(0.95), "Public DVM 612 outline, Week 15. Tables are overviews. Confirm constructions in Fossum or the lab. Do not invent millimeters or a brand as the syllabus.", size=16, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Read the six. OSCE will ask layers, digits 3 and 4, and Penrose not through the incision.")

s = new_content("This hour")
rows = [
    ("0–8 min", "Why wrap", "Unbandaged costs. Three questions."),
    ("8–20 min", "Three layers", "Contact, padding, wrap. Dressing class."),
    ("20–32 min", "Apply and watch", "Stirrups. Distal to proximal. Trouble signs."),
    ("32–42 min", "Coaptation map", "RJ, modified RJ, Spica, Velpeau, Ehmer, cast."),
    ("42–50 min", "Drains and OSCE", "Penrose vs closed suction. Then quiz."),
]
add_rect(s, Inches(0.45), Inches(1.15), Inches(12.4), Inches(0.48), NAVY)
add_text(s, Inches(0.60), Inches(1.15), Inches(2.4), Inches(0.48), "Clock", size=16, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3.10), Inches(1.15), Inches(4.4), Inches(0.48), "Block", size=16, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(7.60), Inches(1.15), Inches(5.0), Inches(0.48), "Protect this", size=16, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, (clk, block, protect) in enumerate(rows):
    y = Inches(1.72) + Inches(i * 0.95)
    add_round(s, Inches(0.45), y, Inches(12.4), Inches(0.86), WHITE)
    add_text(s, Inches(0.60), y, Inches(2.4), Inches(0.86), clk, size=18, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(3.10), y, Inches(4.4), Inches(0.86), block, size=18, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(7.60), y, Inches(5.0), Inches(0.86), protect, size=16, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "If discussion runs, cut coaptation extras. Keep layers, digits 3 and 4, Penrose rule.")

s = new_content("What this hour is not")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(2.50), "Week 9", "Wound-healing stages live there. Today you only need: moist wound, granulation, then a nonadherent contact layer.", accent=GOLD)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(2.50), "Week 7 and 8", "Patterns and materials already happened. A drain tacking suture is not a new pattern hour.", accent=GOLD)
card(s, Inches(0.45), Inches(3.90), Inches(6.15), Inches(2.90), "A brand catalog", "Conforming gauze, elastic wrap, nonadherent pad. Confirm what LIU stocks. Do not invent a product as the syllabus.", accent=NAVY)
card(s, Inches(6.80), Inches(3.90), Inches(6.05), Inches(2.90), "The OSCE", "Hands tonight. This lecture names the job. The station proves you can wrap without cooking the toes.", accent=GREEN)
notes(s, "Vendor names stay in this script: Kling, Vetrap, Elastikon, Telfa. Jackson-Pratt is closed suction on the student slide.")

s = new_section("Part 1", "Why wrap", "An unbandaged wound is a choice, not a default.", "8 minutes")
notes(s, "Short section. Then why bandage.")

s = new_content("Why bandage")
card(s, Inches(0.45), Inches(1.20), Inches(4.05), Inches(5.60), "Protect", "Trauma. Desiccation. Contamination. Irritants. The drain exit. Merck: prevent further trauma and keep the wound from drying out.", accent=GOLD)
card(s, Inches(4.65), Inches(1.20), Inches(4.05), Inches(5.60), "Control", "Compression for edema and dead space. Limit hemorrhage. Absorb exudate. Carry a dressing. Mechanical debridement when that is the job.", accent=NAVY)
card(s, Inches(8.85), Inches(1.20), Inches(4.00), Inches(5.60), "Hold still", "Immobilize a joint or a fracture below the elbow or stifle. Restrict motion. Temporary support is not internal fixation.", accent=GREEN)
notes(s, "Merck Winkler bandage goals Jul 2023 / Sept 2024. One theory: the wrap matches the job. Not every wound wants a Robert Jones.")

s = new_content("Three questions before you wrap")
qs = [
    ("1. What is on this wound?", "Necrotic, exudative, granulating, or closed. The contact layer follows the bed, not the closet."),
    ("2. What load must the wrap carry?", "A laceration needs padding. A radius fracture below the elbow needs rigid support. Do not ask a modified Robert Jones to be a cast."),
    ("3. Can I still see the toes?", "If digits 3 and 4 disappear, you cannot catch ischemia. If the wrap is wet, the skin under it is wet."),
]
for i, (t, d) in enumerate(qs):
    y = Inches(1.20) + Inches(i * 1.75)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.60), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.12), Inches(1.60), GOLD)
    add_text(s, Inches(0.85), y + Inches(0.18), Inches(11.7), Inches(0.48), t, size=22, bold=True, color=NAVY)
    add_text(s, Inches(0.85), y + Inches(0.72), Inches(11.7), Inches(0.70), d, size=18, color=SLATE)
notes(s, "Board the three. They come back on every wrap.")

s = new_section("Part 2", "Three layers", "Contact, padding, wrap. In that order.", "12 minutes")
notes(s, "Layer block.")

s = new_content("The stack")
figure_panel(s, Inches(0.40), Inches(1.15), Inches(6.40), Inches(5.65), "bandage_three_layers.png")
card(s, Inches(7.00), Inches(1.15), Inches(5.85), Inches(5.65), "What to say", "Merck: sufficiently padded, applied evenly and snugly, three layers.\n\nPrimary touches the wound.\nSecondary never does.\nTertiary holds the other two and keeps the world out.\n\nUneven tension is a pressure sore waiting.\nNot enough padding is a pressure sore waiting.\n\nConfirm constructions in Fossum. Do not invent a brand.", accent=GOLD)
notes(s, "Original figure. Not a Fossum plate. Not a vendor photo.")

s = new_content("Primary contact layer")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(5.4), [
    "The only layer allowed to touch the wound.",
    "Jobs: debride, deliver a dressing, absorb, or protect granulation (Merck).",
    "Adherent wide-mesh gauze pulls debris. It is nonselective. Healthy tissue comes off too. Painful. Short-term.",
    "Nonadherent fine mesh or foam protects granulation and suture lines. Semiocclusive lets the wound breathe. Occlusive holds moisture in.",
    "Choice follows exudate, necrosis, and whether granulation is already there. Not a favorite pad from the drawer.",
], size=20, spacing=10)
notes(s, "Do not put Telfa on the student slide. Nonadherent pad is the class.")

s = new_content("Dressing class follows the bed")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(2.70), "Adherent / wet-to-dry", "Necrotic or dirty bed that still needs mechanical debridement. Saline-moist wide mesh, then dry gauze. Remove when the contact layer has dried. Painful. Nonselective.", accent=GOLD)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(2.70), "Nonadherent", "Clean wound, suture line, or granulation. Protects the bed. Semiocclusive or occlusive. This is the default once the bed is healthy.", accent=GREEN)
card(s, Inches(0.45), Inches(4.10), Inches(6.15), Inches(2.70), "Absorbent foam / alginate", "High exudate. Foam can take volume. Alginate gels on a wet bed. Not for a dry wound or exposed bone or tendon (Merck).", accent=NAVY)
card(s, Inches(6.80), Inches(4.10), Inches(6.05), Inches(2.70), "Hydrogel / hydrocolloid", "Donate moisture to a dry or necrotic bed. Can macerate healthy skin. Hydrocolloid often fails to stick on veterinary skin (Merck).", accent=RED)
notes(s, "Merck dressing table named only. Do not harvest a two-week antimicrobial-dressing clock as lobby law.")

s = new_content("Wet-to-dry is not the default")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(3.6), [
    "One theory. No table fight. Wet-to-dry is a debridement tool, not a moist-wound lifestyle.",
    "Use it while the bed is necrotic or heavily contaminated. Switch to nonadherent when granulation appears.",
    "Wet-to-wet that never dries macerates the bed (Merck). Do not leave a sopping contact layer as a plan.",
    "A too-tight wrap on a foam dressing can cancel the foam. Padding still has to be even.",
], size=20, spacing=10)
add_round(s, Inches(0.5), Inches(5.15), Inches(12.3), Inches(1.75), RED_LT)
add_text(s, Inches(0.75), Inches(5.35), Inches(11.9), Inches(1.40), "Do not send a granulating wound home on wet-to-dry because that is what you started with. The bed changed. The contact layer changes with it.", size=18, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "This kills the 2022 slide fight between adherent-first and moist healing. Both are true at different times.")

s = new_content("Secondary and tertiary")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(5.60), "Secondary", "Cast padding or roll cotton.\n\nAbsorbs what the primary lets through.\nPads bony points.\nSupports or immobilizes.\nDecreases dead space.\n\nIt must cover the primary completely. If cotton sits on the wound, you skipped a layer.", accent=GOLD)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(5.60), "Tertiary", "Conforming wrap first, then elastic wrap.\n\nHolds the stack. Protects from dirt and the patient. Adds some immobilization.\n\nSame direction as the other layers. Distal to proximal. About 50 percent overlap. Even tension.\n\nToo tight is ischemia. Too loose falls off. Both fail.", accent=NAVY)
notes(s, "Kling / Vetrap / Elastikon stay in this script. Conforming then elastic on the slide.")

s = new_section("Part 3", "Apply it, then watch it", "Even tension. Visible toes. Dry wrap.", "12 minutes")
notes(s, "Application block.")

s = new_content("Application principles")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(5.4), [
    "Hair and paw dry. Moisture under a wrap is moisture-associated skin damage (Merck).",
    "Stirrups on healthy skin. Distal to proximal. Unroll toward the medial aspect. All layers the same way.",
    "Even tension. About 50 percent overlap. No wrinkles. Padding over bony points.",
    "Leave the tips of digits 3 and 4. Compare them to the other paw.",
    "For fracture coaptation, immobilize the joint above and the joint below. Casts and splints are typically for injuries below the stifle or elbow.",
    "A wrap that is too loose falls off. A wrap that is too tight cooks the limb. Merck: pressure necrosis can cost a limb.",
], size=18, spacing=8)
notes(s, "50 percent overlap is a principle, not a millimeter table. Do not invent mm.")

s = new_content("Stirrups and digits 3 and 4")
figure_panel(s, Inches(0.40), Inches(1.15), Inches(6.10), Inches(5.65), "bandage_stirrups.png")
figure_panel(s, Inches(6.70), Inches(1.15), Inches(6.15), Inches(5.65), "bandage_digits34.png", caption="Leave digits 3 and 4")
notes(s, "OSCE. If they cannot see 3 and 4, they fail the wrap. Rotate stirrups 180 degrees onto the wrap before the outer elastic.")

s = new_content("Sequence")
steps = [
    ("1", "Dry the paw. Place stirrups. Cotton between digits if the foot is in the wrap."),
    ("2", "Primary on the wound. Then secondary, distal to proximal, even tension, about 50 percent overlap."),
    ("3", "Conforming wrap of the tertiary layer the same way."),
    ("4", "Peel the stirrups off the depressor. Rotate 180 degrees. Stick them to the wrap."),
    ("5", "Elastic wrap last. Tips of 3 and 4 still out. Thump a Robert Jones: it should sound like a ripe watermelon, not a rock."),
]
for i, (n, t) in enumerate(steps):
    y = Inches(1.18) + Inches(i * 1.10)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.00), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.85), Inches(1.00), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.85), Inches(1.00), n, size=22, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.55), y, Inches(10.9), Inches(1.00), t, size=18, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Do not invent a throw of Elastikon as a law. Confirm in lab.")

s = new_content("Tie-over bandage")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(5.60), "When", "A wound you cannot circumferential-wrap: high motion, high tension, inguinal, peri-anal, proximal limb.\n\nLoops of suture away from the wound edge hold a primary dressing in place.\n\nStays put when the animal walks.", accent=GOLD)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(5.60), "Costs", "Skin necrosis at the loops. Focal infection at the suture holes. Loop failure.\n\nStill a bandage. Strike-through still means change it.\n\nConfirm loop placement in Fossum. Do not invent bite distances.", accent=RED)
notes(s, "Merck shows a suction drain under a tie-over. Same rule: cover the exit.")

s = new_content("Trouble signs")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(5.60), "Look now", "Foul odor. Swollen, cyanotic, or cold digits. Strike-through. The patient eating the wrap. Pain. Fever. Anorexia.\n\nCompare the toes to the other limb twice a day.\n\nIf the wrap slipped, it is rubbing. If it is wet, take it off.", accent=RED)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(5.60), "Tell the owner", "Keep it clean and dry. Bag for a wet yard. Bag off indoors.\n\nWatch toes, odor, licking, slip, and sores at the top.\n\nWound wraps come off when they are wet or dirty, not when the calendar is pretty. Young, growing animals need more frequent checks. Confirm the interval in Fossum or the lab.", accent=GOLD)
notes(s, "Do not print SID-BID or 2-3 weeks as lobby law. Qualitative: wound wraps often, slings daily, casts more often in growing animals. Confirm Fossum.")

s = new_content("OSCE skills tonight")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(5.4), [
    "Name the three layers out loud before you touch the roll.",
    "Stirrups on. Distal to proximal. About 50 percent overlap. Even tension. No wrinkles.",
    "Tips of digits 3 and 4 visible. If you cannot see them, start over.",
    "A Penrose exits a dependent stab, never the incision. Cover the exit.",
    "If the station is a sling, name Velpeau versus Ehmer before you wrap.",
], size=20, spacing=12)
notes(s, "Course LO 5. Hands after this hour. Do not invent a station script that is not the coordinator's.")

s = new_section("Part 4", "Name the wrap by its job", "RJ is not Velpeau. Ehmer is not a hind-limb hug.", "10 minutes")
notes(s, "Coaptation map.")

s = new_content("Coaptation map")
headers = ("Name", "Job", "Not this")
rows = [
    ("Modified Robert Jones", "Everyday limb wrap. Minimal support.", "Not a fracture fix."),
    ("Reinforced modified RJ", "Splint or thermoplastic in the stack.", "Still not a plate."),
    ("Robert Jones", "Bulky emergency support below elbow or stifle.", "Not a body-wall wrap."),
    ("Spica", "Temporary humerus or femur. Over the shoulder or hip.", "Joints above and below."),
    ("Velpeau", "Forelimb to the chest. Scapula or shoulder.", "Not a hind-limb sling."),
    ("Ehmer", "Hind limb. Hock out, stifle in.", "Not a generic pelvic wrap."),
    ("Cast", "Stable distal fracture in a young animal, or adjunct.", "Not over a wound or a swollen limb."),
]
add_rect(s, Inches(0.32), Inches(1.10), Inches(12.70), Inches(0.42), NAVY)
add_text(s, Inches(0.40), Inches(1.10), Inches(3.40), Inches(0.42), headers[0], size=14, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3.90), Inches(1.10), Inches(4.70), Inches(0.42), headers[1], size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.70), Inches(1.10), Inches(4.10), Inches(0.42), headers[2], size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, (a, b, c) in enumerate(rows):
    y = Inches(1.56) + Inches(i * 0.70)
    add_round(s, Inches(0.32), y, Inches(12.70), Inches(0.64), WHITE)
    add_text(s, Inches(0.40), y, Inches(3.40), Inches(0.64), a, size=14, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(3.90), y, Inches(4.70), Inches(0.64), b, size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(8.70), y, Inches(4.10), Inches(0.64), c, size=14, color=SLATE, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Map, not a recipe. Confirm in Fossum. No size table.")

s = new_content("Robert Jones family")
card(s, Inches(0.45), Inches(1.20), Inches(4.05), Inches(5.60), "Modified RJ", "Soft-tissue wounds. Minimal compression. Minimal immobilization.\n\nPadding, conforming wrap, elastic wrap.\n\nThis is the everyday limb bandage after a laceration is closed.", accent=GOLD)
card(s, Inches(4.65), Inches(1.20), Inches(4.05), Inches(5.60), "Reinforced", "Same stack. Splint rod, fiberglass, or thermoplastic between conforming wrap and elastic wrap.\n\nExtra support for selected orthopedic injuries. Still temporary.", accent=NAVY)
card(s, Inches(8.85), Inches(1.20), Inches(4.00), Inches(5.60), "Robert Jones", "Bulky cotton. Emergency, temporary. Fractures below elbow or stifle.\n\nStovepipe. Even compression. Watermelon thump.\n\nDigits 3 and 4 out.", accent=GREEN)
notes(s, "One theory: bulk is not better for every wound. Modified RJ for a laceration. RJ for a distal fracture until surgery.")

s = new_content("Spica, Velpeau, Ehmer")
figure_panel(s, Inches(0.40), Inches(1.15), Inches(4.20), Inches(5.65), "bandage_velpeau.png", caption="Velpeau")
figure_panel(s, Inches(4.75), Inches(1.15), Inches(4.20), Inches(5.65), "bandage_ehmer.png", caption="Ehmer")
card(s, Inches(9.10), Inches(1.15), Inches(3.75), Inches(5.65), "Spica", "Humerus or femur. The wrap goes over the trunk so the joint above is in the wrap.\n\nTemporary. Joints above and below still apply.\n\nConfirm construction in Fossum.", accent=GOLD)
notes(s, "Ehmer: abduction and internal rotation after craniodorsal coxofemoral luxation. Velpeau: non-weight-bearing thoracic limb. Do not mix them.")

s = new_content("Casts")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(5.4), [
    "Selected, minimally displaced, stable fractures of radius, ulna, tibia, or fibula. Young animals heal fast. Incomplete fractures. Adjunct after internal fixation.",
    "Do not put a cast on a skin wound or a swollen limb. Swelling goes down. The cast does not.",
    "Stockinette, padding, casting tape. Outer wrap. Digits 3 and 4 still visible if the limb allows.",
    "Growing animals need more frequent checks than an adult. Confirm the interval in Fossum or the lab. Do not invent a two-week law.",
    "A cast is rigid support. It is not a reason to skip the joint-above and joint-below rule.",
], size=20, spacing=10)
notes(s, "No vendor casting-tape table.")

s = new_section("Part 5", "The drain is not the incision", "Kill dead space. Then take it out.", "8 minutes")
notes(s, "Drain block. OSCE.")

s = new_content("Why a drain")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(5.4), [
    "Remove fluid or gas. Stop it from coming back. Kill dead space. Sample the pocket.",
    "Relieves pressure that hurts perfusion and hurts the patient.",
    "Every drain is a foreign body. It incites inflammation. It can help bacteria in or help bacteria out.",
    "Indications: dead space, contamination, infection, fluid or gas that will reaccumulate.",
    "A drain is not a substitute for debridement, lavage, or a tight dead-space closure you could have done.",
], size=20, spacing=10)
notes(s, "Merck Winkler drains Jul 2023 / Sept 2024. Today's Veterinary Practice: do not exit through the incision.")

s = new_content("Passive versus active")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(5.60), "Passive", "Gravity, overflow, capillary action. Fluid runs along the outside of a Penrose.\n\nMust exit dependent. Open system. Higher ascending-infection risk.\n\nLatex, silicone, polyethylene. Soft latex conforms. Fenestrating a Penrose cuts surface area and cuts function.\n\nCannot connect to suction. Cannot work against gravity.", accent=GOLD)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(5.60), "Active", "Closed suction. Negative pressure. Exit can be anywhere the seal holds.\n\nYou can measure the fluid. Lower infection risk than an open Penrose (Merck).\n\nAir leak kills the vacuum. Obstruction is the usual failure.\n\nFenestrated tubing belongs in the pocket, not in the tunnel.", accent=NAVY)
notes(s, "Jackson-Pratt stays in this script. Closed suction on the slide.")

s = new_content("Penrose rules")
figure_panel(s, Inches(0.40), Inches(1.15), Inches(6.40), Inches(5.65), "bandage_penrose.png")
card(s, Inches(7.00), Inches(1.15), Inches(5.85), Inches(5.65), "What to say", "Single dependent exit. Not two holes if you can help it.\n\nNever through the incision. Never lying under the suture line.\n\nPass from inside out through a stab. Tack proximally. Bandage the exit.\n\nDo not fenestrate. Drainage is surface area.\n\nCover. Keep clean. Confirm construction in Fossum.", accent=GOLD)
notes(s, "OSCE fail: drain out the incision. Percutaneous tack, not a buried tack you will lose.")

s = new_content("Closed suction")
figure_panel(s, Inches(0.40), Inches(1.15), Inches(6.40), Inches(5.65), "bandage_closed_suction.png")
card(s, Inches(7.00), Inches(1.15), Inches(5.85), Inches(5.65), "What to say", "Fenestrated portion in the deepest pocket.\n\nExit away from the incision. Close the wound completely. Air leak kills suction.\n\nPurse-string plus finger-trap at the skin. Then bandage.\n\nEmpty and measure. Cytology if the pocket was dirty.\n\nConfirm in Fossum. Do not invent a vacuum number.", accent=NAVY)
notes(s, "Purse-string is Week 7 language: circumferential constriction. Finger-trap holds the tube.")

s = new_content("Take the drain out")
add_bullets(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(5.4), [
    "Remove it as soon as it is not helping. Infection risk rises the longer it stays.",
    "Quantity down. Character serous or serosanguineous. It rarely goes to zero: the drain itself is a foreign body.",
    "If the wound was infected, sample for cytology before you pull.",
    "Active: cut purse-string and finger-trap, then slow withdrawal. Passive: cut the tack, then slow withdrawal. Count the piece. The whole drain must come out.",
    "Printed day ranges stay in Fossum. Do not invent a 3-to-7-day law on the board.",
], size=20, spacing=10)
notes(s, "Merck: leave until quantity decreases and it is no longer purulent. Cytology allowed.")

s = new_content("Drain complications")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(5.60), "Infection and failure", "Ascending infection, especially an open Penrose. Premature removal. Slippage back into the pocket. Drain broken off in the wound.\n\nA suture through the drain will snap it on the way out. Count the piece.", accent=RED)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(5.60), "Do not", "Do not exit through the incision. Do not leave an uncovered exit. Do not fenestrate a Penrose. Do not keep a dead drain because the calendar is not done.\n\nAir leak kills closed suction. Obstruction is the usual failure. Check the tube before you blame the pocket.", accent=NAVY)
notes(s, "Then quiz.")

s = new_content("Quiz. Write the wrap or the drain")
card(s, Inches(0.45), Inches(1.20), Inches(6.15), Inches(2.70), "Case A", "Closed laceration on a canine antebrachium. Toes will swell. Which wrap, and which two toes stay visible?", accent=GOLD)
card(s, Inches(6.80), Inches(1.20), Inches(6.05), Inches(2.70), "Case B", "Necrotic open wound yesterday. Today you see granulation. What happens to the contact layer?", accent=NAVY)
card(s, Inches(0.45), Inches(4.10), Inches(6.15), Inches(2.70), "Case C", "Craniodorsal coxofemoral luxation just reduced. Name the sling and the two limb positions.", accent=GREEN)
card(s, Inches(6.80), Inches(4.10), Inches(6.05), Inches(2.70), "Case D", "Dead space after a large excision. Student wants the Penrose out the incision because it is convenient. What is still true?", accent=RED)
notes(s, "Do not advance until they write. OSCE language.")

s = new_content("Quiz key")
keys = [
    "A. Modified Robert Jones. Tips of digits 3 and 4. Not a Robert Jones unless you need bulky distal-fracture support.",
    "B. Stop wet-to-dry. Switch to nonadherent. The bed changed. The contact layer changes with it.",
    "C. Ehmer. Hock out (abduction). Stifle in (internal rotation). Velpeau is the forelimb.",
    "D. Never through the incision. Single dependent exit. Bandage the exit. Do not fenestrate a Penrose.",
]
for i, t in enumerate(keys):
    y = Inches(1.20) + Inches(i * 1.35)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(1.20), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.85), Inches(1.20), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.85), Inches(1.20), str(i + 1), size=22, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.55), y, Inches(10.9), Inches(1.20), t, size=18, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Read the keys. Then OSCE list.")

s = new_content("Key points")
pearls = [
    "One theory: match the contact layer, the wrap, or the drain to the bed, the load, and the dead space.",
    "Three layers. Primary touches the wound. Secondary pads. Tertiary holds.",
    "Wet-to-dry is short-term debridement. Granulation gets a nonadherent layer.",
    "Distal to proximal. Even tension. About 50 percent overlap. Digits 3 and 4 visible.",
    "Name the wrap by its job. RJ is not Velpeau. Ehmer is not a hug.",
    "Drains never exit the incision. Remove them when they stop helping.",
]
for i, t in enumerate(pearls):
    y = Inches(1.15) + Inches(i * 0.92)
    add_round(s, Inches(0.5), y, Inches(12.3), Inches(0.84), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.85), Inches(0.84), GOLD)
    add_text(s, Inches(0.5), y, Inches(0.85), Inches(0.84), str(i + 1), size=20, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.55), y, Inches(10.9), Inches(0.84), t, size=18, color=INK, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "Six lines. Then questions.")

s = prs.slides.add_slide(BLANK)
add_rect(s, 0, 0, W, H, NAVY)
add_rect(s, 0, 0, W, Inches(0.16), GOLD)
add_rect(s, 0, 0, Inches(0.22), H, GOLD)
add_text(s, Inches(0.55), Inches(0.26), Inches(12.2), Inches(0.28), "DVM 612  ·  PRINCIPLES OF SURGERY  ·  WEEK 15", size=14, bold=True, color=GOLD)
add_text(s, Inches(0.55), Inches(0.52), Inches(12.2), Inches(0.48), "Questions", size=28, bold=True, color=WHITE)
add_text(s, Inches(0.55), Inches(1.02), Inches(12.2), Inches(0.70), "Which layer touches the wound? Which two toes stay out? Where does a Penrose exit?", size=16, color=GOLD_LT)
add_text(s, Inches(0.55), Inches(1.78), Inches(12.2), Inches(0.32), "References  (course text and public pages used in this hour)", size=14, bold=True, color=GOLD)
left_refs = (
    "1. Fossum TW. Small Animal Surgery. 5th ed. Elsevier; 2018. Named. No page dump. No invented size table.\n\n"
    "2. Long Island University CVM. DVM 612 Principles of Surgery course outline (public). Week 15: drains and bandages, OSCE. Course LO 5.\n\n"
    "3. Winkler KP. Wound bandages and dressings for small animals. Merck Veterinary Manual. Full review Jul 2023; last updated Sept 2024.\n\n"
    "4. Winkler KP. Drains in wound management of small animals. Merck Veterinary Manual. Full review Jul 2023; last updated Sept 2024."
)
right_refs = (
    "5. Today's Veterinary Practice. Surgical drains: placement, management, and removal. Public teaching page. Exit away from the incision.\n\n"
    "6. Week 9 owns healing stages. Week 7 owns purse-string and finger-trap names.\n\n"
    "7. Printed change intervals and brand catalogs stay on those pages. Confirm in lab.\n\n"
    "8. Original teaching figures in lectures/assets/bandage/. Not Fossum plates. Not vendor photos."
)
add_text(s, Inches(0.55), Inches(2.16), Inches(6.05), Inches(4.40), left_refs, size=PT_REF, color=WHITE)
add_text(s, Inches(6.75), Inches(2.16), Inches(6.05), Inches(4.40), right_refs, size=PT_REF, color=WHITE)
add_text(s, Inches(0.55), Inches(6.72), Inches(12.2), Inches(0.32), "Dr. Yujin Kim, D.V.M., Ph.D., FFCP  ·  Lewyt CVM  ·  Long Island University", size=14, color=GOLD)
notes(s, "Take questions. If none: three questions are bed, load, toes. Penrose never through the incision. Dismiss on time.")

if len(prs.slides) != EXPECTED_SLIDES:
    raise SystemExit(f"Slide count {len(prs.slides)} != {EXPECTED_SLIDES}")

stamp_footers()
prs.save(str(PPTX))

script_lines = [
    "DVM 612 Week 15 instructor script",
    "Instructor: Dr. Yujin Kim, D.V.M., Ph.D., FFCP",
    "",
    "36 slides. 50 minutes. Week 15 of the public DVM 612 outline: drains and bandages, OSCE.",
    "Do not alter the Week 4 or Week 7 decks. Do not invent a brand catalog or a change-interval table.",
    "Vendor names stay in this script: Kling, Vetrap, Elastikon, Telfa, Jackson-Pratt.",
    "Owner names stay off slides. MoMo and Willie stay off this hour.",
    "",
    "FIGURES: original teaching stills in lectures/assets/bandage/. Not Fossum plates. Not vendor photos.",
    "",
]
for i, slide in enumerate(prs.slides, 1):
    title = ""
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text.strip().split("\n")[0].strip()
        if not t or t.startswith("DVM 612  |"):
            continue
        if "/" in t and t.replace(" ", "").replace("/", "").isdigit():
            continue
        if 4 <= len(t) <= 90:
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

script_path = OUT_DIR / "DVM-612_Week15_Instructor_Script.txt"
script_path.write_text("\n".join(script_lines), encoding="utf-8")
print(f"Saved {PPTX}")
print(f"Script {script_path}")
print(f"Slides {len(prs.slides)}")
