"""Shared parts for the second batch of reaction stickers.

Every sticker is drawn once and painted in one of a few styles by `Style`:

- glossy:  soft radial shading overlay, rim shade and specular highlights (classic emoji look).
- flat:    flat colours with a thick white die-cut border and a soft drop shadow (sticker).
- outline: bold ink outline on every part, cel shade and a hard offset shadow (cartoon).

Main colours stay slottable in every style: shading is a translucent overlay on top of the
slotted fill, never a baked gradient. Layers added first draw on top (see lottie_kit.Comp).
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

from _common import particle, sampled  # noqa: E402,F401
from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import HOLD, LINEAR, Anim, Comp  # noqa: E402,F401

CATEGORY = "reactions"
SPRING = (0.3, 1.9, 0.55, 1.0)
WHITE = "#FFFFFF"
BORDER = 12          # die-cut border thickness (px outside the silhouette)
LINE = 9             # outline-style silhouette line
FLINE = 7            # outline-style feature line
INK = {"glossy": "#4A2A10", "flat": "#3F2616", "outline": "#161616"}
FACE = {"glossy": "#FFC83D", "flat": "#FFCC3A", "outline": "#FFD23F"}
CAVITY = "#7A2614"
TONGUE = "#F2677A"
TEAR = "#4FC3F7"
RED = "#FF3B5C"
TAU = 2 * math.pi


# ---------------------------------------------------------------- math

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


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


def spring(u, freq=0.9, decay=5.0):
    """Damped spring 0 -> 1 over local time u (frames/10 feel): overshoots then settles."""
    if u <= 0:
        return 0.0
    return 1 - math.exp(-decay * u) * math.cos(TAU * freq * u)


def bump(t, t0, t1):
    """0 -> 1 -> 0 half-sine between t0 and t1."""
    if t <= t0 or t >= t1:
        return 0.0
    return math.sin(math.pi * (t - t0) / (t1 - t0))


def wave(t, T, k=1, ph=0.0):
    return math.sin(TAU * (k * t / T + ph))


def rot(p, deg):
    a = math.radians(deg)
    return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))


def smooth_closed(pts, k=1 / 6):
    """Closed Catmull-Rom curve through pts as a bezier() dict (for morphs keep len(pts) fixed)."""
    n = len(pts)
    ins, outs = [], []
    for i in range(n):
        a, c = pts[i - 1], pts[(i + 1) % n]
        tx, ty = (c[0] - a[0]) * k, (c[1] - a[1]) * k
        ins.append((-tx, -ty))
        outs.append((tx, ty))
    return bezier(pts, ins, outs, True)


def smooth_open(pts, k=1 / 6):
    n = len(pts)
    ins, outs = [], []
    for i in range(n):
        a, c = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        tx, ty = (c[0] - a[0]) * k, (c[1] - a[1]) * k
        ins.append((-tx, -ty))
        outs.append((tx, ty))
    return bezier(pts, ins, outs, False)


def morph(fn, t0, t1, step=2, name="morph"):
    """Path whose bezier comes from fn(t) (same vertex count every frame), sampled."""
    ts, t = [], t0
    while t < t1 - 1e-6:
        ts.append(t)
        t += step
    ts.append(t1)
    return path(Anim([(t, fn(t), LINEAR) for t in ts]), name)


def S(d, scale=1.0, offset=(0, 0)):
    return svg_shapes(d, scale, offset)


# ---------------------------------------------------------------- common silhouettes

HEART_D = ("M 0 38 C -30 20 -54 0 -54 -20 C -54 -39 -40 -51 -25 -51 C -13 -51 -4 -44 0 -33 "
           "C 4 -44 13 -51 25 -51 C 40 -51 54 -39 54 -20 C 54 0 30 20 0 38 Z")
TEAR_D = "M 0 -24 C 4 -14 13 -6 13 4 A 13 13 0 0 1 -13 4 C -13 -6 -4 -14 0 -24 Z"


def star_d(r, inner=0.48, points=5, rot0=-90):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot0 + i * 180 / points)
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def sparkle_d(r, pinch=0.16):
    tips = [(0, -r), (r, 0), (0, r), (-r, 0)]
    d = f"M 0 {-r} "
    for a, b in zip(tips, tips[1:] + tips[:1]):
        c1 = (a[0] * 0.25 + b[0] * pinch, a[1] * 0.25 + b[1] * pinch)
        c2 = (b[0] * 0.25 + a[0] * pinch, b[1] * 0.25 + a[1] * pinch)
        d += f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {b[0]} {b[1]} "
    return d + "Z"


def arc_d(r, a0, a1, cx=0, cy=0):
    """Open circular arc (degrees, 0 = +x, clockwise on screen)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f"M {p0[0]:.2f} {p0[1]:.2f} A {r} {r} 0 {large} {sweep} {p1[0]:.2f} {p1[1]:.2f}"


