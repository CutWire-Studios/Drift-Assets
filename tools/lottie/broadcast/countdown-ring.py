import math
import random

from _broadcast2 import *

S = 520
C = (S / 2, S / 2)
F = 30  # one second per loop: the ring runs down once per count
TEXT = (C[0] - 120, C[1] - 84, 240, 168)


def full_arc(r):
    return arc_path(r, -90, 270, C)


def ticks(r0, r1, n, width, color="#FFFFFF", slot=None, opacity=100, name="ticks"):
    return group([polyline([(0, -r0), (0, -r1)]),
                  stroke(color, width=width, slot=slot, opacity=opacity, cap="butt"),
                  repeater(n, rotation=360 / n)], name, position=C)


def modern():
    """Thick round-capped ring runs down clockwise with a bright head dot; the disc bumps on each count."""
    comp = Comp("countdown-ring", S, S, fps=30, frames=F)
    comp.slot("primary", "#FF3B5C")
    comp.slot("background", "#16161C")
    comp.slot("icon", "#FFFFFF")
    R = 188
    run = keys((0, 100, LINEAR), (25, 0, EASE_OUT), (F, 100))
    spin = keys((0, 360, LINEAR), (25, 0, EASE_OUT), (F, 360))
    bump = keys((0, [104, 104], EASE_OUT), (8, [100, 100], HOLD), (25, [100, 100], EASE_IN),
                (27, [96, 96], EASE_OUT), (F, [104, 104]))
    face = rig(comp, "face", C, scale=bump)
    lay(comp, "head", [group([ellipse((16, 16), (C[0], C[1] - R)), fill(slot="icon")], "dot"),
                       group([ellipse((30, 30), (C[0], C[1] - R)), fill(slot="icon", opacity=25)], "halo")],
        C, rotation=spin, parent=face)
    lay(comp, "ring", [group([full_arc(R), trim(end=run), stroke(slot="primary", width=26)], "ring")],
        C, parent=face)
    lay(comp, "track", [group([full_arc(R), stroke(slot="icon", width=26, opacity=14)], "track")], C,
        parent=face)
    lay(comp, "minor ticks", [ticks(226, 236, 60, 3, slot="icon", opacity=45)], C, parent=face)
    lay(comp, "major ticks", [ticks(222, 242, 12, 6, slot="icon")], C, parent=face)
    lay(comp, "disc sheen", [group([ellipse((300, 300), C), gradient_fill(
        [(0, "#FFFFFF", 0.09), (1, "#FFFFFF", 0.0)], (C[0], C[1] - 150), (C[0], C[1] + 60))], "sheen")],
        C, parent=face)
    lay(comp, "disc", [group([ellipse((300, 300), C), fill(slot="background")], "disc"),
                       group([ellipse((500, 500), C), fill(slot="background", opacity=55)], "plate")],
        C, parent=face)
    return comp


def pie_keys(n=24, r=420):
    """Pie wedge from 12 o'clock growing clockwise to a full turn over the loop (one key per frame)."""
    ks = []
    for f in range(F):
        a = 360 * f / (F - 1)
        pts = [C] + [(C[0] + r * math.cos(math.radians(-90 + a * i / (n - 1))),
                      C[1] + r * math.sin(math.radians(-90 + a * i / (n - 1)))) for i in range(n)]
        ks.append((f, bezier(pts), LINEAR))
    return Anim(ks)


