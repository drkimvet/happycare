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


def anesthesia_record(filled="blank"):
    W, H = 2400, 1350
    im = Image.new("RGB", (W, H), OFF)
    d = ImageDraw.Draw(im)
    draw_header(
        d,
        W,
        "Small-animal anesthesia / sedation record",
        "DVM 612  ·  Preop · intra · recovery  ·  fill every box that applies",
    )

    # Identity row
    y = 104
    labels = [
        (28, 380, "Patient"),
        (380, 780, "Species / breed"),
        (780, 1040, "Sex / age"),
        (1040, 1280, "Weight"),
        (1280, 1560, "Date"),
        (1560, 1780, "ASA"),
        (1780, 2372, "Procedure"),
    ]
    for x0, x1, lab in labels:
        cell(d, x0, y, x1, y + 28, lab, fill=NAVY, fg=WHITE, size=12, bold=True, align="center")

    values = {
        "blank": ["", "", "", "", "", "", ""],
        "willie": [
            "Willie",
            "Canine  ·  Cavalier King Charles",
            "MN  ·  6 y 11 mo",
            "13.7 kg  BCS 6/9",
            "13 Sep 2026",
            "III-E",
            "Alfaxalone sedation: deep AS clean + cytology",
        ],
        "momo": [
            "MoMo",
            "Feline  ·  DSH",
            "SF  ·  6 yr",
            "4.25 kg  BCS 5/9",
            "13 Sep 2026",
            "IV-E",
            "Exploratory considered; cancelled (renal, not GI)",
        ],
    }[filled]
    for (x0, x1, _), val in zip(labels, values):
        cell(d, x0, y + 28, x1, y + 70, val, size=15, bold=True)

    # Preop vitals / PE
    y = 186
    d.rectangle([28, y, 2372, y + 36], fill=TEAL)
    d.text((40, y + 18), "Preoperative evaluation  (complete BEFORE premedication)", font=font(16, True), fill=WHITE, anchor="lm")

    y = 228
    preop_h = [
        (28, 280, "T °F"),
        (280, 500, "HR"),
        (500, 720, "RR"),
        (720, 980, "mm / CRT"),
        (980, 1280, "Mentation"),
        (1280, 1680, "Heart / lungs"),
        (1680, 2372, "Problems that change the plan"),
    ]
    preop_v = {
        "blank": ["", "", "", "", "", "", ""],
        "willie": ["100.8", "132", "52", "pink / 2 s", "quiet, dull", "II/VI left systolic; lungs clear", "Vestibular + AS otitis; TM swollen; murmur; no NSAID after DexSP"],
        "momo": ["98.0", "200", "30", "pink, tacky / <2", "QAR", "NSR, no murmur; eupneic", "Vomiting; possible FB vs toxin; azotemia; bilateral renomegaly"],
    }[filled]
    for (x0, x1, lab), val in zip(preop_h, preop_v):
        cell(d, x0, y, x1, y + 26, lab, fill=(228, 236, 238), fg=TEAL, size=11, bold=True, align="center")
        cell(d, x0, y + 26, x1, y + 70, val, size=13)

    # Drugs
    y = 310
    d.rectangle([28, y, 2372, y + 32], fill=NAVY)
    d.text((40, y + 16), "Drugs  ·  fluids  ·  airway   (dose, route, time)", font=font(15, True), fill=WHITE, anchor="lm")

    y = 348
    drug_labs = ["Premed / adjuncts", "Induction / sedation", "Maintenance", "Fluids", "Local / other", "Airway"]
    drug_v = {
        "blank": [""] * 6,
        "willie": [
            "Cerenia IV; DexSP 0.68 mL SQ  ·  no NSAID",
            "Alfaxalone 2.74 mL IV (~2 mg/kg of 10 mg/mL)",
            "Injectable sedation for ear clean (not a celiotomy)",
            "IV crystalloid running",
            "Animax infused AS after clean. Aminoglycoside risk if OMI",
            "Protect airway; pad; he falls. Do not skip monitoring.",
        ],
        "momo": [
            "None before work-up",
            "NONE for exploratory. Do not induce",
            "N/A",
            "IVF 1.5× maint (40 mL/kg/d)",
            "Cerenia 1 mg/kg IV q24; ondansetron 0.5 mg/kg IV q8; Unasyn 30 mg/kg IV q8; AlOH PO",
            "N/A. Not a surgical anesthetic event",
        ],
    }[filled]
    col_w = (2372 - 28) / 6
    for i, (lab, val) in enumerate(zip(drug_labs, drug_v)):
        x0 = 28 + i * col_w
        x1 = 28 + (i + 1) * col_w
        cell(d, x0, y, x1, y + 28, lab, fill=GOLD, fg=NAVY, size=12, bold=True, align="center")
        # wrap value
        d.rectangle([x0, y + 28, x1, y + 118], fill=WHITE, outline=LINE, width=1)
        # simple wrap
        words = val.split()
        lines, cur = [], ""
        f = font(13)
        for w in words:
            trial = (cur + " " + w).strip()
            if f.getlength(trial) < (x1 - x0 - 16):
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        ty = y + 40
        for line in lines[:4]:
            d.text((x0 + 8, ty), line, font=f, fill=INK, anchor="lt")
            ty += 18

    # Monitoring grid
    y = 480
    d.rectangle([28, y, 2372, y + 32], fill=TEAL)
    d.text((40, y + 16), "Intra-procedure monitoring  (every 5 min while sedated/anesthetized)", font=font(15, True), fill=WHITE, anchor="lm")

    y = 518
    times = ["0", "5", "10", "15", "20", "25", "30", "35", "40"]
    rows = ["Time (min)", "HR", "RR", "SpO2 %", "ETCO2", "BP", "Temp °F", "Plane / jaw", "Events"]
    willie_grid = {
        "Time (min)": times,
        "HR": ["132", "118", "110", "108", "112", "", "", "", ""],
        "RR": ["52", "28", "24", "22", "24", "", "", "", ""],
        "SpO2 %": ["", "98", "99", "98", "98", "", "", "", ""],
        "ETCO2": ["", "", "", "", "", "", "", "", ""],
        "BP": ["", "", "", "", "", "", "", "", ""],
        "Temp °F": ["100.8", "", "", "", "100.2", "", "", "", ""],
        "Plane / jaw": ["awake", "sedated", "plane OK", "plane OK", "lightening", "", "", "", ""],
        "Events": ["IVC/fluids", "alfaxalone", "ear clean AS", "cytology", "recover", "", "", "", ""],
    }
    momo_grid = {k: [""] * 9 for k in rows}
    momo_grid["Time (min)"] = times
    momo_grid["Events"] = ["STOP", "Do not", "induce", "for FB", "explore", "", "", "", ""]

    grid = {"blank": {k: ([k] if k == "Time (min)" else [""] * 9) for k in rows}, "willie": willie_grid, "momo": momo_grid}[filled]
    if filled == "blank":
        grid["Time (min)"] = times

    label_w = 220
    grid_x = 28 + label_w
    col = (2372 - grid_x) / 9
    row_h = 36
    for r, name in enumerate(rows):
        yy = y + r * row_h
        fill = NAVY if r == 0 else (WHITE if r % 2 == 0 else (236, 242, 244))
        fg = WHITE if r == 0 else INK
        cell(d, 28, yy, 28 + label_w, yy + row_h, name, fill=fill, fg=fg, size=13, bold=True, align="center")
        for c in range(9):
            val = grid[name][c] if name in grid else ""
            cfill = GOLD if (filled == "momo" and r == 0) else fill
            cell(
                d,
                grid_x + c * col,
                yy,
                grid_x + (c + 1) * col,
                yy + row_h,
                val,
                fill=cfill if r == 0 else fill,
                fg=WHITE if r == 0 else INK,
                size=13,
                bold=(r == 0),
                align="center",
            )

    # Recovery + checklist
    y = 518 + 9 * 36 + 16
    d.rectangle([28, y, 1180, y + 32], fill=GREEN)
    d.text((40, y + 16), "Recovery  (the surgery is not over)", font=font(15, True), fill=WHITE, anchor="lm")
    d.rectangle([1200, y, 2372, y + 32], fill=RED)
    d.text((1212, y + 16), "Never-blank boxes", font=font(15, True), fill=WHITE, anchor="lm")

    rec_items = {
        "blank": ["Extubate when swallow returns (species-specific)", "SpO2 / mm / CRT / pulse", "Temp: rewarm, do not burn", "Pain score + the analgesic you planned", "Incision / procedure site check", "E-collar before they can lick", "Urinate? Client phone on the board"],
        "willie": [
            "Recover padded, no stairs",
            "Watch nystagmus, circling, vomiting, seizures",
            "No NSAID (DexSP already given)",
            "Meclizine 25 mg PO BID × 5 d",
            "Cerenia 60 mg PO SID × 4 d",
            "MRI recommended; TECA-LBO only if medical fails",
            "Confine. Call the owner with neuro status",
        ],
        "momo": [
            "Not a recovery from surgery",
            "Hospitalized: QAR, IVF, antiemetics, Unasyn",
            "Recheck renal values. Worsened on fluids",
            "AUS: R kidney fluid-filled, non-functional; L kidney abnormal",
            "IM referral for FNA of LEFT kidney discussed",
            "Prognosis guarded to poor",
            "Owner elected humane euthanasia",
        ],
    }[filled]
    yy = y + 40
    for i, t in enumerate(rec_items):
        d.rectangle([28, yy + i * 28, 1180, yy + i * 28 + 26], fill=WHITE, outline=LINE)
        d.rectangle([36, yy + i * 28 + 6, 54, yy + i * 28 + 22], outline=GREEN, width=2)
        if filled != "blank":
            d.line([40, yy + i * 28 + 14, 50, yy + i * 28 + 20], fill=GREEN, width=2)
            d.line([50, yy + i * 28 + 20, 62, yy + i * 28 + 8], fill=GREEN, width=2)
        d.text((70, yy + i * 28 + 13), t, font=font(14), fill=INK, anchor="lm")

    never = [
        "Identity / consent / DNR",
        "Today’s PE + ASA (not yesterday’s)",
        "Last meal",
        "IV catheter patent",
        "Monitoring on before drugs",
        "Abx 30–60 min pre-incision IF indicated",
        "Pain plan written",
        "Who calls the client, and when",
    ]
    if filled == "momo":
        never = [
            "Imaging BEFORE the exploratory",
            "Serial creatinine. Do not ignore a rising value",
            "USG 1.042 ≠ ‘kidneys are fine’",
            "POCUS: kidneys, not a surgical GI obstruction",
            "Do not cut a non-surgical abdomen",
            "Consent includes no-surgery and euthanasia",
            "NSAIDs contraindicated in this azotemic cat",
            "Record the decision not to operate",
        ]
    for i, t in enumerate(never):
        d.rectangle([1200, yy + i * 28, 2372, yy + i * 28 + 26], fill=WHITE, outline=LINE)
        d.text((1216, yy + i * 28 + 13), "▸  " + t, font=font(14), fill=RED if filled == "momo" else INK, anchor="lm")

    if filled == "momo":
        d.rectangle([700, 640, 1700, 760], fill=(139, 46, 46))
        d.text((1200, 700), "DO NOT INDUCE  ·  SURGERY CANCELLED", font=font(28, True), fill=WHITE, anchor="mm")

    path = OUT / f"anesthesia_record_{filled}.png"
    im.save(path, "PNG")
    print("wrote", path)
    return path


