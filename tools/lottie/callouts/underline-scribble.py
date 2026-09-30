import math

from _common import Brush, Comp, cubic_pts, emit, pressure
import _callouts2 as c2
from drift_lottie import Variant, build_asset
from lottie_kit import anim

W, H = 800, 160


def scribble():
    comp = Comp("underline-scribble", W, H, fps=30, frames=30)
    comp.slot("primary", "#FF2D2D")

    base = 19
    # long confident stroke left to right, then a quicker, shorter return stroke underneath
    first = [(40, 46), (52, 62), (72, 70)] + cubic_pts((72, 70), (280, 86), (540, 70), (764, 46), 60)[1:]
    second = cubic_pts((724, 72), (560, 98), (330, 112), (104, 112), 50)

    strokes = [
        Brush(first, 1, 13, pressure(base, taper_in=0.04, taper_out=0.14, min_in=0.5, min_out=0.2,
                                     wobble=0.14, seed=31),
              max_width=base * 1.2, easing=(0.5, 0.0, 0.35, 1.0), slot="primary", name="line-a"),
        Brush(second, 13, 22, pressure(base * 0.9, taper_in=0.06, taper_out=0.3, min_in=0.55,
                                       min_out=0.1, wobble=0.14, seed=32),
              max_width=base * 1.1, easing=(0.4, 0.0, 0.3, 1.0), smooth=False, slot="primary",
              name="line-b"),
    ]
    emit(comp, strokes)
    return comp


def clean():
    """Two crisp rounded lines: a long one shoots across, a shorter one follows underneath."""
    comp = Comp("underline-scribble--clean", W, H, fps=30, frames=30)
    comp.slot("primary", "#FF2D2D")
    ease = (0.6, 0.0, 0.2, 1.0)
    comp.layer("line-a", [c2.clean_line([(48, 62), (752, 62)], 16, t0=1, t1=12, ease=ease)],
               anchor=(W / 2, 62), position=(W / 2, 62),
               scale=anim([(11, [100, 100], c2.SETTLE), (14, [100, 150], c2.SETTLE), (19, [100, 100])]))
    comp.layer("line-b", [c2.clean_line([(150, 98), (650, 98)], 9, t0=8, t1=17, ease=ease, mid=True)])
    return comp


def neon():
    """Neon squiggle: a wavy glowing line that flickers on as it draws left to right."""
    comp = Comp("underline-scribble--neon", W, H, fps=30, frames=30)
    comp.slot("primary", "#FFE14D")
    n = 160
    pts = [(56 + 688 * i / n, 80 + 18 * math.sin(i / n * 2 * math.pi * 5.5)) for i in range(n + 1)]
    comp.layer("wave", [c2.neon_line(pts, 10, t0=1, t1=17, ease=(0.45, 0.0, 0.25, 1.0))],
               opacity=c2.flicker(1))
    return comp


build_asset("callouts", "underline-scribble", "Underline Scribble",
            "An underline that draws itself under a word or line of text for emphasis.",
            ["underline", "scribble", "marker", "emphasis", "hand-drawn", "text"], [
    Variant("scribble", "Marker Double", scribble(), "intro-hold", thumb_t=0.99,
            description="Quick hand-drawn double underline: a long marker stroke and a shorter return stroke."),
    Variant("clean", "Clean", clean(), "intro-hold", thumb_t=0.99,
            description="Crisp rounded line that shoots across with a little squash, with a shorter line underneath."),
    Variant("neon", "Neon Squiggle", neon(), "intro-hold", thumb_t=0.99,
            description="Wavy neon line that flickers on as it draws across."),
])
