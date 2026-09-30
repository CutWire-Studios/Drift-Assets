"""Shared conventions for the transitions category.

Every transition is a full 1920x1080 frame, 30 fps, played as intro-hold-outro:

    frame 0          empty (fully transparent)
    a0 .. a1         intro: the shapes cover the frame       (marker "intro" = 0 .. a1)
    a1 .. b0         hold: the frame is completely covered   (the editor cuts here and may stretch it)
    b0 .. b1         outro: the shapes reveal the next clip  (marker "outro" = b0 .. end)
    b1 .. n-1        empty again

A generator describes one covering "layer" as a function of its own timing tuple tm = (a0, a1, b0,
b1), so the same motion can be drawn flat (one colour) or stacked (primary / secondary / accent
following each other, see `stack()`).

    from _common import *
    t = Timing()                       # or Timing.snappy() / Timing.smooth()
    comp = base("my-wipe", t, "violet", slots=("primary",))
    panel(comp, "primary", t.tm)       # your drawing helper
    build("my-wipe", "My Wipe", "...", [...tags], [V("flat", "Flat", comp, t, "...")])
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from drift_lottie import *  # noqa: E402,F401,F403
from drift_lottie import Variant, build_asset  # noqa: E402
from lottie_kit import Comp, Anim, anim, bezier, path, rect, ellipse, fill, stroke, group, trim, \
    LINEAR, HOLD, EASE_IN_OUT  # noqa: E402

CATEGORY = "transitions"
W, H = 1920, 1080
CX, CY = W / 2, H / 2
C = (CX, CY)
HALF_DIAG = math.hypot(W, H) / 2  # ~1101: radius a centred shape needs to reach the corners

# Easings (out_x, out_y, in_x, in_y)
SMOOTH = (0.65, 0.0, 0.35, 1.0)      # cubic in-out: calm, even
SNAPPY = (0.76, 0.0, 0.24, 1.0)      # quart in-out: slow start, whip, hard settle
ACCEL = (0.6, 0.0, 0.9, 0.5)         # speeds up into the cut
DECEL = (0.1, 0.5, 0.4, 1.0)         # leaves the cut fast, settles
BACK = (0.3, 0.0, 0.3, 1.35)         # in-out with a little overshoot at the end
POP = (0.5, 0.0, 0.3, 1.2)           # slower build, small overshoot

PALETTES = {
    "violet": {"primary": "#5B3DF5", "secondary": "#FF4F8B", "accent": "#FFC93C"},
    "ocean": {"primary": "#0F5BFF", "secondary": "#18C8E8", "accent": "#B6F24A"},
    "sunset": {"primary": "#FF4D2E", "secondary": "#FF9F1C", "accent": "#FFE066"},
    "mint": {"primary": "#0E1B33", "secondary": "#12B8A6", "accent": "#F7D35C"},
    "cherry": {"primary": "#E8254F", "secondary": "#FF8FA8", "accent": "#FFF1F4"},
    "night": {"primary": "#15121F", "secondary": "#7B4DFF", "accent": "#2EE6D6"},
    "ember": {"primary": "#1A0D08", "secondary": "#E8441C", "accent": "#FFB43A"},
    "lime": {"primary": "#161A1D", "secondary": "#C6FF3D", "accent": "#FF3D7F"},
    "paper": {"primary": "#F4EFE6", "secondary": "#2B2B33", "accent": "#E24B3B"},
}


class Timing:
    """Frame layout of a transition. tm is the (a0, a1, b0, b1) tuple handed to layer helpers."""

    def __init__(self, intro=14, hold=10, outro=14, tail=2):
        self.a0, self.a1 = 0, intro
        self.b0 = intro + hold
        self.b1 = self.b0 + outro
        self.n = self.b1 + tail

    @classmethod
    def snappy(cls):
        return cls(10, 8, 10)

    @classmethod
    def smooth(cls):
        return cls(16, 10, 16)

    @property
    def tm(self):
        return (self.a0, self.a1, self.b0, self.b1)

    def thumb(self, frac=0.45):
        """Normalized time part-way through the intro (frame shape readable, partly covered)."""
        return (self.a0 + frac * (self.a1 - self.a0)) / self.n


def stack(t, lag=3, slots=("primary", "secondary", "accent")):
    """Timing for stacked colour layers, top layer first (add layers in this order).

    The bottom layer (last slot) leads the intro and trails the outro; the top one (first slot)
    arrives last and leaves first, so the colours peel back in order.
    """
    a0, a1, b0, b1 = t.tm
    k = len(slots) - 1
    out = []
    for i, s in enumerate(slots):
        d = (k - i) * lag
        out.append((s, (a0 + d, a1 - i * lag, b0 + i * lag, b1 - d)))
    return out


def base(name, t, palette="violet", slots=("primary",)):
    comp = Comp(name, W, H, fps=30, frames=t.n)
    comp.marker("intro", 0, t.a1)
    comp.marker("outro", t.b0, t.n - t.b0)
    pal = PALETTES[palette] if isinstance(palette, str) else palette
    for s in slots:
        comp.slot(s, pal[s])
    return comp


def io(tm, start, cover, end, ein=SMOOTH, eout=None):
    """Anim that goes start -> cover over the intro, holds, then cover -> end over the outro."""
    a0, a1, b0, b1 = tm
    return Anim([(a0, start, ein), (a1, cover, LINEAR), (b0, cover, eout or ein), (b1, end, LINEAR)])


def lerp(a, b, u):
    if isinstance(a, (list, tuple)):
        return [x + (y - x) * u for x, y in zip(a, b)]
    return a + (b - a) * u


def rot(p, deg, about=(0, 0)):
    r = math.radians(deg)
    x, y = p[0] - about[0], p[1] - about[1]
    return (about[0] + x * math.cos(r) - y * math.sin(r), about[1] + x * math.sin(r) + y * math.cos(r))


def poly(points, name="poly"):
    return path(bezier(points, closed=True), name)


def smooth_closed(points, tension=1.0):
    """Closed Catmull-Rom style bezier through points."""
    n = len(points)
    it, ot = [], []
    for i in range(n):
        p0, p2 = points[i - 1], points[(i + 1) % n]
        tx, ty = (p2[0] - p0[0]) / 6 * tension, (p2[1] - p0[1]) / 6 * tension
        it.append((-tx, -ty))
        ot.append((tx, ty))
    return bezier(points, it, ot, closed=True)


def smooth_open(points, tension=1.0):
    n = len(points)
    it, ot = [], []
    for i in range(n):
        p0, p2 = points[max(i - 1, 0)], points[min(i + 1, n - 1)]
        tx, ty = (p2[0] - p0[0]) / 6 * tension, (p2[1] - p0[1]) / 6 * tension
        it.append((-tx, -ty))
        ot.append((tx, ty))
    return bezier(points, it, ot, closed=False)


def blob_points(n, radius, seed, wobble=0.18, phase=0.0, center=(0, 0), stretch=(1, 1)):
    """n points round an organic blob; `phase` moves the wobble smoothly (for morphing keys)."""
    r = random.Random(seed)
    f = [(r.uniform(0, 6.28), r.uniform(0.5, 1.0)) for _ in range(3)]
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        w = sum(amp * math.sin(a * (k + 2) + ph + phase * (k + 1)) for k, (ph, amp) in enumerate(f)) / 2.2
        rr = radius * (1 + wobble * w)
        pts.append((center[0] + math.cos(a) * rr * stretch[0], center[1] + math.sin(a) * rr * stretch[1]))
    return pts


def cover_rect(margin=80):
    """Rect covering the whole canvas (plus margin), in canvas coordinates."""
    return rect((W + 2 * margin, H + 2 * margin), position=C)


def hole_group(hole_items, slot, name="hole", big=6000, **tr):
    """A huge sheet with holes (even-odd) — animate the holes growing to reveal."""
    return group([rect((big, big))] + list(hole_items) + [fill(slot=slot, even_odd=True)], name, **tr)


def V(vid, name, comp, t, description, thumb=0.45, region=(420, 0, 1080, 1080), bg=None, tags=None):
    """Transition variant: intro-hold-outro, no text area, square close-up thumbnail mid-intro."""
    return Variant(vid, name, comp, "intro-hold-outro", thumb_t=round(t.thumb(thumb), 4), region=region,
                   pad=0 if region else None, bg=bg, description=description, tags=tags)


def build(asset_id, name, description, tags, variants):
    build_asset(CATEGORY, asset_id, name, description, tags, variants)


def ease_at(e, u):
    """Evaluate an easing tuple (x1, y1, x2, y2) at progress u in 0..1 (cubic-bezier timing)."""
    if u <= 0:
        return 0.0
    if u >= 1:
        return 1.0
    x1, y1, x2, y2 = e

    def bz(a, b, s):
        return 3 * a * s * (1 - s) ** 2 + 3 * b * s * s * (1 - s) + s ** 3

    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if bz(x1, x2, mid) < u:
            lo = mid
        else:
            hi = mid
    return bz(y1, y2, (lo + hi) / 2)


def sampled(t0, t1, fn, ease=SMOOTH, step=2):
    """Keys from t0 to t1 every `step` frames of fn(eased_u, frame) (for paths that morph as they move)."""
    frames = list(range(int(t0), int(t1), step)) + [t1]
    return [(f, fn(ease_at(ease, (f - t0) / (t1 - t0)), f), LINEAR) for f in frames]


def inside(poly_pts, x, y):
    """Point-in-polygon (even-odd) for a list of (x, y)."""
    c = False
    n = len(poly_pts)
    for i in range(n):
        x1, y1 = poly_pts[i]
        x2, y2 = poly_pts[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def cover_scale(poly_pts, center=(0, 0), margin=40, step=24):
    """Smallest scale of poly_pts (about its origin, placed at canvas `center`) that holds the whole frame."""
    border = []
    for x in range(-margin, W + margin + 1, step):
        border += [(x, -margin), (x, H + margin)]
    for y in range(-margin, H + margin + 1, step):
        border += [(-margin, y), (W + margin, y)]
    lo, hi = 0.01, 100000.0
    for _ in range(40):
        mid = (lo + hi) / 2
        ok = all(inside(poly_pts, (x - center[0]) / mid, (y - center[1]) / mid) for x, y in border)
        if ok:
            hi = mid
        else:
            lo = mid
    return hi


GENTLE = (0.4, 0.0, 0.6, 1.0)


def zoom_curve(ease=GENTLE, k=5.0):
    """Scale fraction 0..1 over (eased) time growing exponentially, so the zoom reads at an even rate."""
    return lambda u: (math.exp(k * ease_at(ease, u)) - 1) / (math.exp(k) - 1)


def grow_open(comp, slot, tm, shape, scale, curve=None, out_curve=None, spin=(0, 0), outline=None, outline_w=0,
              center=C, name="shape", hole_shape=None, ein=SMOOTH, over=1.25):
    """A shape (bezier in its own units) zooms from nothing to `scale` (px per unit) to cover the frame, then a
    hole of the same shape zooms open from the middle to reveal. curve/out_curve: u -> fraction of the final
    scale (default zoom_curve()). spin: (degrees turned during intro, during outro)."""
    a0, a1, b0, b1 = tm
    s = scale * 100
    curve = curve or zoom_curve()
    out_curve = out_curve or zoom_curve(GENTLE, 4.0)
    ks = [(f, [s * curve((f - a0) / (a1 - a0))] * 2, LINEAR) for f in range(a0, a1 + 1)]
    items = [path(shape), fill(slot=slot)]
    if outline:
        items.insert(1, stroke(slot=outline, width=outline_w))
    comp.layer(name + "-in", [group(items, name, scale=Anim(ks), rotation=anim([(a0, -spin[0], ein), (a1, 0)]))],
               position=center, op=b0 + 1)
    hole = path(hole_shape or shape)
    hs = Anim([(f, [s * over * out_curve((f - b0) / (b1 - b0))] * 2, LINEAR) for f in range(b0, b1 + 1)])
    hr = anim([(b0, 0, SMOOTH), (b1, spin[1])])
    items = [group([rect((80000, 80000)), group([hole], "hole", scale=hs, rotation=hr),
                    fill(slot=slot, even_odd=True)], "sheet")]
    if outline:
        items.insert(0, group([hole, stroke(slot=outline, width=outline_w)], "rim", scale=hs, rotation=hr))
    comp.layer(name + "-out", items, position=center, ip=b0)
