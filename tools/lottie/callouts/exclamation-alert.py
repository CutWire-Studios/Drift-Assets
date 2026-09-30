import math

from _common import (LINEAR, Comp, anim, bezier, ellipse, fill, group, path, stroke,
                     trim)
import _callouts2 as c2
from drift_lottie import Variant, build_asset

W, H = 380, 480
CX, BASE = W / 2, 408


def bold():
    comp = Comp("exclamation-alert", W, H, fps=30, frames=30)
    comp.slot("primary", "#FF2D2D")
    comp.slot("outline", "#141414")

    cx = W / 2
    base_y = 408  # bottom of the dot: the glyph pops up and pivots from here


    def bar():
        """Tapered bar of the '!', rounded at both ends, relative to (cx, base_y)."""
        top, bot, wt, wb = -292, -112, 44, 26
        k = 0.55
        v = [(-wt, top + 8), (0, top - 24), (wt, top + 8), (wb, bot), (0, bot + 20), (-wb, bot)]
        i = [(0, 16), (-wt * k * 1.3, 0), (0, -16), (0, 0), (wb * k * 1.3, 0), (0, 0)]
        o = [(0, -16), (wt * k * 1.3, 0), (0, 16), (0, 0), (-wb * k * 1.3, 0), (0, 0)]
        return bezier(v, i, o)


    def shine():
        """Soft highlight stripe on the left of the bar."""
        v = [(-28, -280), (-14, -300), (-15, -150), (-22, -150)]
        return bezier(v, [(0, 8), (-6, 0), (0, 0), (0, 0)], [(0, -8), (0, 0), (0, 0), (0, 0)])


    glyph = [
        group([path(bar(), "bar"), stroke(slot="outline", width=9), fill(slot="primary")], "bar"),
        group([path(shine(), "shine"), fill("#FFFFFF", 38)], "shine"),
        group([ellipse((70, 70), (0, -40)), stroke(slot="outline", width=9), fill(slot="primary")],
              "dot"),
        group([ellipse((20, 13)), fill("#FFFFFF", 38)], "dot-shine", position=(-13, -53), rotation=-35),
    ]
    glyph = [glyph[1], glyph[0], glyph[3], glyph[2]]  # shine above its shape

    S = (0.2, 0.0, 0.3, 1.0)
    scale = anim([(0, [0, 0], S), (4, [110, 116], S), (7, [106, 90], S), (10, [96, 104], S),
                  (13, [100, 100])])
    pos = anim([(0, [cx, base_y + 40], S), (4, [cx, base_y - 14], S), (8, [cx, base_y + 4], S),
                (11, [cx, base_y])])
    rot_keys = [(0, 0, LINEAR)]
    for n, f in enumerate(range(6, 21, 2)):
        amp = 11 * (1 - n / 8) ** 1.5
        rot_keys.append((f, amp if n % 2 == 0 else -amp, (0.4, 0.0, 0.6, 1.0)))
    rot_keys.append((22, 0))
    comp.layer("glyph", glyph, anchor=(0, 0), position=pos, scale=scale, rotation=anim(rot_keys))

    # alert lines bursting out around the top of the mark
    lines = []
    for side in (-1, 1):
        for j, (ang, r0, r1) in enumerate([(-28, 110, 150), (-58, 118, 166)]):
            a = math.radians(-90 + side * (90 + ang))
            c = (cx, base_y - 236)
            p0 = (c[0] + r0 * math.cos(a), c[1] + r0 * math.sin(a))
            p1 = (c[0] + r1 * math.cos(a), c[1] + r1 * math.sin(a))
            d = 5 + j
            lines.append(group([path(bezier([p0, p1], closed=False), "line"),
                                trim(0, anim([(d, 0, S), (d + 5, 100)])),
                                stroke(slot="primary", width=11)], f"line-{side}-{j}"))
    # a centre line straight up above the mark
    top = (cx, base_y - 236)
    lines.append(group([path(bezier([(top[0], top[1] - 112), (top[0], top[1] - 150)], closed=False)),
                        trim(0, anim([(6, 0, S), (11, 100)])), stroke(slot="primary", width=11)],
                       "line-top"))
    comp.layer("alert-lines", lines, ip=5)
    return comp


def bar_outline(top=-272, bot=-128, rt=40, rb=22):
    """Tapered '!' bar outline (clockwise from the top), relative to the dot's baseline."""
    pts = c2.arc((0, top), rt, rt, 180, 360, 24)
    pts += c2.arc((0, bot), rb, rb, 0, 180, 16)
    return c2.dense(pts + [pts[0]])


