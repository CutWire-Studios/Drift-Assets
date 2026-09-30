"""Thought cloud with trailing dots, popping in dot by dot."""
import math

from _callouts2 import *

W, H = 540, 430
N = 40
C = (296, 170)
RX, RY = 216, 136
BUMPS = 11
DOTS = [((150, 322), 28), ((104, 366), 19), ((72, 398), 12)]  # (centre, radius), cloud end first
TEXT = (C[0] - 150, C[1] - 70, 300, 140)


def cloud():
    pts = []
    n = 480
    for i in range(n):
        t = 2 * math.pi * i / n - math.pi / 2
        s = 0.86 + 0.16 * abs(math.sin(BUMPS * (t + math.pi / 2) / 2)) ** 0.6
        pts.append((C[0] + RX * s * math.cos(t), C[1] + RY * s * math.sin(t)))
    return dense(pts + [pts[0]])[:-1]


def make(style):
    comp = Comp(f"thought-bubble-cloud--{style}", W, H, frames=N)
    t = 0
    for k, (c, r) in enumerate(DOTS[::-1]):
        bubble(comp, ellipse_pts(c, r, r * 0.92, start=-120), style, c, t0=t, seed=k + 2,
               width=8 if style != "clean" else None, name=f"dot{k}", dur=6)
        t += 4
    out = cloud()
    bubble(comp, out, style, DOTS[0][0], t0=t, seed=4, width=10 if style == "hand" else 9,
           draw_start=(C[0] - RX, C[1]))
    return comp


build_asset(CATEGORY, "thought-bubble-cloud", "Thought Bubble Cloud",
            "A fluffy thought cloud whose trail of dots pops in one by one before the cloud; type "
            "the thought inside it.",
            ["thought", "bubble", "cloud", "thinking", "idea", "comic", "callout"], [
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Flat white cloud and dots with a soft shadow, squashing in."),
    Variant("bold", "Comic", make("bold"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="e8e8ee",
            description="Comic cloud with a thick ink outline and a hard red shadow."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="e8e8ee",
            description="Marker-drawn cloud and dots, drawn on in sequence."),
])
