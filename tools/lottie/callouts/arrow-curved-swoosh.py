"""Curved swoosh arrow that dips and sweeps up to the right as it draws on."""
from _callouts2 import *

W, H = 560, 380
N = 36
PTS = dense(cubic((58, 92), (96, 360), (360, 372), (500, 150), 80))


def make(style):
    comp = Comp(f"arrow-curved-swoosh--{style}", W, H, frames=N)
    comp.slot("primary", "#FF2D2D")
    if style == "bold":
        comp.slot("outline", INK)
    width = {"hand": 22, "clean": 17, "bold": 34}[style]
    arrow(comp, PTS, style, 1, 17, width, seed=4)
    return comp


build_asset(CATEGORY, "arrow-curved-swoosh", "Curved Swoosh Arrow",
            "A long curved arrow that swoops down and sweeps up to the right as it draws on; point it "
            "at whatever you want viewers to notice.",
            ["arrow", "curved", "swoosh", "pointer", "callout", "draw-on"], [
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Tapered marker stroke with a flicked-on arrowhead."),
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99,
            description="Even vector line with a rounded solid arrowhead that pops on."),
    Variant("bold", "Comic Bold", make("bold"), "intro-hold", thumb_t=0.99, bg="e8e8ee",
            description="Chunky tapered comic arrow with an ink outline and hard shadow."),
])
