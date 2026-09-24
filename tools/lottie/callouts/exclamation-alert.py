import math

from _common import (LINEAR, Comp, anim, bezier, ellipse, fill, finish, group, path, stroke,
                     trim)

W, H = 380, 480
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

finish(comp, "exclamation-alert", "Exclamation Alert",
       "Red exclamation mark that pops up and shakes with alert lines, stealth-game style.",
       ["exclamation", "alert", "surprise", "warning", "attention", "reaction"], "intro-hold")
