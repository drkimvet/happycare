#!/usr/bin/env python3
"""Original DVM 612 teaching charts (anesthesia record, recovery sheet). Not a hospital form."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("/workspace/lectures/assets")
OUT.mkdir(parents=True, exist_ok=True)

NAVY = (11, 44, 74)
GOLD = (197, 163, 90)
TEAL = (27, 107, 122)
RED = (139, 46, 46)
INK = (28, 28, 28)
MUTED = (91, 100, 110)
WHITE = (255, 255, 255)
OFF = (246, 247, 249)
LINE = (210, 214, 220)
GREEN = (46, 107, 79)


def font(size, bold=False):
    path = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf" if bold else "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def box(d, xy, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=8, fill=fill, outline=outline, width=width)


def cell(d, x0, y0, x1, y1, text="", *, fill=WHITE, fg=INK, size=13, bold=False, align="left"):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=LINE, width=1)
    if not text:
        return
    f = font(size, bold)
    pad = 6
    if align == "center":
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), text, font=f, fill=fg, anchor="mm")
    else:
        d.text((x0 + pad, (y0 + y1) / 2), text, font=f, fill=fg, anchor="lm")


def draw_header(d, w, title, subtitle):
    d.rectangle([0, 0, w, 78], fill=NAVY)
    d.rectangle([0, 78, w, 86], fill=GOLD)
    d.text((28, 24), title, font=font(28, True), fill=WHITE, anchor="lt")
    d.text((28, 56), subtitle, font=font(14), fill=GOLD, anchor="lt")
    d.text((w - 28, 40), "Teaching record  ·  not a hospital original", font=font(13), fill=GOLD, anchor="rm")


def checkbox_list(d, x0, y0, x1, items, *, checked=False, box_color=GREEN, text_size=20, row_h=86):
    f = font(text_size)
    for i, t in enumerate(items):
        yy = y0 + i * row_h
        d.rectangle([x0, yy, x1, yy + row_h - 8], fill=WHITE, outline=LINE, width=1)
        bx, by = x0 + 16, yy + (row_h - 8) / 2 - 12
        d.rectangle([bx, by, bx + 24, by + 24], outline=box_color, width=3)
        if checked:
            d.line([bx + 4, by + 13, bx + 10, by + 19], fill=box_color, width=3)
            d.line([bx + 10, by + 19, bx + 20, by + 5], fill=box_color, width=3)
        lines = wrap_text(t, f, x1 - x0 - 70)
        ty = yy + (row_h - 8) / 2 - (len(lines[:2]) - 1) * 12
        for line in lines[:2]:
            d.text((x0 + 54, ty), line, font=f, fill=INK, anchor="lm")
            ty += 24


def anesthesia_record(filled="blank"):
    """Preop + recovery teaching record. Intra-op grid is not the point of this hour."""
    W, H = 2400, 1350
    im = Image.new("RGB", (W, H), OFF)
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 88, W, 96], fill=GOLD)
    d.text((28, 22), "Perioperative record", font=font(36, True), fill=WHITE, anchor="lt")
    d.text((28, 62), "DVM 612  ·  Preoperative evaluation and recovery  ·  teaching form, not a hospital original", font=font(18), fill=GOLD, anchor="lt")
    d.text((W - 28, 44), "Complete this page before the first drug", font=font(18), fill=GOLD, anchor="rm")

    y = 112
    labels = [
        (28, 360, "Patient"),
        (360, 860, "Species / breed"),
        (860, 1180, "Sex / age"),
        (1180, 1480, "Weight"),
        (1480, 1760, "ASA"),
        (1760, 2372, "What you planned today"),
    ]
    for x0, x1, lab in labels:
        cell(d, x0, y, x1, y + 32, lab, fill=NAVY, fg=WHITE, size=16, bold=True, align="center")
    values = {
        "blank": ["", "", "", "", "", ""],
        "willie": ["Willie", "Canine  ·  Cavalier", "MN  ·  6 y 11 mo", "13.7 kg  BCS 6/9", "3-E", "Sedated ear clean. Not a celiotomy."],
        "momo": ["MoMo", "Feline  ·  DSH", "SF  ·  6 yr", "4.25 kg  BCS 5/9", "4-E", "Exploratory considered. Then cancelled."],
    }[filled]
    for (x0, x1, lab), val in zip(labels, values):
        asa = lab == "ASA"
        fill = GOLD if (asa and val) else WHITE
        fg = NAVY if (asa and val) else INK
        cell(d, x0, y + 32, x1, y + 100, val, fill=fill, fg=fg, size=28 if asa else 20, bold=True, align="center")

    y = 228
    d.rectangle([28, y, 2372, y + 44], fill=TEAL)
    d.text((40, y + 22), "PREOPERATIVE EVALUATION   ·   complete before any drug", font=font(22, True), fill=WHITE, anchor="lm")

    y = 280
    preop_h = [
        (28, 280, "T °F"),
        (280, 520, "HR"),
        (520, 760, "RR"),
        (760, 1100, "mm / CRT"),
        (1100, 1480, "Mentation"),
        (1480, 2372, "Heart / lungs"),
    ]
    preop_v = {
        "blank": ["", "", "", "", "", ""],
        "willie": ["100.8", "132", "52", "pink / 2 s", "quiet, dull", "II/VI left systolic; lungs clear"],
        "momo": ["98.0", "200", "30", "pink, tacky / <2 s", "QAR", "NSR; no murmur; eupneic"],
    }[filled]
    for (x0, x1, lab), val in zip(preop_h, preop_v):
        cell(d, x0, y, x1, y + 28, lab, fill=(228, 236, 238), fg=TEAL, size=16, bold=True, align="center")
        cell(d, x0, y + 28, x1, y + 88, val, size=22, bold=True, align="center")

    y = 380
    d.rectangle([28, y, 2372, y + 88], fill=WHITE, outline=LINE, width=1)
    d.rectangle([28, y, 320, y + 88], fill=GOLD)
    d.text((174, y + 44), "What changes\nthe plan", font=font(18, True), fill=NAVY, anchor="mm")
    plan = {
        "blank": "",
        "willie": "Acute vestibular disease + severe AS otitis + murmur. Still pink, walking, kidneys normal. DexSP 0.68 mL SQ already given: skip NSAID. Alfaxalone only after this header is complete.",
        "momo": "Vomiting that looked like a foreign body. PE did not prove GI obstruction. Creatinine 3.0, then 4.71 on fluids. Right kidney fluid-filled and non-functional. NSAIDs contraindicated. Do not clip.",
    }[filled]
    fplan = font(20)
    lines = wrap_text(plan, fplan, 2000)
    ty = y + 18
    for line in lines[:3]:
        d.text((340, ty), line, font=fplan, fill=INK, anchor="lt")
        ty += 24

    mid = 1188
    y = 484
    d.rectangle([28, y, mid - 12, y + 44], fill=NAVY)
    d.text((40, y + 22), "PRE-OP BOXES   ·   before the first drug", font=font(20, True), fill=GOLD, anchor="lm")
    d.rectangle([mid + 12, y, 2372, y + 44], fill=GREEN)
    d.text((mid + 24, y + 22), "RECOVERY / NEXT 24 HOURS   ·   the operation is not over", font=font(20, True), fill=WHITE, anchor="lm")

    preop_boxes = {
        "blank": [
            "Identity, consent, DNR",
            "Today’s PE and ASA written",
            "Last meal recorded",
            "IV catheter patent",
            "Monitoring on before drugs",
            "Pain plan, including skip-NSAID if steroids given",
            "Who calls the client, and when",
        ],
        "willie": [
            "ASA Status 3-E written before alfaxalone",
            "Today’s PE: vestibular + AS otitis + murmur",
            "Skip NSAID: DexSP already given",
            "IV in. Monitoring on. Then sedate.",
            "Ear/eye: dilute PVP-I, not 7.5% scrub",
            "Aminoglycoside risk if the middle ear is involved",
            "MRI later. New ASA on the day of TECA-LBO",
        ],
        "momo": [
            "ASA Status 4-E after labs and imaging",
            "POCUS / AUS before any clippers",
            "Serial creatinine 3.0 then 4.71. Act on it.",
            "No clippers. No incision. No exploratory.",
            "NSAIDs contraindicated (azotemic cat)",
            "Consent includes medical care and euthanasia",
            "Write SURGERY CANCELLED on this record",
        ],
    }[filled]
    rec_items = {
        "blank": [
            "Extubate when swallow returns",
            "mm / CRT / pulse every 15 minutes",
            "Rewarm. Check skin so you do not burn",
            "Pain score and the analgesic you planned",
            "Incision or procedure-site check",
            "E-collar on before they can lick",
            "Pale + tachycardic after celiotomy: return to OR",
        ],
        "willie": [
            "Recover padded. No stairs tonight.",
            "Watch nystagmus, circling, vomiting, seizures",
            "Skip NSAID in recovery (DexSP already given)",
            "Meclizine 25 mg PO BID × 5 d",
            "Cerenia 60 mg PO SID × 4 d",
            "Confine. Call the owner with neuro status",
            "MRI recommended. TECA-LBO only if medical fails",
        ],
        "momo": [
            "This is not a recovery from surgery",
            "IVF, antiemetics, Unasyn. Recheck kidneys.",
            "Rising creatinine cancelled the cut",
            "Right kidney non-functional on AUS",
            "Offer supportive care, referral, or euthanasia",
            "That conversation is still surgery",
            "Owner elected humane euthanasia",
        ],
    }[filled]
    checkbox_list(d, 28, 540, mid - 12, preop_boxes, checked=(filled != "blank"), box_color=TEAL, text_size=22, row_h=86)
    checkbox_list(d, mid + 12, 540, 2372, rec_items, checked=(filled != "blank"), box_color=GREEN, text_size=22, row_h=86)

    y = 1156
    if filled == "momo":
        d.rectangle([28, y, 2372, 1328], fill=RED)
        d.text((W / 2, 1218), "SURGERY CANCELLED   ·   RECORD THE DECISION", font=font(32, True), fill=WHITE, anchor="mm")
        d.text((W / 2, 1272), "A cancelled exploratory is a successful preoperative evaluation.", font=font(20), fill=(244, 235, 211), anchor="mm")
    else:
        d.rectangle([28, y, 2372, 1328], fill=WHITE, outline=GOLD, width=3)
        note = {
            "blank": "If sedation or anesthesia is used, monitors are on first. The 5-minute grid belongs on this page, but this hour is the header, the prep, and recovery.",
            "willie": "Sedation happened after this header. Monitors on, then alfaxalone. This hour is the preop header, the ear and eye prep, and recovery.",
        }[filled]
        d.text((44, 1196), "If you sedate or anesthetize", font=font(18, True), fill=NAVY, anchor="lt")
        fn = font(20)
        ty = 1230
        for line in wrap_text(note, fn, 2280)[:3]:
            d.text((44, ty), line, font=fn, fill=INK, anchor="lt")
            ty += 28

    path = OUT / f"anesthesia_record_{filled}.png"
    im.save(path, "PNG")
    print("wrote", path)
    return path


def recovery_flowsheet():
    """Postoperative flowsheet for this hour: airway, perfusion, heat, pain, incision."""
    W, H = 2400, 1350
    im = Image.new("RGB", (W, H), OFF)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 88, W, 96], fill=GOLD)
    d.text((28, 22), "Postoperative flowsheet  ·  first 2 hours", font=font(36, True), fill=WHITE, anchor="lt")
    d.text((28, 62), "DVM 612  ·  Stay with the patient  ·  teaching form, not a hospital original", font=font(18), fill=GOLD, anchor="lt")

    y = 112
    headers = [(28, 520, "Patient"), (520, 1200, "Procedure"), (1200, 1680, "Extubate time"), (1680, 2372, "Recovery lead")]
    for x0, x1, lab in headers:
        cell(d, x0, y, x1, y + 32, lab, fill=NAVY, fg=WHITE, size=16, bold=True, align="center")
        cell(d, x0, y + 32, x1, y + 92, "", size=22)

    y = 220
    times = ["0–5 min", "15 min", "30 min", "45 min", "60 min", "90 min", "120 min"]
    rows = ["Time", "Airway", "mm / CRT / pulse", "Temp °F", "Pain score", "Incision", "E-collar on"]
    label_w = 280
    grid_x = 28 + label_w
    col = (2372 - grid_x) / 7
    row_h = 118
    for r, name in enumerate(rows):
        yy = y + r * row_h
        fill = TEAL if r == 0 else (WHITE if r % 2 == 0 else (236, 242, 244))
        fg = WHITE if r == 0 else INK
        cell(d, 28, yy, 28 + label_w, yy + row_h, name, fill=fill, fg=fg, size=20, bold=True, align="center")
        for c in range(7):
            val = times[c] if r == 0 else ""
            cell(
                d,
                grid_x + c * col,
                yy,
                grid_x + (c + 1) * col,
                yy + row_h,
                val,
                fill=fill if r == 0 else (WHITE if r % 2 == 0 else (236, 242, 244)),
                fg=WHITE if r == 0 else INK,
                size=20,
                bold=(r == 0),
                align="center",
            )

    y = y + 7 * row_h + 16
    d.rectangle([28, y, 2372, 1328], fill=WHITE, outline=GOLD, width=4)
    d.text((48, y + 28), "Call the surgeon NOW if:", font=font(24, True), fill=RED, anchor="lt")
    d.text(
        (48, y + 78),
        "Pale mm + tachycardia after celiotomy   ·   incision opening / viscera   ·   unrelenting pain",
        font=font(22),
        fill=INK,
        anchor="lt",
    )
    d.text(
        (48, y + 116),
        "Dyspnea   ·   seizure   ·   T < 97 °F and not waking   ·   no urine with a large bladder",
        font=font(22),
        fill=INK,
        anchor="lt",
    )

    path = OUT / "recovery_flowsheet.png"
    im.save(path, "PNG")
    print("wrote", path)


def kit_sheet():
    W, H = 2400, 1350
    im = Image.new("RGB", (W, H), OFF)
    d = ImageDraw.Draw(im)
    draw_header(d, W, "What must be in the room", "If it is not here before induction, you are not ready")

    cols = [
        (NAVY, "PRE-OP", [
            "Consent, estimate, DNR / code",
            "Today’s PE + ASA written",
            "Last meal recorded",
            "Labs you will actually use",
            "IV catheter + fluids",
            "Premed / induction drawn, labeled",
            "Analgesia plan (opioid ± NSAID ± local)",
            "Abx decision: yes (timed) or no",
            "Client phone on the board",
        ]),
        (TEAL, "PATIENT & SURGEON PREP", [
            "#40 clippers, spare blade, vacuum",
            "Eye lube; ear/eye protection plan",
            "Dirty-prep kit + sterile-prep kit",
            "7.5% PVP-I ~5 min, then 5% vet paint; eye 1:50 of 10% (Roberts 1986)",
            "Sterile gauze, bowls, gloves",
            "Four towels + large drape + clamps",
            "Gowns, closed-glove pairs (extra)",
            "Warming, padding, ties, ET tube",
            "Timeout / checklist card",
        ]),
        (GREEN, "POST-OP", [
            "Pulse ox, thermometer, stethoscope",
            "Oxygen / airway kit in recovery",
            "Heat (that cannot burn)",
            "Pain scale + the drugs you planned",
            "E-collar / suit that actually fits",
            "Recovery flowsheet (this lecture)",
            "Emergency criteria on discharge sheet",
            "Written meds + recheck date",
            "Who stays with the patient until sternal",
        ]),
    ]
    for i, (color, title, items) in enumerate(cols):
        x0 = 28 + i * 790
        x1 = x0 + 770
        d.rounded_rectangle([x0, 110, x1, 1288], radius=16, fill=WHITE, outline=LINE, width=2)
        d.rectangle([x0, 110, x1, 178], fill=color)
        d.text(((x0 + x1) / 2, 144), title, font=font(22, True), fill=WHITE, anchor="mm")
        for j, t in enumerate(items):
            yy = 210 + j * 116
            d.rounded_rectangle([x0 + 24, yy, x1 - 24, yy + 96], radius=10, fill=OFF)
            d.ellipse([x0 + 44, yy + 30, x0 + 80, yy + 66], outline=color, width=3)
            d.text((x0 + 62, yy + 48), str(j + 1), font=font(16, True), fill=color, anchor="mm")
            d.text((x0 + 104, yy + 48), t, font=font(18), fill=INK, anchor="lm")

    path = OUT / "what_you_need.png"
    im.save(path, "PNG")
    print("wrote", path)


def wrap_text(text, f, max_w):
    words = str(text).replace("/", " / ").split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def cell_wrap(d, x0, y0, x1, y1, text, *, fill=WHITE, fg=INK, size=12, bold=False):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=LINE, width=1)
    f = font(size, bold)
    lines = wrap_text(text, f, x1 - x0 - 14)
    line_h = size + 3
    total = line_h * min(len(lines), 4)
    ty = (y0 + y1) / 2 - total / 2 + line_h / 2
    for line in lines[:4]:
        d.text(((x0 + x1) / 2, ty), line, font=f, fill=fg, anchor="mm")
        ty += line_h


def asa_lab_table(filename, title, subtitle, headers, rows):
    W, H = 2400, 1350
    im = Image.new("RGB", (W, H), OFF)
    d = ImageDraw.Draw(im)
    draw_header(d, W, title, subtitle)

    cols = ["Finding", "Status 1", "Status 2", "Status 3", "Status 4", "Status 5"]
    col_fills = [NAVY, GREEN, TEAL, GOLD, RED, NAVY]
    x0 = 20
    x1 = W - 20
    widths = [280, 350, 350, 380, 430, 370]
    # normalize to x1-x0
    scale = (x1 - x0) / sum(widths)
    widths = [int(w * scale) for w in widths]
    y = 100
    row_h = int((H - 160) / (len(rows) + 1))
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)

    for c, (lab, fill) in enumerate(zip(cols, col_fills)):
        cell_wrap(d, xs[c], y, xs[c + 1], y + row_h, lab, fill=fill, fg=WHITE, size=16, bold=True)
    y += row_h
    stripe = [(255, 255, 255), (236, 242, 244)]
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            if c == 0:
                fill, fg, bold, size = NAVY, WHITE, True, 13
            else:
                fill, fg, bold, size = stripe[r % 2], INK, False, 12
            cell_wrap(d, xs[c], y, xs[c + 1], y + row_h, val, fill=fill, fg=fg, size=size, bold=bold)
        y += row_h

    d.rectangle([20, H - 52, W - 20, H - 16], fill=GOLD)
    d.text(
        (W / 2, H - 34),
        "Working teaching bands. They inform ASA. Today’s PE writes the number. Isolated numbers are not automatic Status. Read venous EPOC pO2 as venous, not arterial.",
        font=font(14, True),
        fill=NAVY,
        anchor="mm",
    )
    path = OUT / filename
    im.save(path, "PNG")
    print("wrote", path)


def cbc_chem_asa():
    asa_lab_table(
        "asa_cbc_chem.png",
        "CBC and chemistry → ASA Status",
        "Working teaching table  ·  use with today’s PE  ·  DVM 612",
        None,
        [
            ["CBC", "Normal", "Mild anemia / leukogram change", "Moderate anemia / inflammatory disease", "Severe anemia, marked thrombocytopenia, severe inflammatory / septic pattern", "Massive hemorrhage / severe marrow / sepsis with instability"],
            ["PCV", "Normal", "30–34% dog / 25–29% cat", "20–29% dog / 15–24% cat", "<20% dog / <15% cat", "Profound + shock"],
            ["Platelets", "Normal", "100–150 K", "50–99 K", "<50 K", "<30 K + active bleeding"],
            ["WBC", "Normal", "Mild deviation", "Moderate deviation", "Severe deviation + systemic disease", "Severe sepsis / leukopenia + shock"],
            ["Creatinine", "Normal", "Mild ↑", "Moderate ↑ / CKD", "Severe ↑ + uremia", "Severe renal failure + shock"],
            ["BUN", "Normal", "Mild ↑", "Moderate ↑", "Severe ↑ + uremia", "Severe + multisystem failure"],
            ["ALT / AST", "Normal", "<2×", "2–10×", ">10× + dysfunction", "Severe hepatic failure"],
            ["ALP", "Normal", "Mild isolated ↑", "Moderate / marked + disease", "Marked + cholestasis", "Hepatic failure"],
            ["Bilirubin", "Normal", "Mild ↑", "Moderate ↑", "Marked ↑ + dysfunction", "Severe hepatic / hemolytic crisis"],
            ["Albumin", "Normal", "2.0–2.5 g/dL", "1.5–1.9 g/dL", "1.0–1.4 g/dL", "<1.0 + clinical compromise"],
            ["Glucose", "Normal", "60–70 or 120–180", "50–59 or 180–300", "<50 or >300", "<40 + instability / DKA"],
            ["Na", "Normal", "130–139 or 156–165", "125–129 or 166–175", "120–124 or >175", "<120 + instability"],
            ["K", "Normal", "5.1–5.5 or 3.0–3.5", "5.6–6.0 or 2.5–2.9", ">6.0 or <2.5", "Severe + ECG / shock"],
            ["Phosphorus", "Normal", "Mild ↑", "Moderate ↑", "Severe ↑ + renal / metabolic disease", "Severe + multisystem failure"],
        ],
    )


def epoc_asa():
    asa_lab_table(
        "asa_epoc.png",
        "EPOC / blood gas → ASA Status",
        "Working teaching table  ·  pH, lactate, gases, bicarbonate, base excess  ·  DVM 612",
        None,
        [
            ["pH", "7.35–7.45", "7.30–7.34", "7.20–7.29", "<7.20", "Profound acidosis + shock"],
            ["Lactate", "<2–2.5", "2.5–4", "4–6", ">6", "Very high + hypoperfusion"],
            ["pCO₂", "Normal", "46–55", "56–65", ">65–70", "Severe ventilatory failure"],
            ["pO₂ (arterial)", "Normal", "60–79", "40–59", "<40", "Critical hypoxemia"],
            ["HCO₃⁻", "Normal", "16–17 or 25–28", "12–15 or 29–32", "<12 or >32", "Severe metabolic failure"],
            ["Base excess", "−4 to +4", "−5 to −7", "−8 to −10", "≤ −10 to −12", "Profound abnormality + instability"],
        ],
    )


if __name__ == "__main__":
    anesthesia_record("blank")
    anesthesia_record("willie")
    anesthesia_record("momo")
    recovery_flowsheet()
