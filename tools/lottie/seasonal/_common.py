"""Shared helpers for the seasonal / holiday Lottie overlays.

Math and motion helpers (seamless-loop sampling, particles, falling/rising drifts), path helpers
(SVG-ish strings, Catmull-Rom curves, morphs, hand-drawn "boil"), and a few reusable parts
(flames, soft glows, sparkles, catenary wires). Layers added first draw on top (lottie_kit.Comp).
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

from drift_lottie import Variant, build_asset  # noqa: E402,F401
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import HOLD, LINEAR, Anim, Comp  # noqa: E402,F401

CATEGORY = "seasonal"
TAU = 2 * math.pi
WHITE = "#FFFFFF"
INK = "#2A2233"          # doodle ink
SPRING = (0.3, 1.9, 0.55, 1.0)
DECEL = (0.2, 0.0, 0.1, 1.0)


def build(aid, name, description, tags, variants):
    build_asset(CATEGORY, aid, name, description, tags, variants)


# ---------------------------------------------------------------- math

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, k):
    return a + (b - a) * k


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x, p=3):
    return 1 - (1 - clamp(x)) ** p


def ease_in(x, p=2):
    return clamp(x) ** p


def ease_in_out(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back_out(x, s=1.9):
    x = clamp(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def spring(u, freq=1.0, decay=5.0):
    """Damped spring 0 -> 1 over normalized time u: overshoots then settles."""
    if u <= 0:
        return 0.0
    return 1 - math.exp(-decay * u) * math.cos(TAU * freq * u)


def bump(t, t0, t1):
    """0 -> 1 -> 0 half-sine between t0 and t1."""
    if t <= t0 or t >= t1:
        return 0.0
    return math.sin(math.pi * (t - t0) / (t1 - t0))


def wave(t, T, k=1, ph=0.0):
    """Seamless over T when k is an integer."""
    return math.sin(TAU * (k * t / T + ph))


def flicker(t, T, seed=0, amt=1.0):
    """Seamless pseudo-random flicker in about [-1, 1] (sum of integer-harmonic sines)."""
    r = random.Random(seed)
    v = 0.0
    for k, w in ((3, 0.45), (5, 0.3), (8, 0.18), (13, 0.12)):
        v += w * math.sin(TAU * (k * t / T + r.random()))
    return v * amt


def rot(p, deg):
    a = math.radians(deg)
    return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))


def rng(seed):
    return random.Random(seed)


# ---------------------------------------------------------------- sampling / particles

def sampled(fn, t0, t1, step=1, easing=LINEAR):
    """Keys sampled from fn(t) at t0, t0+step, ..., t1 (t1 always included)."""
    ts, t = [], t0
    while t < t1 - 1e-6:
        ts.append(round(t, 3))
        t += step
    ts.append(t1)
    return Anim([(t, fn(t), easing) for t in ts])


def looped(fn, T, step=2):
    """sampled() over a whole loop; fn(T) is forced to fn(0) so the loop is exact."""
    return sampled(lambda t: fn(0 if t >= T else t), 0, T, step)


def particle(comp, name, shapes, t0, life, total, fn, step=1, wrap=True, parent=None, **static):
    """A short-lived layer whose transform comes from fn(u) -> dict(position=, scale=, rotation=,
    opacity=) for local time u in [0, life]. If it outlives the comp and wrap is set, a copy
    shifted back by `total` frames keeps a loop seamless."""
    starts = [t0] + ([t0 - total] if wrap and t0 + life > total else [])
    for s in starts:
        keys = {}
        for k in fn(0):
            keys[k] = sampled(lambda t, k=k, s=s: fn(min(max(t - s, 0), life))[k], s, s + life, step)
        comp.layer(name, shapes, ip=s, op=s + life, parent=parent, **static, **keys)


def drift(comp, name, n, T, W, H, shapes, seed, life=(0.8, 1.0), size=(0.7, 1.1), sway=18,
          spin=120, flip=0.0, tumble=0.0, fade=0.12, rise=False, margin=60, step=2, x_range=None,
          wind=0.0, depth=None, opacity=(100, 100), y_range=None):
    """Particles falling (or rising) across a W x H box, staggered so a loop of T frames is seamless.

    shapes(i, depth) -> shape items for particle i. wind: horizontal travel (px) over a lifetime.
    flip / tumble: 3D flutter amounts on scale-x / scale-y. depth(i) -> 0..1 optional parallax
    factor (0 far: small, slow, faint; 1 near) used with size/opacity ranges.
    """
    r = random.Random(seed)
    xr = x_range or (margin * 0.4 - wind * 0.5, W - margin * 0.4 - wind * 0.5)
    lanes = [xr[0] + (xr[1] - xr[0]) * (i + 0.5) / n for i in range(n)]
    r.shuffle(lanes)
    for i in range(n):
        d = depth(i) if depth else r.random()
        lf = round(T * lerp(life[1], life[0], d) if depth else T * r.uniform(*life))
        t0 = round(i * T / n + r.uniform(0, T / n * 0.7), 2) % T
        x0 = lanes[i] + r.uniform(-10, 10)
        sz = lerp(size[0], size[1], d) if depth else r.uniform(*size)
        op = lerp(opacity[0], opacity[1], d)
        amp = r.uniform(0.5, 1.0) * sway * r.choice((-1, 1))
        ph = r.uniform(0, 1)
        sp = r.uniform(0.4, 1.0) * spin * r.choice((-1, 1))
        fw = r.uniform(1.0, 2.2)
        rot0 = r.uniform(-40, 40)
        ya, yb = y_range or ((H + margin, -margin) if rise else (-margin, H + margin))

        def fn(u, x0=x0, sz=sz, amp=amp, ph=ph, sp=sp, fw=fw, rot0=rot0, lf=lf, op=op):
            k = u / lf
            y = ya + (yb - ya) * k
            x = x0 + wind * k + amp * math.sin(TAU * (k * 1.3 + ph))
            fx = 1 - flip * (0.5 - 0.5 * math.cos(TAU * (k * fw + ph)))
            fy = 1 - tumble * (0.5 - 0.5 * math.cos(TAU * (k * fw * 0.7 + ph + 0.3)))
            o = smooth(k / fade) * smooth((1 - k) / fade) if fade else 1
            s = 100 * sz
            return {"position": (x, y),
                    "rotation": rot0 + sp * k + amp * 0.5 * math.cos(TAU * (k * 1.3 + ph)),
                    "scale": (s * fx, s * fy), "opacity": op * o}

        particle(comp, f"{name}{i}", shapes(i, d), t0, lf, T, fn, step=step)


# ---------------------------------------------------------------- paths

def S(d, scale=1.0, offset=(0, 0)):
    return svg_shapes(d, scale, offset)


def pts_d(pts, closed=True):
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    return d + (" Z" if closed else "")


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


def boil(bez_fn, T, every=4, amp=2.2, seed=1, name="boil"):
    """Hand-drawn line boil: bez_fn(jitter) -> bezier, where jitter(i) -> (dx, dy) per vertex.
    New jitter every `every` frames with held keys; seamless over T (T % every == 0)."""
    keys = []
    n = max(1, T // every)
    for j in range(n):
        r = random.Random(seed * 1000 + j)
        cache = {}

        def jit(i, r=r, cache=cache):
            if i not in cache:
                cache[i] = (r.uniform(-amp, amp), r.uniform(-amp, amp))
            return cache[i]
        keys.append((j * every, bez_fn(jit), HOLD))
    keys.append((T, keys[0][1], HOLD))
    return path(Anim(keys), name)


def boil_pts(pts, T, closed=True, every=4, amp=2.2, seed=1, k=1 / 6):
    """boil() for a Catmull-Rom curve through pts."""
    mk = smooth_closed if closed else smooth_open
    return boil(lambda j: mk([(x + j(i)[0], y + j(i)[1]) for i, (x, y) in enumerate(pts)], k), T,
                every, amp, seed)


def circle_pts(r, n=12, cx=0, cy=0, sx=1.0, sy=1.0, a0=-90):
    return [(cx + r * sx * math.cos(math.radians(a0 + 360 * i / n)),
             cy + r * sy * math.sin(math.radians(a0 + 360 * i / n))) for i in range(n)]


def arc_d(r, a0, a1, cx=0, cy=0):
    """Open circular arc (degrees, 0 = +x, clockwise on screen)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f"M {p0[0]:.2f} {p0[1]:.2f} A {r} {r} 0 {large} {sweep} {p1[0]:.2f} {p1[1]:.2f}"