def film():
    """Film-leader countdown: crosshair, double circle and a dark sweep wedge, with flicker and dust."""
    comp = Comp("countdown-ring--film", S, S, fps=30, frames=F)
    comp.slot("background", "#8C8A84")
    comp.slot("outline", "#F4F1E8")
    comp.slot("secondary", "#2A2926")
    rng = random.Random(3)
    # dust and hair specks popping for single frames
    for i in range(7):
        t = rng.randrange(0, F - 2)
        x, y = rng.uniform(40, S - 40), rng.uniform(40, S - 40)
        if i % 3 == 0:
            p = [(x, y), (x + rng.uniform(-30, 30), y + rng.uniform(10, 40)), (x + rng.uniform(-20, 20), y + 60)]
            sh = [group([path(bezier(p, [(0, 0)] * 3, [(0, 0)] * 3, closed=False)),
                         stroke("#111111", width=2, opacity=70)], "hair")]
        else:
            sh = [group([ellipse((rng.uniform(4, 9),) * 2, (x, y)), fill("#111111", 75)], "speck")]
        comp.layer(f"dust{i}", sh, ip=t, op=t + 2)
    # vertical scratch drifting
    comp.layer("scratch", [box(0, 0, 2, S, "#FFFFFF", opacity=35)],
               position=keys((0, [150, 0], HOLD), (9, [310, 0], HOLD), (17, [120, 0], HOLD), (24, [380, 0], HOLD),
                             (F, [150, 0])))
    comp.layer("cross", [group([polyline([(20, C[1]), (S - 20, C[1])]), polyline([(C[0], 20), (C[0], S - 20)]),
                                stroke(slot="secondary", width=4, cap="butt")], "cross")])
    comp.layer("rings", [group([ellipse((408, 408), C), stroke(slot="outline", width=10)], "outer"),
                         group([ellipse((352, 352), C), stroke(slot="outline", width=6)], "inner")])
    comp.layer("wedge matte", [group([rect((S - 16, S - 16), C, 34), fill("#FFFFFF")], "gate")])
    comp.layer("wedge", [group([path(pie_keys()), fill(slot="secondary", opacity=55)], "wedge")], matte="alpha")
    comp.layer("hand", [group([polyline([C, (C[0], C[1] - 204)]), stroke(slot="secondary", width=5)], "hand")],
               anchor=C, position=C, rotation=keys((0, 0, LINEAR), (F - 1, 360, HOLD), (F, 360)))
    # frame with rounded film-gate corners, flickering exposure
    flick = keys((0, 100, HOLD), (4, 92, HOLD), (6, 100, HOLD), (13, 88, HOLD), (14, 100, HOLD), (21, 94, HOLD),
                 (23, 100, HOLD), (F, 100))
    comp.layer("grain", [vignette(S, S, 0.6, 0.45, "#1A1814")], opacity=flick)
    comp.layer("gate", [group([rect((S - 16, S - 16), C, 34), fill(slot="background")], "gate")], opacity=flick)
    return comp


def neon():
    """Sixty glowing tick segments switch off one by one around a neon double ring."""
    comp = Comp("countdown-ring--neon", S, S, fps=30, frames=F)
    comp.slot("primary", "#27F2FF")
    comp.slot("accent", "#FF3DDB")
    R = 196
    per = 2 * math.pi * R / 60
    dash = [per * 0.42, per * 0.58, per * 0.21]
    run = keys((0, 100, LINEAR), (25, 0, EASE_OUT), (F, 100))
    pulse = keys((0, 100, EASE_OUT), (6, 70, EASE_IN_OUT), (25, 70, EASE_IN), (F, 100))
    lit = [group([full_arc(R), trim(end=run),
                  stroke("#FFFFFF", width=8, opacity=90, cap="butt", dashes=dash)], "core"),
           group([full_arc(R), trim(end=run), stroke(slot="primary", width=30, cap="butt", dashes=dash)], "tube")]
    for w_, o in ((50, 10), (78, 5)):
        lit.append(group([full_arc(R), trim(end=run), stroke(slot="primary", width=w_, opacity=o)], f"glow{w_}"))
    comp.layer("lit", lit)
    comp.layer("unlit", [group([full_arc(R), stroke(slot="primary", width=30, opacity=13, cap="butt",
                                                     dashes=dash)], "unlit")])
    ring = [ellipse((476, 476), C)]
    comp.layer("outer", glow_strokes(ring, slot="accent", width=5), opacity=pulse)
    comp.layer("inner", glow_strokes([ellipse((316, 316), C)], slot="accent", width=4, core=False),
               opacity=pulse)
    comp.layer("tint", [group([ellipse((316, 316), C), fill("#0B0716", 70)], "tint")])
    return comp


build_asset(CAT, "countdown-ring", "Countdown Ring",
            "Circular countdown timer that runs down once per second, ready to loop under each number. "
            "Put the number in the centre with the text tool.",
            ["countdown", "timer", "ring", "clock", "seconds", "circle", "broadcast"], [
    V("modern", "Modern Ring", modern(), "loop", text_area=TEXT, thumb_t=0.35,
            description="Thick ring with tick marks around a dark disc; a head dot leads the ring down."),
    V("film", "Film Leader", film(), "loop", text_area=TEXT, thumb_t=0.4,
            description="Old film-leader countdown: crosshair, double circle and a sweeping wedge with dust and flicker."),
    V("neon", "Neon Ticks", neon(), "loop", text_area=TEXT, thumb_t=0.35, bg="0e0b18",
            description="Sixty glowing tick segments switch off one by one inside a neon double ring."),
])
