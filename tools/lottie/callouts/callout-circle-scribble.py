import math

from _common import Brush, Comp, emit, jitter, pressure
import _callouts2 as c2
from drift_lottie import Variant, build_asset
from lottie_kit import EASE_IN, EASE_OUT, anim, ellipse, fill, group, stroke

W, H = 640, 440
C = (W / 2, H / 2)
RX, RY = 262, 166


def scribble():
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
    return comp


def clean():
    """Crisp vector ellipse drawing out both ways from the top, with a faint tint and an echo ring."""
    comp = Comp("callout-circle-scribble--clean", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D")
    pts = c2.ellipse_pts((0, 0), RX, RY, start=-90)
    comp.layer("ring", [c2.clean_line(pts, 12, t0=1, t1=18, mid=True, ease=(0.5, 0.0, 0.2, 1.0))], position=C,
               rotation=-4, scale=anim([(16, [100, 100], c2.SETTLE), (20, [103, 103], c2.SETTLE), (26, [100, 100])]))
    comp.layer("echo", [group([ellipse((2 * RX, 2 * RY)), stroke(slot="primary", width=anim([(17, 8, EASE_OUT),
                                                                                             (31, 1)]))], "e")],
               position=C, rotation=-4, ip=17, op=32, scale=anim([(17, [100, 100], c2.DECEL), (31, [112, 118])]),
               opacity=anim([(17, 70, EASE_IN), (31, 0)]))
    comp.layer("tint", [group([ellipse((2 * RX, 2 * RY)), fill(slot="primary", opacity=10)], "t")], position=C,
               rotation=-4, opacity=anim([(10, 0, EASE_OUT), (24, 100)]))
    return comp


def neon():
    """Neon tube ellipse that flickers on while it traces round, then hums."""
    comp = Comp("callout-circle-scribble--neon", W, H, fps=30, frames=36)
    comp.slot("primary", "#2DE2FF")
    pts = c2.ellipse_pts((0, 0), RX - 10, RY - 8, start=-130, turns=1.0)
    comp.layer("ring", [c2.neon_line(pts, 11, t0=1, t1=20, ease=(0.45, 0.0, 0.25, 1.0))], position=C, rotation=-6,
               opacity=c2.flicker(1))
    return comp


build_asset("callouts", "callout-circle-scribble", "Circle Scribble",
            "A circle drawn around a subject to single it out; place it over whatever you want "
            "viewers to look at.",
            ["circle", "scribble", "highlight", "thumbnail", "marker", "hand-drawn"], [
    Variant("scribble", "Marker Scribble", scribble(), "intro-hold", thumb_t=0.99,
            description="Red marker circle scribbled around a subject, with the classic overshooting end."),
    Variant("clean", "Clean", clean(), "intro-hold", thumb_t=0.99,
            description="Crisp vector ellipse that draws out both ways from the top, with a faint tint and an echo ring."),
    Variant("neon", "Neon", neon(), "intro-hold", thumb_t=0.99,
            description="Glowing neon ring that flickers on as it traces round."),
])