def recovery_flowsheet():
    W, H = 2400, 1350
    im = Image.new("RGB", (W, H), OFF)
    d = ImageDraw.Draw(im)
    draw_header(d, W, "Immediate postoperative flowsheet  (first 2 hours)", "DVM 612  ·  ABC + temperature + pain  ·  stay with the patient")

    y = 104
    for x0, x1, lab in [(28, 500, "Patient"), (500, 1100, "Procedure"), (1100, 1500, "Extubate time"), (1500, 1900, "Pain scale used"), (1900, 2372, "Recovery lead")]:
        cell(d, x0, y, x1, y + 26, lab, fill=NAVY, fg=WHITE, size=12, bold=True, align="center")
        cell(d, x0, y + 26, x1, y + 70, "", size=14)

    y = 186
    times = ["0–5 min", "15 min", "30 min", "45 min", "60 min", "90 min", "120 min"]
    rows = ["Time", "HR", "RR / effort", "mm / CRT", "SpO2", "Temp °F", "Pain score", "Incision", "Pee / vomit", "Rx given"]
    label_w = 200
    grid_x = 28 + label_w
    col = (2372 - grid_x) / 7
    row_h = 70
    for r, name in enumerate(rows):
        yy = y + r * row_h
        fill = TEAL if r == 0 else (WHITE if r % 2 == 0 else (236, 242, 244))
        fg = WHITE if r == 0 else INK
        cell(d, 28, yy, 28 + label_w, yy + row_h, name, fill=fill, fg=fg, size=14, bold=True, align="center")
        for c in range(7):
            val = times[c] if r == 0 else ""
            cell(d, grid_x + c * col, yy, grid_x + (c + 1) * col, yy + row_h, val, fill=fill if r == 0 else (WHITE if r % 2 == 0 else (236, 242, 244)), fg=WHITE if r == 0 else INK, size=14, bold=(r == 0), align="center")

    y = y + 10 * row_h + 16
    d.rectangle([28, y, 2372, y + 90], fill=WHITE, outline=GOLD, width=3)
    d.text((44, y + 16), "Call the surgeon NOW if:", font=font(16, True), fill=RED, anchor="lt")
    d.text((44, y + 48), "Pale mm + tachycardia after celiotomy  ·  incision opening / viscera  ·  unrelenting pain  ·  dyspnea  ·  seizure  ·  T < 97 °F and not waking  ·  no urine with a large bladder", font=font(15), fill=INK, anchor="lt")

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
            "10% PVP-I (mucosa/eye 1:20–1:50) and/or 2–4% CHG",
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
        "Working teaching bands. They inform ASA; they do not replace today’s PE. Isolated numbers are not automatic Status. Venous EPOC pO2 is not arterial pO2.",
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
    kit_sheet()
    cbc_chem_asa()
    epoc_asa()
