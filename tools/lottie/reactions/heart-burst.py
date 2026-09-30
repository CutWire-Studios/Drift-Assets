"""Hearts float up with a wobble, pop in and fade out, staggered so the loop is never empty."""

import math
import random

from _common import *
import _reactions2 as r2
from drift_lottie import Variant, build_asset

T = 60
W, H = 400, 560
PINK, LIGHT = "#FF3B6B", "#FF8FB1"

HEART_D = ("M 0 38 C -30 20 -54 0 -54 -20 C -54 -39 -40 -51 -25 -51 C -13 -51 -4 -44 0 -33 "
           "C 4 -44 13 -51 25 -51 C 40 -51 54 -39 54 -20 C 54 0 30 20 0 38 Z")


def heart(color, sid):
    return [
        group([ellipse((10, 10)), fill("#FFFFFF", 80)], name="glint2", position=(-14, -38)),
        group([ellipse((24, 14)), fill("#FFFFFF", 80)], name="glint", position=(-33, -24),
              rotation=-50),
        group(svg_shapes("M 54 -20 C 54 0 30 20 0 38 C 10 22 40 4 46 -20 C 48 -30 46 -40 40 -46 "
                         "C 48 -41 54 -32 54 -20 Z") + [fill("#000000", 12)], name="shade"),
        group(svg_shapes(HEART_D) + [fill(color, slot=sid)], name="heart"),
    ]


def glossy():
    comp = Comp("heart-burst", W, H, fps=30, frames=T)
    comp.slot("primary", PINK)
    comp.slot("secondary", LIGHT)

    rng = random.Random(7)
    N, LIFE = 9, 52
    xs = [200, 290, 115, 245, 160, 300, 100, 225, 150]
    for i in range(N):
        t0 = i * T / N
        x0 = xs[i] + rng.uniform(-10, 10)
        size = rng.uniform(0.6, 0.95) if i % 3 else 1.1
        amp = rng.uniform(16, 28) * (1 if i % 2 else -1)
        wob = rng.uniform(0.9, 1.3)
        rise = rng.uniform(390, 440)
        y0 = 500

        def fn(u, x0=x0, size=size, amp=amp, wob=wob, rise=rise):
            k = u / LIFE
            w = math.sin(2 * math.pi * wob * k)
            y = y0 - rise * (1 - (1 - k) ** 1.3)
            if u < 5:
                s = size * 1.18 * (u / 5) ** 0.7
            elif u < 11:
                s = size * (1.18 - 0.18 * (1 - math.cos(math.pi * (u - 5) / 6)) / 2)
            else:
                s = size * (1 - 0.25 * (u - 11) / (LIFE - 11))
            stretch = 1 + 0.06 * math.cos(2 * math.pi * wob * k * 2)
            return {"position": (x0 + amp * w, y),
                    "rotation": -14 * math.cos(2 * math.pi * wob * k) * (1 if amp > 0 else -1),
                    "scale": (100 * s / stretch, 100 * s * stretch),
                    "opacity": 100 if u < LIFE - 14 else 100 * ((LIFE - u) / 14) ** 1.3}

        col, sid = (PINK, "primary") if i % 3 != 1 else (LIGHT, "secondary")
        particle(comp, f"heart{i}", heart(col, sid), round(t0, 2), LIFE, T, fn, step=2)
    return comp


def flat():
    """Die-cut sticker hearts that bob up in a zig-zag stream, each popping in with a squash."""
    st = r2.Style("flat")
    comp = Comp("heart-burst--flat", W, H, fps=30, frames=T)
    comp.slot("primary", PINK)
    comp.slot("secondary", LIGHT)
    comp.slot("outline", r2.WHITE)
    rnd = random.Random(3)
    n, life = 6, 54
    xs = [200, 270, 130, 230, 160, 250]
    for i in range(n):
        t0 = i * T / n
        size = 0.95 if i % 2 == 0 else 0.7
        tilt = rnd.uniform(8, 16) * (1 if i % 2 else -1)
        x0 = xs[i]

        def fn(u, x0=x0, size=size, tilt=tilt):
            k = u / life
            y = 500 - 400 * (1 - (1 - k) ** 1.4)
            x = x0 + 22 * math.sin(2 * math.pi * (k * 1.2)) * (1 if tilt > 0 else -1)
            pop = r2.spring(u / 10, 0.9, 4.5)
            sq = 1 + 0.12 * math.sin(2 * math.pi * k * 2.4) * (1 - k)
            s = 100 * size * pop * (1 - 0.2 * k)
            return {"position": (x, y), "rotation": tilt * math.cos(2 * math.pi * k * 1.2),
                    "scale": (s * sq, s / sq),
                    "opacity": 100 if u < life - 12 else 100 * ((life - u) / 12) ** 1.2}

        col, sid = (PINK, "primary") if i % 3 != 1 else (LIGHT, "secondary")
        top = [group([ellipse((20, 11)), fill(r2.WHITE, 85)], name="gleam", position=(-30, -26), rotation=-50)]
        particle(comp, f"heart{i}", st.body(svg_shapes(HEART_D), col, sid, (-54, -51, 54, 38), top=top),
                 round(t0, 2), life, T, fn, step=2)
    return comp


