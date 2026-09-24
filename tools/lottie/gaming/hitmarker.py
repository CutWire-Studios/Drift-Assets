import math

from _common import *

W = H = 200
F = 12
comp = Comp("hitmarker", W, H, fps=30, frames=F)
comp.slot("primary", "#FFFFFF")

c = W / 2
R0, R1 = 20, 52


def tick(angle):
    dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    seg = lambda a, b: polyline([(dx * a, dy * a), (dx * b, dy * b)])
    return group([group([seg(R0, R1), stroke(slot="primary", width=7, cap="butt")], "tick"),
                  group([seg(R0 - 2, R1 + 2), stroke("#000000", width=11, opacity=35, cap="butt")],
                        "shadow")], f"tick {angle}")


comp.layer("hitmarker", [tick(a) for a in (45, 135, 225, 315)],
           position=(c, c),
           scale=anim([(0, [155, 155], SNAP_OUT), (4, [100, 100], HOLD), (6, [100, 100], EASE_OUT),
                       (F - 1, [112, 112])]),
           opacity=anim([(0, 0, LINEAR), (1, 100, HOLD), (6, 100, EASE_IN), (F - 1, 0)]))

finish(comp, "hitmarker", "Hitmarker",
       "FPS-style hitmarker: four white diagonal ticks snap in with a scale punch and fade out. "
       "One-shot (0.4 s) that ends empty; stack copies on each hit.",
       ["hitmarker", "hit", "fps", "shooter", "crosshair", "gaming", "sfx"], "intro-hold",
       thumb_t=0.4, region=(40, 40, 120, 120))
