"""Confetti cannon: a pop from the bottom, pieces tumble up, arc over with drag and flutter down."""

import math
import random

from _common import *
import _reactions2 as r2
from drift_lottie import Variant, build_asset

T = 75
W, H = 800, 700
OX, OY = 400, 650
COLORS = [("primary", "#FF4D6D"), ("secondary", "#FFC93C"), ("accent", "#2EC4B6")]


def simulate(angle, speed, drag, g, t_end, sway, sway_ph, ox=OX, oy=OY):
    x, y = ox, oy
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



def flat():
    comp = Comp("confetti-burst", W, H, fps=30, frames=T)
    for sid, c in COLORS:
        comp.slot(sid, c)

    rng = random.Random(11)



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
    return comp


def cartoon_piece(st, rnd, col, sid):
    """Outlined cartoon confetti: star, squiggle, circle or triangle."""
    kind = rnd.random()
    ink = [stroke(st.ink, 5, slot="outline")]
    if kind < 0.3:
        return [group(svg_shapes(r2.star_d(15, 0.5)) + ink + [fill(col, slot=sid)])]
    if kind < 0.55:
        d = "M -18 0 C -12 -10 -6 -10 0 0 C 6 10 12 10 18 0"
        return [group(svg_shapes(d) + [stroke(col, 7, slot=sid)]), group(svg_shapes(d) + [stroke(st.ink, 15, slot="outline")])]
    if kind < 0.8:
        return [group([ellipse((20, 20))] + ink + [fill(col, slot=sid)])]
    return [group(svg_shapes("M 0 -13 L 12 9 L -12 9 Z") + [stroke(st.ink, 5, slot="outline", join="round"),
                                                           fill(col, slot=sid)])]


def radial():
    """Cartoon party pop: outlined stars, squiggles and dots explode out from the middle, hang and drift down."""
    st = r2.Style("outline")
    comp = Comp("confetti-burst--outline", W, H, fps=30, frames=T)
    for sid, c in COLORS:
        comp.slot(sid, c)
    comp.slot("outline", st.ink)
    cx, cy = W / 2, 330
    rnd = random.Random(21)
    for i in range(44):
        sid, col = COLORS[i % 3]
        a = rnd.uniform(0, 2 * math.pi)
        speed = rnd.uniform(18, 42)
        launch = rnd.uniform(0, 3)
        life = int(rnd.uniform(58, 72) - launch)
        pts = simulate(a, speed, 0.885, 0.36, life + 1, rnd.uniform(8, 20), rnd.uniform(0, 6.28), cx, cy)
        spin = rnd.uniform(3, 9) * rnd.choice((-1, 1))
        rot0 = rnd.uniform(0, 360)
        size = rnd.uniform(0.9, 1.35)

        def fn(u, pts=pts, spin=spin, rot0=rot0, size=size, life=life):
            k = min(int(u), len(pts) - 2)
            f = u - k
            x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f
            y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
            s = 100 * size * (r2.back_out(min(u / 5, 1)) if u < 5 else 1)
            return {"position": (x, y), "rotation": rot0 + spin * u, "scale": (s, s),
                    "opacity": 100 if u < life - 12 else 100 * max(0.0, (life - u) / 12)}

        particle(comp, f"piece{i}", cartoon_piece(st, rnd, col, sid), round(launch, 2), life, T, fn, step=3,
                 wrap=False)
    # the pop itself: a quick outlined flash star
    comp.layer("flash", [group(svg_shapes(r2.star_d(70, 0.45, 8)) + [stroke(st.ink, 7, slot="outline"),
                                                                     fill(COLORS[1][1], slot="secondary")])],
               position=(cx, cy), op=10, scale=anim([(0, [20, 20], SNAP_OUT), (4, [120, 120], EASE_IN), (9, [0, 0])]),
               rotation=anim([(0, -30), (9, 20)]))
    return comp


