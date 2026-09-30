"""Shared helpers for the lt2 batch of lower thirds (variant builds via drift_lottie).

Shapes are drawn in canvas coordinates. `lay()` / `rig()` put the layer's anchor on a pivot so
scale and rotation happen around it, and take an optional animated [dx, dy] offset.
Layers added first draw on top.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from _common import EXPO_OUT, QUART_OUT, EXPO_IN, CUBIC_IN, INOUT, SOFT_OUT, io, keys  # noqa: E402,F401
from drift_lottie import *  # noqa: E402,F401,F403
from drift_lottie import Variant, build_asset  # noqa: E402
from lottie_kit import Anim, HOLD, LINEAR, EASE_IN, EASE_OUT, EASE_IN_OUT, OVERSHOOT, SNAP_OUT  # noqa: E402

N = 150      # 5 s
OUT = 120    # outro marker start
SPRING = (0.3, 1.8, 0.55, 1.0)
BACK_IN = (0.5, -0.4, 0.8, 0.4)


def base(name, w, h, intro_end, frames=N, outro=OUT):
    c = Comp(name, w, h, fps=30, frames=frames)
    c.marker("intro", 0, intro_end)
    c.marker("outro", outro, frames - outro)
    return c


def at(pivot, off=None):
    if off is None:
        return pivot
    return Anim([(t, [v[0] + pivot[0], v[1] + pivot[1]], e) for t, v, e in off.keys])


def lay(comp, name, shapes, pivot=(0, 0), off=None, **kw):
    """Shape layer drawn in canvas coords, scaling/rotating about `pivot`, moved by `off`."""
    return comp.layer(name, shapes, anchor=pivot, position=at(pivot, off), **kw)


def rig(comp, name, pivot=(0, 0), off=None, **kw):
    """Null whose children keep canvas coords; scale/rotation about `pivot`."""
    return comp.null(name, anchor=pivot, position=at(pivot, off), **kw)


# ---------------------------------------------------------------- timing curves

def grow_x(t0, t1, t2, t3, ein=EXPO_OUT, eout=EXPO_IN):
    return io([0, 100], [100, 100], t0, t1, t2, t3, ein, eout)


def grow_y(t0, t1, t2, t3, ein=EXPO_OUT, eout=EXPO_IN):
    return io([100, 0], [100, 100], t0, t1, t2, t3, ein, eout)


def grow(t0, t1, t2, t3, ein=EXPO_OUT, eout=EXPO_IN):
    return io([0, 0], [100, 100], t0, t1, t2, t3, ein, eout)


def pop(t0, t1, t2, t3, peak=110, ein=SPRING):
    """0 -> 100 with overshoot; outro swells to `peak` then shrinks to 0."""
    m = t2 + (t3 - t2) * 0.35
    return keys((t0, [0, 0], ein), (t1, [100, 100], HOLD), (t2, [100, 100], EASE_OUT),
                (m, [peak, peak], EXPO_IN), (t3, [0, 0]))


def fade(t0, t1, t2, t3, v=100, ein=EASE_OUT, eout=EASE_IN):
    return io(0, v, t0, t1, t2, t3, ein, eout)


def slide(dx, dy, t0, t1, t2, t3, ein=EXPO_OUT, eout=EXPO_IN, odx=None, ody=None):
    """Offset anim: from (dx, dy) to rest, then out to (odx, ody) (defaults to the entry offset)."""
    odx = dx if odx is None else odx
    ody = dy if ody is None else ody
    return keys((t0, [dx, dy], ein), (t1, [0, 0], HOLD), (t2, [0, 0], eout), (t3, [odx, ody]))


def draw(t0, t1, t2, t3, ein=INOUT, eout=INOUT):
    """Trim that draws on (end 0->100) and erases from the start on the outro."""
    return trim(end=keys((t0, 0, ein), (t1, 100)), start=keys((t2, 0, eout), (t3, 100)))


def draw_rev(t0, t1, t2, t3, ein=INOUT, eout=INOUT):
    """Draws on, then retracts back the way it came."""
    return trim(end=keys((t0, 0, ein), (t1, 100, HOLD), (t2, 100, eout), (t3, 0)))


def flicker(t0, t_out, pattern=None, out_pattern=None, v=100):
    """Neon-style hold-keyed opacity flicker on, and off again at t_out."""
    pattern = pattern or [(0, 0), (2, v), (4, 15), (6, v), (9, 30), (10, v * 0.6), (13, v)]
    out_pattern = out_pattern or [(0, v), (3, 20), (5, v), (8, 0)]
    k = [(0, 0, HOLD)] if t0 > 0 else []
    k += [(t0 + dt, val, HOLD) for dt, val in pattern]
    k += [(t_out + dt, val, HOLD) for dt, val in out_pattern]
    return keys(*k)


def glitch_off(t_in, t_out, amp=36, steps=6, seed=3, dur=2):
    """Hold-keyed [dx, dy] jitter settling at t_in + steps*dur, and again from t_out."""
    rng = random.Random(seed)
    k = []
    for i in range(steps):
        a = amp * (1 - i / steps)
        k.append((t_in + i * dur, [rng.uniform(-a, a), rng.uniform(-a, a) * 0.25], HOLD))
    k.append((t_in + steps * dur, [0, 0], HOLD))
    for i in range(steps):
        a = amp * (i + 1) / steps
        k.append((t_out + i * dur, [rng.uniform(-a, a), rng.uniform(-a, a) * 0.25], HOLD))
    k.append((t_out + steps * dur, [0, 0]))
    return keys(*k)


def glitch_vis(t_in, t_out, steps=6, dur=2, seed=5):
    """Hold-keyed opacity: stutters on at t_in, stutters off from t_out (ends at 0)."""
    rng = random.Random(seed)
    k = [(0, 0, HOLD)] if t_in > 0 else []
    for i in range(steps):
        k.append((t_in + i * dur, rng.choice([0, 100, 100, 40]), HOLD))
    k.append((t_in + steps * dur, 100, HOLD))
    for i in range(steps):
        k.append((t_out + i * dur, rng.choice([0, 100, 60, 0]), HOLD))
    k.append((t_out + steps * dur, 0, HOLD))
    k.append((t_out + steps * dur + 1, 0))
    return keys(*k)


def ghost_vis(t_in, t_out, steps=6, dur=2):
    """Opacity for RGB-split ghost copies: visible only while glitching."""
    return keys((0, 0, HOLD), (t_in, 80, HOLD), (t_in + steps * dur, 0, HOLD),
                (t_out, 80, HOLD), (t_out + steps * dur, 0, HOLD), (t_out + steps * dur + 1, 0))


def glitch_ghosts(comp, shapes_fn, t_in, t_out, amp=14, parent=None, colors=("#FF2BD6", "#22E5FF")):
    """Two tinted copies (drawn under the real layer) that jitter while glitching."""
    for i, col in enumerate(colors):
        lay(comp, f"ghost-{i}", shapes_fn(col), off=glitch_off(t_in, t_out, amp, seed=11 + i),
            opacity=ghost_vis(t_in, t_out), parent=parent)


# ---------------------------------------------------------------- shapes

def rrect(x, y, w, h, r=0, name="rect"):
    """Rounded rect from its top-left corner."""
    return rect((w, h), (x + w / 2, y + h / 2), r, name)


def poly(points, closed=True, name="poly"):
    return polyline(points, closed, name)


def para(x, y, w, h, k=0.26, name="para"):
    """Parallelogram leaning right; (x, y+h) is the bottom-left corner."""
    s = h * k
    return poly([(x + s, y), (x + w + s, y), (x + w, y + h), (x, y + h)], name=name)


def chamfer(x, y, w, h, c, corners=(1, 0, 1, 0), name="chamfer"):
    """Rect with 45-degree cut corners; corners flags: (tl, tr, br, bl)."""
    tl, tr, br, bl = [c * f for f in corners]
    pts = [(x + tl, y), (x + w - tr, y), (x + w, y + tr), (x + w, y + h - br), (x + w - br, y + h),
           (x + bl, y + h), (x, y + h - bl), (x, y + tl)]
    return poly(pts, name=name)


def diamond(cx, cy, r, name="diamond"):
    return poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], name=name)


def sparkle(cx, cy, r, thin=0.22, name="sparkle"):
    """Four-point twinkle star made of curved beziers."""
    v = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    k = r * (1 - thin)  # tangents point at the centre so the arms are concave
    t = [(0.0, k), (-k, 0.0), (0.0, -k), (k, 0.0)]
    return path(bezier(v, t, t, True), name)


def shadow(x, y, w, h, r=0, dy=10, n=4, spread=5, op=7, color="#000000"):
    """Soft drop shadow faked with stacked translucent rounded rects."""
    return [group([rrect(x - i * spread, y + dy - i * spread * 0.6, w + 2 * i * spread, h + 1.2 * i * spread,
                         r + i * spread), fill(color, op)], f"shadow{i}") for i in range(n)]


def glow_strokes(shapes, slot=None, color="#FFFFFF", width=6, core=True, widths=(30, 18, 10), ops=(9, 16, 30)):
    """Neon tube: wide faint strokes under a solid one, plus a white-hot core."""
    out = []
    if core:
        out.append(group(list(shapes) + [stroke("#FFFFFF", width=width * 0.35, opacity=85)], "core"))
    out.append(group(list(shapes) + [stroke(color, width=width, slot=slot)], "tube"))
    for w_, o in zip(widths, ops):
        out.append(group(list(shapes) + [stroke(color, width=w_ * width / 6, opacity=o, slot=slot)], f"glow{w_}"))
    return out


def sheen(comp, matte_shapes, x0, x1, y0, y1, t0, t1, parent=None, width=90, op=26, angle=22):
    """Diagonal light band sweeping x0 -> x1, clipped to matte_shapes."""
    comp.layer("sheen-matte", list(matte_shapes) + [fill("#FFFFFF")], parent=parent)
    h = (y1 - y0) * 2.2
    band = [group([rect((width, h)), fill("#FFFFFF", op)], "band", rotation=angle),
            group([rect((width * 0.22, h)), fill("#FFFFFF", op)], "band2", position=(width * 0.9, 0),
                  rotation=angle)]
    cy = (y0 + y1) / 2
    comp.layer("sheen", band, parent=parent, matte="alpha",
               position=keys((t0, [x0 - width * 2, cy], (0.45, 0, 0.3, 1)), (t1, [x1 + width * 2, cy])))


def wipe(comp, name, shapes, box, t0, t1, t2, t3, side="left", parent=None, ein=EXPO_OUT, eout=EXPO_IN,
         out_side=None, **kw):
    """Content revealed by a rect matte growing from `side` (left/right/top/bottom/centre)."""
    x, y, w, h = box
    piv = {"left": (x, y + h / 2), "right": (x + w, y + h / 2), "top": (x + w / 2, y),
           "bottom": (x + w / 2, y + h), "centre": (x + w / 2, y + h / 2)}
    sc = {"left": grow_x, "right": grow_x, "top": grow_y, "bottom": grow_y, "centre": grow_x}[side]
    out_side = out_side or side
    if out_side == side:
        s = sc(t0, t1, t2, t3, ein, eout)
        lay(comp, f"{name}-matte", [rrect(x, y, w, h), fill("#FFFFFF")], piv[side], scale=s, parent=parent)
    else:  # enter from one side, leave toward the other: two stacked mattes are not possible, so slide
        dx = {"left": -w, "right": w}[side]
        odx = {"left": -w, "right": w}[out_side]
        comp.layer(f"{name}-matte", [rrect(x, y, w, h), fill("#FFFFFF")], parent=parent,
                   position=slide(dx, 0, t0, t1, t2, t3, ein, eout, odx=odx, ody=0))
    return comp.layer(name, shapes, parent=parent, matte="alpha", **kw)


def row(x, y, w, h):
    return [round(x), round(y), round(w), round(h)]


def V(vid, name, comp, head, sub=None, extra=None, description=None, thumb_t=0.5, bg=None, **kw):
    """Variant with a headline (and optional subtitle / extra named) text area."""
    areas = None
    if sub or extra:
        areas = {"headline": row(*head)}
        if sub:
            areas["subtitle"] = row(*sub)
        areas.update({k: row(*v) for k, v in (extra or {}).items()})
    return Variant(vid, name, comp, "intro-hold-outro", text_area=row(*head), text_areas=areas,
                   thumb_t=thumb_t, bg=bg, description=description, **kw)


def _trims_first(items):
    """Skottie applies a trim only to styles listed after it; move trims ahead of fills/strokes."""
    styles = ("st", "fl", "gf", "gs")
    first = next((i for i, it in enumerate(items) if it.get("ty") in styles), None)
    if first is not None:
        tms = [it for it in items[first:] if it.get("ty") == "tm"]
        if tms:
            rest = [it for it in items[first:] if it.get("ty") != "tm"]
            items[first:] = tms + rest
    for it in items:
        if it.get("ty") == "gr":
            _trims_first(it["it"])


def _inherit_opacity(comp):
    """Lottie parenting does not pass opacity down; give rig children their null's opacity fade."""
    by_ind = {L["ind"]: L for L in comp.layers}
    for L in comp.layers:
        if L["ks"]["o"].get("a"):
            continue
        p = L.get("parent")
        while p is not None:
            P = by_ind[p]
            if P["ty"] == 3 and P["ks"]["o"].get("a"):
                L["ks"]["o"] = P["ks"]["o"]
                break
            p = P.get("parent")


