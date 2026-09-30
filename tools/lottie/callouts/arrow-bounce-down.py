"""Downward arrow that keeps bouncing on its target (seamless loop, two bounces)."""
import math

from _callouts2 import *

W, H = 240, 360
N = 60
CYCLE = 30
TIP = (W / 2, 306)
JUMP = 58
FALL = (0.55, 0.0, 0.9, 0.55)
RISE = (0.1, 0.45, 0.4, 1.0)


def bounce_keys():
    """Each cycle starts at the top of the jump, lands at +12 and springs back up."""
    pos, sc = [], []
    x, y = TIP
    for c in range(0, N, CYCLE):
        pos += [(c, [x, y - JUMP], FALL), (c + 12, [x, y], LINEAR), (c + 17, [x, y], RISE)]
        sc += [(c, [100, 100], EASE_IN), (c + 6, [100, 100], EASE_IN), (c + 11, [93, 110], LINEAR),
               (c + 12, [118, 84], SETTLE), (c + 17, [93, 108], SETTLE), (c + 24, [100, 100], LINEAR)]
    pos.append((N, [x, y - JUMP]))
    sc.append((N, [100, 100]))
    return anim(pos), anim(sc)


def impact(slot):
    """Little comic impact ticks either side of the tip on each landing."""
    items = []
    for c in range(0, N, CYCLE):
        t = c + 12
        for side in (-1, 1):
            for k in range(2):
                p0 = (TIP[0] + side * (46 + k * 8), TIP[1] - 8 - k * 18)
                p1 = (p0[0] + side * 26, p0[1] - 10 - k * 6)
                items.append(group([P([p0, p1]),
                                    trim(anim([(t + 1, 0, SETTLE), (t + 9, 100)]), anim([(t, 0, SETTLE), (t + 5, 100)])),
                                    stroke(INK, 7, slot=slot)], f"tick{c}{side}{k}"))
    return items


def make(style):
    comp = Comp(f"arrow-bounce-down--{style}", W, H, frames=N)
    comp.slot("primary", "#FF2D2D")
    pos, sc = bounce_keys()
    holder = comp.null("bounce", position=pos, scale=sc)
    if style == "clean":
        comp.slot("outline", "#FFFFFF")
        comp.layer("head", [clean_line(chevron(78, 44), 26, "primary")], parent=holder, rotation=90, position=(0, -4))
        comp.layer("shaft", [clean_line([(0, -212), (0, -20)], 26, "primary")], parent=holder)
    elif style == "hand":
        shaft = dense([(4, -214), (-2, -130), (1, -16)], smooth=True)
        left = dense([(-66, -88), (-30, -44), (0, -6)], smooth=True)
        right = dense([(2, -6), (34, -46), (70, -92)], smooth=True)
        comp.layer("ink", [hand_static(right, 24, seed=3, frames=N, taper=(0.1, 0.35), mins=(0.8, 0.5), wob=0.03,
                                       name="right"),
                           hand_static(left, 24, seed=2, frames=N, taper=(0.3, 0.1), mins=(0.5, 0.8), wob=0.03,
                                       name="left"),
                           hand_static(shaft, 24, seed=1, frames=N, taper=(0.1, 0.15), mins=(0.5, 0.7), wob=0.05,
                                       name="shaft")], parent=holder)
    else:  # bold block arrow
        comp.slot("outline", INK)
        pts = [(-27, -214), (27, -214), (27, -96), (74, -96), (0, 0), (-74, -96), (-27, -96)]
        shape = [path(bezier(pts, closed=True)), round_corners(9)]
        shine = [group([P([(-12, -196), (-12, -104)]), stroke("#FFFFFF", 9, opacity=55)], "shine")]
        comp.layer("arrow", shine + comic(shape, "primary", width=11, shadow=(10, 8)), parent=holder)
        comp.layer("impact", impact("outline"))
    return comp


build_asset(CATEGORY, "arrow-bounce-down", "Bouncing Down Arrow",
            "A downward arrow that keeps bouncing on the spot, squashing as it lands; place its tip "
            "right above the thing to look at.",
            ["arrow", "down", "bounce", "pointer", "look-here", "loop"], [
    Variant("clean", "Clean", make("clean"), "loop", thumb_t=0.45,
            description="Round-capped vector arrow with a squash-and-stretch bounce."),
    Variant("hand", "Hand-Drawn", make("hand"), "loop", thumb_t=0.45,
            description="Marker-drawn arrow whose line boils like frame-by-frame animation."),
    Variant("bold", "Comic Block", make("bold"), "loop", thumb_t=0.45, bg="e8e8ee",
            description="Chunky block arrow with an ink outline, shadow and impact ticks on each landing."),
])
