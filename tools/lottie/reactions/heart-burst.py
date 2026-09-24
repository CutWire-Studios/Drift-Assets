"""Hearts float up with a wobble, pop in and fade out, staggered so the loop is never empty."""

import math
import random

from _common import *

T = 60
W, H = 400, 560
PINK, LIGHT = "#FF3B6B", "#FF8FB1"

comp = Comp("heart-burst", W, H, fps=30, frames=T)
comp.slot("primary", PINK)
comp.slot("secondary", LIGHT)

HEART_D = ("M 0 38 C -30 20 -54 0 -54 -20 C -54 -39 -40 -51 -25 -51 C -13 -51 -4 -44 0 -33 "
           "C 4 -44 13 -51 25 -51 C 40 -51 54 -39 54 -20 C 54 0 30 20 0 38 Z")


def heart(color, sid):
    return [
        group([ellipse((10, 10)), fill("#FFFFFF", 80)], name="glint2", position=(-14, -38)),
        group([ellipse((24, 14)), fill("#FFFFFF", 80)], name="glint", position=(-33, -24),
              rotation=-50),
        group(svg_shapes("M 54 -20 C 54 0 30 20 0 38 C 10 22 40 4 46 -20 C 48 -30 46 -40 40 -46 "
                         "C 48 -41 54 -32 54 -20 Z") + [fill("#000000", 12)], name="shade"),
        group(svg_shapes(HEART_D) + [fill(color, slot=sid)], name="heart"),
    ]


rng = random.Random(7)
N, LIFE = 9, 52
xs = [200, 290, 115, 245, 160, 300, 100, 225, 150]
for i in range(N):
    t0 = i * T / N
    x0 = xs[i] + rng.uniform(-10, 10)
    size = rng.uniform(0.6, 0.95) if i % 3 else 1.1
    amp = rng.uniform(16, 28) * (1 if i % 2 else -1)
    wob = rng.uniform(0.9, 1.3)
    rise = rng.uniform(390, 440)
    y0 = 500

    def fn(u, x0=x0, size=size, amp=amp, wob=wob, rise=rise):
        k = u / LIFE
        w = math.sin(2 * math.pi * wob * k)
        y = y0 - rise * (1 - (1 - k) ** 1.3)
        if u < 5:
            s = size * 1.18 * (u / 5) ** 0.7
        elif u < 11:
            s = size * (1.18 - 0.18 * (1 - math.cos(math.pi * (u - 5) / 6)) / 2)
        else:
            s = size * (1 - 0.25 * (u - 11) / (LIFE - 11))
        stretch = 1 + 0.06 * math.cos(2 * math.pi * wob * k * 2)
        return {"position": (x0 + amp * w, y),
                "rotation": -14 * math.cos(2 * math.pi * wob * k) * (1 if amp > 0 else -1),
                "scale": (100 * s / stretch, 100 * s * stretch),
                "opacity": 100 if u < LIFE - 14 else 100 * ((LIFE - u) / 14) ** 1.3}

    col, sid = (PINK, "primary") if i % 3 != 1 else (LIGHT, "secondary")
    particle(comp, f"heart{i}", heart(col, sid), round(t0, 2), LIFE, T, fn, step=2)

build(comp, "reactions", "heart-burst", "Heart Burst",
      "Hearts float up with a gentle wobble, pop in and fade out; staggered so it is never empty. "
      "Seamless loop.",
      ["heart", "love", "like", "hearts", "reaction", "valentine"],
      "loop", 0.5)
