import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"

LINK = ("M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1z"
        "M8 13h8v-2H8v2z"
        "M17 7h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z")


def link_parts(size=240, cx=160, cy=160):
    s = size / 24
    ps = svg_path(LINK, s, (cx - 12 * s, cy - 12 * s))
    return [path(p, f"part{i}") for i, p in enumerate(ps)]


def snap():
    F = 60
    comp = Comp("link-icon", 320, 320, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#3D8BFF")
    L, B, R_ = link_parts()
    ease = (0.2, 0.0, 0.1, 1.0)
    comp.layer("left", [group([L, fill(slot="icon")], "l")], position=Anim([(0, [-80, 0], ease), (14, [0, 0])]),
               opacity=fade(0, 8))
    comp.layer("right", [group([R_, fill(slot="icon")], "r")], position=Anim([(0, [80, 0], ease), (14, [0, 0])]),
               opacity=fade(0, 8))
    comp.layer("bar", [group([B, fill(slot="accent")], "b")], anchor=(160, 160), position=(160, 160),
               scale=Anim([(12, [0, 100], OVERSHOOT), (22, [100, 100])]))
    comp.layer("pop", [group([ellipse((280, 280), (160, 160)), stroke(slot="accent", width=6)], "ring",
                             anchor=(160, 160), position=(160, 160),
                             scale=Anim([(12, [60, 60], EASE_OUT), (30, [110, 110])]),
                             opacity=Anim([(12, 70, EASE_OUT), (30, 0)]))])
    return comp


def tilted():
    F = 60
    comp = Comp("link-icon", 320, 320, frames=F)
    comp.slot("icon", "#FFFFFF")
    L, B, R_ = link_parts(220)
    comp.layer("chain", [group([L, B, R_, fill(slot="icon")], "chain")], anchor=(160, 160), position=(160, 160),
               rotation=Anim([(0, -90, OVERSHOOT), (18, -45, HOLD), (F, -45)]),
               scale=Anim([(0, [0, 0], OVERSHOOT), (16, [100, 100])]))
    return comp


build_asset(CAT, "link-icon", "Link Icon",
            "Chain-link icon for 'link in bio' and 'link in description' moments: two halves snap together with a "
            "ring pop, or a tilted chain spins in.",
            ["link", "chain", "url", "bio", "description", "website", "hyperlink", "share"], [
    Variant("snap", "Snap Together", snap(), "intro-hold", thumb_t=0.95, bg="6a7087"),
    Variant("tilted", "Tilted Chain", tilted(), "intro-hold", thumb_t=0.95, bg="6a7087"),
])