def outline():
    """A big cartoon heart beats twice per loop, throwing out a ring of little outlined hearts each beat."""
    st = r2.Style("outline")
    S2 = 440
    comp = Comp("heart-burst--outline", S2, S2, fps=30, frames=T)
    comp.slot("primary", PINK)
    comp.slot("secondary", LIGHT)
    comp.slot("outline", st.ink)
    c = (S2 / 2, S2 / 2 + 10)
    beats = (0, 30)

    def beat(t):
        v = 0.0
        for b in beats + (T,):
            u = t - b
            if -2 <= u < 14:
                v = max(v, math.exp(-max(u, 0) / 4) * math.sin(math.pi * min(max(u + 2, 0) / 5, 1)))
        return v

    rnd = random.Random(8)
    for bi, b in enumerate(beats):
        for j in range(8):
            a = math.radians(j * 45 + 22.5 * bi + rnd.uniform(-8, 8))
            dist = rnd.uniform(150, 180)
            sz = rnd.uniform(0.3, 0.42)
            spin = rnd.uniform(-40, 40)

            def fn(u, a=a, dist=dist, sz=sz, spin=spin):
                k = u / 26
                d = 70 + (dist - 70) * r2.ease_out(k, 3)
                s = 100 * sz * (r2.back_out(min(u / 6, 1)) if u < 6 else 1 - r2.smooth((k - 0.55) / 0.45))
                return {"position": (c[0] + math.cos(a) * d, c[1] + math.sin(a) * d - 10 * k),
                        "rotation": spin * k, "scale": (s, s)}

            col, sid = (LIGHT, "secondary") if j % 2 else (PINK, "primary")
            particle(comp, f"mini{bi}-{j}", [group(svg_shapes(HEART_D) + st.paint(col, sid, sil=True))],
                     b + 1, 26, T, fn, step=2)
    ring = [group([ellipse((220, 220)), stroke(LIGHT, 8, slot="secondary")], name="ring")]
    for b in beats:
        comp.layer(f"ring{b}", ring, position=c, ip=b + 1, op=b + 19,
                   scale=anim([(b + 1, [60, 60], SNAP_OUT), (b + 18, [150, 150])]),
                   opacity=anim([(b + 1, 90, EASE_IN), (b + 18, 0)]))
    k = 2.3
    shine = [group(svg_shapes("M -38 -30 C -34 -38 -26 -42 -18 -42", k) + [stroke(r2.WHITE, 10)], name="shine")]
    heart = st.body(svg_shapes(HEART_D, k), PINK, "primary", (-54 * k, -51 * k, 54 * k, 38 * k),
                    shade=svg_shapes("M 54 -20 C 54 0 30 20 0 38 C 10 22 40 4 46 -20 "
                                     "C 48 -30 46 -40 40 -46 C 48 -41 54 -32 54 -20 Z", k))
    comp.layers.insert(0, None)  # placeholder so the big heart draws above the burst
    ind = comp.layer("heart", shine + heart, position=c, scale=sampled(lambda t: [100 * (1 + 0.14 * beat(t))] * 2, 0, T))
    comp.layers[0] = comp.layers.pop()
    return comp


build_asset("reactions", "heart-burst", "Heart Burst",
            "Hearts that pop and float for likes and love, looping seamlessly; never empty.",
            ["heart", "love", "like", "hearts", "reaction", "valentine"], [
    Variant("glossy", "Glossy Float", glossy(), "loop", thumb_t=0.5,
            description="Shaded hearts float up with a gentle wobble, pop in and fade out, staggered so it is never empty."),
    Variant("flat", "Flat Sticker", flat(), "loop", thumb_t=0.5,
            description="Die-cut sticker hearts with white borders bob up in a zig-zag stream, each popping in with a squash."),
    Variant("outline", "Bold Outline Beat", outline(), "loop", thumb_t=0.17, bg="e8e8ee",
            description="A big outlined cartoon heart beats twice per loop, throwing out rings of little hearts."),
])
