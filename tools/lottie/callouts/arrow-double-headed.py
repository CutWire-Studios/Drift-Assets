"""Gentle arc with an arrowhead at each end, drawn on."""
from _callouts2 import *

W, H = 620, 260
N = 36
ARC = dense(cubic((64, 190), (200, 60), (420, 60), (556, 190), 90))


def make(style):
    comp = Comp(f"arrow-double-headed--{style}", W, H, frames=N)
    comp.slot("primary", {"hand": "#FF2D2D", "clean": "#FFFFFF", "neon": "#FF3DF2"}[style])
    width = {"hand": 20, "clean": 15, "neon": 13}[style]
    arrow(comp, ARC, style, 2, 16, width, seed=3, both=True)
    return comp


build_asset(CATEGORY, "arrow-double-headed", "Double-Headed Arrow",
            "A gently arched arrow with a head at each end that draws on; use it to "
            "link two things or show a range.",
            ["arrow", "double", "two-way", "compare", "callout", "draw-on"], [
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Marker arc with flicked-on heads at both ends."),
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99,
            description="Even white vector arc with rounded solid heads."),
    Variant("neon", "Neon", make("neon"), "intro-hold", thumb_t=0.99,
            description="Glowing neon arc that flickers on, with chevron heads."),
])