def ray_lines(r0=112, r1=150):
    """Alert lines fanning out above the mark (point pairs, relative to the top of the mark)."""
    out = []
    for side in (-1, 1):
        for ang, a0, a1 in [(-28, r0, r1 + 4), (-58, r0 + 6, r1 + 14)]:
            a = math.radians(-90 + side * (90 + ang))
            out.append([(a0 * math.cos(a), a0 * math.sin(a)), (a1 * math.cos(a), a1 * math.sin(a))])
    out.append([(0, -r0), (0, -r1 - 4)])
    return out


def hand():
    """Marker '!' drawn in two quick strokes, then scribbled alert lines; a little wobble to finish."""
    comp = Comp("exclamation-alert--hand", W, H, fps=30, frames=30)
    comp.slot("primary", "#FF2D2D")
    holder = comp.null("mark", position=(CX, BASE), anchor=(0, 0),
                       rotation=anim([(10, 0, c2.SETTLE), (13, -6, c2.SETTLE), (17, 4, c2.SETTLE), (21, -2, c2.SETTLE),
                                      (25, 0)]))
    bar = c2.dense([(-6, -300), (-2, -220), (2, -132)], smooth=True)
    # the dot is a tight marker spiral that fills itself in
    dot = [(-2 + r * math.cos(a), -40 + r * math.sin(a))
           for r, a in ((24 * (1 - i / 60) + 2, math.radians(-120 + i * 13)) for i in range(61))]
    brushes = [
        c2.hand_line(bar, 1, 8, 60, seed=4, taper=(0.03, 0.9), mins=(0.8, 0.5), wob=0.03, name="bar"),
        c2.hand_line(c2.dense(dot, 2.0), 8, 12, 26, seed=6, taper=(0.1, 0.1), mins=(0.8, 0.8), wob=0.03,
                     name="dot"),
    ]
    top = (0, -236)
    for k, (p0, p1) in enumerate(ray_lines()):
        t = 10 + (k % 3)
        seg = c2.dense([(p0[0] + top[0], p0[1] + top[1]), (p1[0] + top[0], p1[1] + top[1])])
        brushes.append(c2.hand_line(seg, t, t + 4, 13, seed=10 + k, taper=(0.1, 0.3), mins=(0.75, 0.5), wob=0.04,
                                    name=f"ray{k}"))
    c2.emit(comp, brushes, parent=holder)
    return comp


def neon():
    """Neon-sign '!' that flickers on, with glowing alert lines buzzing around it."""
    comp = Comp("exclamation-alert--neon", W, H, fps=30, frames=30)
    comp.slot("primary", "#FF2D55")
    buzz = anim([(8, [100, 100], c2.SETTLE), (10, [104, 104], c2.SETTLE), (14, [100, 100])])
    top = (0, -236)
    rays = [c2.neon_line([(p0[0] + top[0], p0[1] + top[1]), (p1[0] + top[0], p1[1] + top[1])], 8, t0=9, t1=14,
                         ease=c2.SETTLE, name=f"ray{k}") for k, (p0, p1) in enumerate(ray_lines(116, 150))]
    comp.layer("rays", rays, position=(CX, BASE), ip=9, opacity=c2.flicker(9))
    comp.layer("mark", [c2.neon_line(bar_outline(), 10, t0=1, t1=10, closed=False, name="bar"),
                        c2.neon_line(c2.ellipse_pts((0, -40), 34, 34, start=-90), 10, t0=4, t1=11, name="dot")],
               position=(CX, BASE), anchor=(0, 0), scale=buzz, opacity=c2.flicker(1))
    return comp


build_asset("callouts", "exclamation-alert", "Exclamation Alert",
            "Exclamation mark that pops up with alert lines, stealth-game style, for surprises and "
            "warnings.",
            ["exclamation", "alert", "surprise", "warning", "attention", "reaction"], [
    Variant("bold", "Glossy Bold", bold(), "intro-hold", thumb_t=0.99,
            description="Red exclamation mark that pops up and shakes with alert lines, stealth-game style."),
    Variant("hand", "Hand-Drawn", hand(), "intro-hold", thumb_t=0.99,
            description="Marker exclamation mark drawn in two quick strokes with scribbled alert lines."),
    Variant("neon", "Neon", neon(), "intro-hold", thumb_t=0.99,
            description="Neon-sign outline exclamation mark that flickers on with glowing alert lines."),
])
