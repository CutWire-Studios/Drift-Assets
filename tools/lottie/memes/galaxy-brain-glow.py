"""Glowing "galaxy brain" with radiating rays: an ascended-mind loop in three looks."""

from _memes2 import *

S = 600
C = (S / 2, S / 2)
F = 90
# side-view brain built from overlapping lobes (x, y, diameter) around (0, 0)
LOBES = [(0, -8, 290, 190), (-104, -30, 120, 120), (-44, -74, 134, 124), (40, -78, 134, 124),
         (104, -42, 124, 120), (132, 6, 96, 100), (-128, 14, 100, 100), (-30, 42, 170, 96)]
CEREB = (96, 62, 92)
STEM = [(40, 70), (62, 70), (66, 128), (46, 132)]
GYRI = [
    ("s", [(-128, 30), (-70, 8), (-10, 16), (50, 2), (96, 10)]),   # lateral fissure
    ("a", (-104, -30, 40, 200, 320)),
    ("a", (-44, -70, 44, 190, 330)),
    ("a", (40, -74, 44, 210, 350)),
    ("a", (104, -40, 40, 230, 20)),
    ("s", [(-100, 52), (-60, 64), (-20, 56), (20, 66)]),
    ("s", [(-70, -20), (-30, -34), (10, -20), (60, -34), (100, -14)]),
]
CEREB_LINES = [(-30, -10), (-26, 4), (-18, 18)]


def brain_shapes(pos=C, grow=0):
    out = [ellipse((w + grow, h + grow), (pos[0] + x, pos[1] + y)) for x, y, w, h in LOBES]
    out.append(ellipse((CEREB[2] + grow, CEREB[2] * 0.72 + grow), (pos[0] + CEREB[0], pos[1] + CEREB[1])))
    return out


def stem(pos=C):
    return polyline([(pos[0] + x, pos[1] + y) for x, y in STEM], closed=True)


def gyri(pos=C):
    out = []
    for kind, g in GYRI:
        if kind == "s":
            out.append(smooth_path([(pos[0] + x, pos[1] + y) for x, y in g], closed=False))
        else:
            x, y, r, a0, a1 = g
            if a1 < a0:
                a1 += 360
            out.append(arc_path(r, a0, a1, (pos[0] + x, pos[1] + y)))
    cx, cy = pos[0] + CEREB[0], pos[1] + CEREB[1]
    for dx, dy in CEREB_LINES:
        out.append(polyline([(cx + dx, cy + dy), (cx + dx + 44, cy + dy - 2)]))
    return out


def rays(n, r0, r1, w, pos=C, jitter=0.0, seed=1):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a = TAU * i / n + rng.uniform(-jitter, jitter)
        ww = w * (1.0 if i % 2 == 0 else 0.55)
        rr = r1 * (1.0 if i % 2 == 0 else 0.78)
        out.append(wedge(pos[0], pos[1], a, r0, rr, ww, 2))
    return out


def twinkles(comp, n, seed, slot=None, color="#FFFFFF", rmin=190, rmax=280, size=(18, 34)):
    rng = random.Random(seed)
    for i in range(n):
        a = rng.uniform(0, TAU)
        r = rng.uniform(rmin, rmax)
        p = (C[0] + r * math.cos(a), C[1] + r * math.sin(a))
        sz = rng.uniform(*size)
        ph = rng.uniform(0, F)
        k = []
        for j in range(7):
            t = j * F / 6
            v = 0.5 + 0.5 * math.cos(TAU * (t - ph) / F * 2)
            k.append((round(t, 2), [100 * v, 100 * v], SINE))
        k[-1] = (F, k[0][1], LINEAR)
        comp.layer(f"twinkle{i}", [group([sparkle(sz), fill(color, slot=slot)], "s")], position=p, scale=keys(*k))


def cosmic():
    """Bright cyan brain with layered glow, slowly turning violet rays and twinkling stars."""
    comp = base("galaxy-brain-glow", S, S, F)
    comp.slot("primary", "#BDF3FF")
    comp.slot("secondary", "#9B6BFF")
    comp.slot("accent", "#FFFFFF")
    pulse = loop(F, [[100, 100], [104, 104]], SINE)
    twinkles(comp, 9, 3, slot="accent")
    comp.layer("gyri", [group(gyri() + [stroke("#4FB6E8", width=7)], "g")], anchor=C, position=C, scale=pulse)
    comp.layer("brain", [group([ellipse((110, 40), (C[0] - 50, C[1] - 86)), fill("#FFFFFF", 60)], "hi"),
                         group(brain_shapes() + [fill(slot="primary")], "b"),
                         group([stem(), round_corners(10), fill("#7FD8F5")], "stem")],
                 anchor=C, position=C, scale=pulse)
    comp.layer("glow", [group(brain_shapes() + [stroke(slot="primary", width=w, opacity=o)], f"g{w}")
                        for w, o in ((22, 40), (48, 18), (86, 9))],
               anchor=C, position=C, scale=loop(F, [[100, 100], [110, 110]], SINE))
    comp.layer("rays", [group(rays(16, 120, 290, 40) + [fill(slot="secondary", opacity=70)], "r")],
               anchor=C, position=C, rotation=keys((0, 0, LINEAR), (F, 360 / 8)))
    comp.layer("rays2", [group(rays(16, 110, 250, 70, seed=2) + [fill("#4FD8FF", 25)], "r")],
               anchor=C, position=C, rotation=keys((0, 11.25, LINEAR), (F, 11.25 - 360 / 8)))
    comp.layer("nebula", [group([ellipse((520, 520), C),
                                 gradient_fill([(0, "#9B6BFF", 0.55), (0.6, "#3B2A8F", 0.25), (1, "#1B1450", 0)],
                                               C, (C[0] + 260, C[1]), radial=True)], "n")],
               anchor=C, position=C, scale=loop(F, [[100, 100], [92, 92]], SINE))
    return comp