def star_d(r, inner=0.48, points=5, rot0=-90, cx=0, cy=0):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot0 + i * 180 / points)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts_d(pts)


def sparkle_d(r, pinch=0.16):
    """Four-point twinkle star."""
    tips = [(0, -r), (r, 0), (0, r), (-r, 0)]
    d = f"M 0 {-r} "
    for a, b in zip(tips, tips[1:] + tips[:1]):
        c1 = (a[0] * 0.25 + b[0] * pinch, a[1] * 0.25 + b[1] * pinch)
        c2 = (b[0] * 0.25 + a[0] * pinch, b[1] * 0.25 + a[1] * pinch)
        d += f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {b[0]} {b[1]} "
    return d + "Z"


HEART_D = ("M 0 38 C -30 20 -54 0 -54 -20 C -54 -39 -40 -51 -25 -51 C -13 -51 -4 -44 0 -33 "
           "C 4 -44 13 -51 25 -51 C 40 -51 54 -39 54 -20 C 54 0 30 20 0 38 Z")


def heart_pts(s=1.0, n=24):
    """Points on the classic parametric heart (centred, ~108 px wide at s=1), for boil()."""
    out = []
    for i in range(n):
        t = TAU * i / n
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        out.append((x * 3.3 * s, (y + 2) * 3.3 * s))
    return out


