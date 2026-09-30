from _common import Comp, bezier, path, stamp, stroke
from _retro_b import badge_stamp, marker_stamp
from drift_lottie import Variant, build_asset

W = H = 500


def rubber():
    comp = Comp("stamp-check", W, H, fps=30, frames=36)
    comp.slot("primary", "#1FAE4B")
    check = bezier([(-78, 2), (-24, 58), (84, -70)], closed=False)
    stamp(comp, [path(check, "check"), stroke(slot="primary", width=40, join="round")], seed=7,
          tilt=-10)
    return comp


def badge():
    comp = Comp("stamp-check--badge", W, H, fps=30, frames=36)
    comp.slot("primary", "#1FAE4B")
    badge_stamp(comp, [[(-64, 4), (-20, 48), (68, -54)]], tilt=-6)
    return comp


def marker():
    comp = Comp("stamp-check--marker", W, H, fps=30, frames=36)
    comp.slot("primary", "#1FAE4B")
    marker_stamp(comp, [[(-96, -14), (-38, 60), (126, -122)]], seed=7)
    return comp


build_asset("callouts", "stamp-check", "Check Stamp",
            "Green check mark that lands with a satisfying hit, for approvals, right answers and "
            "done items.",
            ["stamp", "check", "approved", "correct", "yes", "tick"], [
    Variant("rubber", "Rubber Stamp", rubber(), "intro-hold", thumb_t=0.99,
            description="Green rubber-stamp check mark that slams down with a little bounce and ink texture."),
    Variant("badge", "Clean Badge", badge(), "intro-hold", thumb_t=0.99,
            description="Flat disc pops in with a twist, a white check draws on and a ripple flicks out."),
    Variant("marker", "Marker Tick", marker(), "intro-hold", thumb_t=0.99,
            description="Teacher-style marker circle scribbled round, then a big tick swooshed through it."),
])
