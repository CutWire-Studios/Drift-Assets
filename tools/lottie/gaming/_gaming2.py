"""Shared parts for the second batch of gaming overlays.

Most assets come in a few house styles built from the same layout:

- modern:  sleek esports/AAA HUD: dark translucent panels, skewed edges, thin rims, glossy sheens.
- pixel:   8/16-bit retro: chunky pixel art traced with `_common.pixel_paths`, stepped (HOLD) motion.
- fantasy: RPG ornate: gold rims, gems, rune rings, magic purples.
- neon:    cyberpunk glow: stacked translucent strokes around a white-hot core.

Main colours stay slottable: shading is a translucent overlay on top of a slotted fill, and
gradient falloffs are applied through alpha mattes so the matted fill keeps its slot.
Layers added first draw on top (see lottie_kit.Comp).
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

from _common import box, grid_cells, pixel_paths  # noqa: E402,F401
from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import (HOLD, LINEAR, Anim, Comp, anim, bezier, ellipse, fill, group, path,  # noqa: E402,F401
                        polyline, rect, star, stroke, trim, gradient_fill)

CAT = "gaming"
SPRING = (0.3, 1.9, 0.55, 1.0)
DECEL = (0.2, 0.0, 0.1, 1.0)
TAU = 2 * math.pi

# palettes
PANEL = "#0F131B"
CYAN = "#35E0FF"
GOLD = "#F6C343"
GOLD_D = "#7A4A0E"
GOLD_L = "#FFE9A3"
INK = "#160E1E"
MAGENTA = "#FF2BD6"
NCYAN = "#27F2FF"
PURPLE = "#9B5CFF"
RED = "#FF3B47"
WHITE = "#FFFFFF"


# ---------------------------------------------------------------- math / timing

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x, p=3):
    return 1 - (1 - clamp(x)) ** p


def ease_in(x, p=2):
    return clamp(x) ** p


def back_out(x, s=1.9):
    x = clamp(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def spring(u, freq=1.2, decay=5.0):
    """Damped spring 0 -> 1 over local time u in seconds-ish units: overshoots then settles."""
    if u <= 0:
        return 0.0
    return 1 - math.exp(-decay * u) * math.cos(TAU * freq * u)


def bump(t, t0, t1):
    """0 -> 1 -> 0 half-sine between t0 and t1."""
    if t <= t0 or t >= t1:
        return 0.0
    return math.sin(math.pi * (t - t0) / (t1 - t0))


def sampled(fn, t0, t1, step=1, easing=LINEAR):
    """Keys sampled from fn(t) at t0, t0+step, ..., t1 (t1 always included)."""
    ts, t = [], t0
    while t < t1 - 1e-6:
        ts.append(round(t, 3))
        t += step
    ts.append(t1)
    return Anim([(t, fn(t), easing) for t in ts])


def stepped(fn, t0, t1, step=2):
    """Like sampled() but every key holds: choppy retro motion."""
    return sampled(fn, t0, t1, step, HOLD)


def particle(comp, name, shapes, t0, life, total, fn, step=1, wrap=True, hold=False, **static):
    """Short-lived layer driven by fn(u) -> {position/scale/rotation/opacity} for u in [0, life].
    With wrap, a copy shifted back by `total` frames keeps a loop seamless."""
    starts = [t0] + ([t0 - total] if wrap and t0 + life > total else [])
    for s in starts:
        keys = {}
        for k in fn(0):
            f = (lambda t, k=k, s=s: fn(min(max(t - s, 0), life))[k])
            keys[k] = sampled(f, s, s + life, step, HOLD if hold else LINEAR)
        comp.layer(name, shapes, ip=max(s, 0), op=min(s + life, total), **static, **keys)


def pop(t0, dur=12, to=100, e=SPRING):
    return anim([(t0, [0, 0], e), (t0 + dur, [to, to])])


def fade(t0, t1, a=0, b=100, e=EASE_OUT):
    return anim([(t0, a, e), (t1, b)])


# ---------------------------------------------------------------- geometry

def pt(r, deg, c=(0, 0)):
    """Point at radius r and angle deg (0 = up, clockwise)."""
    a = math.radians(deg - 90)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def arc_pts(r, a0, a1, n=48, c=(0, 0)):
    return [pt(r, a0 + (a1 - a0) * i / n, c) for i in range(n + 1)]


def arc(r, a0, a1, n=48, c=(0, 0)):
    return polyline(arc_pts(r, a0, a1, n, c))


def seg(p0, p1):
    return polyline([p0, p1])


def poly(pts, closed=True, name="poly"):
    return path(bezier(pts, closed=closed), name)


def ngon(n, r, rot=0, c=(0, 0)):
    return poly([pt(r, rot + i * 360 / n, c) for i in range(n)])


def skew_rect(w, h, sk, c=(0, 0)):
    """Parallelogram w x h whose top edge is shifted right by sk."""
    x, y = c
    return poly([(x - w / 2 + sk / 2, y - h / 2), (x + w / 2 + sk / 2, y - h / 2),
                 (x + w / 2 - sk / 2, y + h / 2), (x - w / 2 - sk / 2, y + h / 2)])


def lbar(x, y, w, h, keys, r=0):
    """Left-anchored rect at (x, y top-left) whose width follows [(frame, fraction, easing)]."""
    if not isinstance(keys, list):
        return rect((w * keys, h), (x + w * keys / 2, y + h / 2), r)
    size = anim([(t, [max(w * f, 0.01), h], e) for t, f, e in keys])
    pos = anim([(t, [x + w * f / 2, y + h / 2], e) for t, f, e in keys])
    return rect(size, pos, r)


def glow(d, color="#FFFFFF", a=0.7, pos=(0, 0), mid=0.3, name="glow"):
    """Soft radial glow disc of diameter d."""
    return group([ellipse((d, d), pos),
                  gradient_fill([(0, color, a), (mid, color, a * 0.55), (1, color, 0)],
                                pos, (pos[0] + d / 2, pos[1]), radial=True)], name)


def spark(s, ratio=0.26, rot=0):
    return star(4, s, s * ratio, rotation=rot)


def sheen(w, h, a=0.28, dark=0.2, name="sheen"):
    """Top-light / bottom-dark translucent overlay for a w x h box centred on 0."""
    return gradient_fill([(0, "#FFFFFF", a), (0.48, "#FFFFFF", a * 0.25), (0.52, "#000000", 0),
                          (1, "#000000", dark)], (0, -h / 2), (0, h / 2), name=name)


def neon(shapes, slot=None, color=None, w=6, core=True, glow_a=1.0, name="neon"):
    """Glowing tube: wide faint strokes, the coloured tube and a white-hot core."""
    out = []
    if core:
        out.append(group(list(shapes) + [stroke("#FFFFFF", width=w * 0.38, opacity=85)], name + " core"))
    out.append(group(list(shapes) + [stroke(color or "#FFFFFF", width=w, slot=slot)], name + " tube"))
    for k, (mul, op) in enumerate(((2.4, 32), (4.4, 14), (7.5, 7))):
        out.append(group(list(shapes) + [stroke(color or "#FFFFFF", width=w * mul, opacity=op * glow_a,
                                                slot=slot)], f"{name} glow{k}"))
    return out


def neon_fill(shapes, slot=None, color=None, w=6, name="neonfill"):
    """Glow halo around a filled shape."""
    return [group(list(shapes) + [stroke(color or "#FFFFFF", width=w * mul, opacity=op, slot=slot)],
                  f"{name}{k}") for k, (mul, op) in enumerate(((1.6, 34), (3.4, 14), (6, 7)))]


# ---------------------------------------------------------------- pixel art

def _pfill(spec):
    """(fill, translucent) for a pixel colour spec."""
    if isinstance(spec, str):
        return fill(spec), False
    if spec[0] == "slot":
        op = spec[2] if len(spec) > 2 else 100
        return fill(slot=spec[1], opacity=op), op < 100
    return fill(spec[0], spec[1]), spec[1] < 100


def pix(rows, colors, px, center=(0, 0), order=None, name="pix"):
    """Pixel art from ASCII rows. colors: char -> colour spec ("#hex", ("#hex", opacity),
    ("slot", name) or ("slot", name, opacity)). order lists chars top (first) to bottom; each opaque
    layer also covers every cell of the layers above it, so neighbouring colours have no AA seams."""
    order = order or list(colors)
    gw, gh = max(len(r) for r in rows), len(rows)
    origin = (center[0] - gw * px / 2, center[1] - gh * px / 2)
    out, acc = [], []
    for ch in order:
        own = grid_cells(rows, ch)
        acc = acc + own
        f, translucent = _pfill(colors[ch])
        cells = own if translucent else acc
        if cells:
            out.append(group([*pixel_paths(cells, px, origin, name), f], f"{name} {ch}"))
    return out


def pix_cells(fn, n):
    """Cells (c, r) of an n x n grid where fn(x, y) is true, x/y relative to the grid centre in cells."""
    return [(c, r) for r in range(n) for c in range(n) if fn(c + 0.5 - n / 2, r + 0.5 - n / 2)]


def pix_group(cells, px, origin, spec, name="cells"):
    return group([*pixel_paths(cells, px, origin, name), _pfill(spec)[0]], name)


def rows_to_cells(rows, chars):
    return [c for ch in chars for c in grid_cells(rows, ch)]


def snap(v, px):
    return round(v / px) * px


# ---------------------------------------------------------------- shared icons (centred on 0, ~1 unit = 1 px)

def skull_d(s=1.0):
    """Skull silhouette with eye/nose holes as separate subpaths (use even_odd fill)."""
    return [
        poly([(x * s, y * s) for x, y in [
            (-22, 4), (-24, -8), (-20, -20), (-10, -27), (0, -29), (10, -27), (20, -20), (24, -8), (22, 4),
            (15, 9), (14, 20), (-14, 20), (-15, 9)]], name="skull"),
        ellipse((13 * s, 12 * s), (-9.5 * s, -4 * s), name="eyeL"),
        ellipse((13 * s, 12 * s), (9.5 * s, -4 * s), name="eyeR"),
        poly([(0, 5 * s), (-4 * s, 12 * s), (4 * s, 12 * s)], name="nose"),
    ]


def skull_teeth(s=1.0):
    return [rect((2.6 * s, 7 * s), (x * s, 17 * s)) for x in (-5.5, 0, 5.5)]


SKULL_PIX = [
    "..KKKKKKK..",
    ".KWWWWWWWK.",
    "KWWWWWWWWWK",
    "KWKKWWWKKWK",
    "KWKKWWWKKWK",
    "KWWWWKWWWWK",
    ".KWWWWWWWK.",
    "..KWKWKWK..",
    "..KKKKKKK..",
]