# ---------------------------------------------------------------- style painter

class Style:
    def __init__(self, kind):
        assert kind in ("glossy", "flat", "outline"), kind
        self.kind = kind
        self.ink = INK[kind]
        self.face = FACE[kind]
        self.glossy, self.flat, self.outline = kind == "glossy", kind == "flat", kind == "outline"

    # -- paints (lists of fill/stroke items applied to the paths before them in a group)

    def gloss(self, box, strength=1.0):
        """Radial shading overlay for a shape with bounding box (x0, y0, x1, y1)."""
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        c = (x0 + w * 0.33, y0 + h * 0.26)
        r = max(w, h) * 0.95
        return gradient_fill([(0, WHITE, 0.42 * strength), (0.38, WHITE, 0), (0.7, "#7A2A00", 0),
                              (1, "#7A2A00", 0.34 * strength)], c, (c[0] + r, c[1]), radial=True,
                             name="gloss")

    def paint(self, color, slot=None, box=None, lw=None, opacity=100, sil=False, gloss=1.0,
              under=False, edge=None):
        """Fill (+ outline / die-cut border / shading) for a part.

        sil=True marks an outer silhouette: flat gets the white die-cut border, outline the thick
        line. Inner parts get only the thinner feature line in the outline style. under=True puts
        the outline under the fill (for silhouettes built from overlapping shapes); edge adds a
        thin rim line in the glossy style."""
        items = []
        if self.outline and lw != 0 and not under:
            items.append(stroke(self.ink, lw or (LINE if sil else FLINE), slot="outline"))
        if self.glossy and edge and not under:
            items.append(stroke(edge, 3.5, 70))
        if self.glossy and box and gloss:
            items.append(self.gloss(box, gloss))
        items.append(fill(color, opacity, slot=slot))
        if self.glossy and edge and under:
            items.append(stroke(edge, 7))
        if self.outline and lw != 0 and under:
            items.append(stroke(self.ink, 2 * (lw or (LINE if sil else FLINE)), slot="outline"))
        if self.flat and sil:
            items.append(stroke(WHITE, 2 * BORDER, slot="outline", name="diecut"))
        return items

    def line(self, w, color=None, opacity=100):
        return [stroke(color or self.ink, w * (1.15 if self.outline else 1), opacity)]

    def shadow(self, shapes, offset=None, name="shadow"):
        """Drop shadow group under a silhouette (flat: soft, outline: hard ink, glossy: none)."""
        if self.glossy:
            return []
        if self.flat:
            return [group(list(shapes) + [fill("#000000", 22), stroke("#000000", 2 * BORDER, 22)],
                          name=name, position=offset or (0, 9))]
        return [group(list(shapes) + [fill(self.ink), stroke(self.ink, LINE)],
                      name=name, position=offset or (6, 8))]

    def body(self, shapes, color, slot=None, box=None, top=(), shade=None, name="body", shadow=True,
             gloss=1.0, under=False, edge=None, spec=True):
        """A silhouette part: [top details..., shade, main, shadow] groups ready for a layer.

        shade: optional paths of a darker cel/rim shade clipped by eye (drawn over the main fill).
        """
        out = list(top)
        if shade:
            out.append(group(list(shade) + [fill("#6A2A00", 22 if self.glossy else 16)], name="shade"))
        if self.glossy and box and spec:
            hx, hy = box[0] + (box[2] - box[0]) * 0.3, box[1] + (box[3] - box[1]) * 0.2
            sz = (box[2] - box[0]) * 0.22
            out.append(group([ellipse((sz, sz * 0.5)), fill(WHITE, 60)], name="spec",
                             position=(hx, hy), rotation=-38))
        out.append(group(list(shapes) + self.paint(color, slot, box, sil=True, gloss=gloss, under=under,
                                                   edge=edge), name=name))
        if shadow:
            out += self.shadow(shapes)
        return out

    # -- faces

    def face_disc(self, R, color=None, slot="primary", shade=True, shapes=None, shadow=True):
        """Round emoji face centred on (0, 0); shapes replaces the disc (e.g. a cut-open head)."""
        color = color or self.face
        disc = list(shapes) if shapes else [ellipse((2 * R, 2 * R))]
        out = []
        if self.glossy:
            out.append(group([ellipse((R * 0.1, R * 0.1)), fill(WHITE, 70)], name="glint",
                             position=(-R * 0.2, -R * 0.8)))
            out.append(group([ellipse((R * 0.44, R * 0.2)), fill(WHITE, 55)], name="highlight",
                             position=(-R * 0.5, -R * 0.6), rotation=-44))
        elif self.flat:
            out.append(group([ellipse((R * 0.3, R * 0.14)), fill(WHITE, 75)], name="highlight",
                             position=(-R * 0.55, -R * 0.55), rotation=-45))
        else:
            out.append(group(S(arc_d(R * 0.74, 200, 238)) + [stroke(WHITE, 10)], name="highlight"))
        if shade:
            rr = R * (1.1 if self.glossy else 1.14)
            out.append(group(S(f"M {-R} 0 A {R} {R} 0 0 0 {R} 0 A {rr} {rr} 0 0 1 {-R} 0 Z") +
                             [fill("#B35C00", 24 if self.glossy else 18)], name="rim"))
        out.append(group(disc + self.paint(color, slot, (-R, -R, R, R), sil=True), name="face"))
        if shadow:
            out += self.shadow(disc)
        return out

    def eye(self, w, h, catch=True):
        """Solid oval eye with a catchlight."""
        out = []
        if catch and not self.flat:
            out.append(group([ellipse((w * 0.36, h * 0.3)), fill(WHITE, 90)], name="catch",
                             position=(-w * 0.16, -h * 0.2)))
        elif catch:
            out.append(group([ellipse((w * 0.3, w * 0.3)), fill(WHITE)], name="catch",
                             position=(-w * 0.15, -h * 0.2)))
        out.append(group([ellipse((w, h)), fill(self.ink)], name="eye"))
        return out

    def white_eye(self, w, h, pupil=0.5, pupil_pos=(0, 0)):
        """Big white eyeball with a pupil."""
        pw = w * pupil
        return [
            group([ellipse((pw * 0.34, pw * 0.34)), fill(WHITE)], name="catch",
                  position=(pupil_pos[0] - pw * 0.18, pupil_pos[1] - pw * 0.2)),
            group([ellipse((pw, pw * 1.08)), fill(self.ink)], name="pupil", position=pupil_pos),
            group([ellipse((w, h))] + self.paint(WHITE, lw=FLINE - 1), name="white"),
        ]

    def mouth(self, d, tongue=None, teeth=None, cavity=CAVITY):
        """Open mouth from an SVG path, with optional tongue ellipse ((w, h), (x, y)) and a teeth
        band path. Everything is clipped to the mouth by construction (drawn small enough)."""
        out = []
        if self.outline:
            out.append(group(S(d) + [stroke(self.ink, FLINE, slot="outline")], name="mouth-line"))
        if teeth:
            out.append(group(S(teeth) + [fill(WHITE)], name="teeth"))
        if tongue:
            out.append(group([ellipse(tongue[0], tongue[1]), fill(TONGUE)], name="tongue"))
        out.append(group(S(d) + [fill(cavity)], name="cavity"))
        return out

    def brow(self, d, w=10):
        return [group(S(d) + self.line(w), name="brow")]


