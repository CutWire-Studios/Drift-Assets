"""Helpers for the second batch of callouts: geometry, line styles, arrows and motion presets.

Every callout here comes in a few styles built from the same outline points:

- hand:   tapered marker ribbons from `_common.Brush` (draw-on) or `hand_static` (boiling line).
- clean:  uniform round-capped vector strokes / flat fills with trim draw-on.
- neon:   stacked glow strokes around a white-hot core, with a flicker on.
- bold:   comic fill with a thick ink outline and a hard offset shadow.
- dashed: dashed vector strokes.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

from _common import Brush, catmull, emit, pressure, resample, ribbon  # noqa: E402,F401
from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import (HOLD, LINEAR, Anim, Comp, anim, bezier, ellipse, fill, group, path,  # noqa: E402,F401
                        rect, round_corners, stroke, trim)

SPRING = (0.3, 1.9, 0.55, 1.0)   # strong back-out for pops
DECEL = (0.2, 0.0, 0.1, 1.0)
SETTLE = (0.2, 0.0, 0.3, 1.0)
DRAW = (0.45, 0.0, 0.3, 1.0)     # pen stroke: eases in, glides out
INK = "#141414"
CATEGORY = "callouts"


# ---------------------------------------------------------------- geometry

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def poly_len(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def dense(pts, spacing=3.0, smooth=False):
    """Evenly resampled polyline (optionally Catmull-Rom smoothed through the points first)."""
    return resample(catmull(pts, 16) if smooth else list(pts), spacing)[0]


def cubic(p0, p1, p2, p3, n=64):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def arc(c, rx, ry, a0, a1, n=None):
    """Points on an ellipse arc, angles in degrees (0 = +x, 90 = +y / down)."""
    n = n or max(8, int(abs(a1 - a0) / 3))
    return [(c[0] + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def rrect_pts(c, w, h, r, start=-90, n=10):
    """Closed rounded-rectangle outline, clockwise, starting at the top middle (start=-90).

    `start` in {-90 top, 0 right, 90 bottom, 180 left}; the first point is not repeated.
    """
    x0, y0, x1, y1 = c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2
    pts = [(c[0], y0)]
    pts += arc((x1 - r, y0 + r), r, r, -90, 0, n)
    pts += arc((x1 - r, y1 - r), r, r, 0, 90, n)
    pts += arc((x0 + r, y1 - r), r, r, 90, 180, n)
    pts += arc((x0 + r, y0 + r), r, r, 180, 270, n)
    pts = dense(pts + [pts[0]])[:-1]
    # rotate so the outline starts on the requested side
    tgt = {-90: (c[0], y0), 0: (x1, c[1]), 90: (c[0], y1), 180: (x0, c[1])}[start]
    k = min(range(len(pts)), key=lambda i: math.dist(pts[i], tgt))
    return pts[k:] + pts[:k]


def ellipse_pts(c, rx, ry, start=-90, turns=1.0, n=None):
    n = n or int(max(rx, ry) * 2 * math.pi * turns / 3)
    return arc(c, rx, ry, start, start + 360 * turns, n)


def fillet(pts, r, n=8):
    """Round the interior corners of a polyline with radius-ish r."""
    out = [pts[0]]
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        la, lc = math.dist(a, b), math.dist(b, c)
        k = min(r, la / 2.2, lc / 2.2)
        p = lerp(b, a, k / la)
        q = lerp(b, c, k / lc)
        for i in range(n + 1):
            t = i / n
            out.append(((1 - t) ** 2 * p[0] + 2 * t * (1 - t) * b[0] + t * t * q[0],
                        (1 - t) ** 2 * p[1] + 2 * t * (1 - t) * b[1] + t * t * q[1]))
    out.append(pts[-1])
    return out


def wobble(pts, amp, seed=0, freq=3.0, closed=False):
    """Offset points along their normals by smooth noise (hand-made unevenness)."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    fr = [freq, freq * 2.3, freq * 5.1]
    if closed:
        fr = [round(f) or 1 for f in fr]
    n = len(pts)
    out = []
    for i, p in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        u = i / max(1, n - 1)
        d = amp * (0.75 * math.sin(fr[0] * 6.283 * u + ph[0]) + 0.25 * math.sin(fr[1] * 6.283 * u + ph[1]))
        out.append((p[0] - ty / ln * d, p[1] + tx / ln * d))
    return out


