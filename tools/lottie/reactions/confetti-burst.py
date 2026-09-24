"""Confetti cannon: a pop from the bottom, pieces tumble up, arc over with drag and flutter down."""

import math
import random

from _common import *

T = 75
W, H = 800, 700
OX, OY = 400, 650
COLORS = [("primary", "#FF4D6D"), ("secondary", "#FFC93C"), ("accent", "#2EC4B6")]

comp = Comp("confetti-burst", W, H, fps=30, frames=T)
for sid, c in COLORS:
    comp.slot(sid, c)

rng = random.Random(11)


def simulate(angle, speed, drag, g, t_end, sway, sway_ph):
    x, y = OX, OY
    vx, vy = speed * math.sin(angle), -speed * math.cos(angle)
    pts = [(x, y)]
    for u in range(1, t_end + 1):
        vx *= drag
        vy = vy * drag + g
        x += vx
        y += vy
        falling = max(0.0, min(1.0, vy / 3))
        pts.append((x + falling * sway * math.sin(sway_ph + u * 0.22), y))
    return pts


pieces = []
for i in range(66):
    angle = math.radians(rng.gauss(0, 24))
    speed = rng.uniform(42, 80) * (1 - 0.2 * abs(angle) / 0.9)
    pieces.append((i, angle, speed))

# fast/central pieces first in the list so they draw on top
for i, angle, speed in pieces:
    sid, col = COLORS[i % 3]
    launch = rng.uniform(0, 4)
    die = rng.uniform(62, 75)
    life = int(die - launch)
    drag = rng.uniform(0.895, 0.91)
    pts = simulate(angle, speed, drag, 0.8, life + 1, rng.uniform(10, 26), rng.uniform(0, 6.28))
    spin0 = rng.uniform(10, 24) * rng.choice((-1, 1))
    rot0 = rng.uniform(0, 360)
    flip_w = rng.uniform(0.18, 0.4)
    flip_ph = rng.uniform(0, 6.28)
    kind = rng.random()
    if kind < 0.6:
        w, h = rng.uniform(16, 20), rng.uniform(26, 34)
        shape = rect((w, h), roundness=2)
    elif kind < 0.85:
        d = rng.uniform(16, 22)
        shape = ellipse((d, d))
    else:
        w, h = rng.uniform(9, 11), rng.uniform(40, 52)
        shape = rect((w, h), roundness=3)
    size = rng.uniform(0.85, 1.15)

    def fn(u, pts=pts, spin0=spin0, rot0=rot0, flip_w=flip_w, flip_ph=flip_ph, size=size,
           life=life):
        k = min(int(u), len(pts) - 2)
        f = u - k
        x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f
        y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
        rot = rot0 + spin0 * (1 - math.exp(-u / 14)) * 14 + 4 * u * (1 if spin0 > 0 else -1)
        flip = math.cos(flip_ph + flip_w * u)
        grow = min(1, 0.3 + u / 3)
        s = 100 * size * grow
        return {"position": (x, y), "rotation": rot,
                "scale": (s * (0.3 + 0.7 * abs(flip)) * (1 if flip >= 0 else -1), s),
                "opacity": 100 if u < life - 14 else 100 * max(0.0, (life - u) / 14)}

    particle(comp, f"piece{i}", [shape, fill(col, slot=sid)], round(launch, 2), life, T, fn,
             step=3, wrap=False)

# muzzle pop: short streaks shooting out of the cannon mouth
streaks = []
for a in (-52, -26, 0, 26, 52):
    r = math.radians(a)
    dx, dy = math.sin(r), -math.cos(r)
    streaks.append(group([path(bezier([(dx * 40, dy * 40), (dx * 120, dy * 120)], closed=False)),
                          trim(start=anim([(0, 0, EASE_IN), (10, 100)]),
                               end=anim([(0, 0, SNAP_OUT), (7, 100)])),
                          stroke("#FFC93C", 9, slot="secondary")], name=f"streak{a}"))
comp.layer("pop", streaks, op=12, position=(OX, OY))

build(comp, "reactions", "confetti-burst", "Confetti Burst",
      "One-shot confetti cannon: rectangles, dots and strips burst upward, tumble over with "
      "gravity and flutter down while fading out; ends empty.",
      ["confetti", "party", "celebration", "burst", "congrats", "reaction"],
      "intro-hold", 0.33)
