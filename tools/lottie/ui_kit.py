"""Shared helpers for the app-ui, devices and status-icons batches (variant builds via drift_lottie).

Shapes are drawn in canvas coordinates. `lay()` / `rig()` put a layer's anchor on a pivot so scale
and rotation happen around it, with an optional animated [dx, dy] offset. Layers added first draw
on top. `label()` draws real words as outlined glyphs (Inter) so no font is needed at playback.

Slot convention for UI assets: background = window/card surface, primary = brand/accent fill
(sent bubble, header), secondary = secondary surface (received bubble, bars), icon = icons and
text, accent = highlight, outline = hairlines.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from drift_lottie import *  # noqa: E402,F401,F403
from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import (Anim, Comp, HOLD, LINEAR, EASE_IN, EASE_OUT, EASE_IN_OUT, OVERSHOOT,  # noqa: E402,F401
                        SNAP_OUT, anim, bezier, transform, ellipse, fill, gradient_fill, group, path, polyline, rect,
                        repeater, star, stroke, trim, svg_shapes, round_corners)
from text_paths import text, text_width  # noqa: E402,F401

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


def label(s, x, y, size, weight=400, slot="icon", color=None, anchor="l", opacity=100, tracking=0.0, name="label"):
    """Outlined text group with its baseline at y. Pass slot= for a colour slot or color= for a fixed hex."""
    f = fill(color, opacity, name="fill") if color else fill(slot=slot, opacity=opacity)
    return group(text(s, x, y, size, weight, anchor, tracking, name) + [f], name)


def circle(cx, cy, d, color=None, slot=None, opacity=100, name="circle", **kw):
    return group([ellipse((d, d), (cx, cy)), fill(color or "#FFFFFF", opacity, slot=slot)], name, **kw)


def line(points, width, color=None, slot=None, opacity=100, cap="round", name="line"):
    return group([polyline(points), stroke(color or "#FFFFFF", width, opacity, slot=slot, cap=cap)], name)


def hole_rect(outer, inner, ro=0, ri=0):
    """Even-odd frame: `outer` and `inner` are (x, y, w, h); returns shape items for a fill(even_odd=True)."""
    return [rect_tl(*outer, ro, "outer"), rect_tl(*inner, ri, "inner")]


def signal_bars(x, base_y, n=4, bar_w=10, gap=5, h0=14, step=10, filled=None, t0=0, stagger=4, slot="icon",
                dim=35, r=3):
    """Cellular bars standing on base_y from x. Bars `filled` (default all) pop up from the baseline at
    t0 + i*stagger; the others stay dimmed."""
    filled = n if filled is None else filled
    out = []
    for i in range(n):
        h = h0 + step * i
        bx = x + i * (bar_w + gap)
        out.append(group([rect_tl(bx, base_y - h, bar_w, h, r), fill(slot=slot, opacity=dim)], f"bar{i}-dim"))
        if i < filled:
            a = t0 + i * stagger
            out.append(group([rect_tl(bx, base_y - h, bar_w, h, r), fill(slot=slot)], f"bar{i}",
                             anchor=(bx + bar_w / 2, base_y), position=(bx + bar_w / 2, base_y),
                             scale=Anim([(a, [100, 0], OVERSHOOT), (a + 8, [100, 100])])))
    return out


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



def blink(frames, on_until, fade_frames=2):
    """Opacity that is on at 0, fades off at `on_until`, fades back on at the loop end."""
    return Anim([(0, 100, HOLD), (on_until, 100, EASE_IN_OUT), (on_until + fade_frames, 0, HOLD),
                 (frames - fade_frames, 0, EASE_IN_OUT), (frames, 100)])



def grow_rect(x, y, w, h, t0, t1, r=0, ease=LINEAR, from_right=False):
    """Rect (top-left x, y) whose width animates 0 -> w between t0 and t1."""
    if from_right:
        return rect(Anim([(t0, [0, h], ease), (t1, [w, h])]),
                    Anim([(t0, [x + w, y + h / 2], ease), (t1, [x + w / 2, y + h / 2])]), r)
    return rect(Anim([(t0, [0, h], ease), (t1, [w, h])]),
                Anim([(t0, [x, y + h / 2], ease), (t1, [x + w / 2, y + h / 2])]), r)


def level_rect(x, y, w, h, stops, r=0):
    """Rect from the left whose width follows stops [(frame, fraction 0..1), ...] (linear)."""
    return rect(Anim([(t, [max(w * f, 0.01), h], LINEAR) for t, f in stops]),
                Anim([(t, [x + w * f / 2, y + h / 2], LINEAR) for t, f in stops]), r)


def hold_on(t0, t1, frames):
    """Opacity 100 only between t0 and t1 (inclusive start, exclusive end)."""
    k = []
    if t0 > 0:
        k.append((0, 0, HOLD))
    k.append((t0, 100, HOLD))
    if t1 < frames:
        k.append((t1, 0, HOLD))
    if len(k) == 1:
        k.append((frames, k[0][1], HOLD))
    return Anim(k)


def rrect_d(x, y, w, h, tl=0, tr=0, br=0, bl=0):
    """SVG path string of a rect with individually rounded corners."""
    return (f"M{x + tl},{y} H{x + w - tr} " + (f"A{tr},{tr} 0 0 1 {x + w},{y + tr} " if tr else "") +
            f"V{y + h - br} " + (f"A{br},{br} 0 0 1 {x + w - br},{y + h} " if br else "") +
            f"H{x + bl} " + (f"A{bl},{bl} 0 0 1 {x},{y + h - bl} " if bl else "") +
            f"V{y + tl} " + (f"A{tl},{tl} 0 0 1 {x + tl},{y} " if tl else "") + "Z")


def rrect_path(x, y, w, h, tl=0, tr=0, br=0, bl=0, name="rrect"):
    return svg_shapes(rrect_d(x, y, w, h, tl, tr, br, bl), name=name)
