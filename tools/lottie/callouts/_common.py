"""Shared helpers for the callouts category: hand-drawn brush strokes and asset output.

A brush stroke is a filled, variable-width ribbon (so it can taper like a real marker) revealed
along its centreline by a trim-path stroke used as an alpha track matte. Long or self-overlapping
strokes are split into chunks, each with its own matte, so a loop crossing itself is not revealed
early.
"""

import json
import math
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "lottie"))
from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import LINEAR, anim, bezier, fill, group, path, stroke, trim  # noqa: E402

RENDER = ROOT / "tools" / "skottie-render" / "build" / "skottie-render"
CATEGORY = "callouts"


# ---------------------------------------------------------------- easing / curves

def ease_eval(e, u):
    """Evaluate a kit easing tuple (x1, y1, x2, y2) at progress u in 0..1."""
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


def catmull(points, samples=24):
    """Centripetal-ish uniform Catmull-Rom through points -> dense polyline."""
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * t
                                    + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(tuple(points[-1]))
    return out


def resample(poly, spacing=2.5):
    """Resample a polyline at even arc-length spacing."""
    d = [0.0]
    for a, b in zip(poly, poly[1:]):
        d.append(d[-1] + math.dist(a, b))
    total = d[-1]
    n = max(2, int(total / spacing) + 1)
    out, j = [], 0
    for i in range(n):
        s = total * i / (n - 1)
        while j < len(d) - 2 and d[j + 1] < s:
            j += 1
        seg = d[j + 1] - d[j] or 1
        t = (s - d[j]) / seg
        a, b = poly[j], poly[j + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out, total


def smoothstep(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- ribbon

def ribbon(center, width_fn, cap_start=True, cap_end=True, start_edge=None, end_edge=None):
    """Closed polygon around `center` whose full width at arc fraction u is width_fn(u).

    Ends get a round cap unless start_edge / end_edge (lists of points, from left side to right
    side) replace it, e.g. for a ragged highlighter end.
    """
    n = len(center)
    left, right, normals = [], [], []
    for i, p in enumerate(center):
        a = center[max(0, i - 1)]
        b = center[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        normals.append((nx, ny))
        w = width_fn(i / (n - 1)) / 2
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))

    def cap(c, nrm, w):
        # half circle from left side to right side, bulging along +/- tangent
        # nrm points to the side the cap starts from; (nrm.y, -nrm.x) then points out of the end
        tx, ty = nrm[1], -nrm[0]
        pts = []
        for k in range(1, 8):
            a = math.pi * k / 8
            pts.append((c[0] + (nrm[0] * math.cos(a) + tx * math.sin(a)) * w,
                        c[1] + (nrm[1] * math.cos(a) + ty * math.sin(a)) * w))
        return pts

    poly = list(left)
    if end_edge is not None:
        poly += end_edge
    elif cap_end:
        poly += cap(center[-1], normals[-1], width_fn(1) / 2)
    poly += right[::-1]
    if start_edge is not None:
        poly += start_edge
    elif cap_start:
        pts = cap(center[0], (-normals[0][0], -normals[0][1]), width_fn(0) / 2)
        poly += pts
    return bezier(poly, closed=True)


def pressure(base, taper_in=0.12, taper_out=0.25, min_in=0.35, min_out=0.15, wobble=0.08, seed=0,
             length=None):
    """Width profile: quick press at the start, lighter flick at the end, slight wobble.

    taper_in / taper_out are fractions of the stroke length.
    """
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    fr = [rnd.uniform(1.2, 2.2), rnd.uniform(3.0, 5.0), rnd.uniform(7, 11)]

    def fn(u):
        w = 1.0
        if taper_in > 0:
            w *= min_in + (1 - min_in) * smoothstep(u / taper_in)
        if taper_out > 0:
            w *= min_out + (1 - min_out) * smoothstep((1 - u) / taper_out)
        w *= 1 + wobble * (0.55 * math.sin(fr[0] * 6.283 * u + ph[0])
                           + 0.3 * math.sin(fr[1] * 6.283 * u + ph[1])
                           + 0.15 * math.sin(fr[2] * 6.283 * u + ph[2]))
        return base * w

    return fn


def jitter(points, amount, seed=0):
    rnd = random.Random(seed)
    return [(x + rnd.uniform(-amount, amount), y + rnd.uniform(-amount, amount)) for x, y in points]


# ---------------------------------------------------------------- brush strokes

class Brush:
    """One pen stroke. Add several to a Strokes set, then emit them onto a comp."""

    def __init__(self, points, t0, t1, width_fn, max_width, easing=(0.45, 0.0, 0.35, 1.0),
                 chunks=1, smooth=True, color="#FFFFFF", slot=None, opacity=100, name="stroke",
                 extra=None, start_edge=None, end_edge=None, spacing=2.5):
        dense = catmull(points) if smooth else points
        self.center, self.length = resample(dense, spacing)
        self.t0, self.t1, self.easing = t0, t1, easing
        self.width_fn, self.max_width = width_fn, max_width
        self.chunks, self.color, self.slot, self.opacity = chunks, color, slot, opacity
        self.name = name
        self.extra = extra or []  # extra shape items (e.g. ink streaks) drawn above the fill
        self.start_edge, self.end_edge = start_edge, end_edge

    def progress(self, f):
        if self.t1 <= self.t0:
            return 1.0 if f >= self.t0 else 0.0
        return ease_eval(self.easing, (f - self.t0) / (self.t1 - self.t0))

    def layers(self):
        """[(name, matte_shapes, content_shapes, ip)] one per chunk."""
        n = len(self.center)
        out = []
        overlap = 3
        for c in range(self.chunks):
            a = round(c * (n - 1) / self.chunks)
            b = round((c + 1) * (n - 1) / self.chunks)
            a0, b0 = max(0, a - (overlap if c else 0)), min(n - 1, b + overlap)
            ua, ub = a / (n - 1), b / (n - 1)
            seg = self.center[a0:b0 + 1]
            wf = (lambda s, a0=a0, b0=b0: self.width_fn((a0 + s * (b0 - a0)) / (n - 1)))
            rib = ribbon(seg, wf, cap_start=(c == 0), cap_end=(c == self.chunks - 1),
                         start_edge=self.start_edge if c == 0 else None,
                         end_edge=self.end_edge if c == self.chunks - 1 else None)
            keys, prev = [], None
            f0 = math.floor(self.t0)
            f1 = math.ceil(self.t1)
            for f in range(f0, f1 + 1):
                p = self.progress(f)
                v = 100 * max(0.0, min(1.0, (p - ua) / (ub - ua)))
                keys.append((f, v))
            # drop runs of repeated values, keeping the run edges
            ks = [k for i, k in enumerate(keys)
                  if i == 0 or i == len(keys) - 1 or not (keys[i - 1][1] == k[1] == keys[i + 1][1])]
            end = anim([(f, v, LINEAR) for f, v in ks]) if len(ks) > 1 else 100
            ip = f0
            for f, v in ks:
                if v > 0:
                    break
                ip = f
            matte = [group([path(bezier(seg, closed=False)), trim(0, end),
                            stroke("#FFFFFF", self.max_width + 6, cap="round")], "reveal")]
            content = [group([path(rib, "ribbon"), fill(self.color, self.opacity, slot=self.slot)]
                             + self.extra, "ink")]
            out.append((f"{self.name}-{c}", matte, content, ip))
        return out


def emit(comp, brushes, parent=None, **tr):
    """Add brushes to comp; later strokes are drawn on top. Returns nothing."""
    specs = [spec for b in brushes for spec in b.layers()]
    for name, matte, content, ip in reversed(specs):
        comp.layer(name + "-matte", matte, ip=ip, parent=parent, **tr)
        comp.layer(name, content, ip=ip, parent=parent, matte="alpha", **tr)


# ---------------------------------------------------------------- output

def _hex(rgba):
    return "#" + "".join(f"{round(c * 255):02X}" for c in rgba[:3])


def finish(comp, asset_id, name, description, tags, playback, text_area=None, thumb_t=0.99,
           bg=None):
    out = ROOT / "lottie" / CATEGORY / asset_id
    out.mkdir(parents=True, exist_ok=True)
    js = out / f"{asset_id}.json"
    comp.save(js)
    cmd = [str(RENDER), str(js), str(out / "thumbnail.png"), "--size", "512", "--t", str(thumb_t),
           "--strict"]
    if bg:
        cmd += ["--bg", bg]
    subprocess.run(cmd, check=True)
    meta = {
        "schema": 1, "id": asset_id, "name": name, "type": "lottie", "category": CATEGORY,
        "file": js.name, "thumbnail": "thumbnail.png", "license": "CC-BY-NC-SA-4.0",
        "description": description, "tags": tags, "width": comp.w, "height": comp.h,
        "fps": comp.fps, "duration": round(comp.frames / comp.fps, 3), "playback": playback,
        "slots": {k: _hex(v["p"]["k"]) for k, v in comp.slots.items()},
        "textArea": text_area,
    }
    (out / "asset.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(js)


def cubic_pts(p0, p1, p2, p3, n=48):
    """Sample a cubic bezier into n+1 points (use with Brush(..., smooth=False))."""
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def stamp(comp, symbol, seed, tilt):
    """Rubber-stamp motion shared by stamp-check / stamp-cross.

    symbol: shape items (drawn with slot "primary") centred on (0, 0) inside a ~300 px ring.
    The stamp drops from large, slams to slightly under size, settles at `tilt` degrees and throws
    out a faint shockwave. Ink texture comes from speckles used as an inverted alpha matte.
    """
    from lottie_kit import ANTICIPATE, ellipse  # noqa: F401
    cx, cy = comp.w / 2, comp.h / 2
    hit = 7
    DROP = (0.55, 0.0, 0.9, 0.6)  # accelerates into the page
    SETTLE = (0.2, 0.0, 0.3, 1.0)
    rnd = random.Random(seed)
    shake = [(0, [cx, cy], LINEAR), (hit, [cx, cy], LINEAR)]
    for k, f in enumerate(range(hit + 1, hit + 6)):
        a = 7 * (1 - k / 5)
        shake.append((f, [cx + rnd.uniform(-a, a), cy + rnd.uniform(-a, a)], LINEAR))
    shake.append((hit + 7, [cx, cy]))
    holder = comp.null("stamp", position=anim(shake),
                       scale=anim([(0, [148, 148], DROP), (hit, [90, 90], SETTLE),
                                   (hit + 4, [104, 104], SETTLE), (hit + 8, [100, 100])]),
                       rotation=anim([(0, tilt - 26, DROP), (hit, tilt + 3, SETTLE),
                                      (hit + 6, tilt)]))

    # speckles, denser around the ring edges so the ink looks chipped
    specks = []
    for i in range(120):
        if i < 70:
            a = rnd.uniform(0, 2 * math.pi)
            r = rnd.choice([160, 142, 132]) + rnd.uniform(-7, 7)
        else:
            a, r = rnd.uniform(0, 2 * math.pi), 125 * math.sqrt(rnd.random())
        s = rnd.uniform(2.5, 7) if rnd.random() < 0.85 else rnd.uniform(7, 10)
        specks.append(ellipse((s * rnd.uniform(0.7, 1.4), s), (r * math.cos(a), r * math.sin(a))))
    comp.layer("wear", [group(specks + [fill("#FFFFFF")], "specks")], parent=holder)
    comp.layer("stamp", [group(symbol, "symbol"),
                         group([ellipse((316, 316)), stroke(slot="primary", width=18)], "ring"),
                         group([ellipse((268, 268)), stroke(slot="primary", width=5)], "ring-inner")],
               parent=holder, matte="alpha_inverted",
               opacity=anim([(0, 0, (0.4, 0.0, 0.8, 1.0)), (hit - 2, 100)]))

    # shockwave where it hits the page
    comp.layer("shockwave", [group([ellipse(anim([(hit, [320, 320], SETTLE), (hit + 12, [470, 470])])),
                                    stroke(slot="primary", width=anim([(hit, 12, SETTLE),
                                                                       (hit + 12, 1)]))],
                                   "ring")],
               position=(cx, cy), ip=hit, op=hit + 12,
               opacity=anim([(hit, 55, SETTLE), (hit + 12, 0)]))