def blush(w=46, h=22, opacity=45):
    return [ellipse((w, h)), fill("#FF6F7D", opacity)]


# ---------------------------------------------------------------- build

def build3(aid, name, description, tags, make, specs):
    """specs: [(vid, vname, playback, thumb_t, description[, bg]), ...]; make(vid) -> Comp."""
    variants = [Variant(sp[0], sp[1], make(sp[0]), sp[2], thumb_t=sp[3], description=sp[4],
                        bg=sp[5] if len(sp) > 5 else None) for sp in specs]
    build_asset(CATEGORY, aid, name, description, tags, variants)


def rng(seed):
    return random.Random(seed)


def face_null(comp, T, R, cx, cy, dpos=None, drot=None, dscale=None, step=1, name="face"):
    """Null anchored at the bottom of a face of radius R centred at (cx, cy); dpos(t) -> (dx, dy),
    drot(t) -> degrees, dscale(t) -> (sx, sy) in %."""
    kw = {}
    kw["position"] = sampled(lambda t: (cx + dpos(t)[0], cy + R + dpos(t)[1]), 0, T, step) if dpos \
        else (cx, cy + R)
    if drot:
        kw["rotation"] = sampled(drot, 0, T, step)
    if dscale:
        kw["scale"] = sampled(lambda t: list(dscale(t)), 0, T, step)
    return comp.null(name, anchor=(0, R), **kw)