def build(aid, name, description, tags, variants):
    for v in variants:
        _inherit_opacity(v.comp)
        for L in v.comp.layers:
            if "shapes" in L:
                _trims_first(L["shapes"])
    build_asset("lower-thirds", aid, name, description, tags, variants)


def rect_grow(x, y, w, h, r, t0, t1, t2, t3, side="left", start=None, ein=EXPO_OUT, eout=EXPO_IN, name="rect"):
    """Rect whose size animates from `start` px along one axis while `side` stays put.

    side: left/right/centre grow the width; top/bottom/middle grow the height.
    """
    horiz = side in ("left", "right", "centre")
    full = w if horiz else h
    s0 = (h if horiz else w) if start is None else start
    s0 = min(s0, full)

    def geo(s):
        if side == "left":
            return [s, h], [x + s / 2, y + h / 2]
        if side == "right":
            return [s, h], [x + w - s / 2, y + h / 2]
        if side == "centre":
            return [s, h], [x + w / 2, y + h / 2]
        if side == "top":
            return [w, s], [x + w / 2, y + s / 2]
        if side == "bottom":
            return [w, s], [x + w / 2, y + h - s / 2]
        return [w, s], [x + w / 2, y + h / 2]

    (sa, pa), (sb, pb) = geo(s0), geo(full)
    return rect(io(sa, sb, t0, t1, t2, t3, ein, eout), io(pa, pb, t0, t1, t2, t3, ein, eout), r, name)


def dstroke(dash, gap, offset=0, **kw):
    """Dashed stroke. lottie_kit's `dashes` omits the offset entry, and Skottie always treats the last
    dash entry as the offset (so [dash, gap] renders as [dash, dash]); this adds it explicitly."""
    s = stroke(**kw)
    s["d"] = [{"n": "d", "nm": "dash", "v": {"a": 0, "k": dash}}, {"n": "g", "nm": "gap", "v": {"a": 0, "k": gap}},
              {"n": "o", "nm": "offset", "v": {"a": 0, "k": offset}}]
    return s
