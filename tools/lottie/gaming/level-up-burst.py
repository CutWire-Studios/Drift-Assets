import math
import random

from _common import *

W = H = 500
F = 45
comp = Comp("level-up-burst", W, H, fps=30, frames=F)
comp.slot("primary", "#FFC21A")
comp.slot("accent", "#FFF1A8")
comp.slot("outline", "#8A4B00")

C = (W / 2, H / 2)
rng = random.Random(7)
fade = lambda t0, t1: anim([(t0, 100, EASE_IN), (t1, 0)])

# rising sparkles
for i in range(16):
    x = C[0] + rng.uniform(-150, 150)
    y = C[1] + rng.uniform(-10, 110)
    t = rng.randint(4, 14)
    life = rng.randint(18, 26)
    rise = rng.uniform(90, 170)
    s = rng.uniform(9, 17)
    shape = star(4, s, s * 0.3) if i % 3 else ellipse((s * 0.8, s * 0.8))
    comp.layer(f"sparkle {i}", [group([shape, fill(slot="accent" if i % 2 else "primary")], "p")],
               ip=t, op=min(F, t + life),
               position=anim([(t, [x, y], EASE_OUT), (t + life, [x + rng.uniform(-20, 20), y - rise])]),
               scale=anim([(t, [0, 0], OVERSHOOT), (t + 5, [100, 100], EASE_IN), (t + life, [20, 20])]),
               rotation=anim([(t, 0, LINEAR), (t + life, rng.choice((-1, 1)) * 120)]))

# arrow with trailing chevrons
arrow = "M 0 -78 L 62 -14 L 26 -14 L 26 58 L -26 58 L -26 -14 L -62 -14 Z"
comp.layer("arrow", [
    group([*svg_shapes("M 0 -64 L 44 -20 L 14 -20 L 14 46 L 0 46 Z"), fill("#FFFFFF", opacity=35)], "shine"),
    group([*svg_shapes(arrow), fill(slot="primary")], "arrow"),
    group([*svg_shapes(arrow), stroke(slot="outline", width=10, join="miter")], "outline"),
], position=anim([(3, [C[0], C[1] + 70], SNAP_OUT), (16, [C[0], C[1] - 4], EASE_IN_OUT),
                  (32, [C[0], C[1] - 14], EASE_IN), (F - 1, [C[0], C[1] - 70])]),
    scale=anim([(3, [30, 30], OVERSHOOT), (14, [100, 100], EASE_IN_OUT), (32, [104, 104], EASE_IN),
                (F - 1, [80, 80])]),
    opacity=anim([(3, 0, EASE_OUT), (6, 100, HOLD), (32, 100, EASE_IN), (F - 1, 0)]))
for j, dy in enumerate((82, 122)):
    t = 7 + j * 3
    comp.layer(f"chevron {j}", [group([polyline([(-38, 20), (0, -18), (38, 20)]),
                                       stroke(slot="primary", width=14, cap="butt", join="miter")], "c")],
               ip=t,
               position=anim([(t, [C[0], C[1] + dy + 30], SNAP_OUT), (t + 12, [C[0], C[1] + dy - 10], EASE_IN),
                              (F - 1, [C[0], C[1] + dy - 50])]),
               opacity=anim([(t, 0, EASE_OUT), (t + 4, 80 - j * 25, EASE_IN), (F - 12 + j * 3, 0)]))

# central flash
comp.layer("flash", [group([ellipse((240, 240)),
                            gradient_fill([(0, "#FFFFFF", 1), (0.3, "#FFFBE6", 0.9), (0.6, "#FFE27A", 0.35), (1, "#FFD23F", 0)],
                                          (0, 0), (120, 0), radial=True)], "glow")],
           position=C, scale=anim([(0, [30, 30], SNAP_OUT), (6, [110, 110], EASE_OUT), (16, [130, 130])]),
           opacity=anim([(0, 0, LINEAR), (2, 100, EASE_OUT), (16, 0)]))

# shockwave rings
for k, (t, d0, d1, w, slot) in enumerate(((2, 80, 440, 16, "primary"), (6, 60, 360, 6, "accent"))):
    comp.layer(f"ring {k}", [group([ellipse(anim([(t, [d0, d0], SNAP_OUT), (t + 20, [d1, d1])])),
                                    stroke(slot=slot, width=anim([(t, w, EASE_OUT), (t + 20, 1)]))], "ring")],
               ip=t, op=t + 21, position=C, opacity=anim([(t, 100, EASE_IN), (t + 20, 0)]))

# light rays
ray = lambda L, w: polyline([(0, -24), (-w, -L), (w, -L)], closed=True)
rays = []
for i in range(12):
    L = 230 if i % 2 == 0 else 170
    w = 18 if i % 2 == 0 else 11
    rays.append(group([ray(L, w)], f"ray {i}", rotation=i * 30))
ray_scale = anim([(0, [0, 0], SNAP_OUT), (12, [100, 100], EASE_OUT), (F - 1, [112, 112])])
comp.layer("rays falloff", [group([ellipse((480, 480)),
                                   gradient_fill([(0, "#FFFFFF", 1), (0.35, "#FFFFFF", 1), (1, "#FFFFFF", 0)],
                                                 (0, 0), (240, 0), radial=True)], "falloff")],
           position=C, scale=ray_scale)
comp.layer("rays", [group(rays + [fill(slot="primary", opacity=70)], "rays")], matte="alpha",
           position=C, scale=ray_scale,
           rotation=anim([(0, -12, EASE_OUT), (F - 1, 18)]),
           opacity=anim([(0, 0, LINEAR), (2, 100, HOLD), (12, 100, EASE_IN_OUT), (34, 0)]))

finish(comp, "level-up-burst", "Level Up Burst",
       "Gold level-up burst: light rays, a shockwave ring and rising sparkles around an upward arrow. "
       "One-shot (1.5 s) that ends empty.",
       ["level up", "levelup", "burst", "arrow", "upgrade", "gaming", "reward"], "intro-hold",
       thumb_t=0.33)
