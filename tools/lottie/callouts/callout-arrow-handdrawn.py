import math

from _common import Brush, Comp, cubic_pts, emit, pressure
import _callouts2 as c2
from drift_lottie import Variant, build_asset

W, H = 520, 400
START, TIP = (58, 342), (452, 118)


def hand():
    comp = Comp("callout-arrow-handdrawn", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D")

    base = 24
    start, tip = (58, 342), (452, 118)
    shaft = cubic_pts(start, (118, 222), (250, 138), tip)

    # the head opens around the direction the shaft arrives from
    ang = math.atan2(tip[1] - 138, tip[0] - 250)


    def barb(side, length, spread):
        a = ang + math.pi + side * math.radians(spread)
        return (tip[0] + length * math.cos(a), tip[1] + length * math.sin(a))


    def bowed(p, q, bow):
        """Slightly curved segment p -> q; bow in px to the left of travel."""
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy)
        c = (mx - dy / ln * bow, my + dx / ln * bow)
        return cubic_pts(p, ((p[0] + 2 * c[0]) / 3, (p[1] + 2 * c[1]) / 3),
                         ((q[0] + 2 * c[0]) / 3, (q[1] + 2 * c[1]) / 3), q, 24)


    up, down = barb(-1, 112, 42), barb(1, 104, 44)
    # first head stroke runs a little past the tip, like a quick pen that overshoots
    past = (tip[0] + 9 * math.cos(ang - 0.35), tip[1] + 9 * math.sin(ang - 0.35))

    strokes = [
        Brush(shaft, 1, 16, pressure(base, taper_in=0.05, taper_out=0.1, min_in=0.45, min_out=0.6,
                                     wobble=0.18, seed=3),
              max_width=base * 1.25, easing=(0.45, 0.0, 0.3, 1.0), smooth=False, slot="primary",
              name="shaft"),
        Brush(bowed(up, past, -6), 17, 22, pressure(base, taper_in=0.2, taper_out=0.1, min_in=0.75,
                                                    min_out=0.8, wobble=0.1, seed=5),
              max_width=base * 1.2, easing=(0.4, 0.0, 0.3, 1.0), smooth=False, slot="primary",
              name="head-a"),
        Brush(bowed(tip, down, -5), 23, 28, pressure(base, taper_in=0.1, taper_out=0.35, min_in=0.9,
                                                     min_out=0.55, wobble=0.1, seed=7),
              max_width=base * 1.2, easing=(0.4, 0.0, 0.3, 1.0), smooth=False, slot="primary",
              name="head-b"),
    ]
    emit(comp, strokes)
    return comp


def styled(style, width, head=None):
    comp = Comp(f"callout-arrow-handdrawn--{style}", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D" if style == "clean" else "#FF3DBB")
    shaft = c2.dense(cubic_pts(START, (118, 222), (250, 138), TIP, 80))
    c2.arrow(comp, shaft, style, 1, 16, width, head=head, seed=3)
    return comp


build_asset("callouts", "callout-arrow-handdrawn", "Hand-Drawn Arrow",
            "Curved arrow that sweeps up and to the right as it draws on; point it at whatever you "
            "want viewers to notice.",
            ["arrow", "pointer", "marker", "hand-drawn", "thumbnail", "callout"], [
    Variant("hand", "Marker", hand(), "intro-hold", thumb_t=0.99,
            description="Marker-style curved arrow drawn on: the shaft sweeps up, then the head is flicked on."),
    Variant("clean", "Clean", styled("clean", 18), "intro-hold", thumb_t=0.99,
            description="Even vector line with a rounded solid arrowhead that pops on."),
    Variant("neon", "Neon", styled("neon", 13, 72), "intro-hold", thumb_t=0.99,
            description="Glowing neon tube that flickers on as it draws, with a chevron head."),
])
