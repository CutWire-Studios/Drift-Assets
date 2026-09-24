"""Tiny Lottie authoring kit.

Builds Lottie 5.x JSON that Skottie (Drift's renderer) plays without expressions, images or text.
Colours that users should be able to change are exposed as Lottie slots (`sid`), which Drift
surfaces as per-clip colour overrides.

    from lottie_kit import *
    comp = Comp("like-button", 400, 400, fps=30, frames=60)
    comp.slot("primary", "#FF0000")
    comp.layer("button", [rect((200, 80), roundness=40), fill(slot="primary")],
               position=(200, 200), scale=anim([(0, [0, 0], OVERSHOOT), (12, [100, 100])]))
    comp.save("like-button.json")
"""

import json
import math
import re

# Bezier easings as (out_x, out_y, in_x, in_y): "out" leaves the current key, "in" enters the next.
LINEAR = (0.0, 0.0, 1.0, 1.0)
EASE = (0.25, 0.1, 0.25, 1.0)
EASE_IN = (0.42, 0.0, 1.0, 1.0)
EASE_OUT = (0.0, 0.0, 0.58, 1.0)
EASE_IN_OUT = (0.42, 0.0, 0.58, 1.0)
SNAP_OUT = (0.16, 1.0, 0.3, 1.0)  # fast start, long settle
OVERSHOOT = (0.34, 1.56, 0.64, 1.0)  # back-out: goes ~10% past the target
ANTICIPATE = (0.36, 0.0, 0.66, -0.56)  # back-in: dips back before leaving
HOLD = "hold"


def hex_color(c, alpha=1.0):
    """'#RRGGBB' / '#RRGGBBAA' / (r,g,b[,a]) 0..1 -> [r,g,b,a]."""
    if isinstance(c, str):
        c = c.lstrip("#")
        r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
        a = int(c[6:8], 16) / 255 if len(c) == 8 else alpha
        return [r, g, b, a]
    c = list(c)
    return c + [alpha] if len(c) == 3 else c


def _vec(v):
    return list(v) if isinstance(v, (list, tuple)) else [v]


class Anim:
    """Animated property. keys: [(frame, value, easing_to_next), ...]; last key's easing ignored."""

    def __init__(self, keys):
        self.keys = [k if len(k) == 3 else (k[0], k[1], EASE_IN_OUT) for k in keys]

    def lottie(self):
        out = []
        for i, (t, v, e) in enumerate(self.keys):
            k = {"t": t, "s": _vec(v)}
            if i < len(self.keys) - 1:
                if e == HOLD:
                    k["h"] = 1
                else:
                    ox, oy, ix, iy = e
                    k["o"] = {"x": [ox], "y": [oy]}
                    k["i"] = {"x": [ix], "y": [iy]}
            out.append(k)
        return {"a": 1, "k": out}


def anim(keys):
    return Anim(keys)


def loop(frames, values, easing=EASE_IN_OUT, start=0):
    """Evenly spaced keys that end on the first value, for seamless loops of length `frames`."""
    vals = list(values) + [values[0]]
    step = frames / (len(vals) - 1)
    return Anim([(start + round(i * step, 3), v, easing) for i, v in enumerate(vals)])


def _color(c, sid):
    p = c.lottie() if isinstance(c, Anim) else {"a": 0, "k": hex_color(c)}
    if isinstance(c, Anim):
        for k in p["k"]:
            k["s"] = hex_color(k["s"]) if isinstance(k["s"][0], str) else k["s"]
    if sid:
        p["sid"] = sid
    return p


def _p(v):
    """Property whose static value is a vector (position, size...)."""
    if isinstance(v, Anim):
        return v.lottie()
    return {"a": 0, "k": _vec(v)}


def _s(v):
    """Property whose static value is a scalar (opacity, rotation, width...)."""
    if isinstance(v, Anim):
        out = v.lottie()
        for k in out["k"]:
            k["s"] = _vec(k["s"])
        return out
    return {"a": 0, "k": v}


def transform(anchor=(0, 0), position=(0, 0), scale=(100, 100), rotation=0, opacity=100,
              skew=0, skew_axis=0, shape=False):
    t = {"a": _p(anchor), "p": _p(position), "s": _p(scale), "r": _s(rotation), "o": _s(opacity),
         "sk": _s(skew), "sa": _s(skew_axis)}
    if shape:
        t["ty"] = "tr"
    return t


