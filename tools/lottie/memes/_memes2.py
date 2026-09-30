"""Shared helpers for the memes2 batch (variant builds via drift_lottie).

Shapes are mostly drawn in canvas coordinates; `lay()` / `rig()` put a layer's anchor on a pivot so
scale and rotation happen around it. Layers added first draw on top (see lottie_kit.Comp).
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

from _common import particle, pixel_outline, sampled  # noqa: E402,F401
from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import HOLD, LINEAR, Anim, Comp  # noqa: E402,F401

CAT = "memes"
SPRING = (0.3, 1.8, 0.55, 1.0)
DECEL = (0.2, 0.0, 0.1, 1.0)
EXPO_OUT = (0.16, 1.0, 0.3, 1.0)
EXPO_IN = (0.7, 0.0, 0.84, 0.0)
BACK_IN = (0.5, -0.4, 0.8, 0.4)
SINE = (0.37, 0.0, 0.63, 1.0)
INK = "#141418"
TAU = 2 * math.pi


def keys(*k):
    return Anim(list(k))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x, p=3):
    return 1 - (1 - clamp(x)) ** p


def base(name, w, h, frames, intro_end=None, outro=None):
    c = Comp(name, w, h, fps=30, frames=frames)
    if intro_end is not None:
        c.marker("intro", 0, intro_end)
    if outro is not None:
        c.marker("outro", outro, frames - outro)
    return c


def at(pivot, off=None):
    if off is None:
        return pivot
    if not isinstance(off, Anim):
        return (pivot[0] + off[0], pivot[1] + off[1])
    return Anim([(t, [v[0] + pivot[0], v[1] + pivot[1]], e) for t, v, e in off.keys])


def lay(comp, name, shapes, pivot=(0, 0), off=None, **kw):
    """Shape layer drawn in canvas coords, scaling/rotating about `pivot`, moved by `off`."""
    return comp.layer(name, shapes, anchor=pivot, position=at(pivot, off), **kw)


def rig(comp, name, pivot=(0, 0), off=None, **kw):
    """Null whose children keep canvas coords; scale/rotation about `pivot`."""
    return comp.null(name, anchor=pivot, position=at(pivot, off), **kw)


def fade(t0, t1, t2=None, t3=None, to=100, e_in=EASE_OUT, e_out=EASE_IN):
    k = [(t0, 0, e_in), (t1, to, HOLD if t2 is not None else LINEAR)]
    if t2 is not None:
        k += [(t2, to, e_out), (t3, 0)]
    return Anim(k)


def pop(t0, dur=14, t2=None, dur_out=8, spring=SPRING, to=100):
    k = [(t0, [0, 0], spring), (t0 + dur, [to, to], HOLD if t2 is not None else LINEAR)]
    if t2 is not None:
        k += [(t2, [to, to], BACK_IN), (t2 + dur_out, [0, 0])]
    return Anim(k)


def arc(r, a0, a1, center=(0, 0), ry=None):
    """Circular/elliptical arc (degrees, 0 = right, clockwise with y down) as an open bezier()."""
    ry = r if ry is None else ry
    n = max(1, math.ceil(abs(a1 - a0) / 90))
    d = math.radians(a1 - a0) / n
    k = 4 / 3 * math.tan(d / 4)
    v, it, ot = [], [], []
    for i in range(n + 1):
        a = math.radians(a0) + i * d
        x, y = center[0] + r * math.cos(a), center[1] + ry * math.sin(a)
        tx, ty = -math.sin(a) * r * k, math.cos(a) * ry * k
        v.append((x, y))
        it.append((-tx, -ty))
        ot.append((tx, ty))
    return bezier(v, it, ot, closed=False)


def arc_path(r, a0, a1, center=(0, 0), name="arc", ry=None):
    return path(arc(r, a0, a1, center, ry), name)


def smooth_path(pts, closed=True, tension=0.5, name="smooth"):
    """Catmull-Rom style smooth path through the points."""
    n = len(pts)
    it, ot = [], []
    for i in range(n):
        if closed:
            p0, p2 = pts[(i - 1) % n], pts[(i + 1) % n]
        else:
            p0, p2 = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        tx, ty = (p2[0] - p0[0]) * tension / 3, (p2[1] - p0[1]) * tension / 3
        it.append((-tx, -ty))
        ot.append((tx, ty))
    return path(bezier(pts, it, ot, closed), name)


def smooth_bez(pts, closed=True, tension=0.5):
    return smooth_path(pts, closed, tension)["ks"]["k"]


def rect_tl(x, y, w, h, r=0, name="rect"):
    return rect((w, h), (x + w / 2, y + h / 2), r, name)


def vignette(w, h, strength=0.7, inner=0.45, color="#000000", mid=None):
    """Radial darkening towards the edges; transparent in the middle."""
    r = math.hypot(w, h) / 2
    stops = [(0, color, 0), (inner, color, 0)]
    if mid:
        stops.append(mid)
    stops.append((1, color, strength))
    return group([rect((w * 1.02, h * 1.02), (w / 2, h / 2)),
                  gradient_fill(stops, (w / 2, h / 2), (w / 2 + r, h / 2), radial=True)], "vignette")


def wedge(cx, cy, ang, r0, r1, w0, w1=0):
    """Tapered radial speed-line wedge from radius r0 (width w0) to r1 (width w1)."""
    c, s = math.cos(ang), math.sin(ang)
    nx, ny = -s, c
    p = lambda r, w: (cx + c * r + nx * w / 2, cy + s * r + ny * w / 2)
    q = lambda r, w: (cx + c * r - nx * w / 2, cy + s * r - ny * w / 2)
    return polyline([p(r1, w1), p(r0, w0), q(r0, w0), q(r1, w1)] if w1 else
                    [p(r1, w0), q(r1, w0), (cx + c * r0, cy + s * r0)], closed=True)


def speed_lines(cx, cy, n, r_in, r_out, width, seed, jitter=0.35, wobble=0.25):
    """Radial tapered lines pointing at (cx, cy): wide at the frame edge, sharp inside."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a = TAU * (i + rng.uniform(-jitter, jitter)) / n
        ri = r_in * (1 + rng.uniform(-wobble, wobble))
        out.append(wedge(cx, cy, a, ri, r_out, width * rng.uniform(0.4, 1.3)))
    return out


