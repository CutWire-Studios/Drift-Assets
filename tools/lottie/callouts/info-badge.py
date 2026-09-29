"""Circular info badge with an "i" built from a dot and a bar."""
from _callouts2 import *

W = H = 260
N = 30
C = (W / 2, H / 2)
R = 100


def make(style):
    comp = Comp(f"info-badge--{style}", W, H, frames=N)
    comp.slot("primary", "#2D8CFF")
    if style == "solid":
        comp.slot("icon", "#FFFFFF")
        comp.layer("dot", [group([ellipse((34, 34)), fill(slot="icon")], "d")],
                   position=anim([(6, [C[0], C[1] - 120], (0.5, 0.0, 0.9, 0.5)), (12, [C[0], C[1] - 46], SETTLE),
                                  (16, [C[0], C[1] - 56], (0.4, 0.0, 0.9, 0.6)), (20, [C[0], C[1] - 46])]),
                   scale=anim([(11, [100, 100], SETTLE), (12, [125, 75], SETTLE), (16, [95, 105], SETTLE),
                               (20, [120, 82], SETTLE), (24, [100, 100])]), ip=6)
        comp.layer("bar", [group([rect((30, 84), (0, -42), 12), fill(slot="icon")], "b")],
                   position=(C[0], C[1] + 64), scale=anim([(3, [100, 0], SPRING), (13, [100, 100])]), ip=3)
        comp.layer("disc", [group([ellipse((2 * R, 2 * R)), fill(slot="primary")], "d")], position=C,
                   scale=pop(0, 12, 116))
        comp.layer("shadow", [group([ellipse((2 * R, 2 * R)), fill("#000000", 28)], "s")],
                   position=(C[0], C[1] + 8), scale=pop(0, 12, 116))
    elif style == "outline":
        comp.layer("dot", [group([ellipse((30, 30)), fill(slot="primary")], "d")], position=(C[0], C[1] - 48),
                   scale=pop(16, 10, 150), ip=16)
        comp.layer("bar", [clean_line([(C[0], C[1] - 12), (C[0], C[1] + 50)], 24, t0=8, t1=18, ease=SETTLE)])
        comp.layer("ring", [group([ellipse((2 * R - 14, 2 * R - 14)), trim(0, draw(0, 16)),
                                   stroke(slot="primary", width=14)], "r")], position=C, rotation=-90)
    else:
        pts = wobble(closed_loop(ellipse_pts(C, R - 8, R - 12, start=-110), 0.1, 7), 3, seed=6, freq=2)
        bar = dense([(C[0] + 2, C[1] - 12), (C[0] - 2, C[1] + 52)])
        dot = closed_loop(ellipse_pts((C[0] + 1, C[1] - 48), 7, 6, start=0), 0.2, 2)
        emit(comp, [hand_line(pts, 1, 15, 15, seed=4, chunks=2, taper=(0.04, 0.12), mins=(0.5, 0.25)),
                    hand_line(bar, 15, 21, 22, seed=5, taper=(0.1, 0.2), mins=(0.85, 0.75), wob=0.02),
                    hand_line(dot, 22, 26, 17, seed=6, taper=(0.1, 0.1), mins=(0.9, 0.9), wob=0.02)])
    return comp


build_asset(CATEGORY, "info-badge", "Info Badge",
            "Round information badge with an \"i\" made of a dot and a bar; pop it next to a tip or "
            "note.",
            ["info", "information", "badge", "tip", "note", "icon", "help"], [
    Variant("solid", "Solid", make("solid"), "intro-hold", thumb_t=0.99,
            description="Blue disc pops in, the bar grows up and the dot drops in with a bounce."),
    Variant("outline", "Outline", make("outline"), "intro-hold", thumb_t=0.99,
            description="Ring draws round, then the bar strokes on and the dot pops."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Marker circle and \"i\" scribbled on in three quick strokes."),
])