# ---------------------------------------------------------------- shapes

def rect(size, position=(0, 0), roundness=0, name="rect"):
    return {"ty": "rc", "nm": name, "d": 1, "s": _p(size), "p": _p(position), "r": _s(roundness)}


def ellipse(size, position=(0, 0), name="ellipse"):
    return {"ty": "el", "nm": name, "d": 1, "s": _p(size), "p": _p(position)}


def star(points, outer_radius, inner_radius=None, position=(0, 0), rotation=0,
         outer_roundness=0, inner_roundness=0, name="star"):
    """Star (inner_radius given) or regular polygon (inner_radius None)."""
    s = {"ty": "sr", "nm": name, "d": 1, "sy": 1 if inner_radius is not None else 2,
         "pt": _s(points), "p": _p(position), "r": _s(rotation),
         "or": _s(outer_radius), "os": _s(outer_roundness)}
    if inner_radius is not None:
        s["ir"] = _s(inner_radius)
        s["is"] = _s(inner_roundness)
    return s


def bezier(vertices, in_tangents=None, out_tangents=None, closed=True):
    n = len(vertices)
    return {"c": closed, "v": [list(v) for v in vertices],
            "i": [list(t) for t in (in_tangents or [(0, 0)] * n)],
            "o": [list(t) for t in (out_tangents or [(0, 0)] * n)]}


def path(shape, name="path"):
    """shape: bezier(...) dict, or Anim of bezier dicts (all with equal vertex counts)."""
    if isinstance(shape, Anim):
        ks = Anim([(t, [v], e) for t, v, e in shape.keys]).lottie()
        return {"ty": "sh", "nm": name, "ks": ks}
    return {"ty": "sh", "nm": name, "ks": {"a": 0, "k": shape}}


def polyline(points, closed=False, name="polyline"):
    return path(bezier(points, closed=closed), name)


def fill(color="#FFFFFF", opacity=100, slot=None, even_odd=False, name="fill"):
    return {"ty": "fl", "nm": name, "c": _color(color, slot), "o": _s(opacity), "r": 2 if even_odd else 1}


def stroke(color="#FFFFFF", width=4, opacity=100, slot=None, cap="round", join="round", dashes=None,
           name="stroke"):
    s = {"ty": "st", "nm": name, "c": _color(color, slot),
         "o": _s(opacity), "w": _s(width),
         "lc": {"butt": 1, "round": 2, "square": 3}[cap], "lj": {"miter": 1, "round": 2, "bevel": 3}[join],
         "ml": 4}
    if dashes:
        s["d"] = [{"n": "d" if i % 2 == 0 else "g", "nm": "d", "v": _s(v)} for i, v in enumerate(dashes)]
    return s


def gradient_fill(stops, start, end, radial=False, opacity=100, name="gradient"):
    """stops: [(offset 0..1, '#RRGGBB'[, alpha])]. Gradient colours cannot be slotted."""
    colors, alphas = [], []
    for s in stops:
        r, g, b, a = hex_color(s[1], s[2] if len(s) > 2 else 1.0)
        colors += [s[0], r, g, b]
        alphas += [s[0], a]
    return {"ty": "gf", "nm": name, "o": _s(opacity), "r": 1, "t": 2 if radial else 1,
            "s": _p(start), "e": _p(end), "g": {"p": len(stops), "k": {"a": 0, "k": colors + alphas}}}


def trim(start=0, end=100, offset=0, name="trim"):
    """Trim paths; animate `end` 0->100 for draw-on strokes."""
    return {"ty": "tm", "nm": name, "s": _s(start), "e": _s(end), "o": _s(offset), "m": 1}


def round_corners(radius, name="round"):
    return {"ty": "rd", "nm": name, "r": _s(radius)}


def repeater(copies, position=(0, 0), rotation=0, scale=(100, 100), start_opacity=100, end_opacity=100,
             name="repeater"):
    return {"ty": "rp", "nm": name, "c": _s(copies), "o": _s(0), "m": 1,
            "tr": {"ty": "tr", "a": _p((0, 0)), "p": _p(position), "s": _p(scale), "r": _s(rotation),
                   "so": _s(start_opacity), "eo": _s(end_opacity)}}


def group(items, name="group", **tr):
    """Shape group; keyword args go to its transform (anchor, position, scale, rotation, opacity)."""
    return {"ty": "gr", "nm": name, "it": list(items) + [transform(shape=True, **tr)]}