def neon():
    """Line-art brain traced in neon tubes; light pulses race out along thin rays."""
    comp = base("galaxy-brain-glow--neon", S, S, F)
    comp.slot("primary", "#FF4FD8")
    comp.slot("secondary", "#4FF0FF")
    twinkles(comp, 7, 5, slot="secondary", size=(12, 22))
    comp.layer("gyri", glow_strokes(gyri(), slot="primary", width=6, widths=(3, 1.8), ops=(10, 22)))
    comp.layer("stem", glow_strokes([polyline([(C[0] + 52, C[1] + 92), (C[0] + 58, C[1] + 134)])], slot="primary", width=12, widths=(3, 1.8), ops=(8, 18)))
    comp.layer("knock", [group(brain_shapes() + [fill("#000000")], "k")])
    comp.layer("outline", glow_strokes(brain_shapes(), slot="primary", width=16, widths=(3, 1.8), ops=(8, 18)),
               matte="alpha_inverted")
    n, life = 12, 22
    for i in range(n):
        a = TAU * i / n
        p0 = (C[0] + 175 * math.cos(a), C[1] + 175 * math.sin(a))
        p1 = (C[0] + 285 * math.cos(a), C[1] + 285 * math.sin(a))
        for j in range(3):
            t0 = (i * 7 + j * F / 3) % F
            for s0 in [t0] + ([t0 - F] if t0 + life > F else []):
                comp.layer(f"pulse{i}-{j}", [group([polyline([p0, p1]),
                                                    trim(start=keys((s0, 0, LINEAR), (s0 + life, 75)),
                                                         end=keys((s0, 25, LINEAR), (s0 + life, 100))),
                                                    stroke("#FFFFFF", width=6)], "pulse")],
                           ip=max(0, s0), op=min(F, s0 + life))
        comp.layer(f"ray{i}", [group([polyline([p0, p1]), stroke(slot="secondary", width=4, opacity=50)], "r")])
    return comp


def ascend():
    """White-gold radiant brain: halo rings keep radiating outward and long gold rays turn slowly."""
    comp = base("galaxy-brain-glow--ascend", S, S, F)
    comp.slot("primary", "#FFF6DC")
    comp.slot("accent", "#FFC83D")
    comp.slot("secondary", "#FFE9A8")
    twinkles(comp, 8, 9, slot="primary", rmin=200, rmax=285)
    comp.layer("gyri", [group(gyri() + [stroke("#E7B24A", width=6, opacity=80)], "g")])
    comp.layer("brain", [group(brain_shapes() + [fill(slot="primary")], "b"),
                         group([stem(), round_corners(10), fill("#F4D48A")], "stem")])
    comp.layer("glow", [group(brain_shapes() + [stroke(slot="accent", width=w, opacity=o)], f"g{w}")
                        for w, o in ((16, 60), (40, 25), (80, 10))])
    for i in range(3):
        t0 = i * F / 3

        def fn(u):
            p = u / 60
            return {"scale": [60 + 90 * p, 60 + 90 * p], "opacity": 80 * (1 - p) * clamp(p * 6)}
        particle(comp, f"halo{i}", [group([ellipse((360, 300)), stroke(slot="accent", width=6)], "h")],
                 t0, 60, F, fn, step=3, position=C)
    comp.layer("rays", [group(rays(24, 150, 300, 22) + [fill(slot="secondary", opacity=65)], "r")],
               anchor=C, position=C, rotation=keys((0, 0, LINEAR), (F, 360 / 12)))
    comp.layer("aura", [group([ellipse((560, 560), C),
                               gradient_fill([(0, "#FFE9A8", 0.6), (0.55, "#FFC83D", 0.2), (1, "#FFC83D", 0)],
                                             C, (C[0] + 280, C[1]), radial=True)], "a")],
               anchor=C, position=C, scale=loop(F, [[100, 100], [94, 94]], SINE))
    return comp


build_asset(CAT, "galaxy-brain-glow", "Galaxy Brain",
            "A glowing brain with radiating galaxy rays and twinkling stars on a seamless loop, for peak big-brain "
            "moments. Place it beside or over a head.",
            ["galaxy brain", "brain", "glow", "smart", "enlightened", "meme", "loop"], [
    Variant("cosmic", "Cosmic", cosmic(), "loop", thumb_t=0.3,
            description="Bright cyan brain with layered glow, turning violet rays and a nebula haze."),
    Variant("neon", "Neon Outline", neon(), "loop", thumb_t=0.3,
            description="Line-art brain in neon tubes with light pulses racing out along thin rays."),
    Variant("ascend", "Ascended", ascend(), "loop", thumb_t=0.3,
            description="White-gold radiant brain with halo rings radiating outward and slow gold rays."),
])
