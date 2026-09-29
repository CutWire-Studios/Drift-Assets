"""Shared helpers for the broadcast2 batch (variant builds via drift_lottie).

Shapes are drawn in canvas coordinates. `lay()` / `rig()` put a layer's anchor on a pivot so
scale and rotation happen around it, with an optional animated [dx, dy] offset.
Layers added first draw on top.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from drift_lottie import *  # noqa: E402,F401,F403
from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import (Anim, Comp, HOLD, LINEAR, EASE_IN, EASE_OUT, EASE_IN_OUT, OVERSHOOT,  # noqa: E402,F401
                        SNAP_OUT, anim, bezier, transform, ellipse, fill, gradient_fill, group, path, polyline, rect,
                        repeater, star, stroke, trim, svg_shapes)

CAT = "broadcast"
SPRING = (0.3, 1.8, 0.55, 1.0)
DECEL = (0.2, 0.0, 0.1, 1.0)
EXPO_OUT = (0.16, 1.0, 0.3, 1.0)
EXPO_IN = (0.7, 0.0, 0.84, 0.0)
QUART_OUT = (0.25, 1.0, 0.5, 1.0)
INOUT = (0.76, 0.0, 0.24, 1.0)
BACK_IN = (0.5, -0.4, 0.8, 0.4)
SINE = (0.37, 0.0, 0.63, 1.0)


def keys(*k):
    return Anim(list(k))


def base(name, w, h, frames, intro_end=None, outro=None):
    c = Comp(name, w, h, fps=30, frames=frames)
    if intro_end is not None:
        c.marker("intro", 0, intro_end)
    if outro is not None:
        c.marker("outro", outro, frames - outro)
    return c


def io(a, b, t0, t1, t2=None, t3=None, ein=EXPO_OUT, eout=EXPO_IN):
    """a -> b over t0..t1, (hold, then b -> a over t2..t3)."""
    if t2 is None:
        return Anim([(t0, a, ein), (t1, b)])
    return Anim([(t0, a, ein), (t1, b, HOLD), (t2, b, eout), (t3, a)])


def fade(t0, t1, t2=None, t3=None, to=100):
    return io(0, to, t0, t1, t2, t3, EASE_OUT, EASE_IN)


def pop(t0, dur=14, t2=None, dur_out=8, spring=SPRING):
    k = [(t0, [0, 0], spring), (t0 + dur, [100, 100], HOLD if t2 else LINEAR)]
    if t2:
        k += [(t2, [100, 100], BACK_IN), (t2 + dur_out, [0, 0])]
    return Anim(k)


def rect_tl(x, y, w, h, r=0, name="rect"):
    return rect((w, h), (x + w / 2, y + h / 2), r, name)


def box(x, y, w, h, color="#FFFFFF", r=0, slot=None, opacity=100, name="box"):
    """Filled rectangle from its top-left corner."""
    return group([rect_tl(x, y, w, h, r), fill(color, opacity, slot=slot)], name)


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


def arc(r, a0, a1, center=(0, 0)):
    """Circular arc (degrees, 0 = right, clockwise with y down) as an open bezier()."""
    n = max(1, math.ceil(abs(a1 - a0) / 90))
    d = math.radians(a1 - a0) / n
    k = 4 / 3 * math.tan(d / 4)
    v, it, ot = [], [], []
    for i in range(n + 1):
        a = math.radians(a0) + i * d
        x, y = center[0] + r * math.cos(a), center[1] + r * math.sin(a)
        tx, ty = -math.sin(a) * r * k, math.cos(a) * r * k
        v.append((x, y))
        it.append((-tx, -ty))
        ot.append((tx, ty))
    return bezier(v, it, ot, closed=False)


def arc_path(r, a0, a1, center=(0, 0), name="arc"):
    return path(arc(r, a0, a1, center), name)


def glow_strokes(shapes, slot=None, color="#FFFFFF", width=6, core=True, widths=(30, 18, 10),
                 ops=(8, 15, 30), cap="round", extra=()):
    """Neon tube: wide faint strokes under a solid one, plus a white-hot core.

    extra: items (e.g. a trim) inserted after the shapes in every group.
    """
    out = []
    shapes, extra = list(shapes), list(extra)
    if core:
        out.append(group(shapes + extra + [stroke("#FFFFFF", width=width * 0.35, opacity=85, cap=cap)], "core"))
    out.append(group(shapes + extra + [stroke(color, width=width, slot=slot, cap=cap)], "tube"))
    for w_, o in zip(widths, ops):
        out.append(group(shapes + extra + [stroke(color, width=w_ * width / 6, opacity=o, slot=slot, cap=cap)],
                         f"glow{w_}"))
    return out


def soft_glow(shapes, slot=None, color="#FFFFFF", spread=(14, 30, 52), ops=(22, 12, 6)):
    """Fill + wide faint strokes of the same shape, for glowing solid shapes."""
    shapes = list(shapes)
    out = [group(shapes + [fill(color, slot=slot)], "body")]
    for s, o in zip(spread, ops):
        out.append(group(shapes + [stroke(color, width=s, opacity=o, slot=slot)], f"halo{s}"))
    return out


def corners(x0, y0, x1, y1, arm):
    """Four L-shaped corner brackets as polylines."""
    return [polyline([(x0, y0 + arm), (x0, y0), (x0 + arm, y0)]),
            polyline([(x1 - arm, y0), (x1, y0), (x1, y0 + arm)]),
            polyline([(x1, y1 - arm), (x1, y1), (x1 - arm, y1)]),
            polyline([(x0 + arm, y1), (x0, y1), (x0, y1 - arm)])]


def blink(frames, on_until, fade_frames=2):
    """Opacity that is on at 0, fades off at `on_until`, fades back on at the loop end."""
    return Anim([(0, 100, HOLD), (on_until, 100, EASE_IN_OUT), (on_until + fade_frames, 0, HOLD),
                 (frames - fade_frames, 0, EASE_IN_OUT), (frames, 100)])


def scanlines(comp, w, h, period=6, thick=2, opacity=14, frames=None, color="#000000", name="scanlines",
              drift=True):
    frames = frames or comp.frames
    pos = keys((0, [0, 0], LINEAR), (frames, [0, period * 2])) if drift else (0, 0)
    return comp.layer(name, [group([rect((w, thick), (w / 2, -period * 3)), fill(color),
                                    repeater(int(h // period) + 6, position=(0, period))], "lines")],
                      position=pos, opacity=opacity)


def vignette(w, h, strength=0.55, inner=0.55, color="#000000"):
    """Radial darkening towards the edges; transparent in the middle."""
    r = math.hypot(w, h) / 2
    return group([rect((w * 1.02, h * 1.02), (w / 2, h / 2)),
                  gradient_fill([(0, color, 0), (inner, color, 0), (1, color, strength)],
                                (w / 2, h / 2), (w / 2 + r, h / 2), radial=True)], "vignette")


def noise_rows(w, h, seed, row=6, color="#FFFFFF", density=0.45, min_len=4, max_len=60, n_dash=8,
               opacity=100, x0=-200):
    """Old-TV noise: each row is a dashed line with random dash/gap lengths."""
    rng = random.Random(seed)
    items = []
    for i in range(int(h // row) + 1):
        y = i * row + row / 2
        d = []
        for _ in range(n_dash):
            d.append(round(rng.uniform(min_len, max_len * density)))
            d.append(round(rng.uniform(min_len, max_len * (1 - density))))
        d.append(round(rng.uniform(0, 300)))
        items.append(group([polyline([(x0, y), (w - x0, y)]),
                            stroke(color, width=row, cap="butt", dashes=d, opacity=opacity)], f"r{i}"))
    return items


def mic_shapes(s=1.0, cx=0.0, cy=0.0):
    """Podcast mic outline (capsule, cradle, stand) centred on (cx, cy); ~ 60*s wide, 100*s tall."""
    c = lambda x, y: (cx + x * s, cy + y * s)
    capsule = rect((34 * s, 58 * s), c(0, -18), 17 * s, "capsule")
    cradle = path(arc(28 * s, 0, 180, c(0, -8)), "cradle")
    stem = polyline([c(0, 20), c(0, 38)], name="stem")
    foot = polyline([c(-16, 38), c(16, 38)], name="foot")
    return capsule, [cradle, stem, foot]


def mic_icon(s=1.0, cx=0.0, cy=0.0, color="#FFFFFF", slot=None, width=None, solid_capsule=True,
             opacity=100):
    capsule, rest = mic_shapes(s, cx, cy)
    w = width or 7 * s
    out = [group(rest + [stroke(color, width=w, slot=slot, opacity=opacity)], "stand")]
    if solid_capsule:
        out.append(group([capsule, fill(color, slot=slot, opacity=opacity)], "capsule"))
    else:
        out.append(group([capsule, stroke(color, width=w, slot=slot, opacity=opacity)], "capsule"))
    return out


def sparkle(size, cx=0.0, cy=0.0, pinch=0.18):
    """Four-point sparkle star path centred on (cx, cy)."""
    r, q = size / 2, size / 2 * pinch
    pts = [(cx, cy - r), (cx + q, cy - q), (cx + r, cy), (cx + q, cy + q), (cx, cy + r), (cx - q, cy + q),
           (cx - r, cy), (cx - q, cy - q)]
    return polyline(pts, closed=True, name="sparkle")


HEART = ("M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09"
         "C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z")
SEND = "M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"


def icon(d, size, center=(0, 0), box_=24.0, name="icon"):
    s = size / box_
    return svg_shapes(d, s, (center[0] - box_ * s / 2, center[1] - box_ * s / 2), name)


def lerp(a, b, t):
    return a + (b - a) * t


def wave_keys(frames, values, easing=SINE, start=0):
    """Seamless loop through `values` (first value repeated at the end)."""
    vals = list(values) + [values[0]]
    step = frames / (len(vals) - 1)
    return Anim([(start + round(i * step, 3), v, easing) for i, v in enumerate(vals)])


def bar_levels(rng, n, lo, hi, smooth=None):
    """n random levels between lo and hi; optionally biased by a 0..1 envelope value."""
    out = []
    for _ in range(n):
        v = rng.uniform(lo, hi)
        if smooth is not None:
            v = lo + (v - lo) * smooth
        out.append(v)
    return out


def inherit_opacity(comp):
    """Skottie does not pass a parent null's opacity to its children: wrap each child's shapes in a
    group carrying the (chained) null opacities instead."""
    by_ind = {L["ind"]: L for L in comp.layers}
    for L in comp.layers:
        if L["ty"] != 4:
            continue
        ops = []
        p = L.get("parent")
        while p is not None:
            P = by_ind[p]
            if P["ty"] == 3 and (P["ks"]["o"].get("a") or P["ks"]["o"].get("k") != 100):
                ops.append(P["ks"]["o"])
            p = P.get("parent")
        for o in ops:
            tr = transform(shape=True)
            tr["o"] = o
            L["shapes"] = [{"ty": "gr", "nm": "parent opacity", "it": L["shapes"] + [tr]}]
    return comp


def V(vid, name, comp, playback, **kw):
    """Variant() after making parent-null opacity work in Skottie."""
    return Variant(vid, name, inherit_opacity(comp), playback, **kw)
