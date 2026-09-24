import math
import random

from _common import (ANTICIPATE, HOLD, LINEAR, Comp, anim, bezier, fill, finish, group, path,
                     stroke, trim)

W = H = 600
C = (W / 2, H / 2)
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

finish(comp, "impact-burst-comic", "Comic Impact Burst",
       "Spiky comic-book starburst in red and yellow with a black outline that slams in with a "
       "shake; room in the middle for your own word.",
       ["comic", "burst", "pow", "impact", "boom", "explosion", "pop-art"], "intro-hold-outro",
       text_area=[int(C[0]) - 95, int(C[1]) - 60, 190, 120], thumb_t=0.5)
