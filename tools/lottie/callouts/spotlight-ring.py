"""Glowing ring that pulses around a subject (seamless loop)."""
from _callouts2 import *

W = H = 440
N = 60
C = (W / 2, H / 2)
R = 150


def pulse(lo=100, hi=106):
    return anim([(0, [lo, lo], EASE_IN_OUT), (15, [hi, hi], EASE_IN_OUT), (30, [lo, lo], EASE_IN_OUT),
                 (45, [hi, hi], EASE_IN_OUT), (60, [lo, lo])])


def ripple(comp, slot, width, t, name):
    comp.layer(name, [group([ellipse((2 * R, 2 * R)), stroke(slot=slot, width=anim([(t, width, EASE_OUT),
                                                                                     (t + 26, 1)]))], "r")],
               position=C, ip=t, op=t + 27,
               scale=anim([(t, [100, 100], DECEL), (t + 26, [132, 132])]),
               opacity=anim([(t, 70, EASE_IN), (t + 26, 0)]))


def make(style):
    comp = Comp(f"spotlight-ring--{style}", W, H, frames=N)
    comp.slot("primary", {"glow": "#FFD21F", "dashed": "#FFFFFF", "hand": "#FF2D2D"}[style])
    if style == "glow":
        ring = [ellipse((2 * R, 2 * R))]
        glow = anim([(0, 55, EASE_IN_OUT), (15, 100, EASE_IN_OUT), (30, 55, EASE_IN_OUT), (45, 100, EASE_IN_OUT),
                     (60, 55)])
        comp.layer("core", [group(ring + [stroke("#FFFFFF", 4, opacity=85)], "core"),
                            group(ring + [stroke(slot="primary", width=12)], "tube")], position=C, scale=pulse())
        comp.layer("glow", [group(ring + [stroke(slot="primary", width=w, opacity=o)], f"g{w}")
                            for w, o in [(26, 40), (44, 18), (70, 8)]], position=C, scale=pulse(), opacity=glow)
        for t in (-10, 20):  # ripples; the one at -10 wraps round to 50
            ripple(comp, "primary", 8, t % N, f"ripple{t}")
        comp.layer("ripple-wrap", [group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=anim(
            [(-10, 8, EASE_OUT), (16, 1)]))], "r")], position=C, ip=0, op=17,
            scale=anim([(-10, [100, 100], DECEL), (16, [132, 132])]), opacity=anim([(-10, 70, EASE_IN), (16, 0)]))
    elif style == "dashed":
        n = 28
        per = 2 * 3.14159265 * R / n
        comp.layer("dashes", [group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=10, cap="round",
                                                                     dashes=[per * 0.45, per * 0.55])], "d")],
                   position=C, rotation=anim([(0, 0, LINEAR), (60, 360 / n * 4)]), scale=pulse(100, 104))
        comp.layer("inner", [group([ellipse((2 * R - 44, 2 * R - 44)), stroke(slot="primary", width=4,
                                                                            opacity=70)], "i")],
                   position=C, scale=pulse(100, 96))
        for k in range(4):
            import math
            a = math.radians(k * 90)
            p0 = (math.cos(a) * (R + 16), math.sin(a) * (R + 16))
            p1 = (math.cos(a) * (R + 40), math.sin(a) * (R + 40))
            comp.layer(f"tick{k}", [clean_line([p0, p1], 8)], position=C, scale=pulse(100, 108))
    else:
        pts = closed_loop(ellipse_pts((0, 0), R, R * 0.94, start=-120), 0.1, 10)
        pts = wobble(pts, 3, seed=4, freq=2)
        comp.layer("ring", [hand_static(pts, 18, seed=6, frames=N, every=5, amp=2.2, taper=(0.04, 0.12),
                                        mins=(0.5, 0.2), wob=0.14)], position=C, scale=pulse(100, 105),
                   rotation=-6)
        for t in (5, 35):
            comp.layer(f"echo{t}", [hand_static(pts, 10, seed=6, taper=(0.04, 0.12), mins=(0.5, 0.2), wob=0.14)],
                       position=C, ip=t, op=t + 22, rotation=-6,
                       scale=anim([(t, [104, 104], DECEL), (t + 22, [126, 126])]),
                       opacity=anim([(t, 50, EASE_IN), (t + 22, 0)]))
    return comp


build_asset(CATEGORY, "spotlight-ring", "Spotlight Ring",
            "A ring that keeps pulsing around a subject to draw the eye to it; place it over whatever "
            "you want to spotlight.",
            ["spotlight", "ring", "circle", "pulse", "highlight", "focus", "loop"], [
    Variant("glow", "Glow", make("glow"), "loop", thumb_t=0.25,
            description="Glowing ring that breathes and sends out soft ripples."),
    Variant("dashed", "Dashed", make("dashed"), "loop", thumb_t=0.25,
            description="Slowly turning dashed ring with an inner ring and four ticks."),
    Variant("hand", "Hand-Drawn", make("hand"), "loop", thumb_t=0.5,
            description="Boiling marker circle that pulses and echoes outwards."),
])
