#!/usr/bin/env python3
"""Original teaching stills for DVM 612 Week 15. Not textbook plates."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
NAVY = (11, 44, 74)
GOLD = (197, 163, 90)
GOLD_LT = (244, 235, 211)
OFF = (246, 247, 249)
INK = (28, 28, 28)
SLATE = (61, 74, 87)
WHITE = (255, 255, 255)
SKIN = (232, 196, 164)
RED = (139, 46, 46)
GREEN = (46, 107, 79)


def font(size):
    for name in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "LiberationSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def canvas(w=1400, h=1050):
    im = Image.new("RGB", (w, h), OFF)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 70], fill=NAVY)
    return im, d


def caption(d, w, text):
    d.text((24, 18), text, fill=GOLD, font=font(28))


def save(im, name):
    path = OUT / name
    im.save(path, "PNG", optimize=True)
    print(path, path.stat().st_size)


def layers():
    im, d = canvas()
    caption(d, 1400, "Three bandage layers  ·  original teaching figure")
    boxes = [
        (160, 160, 1240, 380, GOLD, "1. Primary  ·  contact", "Touches the wound. Adherent or nonadherent.\nChoice follows exudate, necrosis, and granulation."),
        (160, 420, 1240, 640, NAVY, "2. Secondary  ·  padding", "Absorbs. Pads. Supports. Never sits on the wound itself."),
        (160, 680, 1240, 900, GREEN, "3. Tertiary  ·  wrap", "Holds the stack. Protects from the environment. Even tension."),
    ]
    for l, t, r, b, c, title, body in boxes:
        d.rounded_rectangle([l, t, r, b], radius=24, fill=WHITE, outline=c, width=8)
        d.rectangle([l, t, l + 18, b], fill=c)
        d.text((l + 48, t + 28), title, fill=c, font=font(36))
        d.text((l + 48, t + 90), body, fill=SLATE, font=font(28))
    save(im, "bandage_three_layers.png")


def stirrups():
    im, d = canvas()
    caption(d, 1400, "Tape stirrups  ·  original teaching figure")
    d.rounded_rectangle([430, 140, 970, 980], radius=80, fill=SKIN, outline=NAVY, width=6)
    d.polygon([(430, 140), (700, 40), (970, 140)], fill=SKIN, outline=NAVY)
    d.rectangle([520, 200, 620, 980], fill=GOLD)
    d.rectangle([780, 200, 880, 980], fill=GOLD)
    d.rectangle([500, 900, 900, 980], fill=NAVY)
    d.text((520, 910), "tongue depressor holds the tails", fill=GOLD_LT, font=font(26))
    d.text((80, 420), "Medial\nstirrup", fill=NAVY, font=font(32))
    d.text((1040, 420), "Lateral\nstirrup", fill=NAVY, font=font(32))
    d.text((200, 820), "Rotate 180 degrees onto the wrap before the outer elastic.", fill=SLATE, font=font(28))
    save(im, "bandage_stirrups.png")


def digits():
    im, d = canvas()
    caption(d, 1400, "Leave digits 3 and 4  ·  original teaching figure")
    d.ellipse([420, 280, 980, 980], fill=GOLD_LT, outline=NAVY, width=8)
    d.ellipse([500, 380, 900, 820], fill=SKIN, outline=NAVY, width=6)
    toes = [(540, 220), (660, 160), (790, 160), (910, 220)]
    labels = ["2", "3", "4", "5"]
    for (x, y), lab, i in zip(toes, labels, range(4)):
        fill = GOLD if lab in {"3", "4"} else WHITE
        d.ellipse([x, y, x + 110, y + 220], fill=fill, outline=NAVY, width=6)
        d.text((x + 38, y + 70), lab, fill=NAVY, font=font(42))
    d.text((160, 860), "Tips of 3 and 4 stay visible so you can check color, heat, and swelling.", fill=SLATE, font=font(28))
    save(im, "bandage_digits34.png")


def penrose():
    im, d = canvas()
    caption(d, 1400, "Penrose: dependent exit, not the incision  ·  original teaching figure")
    d.rounded_rectangle([280, 180, 1120, 720], fill=SKIN, outline=NAVY, width=6)
    d.line([(400, 280), (1000, 280)], fill=NAVY, width=10)
    d.text((430, 200), "Primary incision  ·  drain does NOT exit here", fill=RED, font=font(28))
    d.ellipse([620, 360, 780, 620], outline=GREEN, width=8)
    d.text((560, 640), "Pocket", fill=GREEN, font=font(28))
    d.rectangle([680, 700, 760, 940], fill=GOLD, outline=NAVY, width=4)
    d.ellipse([640, 900, 800, 980], fill=GOLD, outline=NAVY, width=4)
    d.text((800, 880), "Single dependent exit", fill=NAVY, font=font(30))
    d.text((160, 980), "Gravity and capillary action along the outside of the latex. Do not fenestrate.", fill=SLATE, font=font(26))
    save(im, "bandage_penrose.png")


def suction():
    im, d = canvas()
    caption(d, 1400, "Closed suction  ·  original teaching figure")
    d.rounded_rectangle([180, 200, 780, 700], fill=SKIN, outline=NAVY, width=6)
    d.line([(280, 300), (680, 300)], fill=NAVY, width=10)
    d.text((300, 220), "Closed incision", fill=NAVY, font=font(28))
    d.ellipse([360, 380, 600, 560], outline=GREEN, width=8)
    for x in range(400, 580, 28):
        d.ellipse([x, 450, x + 12, 470], fill=GREEN)
    d.line([(600, 470), (980, 470), (980, 780)], fill=NAVY, width=10)
    d.ellipse([880, 760, 1160, 980], fill=GOLD_LT, outline=NAVY, width=8)
    d.text((910, 850), "Grenade\nreservoir", fill=NAVY, font=font(30))
    d.text((160, 740), "Fenestrated tubing in the pocket. Air leak kills the vacuum.", fill=SLATE, font=font(28))
    save(im, "bandage_closed_suction.png")


def ehmer():
    im, d = canvas()
    caption(d, 1400, "Ehmer sling  ·  original teaching figure")
    d.ellipse([520, 180, 880, 420], fill=SKIN, outline=NAVY, width=6)
    d.line([(700, 420), (620, 700)], fill=NAVY, width=18)
    d.line([(620, 700), (860, 780)], fill=NAVY, width=18)
    d.line([(860, 780), (920, 960)], fill=NAVY, width=18)
    d.arc([480, 500, 980, 900], start=200, end=20, fill=GOLD, width=18)
    d.text((160, 500), "Hock OUT\n(abduction)", fill=NAVY, font=font(32))
    d.text((980, 640), "Stifle IN\n(internal rotation)", fill=NAVY, font=font(32))
    d.text((200, 960), "Non-weight-bearing hind limb. Coxofemoral luxation conversation.", fill=SLATE, font=font(26))
    save(im, "bandage_ehmer.png")


def velpeau():
    im, d = canvas()
    caption(d, 1400, "Velpeau sling  ·  original teaching figure")
    d.ellipse([560, 140, 900, 420], fill=SKIN, outline=NAVY, width=6)
    d.rounded_rectangle([500, 400, 960, 860], radius=40, fill=SKIN, outline=NAVY, width=6)
    d.polygon([(500, 480), (280, 620), (500, 720)], fill=GOLD, outline=NAVY)
    d.text((160, 500), "Forelimb\nflexed to chest", fill=NAVY, font=font(32))
    d.text((200, 920), "Non-weight-bearing thoracic limb. Shoulder or scapula conversation.", fill=SLATE, font=font(26))
    save(im, "bandage_velpeau.png")


if __name__ == "__main__":
    layers()
    stirrups()
    digits()
    penrose()
    suction()
    ehmer()
    velpeau()
