"""Round numbered-step badge (no digit drawn: the number goes in the text area)."""
import math

from _callouts2 import *

W = H = 280
N = 30
C = (W / 2, H / 2)
R = 100
TEXT = (C[0] - 64, C[1] - 64, 128, 128)


def sparks(comp, t, slot):
    items = []
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        p0 = (math.cos(a) * (R + 10), math.sin(a) * (R + 10))
        p1 = (math.cos(a) * (R + 30), math.sin(a) * (R + 30))
        items.append(group([P([p0, p1]), trim(anim([(t + 2, 0, SETTLE), (t + 10, 100)]),
                                             anim([(t, 0, SETTLE), (t + 6, 100)])),
                            stroke(slot=slot, width=6)], f"s{k}"))
    comp.layer("sparks", items, position=C, ip=t, op=t + 11)


def make(style):
    comp = Comp(f"number-badge-circle--{style}", W, H, frames=N)
    comp.slot("primary", "#FF2D2D")
    if style == "solid":
        comp.slot("outline", "#FFFFFF")
        sparks(comp, 6, "primary")
        comp.layer("badge", [group([ellipse((2 * R - 26, 2 * R - 26)), stroke(slot="outline", width=5)], "ring"),
                             group([ellipse((2 * R, 2 * R)), fill(slot="primary")], "disc")],
                   position=C, scale=pop(0, 14, 118), rotation=anim([(0, -30, SETTLE), (14, 0)]))
        comp.layer("shadow", [group([ellipse((2 * R, 2 * R)), fill("#000000", 30)], "s")],
                   position=(C[0], C[1] + 8), scale=pop(0, 14, 118))
    elif style == "outline":
        comp.layer("ring", [group([ellipse((2 * R - 12, 2 * R - 12)), trim(0, draw(0, 16), anim([(0, -90, DRAW),
                                                                                             (16, 0)])),
                                   stroke(slot="primary", width=14)], "r")], position=C, rotation=-90)
        comp.layer("inner", [group([ellipse((2 * R - 46, 2 * R - 46)), stroke(slot="primary", width=4)], "f")],
                   position=C, scale=pop(10, 12, 112), ip=10)
        comp.layer("orbit", [group([ellipse((18, 18)), fill(slot="primary")], "d", position=(0, -R + 6))],
                   position=C, rotation=anim([(0, -180, DRAW), (16, 0)]),
                   scale=anim([(14, [100, 100], SETTLE), (20, [0, 0])]), op=20)
    else:
        # two loose loops, the second a little smaller and off-centre, like a quick double circle
        pts = [(C[0] + (R - 8 - 10 * u) * math.cos(a) + 5 * u, C[1] + (R - 14 - 8 * u) * math.sin(a) - 3 * u)
               for u, a in ((i / 300, math.radians(-100 + 690 * i / 300)) for i in range(301))]
        pts = wobble(dense(pts), 2.5, seed=3, freq=3)
        emit(comp, [hand_line(pts, 1, 20, 13, seed=4, chunks=3, taper=(0.03, 0.12), mins=(0.5, 0.2))])
    return comp


build_asset(CATEGORY, "number-badge-circle", "Number Badge Circle",
            "Round step badge for numbered lists and tutorials; type the step number in the middle.",
            ["number", "badge", "step", "circle", "tutorial", "list", "counter"], [
    Variant("solid", "Solid", make("solid"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Solid red disc with an inner white ring; it spins in with a spark burst."),
    Variant("outline", "Outline", make("outline"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Thick ring drawn round by a dot, then a thin inner ring pops in."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Quick double-loop marker circle scribbled round."),
])
