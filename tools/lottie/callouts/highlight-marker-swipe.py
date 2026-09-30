import random

from _common import (Comp, anim, bezier, cubic_pts, fill, group, path, pressure, resample,
                     ribbon)
import _callouts2 as c2
from drift_lottie import Variant, build_asset
from lottie_kit import EASE_OUT, rect

W, H = 800, 140
BW, BH = 736, 84
BC = (402, 70)


def marker():
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
    return comp


def clean():
    """Flat rounded bar with slanted ends that grows out from the left and settles."""
    comp = Comp("highlight-marker-swipe--clean", W, H, fps=30, frames=30)
    comp.slot("primary", "#FFD60A")
    x0 = BC[0] - BW / 2
    comp.layer("bar", [group([rect((BW, BH - 8), roundness=14), fill(slot="primary")], "bar", skew=-14)],
               anchor=(-BW / 2, 0), position=(x0 + 8, BC[1]), opacity=60,
               scale=anim([(1, [0, 100], (0.6, 0.0, 0.2, 1.0)), (13, [102, 100], c2.SETTLE), (18, [100, 100])]))
    return comp


def bold():
    """Comic label block with an ink outline and hard shadow that slams in with a tilt."""
    comp = Comp("highlight-marker-swipe--bold", W, H, fps=30, frames=30)
    comp.slot("primary", "#FFD60A")
    comp.slot("outline", c2.INK)
    comp.layer("block", c2.comic([rect((BW - 24, BH - 8), roundness=6)], "primary", "outline", "outline",
                                 width=6, shadow=(8, 8)),
               position=(BC[0] - 4, BC[1] - 2),
               scale=anim([(1, [0, 60], c2.SETTLE), (7, [104, 112], c2.SETTLE), (11, [99, 96], c2.SETTLE),
                           (15, [100, 100])]),
               rotation=anim([(1, -6, c2.SETTLE), (8, 1.5, c2.SETTLE), (14, -1)]))
    return comp


build_asset("callouts", "highlight-marker-swipe", "Highlighter Swipe",
            "A highlight band swiped in behind a word or line of text to make it stand out.",
            ["highlight", "highlighter", "marker", "emphasis", "hand-drawn", "text"], [
    Variant("marker", "Highlighter", marker(), "intro-hold", thumb_t=0.99, bg="e8e8ee",
            description="Translucent yellow highlighter stroke swiped left to right behind a word or line."),
    Variant("clean", "Clean Bar", clean(), "intro-hold", thumb_t=0.99, bg="e8e8ee",
            description="Flat translucent bar with slanted ends that grows out from the left."),
    Variant("bold", "Comic Label", bold(), "intro-hold", thumb_t=0.99, bg="e8e8ee",
            description="Solid comic label block with an ink outline and hard shadow that slams in with a tilt."),
])
