import math
import random
from _common import *

W, H = 1000, 290
PAINT = (0.45, 0.0, 0.15, 1.0)


def smooth(pts, closed=True, k=0.18):
    """Catmull-Rom style tangents so the ragged outline stays soft."""
    n = len(pts)
    it, ot = [], []
    for i in range(n):
        if not closed and (i == 0 or i == n - 1):
            it.append((0, 0)); ot.append((0, 0)); continue
        a, b = pts[i - 1], pts[(i + 1) % n]
        tx, ty = (b[0] - a[0]) * k, (b[1] - a[1]) * k
        it.append((-tx, -ty)); ot.append((tx, ty))
    return bezier(pts, it, ot, closed)


def brush(rng, x0, x1, cy, half, fingers, bend=8, step=11):
    """Filled brush-stroke outline: rounded blobby start, ragged edges, dry-brush split tail."""
    def mid(x):
        u = (x - x0) / (x1 - x0)
        return cy - bend * math.sin(u * math.pi) + 3 * math.sin(u * 7.3)

    def thick(x):
        u = (x - x0) / (x1 - x0)
        return half * (0.9 + 0.1 * math.sin(u * math.pi)) * (1 - 0.08 * u)

    n = int((x1 - x0) / step)
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    top = [(x, mid(x) - thick(x) + rng.uniform(-1.6, 1.6) + 1.4 * math.sin(x * 0.045)) for x in xs]
    bot = [(x, mid(x) + thick(x) + rng.uniform(-1.6, 1.6) + 1.4 * math.sin(x * 0.051 + 1)) for x in xs]

    # dry-brush tail: fingers from top to bottom
    tail = []
    t_top, t_bot = top[-1][1], bot[-1][1]
    for f in range(fingers):
        ya = t_top + (t_bot - t_top) * f / fingers
        yb = t_top + (t_bot - t_top) * (f + 1) / fingers
        tip = x1 + rng.uniform(15, 75)
        if f > 0:
            tail.append((x1 - rng.uniform(4, 22), ya))
        tail.append((tip, (ya + yb) / 2 + rng.uniform(-3, 3)))
    # blobby rounded start
    head = []
    ym, r = (top[0][1] + bot[0][1]) / 2, (bot[0][1] - top[0][1]) / 2
    for i in range(1, 9):
        a = math.pi / 2 + math.pi * i / 9
        rr = r * (1 + rng.uniform(-0.05, 0.05))
        head.append((x0 + math.cos(a) * rr * 0.55, ym + math.sin(a) * rr))
    pts = top + tail + bot[::-1] + head
    return pts


def holes(rng, x_from, x_to, cy, half, count):
    out = []
    for j in range(count):
        x = rng.uniform(x_from, x_to)
        y = cy - half * 0.7 + 1.4 * half * (j + 0.5) / count + rng.uniform(-2, 2)
        L, T = rng.uniform(40, 90), rng.uniform(1.5, 3.2)
        out.append(bezier([(x - L / 2, y), (x, y - T), (x + L / 2, y), (x, y + T)],
                          [(0, 0), (-L / 4, 0), (0, 0), (L / 4, 0)],
                          [(0, 0), (L / 4, 0), (0, 0), (-L / 4, 0)]))
    return out


comp = Comp("title-brush-stroke", W, H, fps=FPS, frames=FRAMES)
comp.slot("primary", "#FF4D6D")
comp.slot("accent", "#FFC43D")

rng = random.Random(11)
MAIN = dict(x0=90, x1=860, cy=118, half=64)
SUB = dict(x0=360, x1=850, cy=236, half=24)

main_shapes = [path(smooth(brush(rng, fingers=7, bend=10, **MAIN)), "body")]
main_shapes += [path(h, f"hole{i}") for i, h in enumerate(holes(rng, 700, 780, MAIN["cy"], MAIN["half"], 5))]
for i, (dx, dy, s) in enumerate(((962, 78, 9), (946, 150, 6), (980, 120, 5))):
    main_shapes.append(ellipse((s * 2, s * 2), (dx, dy), name=f"drop{i}"))

sub_shapes = [path(smooth(brush(rng, fingers=4, bend=4, **SUB)), "body")]
sub_shapes += [path(h, f"hole{i}") for i, h in enumerate(holes(rng, 770, 800, SUB["cy"], SUB["half"], 2))]


def painted(name, shapes, slot, cy, width, x_from, x_to, t0, t1, t2, t3, rot):
    wob = [(x_from, cy + 14), ((x_from + x_to) / 2, cy - 10), (x_to, cy + 6)]
    comp.layer(f"{name}-matte", [
        path(smooth(wob, closed=False, k=0.25)),
        stroke("#FFFFFF", width=width, cap="round"),
        trim(start=keys((0, 0, HOLD), (t2, 0, (0.5, 0, 0.75, 0.6)), (t3, 100)),
             end=keys((t0, 0, PAINT), (t1, 100))),
    ], anchor=(W / 2, cy), position=(W / 2, cy), rotation=rot)
    comp.layer(name, [group(shapes + [fill(slot=slot, even_odd=True)])], matte="alpha",
               anchor=(W / 2, cy), position=(W / 2, cy), rotation=rot)


painted("sub", sub_shapes, "accent", SUB["cy"], 90, 250, 990, 12, 32, 118, 136, -1.2)
painted("main", main_shapes, "primary", MAIN["cy"], 200, -60, 1060, 0, 26, 122, 142, -1.5)

build(comp, "title-brush-stroke", "Brush Stroke Title",
      "Painterly brush-stroke title plate that paints on left to right, with a smaller accent stroke for a subtitle.",
      ["title", "brush", "paint", "vlog", "handmade", "stroke", "lower third"],
      {"title": [150, 72, 530, 92], "subtitle": [400, 220, 360, 34]},
      thumb_t=0.5, intro_end=32)