def foil():
    """Twin cannons fire glossy foil confetti from both bottom corners that crosses over and flutters down."""
    comp = Comp("confetti-burst--glossy", W, H, fps=30, frames=T)
    for sid, c in COLORS:
        comp.slot(sid, c)
    rnd = random.Random(33)
    guns = [(60, 670, 1), (740, 670, -1)]
    for i in range(60):
        gx, gy, side = guns[i % 2]
        sid, col = COLORS[(i // 2) % 3]
        angle = math.radians(side * (26 + rnd.gauss(0, 8)))
        speed = rnd.uniform(50, 72)
        launch = rnd.uniform(0, 5)
        life = int(rnd.uniform(62, 75) - launch)
        pts = simulate(angle, speed, rnd.uniform(0.9, 0.915), 0.8, life + 1, rnd.uniform(12, 26),
                       rnd.uniform(0, 6.28), gx, gy)
        spin = rnd.uniform(10, 22) * rnd.choice((-1, 1))
        rot0 = rnd.uniform(0, 360)
        flip_w, flip_ph = rnd.uniform(0.2, 0.42), rnd.uniform(0, 6.28)
        if rnd.random() < 0.7:
            w, h = rnd.uniform(18, 22), rnd.uniform(28, 36)
            base = rect((w, h), roundness=3)
            gleam = group([rect((w * 0.28, h * 0.8), (-w * 0.2, 0), roundness=2), fill("#FFFFFF", 55)], name="gleam")
        else:
            d = rnd.uniform(18, 24)
            base = ellipse((d, d))
            gleam = group([ellipse((d * 0.4, d * 0.28), (-d * 0.14, -d * 0.18)), fill("#FFFFFF", 70)], name="gleam")
        shade = group([base, gradient_fill([(0, "#FFFFFF", 0.35), (0.5, "#FFFFFF", 0), (1, "#000000", 0.3)],
                                           (-12, -16), (12, 16))], name="sheen")
        shapes = [gleam, shade, group([base, fill(col, slot=sid)], name="foil")]

        def fn(u, pts=pts, spin=spin, rot0=rot0, flip_w=flip_w, flip_ph=flip_ph, life=life):
            k = min(int(u), len(pts) - 2)
            f = u - k
            x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f
            y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
            flip = math.cos(flip_ph + flip_w * u)
            s = 100 * min(1, 0.3 + u / 3)
            return {"position": (x, y), "rotation": rot0 + spin * (1 - math.exp(-u / 14)) * 14,
                    "scale": (s * (0.25 + 0.75 * abs(flip)), s),
                    "opacity": 100 if u < life - 14 else 100 * max(0.0, (life - u) / 14)}

        particle(comp, f"foil{i}", shapes, round(launch, 2), life, T, fn, step=3, wrap=False)
    for gx, gy, side in guns:
        streaks = []
        for a in (-24, 0, 24):
            r = math.radians(side * 26 + a)
            dx, dy = math.sin(r), -math.cos(r)
            streaks.append(group([path(bezier([(dx * 30, dy * 30), (dx * 110, dy * 110)], closed=False)),
                                  trim(start=anim([(0, 0, EASE_IN), (10, 100)]), end=anim([(0, 0, SNAP_OUT), (7, 100)])),
                                  stroke("#FFC93C", 9, slot="secondary")], name=f"streak{a}"))
        comp.layer(f"pop{side}", streaks, op=12, position=(gx, gy))
    return comp


build_asset("reactions", "confetti-burst", "Confetti Burst",
            "One-shot confetti burst: pieces fly out, tumble with gravity and flutter down while fading; "
            "ends empty.",
            ["confetti", "party", "celebration", "burst", "congrats", "reaction"], [
    Variant("flat", "Flat Cannon", flat(), "intro-hold", thumb_t=0.33,
            description="One-shot confetti cannon: rectangles, dots and strips burst upward, tumble over with "
                        "gravity and flutter down while fading out."),
    Variant("outline", "Cartoon Pop", radial(), "intro-hold", thumb_t=0.2, bg="e8e8ee",
            description="Outlined cartoon stars, squiggles and dots explode out from the middle and drift down."),
    Variant("glossy", "Glossy Twin Cannons", foil(), "intro-hold", thumb_t=0.33,
            description="Shiny foil confetti fired from both bottom corners that crosses over and flutters down."),
])