def add_mouth(comp, st, d, parent, tongue=None, teeth=None, cavity=CAVITY, name="mouth", **tr):
    """Open mouth clipped by an alpha matte: cavity, optional tongue ((w, h), (x, y)) and teeth
    band path, plus the ink outline in the outline style. tr goes to the mouth null."""
    m = comp.null(name, parent=parent, **tr)
    if st.outline:
        comp.layer(name + "-line", [group(S(d) + [stroke(st.ink, FLINE, slot="outline")])], parent=m)
    comp.layer(name + "-matte", [group(S(d) + [fill(WHITE)])], parent=m)
    inside = []
    if teeth:
        inside.append(group(S(teeth) + [fill(WHITE)], name="teeth"))
    if tongue:
        inside.append(group([ellipse(tongue[0], tongue[1]), fill(TONGUE)], name="tongue"))
    inside.append(group(S(d) + [fill(cavity)], name="cavity"))
    comp.layer(name + "-inside", inside, parent=m, matte="alpha")
    return m


def mirror(shapes, dx=0.0):
    """Copies of static path() shapes mirrored left-right (x -> -x + dx)."""
    out = []
    for sh in shapes:
        b = sh["ks"]["k"]
        out.append(path(bezier([(-x + dx, y) for x, y in b["v"]], [(-x, y) for x, y in b["i"]],
                               [(-x, y) for x, y in b["o"]], b["c"])))
    return out


def capsule_d(p0, p1, r):
    """Stadium (rounded bar) of radius r from p0 to p1 as an SVG path."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1e-6
    nx, ny = -dy / L * r, dx / L * r
    a = (p0[0] + nx, p0[1] + ny)
    b = (p1[0] + nx, p1[1] + ny)
    c = (p1[0] - nx, p1[1] - ny)
    d = (p0[0] - nx, p0[1] - ny)
    # clockwise on screen, like lottie rect/ellipse, so overlapping unions don't cancel out
    return (f"M {a[0]:.2f} {a[1]:.2f} A {r} {r} 0 0 1 {d[0]:.2f} {d[1]:.2f} L {c[0]:.2f} {c[1]:.2f} "
            f"A {r} {r} 0 0 1 {b[0]:.2f} {b[1]:.2f} Z")


def capsule(p0, p1, r):
    return S(capsule_d(p0, p1, r))


def rain(comp, name, n, T, W, H, shapes, seed, life=(0.8, 1.0), size=(0.7, 1.1), sway=18,
         spin=120, flip=0.0, fade=0.14, rise=False, margin=50, step=2, x_range=None, tumble=0.0,
         y_end=None, fade_out=None):
    """Particles falling (or rising) across the canvas, staggered so a loop of T frames is seamless.

    shapes(i) -> shape items for particle i. flip: amount of 3D flutter (scale-x cosine), tumble:
    extra scale-y flutter. Particles fade in/out near the ends so they never hard-clip.
    """
    r = random.Random(seed)
    xr = x_range or (margin * 0.6, W - margin * 0.6)
    lanes = [xr[0] + (xr[1] - xr[0]) * (i + 0.5) / n for i in range(n)]
    r.shuffle(lanes)
    for i in range(n):
        lf = round(T * r.uniform(*life))
        t0 = round(i * T / n + r.uniform(0, T / n * 0.6), 2) % T
        x0 = lanes[i] + r.uniform(-12, 12)
        sz = r.uniform(*size)
        amp = r.uniform(0.5, 1.0) * sway * r.choice((-1, 1))
        ph = r.uniform(0, 1)
        sp = r.uniform(0.5, 1.0) * spin * r.choice((-1, 1))
        fw = r.uniform(1.0, 2.2)
        rot0 = r.uniform(-30, 30)

        def fn(u, x0=x0, sz=sz, amp=amp, ph=ph, sp=sp, fw=fw, rot0=rot0, lf=lf):
            k = u / lf
            ya, yb = (H + margin, -margin) if rise else (-margin, H + margin)
            if y_end is not None:
                yb = y_end
            y = ya + (yb - ya) * k
            x = x0 + amp * math.sin(TAU * (k * 1.3 + ph))
            fx = 1 - flip * (0.5 - 0.5 * math.cos(TAU * (k * fw + ph)))
            fy = 1 - tumble * (0.5 - 0.5 * math.cos(TAU * (k * fw * 0.7 + ph + 0.3)))
            o = smooth(k / fade) * smooth((1 - k) / (fade_out or fade))
            s = 100 * sz
            return {"position": (x, y), "rotation": rot0 + sp * k + (amp * 0.6 * math.cos(TAU * (k * 1.3 + ph))),
                    "scale": (s * fx, s * fy), "opacity": 100 * o}

        particle(comp, f"{name}{i}", shapes(i), t0, lf, T, fn, step=step)
