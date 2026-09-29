"""Zigzag arrow that zaps across in sharp switchbacks."""
from _callouts2 import *

W, H = 580, 320
N = 36
PTS = dense(fillet([(46, 236), (150, 96), (226, 226), (330, 88), (404, 214), (522, 100)], 22))


def make(style):
    comp = Comp(f"arrow-zigzag--{style}", W, H, frames=N)
    comp.slot("primary", {"hand": "#FF2D2D", "clean": "#FFD21F", "neon": "#29E6FF"}[style])
    width = {"hand": 20, "clean": 16, "neon": 11}[style]
    arrow(comp, PTS, style, 1, 18, width, seed=9)
    return comp


build_asset(CATEGORY, "arrow-zigzag", "Zigzag Arrow",
            "A zigzag arrow that zaps across in quick switchbacks and ends pointing up and to the right.",
            ["arrow", "zigzag", "lightning", "pointer", "callout", "draw-on"], [
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Quick marker zigzag with a flicked-on arrowhead."),
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99,
            description="Even vector zigzag with a rounded solid arrowhead."),
    Variant("neon", "Neon", make("neon"), "intro-hold", thumb_t=0.99,
            description="Glowing neon tube that flickers on as it zaps across."),
])
