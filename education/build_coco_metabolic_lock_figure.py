#!/usr/bin/env python3
"""Two-panel teaching figure for the Coco case. English labels only."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import (
    Arc,
    Circle,
    FancyArrowPatch,
    FancyBboxPatch,
    FancyBboxPatch as FBP,
    Polygon,
    Rectangle,
    Wedge,
)

OUT = Path(__file__).resolve().parent
W, H = 18.0, 10.7
DPI = 300

NAVY = "#1B365D"
SLATE = "#4A5568"
GREY = "#E8EBF0"
GREY2 = "#C9D1DA"
LEFT_BG = "#F7F3EE"
RIGHT_BG = "#EEF3F8"
ORANGE = "#C56A20"
RUST = "#8B2E12"
RED = "#B42318"
TEAL = "#1C4E6B"
GREEN = "#2C6B4A"
WHITE = "#FFFFFF"
INK = "#1A1A1A"
WARM_BOX = "#F8E8E0"
COOL_BOX = "#E4EEF4"
SOFT_RED = "#FDECEC"
SOFT_GREEN = "#E6F2EA"

FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
FONT_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
FONT_SB = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_BD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"

for _p in (FONT_REG, FONT_MED, FONT_SB, FONT_BD):
    fm.fontManager.addfont(_p)


def fp(size: float, which: str = "reg"):
    path = {"reg": FONT_REG, "med": FONT_MED, "sb": FONT_SB, "bd": FONT_BD}[which]
    return fm.FontProperties(fname=path, size=size)


def box(ax, x, y, w, h, facecolor, edgecolor, lw=1.15, radius=0.07, z=2):
    p = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=z,
    )
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, *, size=9.0, color=INK, which="reg", ha="center", va="center", z=5):
    ax.text(
        x,
        y,
        s,
        fontproperties=fp(size, which),
        color=color,
        ha=ha,
        va=va,
        zorder=z,
        linespacing=1.28,
    )


def arrow(ax, x1, y1, x2, y2, color=SLATE, lw=1.55, scale=13):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=scale,
            linewidth=lw,
            color=color,
            zorder=3,
        )
    )


def badge(ax, x, y, letter, fill, edge):
    ax.add_patch(Circle((x, y), 0.16, facecolor=fill, edgecolor=edge, lw=1.2, zorder=5))
    txt(ax, x, y, letter, size=11.5, color=WHITE, which="bd")


def drop_icon(ax, x, y, color, scale=1.0):
    ax.add_patch(Circle((x, y - 0.045 * scale), 0.062 * scale, facecolor=color, edgecolor=color, zorder=5))
    ax.add_patch(
        Polygon(
            [
                (x, y + 0.10 * scale),
                (x - 0.062 * scale, y - 0.01 * scale),
                (x + 0.062 * scale, y - 0.01 * scale),
            ],
            facecolor=color,
            edgecolor=color,
            zorder=5,
        )
    )


def flask_icon(ax, x, y, color):
    ax.add_patch(Rectangle((x - 0.046, y - 0.10), 0.092, 0.16, facecolor=WHITE, edgecolor=color, lw=1.6, zorder=5))
    ax.add_patch(Rectangle((x - 0.040, y - 0.10), 0.080, 0.07, facecolor=color, edgecolor=color, zorder=6))
    ax.add_patch(Rectangle((x - 0.056, y + 0.06), 0.112, 0.028, facecolor=color, edgecolor=color, zorder=5))
    ax.add_line(Line2D([x - 0.028, x + 0.028], [y - 0.02, y - 0.02], color=WHITE, lw=1.0, zorder=7))
    ax.add_line(Line2D([x - 0.028, x + 0.028], [y + 0.02, y + 0.02], color=color, lw=0.8, zorder=7))


def key_icon(ax, x, y, color, scale=1.25):
    ax.add_patch(
        Circle((x - 0.085 * scale, y), 0.052 * scale, facecolor="none", edgecolor=color, lw=1.8, zorder=5)
    )
    ax.add_line(Line2D([x - 0.035 * scale, x + 0.13 * scale], [y, y], color=color, lw=2.0, zorder=5))
    ax.add_line(Line2D([x + 0.07 * scale, x + 0.07 * scale], [y, y - 0.045 * scale], color=color, lw=1.7, zorder=5))
    ax.add_line(Line2D([x + 0.115 * scale, x + 0.115 * scale], [y, y - 0.032 * scale], color=color, lw=1.7, zorder=5))


def lock_icon(ax, x, y, color, *, open_shackle=False, scale=1.0):
    bw, bh = 0.26 * scale, 0.20 * scale
    ax.add_patch(
        FBP(
            (x - bw / 2, y - bh * 0.58),
            bw,
            bh,
            boxstyle=f"round,pad=0.008,rounding_size={0.035 * scale}",
            facecolor=color,
            edgecolor=color,
            zorder=5,
        )
    )
    ax.add_patch(Circle((x, y - 0.015 * scale), 0.032 * scale, facecolor=WHITE, edgecolor=WHITE, zorder=6))
    if open_shackle:
        ax.add_patch(
            Arc(
                (x + 0.085 * scale, y + 0.06 * scale),
                0.20 * scale,
                0.24 * scale,
                angle=18,
                theta1=35,
                theta2=210,
                color=color,
                lw=2.4,
                zorder=5,
            )
        )
    else:
        ax.add_patch(
            Arc(
                (x, y + 0.05 * scale),
                0.17 * scale,
                0.22 * scale,
                angle=0,
                theta1=5,
                theta2=175,
                color=color,
                lw=2.4,
                zorder=5,
            )
        )


def moon_icon(ax, x, y, color):
    ax.add_patch(Circle((x, y), 0.062, facecolor=color, edgecolor=color, zorder=5))
    ax.add_patch(Circle((x + 0.024, y + 0.012), 0.048, facecolor=WHITE, edgecolor=WHITE, zorder=6))


def bowl_icon(ax, x, y, color):
    ax.add_patch(Wedge((x, y), 0.085, 185, 355, facecolor=color, edgecolor=color, zorder=5))
    ax.add_patch(Circle((x - 0.022, y + 0.012), 0.018, facecolor=ORANGE, edgecolor=ORANGE, zorder=6))
    ax.add_patch(Circle((x + 0.028, y + 0.018), 0.014, facecolor=GREEN, edgecolor=GREEN, zorder=6))


def vial_icon(ax, x, y, color):
    ax.add_patch(Rectangle((x - 0.028, y - 0.08), 0.056, 0.14, facecolor=color, edgecolor=color, zorder=5))
    ax.add_patch(Rectangle((x - 0.020, y + 0.06), 0.040, 0.038, facecolor=SLATE, edgecolor=SLATE, zorder=6))
    drop_icon(ax, x + 0.07, y + 0.02, ORANGE, scale=0.62)


def brain_icon(ax, x, y, color):
    ax.add_patch(Circle((x - 0.035, y + 0.012), 0.078, facecolor=color, edgecolor=color, zorder=5, alpha=0.88))
    ax.add_patch(Circle((x + 0.045, y), 0.072, facecolor=color, edgecolor=color, zorder=5, alpha=0.88))


def kidney_icon(ax, x, y, color):
    ax.add_patch(Circle((x, y + 0.035), 0.062, facecolor=color, edgecolor=color, zorder=5))
    ax.add_patch(Circle((x + 0.012, y - 0.045), 0.056, facecolor=color, edgecolor=color, zorder=5))


def draw_left(ax):
    box(ax, 0.22, 0.40, 8.56, 9.38, LEFT_BG, GREY2, lw=1.05, radius=0.10)
    box(ax, 0.40, 9.18, 8.20, 0.44, WARM_BOX, RUST, lw=1.25, radius=0.06)
    badge(ax, 0.68, 9.40, "A", RUST, RUST)
    txt(
        ax,
        4.62,
        9.40,
        "The Conventional Trap: Treating the Symptom, Not the Cause",
        size=11.4,
        color=RUST,
        which="bd",
    )

    box(ax, 0.44, 8.10, 2.70, 0.90, WHITE, SLATE, lw=1.05)
    drop_icon(ax, 0.74, 8.58, TEAL, scale=1.05)
    txt(ax, 2.00, 8.68, "Severe polydipsia", size=9.0, color=NAVY, which="sb")
    txt(ax, 2.00, 8.38, "PU / PD", size=8.2, color=SLATE, which="med")

    box(ax, 5.86, 8.10, 2.70, 0.90, WHITE, SLATE, lw=1.05)
    flask_icon(ax, 6.16, 8.56, TEAL)
    txt(ax, 7.42, 8.68, "Hyposthenuria", size=9.0, color=NAVY, which="sb")
    txt(ax, 7.42, 8.38, "USG 1.004*", size=8.2, color=SLATE, which="med")

    arrow(ax, 3.14, 8.30, 3.55, 7.92, SLATE)
    arrow(ax, 5.86, 8.30, 5.45, 7.92, SLATE)

    box(ax, 2.55, 6.95, 3.90, 0.98, WARM_BOX, RUST, lw=1.45, radius=0.07)
    txt(ax, 4.50, 7.68, "Old specialist label", size=8.0, color=RUST, which="sb")
    txt(ax, 4.50, 7.28, "PRIMARY CENTRAL DI (CDI)", size=11.0, color=NAVY, which="bd")

    box(ax, 0.44, 5.72, 8.12, 1.02, SOFT_RED, RED, lw=1.25, radius=0.06)
    txt(ax, 0.72, 6.36, "?", size=22, color=RED, which="bd", ha="left")
    txt(ax, 4.70, 6.42, "Metabolic data missed", size=9.2, color=RUST, which="bd")
    txt(
        ax,
        4.70,
        6.10,
        "Intact PTH  25.00 pmol/L  (2.5× high)*     ·     ionized Ca normal*",
        size=8.6,
        color=NAVY,
        which="med",
    )
    txt(
        ax,
        4.70,
        5.86,
        "Lecture-note values. Not on the Antech / IDEXX pages in the student packet.",
        size=7.6,
        color=SLATE,
        which="reg",
    )

    txt(ax, 4.50, 5.50, "Vicious cycle after the label", size=9.0, color=SLATE, which="sb")

    box(ax, 0.44, 4.30, 2.42, 1.02, WHITE, RUST, lw=1.05)
    txt(ax, 1.65, 5.02, "Vetoryl (trilostane)", size=8.4, color=RUST, which="sb")
    txt(ax, 1.65, 4.68, "Stopped after anorexia\nand lethargy recorded", size=8.0, color=NAVY, which="reg")

    arrow(ax, 2.90, 4.81, 3.18, 4.81, RUST)
    box(ax, 3.22, 4.30, 1.95, 1.02, WHITE, SLATE, lw=1.05)
    txt(ax, 4.20, 4.81, "Cessation\nof meds", size=9.2, color=NAVY, which="bd")

    arrow(ax, 5.21, 4.81, 5.48, 4.81, RUST)
    box(ax, 5.52, 4.22, 3.04, 1.18, WARM_BOX, RUST, lw=1.35)
    txt(ax, 7.04, 5.12, "Desmopressin cycle", size=8.4, color=RUST, which="sb")
    txt(ax, 7.04, 4.76, "1 drop TID  →  2 drops BID", size=8.6, color=NAVY, which="bd")
    txt(ax, 7.04, 4.44, "Printed chart. Failure to concentrate.", size=7.4, color=SLATE, which="reg")

    box(ax, 0.44, 3.12, 3.92, 0.92, WHITE, SLATE, lw=1.05)
    moon_icon(ax, 0.78, 3.58, TEAL)
    txt(ax, 2.58, 3.70, "Agitation and night waking", size=8.8, color=NAVY, which="sb")
    txt(ax, 2.58, 3.38, "Owner sees “dementia,” not dilute urine", size=7.6, color=SLATE, which="reg")

    box(ax, 4.58, 3.12, 3.98, 0.92, WHITE, SLATE, lw=1.05)
    txt(ax, 6.57, 3.70, "Vomiting / GI upset", size=8.8, color=NAVY, which="sb")
    txt(ax, 6.57, 3.38, "Later bronchitis and pneumonia", size=7.6, color=SLATE, which="reg")

    box(ax, 0.44, 0.56, 8.12, 2.36, WHITE, GREY2, lw=1.05)
    txt(ax, 4.50, 2.66, "What the printed chart actually supports", size=9.0, color=SLATE, which="sb")
    txt(
        ax,
        4.50,
        1.55,
        "A CDI label was entered without an ACTH, LDDS, or water-deprivation page in the packet.\n"
        "Three things moved in two weeks: trilostane stopped, a conflicting UTI treated,\n"
        "and desmopressin started. A response is not proof of primary central ADH deficiency.\n"
        "Creatinine stayed 0.3–0.8 mg/dL. Normal creatinine does not close polyuria.\n"
        "USG 1.004* is a lecture-note figure. Printed in-house values start at 1.006 / 1.008.",
        size=8.2,
        color=INK,
        which="reg",
    )


def draw_right(ax):
    box(ax, 9.22, 0.40, 8.56, 9.38, RIGHT_BG, "#B7C9D6", lw=1.05, radius=0.10)
    box(ax, 9.40, 9.18, 8.20, 0.44, COOL_BOX, TEAL, lw=1.25, radius=0.06)
    badge(ax, 9.68, 9.40, "B", TEAL, TEAL)
    txt(
        ax,
        13.62,
        9.40,
        "The Metabolic Working Model: Unlocking V2 / AQP2",
        size=11.4,
        color=TEAL,
        which="bd",
    )

    box(ax, 9.40, 8.10, 8.20, 0.90, COOL_BOX, TEAL, lw=1.35)
    txt(ax, 13.50, 8.74, "Working diagnosis  (proposed)", size=8.0, color=TEAL, which="sb")
    txt(
        ax,
        13.50,
        8.38,
        "Secondary nephrogenic DI     ·     secondary hyperparathyroidism",
        size=10.2,
        color=NAVY,
        which="bd",
    )

    box(ax, 9.40, 6.08, 8.20, 1.86, WHITE, RUST, lw=1.25)
    txt(ax, 13.50, 7.70, "Proposed lock     ·     excess PTH*     ·     inactive V2 / AQP2", size=8.8, color=RUST, which="sb")
    key_icon(ax, 10.20, 6.88, SLATE, scale=1.85)
    txt(ax, 10.20, 6.38, "DDAVP  (key)", size=8.0, color=SLATE, which="med")
    lock_icon(ax, 12.05, 6.88, RUST, open_shackle=False, scale=1.55)
    txt(ax, 12.05, 6.38, "V2 / AQP2  inactive", size=8.0, color=RUST, which="sb")
    box(ax, 12.55, 7.18, 0.92, 0.28, SOFT_RED, RED, lw=0.9, radius=0.05)
    txt(ax, 13.01, 7.32, "PTH* holds", size=7.0, color=RED, which="sb")
    # blocked mark on the shaft
    ax.add_line(Line2D([10.72, 11.42], [6.88, 6.88], color=RUST, lw=2.0, zorder=4))
    ax.text(11.07, 6.88, "×", fontproperties=fp(16, "bd"), color=RED, ha="center", va="center", zorder=6)
    box(ax, 13.55, 6.48, 3.78, 0.78, WARM_BOX, RUST, lw=1.15)
    txt(ax, 15.44, 6.98, "USG 1.004*     ·     failure to concentrate", size=9.0, color=NAVY, which="bd")
    txt(ax, 15.44, 6.68, "The key does not turn while the lock is held.", size=7.6, color=SLATE, which="reg")
    txt(
        ax,
        13.50,
        6.22,
        "Hypothesis only: PTH 2.5× high* is proposed to resist the V2 / AQP2 cascade. No receptor assay is in the record.",
        size=7.5,
        color=SLATE,
        which="reg",
    )

    box(ax, 9.40, 4.58, 8.20, 1.42, WHITE, TEAL, lw=1.25)
    txt(ax, 13.50, 5.76, "Targeted therapeutic plan  (as taught)", size=8.8, color=TEAL, which="sb")
    bowl_icon(ax, 10.05, 5.12, TEAL)
    txt(ax, 11.42, 5.28, "Dietary correction", size=8.8, color=NAVY, which="sb")
    txt(ax, 11.42, 4.96, "Ca : P ratio  ·  less bovine tissue", size=7.6, color=SLATE, which="reg")
    vial_icon(ax, 13.55, 5.14, TEAL)
    txt(ax, 15.18, 5.28, "Calcitriol / vitamin D3", size=8.8, color=NAVY, which="sb")
    txt(ax, 15.18, 4.96, "Confirm the number in Plumb", size=7.6, color=SLATE, which="reg")
    txt(
        ax,
        13.50,
        4.72,
        "Goal: suppress PTH into the reference interval, then retest ionized Ca, PTH, phosphorus, and 25-OH D.",
        size=7.6,
        color=SLATE,
        which="reg",
    )

    box(ax, 9.40, 2.82, 8.20, 1.60, WHITE, GREEN, lw=1.35)
    txt(ax, 13.50, 4.18, "Proposed unlock     ·     corrected minerals     ·     active V2 / AQP2", size=8.8, color=GREEN, which="sb")
    key_icon(ax, 10.20, 3.48, GREEN, scale=1.85)
    txt(ax, 10.20, 2.98, "DDAVP  (key)", size=8.0, color=GREEN, which="med")
    lock_icon(ax, 12.05, 3.48, GREEN, open_shackle=True, scale=1.55)
    txt(ax, 12.05, 2.98, "V2 / AQP2  active", size=8.0, color=GREEN, which="sb")
    arrow(ax, 10.72, 3.48, 11.42, 3.48, GREEN, lw=2.0, scale=15)
    box(ax, 13.55, 3.10, 3.78, 0.78, SOFT_GREEN, GREEN, lw=1.15)
    txt(ax, 15.44, 3.62, "USG 1.012–1.017*     ·     sleep improved*", size=8.8, color=NAVY, which="bd")
    txt(ax, 15.44, 3.30, "Corrected minerals are proposed to release the cascade.", size=7.6, color=SLATE, which="reg")

    box(ax, 9.40, 0.56, 8.20, 2.18, WHITE, GREY2, lw=1.05)
    txt(ax, 13.50, 2.50, "How a doctor should read this panel", size=9.0, color=SLATE, which="sb")
    txt(
        ax,
        13.50,
        1.48,
        "A rising USG after diet and vitamin D support is compatible with a metabolic contribution.\n"
        "It does not by itself prove receptor-level resistance, and it does not exclude residual\n"
        "CDI, hyperadrenocorticism, or infection. Sort every claim into four boxes:\n"
        "observed finding  ·  interpretation  ·  causal hypothesis  ·  diagnostic conclusion.\n"
        "This figure is a teaching model. It is not a proof that Coco did not have CDI.",
        size=8.2,
        color=INK,
        which="reg",
    )


def main() -> None:
    fig = plt.figure(figsize=(W, H), dpi=DPI, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    ax.set_facecolor(WHITE)

    txt(
        ax,
        9.0,
        10.42,
        "From Resistance to Recovery: Breaking the Metabolic Lock",
        size=19.5,
        color=NAVY,
        which="bd",
    )
    txt(
        ax,
        9.0,
        10.02,
        "Coco   ·   Integration Medicine III   ·   A  conventional central-ADH path    vs    B  proposed renal / mineral path",
        size=9.0,
        color=SLATE,
        which="med",
    )

    ax.add_line(Line2D([9.00, 9.00], [0.48, 9.55], color=GREY2, lw=1.15, zorder=3))

    draw_left(ax)
    draw_right(ax)

    txt(
        ax,
        9.0,
        0.18,
        "* Lecture-note values (PTH 25.00 pmol/L; USG 1.004–1.006 and 1.012–1.017). Confirm against the laboratory page before publication.  "
        "Dr. Yujin Kim, DVM, PhD, FFCP  ·  Lewyt College of Veterinary Medicine.",
        size=7.3,
        color=SLATE,
        which="reg",
    )

    png = OUT / "IM3_Coco_Metabolic_Lock_Figure.png"
    pdf = OUT / "IM3_Coco_Metabolic_Lock_Figure.pdf"
    fig.savefig(png, dpi=DPI, facecolor=WHITE)
    fig.savefig(pdf, dpi=DPI, facecolor=WHITE)
    plt.close(fig)
    print(png, png.stat().st_size)
    print(pdf, pdf.stat().st_size)


if __name__ == "__main__":
    main()
