from _common import *

W, H, F = 1400, 420, 75
comp = Comp("game-show-panel", W, H, fps=30, frames=F)
comp.slot("primary", "#0B2470")

CX, CY = W / 2, H / 2
PW, PH, R = 1320, 340, 30


def plate(d):
    return rect((PW - 2 * d, PH - 2 * d), (CX, CY), max(R - d, 2))


def vgrad(stops):
    return gradient_fill(stops, (0, CY - PH / 2), (0, CY + PH / 2))


GOLD_HI = [(0, "#FFF0B0"), (0.35, "#F0C75A"), (0.7, "#B7862A"), (1, "#7A5410")]
GOLD_LO = [(0, "#6E4A0C"), (0.4, "#A77A22"), (1, "#FBE28E")]
IN = 18

par = comp.null("panel", anchor=(CX, CY), position=(CX, CY),
                scale=anim([(0, [0, 5], SNAP_OUT), (11, [100, 5], EASE_IN_OUT), (13, [100, 5], OVERSHOOT),
                             (25, [100, 100])]),
                opacity=anim([(0, 0, EASE_OUT), (3, 100)]))

comp.layer("sweep matte", [group([plate(0), fill("#FFFFFF")], "matte")], parent=par)
comp.layer("sweep", [group([rect((220, 900)), gradient_fill(
    [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.42), (1, "#FFFFFF", 0)], (-110, 0), (110, 0))], "band",
    rotation=18)],
    position=anim([(0, [-260, CY], HOLD), (28, [-260, CY], EASE_IN_OUT), (54, [W + 260, CY])]),
    matte="alpha")
comp.layer("glow", [group([plate(IN), gradient_fill(
    [(0, "#FFFFFF", 0.20), (0.55, "#FFFFFF", 0.06), (1, "#000000", 0.14)], (CX, CY - 30),
    (CX + PW / 2, CY), radial=True)], "glow")], parent=par)
comp.layer("face", [group([plate(IN), fill(slot="primary")], "face")], parent=par)
comp.layer("inner line", [group([plate(IN - 2), fill("#3B2806")], "line")], parent=par)
comp.layer("bevel in", [group([plate(10), vgrad(GOLD_LO)], "bevel in")], parent=par)
comp.layer("bevel out", [group([plate(2), vgrad(GOLD_HI)], "bevel out")], parent=par)
comp.layer("edge", [group([plate(0), fill("#2A1C04")], "edge")], parent=par)
comp.layer("shadow", [group([plate(-4), fill("#000000", 30)], "shadow", position=(0, 8))], parent=par)

finish(comp, "broadcast", "game-show-panel", "Game Show Panel",
       "Big quiz-show question plate: deep blue face with a bevelled gold frame that opens out and "
       "catches a light sweep.",
       ["quiz", "game show", "question", "trivia", "panel", "plate", "gold"], "intro-hold",
       text_area=[80, 70, 1240, 280], thumb_t=0.52)
