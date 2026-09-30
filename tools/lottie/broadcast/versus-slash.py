import math
import random

from _broadcast2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 60
HIT = 10  # halves meet
SLAM = (0.55, 0.0, 0.9, 0.6)  # accelerating into the impact


def shake(comp, t=HIT, amp=26):
    ks = [(0, [0, 0], HOLD), (t, [0, 0], HOLD)]
    rng = random.Random(1)
    a = amp
    for i in range(1, 8):
        ks.append((t + i * 1.5, [rng.uniform(-a, a), rng.uniform(-a, a)], LINEAR))
        a *= 0.72
    ks.append((t + 13, [0, 0], HOLD))
    ks.append((F, [0, 0]))
    return rig(comp, "camera", C, off=Anim(ks), scale=keys((t, [104, 104], EXPO_OUT), (t + 14, [100, 100])))


def bolt_pts(p0, p1, n=11, jit=46, seed=3):
    rng = random.Random(seed)
    pts = []
    for i in range(n + 1):
        u = i / n
        x, y = p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u
        if 0 < i < n:
            x += rng.uniform(-jit, jit) * (1 if i % 2 else -1)
        pts.append((x, y))
    return pts


def bolt(comp, pts, slot, parent, t=HIT, width=9):
    ln = polyline(pts)
    tr = [trim(end=keys((t - 1, 0, EXPO_OUT), (t + 4, 100)))]
    flick = keys((0, 0, HOLD), (t - 1, 100, HOLD), (t + 6, 40, HOLD), (t + 8, 100, HOLD), (t + 12, 55, HOLD),
                 (t + 14, 100, HOLD), (t + 24, 70, HOLD), (t + 26, 100, HOLD), (F, 100))
    comp.layer("bolt", glow_strokes([ln], slot=slot, width=width, widths=(40, 22, 12), ops=(10, 18, 34), extra=tr,
                                    cap="round"), parent=parent, opacity=flick, ip=t - 1)
    # side branches
    rng = random.Random(9)
    br = []
    for i in (3, 6, 8):
        p = pts[i]
        d = 1 if i % 2 else -1
        q = (p[0] + d * rng.uniform(70, 120), p[1] + rng.uniform(40, 80))
        r = (q[0] + d * rng.uniform(30, 60), q[1] + rng.uniform(30, 60))
        br.append(polyline([p, q, r]))
    comp.layer("branches", glow_strokes(br, slot=slot, width=width * 0.5, widths=(24, 12), ops=(12, 24),
                                        extra=[trim(end=keys((t + 2, 0, EXPO_OUT), (t + 7, 100)))]),
               parent=parent, ip=t + 2, opacity=keys((t + 2, 100, HOLD), (t + 9, 0, HOLD), (t + 12, 100, HOLD),
                                                        (t + 14, 0, HOLD), (t + 24, 100, HOLD), (F, 100)))


def seam_flash(comp, pts, parent, t=HIT):
    comp.layer("seam flash", [group([polyline(pts), stroke("#FFFFFF", width=260, opacity=60)], "wide"),
                              group([polyline(pts), stroke("#FFFFFF", width=90)], "core")],
               parent=parent, ip=t, op=t + 9, opacity=keys((t, 100, EASE_OUT), (t + 8, 0)))
    comp.layer("screen flash", [box(0, 0, W, H, "#FFFFFF")], ip=t, op=t + 5,
               opacity=keys((t, 55, EASE_OUT), (t + 4, 0)))


def stripes(poly_pts, color="#000000", op=10, step=60, angle=-30):
    """Diagonal stripes clipped visually by being drawn inside the half (caller uses a matte)."""
    lines = [polyline([(-400 + i * step, -200), (-400 + i * step + 800 * math.tan(math.radians(angle)), H + 200)])
             for i in range(int((W + 800) / step))]
    return group(lines + [stroke(color, width=step * 0.35, opacity=op, cap="butt")], "stripes")


def half(comp, name, pts, slot, off, parent, texture=None):
    shp = polyline(pts, closed=True)
    if texture:
        comp.layer(f"{name} tex matte", [group([shp, fill("#FFFFFF")], "m")], parent=parent, position=off)
        comp.layer(f"{name} tex", [texture], parent=parent, position=off, matte="alpha")
    comp.layer(f"{name} shade", [group([shp, gradient_fill([(0, "#000000", 0), (1, "#000000", 0.35)],
                                                         (C[0], 0), (C[0], H))], "shade")], parent=parent, position=off)
    comp.layer(name, [group([shp, fill(slot=slot)], "fill")], parent=parent, position=off)


def diagonal():
    """Two colour halves slam in from the sides along a diagonal seam; a lightning slash cracks down it."""
    comp = Comp("versus-slash", W, H, fps=30, frames=F)
    comp.slot("primary", "#1E6BFF")
    comp.slot("secondary", "#FF2E3E")
    comp.slot("accent", "#FFE45C")
    cam = shake(comp)
    top, bot = (C[0] + 170, -40), (C[0] - 170, H + 40)
    pts = bolt_pts(top, bot)
    seam_flash(comp, [top, bot], cam)
    bolt(comp, pts, "accent", cam, width=14)
    L = [(-300, -60), (top[0], -60), (bot[0], H + 60), (-300, H + 60)]
    R = [(top[0], -60), (W + 300, -60), (W + 300, H + 60), (bot[0], H + 60)]
    half(comp, "left", L, "primary", keys((0, [-W, 0], SLAM), (HIT, [0, 0])), cam, stripes(L))
    half(comp, "right", R, "secondary", keys((0, [W, 0], SLAM), (HIT, [0, 0])), cam, stripes(R))
    return comp


