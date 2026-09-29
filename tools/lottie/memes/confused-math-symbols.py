"""Maths symbols float around a head: the "confused calculating" meme loop, in three looks."""

from _memes2 import *

W, H = 1240, 760
C = (W / 2, H / 2 + 70)   # the head goes here
F = 90


def sym_plus(s=1.0):
    return [polyline([(-30 * s, 0), (30 * s, 0)]), polyline([(0, -30 * s), (0, 30 * s)])]


def sym_pi(s=1.0):
    return [polyline([(-38 * s, -26 * s), (40 * s, -30 * s)]),
            path(bezier([(-16 * s, -27 * s), (-22 * s, 34 * s)], [(0, 0), (6 * s, -20 * s)], [(0, 20 * s), (0, 0)],
                        closed=False)),
            path(bezier([(14 * s, -28 * s), (16 * s, 26 * s), (32 * s, 30 * s)], [(0, 0), (-4 * s, -10 * s), (-8 * s, 4 * s)],
                        [(0, 18 * s), (2 * s, 8 * s), (0, 0)], closed=False))]


def sym_integral(s=1.0):
    return [path(bezier([(22 * s, -52 * s), (6 * s, -44 * s), (-6 * s, 44 * s), (-22 * s, 52 * s)],
                        [(0, 0), (6 * s, -12 * s), (4 * s, -40 * s), (8 * s, 4 * s)],
                        [(-8 * s, -4 * s), (-4 * s, 40 * s), (-6 * s, 12 * s), (0, 0)], closed=False))]


def sym_sqrt(s=1.0):
    return [polyline([(-44 * s, 4 * s), (-32 * s, -4 * s), (-18 * s, 30 * s), (0, -34 * s), (48 * s, -34 * s)])]


def sym_triangle(s=1.0):
    return [polyline([(0, -34 * s), (36 * s, 28 * s), (-36 * s, 28 * s)], closed=True)]


def sym_equals(s=1.0):
    return [polyline([(-30 * s, -11 * s), (30 * s, -11 * s)]), polyline([(-30 * s, 11 * s), (30 * s, 11 * s)])]


def sym_divide(s=1.0):
    return [polyline([(-30 * s, 0), (30 * s, 0)]), ellipse((10 * s, 10 * s), (0, -20 * s)),
            ellipse((10 * s, 10 * s), (0, 20 * s))]


def sym_infinity(s=1.0):
    return [smooth_path([(0, 0), (24 * s, -18 * s), (44 * s, 0), (24 * s, 18 * s), (0, 0), (-24 * s, -18 * s),
                         (-44 * s, 0), (-24 * s, 18 * s)], closed=True)]


def sym_graph(s=1.0):
    return [polyline([(-36 * s, -36 * s), (-36 * s, 34 * s), (40 * s, 34 * s)]),
            path(bezier([(-30 * s, 20 * s), (0, -24 * s), (34 * s, 18 * s)], [(0, 0), (-16 * s, 0), (-10 * s, -20 * s)],
                        [(10 * s, -20 * s), (16 * s, 0), (0, 0)], closed=False))]


def sym_angle(s=1.0):
    return [polyline([(40 * s, -30 * s), (-36 * s, 26 * s), (44 * s, 26 * s)]),
            path(arc(34 * s, -36, 0, (-36 * s, 26 * s)))]


def sym_circle(s=1.0):
    return [ellipse((70 * s, 70 * s)), polyline([(0, 0), (35 * s, 0)]), ellipse((10 * s, 10 * s))]


SYMS = [sym_pi, sym_plus, sym_integral, sym_sqrt, sym_triangle, sym_equals, sym_infinity, sym_graph, sym_divide,
        sym_circle]
DOT_SYMS = {sym_divide}