def offset(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def heading(pts, back=6):
    a, b = pts[max(0, len(pts) - 1 - back)], pts[-1]
    return math.atan2(b[1] - a[1], b[0] - a[0])


def cut_end(pts, length):
    """Drop `length` px off the end of an evenly spaced polyline."""
    total, out = 0.0, list(pts)
    while len(out) > 2 and total < length:
        total += math.dist(out[-1], out[-2])
        out.pop()
    return out


def closed_loop(pts, overshoot=0.08, drift=6):
    """A closed outline as a pen would draw it: past the start by `overshoot`, drifting outwards."""
    n = len(pts)
    extra = int(n * overshoot)
    tail = [pts[i % n] for i in range(extra + 1)]
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    out = list(pts)
    for i, p in enumerate(tail):
        k = (i / max(1, extra)) * drift
        dx, dy = p[0] - cx, p[1] - cy
        ln = math.hypot(dx, dy) or 1
        out.append((p[0] + dx / ln * k, p[1] + dy / ln * k))
    return out


def P(pts, closed=False, name="path"):
    return path(bezier(pts, closed=closed), name)


# ---------------------------------------------------------------- motion presets

def pop(t0, dur=12, peak=112, start=0, end=100):
    """Scale keys: start -> peak -> slight dip -> end."""
    a, b = t0 + round(dur * 0.5), t0 + round(dur * 0.78)
    dip = end - (peak - end) * 0.35
    return anim([(t0, [start, start], SETTLE), (a, [peak, peak], SETTLE), (b, [dip, dip], SETTLE),
                 (t0 + dur, [end, end])])


def squash_pop(t0, dur=14):
    """Pop that stretches then squashes before settling (for bubbles and badges)."""
    k = [(0, 0), (0.45, 1.12, 1.08), (0.7, 0.94, 0.98), (0.88, 1.02, 1.0), (1, 1.0)]
    keys = []
    for item in k:
        u, sx = item[0], item[1]
        sy = item[2] if len(item) > 2 else sx
        keys.append((t0 + round(dur * u), [sx * 100, sy * 100], SETTLE))
    return anim(keys)


def flicker(t0, hold=100):
    """Neon tube switching on: two stutters, then steady."""
    return anim([(t0, 0, HOLD), (t0 + 1, 85, HOLD), (t0 + 3, 15, HOLD), (t0 + 5, 100, HOLD),
                 (t0 + 7, 35, HOLD), (t0 + 8, hold)])


def draw(t0, t1, ease=DRAW):
    return anim([(t0, 0, ease), (t1, 100)])


# ---------------------------------------------------------------- line styles (shape groups)

def clean_line(pts, width, slot="primary", t0=None, t1=None, closed=False, ease=DRAW, cap="round",
               dashes=None, color="#FFFFFF", opacity=100, name="line", mid=False):
    """Vector stroke; with t0/t1 it draws on from the start (or from the middle out, mid=True)."""
    items = [P(pts, closed)]
    if t0 is not None and mid:
        items.append(trim(anim([(t0, 50, ease), (t1, 0)]), anim([(t0, 50, ease), (t1, 100)])))
    elif t0 is not None:
        items.append(trim(0, draw(t0, t1, ease)))
    items.append(stroke(color, width, slot=slot, cap=cap, dashes=dashes, opacity=opacity))
    return group(items, name)


def neon_line(pts, width, slot="primary", t0=None, t1=None, closed=False, ease=DRAW, core="#FFFFFF",
              name="neon", mid=False):
    """Glow halo (wide faint strokes) + tube (slot colour) + white-hot core."""
    out = []
    for w, op, s, col in [(width * 4.2, 10, slot, None), (width * 2.6, 22, slot, None),
                          (width * 1.6, 45, slot, None), (width, 100, slot, None),
                          (width * 0.36, 90, None, core)]:
        out.append(clean_line(pts, w, s, t0, t1, closed, ease, color=col or "#FFFFFF", opacity=op,
                              name=f"{name}-{round(w)}", mid=mid))
    return group(out[::-1], name)  # core first = on top


def hand_ribbon(pts, width, seed=0, taper=(0.08, 0.2), mins=(0.5, 0.25), wob=0.14):
    fn = pressure(width, taper_in=taper[0], taper_out=taper[1], min_in=mins[0], min_out=mins[1],
                  wobble=wob, seed=seed)
    return ribbon(pts, fn), fn


def hand_line(pts, t0, t1, width, slot="primary", seed=0, chunks=1, ease=DRAW, taper=(0.06, 0.18),
              mins=(0.5, 0.3), wob=0.16, name="stroke"):
    """Brush stroke (draw-on marker) along already-dense points; add with emit(comp, [...])."""
    fn = pressure(width, taper_in=taper[0], taper_out=taper[1], min_in=mins[0], min_out=mins[1],
                  wobble=wob, seed=seed)
    return Brush(pts, t0, t1, fn, max_width=width * 1.3, easing=ease, chunks=chunks, smooth=False,
                 slot=slot, name=name)


def hand_static(pts, width, slot="primary", seed=0, frames=None, every=5, amp=1.6, taper=(0.06, 0.18),
                mins=(0.5, 0.3), wob=0.16, color="#FFFFFF", name="ink"):
    """Brush ribbon without a reveal. With `frames`, the line boils (re-jitters every `every` frames)."""
    fn = pressure(width, taper_in=taper[0], taper_out=taper[1], min_in=mins[0], min_out=mins[1],
                  wobble=wob, seed=seed)
    if not frames:
        return group([path(ribbon(pts, fn)), fill(color, slot=slot)], name)
    pts = dense(pts, 5.0)  # coarser points keep the per-key ribbons small
    freq = max(0.7, poly_len(pts) / 260)
    shapes = [ribbon(wobble(pts, amp, seed=seed * 7 + k, freq=freq), fn) for k in range(3)]
    keys, k, f = [], 0, 0
    while f < frames:
        keys.append((f, shapes[k % 3], HOLD))
        f += every
        k += 1
    keys.append((frames, shapes[0], HOLD))
    return group([path(Anim(keys)), fill(color, slot=slot)], name)


def comic(shape_items, fill_slot="primary", outline_slot="outline", shadow_slot="outline", width=9,
          shadow=(8, 10), fill_color="#FFFFFF", shadow_opacity=100, name="comic"):
    """Fill + ink outline, over a hard offset shadow of the same shape."""
    main = group(list(shape_items) + [stroke(INK, width, slot=outline_slot), fill(fill_color, slot=fill_slot)],
                 name)
    items = [main]
    if shadow:
        items.append(group(list(shape_items) + [fill(INK, shadow_opacity, slot=shadow_slot)], name + "-shadow",
                           position=shadow))
    return items


def reveal(comp, center, t0, t1, content, width, ease=DRAW, parent=None, name="reveal", **tr):
    """Content layer revealed along `center` by a trim-path matte (for filled shapes drawn on)."""
    ip = math.floor(t0)
    comp.layer(name + "-matte", [group([P(center), trim(0, draw(t0, t1, ease)),
                                        stroke("#FFFFFF", width, cap="round")], "m")],
               ip=ip, parent=parent, **tr)
    return comp.layer(name, content, ip=ip, parent=parent, matte="alpha", **tr)


def taper_ribbon(pts, w0, w1, ease_pow=0.7):
    """Filled ribbon widening from w0 at the tail to w1 at the head (no caps at the head end)."""
    fn = lambda u: w0 + (w1 - w0) * (u ** ease_pow)  # noqa: E731
    return ribbon(pts, fn, cap_start=True, cap_end=False)


# ---------------------------------------------------------------- arrows

def tri_head(size, fat=0.95):
    """Filled arrowhead pointing +x, tip at (0, 0)."""
    return [(0, 0), (-size, -size * fat * 0.62), (-size * 0.75, 0), (-size, size * fat * 0.62)]


def chevron(size, spread=38):
    a = math.radians(180 - spread)
    b = math.radians(180 + spread)
    return [(size * math.cos(a), size * math.sin(a)), (0, 0), (size * math.cos(b), size * math.sin(b))]


def arrow(comp, pts, style, t0, t1, width, head=None, slot="primary", seed=1, both=False, parent=None,
          name="arrow"):
    """Arrow along dense `pts` (tail -> tip), drawn on between t0 and t1, head arrives after.

    style: hand | clean | bold | neon | dashed. Returns the frame the arrow is complete.
    """
    head = head or width * {"hand": 4.6, "clean": 4.0, "bold": 3.4, "neon": 4.4, "dashed": 3.8}[style]
    ends = [pts] + ([pts[::-1]] if both else [])
    done = t1
    if style == "hand":
        emit(comp, [hand_line(pts, t0, t1, width, slot, seed, chunks=2 if poly_len(pts) > 700 else 1,
                              taper=(0.05, 0.08), mins=(0.5, 0.7), wob=0.1, name=name)], parent=parent)
        barbs = []
        for j, p in enumerate(ends):
            tip, ang = p[-1], heading(p, 10)
            for k, (side, ln, sp) in enumerate([(-1, head * 1.05, 40), (1, head, 42)]):
                a = ang + math.pi + side * math.radians(sp)
                far = (tip[0] + ln * math.cos(a), tip[1] + ln * math.sin(a))
                seg = dense([far, lerp(far, tip, 0.5), tip] if k == 0 else [tip, lerp(tip, far, 0.5), far],
                            smooth=True)
                ta = t1 + 1 + k * 5
                barbs.append(hand_line(seg, ta, ta + 5, width, slot, seed + 10 + k + j * 5,
                                       taper=(0.2, 0.3) if k == 0 else (0.1, 0.4), mins=(0.75, 0.5),
                                       wob=0.03, name=f"{name}-barb{j}{k}"))
                done = ta + 5
        emit(comp, barbs, parent=parent)
        return done
    # heads are added first so they draw above the shaft
    if style in ("clean", "dashed"):
        for j, p in enumerate(ends):
            tip, ang = p[-1], heading(p, max(12, int(head * 0.55 / 3)))
            if style == "clean":
                shape = [group([path(bezier(tri_head(head), closed=True)), round_corners(width * 0.3),
                                fill(slot=slot)], "head")]
            else:
                shape = [clean_line(chevron(head * 0.8), width, slot, t1 - 1, t1 + 5, ease=SETTLE)]
            comp.layer(f"{name}-head{j}", shape, parent=parent, position=tip,
                       rotation=math.degrees(ang), scale=pop(t1 - 3, 10, 125), ip=t1 - 3)
        shaft = cut_end(pts, head * 0.55) if style == "clean" else pts
        if both and style == "clean":
            shaft = cut_end(shaft[::-1], head * 0.55)[::-1]
        dashes = [width * 1.6, width * 1.3] if style == "dashed" else None
        comp.layer(name, [clean_line(shaft, width, slot, t0, t1, cap="round", dashes=dashes, mid=both)],
                   parent=parent)
        return t1 + 7
    if style == "bold":
        body = [path(taper_ribbon(cut_end(pts, head * 0.3), width * 0.55, width * 1.35))]
        ow, sh = width * 0.42, (9, 13)
        heads = []
        for j, p in enumerate(ends):
            tip, ang = p[-1], heading(p, max(12, int(head * 0.55 / 3)))
            tri = [path(bezier(tri_head(head * 1.15, 1.05), closed=True)), round_corners(4)]
            ca, sa = math.cos(-ang), math.sin(-ang)
            local = (sh[0] * ca - sh[1] * sa, sh[0] * sa + sh[1] * ca)  # shadow offset in the head's frame
            heads.append((tip, ang, tri, local))
        for layer in ("main", "shadow"):
            for j, (tip, ang, tri, local) in enumerate(heads):
                items = comic(tri, "primary", width=ow, shadow=local)
                comp.layer(f"{name}-head{j}-{layer}", [items[0] if layer == "main" else items[1]],
                           parent=parent, position=tip, rotation=math.degrees(ang), scale=pop(t1 - 4, 11, 128),
                           ip=t1 - 4)
            items = comic(body, "primary", width=ow, shadow=sh)
            reveal(comp, pts if layer == "main" else offset(pts, *sh), t0, t1,
                   [items[0] if layer == "main" else items[1]], width * 2.2 + 30, parent=parent,
                   name=f"{name}-{layer}")
        return t1 + 7
    if style == "neon":
        for j, p in enumerate(ends):
            tip, ang = p[-1], heading(p, max(12, int(head * 0.55 / 3)))
            ch = chevron(head * 0.85)
            comp.layer(f"{name}-head{j}", [neon_line(ch[:2][::-1], width, slot, t1 - 2, t1 + 4, ease=SETTLE,
                                                     name="a"),
                                           neon_line(ch[1:], width, slot, t1 - 2, t1 + 4, ease=SETTLE, name="b")],
                       parent=parent, position=tip, rotation=math.degrees(ang), ip=t1 - 2)
        comp.layer(name, [neon_line(pts, width, slot, t0, t1, mid=both)], parent=parent, opacity=flicker(t0))
        return t1 + 5
    raise ValueError(style)


# ---------------------------------------------------------------- bubbles

def with_tail(outline, tail_at, tip, half_width, bend=0.3):
    """Replace the outline points within `half_width` px (along the outline) of `tail_at` with a tail
    to `tip`. `tail_at` is an index into the evenly spaced closed outline."""
    n = len(outline)
    step = math.dist(outline[0], outline[1]) or 3
    k = int(half_width / step)
    a, b = (tail_at - k) % n, (tail_at + k) % n
    out = []
    i = b
    # walk from b round to a (the part we keep), then add the tail
    while i != a:
        out.append(outline[i])
        i = (i + 1) % n
    out.append(outline[a])
    pa, pb = outline[a], outline[b]
    ma, mb = lerp(pa, tip, 0.5), lerp(pb, tip, 0.5)
    ca, cb = lerp(ma, mb, bend), lerp(mb, ma, bend)  # pull both sides in: a slim, curved tail
    q = lambda p0, c, p1, n=24: [((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * c[0] + t * t * p1[0],  # noqa: E731
                                 (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * c[1] + t * t * p1[1])
                                for t in (i / n for i in range(n + 1))]
    out += dense(q(pa, ca, tip), 3)[1:]
    out += dense(q(tip, cb, pb), 3)[1:-1]
    return out


def nearest(outline, p):
    return min(range(len(outline)), key=lambda i: math.dist(outline[i], p))


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def rotate(pts, deg, c=(0, 0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def outlined(pts, style, fill_slot, outline_slot, width, seed=0, frames=None, fill_color="#FFFFFF", name="part"):
    """One closed part: fill + outline, either as clean vector stroke or boiling marker ribbon."""
    if style == "hand":
        line = closed_loop(pts, 0.06, 2)
        return group([hand_static(line, width, outline_slot, seed, frames, taper=(0.04, 0.06), mins=(0.6, 0.6),
                                  wob=0.12, color=INK, name="ink"),
                      group([P(pts, True), fill(fill_color, slot=fill_slot)], "fill")], name)
    return group([P(pts, True), stroke(INK, width, slot=outline_slot), fill(fill_color, slot=fill_slot)], name)


def bubble(comp, outline, style, tip, t0=0, seed=1, width=None, draw_start=None, name="bubble", dur=20):
    """A closed bubble outline in one of three looks, popping out from `tip` (canvas coords).

    clean: flat `background` fill with a soft drop shadow, squash-and-stretch pop.
    bold:  `background` fill, thick `outline` ink and a hard `primary` offset shadow, springy pop.
    hand:  marker outline (`outline`) drawn on around the shape while the fill fades up.
    Declares the slots it uses. Returns the frame the bubble is fully on.
    """
    anchor = {"anchor": tip, "position": tip}
    if style == "clean":
        comp.slot("background", "#FFFFFF")
        comp.layer(name, [group([P(outline, True), fill(slot="background")], "fill")], scale=squash_pop(t0, 14),
                   ip=t0, **anchor)
        comp.layer(name + "-shadow", [group([P(outline, True), fill("#000000", 28)], "s", position=(0, 10))],
                   scale=squash_pop(t0, 14), ip=t0, **anchor)
        return t0 + 14
    if style == "bold":
        comp.slot("background", "#FFFFFF")
        comp.slot("outline", INK)
        comp.slot("primary", "#FF2D2D")
        items = comic([P(outline, True)], "background", "outline", "primary", width=width or 9, shadow=(12, 12))
        rot = anim([(t0, -8, SETTLE), (t0 + 8, 3, SETTLE), (t0 + 14, -1, SETTLE), (t0 + 20, 0)])
        comp.layer(name, items, scale=pop(t0, 16, 116), rotation=rot, ip=t0, **anchor)
        return t0 + 16
    comp.slot("background", "#FFFFFF")
    comp.slot("outline", INK)
    pts = outline
    if draw_start is not None:
        k = nearest(pts, draw_start)
        pts = pts[k:] + pts[:k]
    line = wobble(closed_loop(pts, 0.06, 6), 2.5, seed=seed, freq=2)
    emit(comp, [hand_line(line, t0 + 1, t0 + dur, width or 12, "outline", seed, chunks=3 if dur > 10 else 2,
                          taper=(0.03, 0.08), mins=(0.5, 0.3), wob=0.1, name=name + "-line")])
    f = dur / 20
    comp.layer(name, [group([P(outline, True), fill(slot="background")], "fill")],
               opacity=anim([(t0 + round(4 * f), 0, EASE_OUT), (t0 + round(16 * f), 100)]),
               scale=anim([(t0 + round(4 * f), [94, 94], SETTLE), (t0 + round(18 * f), [100, 100])]), **anchor)
    return t0 + dur + 1
