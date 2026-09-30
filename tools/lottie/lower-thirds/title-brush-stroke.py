import math
import random
from _common import *
from _lt2 import rrect, lay, fade, rect_grow, SPRING, BACK_IN
from drift_lottie import Variant, build_asset

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


def classic():
    """Ragged dry-brush strokes paint on left to right."""
    comp = Comp("title-brush-stroke", W, H, fps=FPS, frames=FRAMES)
    comp.slot("primary", "#FF4D6D")
    comp.slot("accent", "#FFC43D")
    comp.marker("intro", 0, 32)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)

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
    return comp


def marker_shape(rng, x0, x1, cy, h, chisel=22, step=40):
    """Highlighter swipe: chisel-cut ends, softly wavering long edges."""
    n = int((x1 - x0) / step)
    top = [(x0 + chisel + (x1 - x0 - chisel) * i / n, cy - h / 2 + rng.uniform(-1.5, 1.5)) for i in range(n + 1)]
    bot = [(x0 + (x1 - x0 - chisel) * i / n, cy + h / 2 + rng.uniform(-1.5, 1.5)) for i in range(n + 1)]
    return bezier(top + bot[::-1])


def swipe_matte(comp, name, x0, x1, cy, h, t0, t1, t2, t3, rot):
    """Rect matte that swipes in from the left and on out to the right."""
    w = x1 - x0 + 80
    comp.layer(f"{name}-matte", [rect((w, h + 40), (x0 - 40 + w / 2, cy)), fill("#FFFFFF")],
               anchor=(W / 2, cy),
               position=keys((0, [W / 2 - w, cy], HOLD), (t0, [W / 2 - w, cy], (0.6, 0, 0.2, 1)), (t1, [W / 2, cy], HOLD),
                             (t2, [W / 2, cy], (0.6, 0, 0.3, 1)), (t3, [W / 2 + w, cy])),
               rotation=rot)


def marker():
    """Two flat highlighter swipes: a fast chisel-tipped pass that swipes on and off left to right."""
    comp = Comp("title-brush-stroke--marker", W, H, fps=FPS, frames=FRAMES)
    comp.slot("primary", "#FF4D6D")
    comp.slot("accent", "#FFC43D")
    comp.marker("intro", 0, 26)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    rng = random.Random(4)
    for name, slot, x0, x1, cy, h, t0, t1, t2, t3, rot in (
            ("sub", "accent", 330, 870, 234, 46, 12, 26, 118, 132, -1.0),
            ("main", "primary", 70, 920, 120, 116, 2, 18, 122, 138, -2.0)):
        swipe_matte(comp, name, x0, x1, cy, h, t0, t1, t2, t3, rot)
        streaks = [group([polyline([(x0 + 40, cy + dy), (x1 - 40, cy + dy + rng.uniform(-2, 2))]),
                          stroke("#000000", width=wd, opacity=7, cap="round")], f"streak{i}")
                   for i, (dy, wd) in enumerate(((-h * 0.28, h * 0.08), (h * 0.18, h * 0.12)))]
        comp.layer(name, streaks + [group([path(marker_shape(rng, x0, x1, cy, h, chisel=h * 0.3)),
                                           fill(slot=slot, opacity=92)], "ink"),
                                    group([path(marker_shape(rng, x1 - h * 0.6, x1, cy, h, chisel=h * 0.3, step=20)),
                                           fill(slot=slot, opacity=40)], "overlap")],
                   matte="alpha", anchor=(W / 2, cy), position=(W / 2, cy), rotation=rot)
    return comp, {"title": [140, 80, 680, 84], "subtitle": [400, 218, 400, 32]}


def roller():
    """A thick rounded paint band rolls out from the left and paint drips run down from its edge."""
    comp = Comp("title-brush-stroke--roller", W, H, fps=FPS, frames=FRAMES)
    comp.slot("primary", "#FF4D6D")
    comp.slot("accent", "#FFC43D")
    comp.marker("intro", 0, 40)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    mx, my, mw, mh = 80, 48, 820, 112
    sx, sy, sw, sh = 110, 196, 470, 44
    # drips from the bottom edge of the main band (appear once the band has passed them)
    for i, (x, ln, wd) in enumerate(((640, 44, 16), (722, 26, 12), (786, 64, 18), (836, 30, 12))):
        t = 6 + int((x - mx) / mw * 20) + 4
        y0 = my + mh - 10
        grow = keys((0, [100, 0], HOLD), (t, [100, 0], (0.4, 0, 0.2, 1)), (t + 34, [100, 100], HOLD),
                    (120, [100, 100], EASE_IN), (134, [100, 0]))
        comp.layer(f"drip{i}", [rrect(x - wd / 2, y0, wd, ln, wd / 2), fill(slot="primary")],
                   anchor=(x, y0), position=(x, y0), scale=grow)
        comp.layer(f"bulb{i}", [ellipse((wd + 6, wd + 8), (x, y0 + ln - wd / 2)), fill(slot="primary")],
                   anchor=(x, y0), position=(x, y0), scale=grow,
                   opacity=keys((0, 0, HOLD), (t + 6, 0, EASE_OUT), (t + 12, 100, HOLD), (124, 100, EASE_IN), (132, 0)))
    comp.layer("sheen", [rect_grow(mx + 30, my + 16, mw - 60, 10, 5, 8, 30, 118, 138, "left", start=0),
                         fill("#FFFFFF", 26)])
    comp.layer("main", [rect_grow(mx, my, mw, mh, mh / 2, 2, 26, 122, 142, "left", start=mh,
                                  ein=(0.45, 0.0, 0.15, 1.0), eout=(0.6, 0, 0.8, 0.4)), fill(slot="primary")],
               opacity=keys((0, 0, HOLD), (2, 0, EASE_OUT), (5, 100, HOLD), (139, 100, EASE_IN), (142, 0)))
    comp.layer("sub", [rect_grow(sx, sy, sw, sh, sh / 2, 14, 36, 116, 134, "left", start=sh,
                                 ein=(0.45, 0.0, 0.15, 1.0), eout=(0.6, 0, 0.8, 0.4)), fill(slot="accent")],
               opacity=keys((0, 0, HOLD), (14, 0, EASE_OUT), (17, 100, HOLD), (131, 100, EASE_IN), (134, 0)))
    return comp, {"title": [mx + 60, my + 16, mw - 120, mh - 32], "subtitle": [sx + 30, sy + 6, sw - 60, sh - 12]}


mc, ma = marker()
rc, ra = roller()
AREAS = {"title": [150, 72, 530, 92], "subtitle": [400, 220, 360, 34]}
build_asset("lower-thirds", "title-brush-stroke", "Brush Stroke Title",
            "Hand-painted title plate that paints on left to right, with a smaller accent stroke for a subtitle.",
            ["title", "brush", "paint", "vlog", "handmade", "stroke", "lower third"], [
    Variant("classic", "Dry Brush", classic(), "intro-hold-outro", text_area=AREAS["title"], text_areas=AREAS,
            thumb_t=0.5,
            description="Painterly dry-brush stroke with a ragged split tail that paints on left to right, with a "
                        "smaller accent stroke for a subtitle."),
    Variant("marker", "Highlighter", mc, "intro-hold-outro", text_area=ma["title"], text_areas=ma, thumb_t=0.5,
            description="Flat chisel-tipped highlighter swipes that zip on from the left and off to the right."),
    Variant("roller", "Paint Roller", rc, "intro-hold-outro", text_area=ra["title"], text_areas=ra, thumb_t=0.5,
            description="Thick rounded paint bands roll out from the left and paint drips run down from the "
                        "edge."),
])