def shake_keys(t0, t1, amp, seed, step=1, decay=True, pivot=(0, 0)):
    """Random position jitter from t0 to t1 that settles to the pivot."""
    rng = random.Random(seed)
    k = []
    t = t0
    while t < t1:
        f = (1 - (t - t0) / (t1 - t0)) if decay else 1
        k.append((t, [pivot[0] + rng.uniform(-amp, amp) * f, pivot[1] + rng.uniform(-amp, amp) * f], LINEAR))
        t += step
    k.append((t1, list(pivot), LINEAR))
    return k


def glow_strokes(shapes, color="#FFFFFF", slot=None, width=6, core=True, widths=(5, 3, 1.8),
                 ops=(8, 16, 34), cap="round", extra=()):
    """Neon tube: wide faint strokes under a solid one, plus a white-hot core."""
    out = []
    shapes, extra = list(shapes), list(extra)
    if core:
        out.append(group(shapes + extra + [stroke("#FFFFFF", width=width * 0.38, opacity=85, cap=cap)], "core"))
    out.append(group(shapes + extra + [stroke(color, width=width, slot=slot, cap=cap)], "tube"))
    for m, o in zip(widths, ops):
        out.append(group(shapes + extra + [stroke(color, width=width * m, opacity=o, slot=slot, cap=cap)],
                         f"glow{m}"))
    return out


def sparkle(size, center=(0, 0)):
    """Four-point twinkle star."""
    s, k = size / 2, size * 0.09
    x, y = center
    return path(bezier([(x, y - s), (x + k, y - k), (x + s, y), (x + k, y + k), (x, y + s), (x - k, y + k),
                        (x - s, y), (x - k, y - k)]), "sparkle")


def arrow_pts(length, head_w, head_l, body_w, tip=(0, 0)):
    """Arrow pointing +x with its tip at `tip`; polygon points."""
    x, y = tip
    return [(x, y), (x - head_l, y - head_w / 2), (x - head_l, y - body_w / 2), (x - length, y - body_w / 2),
            (x - length, y + body_w / 2), (x - head_l, y + body_w / 2), (x - head_l, y + head_w / 2)]


def rot(p, a, c=(0, 0)):
    ca, sa = math.cos(a), math.sin(a)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)
