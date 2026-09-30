"""Warning triangle with an exclamation mark built from shapes, pulsing (seamless loop)."""
import math

from _callouts2 import *

W, H = 340, 320
N = 60
C = (W / 2, 172)  # centroid-ish of the triangle
S = 236  # side length


def tri(side=S, c=C):
    h = side * math.sqrt(3) / 2
    return [(c[0], c[1] - h * 2 / 3), (c[0] + side / 2, c[1] + h / 3), (c[0] - side / 2, c[1] + h / 3)]


def tri_outline(side=S, c=C, r=26):
    t = tri(side, c)
    return dense(fillet([lerp(t[2], t[0], 0.5)] + [t[0], t[1], t[2]] + [lerp(t[2], t[0], 0.5)], r, 10))


def beat(lo=100, hi=108):
    """Two heartbeat-like pulses per loop."""
    keys = []
    for c in (0, 30):
        keys += [(c, [lo, lo], EASE_OUT), (c + 5, [hi, hi], SETTLE), (c + 16, [lo, lo], HOLD)]
    return anim(keys + [(N, [lo, lo])])


def bar_shape():
    """Tapered rounded exclamation bar, (0, 0) at the centre of the mark."""
    v = [(-14, -50), (0, -60), (14, -50), (8, 10), (0, 17), (-8, 10)]
    i = [(0, 8), (-9, 0), (0, -8), (0, 0), (6, 0), (0, 0)]
    o = [(0, -8), (9, 0), (0, 8), (0, 0), (-6, 0), (0, 0)]
    return path(bezier(v, i, o))


def ripples(comp, slot, width):
    for c in (0, 30):
        comp.layer(f"ripple{c}", [clean_line(tri_outline(S, (0, 0)), width, slot, name="r")],
                   position=C, ip=c, op=c + 24, scale=anim([(c, [100, 100], DECEL), (c + 24, [135, 135])]),
                   opacity=anim([(c, 70, EASE_IN), (c + 24, 0)]))


def make(style):
    comp = Comp(f"warning-triangle-pulse--{style}", W, H, frames=N)
    mark = (C[0], C[1] + 6)
    if style == "solid":
        comp.slot("primary", "#FFC400")
        comp.slot("icon", INK)
        comp.layer("mark", [group([bar_shape(), fill(slot="icon")], "bar"),
                            group([ellipse((28, 28), (0, 38)), fill(slot="icon")], "dot")],
                   position=mark, scale=beat(100, 112))
        body = P(tri_outline(S, (0, 0)), True)
        comp.layer("tri", [group([body, stroke(INK, 10, slot="icon"), fill(slot="primary")], "t")],
                   position=C, scale=beat())
        comp.layer("tri-shadow", [group([body, fill("#000000", 28)], "s", position=(0, 9))],
                   position=C, scale=beat())
        ripples(comp, "primary", 8)
    elif style == "neon":
        comp.slot("primary", "#FF3B30")
        glow = anim([(0, 70, EASE_OUT), (5, 100, SETTLE), (16, 70, HOLD), (30, 70, EASE_OUT), (35, 100, SETTLE),
                     (46, 70, HOLD), (60, 70)])
        comp.layer("mark", [neon_line([(0, -52), (0, 8)], 12, name="bar"),
                            neon_line(ellipse_pts((0, 36), 1.5, 1.5, n=12), 14, closed=True, name="dot")],
                   position=mark, scale=beat(100, 106), opacity=glow)
        comp.layer("tri", [neon_line(tri_outline(S, (0, 0)), 10, closed=True)], position=C, scale=beat(100, 104),
                   opacity=glow)
    else:
        comp.slot("primary", "#FFC400")
        comp.slot("outline", INK)
        line = wobble(closed_loop(tri_outline(S, (0, 0)), 0.05, 3), 2.5, seed=3, freq=2)
        bar = dense([(1, -50), (-1, 8)])
        dot = closed_loop(ellipse_pts((0, 37), 5, 5, start=0), 0.2, 1)
        comp.layer("mark", [hand_static(bar, 22, "outline", seed=4, frames=N, taper=(0.1, 0.4), mins=(0.9, 0.55),
                                        wob=0.03, color=INK, name="bar"),
                            hand_static(dot, 18, "outline", seed=5, frames=N, taper=(0.1, 0.1), mins=(0.9, 0.9),
                                        wob=0.02, color=INK, name="dot")], position=mark, scale=beat(100, 110))
        comp.layer("tri", [hand_static(line, 12, "outline", seed=6, frames=N, taper=(0.03, 0.06), mins=(0.6, 0.5),
                                       wob=0.1, color=INK, name="line"),
                           group([P(tri_outline(S - 14, (0, 0)), True), fill(slot="primary")], "fill")],
                   position=C, scale=beat(), rotation=anim([(0, 0, EASE_OUT), (5, -3, SETTLE), (16, 0, HOLD),
                                                            (30, 0, EASE_OUT), (35, 3, SETTLE), (46, 0, HOLD),
                                                            (60, 0)]))
    return comp


build_asset(CATEGORY, "warning-triangle-pulse", "Warning Triangle Pulse",
            "A warning triangle with an exclamation mark that keeps pulsing to grab attention; loops "
            "seamlessly.",
            ["warning", "caution", "alert", "triangle", "exclamation", "danger", "loop"], [
    Variant("solid", "Solid", make("solid"), "loop", thumb_t=0.45,
            description="Yellow rounded triangle with an ink border that beats and sends out ripples."),
    Variant("neon", "Neon", make("neon"), "loop", thumb_t=0.09,
            description="Red neon sign outline whose glow swells on each beat."),
    Variant("hand", "Hand-Drawn", make("hand"), "loop", thumb_t=0.45, bg="e8e8ee",
            description="Marker-drawn doodle with a boiling line that wobbles on each beat."),
])