def vertical():
    """Halves drop in from above and below on a straight seam; a jagged bolt splits them."""
    comp = Comp("versus-slash--vertical", W, H, fps=30, frames=F)
    comp.slot("primary", "#7A2BFF")
    comp.slot("secondary", "#FF8A00")
    comp.slot("accent", "#FFFFFF")
    cam = shake(comp, amp=20)
    top, bot = (C[0], -40), (C[0], H + 40)
    pts = bolt_pts(top, bot, n=14, jit=38, seed=11)
    seam_flash(comp, [top, bot], cam)
    bolt(comp, pts, "accent", cam, width=13)
    L = [(-300, -60), (C[0], -60), (C[0], H + 60), (-300, H + 60)]
    R = [(C[0], -60), (W + 300, -60), (W + 300, H + 60), (C[0], H + 60)]
    half(comp, "left", L, "primary", keys((0, [0, -H - 100], SLAM), (HIT, [0, 0])), cam)
    half(comp, "right", R, "secondary", keys((0, [0, H + 100], SLAM), (HIT, [0, 0])), cam)
    return comp


def comic():
    """Comic-book style: halftone halves with ink outlines slam together behind a jagged VS burst."""
    comp = Comp("versus-slash--comic", W, H, fps=30, frames=F)
    comp.slot("primary", "#00B4FF")
    comp.slot("secondary", "#FF3D7F")
    comp.slot("accent", "#FFE600")
    comp.slot("outline", "#111111")
    cam = shake(comp, amp=30)
    top, bot = (C[0] + 120, -40), (C[0] - 120, H + 40)
    # starburst badge
    n = 14
    rng = random.Random(6)
    burst = []
    for i in range(2 * n):
        a = math.radians(i * 180 / n - 90)
        r = (250 if i % 2 == 0 else 160) * rng.uniform(0.88, 1.08)
        burst.append((C[0] + math.cos(a) * r, C[1] + math.sin(a) * r))
    sc = keys((HIT + 2, [0, 0], SPRING), (HIT + 16, [100, 100]))
    comp.layer("burst", [group([polyline(burst, closed=True), fill(slot="accent")], "burst"),
                         group([polyline(burst, closed=True), stroke(slot="outline", width=14, join="miter")], "ink"),
                         group([polyline(burst, closed=True), fill(slot="outline")], "shadow", position=(14, 16))],
               parent=cam, anchor=C, position=C, scale=sc, rotation=keys((HIT + 2, -25, EXPO_OUT), (HIT + 16, -6)))
    # speed lines around the burst
    lines = []
    for i in range(20):
        a = math.radians(i * 18 + rng.uniform(-4, 4))
        r0, r1 = rng.uniform(290, 330), rng.uniform(420, 560)
        lines.append(group([polyline([(C[0] + math.cos(a) * r0, C[1] + math.sin(a) * r0),
                                      (C[0] + math.cos(a) * r1, C[1] + math.sin(a) * r1)]),
                            trim(start=keys((HIT + 4, 0, EASE_IN), (HIT + 16, 100)), end=keys((HIT + 2, 0, EXPO_OUT),
                                                                                            (HIT + 10, 100))),
                            stroke(slot="outline", width=10)], f"l{i}"))
    comp.layer("speed", lines, parent=cam, ip=HIT + 2, op=HIT + 17)
    comp.layer("seam", [group([polyline([top, bot]), stroke(slot="outline", width=26, cap="butt")], "ink")],
               parent=cam, opacity=keys((HIT - 1, 0, HOLD), (HIT, 100)))
    seam_flash(comp, [top, bot], cam)
    L = [(-300, -60), (top[0], -60), (bot[0], H + 60), (-300, H + 60)]
    R = [(top[0], -60), (W + 300, -60), (W + 300, H + 60), (bot[0], H + 60)]

    def dots(off_x):
        return group([ellipse((18, 18)), fill("#000000", 16),
                      repeater(46, position=(48, 0)),
                      repeater(26, position=(0, 44))], "halftone", position=(off_x - 150, -20))
    half(comp, "left", L, "primary", keys((0, [-W, 0], SLAM), (HIT, [0, 0])), cam, dots(0))
    half(comp, "right", R, "secondary", keys((0, [W, 0], SLAM), (HIT, [0, 0])), cam, dots(10))
    return comp, (C[0] - 150, C[1] - 90, 300, 180)


AREAS = {"vs": (C[0] - 130, C[1] - 90, 260, 180), "left": (140, H - 250, 600, 130),
         "right": (W - 740, H - 250, 600, 130)}
cm, ct = comic()
build_asset(CAT, "versus-slash", "Versus Slash",
            "Full-frame VS card: two colour halves slam together and a lightning slash cracks down the seam. "
            "Text areas for VS in the middle and a name on each side.",
            ["versus", "vs", "battle", "fight", "comparison", "lightning", "matchup", "gaming"], [
    V("diagonal", "Diagonal Slash", diagonal(), "intro-hold", text_area=AREAS["vs"], text_areas=AREAS,
      thumb_t=0.55, description="Striped colour halves slam in from the sides on a diagonal seam, split by a lightning bolt."),
    V("vertical", "Vertical Drop", vertical(), "intro-hold", text_area=AREAS["vs"], text_areas=AREAS,
      thumb_t=0.55, description="Halves drop in from above and below on a straight seam; a jagged white bolt splits them."),
    V("comic", "Comic", cm, "intro-hold", text_area=ct, text_areas={**AREAS, "vs": ct}, thumb_t=0.6,
      description="Comic-book halftone halves with an ink seam and a jagged yellow VS burst with speed lines."),
])
