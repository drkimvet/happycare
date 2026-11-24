#!/usr/bin/env python3
"""Composite an anatomically correct vertical mattress onto a photoreal pad.

Far-far then near-near. Surface bars sit on each side of the incision.
Original teaching figure. Not a textbook scan.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
PAD = HERE / "blank_rect.png"
OUT = HERE / "suture3d_vertical_mattress.png"

# Top-face quad of the rectangular teaching pad (NW far-left, NE far-right,
# SE near-right, SW near-left). Inset sutures stay on the surface.
CORNERS = {
    "NW": np.array((218.0, 268.0)),
    "NE": np.array((792.0, 158.0)),
    "SE": np.array((952.0, 552.0)),
    "SW": np.array((372.0, 688.0)),
}

NAVY = (11, 24, 42, 255)
NAVY_EDGE = (6, 14, 26, 255)
HIGHLIGHT = (186, 198, 210, 165)
SHADOW = (28, 22, 18, 80)
HOLE = (42, 32, 28, 230)
HOLE_CORE = (22, 16, 14, 255)
INCISION = (108, 70, 58, 210)


def xy(u, v):
    nw, ne, se, sw = (CORNERS[k] for k in ("NW", "NE", "SE", "SW"))
    p = (1 - v) * ((1 - u) * nw + u * ne) + v * ((1 - u) * sw + u * se)
    return float(p[0]), float(p[1])


def polyline(u0, v0, u1, v1, n=24):
    return [xy(u0 + (u1 - u0) * i / n, v0 + (v1 - v0) * i / n) for i in range(n + 1)]


def width_at(v, base):
    return max(3, int(round(base * (0.82 + 0.18 * v))))


def draw_thread(draw, pts, base_w=6):
    if len(pts) < 2:
        return
    v_mean = 0.5
    w = width_at(v_mean, base_w)
    shadow = [(x + 1.8, y + 2.4) for x, y in pts]
    draw.line(shadow, fill=SHADOW, width=w + 4, joint="curve")
    draw.line(pts, fill=NAVY_EDGE, width=w + 2, joint="curve")
    draw.line(pts, fill=NAVY, width=w, joint="curve")
    hi = [(x - 0.8, y - 1.0) for x, y in pts]
    draw.line(hi, fill=HIGHLIGHT, width=max(1, w // 3), joint="curve")


def draw_hole(draw, u, v, r=3.8):
    x, y = xy(u, v)
    scale = 0.80 + 0.20 * v
    rx, ry = r * scale, r * scale * 0.62
    draw.ellipse((x - rx, y - ry + 0.8, x + rx, y + ry + 0.8), fill=(30, 24, 20, 70))
    draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=HOLE)
    draw.ellipse((x - rx * 0.45, y - ry * 0.55, x + rx * 0.2, y - ry * 0.05), fill=HOLE_CORE)


def draw_knot(draw, u, v):
    cx, cy = xy(u, v)
    blobs = (
        (-2.8, -1.6, 3.4, 2.6),
        (1.6, -2.0, 3.2, 2.5),
        (-0.2, 0.8, 3.6, 2.7),
        (2.4, 1.2, 2.8, 2.2),
    )
    for dx, dy, rw, rh in blobs:
        draw.ellipse((cx + dx - rw, cy + dy - rh, cx + dx + rw, cy + dy + rh), fill=NAVY)
    tails = [
        [(cx - 6, cy + 2), (cx - 15, cy + 9)],
        [(cx - 3, cy + 4), (cx - 9, cy + 14)],
    ]
    for t in tails:
        draw.line(t, fill=NAVY, width=3, joint="curve")


def stitch(draw, v):
    fl, nl, nr, fr = 0.18, 0.40, 0.60, 0.82
    draw_thread(draw, polyline(fl, v, nl, v), base_w=8)
    draw_thread(draw, polyline(nr, v, fr, v), base_w=8)
    for u in (fl, nl, nr, fr):
        draw_hole(draw, u, v)
    draw_knot(draw, (fl + nl) / 2.0, v)


def main():
    base = Image.open(PAD).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.line(polyline(0.5, 0.24, 0.5, 0.76, n=40), fill=INCISION, width=3, joint="curve")
    stitch(draw, 0.36)
    stitch(draw, 0.56)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.28))
    Image.alpha_composite(base, overlay).convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
