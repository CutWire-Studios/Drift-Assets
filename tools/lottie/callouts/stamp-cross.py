from _common import Comp, bezier, finish, path, stamp, stroke

W = H = 500
comp = Comp("stamp-cross", W, H, fps=30, frames=36)
comp.slot("primary", "#FF2D2D")

a = bezier([(-70, -70), (70, 70)], closed=False)
b = bezier([(70, -70), (-70, 70)], closed=False)
stamp(comp, [path(a, "stroke-a"), path(b, "stroke-b"), stroke(slot="primary", width=42)], seed=11,
      tilt=8)

finish(comp, "stamp-cross", "Cross Stamp",
       "Red rubber-stamp cross that slams down with a little bounce and ink texture.",
       ["stamp", "cross", "rejected", "wrong", "no", "denied"], "intro-hold")