def spots(n, rx, ry, seed, cx=C[0], cy=C[1]):
    """Positions on two staggered arcs over and beside the head (the face below stays clear)."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a = math.radians(184 + i * 172 / (n - 1)) + rng.uniform(-0.03, 0.03)
        r = rng.uniform(0.95, 1.05)
        out.append((cx + rx * r * math.cos(a), cy - 40 + ry * r * math.sin(a)))
    return out


def paint(shapes, fn, sym):
    """Strokes for line symbols; filled dots stay dots."""
    dots = [s for s in shapes if s["ty"] == "el" and s["s"]["k"][0] < 20]
    lines = [s for s in shapes if s not in dots]
    out = fn(lines, False)
    if dots:
        out = fn(dots, True) + out
    return out


def chalk():
    """Hand-chalked white symbols drifting slowly and fading in and out around the head."""
    comp = base("confused-math-symbols", W, H, F)
    comp.slot("primary", "#FFFFFF")
    rng = random.Random(1)
    pts = spots(9, 520, 350, 2)
    for i, (sym, p) in enumerate(zip(SYMS, pts)):
        s = rng.uniform(1.4, 1.7)
        ph = rng.uniform(0, TAU)
        dx, dy = rng.uniform(14, 30), rng.uniform(10, 24)
        rot0 = rng.uniform(-25, 25)

        def st(items, dot):
            if dot:
                return [group(items + [fill(slot="primary", opacity=85)], "dots")]
            return [group(items + [stroke(slot="primary", width=9, opacity=85)], "chalk"),
                    group(items + [stroke(slot="primary", width=4, opacity=40)], "grain", position=(4, 3))]
        n = 7
        pos = keys(*[(round(j * F / (n - 1), 2), [p[0] + dx * math.cos(TAU * j / (n - 1) + ph),
                                                   p[1] + dy * math.sin(TAU * j / (n - 1) * 2 + ph)], SINE)
                     for j in range(n)])
        rotk = keys(*[(round(j * F / (n - 1), 2), rot0 + 10 * math.sin(TAU * j / (n - 1) + ph), SINE) for j in range(n)])
        opk = keys(*[(round(j * F / (n - 1), 2), 55 + 45 * math.cos(TAU * j / (n - 1) + ph * 1.7), SINE)
                     for j in range(n)])
        comp.layer(f"sym{i}", paint(sym(s), st, sym), position=pos, rotation=rotk, opacity=opk)
    return comp


def neon():
    """Glowing neon symbols orbit the head on a tilted ring, bigger and brighter at the front."""
    comp = base("confused-math-symbols--neon", W, H, F)
    comp.slot("primary", "#4FF0FF")
    comp.slot("secondary", "#FF4FD8")
    comp.slot("accent", "#FFE14D")
    slots = ("primary", "secondary", "accent")
    n = 9
    rx, ry = 480, 130
    cy = C[1] - 250
    for i in range(n):
        sym = SYMS[i]
        a0 = TAU * i / n
        sl = slots[i % 3]

        def st(items, dot, sl=sl):
            if dot:
                return [group(items + [fill(slot=sl)], "dots")]
            return glow_strokes(items, slot=sl, width=7, widths=(3.2, 1.8), ops=(10, 22))
        m = 13
        ks_p, ks_s, ks_o = [], [], []
        for j in range(m):
            t = round(j * F / (m - 1), 2)
            a = a0 + TAU * j / (m - 1)
            depth = (math.sin(a) + 1) / 2   # 0 back, 1 front
            ks_p.append((t, [C[0] + rx * math.cos(a), cy + ry * math.sin(a)], LINEAR))
            ks_s.append((t, [70 + 50 * depth] * 2, LINEAR))
            ks_o.append((t, 35 + 65 * depth, LINEAR))
        comp.layer(f"sym{i}", paint(sym(1.6), st, sym), position=keys(*ks_p), scale=keys(*ks_s),
                   opacity=keys(*ks_o), rotation=loop(F, [-12, 12], SINE))
    # the orbit ring itself, faint
    comp.layer("orbit", [group([ellipse((2 * rx, 2 * ry), (C[0], cy)),
                                stroke(slot="primary", width=3, opacity=25, dashes=[14, 18])], "o")])
    return comp


def sticker():
    """Chunky colourful sticker symbols with ink outlines that bob and wobble around the head."""
    comp = base("confused-math-symbols--sticker", W, H, F)
    comp.slot("primary", "#FF5A5F")
    comp.slot("secondary", "#3DB2FF")
    comp.slot("accent", "#FFD23F")
    comp.slot("outline", INK)
    slots = ("primary", "secondary", "accent")
    rng = random.Random(7)
    pts = spots(8, 520, 350, 5)
    for i, p in enumerate(pts):
        sym = SYMS[i]
        sl = slots[i % 3]
        s = rng.uniform(1.4, 1.7)
        ph = i * F / len(pts)

        def st(items, dot, sl=sl):
            if dot:
                return [group(items + [fill(slot=sl), stroke(slot="outline", width=8)], "dots")]
            return [group(items + [stroke(slot=sl, width=16)], "c"),
                    group(items + [stroke(slot="outline", width=30)], "ink"),
                    group(items + [stroke("#000000", width=30, opacity=25)], "shadow", position=(5, 7))]
        bob = keys(*[(round(j * F / 6, 2), [p[0], p[1] + 16 * math.sin(TAU * j / 6 + ph)], SINE) for j in range(7)])
        wob = keys(*[(round(j * F / 6, 2), 14 * math.sin(TAU * j / 6 * 2 + ph), SINE) for j in range(7)])
        comp.layer(f"sym{i}", paint(sym(s), st, sym), position=bob, rotation=wob)
    return comp


build_asset(CAT, "confused-math-symbols", "Confused Math Symbols",
            "Maths-ish symbols (plus, pi, integral, root, triangles and more) float around a head on a seamless loop "
            "for the confused-calculating meme. Put the face in the clear middle.",
            ["math", "confused", "calculating", "thinking", "symbols", "meme", "loop"], [
    Variant("chalk", "Chalk", chalk(), "loop", thumb_t=0.2,
            description="Hand-chalked white symbols drifting and fading around the head."),
    Variant("neon", "Neon Orbit", neon(), "loop", thumb_t=0.2,
            description="Glowing neon symbols orbiting the head on a tilted ring."),
    Variant("sticker", "Stickers", sticker(), "loop", thumb_t=0.2,
            description="Chunky colourful symbols with ink outlines that bob and wobble."),
])
