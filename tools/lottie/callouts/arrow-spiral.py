"""Loop-de-loop arrow: swings into a curl and shoots off to the right."""
import math

from _callouts2 import *

W, H = 580, 400
N = 42


def spiral():
    a, b = 62, 118
    pts = []
    for i in range(241):
        t = -1.12 * math.pi + (2.3 * math.pi) * i / 240
        pts.append((a * t - b * math.sin(t), -b * math.cos(t) * 0.95))
    x0, y0, x1, y1 = bbox(pts)
    return dense(offset(pts, W / 2 - (x0 + x1) / 2 - 8, H / 2 - (y0 + y1) / 2 + 6))


PTS = spiral()


def make(style):
    comp = Comp(f"arrow-spiral--{style}", W, H, frames=N)
    comp.slot("primary", {"hand": "#FF2D2D", "clean": "#FFD21F", "dashed": "#FFFFFF"}[style])
    width = {"hand": 19, "clean": 15, "dashed": 12}[style]
    arrow(comp, PTS, style, 1, 24, width, seed=5)
    return comp


build_asset(CATEGORY, "arrow-spiral", "Spiral Arrow",
            "A playful loop-de-loop arrow that curls round and shoots off to the right.",
            ["arrow", "spiral", "loop", "curl", "pointer", "callout"], [
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Marker loop with a flicked-on arrowhead."),
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99,
            description="Even vector loop with a rounded solid arrowhead."),
    Variant("dashed", "Dashed", make("dashed"), "intro-hold", thumb_t=0.99,
            description="Dashed path loop, like a route on a map, with an open chevron head."),
])
