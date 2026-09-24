from _common import Comp, bezier, finish, path, stamp, stroke

W = H = 500
comp = Comp("stamp-check", W, H, fps=30, frames=36)
comp.slot("primary", "#1FAE4B")

check = bezier([(-78, 2), (-24, 58), (84, -70)], closed=False)
stamp(comp, [path(check, "check"), stroke(slot="primary", width=40, join="round")], seed=7,
      tilt=-10)

finish(comp, "stamp-check", "Check Stamp",
       "Green rubber-stamp check mark that slams down with a little bounce and ink texture.",
       ["stamp", "check", "approved", "correct", "yes", "tick"], "intro-hold")
