"""Shared helpers for the infographics category (bars, rings, charts and gauges).

Three house styles recur across the category so a user can build a matching dashboard:
  flat   - clean modern shapes, soft tracks, no card;
  neon   - dark glass panel, glowing tubes with a white-hot core;
  sketch - paper card, wobbly ink outlines and marker scribble fills.

Shapes are drawn in canvas coordinates; `lay()` / `rig()` pivot a layer about a point.
Layers added first draw on top. No digits or letters are drawn anywhere: every value and
label is a text area.
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
                        SNAP_OUT, anim, bezier, ellipse, fill, gradient_fill, group, path, polyline, rect,
                        repeater, star, stroke, trim)

CAT = "infographics"
V = Variant
SPRING = (0.3, 1.8, 0.55, 1.0)
SOFT_SPRING = (0.3, 1.45, 0.55, 1.0)
DECEL = (0.2, 0.0, 0.1, 1.0)
EXPO_OUT = (0.16, 1.0, 0.3, 1.0)
EXPO_IN = (0.7, 0.0, 0.84, 0.0)
QUART_OUT = (0.25, 1.0, 0.5, 1.0)
INOUT = (0.76, 0.0, 0.24, 1.0)
BACK_IN = (0.5, -0.4, 0.8, 0.4)
SINE = (0.37, 0.0, 0.63, 1.0)

# house palettes (defaults for the colour slots)
FLAT = {"primary": "#5B6CFF", "secondary": "#FF6B8A", "accent": "#FFC247", "icon": "#2ED3A0",
        "background": "#FFFFFF", "outline": "#FFFFFF"}
NEON = {"primary": "#23E5FF", "secondary": "#FF3DCB", "accent": "#B6FF3B", "icon": "#FFB23D",
        "background": "#0D1024", "outline": "#23E5FF"}
SKETCH = {"primary": "#FF5A4E", "secondary": "#3D8BFF", "accent": "#FFC83D", "icon": "#35C27A",
          "background": "#FFF9EC", "outline": "#26262E"}
INK_W = 4.5


def keys(*k):
    return Anim(list(k))


def slots(comp, pal, *ids):
    for i in ids:
        comp.slot(i, pal[i])


def fade(t0, t1, to=100, t2=None, t3=None):
    k = [(t0, 0, EASE_OUT), (t1, to, HOLD if t2 is not None else LINEAR)]
    if t2 is not None:
        k += [(t2, to, EASE_IN), (t3, 0)]
    return Anim(k)


def pop(t0, dur=14, spring=SPRING, s0=0):
    return Anim([(t0, [s0, s0], spring), (t0 + dur, [100, 100])])


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


def rect_tl(x, y, w, h, r=0, name="rect"):
    return rect((w, h), (x + w / 2, y + h / 2), r, name)


def box(x, y, w, h, color="#FFFFFF", r=0, slot=None, opacity=100, name="box"):
    return group([rect_tl(x, y, w, h, r), fill(color, opacity, slot=slot)], name)


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


def pt(c, r, a):
    """Point at angle a (degrees, 0 = right, clockwise) and radius r around c."""
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def ease_eval(e, u):
    """Evaluate a kit easing tuple at progress u (0..1)."""
    if e == HOLD:
        return 0.0 if u < 1 else 1.0
    x1, y1, x2, y2 = e
    if u <= 0:
        return 0.0
    if u >= 1:
        return 1.0

    def bz(a, b, t):
        return 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3

    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if bz(x1, x2, mid) < u:
            lo = mid
        else:
            hi = mid
    return bz(y1, y2, (lo + hi) / 2)


def first_frame(e, t0, t1, target):
    """First frame in t0..t1 at which the eased 0..1 progress reaches `target`."""
    for f in range(int(t0), int(t1) + 1):
        if ease_eval(e, (f - t0) / (t1 - t0)) >= target - 1e-6:
            return f
    return t1


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------- neon

def glow_strokes(shapes, slot=None, color="#FFFFFF", width=6, core=True, widths=(30, 18, 10),
                 ops=(8, 15, 30), cap="round", extra=(), name="neon"):
    """Neon tube: wide faint strokes under a solid one, plus a white-hot core.
    extra: items (e.g. a trim) inserted after the shapes in every group."""
    out = []
    shapes, extra = list(shapes), list(extra)
    if core:
        out.append(group(shapes + extra + [stroke("#FFFFFF", width=width * 0.35, opacity=85, cap=cap)],
                         f"{name}-core"))
    out.append(group(shapes + extra + [stroke(color, width=width, slot=slot, cap=cap)], f"{name}-tube"))
    for w_, o in zip(widths, ops):
        out.append(group(shapes + extra + [stroke(color, width=w_ * width / 6, opacity=o, slot=slot, cap=cap)],
                         f"{name}-glow{w_}"))
    return out


def soft_glow(shapes, slot=None, color="#FFFFFF", spread=(12, 26, 44), ops=(24, 12, 6), body_opacity=100):
    """Fill + wide faint strokes of the same shape, for glowing solid shapes."""
    shapes = list(shapes)
    out = [group(shapes + [fill(color, body_opacity, slot=slot)], "body")]
    for s, o in zip(spread, ops):
        out.append(group(shapes + [stroke(color, width=s, opacity=o, slot=slot)], f"halo{s}"))
    return out


def neon_panel(comp, x, y, w, h, t0=0, r=28, grid=None, name="panel", parent=None, border_slot="outline"):
    """Dark glass panel with a faint border (and optional grid spacing) that fades/zooms in."""
    cx, cy = x + w / 2, y + h / 2
    sc = keys((t0, [94, 94], EXPO_OUT), (t0 + 16, [100, 100]))
    op = fade(t0, t0 + 8)
    items = [group([rect((w, h), (cx, cy), r), stroke(slot=border_slot, width=2.5, opacity=45)], "border"),
             group([rect((w - 10, h - 10), (cx, cy), r - 5), stroke("#FFFFFF", width=1, opacity=8)], "inner")]
    comp.layer(f"{name}-border", items, anchor=(cx, cy), position=(cx, cy), scale=sc, opacity=op, parent=parent)
    if grid:
        g = []
        gx = x + grid
        while gx < x + w - grid / 2:
            g.append(polyline([(gx, y + 14), (gx, y + h - 14)]))
            gx += grid
        gy = y + grid
        while gy < y + h - grid / 2:
            g.append(polyline([(x + 14, gy), (x + w - 14, gy)]))
            gy += grid
        comp.layer(f"{name}-grid", [group(g + [stroke(slot=border_slot, width=1, opacity=10)], "grid")],
                   anchor=(cx, cy), position=(cx, cy), scale=sc, opacity=op, parent=parent)
    comp.layer(f"{name}-fill", [group([rect((w, h), (cx, cy), r), fill(slot="background", opacity=90)], "glass"),
                                group([rect((w + 24, h + 24), (cx, cy + 10), r + 12), fill("#000000", 18)], "shadow")],
               anchor=(cx, cy), position=(cx, cy), scale=sc, opacity=op, parent=parent)


# ---------------------------------------------------------------- sketch (hand drawn)

def catmull(points, samples=10, closed=False):
    pts = list(points)
    if closed:
        pts = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        pts = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * t
                                    + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(tuple(pts[-2]))
    return out


def densify(points, step=40):
    """Insert points along each segment every ~step px."""
    out = [points[0]]
    for a, b in zip(points, points[1:]):
        n = max(1, round(math.dist(a, b) / step))
        for i in range(1, n + 1):
            out.append((lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)))
    return out


def wobble(points, amp=2.0, seed=0, step=40, samples=6):
    """Hand-drawn version of a polyline: densified, jittered, smoothed (open)."""
    rnd = random.Random(seed)
    d = densify(points, step)
    j = [(x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)) for x, y in d]
    j[0], j[-1] = d[0], d[-1]
    return catmull(j, samples)


def sk_path(points, name="ink"):
    return path(bezier(points, closed=False), name)


def sketch_rect_pts(x, y, w, h, seed=0, amp=2.2, over=8, step=46):
    """Open wobbly rectangle that starts just before the top-left and overshoots it at the end."""
    rnd = random.Random(seed)
    o = over
    pts = [(x - o * 0.4, y + rnd.uniform(-1, 2)), (x + w, y), (x + w, y + h), (x, y + h), (x, y - 2),
           (x + o * 1.6, y - rnd.uniform(0, 3))]
    return wobble(pts, amp, seed, step)


def sketch_line_pts(a, b, seed=0, amp=1.6, step=46):
    return wobble([a, b], amp, seed, step)


def sketch_circle_pts(c, rx, ry=None, seed=0, amp=0.03, turns=1.07, n=28, a0=-100):
    """Open wobbly ellipse drawn a little past a full turn, like a quick pen loop."""
    rnd = random.Random(seed)
    ry = rx if ry is None else ry
    m = int(n * turns)
    pts = []
    for i in range(m + 1):
        a = math.radians(a0 + 360 * i / n)
        k = 1 + rnd.uniform(-amp, amp) + 0.04 * i / m
        pts.append((c[0] + rx * k * math.cos(a), c[1] + ry * k * math.sin(a)))
    return catmull(pts, 4)


def ink(pts_list, width=INK_W, slot="outline", draw=None, color="#26262E", opacity=100, name="ink"):
    """Ink strokes (list of point lists); draw=(t0, t1[, easing]) draws them on with a trim."""
    items = [sk_path(p, f"{name}{i}") for i, p in enumerate(pts_list)]
    if draw:
        e = draw[2] if len(draw) > 2 else EASE_IN_OUT
        items.append(trim(end=keys((draw[0], 0, e), (draw[1], 100))))
    items.append(stroke(color, width=width, slot=slot, opacity=opacity))
    return group(items, name)


def scribble_pts(x, y, w, h, spacing=14, slant=20, seed=0, over=2):
    """Zig-zag marker scribble covering the rect, left to right."""
    rnd = random.Random(seed)
    pts = []
    n = max(2, int(w / spacing) + 1)
    for i in range(n + 1):
        xx = x + i * w / n
        if i % 2 == 0:
            pts.append((xx + slant / 2 + rnd.uniform(-2, 2), y - over + rnd.uniform(-2, 2)))
        else:
            pts.append((xx - slant / 2 + rnd.uniform(-2, 2), y + h + over + rnd.uniform(-2, 2)))
    return pts


def scribble_v_pts(x, y, w, h, spacing=14, slant=8, seed=0, over=4):
    """Zig-zag scribble covering the rect, bottom to top (horizontal strokes)."""
    rnd = random.Random(seed)
    pts = []
    n = max(2, int(h / spacing) + 1)
    for i in range(n + 1):
        yy = y + h - i * h / n
        if i % 2 == 0:
            pts.append((x - over + rnd.uniform(-2, 2), yy + slant / 2 + rnd.uniform(-2, 2)))
        else:
            pts.append((x + w + over + rnd.uniform(-2, 2), yy - slant / 2 + rnd.uniform(-2, 2)))
    return pts


def marker(pts, width, slot="primary", draw=None, opacity=88, name="marker", color="#FF5A4E"):
    items = [polyline(pts, name="scribble")]
    if draw:
        e = draw[2] if len(draw) > 2 else EASE_IN_OUT
        items.append(trim(end=keys((draw[0], 0, e), (draw[1], 100))))
    items.append(stroke(color, width=width, slot=slot, opacity=opacity, join="round"))
    return group(items, name)


class Paper:
    """Off-white paper card (background slot) with a soft shadow, dropped in with a little tilt.

        card = Paper(comp, x, y, w, h)     # creates the rig null (parent contents to card.rig)
        ... add content layers with parent=card.rig ...
        card.sheet()                        # adds the sheet last, so it draws underneath
    """

    def __init__(self, comp, x, y, w, h, t0=0, r=18, tilt=-1.2, name="paper", parent=None, lines=None):
        self.comp, self.x, self.y, self.w, self.h, self.t0, self.r = comp, x, y, w, h, t0, r
        self.name, self.lines = name, lines
        cx, cy = x + w / 2, y + h / 2
        self.rig = rig(comp, name, (cx, cy), parent=parent,
                       rotation=keys((t0, tilt - 4, EXPO_OUT), (t0 + 18, tilt)),
                       scale=keys((t0, [90, 90], SOFT_SPRING), (t0 + 16, [100, 100])))

    def sheet(self):
        comp, x, y, w, h, r, name = self.comp, self.x, self.y, self.w, self.h, self.r, self.name
        cx, cy = x + w / 2, y + h / 2
        op = fade(self.t0, self.t0 + 6)
        if self.lines:
            ls = []
            yy = y + self.lines
            while yy < y + h - 10:
                ls.append(polyline([(x + 18, yy), (x + w - 18, yy)]))
                yy += self.lines
            comp.layer(f"{name}-rules", [group(ls + [stroke("#5A8BD8", width=1.5, opacity=22)], "rules")],
                       parent=self.rig, opacity=op)
        comp.layer(f"{name}-sheet", [group([rect((w, h), (cx, cy), r), fill(slot="background")], "sheet"),
                                     group([rect((w, h), (cx + 3, cy + 8), r), fill("#000000", 22)], "shadow"),
                                     group([rect((w + 14, h + 14), (cx + 4, cy + 14), r + 7), fill("#000000", 10)],
                                           "shadow2")],
                   parent=self.rig, opacity=op)


def tape(comp, c, w=90, h=30, rot=-8, t0=0, parent=None, name="tape"):
    comp.layer(name, [group([rect((w, h), c, 3), fill("#FFFFFF", 45)], "tape"),
                      group([rect((w, h), (c[0], c[1] + 2), 3), fill("#000000", 8)], "tape-sh")],
               anchor=c, position=c, rotation=rot, parent=parent,
               scale=keys((t0, [0, 100], EXPO_OUT), (t0 + 10, [100, 100])), opacity=fade(t0, t0 + 3))


# ---------------------------------------------------------------- flat bits

def glint_band(comp, matte_shapes, x0, x1, cy, h, t0, t1, parent=None, name="glint", width=40, opacity=55,
               ip=0):
    """A soft white diagonal band sweeping x0 -> x1, clipped to `matte_shapes` (alpha matte)."""
    comp.layer(f"{name}-matte", matte_shapes, parent=parent, ip=ip)
    comp.layer(name, [group([rect((width, h * 3), (0, 0)),
                             gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 1), (1, "#FFFFFF", 0)],
                                           (-width / 2, 0), (width / 2, 0))], "band", rotation=18)],
               parent=parent, matte="alpha", opacity=opacity, ip=ip,
               position=keys((t0, [x0, cy], EASE_IN_OUT), (t1, [x1, cy])))


def spark(comp, c, t0, color="#FFFFFF", size=46, name="spark", parent=None, slot=None):
    """Four-point twinkle that flashes at c."""
    s = size
    pts = [(0, -s / 2), (s * 0.09, -s * 0.09), (s / 2, 0), (s * 0.09, s * 0.09), (0, s / 2),
           (-s * 0.09, s * 0.09), (-s / 2, 0), (-s * 0.09, -s * 0.09)]
    comp.layer(name, [group([polyline(pts, closed=True), fill(color, slot=slot)], "twinkle")],
               position=c, parent=parent, ip=t0, op=t0 + 16,
               scale=keys((t0, [0, 0], EASE_OUT), (t0 + 6, [100, 100], EASE_IN), (t0 + 16, [0, 0])),
               rotation=keys((t0, 0, LINEAR), (t0 + 16, 45)))


def ring_pulse(comp, c, t0, r0, r1, slot="primary", width=4, dur=18, name="ripple", parent=None, yscale=100,
               color="#FFFFFF"):
    comp.layer(name, [group([ellipse((r0 * 2, r0 * 2)), stroke(color, width=width, slot=slot)], "ring")],
               position=c, parent=parent, ip=t0, op=t0 + dur + 1,
               scale=keys((t0, [100, yscale], DECEL), (t0 + dur, [r1 / r0 * 100, r1 / r0 * yscale])),
               opacity=keys((t0, 100, EASE_IN), (t0 + dur, 0)))


def burst_lines(comp, c, t0, r0, r1, n=8, slot="accent", width=5, rot=0, name="burst", parent=None,
                color="#FFFFFF", dur=14):
    ls = [polyline([pt((0, 0), r0, rot + i * 360 / n), pt((0, 0), r1, rot + i * 360 / n)]) for i in range(n)]
    comp.layer(name, [group(ls + [trim(start=keys((t0 + 3, 0, EASE_OUT), (t0 + dur, 100)),
                                       end=keys((t0, 0, EASE_OUT), (t0 + dur - 4, 100))),
                                  stroke(color, width=width, slot=slot)], "rays")],
               position=c, parent=parent, ip=t0, op=t0 + dur + 1)


def tick_shape(c, s=1.0):
    return polyline([(c[0] - 11 * s, c[1] + 1 * s), (c[0] - 3 * s, c[1] + 9 * s), (c[0] + 12 * s, c[1] - 9 * s)])


def arrow_head(tip, frm, size=16, spread=32):
    """Open V arrow head polyline at `tip`, pointing away from `frm`."""
    a = math.degrees(math.atan2(tip[1] - frm[1], tip[0] - frm[0]))
    return [pt(tip, size, a + 180 - spread), tip, pt(tip, size, a + 180 + spread)]


def top_round_bar(cx, w, top, bottom, r):
    """Closed bezier of a bar with rounded top corners and a square bottom."""
    k = 0.5523 * r
    x0, x1 = cx - w / 2, cx + w / 2
    v = [(x0, bottom), (x0, top + r), (x0 + r, top), (x1 - r, top), (x1, top + r), (x1, bottom)]
    it = [(0, 0), (0, 0), (-k, 0), (0, 0), (0, -k), (0, 0)]
    ot = [(0, 0), (0, -k), (0, 0), (k, 0), (0, 0), (0, 0)]
    return bezier(v, it, ot, closed=True)
