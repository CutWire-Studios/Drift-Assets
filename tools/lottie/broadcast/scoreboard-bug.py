from _common import *

W, H, F = 846, 140, 60
comp = Comp("scoreboard-bug", W, H, fps=30, frames=F)
comp.slot("background", "#111111")
comp.slot("primary", "#D7263D")
comp.slot("secondary", "#1C6FE0")
comp.slot("accent", "#F5B700")
comp.slot("icon", "#34343D")

Y0, BH = 30, 80
YC = Y0 + BH / 2
CHIP = 22
NAME_A = (30 + CHIP, 200)
SCORE_A = (NAME_A[0] + NAME_A[1], 80)
SCORE_B = (SCORE_A[0] + 82, 80)
NAME_B = (SCORE_B[0] + 80, 200)
CHIP_B = NAME_B[0] + NAME_B[1]
BAR = (30, CHIP_B + CHIP)
CLOCK = (BAR[1] + 10, W - 30 - BAR[1] - 10)


def sheen(x, w, y=Y0, h=BH, r=0):
    return group([rect((w, h), (x + w / 2, y + h / 2), r),
                  gradient_fill([(0, "#FFFFFF", 0.12), (0.5, "#FFFFFF", 0.02), (0.5, "#FFFFFF", 0),
                                 (1, "#000000", 0.0)], (0, y), (0, y + h))], "sheen")


def wipe(name, shapes, x0, x1, t0, t1):
    w = x1 - x0
    comp.layer(name + " matte", [box(x0, Y0 - 10, w, BH + 20, "#FFFFFF")],
               anchor=(x0, YC), position=(x0, YC),
               scale=anim([(t0, [0, 100], SNAP_OUT), (t1, [100, 100])]))
    comp.layer(name, shapes, matte="alpha")


def pop(name, x, w, color=None, slot=None, t0=0):
    comp.layer(name, [sheen(x, w, Y0 + 6, BH - 12, 4), box(x, Y0 + 6, w, BH - 12, color or "#2A2A31", 4, slot=slot)],
               anchor=(x + w / 2, YC), position=(x + w / 2, YC),
               scale=anim([(t0, [0, 100], OVERSHOOT), (t0 + 10, [100, 100])]),
               opacity=anim([(t0, 0, EASE_OUT), (t0 + 4, 100)]))


def chip(name, x, slot, t0):
    comp.layer(name, [box(x, Y0, CHIP, BH, slot=slot)],
               anchor=(x, Y0 + BH), position=(x, Y0 + BH),
               scale=anim([(t0, [100, 0], SNAP_OUT), (t0 + 12, [100, 100])]))


# accent underline draws on beneath the whole bug
line_y = Y0 + BH + 2.5
comp.layer("accent line", [group([polyline([(30, line_y), (W - 30, line_y)]),
                                  stroke(slot="accent", width=5, cap="butt"),
                                  trim(end=anim([(8, 0, SNAP_OUT), (30, 100)]))], "line")])
pop("score a", SCORE_A[0] + 6, SCORE_A[1] - 12, slot="icon", t0=12)
pop("score b", SCORE_B[0] + 6, SCORE_B[1] - 12, slot="icon", t0=15)
chip("chip a", 30, "primary", 6)
chip("chip b", CHIP_B, "secondary", 9)
wipe("bar", [sheen(BAR[0], BAR[1] - BAR[0]),
             box(SCORE_A[0] + SCORE_A[1], Y0 + 14, 2, BH - 28, "#FFFFFF", opacity=18),
             box(BAR[0], Y0, BAR[1] - BAR[0], BH, slot="background")], BAR[0], BAR[1], 0, 16)
wipe("clock", [sheen(*CLOCK), box(CLOCK[0], Y0, CLOCK[1], BH, slot="background")],
     CLOCK[0], CLOCK[0] + CLOCK[1], 10, 24)

finish(comp, "broadcast", "scoreboard-bug", "Scoreboard Bug",
       "Sports score bug with two team colour chips, empty team-name, score and clock boxes. "
       "Text area covers the whole bar; place names, scores and clock inside their boxes.",
       ["scoreboard", "score", "sports", "broadcast", "bug", "football", "soccer"], "intro-hold",
       text_area=[30, Y0, W - 60, BH], thumb_t=1.0, bg="e8e8ee")
