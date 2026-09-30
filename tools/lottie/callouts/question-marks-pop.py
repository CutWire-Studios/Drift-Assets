import math

from _common import (ANTICIPATE, Comp, anim, ellipse, fill, group, stroke, svg_shapes)
import _callouts2 as c2
from drift_lottie import Variant, build_asset
from lottie_kit import HOLD

W, H = 460, 380
MARKS = [(230, 250, 118, 4, 0, 46), (106, 318, 82, -22, 6, 49), (360, 330, 88, 20, 12, 52)]
HOOK_PTS = c2.dense(c2.cubic((-34, -112), (-34, -160), (34, -166), (36, -118), 40)
                    + c2.cubic((36, -118), (38, -84), (2, -82), (2, -46), 40)[1:], 2.5)


def bold():
    comp = Comp("question-marks-pop", W, H, fps=30, frames=60)
    comp.slot("primary", "#FF2D2D")
    comp.slot("outline", "#141414")

    # '?' as a thick round-capped hook plus a dot, centred so (0, 0) sits at the bottom of the dot
    HOOK = "M -34 -112 C -34 -160 34 -166 36 -118 C 38 -84 2 -82 2 -46"
    DOT = (2, -12)


    def glyph():
        return [
            group(svg_shapes(HOOK, name="hook") + [stroke(slot="primary", width=26)], "hook"),
            group([ellipse((30, 30), DOT), fill(slot="primary")], "dot"),
            group(svg_shapes(HOOK, name="hook-o") + [stroke(slot="outline", width=40)], "hook-outline"),
            group([ellipse((44, 44), DOT), fill(slot="outline")], "dot-outline"),
        ]


    POP = (0.2, 0.0, 0.3, 1.0)
    WOB = (0.45, 0.0, 0.55, 1.0)
    marks = [  # (x, y of the dot bottom, size %, lean in degrees, pop-in frame, pop-out frame)
        (230, 250, 118, 4, 0, 46),
        (106, 318, 82, -22, 6, 49),
        (360, 330, 88, 20, 12, 52),
    ]
    for n, (x, y, size, lean, d, out) in enumerate(marks):
        s = size
        scale = anim([(d, [0, 0], POP), (d + 5, [s * 1.18, s * 1.18], POP),
                      (d + 9, [s * 0.93, s * 0.93], POP), (d + 13, [s, s], WOB),
                      (out, [s, s], ANTICIPATE), (out + 7, [0, 0])])
        rot = [(d, lean - 24, POP), (d + 8, lean + 9, WOB)]
        f, sign = d + 8, -1
        while f + 9 < out:
            f += 9
            rot.append((f, lean + sign * 7, WOB))
            sign = -sign
        rot.append((out + 7, lean + sign * 14))
        pos = anim([(d, [x, y + 26], POP), (d + 7, [x, y], WOB), (out, [x, y - 8], ANTICIPATE),
                    (out + 7, [x, y + 10])])
        comp.layer(f"question-{n}", glyph(), position=pos, scale=scale, rotation=anim(rot),
                   ip=d, op=out + 7)
    return comp


def holder(comp, n, x, y, size, lean, d, out, pop_in=True):
    """Null for one mark: settles in, sways while it waits, then pops away (loop-safe)."""
    s = size
    sc = [(d, [s * 0.7, s * 0.7] if not pop_in else [0, 0], c2.SETTLE), (d + 6, [s * 1.08, s * 1.08], c2.SETTLE),
          (d + 11, [s, s], c2.SETTLE), (out, [s, s], ANTICIPATE), (out + 7, [0, 0])]
    rot = [(d, lean - 14, c2.SETTLE), (d + 9, lean + 6, (0.45, 0.0, 0.55, 1.0))]
    f, sign = d + 9, -1
    while f + 10 < out:
        f += 10
        rot.append((f, lean + sign * 6, (0.45, 0.0, 0.55, 1.0)))
        sign = -sign
    rot.append((out + 7, lean + sign * 12))
    return comp.null(f"mark{n}", position=(x, y), scale=anim(sc), rotation=anim(rot), ip=d, op=out + 7)


def hand():
    """Marker question marks that scribble themselves on one after another, sway, then pop away."""
    comp = Comp("question-marks-pop--hand", W, H, fps=30, frames=60)
    comp.slot("primary", "#FF2D2D")
    for n, (x, y, size, lean, d, out) in enumerate(MARKS):
        h = holder(comp, n, x, y, size, lean, d, out, pop_in=False)
        dot = [(2 + r * math.cos(a), -14 + r * math.sin(a))
               for r, a in ((10 * (1 - i / 40) + 1.5, math.radians(-90 + i * 16)) for i in range(41))]
        c2.emit(comp, [c2.hand_line(HOOK_PTS, d, d + 8, 24, seed=3 + n, taper=(0.06, 0.3), mins=(0.7, 0.5),
                                    wob=0.06, name=f"hook{n}"),
                       c2.hand_line(c2.dense(dot, 1.5), d + 8, d + 11, 13, seed=9 + n, taper=(0.1, 0.1),
                                    mins=(0.8, 0.8), wob=0.03, name=f"dot{n}")], parent=h, op=out + 7)
    return comp


def neon():
    """Neon question marks that flicker on one after another, hum, then blink out."""
    comp = Comp("question-marks-pop--neon", W, H, fps=30, frames=60)
    comp.slot("primary", "#B84DFF")
    for n, (x, y, size, lean, d, out) in enumerate(MARKS):
        h = holder(comp, n, x, y, size, lean, d, out, pop_in=False)
        off = anim([(0, 100, HOLD), (out, 100, HOLD), (out + 1, 30, HOLD), (out + 2, 100, HOLD), (out + 7, 100)])
        comp.layer(f"glyph{n}", [c2.neon_line(HOOK_PTS, 11, t0=d, t1=d + 8, name="hook"),
                                 c2.neon_line(c2.ellipse_pts((2, -14), 9, 9, start=-90), 9, t0=d + 6, t1=d + 10,
                                              name="dot")],
                   parent=h, ip=d, op=out + 7, opacity=c2.flicker(d) if n % 2 == 0 else off)
    return comp


build_asset("callouts", "question-marks-pop", "Question Marks Pop",
            "Three question marks pop in one after another and wobble in confusion, then pop away; "
            "loops seamlessly.",
            ["question", "confused", "huh", "reaction", "thinking", "cartoon"], [
    Variant("bold", "Comic Bold", bold(), "loop", thumb_t=0.55,
            description="Three chunky outlined question marks that pop in one after another and wobble in confusion."),
    Variant("hand", "Hand-Drawn", hand(), "loop", thumb_t=0.55,
            description="Marker question marks that scribble themselves on one after another, sway, then pop away."),
    Variant("neon", "Neon", neon(), "loop", thumb_t=0.55,
            description="Neon question marks that flicker on one after another, hum, then shrink away."),
])