# ---------------------------------------------------------------- SVG path import

_CMD = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def _arc_to_cubics(x1, y1, rx, ry, phi, large, sweep, x2, y2):
    if rx == 0 or ry == 0:
        return [((x1, y1), (x2, y2), (x2, y2))]
    cp, sp = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    rx, ry = abs(rx), abs(ry)
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = math.sqrt(max(0, num / den)) * (-1 if large == sweep else 1)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx, cy = cp * cxp - sp * cyp + (x1 + x2) / 2, sp * cxp + cp * cyp + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a

    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dt > 0:
        dt -= 2 * math.pi
    elif sweep and dt < 0:
        dt += 2 * math.pi
    n = max(1, math.ceil(abs(dt) / (math.pi / 2)))
    d = dt / n
    k = 4 / 3 * math.tan(d / 4)
    out = []
    for i in range(n):
        a1, a2 = t1 + i * d, t1 + (i + 1) * d

        def pt(a, s=1.0, deriv=False):
            if deriv:
                ex, ey = -rx * math.sin(a), ry * math.cos(a)
            else:
                ex, ey = rx * math.cos(a), ry * math.sin(a)
            X = cp * ex - sp * ey
            Y = sp * ex + cp * ey
            return (X, Y) if deriv else (X + cx, Y + cy)

        p1, p2 = pt(a1), pt(a2)
        d1, d2 = pt(a1, deriv=True), pt(a2, deriv=True)
        c1 = (p1[0] + k * d1[0], p1[1] + k * d1[1])
        c2 = (p2[0] - k * d2[0], p2[1] - k * d2[1])
        out.append((c1, c2, p2))
    return out


def svg_path(d, scale=1.0, offset=(0, 0)):
    """Parse an SVG path `d` string into a list of bezier() dicts (one per subpath).

    Coordinates are transformed as p * scale + offset. Use with path() inside a group; combine
    subpaths in one group with fill(even_odd=True) or rely on winding for holes.
    """
    toks = _CMD.findall(d)
    i, cmd = 0, None
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    last_ctrl = None
    subpaths = []
    segs = None  # list of [vertex, in_tangent_abs, out_tangent_abs]

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    def flag():
        # Arc flags are single digits and may be written without separators ("a1 1 0 011 1").
        nonlocal i
        t = toks[i]
        if len(t) > 1 and t[0] in "01":
            toks[i] = t[1:]
            return int(t[0])
        i += 1
        return int(float(t))

    def begin(p):
        nonlocal segs
        if segs:
            subpaths.append((segs, False))
        segs = [[p, p, p]]

    def cubic(c1, c2, p):
        segs[-1][2] = c1
        segs.append([p, c2, p])

    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                if segs:
                    # merge a closing vertex that duplicates the first
                    if len(segs) > 1 and math.dist(segs[-1][0], segs[0][0]) < 1e-6:
                        segs[0][1] = segs[-1][1]
                        segs.pop()
                    subpaths.append((segs, True))
                    segs = None
                cur = start
                last_ctrl = None
                continue
        rel = cmd.islower()
        C = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if C == "M":
            p = (num() + ox, num() + oy)
            begin(p)
            cur = start = p
            cmd = "l" if rel else "L"
            last_ctrl = None
        elif C == "L":
            p = (num() + ox, num() + oy)
            if segs is None:
                begin(cur)
            cubic(cur, p, p)
            cur, last_ctrl = p, None
        elif C == "H":
            p = (num() + (cur[0] if rel else 0), cur[1])
            if segs is None:
                begin(cur)
            cubic(cur, p, p)
            cur, last_ctrl = p, None
        elif C == "V":
            p = (cur[0], num() + (cur[1] if rel else 0))
            if segs is None:
                begin(cur)
            cubic(cur, p, p)
            cur, last_ctrl = p, None
        elif C in "CS":
            if C == "C":
                c1 = (num() + ox, num() + oy)
            else:
                c1 = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur
            c2 = (num() + ox, num() + oy)
            p = (num() + ox, num() + oy)
            if segs is None:
                begin(cur)
            cubic(c1, c2, p)
            cur, last_ctrl = p, c2
        elif C in "QT":
            if C == "Q":
                q = (num() + ox, num() + oy)
            else:
                q = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur
            p = (num() + ox, num() + oy)
            c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1]))
            c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
            if segs is None:
                begin(cur)
            cubic(c1, c2, p)
            cur, last_ctrl = p, q
        elif C == "A":
            rx, ry, phi = num(), num(), num()
            large, sweep = flag(), flag()
            p = (num() + ox, num() + oy)
            if segs is None:
                begin(cur)
            for c1, c2, pp in _arc_to_cubics(cur[0], cur[1], rx, ry, phi, large, sweep, p[0], p[1]):
                cubic(c1, c2, pp)
            cur, last_ctrl = p, None
        else:
            raise ValueError(f"unsupported SVG path command {cmd}")
    if segs and len(segs) > 1:
        subpaths.append((segs, False))

    sx, sy = offset
    out = []
    for segs, closed in subpaths:
        tf = lambda q: (q[0] * scale + sx, q[1] * scale + sy)
        v = [tf(s[0]) for s in segs]
        it = [(tf(s[1])[0] - vv[0], tf(s[1])[1] - vv[1]) for s, vv in zip(segs, v)]
        ot = [(tf(s[2])[0] - vv[0], tf(s[2])[1] - vv[1]) for s, vv in zip(segs, v)]
        out.append(bezier(v, it, ot, closed))
    return out


