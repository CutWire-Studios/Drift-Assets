from _common import Comp, bezier, path, stamp, stroke
from _retro_b import badge_stamp, marker_stamp
from drift_lottie import Variant, build_asset

W = H = 500


def rubber():
    comp = Comp("stamp-cross", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D")
    a = bezier([(-70, -70), (70, 70)], closed=False)
    b = bezier([(70, -70), (-70, 70)], closed=False)
    stamp(comp, [path(a, "stroke-a"), path(b, "stroke-b"), stroke(slot="primary", width=42)], seed=11,
          tilt=8)
    return comp


def badge():
    comp = Comp("stamp-cross--badge", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D")
    badge_stamp(comp, [[(-54, -54), (54, 54)], [(54, -54), (-54, 54)]], tilt=6)
    return comp


def marker():
    comp = Comp("stamp-cross--marker", W, H, fps=30, frames=36)
    comp.slot("primary", "#FF2D2D")
    marker_stamp(comp, [[(-80, -86), (0, -4), (84, 80)], [(82, -90), (4, 0), (-78, 84)]], seed=11,
                 start=-60, tilt=6, taper=(0.12, 0.25), mins=(0.7, 0.45))
    return comp


build_asset("callouts", "stamp-cross", "Cross Stamp",
            "Red cross that lands with a hard hit, for rejections, wrong answers and things to avoid.",
            ["stamp", "cross", "rejected", "wrong", "no", "denied"], [
    Variant("rubber", "Rubber Stamp", rubber(), "intro-hold", thumb_t=0.99,
            description="Red rubber-stamp cross that slams down with a little bounce and ink texture."),
    Variant("badge", "Clean Badge", badge(), "intro-hold", thumb_t=0.99,
            description="Flat disc pops in with a twist, a white cross draws on stroke by stroke and a ripple flicks out."),
    Variant("marker", "Marker Cross", marker(), "intro-hold", thumb_t=0.99,
            description="Marker circle scribbled round, then two quick crossing marker strokes."),
])