def capsule_d(p0, p1, r):
    """Stadium (rounded bar) of radius r from p0 to p1 as an SVG path (clockwise)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1e-6
    nx, ny = -dy / L * r, dx / L * r
    a = (p0[0] + nx, p0[1] + ny)
    b = (p1[0] + nx, p1[1] + ny)
    c = (p1[0] - nx, p1[1] - ny)
    d = (p0[0] - nx, p0[1] - ny)
    return (f"M {a[0]:.2f} {a[1]:.2f} A {r} {r} 0 0 1 {d[0]:.2f} {d[1]:.2f} L {c[0]:.2f} {c[1]:.2f} "
            f"A {r} {r} 0 0 1 {b[0]:.2f} {b[1]:.2f} Z")


def mirror_pts(pts):
    return [(-x, y) for x, y in reversed(pts)]


def sag_pts(p0, p1, sag, n=16):
    """Hanging wire from p0 to p1 sagging by `sag` px at the middle (parabola)."""
    out = []
    for i in range(n + 1):
        k = i / n
        out.append((lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) + sag * 4 * k * (1 - k)))
    return out


def sag_at(p0, p1, sag, k):
    return (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) + sag * 4 * k * (1 - k))


def sag_slope(p0, p1, sag, k):
    """Angle (deg) of the hanging wire at k."""
    dx = p1[0] - p0[0]
    dy = (p1[1] - p0[1]) + sag * 4 * (1 - 2 * k)
    return math.degrees(math.atan2(dy, dx))


# ---------------------------------------------------------------- parts

def glow(r, color, opacity=60, falloff=((0, 1.0), (0.35, 0.45), (1, 0.0)), position=(0, 0),
         name="glow", sy=1.0):
    """Soft radial glow disc (fixed colour: gradients cannot be slotted)."""
    stops = [(o, color, a) for o, a in falloff]
    return group([group([ellipse((2 * r, 2 * r)),
                         gradient_fill(stops, (0, 0), (r, 0), radial=True, opacity=opacity)], "disc",
                        scale=(100, 100 * sy))],
                 name, position=position)


def slot_glow(r, slot, color, opacity=40, rings=5, position=(0, 0), name="glow", sy=1.0):
    """Slottable soft glow: concentric translucent discs of one slotted colour."""
    items = []
    for j in range(rings):
        k = (j + 1) / rings
        items.append(group([ellipse((2 * r * k, 2 * r * k * sy)), fill(color, opacity / rings, slot=slot)],
                           f"{name}{j}"))
    return group(items, name, position=position)


def flame_bez(h, w, tip=0.0, lean=0.0):
    """Teardrop flame: base at (0, 0), tip at (tip, -h). w: half-width of the belly."""
    by = -h * 0.28
    return bezier(
        [(tip, -h), (w + lean * 0.3, by), (0, w * 0.55), (-w + lean * 0.3, by)],
        [(-w * 0.05, 0), (w * 0.12 + lean * 0.1, -h * 0.34), (w * 0.62, 0), (-w * 0.02, w * 0.62)],
        [(w * 0.05, 0), (0.02 * w, w * 0.62), (-w * 0.62, 0), (-w * 0.12 + lean * 0.1, -h * 0.34)],
        True)


def flame_layers(comp, name, T, h=60, w=16, seed=0, parent=None, position=(0, 0), step=2,
                 outer="#FF8A1F", mid="#FFC53D", core="#FFF6D8", halo="#FFB347", halo_r=None,
                 halo_opacity=55, slot=None, speed=1.0, lean=0.0, ip=0, op=None, scale=100,
                 opacity=None):
    """Flickering candle flame (outer / mid / core + halo), seamless over T. Returns the null."""
    op = T if op is None else op
    kw = {"opacity": opacity} if opacity is not None else {}
    n = comp.null(name, parent=parent, position=position, ip=ip, op=op, scale=(scale, scale))

    def f(t, k=1.0):
        a = flicker(t * speed, T, seed)
        b = flicker(t * speed, T, seed + 7)
        return flame_bez(h * k * (1 + 0.12 * a), w * k * (1 - 0.06 * a), tip=(w * 0.5 * b + lean) * k,
                         lean=lean * k)

    comp.layer(name + "-core", [group([morph(lambda t: f(t, 0.42), 0, T, step), fill(core)], "core",
                                      position=(0, -h * 0.02))], parent=n, ip=ip, op=op, **kw)
    comp.layer(name + "-mid", [group([morph(lambda t: f(t, 0.7), 0, T, step), fill(mid)], "mid")],
               parent=n, ip=ip, op=op, **kw)
    comp.layer(name + "-outer", [group([morph(lambda t: f(t, 1.0), 0, T, step),
                                        fill(outer, slot=slot)], "outer")], parent=n, ip=ip, op=op, **kw)
    if halo:
        hr = halo_r or h * 1.3
        comp.layer(name + "-halo", [glow(hr, halo, 100, position=(0, -h * 0.35))], parent=n, ip=ip, op=op,
                   opacity=opacity if opacity is not None else
                   looped(lambda t: halo_opacity * (1 + 0.22 * flicker(t * speed, T, seed + 3)), T, step),
                   scale=looped(lambda t: [100 + 6 * flicker(t * speed, T, seed + 5)] * 2, T, step))
    return n


def sparkle(comp, name, pos, T, r=14, color=WHITE, slot=None, t0=0, period=None, parent=None, spin=45,
            opacity=100):
    """Twinkling four-point star that pops in and out once per `period` frames (seamless)."""
    period = period or T
    reps = max(1, round(T / period))
    period = T / reps

    def fnv(t):
        u = ((t - t0) % period) / period
        if u > 0.5:
            return 0
        return 110 * math.sin(math.pi * u / 0.5) ** 1.5
    comp.layer(name, [group(S(sparkle_d(r)) + [fill(color, opacity, slot=slot)], "spark")], parent=parent,
               position=pos, scale=looped(lambda t: [fnv(t)] * 2, T, 1),
               rotation=looped(lambda t: spin * t / T * reps, T, 2))


def dots_ring(r, n, d, color, slot=None, a0=0, opacity=100):
    items = []
    for i in range(n):
        a = math.radians(a0 + 360 * i / n)
        items.append(ellipse((d, d), (r * math.cos(a), r * math.sin(a))))
    return items + [fill(color, opacity, slot=slot)]


def shade_overlay(box, strength=1.0, light=(0.32, 0.25), dark="#3A0A00"):
    """Translucent radial shading over a slotted fill (box = x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    c = (x0 + w * light[0], y0 + h * light[1])
    r = max(w, h) * 0.95
    return gradient_fill([(0, WHITE, 0.4 * strength), (0.4, WHITE, 0), (0.72, dark, 0),
                          (1, dark, 0.38 * strength)], c, (c[0] + r, c[1]), radial=True, name="shade")


def osc_keys(t0, t1, period, lo, hi, ph=0.0, window=None):
    """Eased ping-pong keys between lo and hi (numbers or lists) from t0 to t1; phase in periods.
    window=(a, b) drops keys that cannot affect frames a..b."""
    half = period / 2
    start = t0 - (ph % 1.0) * period
    keys = []
    t, j = start, 0
    while t < t1 + half:
        keys.append((round(t, 3), lo if j % 2 == 0 else hi, EASE_IN_OUT))
        t += half
        j += 1
    if window:
        a, b = window
        keep = [k for i, k in enumerate(keys)
                if (i + 1 < len(keys) and keys[i + 1][0] >= a) and (i == 0 or keys[i - 1][0] <= b)]
        keys = keep or keys[:2]
    return Anim(keys)


def fall(comp, name, n, T, W, H, shapes, seed, speed=(2.0, 4.0), sway=(10, 30), sway_period=(50, 90),
         spin=(0, 0), flip=0.0, flip_period=(30, 60), wind=0.0, margin=60, size=(0.6, 1.2),
         opacity=(100, 100), rise=False, depth_pow=1.0, x_range=None, parent=None):
    """Cheap long-travel particles for full-screen overlays (snow, leaves, hearts...), seamless over T.

    Each particle crosses the whole box at a constant speed (px/frame, from far to near depth),
    with an eased sway / flip / spin inside. Copies shifted by multiples of T keep the loop exact.
    shapes(i, depth) -> shape items; depth 0 = far (small, slow, faint), 1 = near."""
    r = random.Random(seed)
    lo = -margin + min(0.0, -wind * (H + 2 * margin) / speed[0])
    hi = W + margin + max(0.0, -wind * (H + 2 * margin) / speed[0])
    lo, hi = x_range or (lo, hi)
    lanes = [lo + (hi - lo) * (i + 0.5) / n for i in range(n)]
    r.shuffle(lanes)
    order = list(range(n))
    for i in order:
        d = r.random() ** depth_pow
        v = lerp(speed[0], speed[1], d)
        dist = H + 2 * margin
        life = dist / v
        sz = lerp(size[0], size[1], d)
        op = lerp(opacity[0], opacity[1], d)
        t0 = r.uniform(0, T)
        x0 = lanes[i] + r.uniform(-15, 15)
        amp = r.uniform(*sway)
        sp = r.uniform(*sway_period)
        sp = T / max(1, round(T / sp))  # sway period divides T so every copy lines up
        ph = r.random()
        rs = r.uniform(*spin) * r.choice((-1, 1))
        fp = r.uniform(*flip_period)
        fp = T / max(1, round(T / fp))
        rot0 = r.uniform(0, 360)
        ya, yb = (H + margin, -margin) if rise else (-margin, H + margin)
        k = 0
        items = shapes(i, d)
        while True:
            s = t0 - k * T
            if s + life <= 0:
                break
            k += 1
            e = s + life
            pos = Anim([(round(s, 3), [x0, ya], LINEAR), (round(e, 3), [x0 + wind * life, yb], LINEAR)])
            inner = {"position": osc_keys(s, e, sp, [-amp, 0], [amp, 0], ph, (0, T))}
            if rs:
                inner["rotation"] = Anim([(round(s, 3), rot0, LINEAR), (round(e, 3), rot0 + rs * life / 60)])
            else:
                inner["rotation"] = osc_keys(s, e, sp, -amp * 0.5, amp * 0.5, ph + 0.25, (0, T))
            g = group(items, "p")
            g["it"][-1] = transform(shape=True, **inner)
            outer = [g]
            if flip:
                f = group([g], "flip")
                f["it"][-1] = transform(shape=True, scale=osc_keys(s, e, fp, [100, 100],
                                                                    [100 * (1 - flip), 100], ph, (0, T)))
                outer = [f]
            comp.layer(f"{name}{i}", outer, ip=max(0, math.floor(s)), op=min(T, math.ceil(e)), parent=parent,
                       position=pos, scale=(100 * sz, 100 * sz), opacity=op)


def sample_bez(b, per=8):
    """Dense polygon points along a bezier() dict."""
    v, ii, oo = b["v"], b["i"], b["o"]
    n = len(v)
    segs = n if b["c"] else n - 1
    out = []
    for s in range(segs):
        p0, p3 = v[s], v[(s + 1) % n]
        p1 = (p0[0] + oo[s][0], p0[1] + oo[s][1])
        p2 = (p3[0] + ii[(s + 1) % n][0], p3[1] + ii[(s + 1) % n][1])
        for j in range(per):
            t = j / per
            a, b_, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
            out.append((a * p0[0] + b_ * p1[0] + c * p2[0] + d * p3[0],
                        a * p0[1] + b_ * p1[1] + c * p2[1] + d * p3[1]))
    return out


def clip_half(pts, side=1, x0=0.0):
    """Sutherland-Hodgman clip of a closed polygon to x*side >= x0*side."""
    out = []
    n = len(pts)
    inside = lambda p: (p[0] - x0) * side >= 0
    for i in range(n):
        a, b = pts[i - 1], pts[i]
        if inside(b):
            if not inside(a):
                k = (x0 - a[0]) / (b[0] - a[0])
                out.append((x0, a[1] + (b[1] - a[1]) * k))
            out.append(b)
        elif inside(a):
            k = (x0 - a[0]) / (b[0] - a[0])
            out.append((x0, a[1] + (b[1] - a[1]) * k))
    return out
