import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

def check(cx, cy, s, t0, t1, slot="icon", w=None):
    pts = [(cx - 0.48 * s, cy + 0.02 * s), (cx - 0.1 * s, cy + 0.38 * s), (cx + 0.5 * s, cy - 0.32 * s)]
    return group([polyline(pts), stroke(slot=slot, width=w or s * 0.24, join="round"),
                  trim(0, Anim([(t0, 0, EASE_OUT), (t1, 100)]))], "check")


def badge(kind, F=75):
    comp = Comp("verified-badge", 300, 300, frames=F)
    comp.slot("primary", "#1D9BF0")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FFD60A")
    cx = cy = 150
    if kind == "scalloped":
        shape = star(8, 124, 108, (cx, cy), 0, 55, 55) if False else star(10, 128, 112, (cx, cy), 0, 100, 100)
    else:
        shape = ellipse((236, 236), (cx, cy))
    comp.layer("check", [check(cx, cy, 120, 12, 28)])
    comp.layer("badge", [group([shape, fill(slot="primary")], "badge")], anchor=(cx, cy), position=(cx, cy),
               scale=Anim([(0, [0, 0], OVERSHOOT), (14, [100, 100])]),
               rotation=Anim([(0, -90, OVERSHOOT), (16, 0)]))
    comp.layer("shine", [group([ellipse((250, 250), (cx, cy)), stroke(slot="primary", width=6)], "ring",
                               anchor=(cx, cy), position=(cx, cy), scale=Anim([(12, [70, 70], EASE_OUT), (40, [125, 125])]),
                               opacity=Anim([(12, 80, EASE_OUT), (40, 0)]))])
    return comp


def gold(F=75):
    comp = badge("scalloped", F)
    comp.slots["primary"]["p"]["k"] = hex_color("#E8B923")
    return comp


build_asset(CAT, "verified-badge", "Verified Badge",
            "Verified checkmark badge that spins in and draws its tick: a scalloped seal (X / Instagram style), a "
            "round badge, and a gold seal.",
            ["verified", "checkmark", "badge", "blue tick", "official", "social", "creator", "seal"], [
    Variant("scalloped", "Scalloped Seal", badge("scalloped"), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
    Variant("round", "Round", badge("round"), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
    Variant("gold", "Gold Seal", gold(), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
])
