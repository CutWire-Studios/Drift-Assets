import math
import random

from _common import (ANTICIPATE, HOLD, LINEAR, Comp, anim, bezier, fill, group, path,
                     stroke, trim)
import _callouts2 as c2
from drift_lottie import Variant, build_asset

W = H = 600
C = (W / 2, H / 2)
TEXT = (int(C[0]) - 95, int(C[1]) - 60, 190, 120)


def bold():
    comp = Comp("impact-burst-comic", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D")
    comp.slot("secondary", "#FFD21F")
    comp.slot("outline", "#141414")


    def burst(spikes, r_out, r_in, seed, twist=0.0, spread=(0.78, 1.12)):
        """Irregular comic starburst centred on (0, 0): uneven spike lengths and spacing."""
        rnd = random.Random(seed)
        pts = []
        for i in range(spikes):
            a = (i + rnd.uniform(-0.18, 0.18)) / spikes * 2 * math.pi + twist
            ro = r_out * rnd.uniform(*spread)
            pts.append((ro * math.cos(a), ro * math.sin(a)))
            b = (i + 0.5 + rnd.uniform(-0.12, 0.12)) / spikes * 2 * math.pi + twist
            ri = r_in * rnd.uniform(0.9, 1.06)
            pts.append((ri * math.cos(b), ri * math.sin(b)))
        return bezier(pts)


    red = burst(14, 226, 150, seed=3, twist=-0.1, spread=(0.8, 1.12))
    yellow = burst(12, 150, 104, seed=8, twist=0.12, spread=(0.82, 1.1))


    def burst_layer(name, shape, slot, delay, spin):
        d = delay
        sc = anim([(d, [0, 0], (0.2, 0.0, 0.3, 1.0)), (d + 5, [118, 118], EASE_SETTLE),
                   (d + 8, [95, 95], EASE_SETTLE), (d + 11, [100, 100], HOLD), (28, [100, 100]),
                   (30, [108, 108], ANTICIPATE), (35, [0, 0])])
        rot = anim([(d, spin), (d + 9, 0, HOLD), (28, 0, (0.4, 0.0, 0.8, 0.6)), (35, -spin * 0.6)])
        items = [
            group([path(shape, "burst"), stroke(slot="outline", width=9, join="miter"),
                   fill(slot=slot)], "burst"),
            group([path(shape, "shadow"), fill(slot="outline")], "shadow", position=(10, 12)),
        ]
        return comp.layer(name, items, parent=shake, scale=sc, rotation=rot, ip=d)


    EASE_SETTLE = (0.3, 0.0, 0.4, 1.0)

    # a short decaying shake right after the hit
    jit = random.Random(5)
    keys = [(0, list(C), LINEAR)]
    for f in range(4, 13):
        amp = 11 * (1 - (f - 4) / 9)
        keys.append((f, [C[0] + jit.uniform(-amp, amp), C[1] + jit.uniform(-amp, amp)], LINEAR))
    keys.append((14, list(C)))
    shake = comp.null("shake", position=anim(keys))

    # impact lines that flick outwards and vanish
    rays = []
    rnd = random.Random(12)
    for i in range(10):
        a = (i + rnd.uniform(-0.25, 0.25)) / 10 * 2 * math.pi + 0.2
        r0, r1 = rnd.uniform(224, 236), rnd.uniform(268, 286)
        p0 = (r0 * math.cos(a), r0 * math.sin(a))
        p1 = (r1 * math.cos(a), r1 * math.sin(a))
        d = 3 + i % 3
        rays.append(group([path(bezier([p0, p1], closed=False), "ray"),
                           trim(anim([(d + 3, 0, EASE_SETTLE), (d + 9, 100)]),
                                anim([(d, 0, EASE_SETTLE), (d + 5, 100)])),
                           stroke(slot="outline", width=10)], f"ray-{i}"))
    comp.layer("impact-lines", rays, parent=shake, ip=3, op=16)

    burst_layer("burst-yellow", yellow, "secondary", 2, 24)
    burst_layer("burst-red", red, "primary", 0, -18)

    comp.marker("intro", 0, 13)
    comp.marker("outro", 28, 8)
    return comp


def burst_pts(spikes, r_out, r_in, seed, twist=0.0, spread=(0.78, 1.12)):
    """Irregular starburst outline points centred on (0, 0) (same recipe as the comic design)."""
    rnd = random.Random(seed)
    pts = []
    for i in range(spikes):
        a = (i + rnd.uniform(-0.18, 0.18)) / spikes * 2 * math.pi + twist
        ro = r_out * rnd.uniform(*spread)
        pts.append((ro * math.cos(a), ro * math.sin(a)))
        b = (i + 0.5 + rnd.uniform(-0.12, 0.12)) / spikes * 2 * math.pi + twist
        ri = r_in * rnd.uniform(0.9, 1.06)
        pts.append((ri * math.cos(b), ri * math.sin(b)))
    return pts


def outro_scale(keys):
    return anim(keys + [(28, [100, 100], ANTICIPATE), (35, [0, 0])])


def hand():
    """Marker starburst scribbled round in one go, filled with a pop of colour, with flicked speed lines."""
    comp = Comp("impact-burst-comic--hand", W, H, fps=30, frames=36)
    comp.marker("intro", 0, 16)
    comp.marker("outro", 28, 8)
    comp.slot("primary", "#FF2D2D")
    comp.slot("secondary", "#FFD21F")
    holder = comp.null("burst", position=C, scale=outro_scale([(0, [100, 100], LINEAR)]),
                       rotation=anim([(28, 0, (0.4, 0.0, 0.8, 0.6)), (35, -14)]))
    pts = burst_pts(13, 236, 160, seed=3, twist=-0.1, spread=(0.82, 1.08))
    line = c2.dense(c2.closed_loop(c2.dense(pts + [pts[0]], 3)[:-1], 0.05, 8))
    brushes = [c2.hand_line(line, 1, 13, 14, seed=5, chunks=4, ease=(0.35, 0.0, 0.3, 1.0), taper=(0.03, 0.08),
                            mins=(0.5, 0.3), wob=0.12, name="outline")]
    rnd = random.Random(12)
    for i in range(8):
        a = (i + rnd.uniform(-0.2, 0.2)) / 8 * 2 * math.pi + 0.35
        r0, r1 = rnd.uniform(248, 256), rnd.uniform(278, 290)
        seg = c2.dense([(r0 * math.cos(a), r0 * math.sin(a)), (r1 * math.cos(a), r1 * math.sin(a))])
        t = 12 + i % 3
        brushes.append(c2.hand_line(seg, t, t + 3, 11, seed=20 + i, taper=(0.1, 0.4), mins=(0.8, 0.3), wob=0.04,
                                    name=f"ray{i}"))
    c2.emit(comp, brushes, parent=holder)
    fill_pts = c2.P(pts, True)
    comp.layer("fill", [group([fill_pts, fill(slot="secondary")], "fill")], parent=holder, ip=6,
               scale=anim([(6, [40, 40], c2.SETTLE), (12, [106, 106], c2.SETTLE), (16, [100, 100])]),
               opacity=anim([(6, 0, c2.SETTLE), (9, 100)]))
    return comp


def neon():
    """Two nested neon starbursts that flicker on and hum, with glowing impact rays."""
    comp = Comp("impact-burst-comic--neon", W, H, fps=30, frames=36)
    comp.marker("intro", 0, 16)
    comp.marker("outro", 28, 8)
    comp.slot("primary", "#FF2D95")
    comp.slot("secondary", "#FFE14D")
    outer = burst_pts(14, 226, 156, seed=3, twist=-0.1, spread=(0.82, 1.1))
    inner = burst_pts(12, 150, 108, seed=8, twist=0.12, spread=(0.84, 1.08))
    hum = [(0, [70, 70], c2.SETTLE), (6, [104, 104], c2.SETTLE), (10, [100, 100], LINEAR)]
    holder = comp.null("burst", position=C, scale=outro_scale(hum))
    comp.layer("inner", [c2.neon_line(c2.dense(inner + [inner[0]], 3), 9, "secondary", t0=3, t1=12, name="inner")],
               parent=holder, opacity=c2.flicker(3), rotation=anim([(3, 20, c2.SETTLE), (14, 0)]))
    comp.layer("outer", [c2.neon_line(c2.dense(outer + [outer[0]], 3), 11, t0=1, t1=11, name="outer")],
               parent=holder, opacity=c2.flicker(1), rotation=anim([(1, -14, c2.SETTLE), (13, 0)]))
    rays = []
    for i in range(10):
        a = (i + 0.5) / 10 * 2 * math.pi + 0.2
        p0, p1 = (262 * math.cos(a), 262 * math.sin(a)), (286 * math.cos(a), 286 * math.sin(a))
        rays.append(c2.neon_line([p0, p1], 7, t0=8 + i % 3, t1=12 + i % 3, ease=c2.SETTLE, name=f"ray{i}"))
    comp.layer("rays", rays, parent=holder, ip=8, opacity=c2.flicker(8))
    return comp


build_asset("callouts", "impact-burst-comic", "Comic Impact Burst",
            "Spiky comic-book starburst that slams in; room in the middle for your own word.",
            ["comic", "burst", "pow", "impact", "boom", "explosion", "pop-art"], [
    Variant("bold", "Comic Bold", bold(), "intro-hold-outro", thumb_t=0.5, text_area=TEXT,
            description="Spiky comic-book starburst in red and yellow with a black outline that slams in with a shake."),
    Variant("hand", "Hand-Drawn", hand(), "intro-hold-outro", thumb_t=0.5, text_area=TEXT,
            description="Marker starburst scribbled round in one go, then filled with a pop of yellow and flicked speed lines."),
    Variant("neon", "Neon", neon(), "intro-hold-outro", thumb_t=0.5, text_area=TEXT,
            description="Two nested neon starbursts that flicker on and hum, with glowing impact rays."),
])
