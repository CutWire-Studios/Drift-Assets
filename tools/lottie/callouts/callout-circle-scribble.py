import math

from _common import Brush, Comp, emit, finish, jitter, pressure

W, H = 640, 440
comp = Comp("callout-circle-scribble", W, H, fps=30, frames=36)
comp.slot("primary", "#FF2D2D")

cx, cy, rx, ry = W / 2, H / 2, 270, 172
tilt = math.radians(-5)
turns = 1.17
start = math.radians(-58)  # upper right, drawn counter-clockwise on screen
pts = []
N = 16
for i in range(N + 1):
    u = i / N
    a = start - u * turns * 2 * math.pi
    # radius drifts outward over the loop so the overshoot passes just outside the start
    k = 0.93 + 0.1 * u + 0.05 * max(0, u - 0.85) / 0.15 + 0.015 * math.sin(2.0 * a + 0.7) + 0.035 * math.cos(a - 2.3)
    x, y = rx * k * math.cos(a), ry * k * math.sin(a) * (1 + 0.03 * math.sin(a))
    x, y = x * math.cos(tilt) - y * math.sin(tilt), x * math.sin(tilt) + y * math.cos(tilt)
    pts.append((cx + x - 6 * u, cy + y - 10 * u))
pts = jitter(pts, 1.5, seed=4)

base = 20
brush = Brush(pts, 2, 20, pressure(base, taper_in=0.05, taper_out=0.16, min_in=0.4, min_out=0.1,
                                   wobble=0.22, seed=2),
              max_width=base * 1.2, easing=(0.5, 0.0, 0.4, 1.0), chunks=3, slot="primary",
              name="circle")
emit(comp, [brush])

finish(comp, "callout-circle-scribble", "Circle Scribble",
       "Red marker circle scribbled around a subject, with the classic overshooting end.",
       ["circle", "scribble", "highlight", "thumbnail", "marker", "hand-drawn"], "intro-hold")
