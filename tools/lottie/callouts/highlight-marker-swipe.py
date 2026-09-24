import random

from _common import (Comp, anim, bezier, cubic_pts, fill, finish, group, path, pressure, resample,
                     ribbon)

W, H = 800, 140
comp = Comp("highlight-marker-swipe", W, H, fps=30, frames=30)
comp.slot("primary", "#FFD60A")

x0, x1 = 34, 770
center, _ = resample(cubic_pts((x0, 76), (260, 70), (540, 74), (x1, 64), 60), 4)
width = pressure(84, taper_in=0, taper_out=0, wobble=0.05, seed=11)
rnd = random.Random(21)


def ragged(c, half_bottom, half_top, lean, direction):
    """Chisel-tip end from the bottom edge to the top edge (direction +1 at the right end).

    The edge leans like a chisel held at an angle and frays into a few short bristles.
    """
    pts = []
    n = 9
    for i in range(1, n):
        u = i / n
        y = c[1] + half_bottom - u * (half_bottom + half_top)
        fray = rnd.uniform(-5, 5) + (rnd.uniform(4, 11) if i % 3 == 1 else 0)
        pts.append((c[0] + direction * (lean * (0.5 - u) + fray), y))
    return pts if direction > 0 else pts[::-1]


end_edge = ragged(center[-1], width(1) / 2, width(1) / 2, 16, 1)
start_edge = ragged(center[0], width(0) / 2, width(0) / 2, 16, -1)
rib = ribbon(center, width, start_edge=start_edge, end_edge=end_edge)


def band_y(x):
    """Centre line height at x (the band rises slightly towards the right)."""
    return next(p[1] for p in center if p[0] >= x) if x < center[-1][0] else center[-1][1]


def streak(dy, x_a, x_b, h, seed):
    r = random.Random(seed)
    top = [(x, band_y(x) + dy + r.uniform(-0.6, 0.6)) for x in range(int(x_a), int(x_b), 40)]
    bot = [(x, y + h + r.uniform(-0.6, 0.6)) for x, y in reversed(top)]
    return path(bezier(top + bot), f"streak{seed}")


# faint lengthwise streaks where the felt tip laid down less ink
streaks = [group([streak(dy, xa, xb, h, i), fill("#FFFFFF", op)], f"streak-{i}")
           for i, (dy, xa, xb, h, op) in enumerate([(-30, 60, 700, 3, 16), (-8, 120, 760, 2, 11),
                                                    (14, 50, 610, 4, 13), (31, 180, 740, 2, 14)])]

# reveal: a slanted wipe whose leading edge sweeps left to right
top_y, bot_y, lean = -10, H + 10, 18


def wipe(x):
    return bezier([(x0 - 60, top_y), (x + lean, top_y), (x - lean, bot_y), (x0 - 60, bot_y)])


sweep = anim([(2, wipe(x0 - 40), (0.45, 0.0, 0.2, 1.0)), (15, wipe(x1 + 40))])
comp.layer("reveal", [group([path(sweep, "wipe"), fill("#FFFFFF")], "wipe")])
comp.layer("highlight", [group(streaks + [group([path(rib, "band"), fill(slot="primary")], "ink")], "band")],
           matte="alpha", opacity=55)

finish(comp, "highlight-marker-swipe", "Highlighter Swipe",
       "Translucent yellow highlighter stroke swiped left to right behind a word or line.",
       ["highlight", "highlighter", "marker", "emphasis", "hand-drawn", "text"], "intro-hold",
       bg="e8e8ee")
