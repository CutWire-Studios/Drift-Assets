"""Shared parts for the generic social call-to-action assets (cta_actions batch).

Every asset in the batch ships the same three looks, built from one geometry by `body()`:

  classic   flat filled shape with a soft drop shadow.
  outline   line art: only the outer contour of the (unioned) shape is stroked, interior see-through.
  3d-pop    layered: extruded side (slot colour darkened), top highlight rim, bottom shade, drop shadow.

Geometry is a list of shape items (rect/ellipse/path...) centred on (0, 0); a body is a null carrying
the transform with the painted layers parented to it (layers created earlier draw on top).
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import *  # noqa: F401,F403,E402
from _common import SPRING, DECEL, cursor, ripple, burst, pill, glyph, arc_pts, bell_body, bell_clapper  # noqa: F401,E402
from drift_lottie import Variant, build_asset  # noqa: F401,E402
from lottie_kit import (Comp, anim, bezier, ellipse, fill, gradient_fill, group, path, polyline, rect,  # noqa: F401,E402
                        stroke, trim, star, EASE_IN, EASE_OUT, EASE_IN_OUT, SNAP_OUT, OVERSHOOT, LINEAR, HOLD)

CATEGORY = "call-to-action"
STYLES = ("classic", "outline", "3d-pop")
STYLE_NAMES = {"classic": "Classic", "outline": "Line Art", "3d-pop": "3D Pop"}
STYLE_DESC = {
    "classic": "Flat filled shapes with a soft drop shadow.",
    "outline": "Line-art version: clean outer contours, see-through inside.",
    "3d-pop": "Chunky layered look with an extruded side, highlight rim and depth shadow.",
}

# Material Icons "favorite" (Apache 2.0), 24x24
HEART = ("M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09"
         "C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z")


# ---------------------------------------------------------------- geometry

def rpoly(pts, r, closed=True):
    """Polygon with rounded corners (r: one radius or one per vertex) as a bezier()."""
    n = len(pts)
    rs = r if isinstance(r, (list, tuple)) else [r] * n
    v, it, ot = [], [], []
    for i, p in enumerate(pts):
        if not closed and i in (0, n - 1):
            v.append(p), it.append((0, 0)), ot.append((0, 0))
            continue
        a, b = pts[i - 1], pts[(i + 1) % n]
        da, db = math.dist(p, a), math.dist(p, b)
        rr = min(rs[i], da / 2, db / 2)
        if rr <= 0.01:
            v.append(p), it.append((0, 0)), ot.append((0, 0))
            continue
        p1 = (p[0] + (a[0] - p[0]) / da * rr, p[1] + (a[1] - p[1]) / da * rr)
        p2 = (p[0] + (b[0] - p[0]) / db * rr, p[1] + (b[1] - p[1]) / db * rr)
        k = 0.55
        v += [p1, p2]
        it += [(0, 0), ((p[0] - p2[0]) * k, (p[1] - p2[1]) * k)]
        ot += [((p[0] - p1[0]) * k, (p[1] - p1[1]) * k), (0, 0)]
    return bezier(v, it, ot, closed)


def shape(pts, r=0, name="shape"):
    return path(rpoly(pts, r), name)


def star_pts(outer, inner, n=5, rot=-90, center=(0, 0)):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n)
        rr = outer if i % 2 == 0 else inner
        pts.append((center[0] + math.cos(a) * rr, center[1] + math.sin(a) * rr))
    return pts


def heart(size, center=(0, 0)):
    return glyph(HEART, size, (center[0], center[1] + size * 0.03), name="heart")


def ring_pts(r, n, rot=-90, center=(0, 0)):
    return [(center[0] + r * math.cos(math.radians(rot + i * 360 / n)),
             center[1] + r * math.sin(math.radians(rot + i * 360 / n))) for i in range(n)]


# ---------------------------------------------------------------- painting

def body(comp, name, geom, style, slot="primary", parent=None, line=8, line_slot="outline", depth=12,
         ip=0, op=None, shadow=True, tint=0, opacity=100, details=None, detail_width=None, ink=None,
         **tr):
    """Paint `geom` in `style` on layers parented to a new null (which takes the transform kwargs).

    details: extra open paths stroked on top (in the outline colour for line art, else `ink` or a
    translucent dark). ink: hex colour of a sticker-style outer outline for classic / 3d-pop.
    opacity: static or anim, applied to every visible layer (null opacity does not inherit).
    """
    n = comp.null(name, parent=parent, ip=ip, op=op, **tr)
    geom = list(geom)
    dw = detail_width or line

    def L(nm, items, gm=None, **k):
        return comp.layer(f"{name}-{nm}", [group(list(gm or geom) + items, nm)], parent=n, ip=ip, op=op, **k)

    if details:
        if style == "outline":
            L("details", [stroke(slot=line_slot, width=dw, opacity=opacity)], gm=details)
        else:
            L("details", [stroke(ink or "#000000", width=dw, opacity=opacity if ink else _mul(opacity, 0.3))],
              gm=details)
    if style == "outline":
        L("cut", [fill()])
        L("line", [stroke(slot=line_slot, width=line * 2, opacity=opacity)], matte="alpha_inverted")
        if tint:
            L("tint", [fill(slot=slot, opacity=_mul(opacity, tint / 100))])
        return n
    if ink:
        L("ink-cut", [fill()])
        L("ink", [stroke(ink, width=line * 2, opacity=opacity)], matte="alpha_inverted")
    if style == "classic":
        L("face", [fill(slot=slot, opacity=opacity)])
        if shadow:
            L("shadow", [fill("#000000", _mul(opacity, 0.24))], position=(0, max(5, depth * 0.55)))
        return n
    d = depth
    L("hi-cut", [fill()], position=(0, d * 0.42))
    L("hi", [fill("#FFFFFF", _mul(opacity, 0.42))], matte="alpha_inverted")
    L("lo-cut", [fill()], position=(0, -d * 0.45))
    L("lo", [fill("#000000", _mul(opacity, 0.14))], matte="alpha_inverted")
    L("face", [fill(slot=slot, opacity=opacity)])
    for i, f in enumerate((0.5, 1.0)):
        L(f"side{i}-shade", [fill("#000000", _mul(opacity, 0.36))], position=(0, d * f))
        L(f"side{i}", [fill(slot=slot, opacity=opacity)], position=(0, d * f))
    if shadow:
        L("drop", [fill("#000000", _mul(opacity, 0.26))], position=(0, d + 8))
    return n


def _mul(o, k):
    """Opacity (number or Anim of numbers) times k."""
    from lottie_kit import Anim
    if isinstance(o, Anim):
        return Anim([(t, v * k, e) for t, v, e in o.keys])
    return o * k


def fade(t0, t1=None, dur=6, frames=None):
    """Opacity anim: fades in at t0 (and out at t1)."""
    keys = [(t0, 0, EASE_OUT), (t0 + dur, 100, HOLD if t1 is None else LINEAR)]
    if t1 is not None:
        keys += [(t1, 100, EASE_IN), (t1 + dur, 0)]
    return anim(keys)


def pop(t0, dur=14, to=100, spring=SPRING, out_at=None, out_dur=10):
    keys = [(t0, [0, 0], spring), (t0 + dur, [to, to], LINEAR)]
    if out_at is not None:
        keys += [(out_at, [to, to], EASE_OUT), (out_at + 4, [to * 1.08, to * 1.08], EASE_IN),
                 (out_at + out_dur, [0, 0], LINEAR)]
    return anim(keys)


def squash(t, s=100, amt=14, settle=16):
    """Press-and-rebound scale keys starting at frame t (a tap)."""
    return [(t - 3, [s, s], EASE_IN), (t, [s * (1 + amt / 300), s * (1 - amt / 100)], SNAP_OUT),
            (t + 6, [s * (1 + amt / 100), s * (1 + amt / 100)], EASE_IN_OUT),
            (t + 11, [s * 0.97, s * 0.97], EASE_IN_OUT), (t + settle, [s, s], LINEAR)]


def tap(comp, pos, t, size=110, color="#FFFFFF", parent=None):
    """Finger-press indicator: a soft disc that presses in and a ripple."""
    comp.layer("press", [ellipse((size * 0.5, size * 0.5)), fill(color, 45)], ip=t - 2, op=t + 12, position=pos,
               parent=parent, scale=anim([(t - 2, [40, 40], EASE_OUT), (t + 2, [100, 100], EASE_IN),
                                          (t + 11, [150, 150])]),
               opacity=anim([(t + 2, 100, EASE_IN), (t + 11, 0)]))
    ripple(comp, pos, t, size=size, color=color)


def label(comp, style, x, cy, w, h, t0, slot="background", parent=None, dur=16, out_at=None, depth=8,
          line=5, name="label"):
    """Pill that grows rightwards from x (left edge) to width w. Returns the text rect (x, y, w, h)."""
    ks = [(t0, 0, DECEL), (t0 + dur, 1, LINEAR)]
    if out_at is not None:
        ks += [(out_at, 1, EASE_IN), (out_at + 10, 0, LINEAR)]
    size = anim([(t, [h + (w - h) * v, h], e) for t, v, e in ks])
    pos = anim([(t, [-(w - h) * (1 - v) / 2, 0], e) for t, v, e in ks])
    op = [(t0, 0, EASE_OUT), (t0 + 3, 100, HOLD)]
    if out_at is not None:
        op += [(out_at + 7, 100, EASE_IN), (out_at + 10, 0)]
    body(comp, name, [rect(size, position=pos, roundness=h / 2)], style, slot=slot, parent=parent,
         position=(x + w / 2, cy), depth=depth, line=line, opacity=anim(op))
    return text_rect(x, cy, w, h)


def shine(comp, geom, pos, t0, t1, span, frames, parent=None, width=60, opacity=30):
    """Diagonal light band sweeping across `geom` (at `pos`) between frames t0 and t1."""
    comp.layer("shine-matte", [group(list(geom) + [fill()], "m")], position=pos, parent=parent)
    x0, x1 = pos[0] - span, pos[0] + span
    comp.layer("shine", [group([rect((width, span * 2)), fill("#FFFFFF", opacity)], "band", rotation=22)],
               matte="alpha", parent=parent,
               position=anim([(0, [x0, pos[1]], HOLD), (t0, [x0, pos[1]], EASE_IN_OUT), (t1, [x1, pos[1]], HOLD),
                              (frames, [x1, pos[1]])]))


def text_rect(x, cy, w, h):
    return (x + h * 0.42, cy - h * 0.3, w - h * 0.84, h * 0.6)


# ---------------------------------------------------------------- hand (index finger up, tip at (0, 0))

def hand_geom():
    return [
        rect((36, 112), (0, 54), roundness=18, name="finger"),
        rect((30, 46), (31, 106), roundness=15, name="k1"),
        rect((28, 42), (57, 114), roundness=14, name="k2"),
        rect((26, 36), (80, 124), roundness=13, name="k3"),
        shape([(-18, 96), (92, 116), (92, 160), (70, 200), (-8, 200), (-30, 160)], 28, name="palm"),
        group([rect((30, 70), roundness=15)], "thumb", position=(-30, 138), rotation=-38),
    ]


def hand_details():
    return [polyline([(17, 92), (17, 120)], name="d1"), polyline([(45, 98), (45, 122)], name="d2"),
            polyline([(69, 108), (69, 128)], name="d3")]


def hand(comp, style, name="hand", parent=None, ip=0, op=None, **tr):
    """Cartoon pointing hand. classic: white with ink outline; outline: line art; 3d-pop: layered."""
    cuff = [rect((96, 30), (30, 212), roundness=10)]
    n = comp.null(name, parent=parent, ip=ip, op=op, **tr)
    if style == "outline":
        body(comp, name + "-palm", hand_geom(), style, parent=n, line=6, details=hand_details(), ip=ip, op=op)
        body(comp, name + "-cuff", cuff, style, parent=n, line=6, ip=ip, op=op)
    elif style == "classic":
        body(comp, name + "-palm", hand_geom(), style, slot="icon", parent=n, line=5, ink="#15151B",
             details=hand_details(), detail_width=5, ip=ip, op=op, depth=10)
        body(comp, name + "-cuff", cuff, style, slot="secondary", parent=n, line=5, ink="#15151B", ip=ip, op=op)
    else:
        body(comp, name + "-palm", hand_geom(), style, slot="icon", parent=n, details=hand_details(),
             detail_width=5, ip=ip, op=op, depth=12)
        body(comp, name + "-cuff", cuff, style, slot="secondary", parent=n, ip=ip, op=op, depth=12)
    return n


def hand_slots(comp, style):
    if style != "outline":
        comp.slot("icon", "#FFFFFF")
        comp.slot("secondary", "#5B5BF0")
    else:
        comp.slot("outline", "#FFFFFF")