def svg_shapes(d, scale=1.0, offset=(0, 0), name="svg"):
    """svg_path() wrapped as path() shape items, ready to go in a group with a fill."""
    return [path(b, f"{name}{i}") for i, b in enumerate(svg_path(d, scale, offset))]


# ---------------------------------------------------------------- composition

class Comp:
    def __init__(self, name, width, height, fps=30, frames=90):
        self.name, self.w, self.h, self.fps, self.frames = name, width, height, fps, frames
        self.layers = []
        self.slots = {}
        self.markers = []
        self._ind = 0

    def slot(self, sid, color):
        """Declare a user-editable colour slot; reference it with fill(slot=sid) / stroke(slot=sid)."""
        self.slots[sid] = {"p": {"a": 0, "k": hex_color(color)}}
        return sid

    def marker(self, name, start, duration=0):
        self.markers.append({"cm": name, "tm": start, "dr": duration})

    def layer(self, name, shapes, ip=0, op=None, parent=None, matte=None, blend=0, hidden=False,
              **tr):
        """Add a shape layer; layers added first draw on top. Returns its index for parenting.

        matte: "alpha" / "alpha_inverted" / "luma" uses the layer added right before this one as
        its track matte; that layer is marked `td` and is not drawn on its own.
        """
        self._ind += 1
        L = {"ddd": 0, "ind": self._ind, "ty": 4, "nm": name, "sr": 1, "ks": transform(**tr),
             "ao": 0, "shapes": list(shapes), "ip": ip, "op": self.frames if op is None else op,
             "st": 0, "bm": blend}
        if parent is not None:
            L["parent"] = parent
        if hidden:
            L["hd"] = True
        if matte:
            L["tt"] = {"alpha": 1, "alpha_inverted": 2, "luma": 3}[matte]
            self.layers[-1]["td"] = 1
        self.layers.append(L)
        return self._ind

    def null(self, name, ip=0, op=None, parent=None, **tr):
        self._ind += 1
        L = {"ddd": 0, "ind": self._ind, "ty": 3, "nm": name, "sr": 1, "ks": transform(**tr),
             "ao": 0, "ip": ip, "op": self.frames if op is None else op, "st": 0}
        if parent is not None:
            L["parent"] = parent
        self.layers.append(L)
        return self._ind

    def lottie(self):
        d = {"v": "5.12.0", "fr": self.fps, "ip": 0, "op": self.frames, "w": self.w, "h": self.h,
             "nm": self.name, "ddd": 0, "assets": [], "layers": self.layers}
        if self.slots:
            d["slots"] = self.slots
        if self.markers:
            d["markers"] = self.markers
        return d

    def save(self, path):
        def rnd(o):
            if isinstance(o, float):
                r = round(o, 3)
                return int(r) if r == int(r) else r
            if isinstance(o, list):
                return [rnd(x) for x in o]
            if isinstance(o, dict):
                return {k: rnd(v) for k, v in o.items()}
            return o

        with open(path, "w") as f:
            json.dump(rnd(self.lottie()), f, separators=(",", ":"))
