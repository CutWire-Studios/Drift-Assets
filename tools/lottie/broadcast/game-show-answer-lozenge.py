import math

from _common import *

W, H, F = 1400, 180, 120
comp = Comp("game-show-answer-lozenge", W, H, fps=30, frames=F)
comp.slot("primary", "#0A1F5C")
comp.slot("secondary", "#F28C00")
comp.slot("accent", "#1FA23A")

CY = H / 2
X0, X1, HH = 170, 1230, 58  # tip x positions, half height


def hexagon(d=0.0):
    """Hexagon-ended bar inset by d (45-degree ends)."""
    tip = d * math.sqrt(2)
    cor = d * (math.sqrt(2) - 1)
    h = HH - d
    return polyline([(X0 + tip, CY), (X0 + HH + cor, CY - h), (X1 - HH - cor, CY - h),
                     (X1 - tip, CY), (X1 - HH - cor, CY + h), (X0 + HH + cor, CY + h)], closed=True)


SILVER = [(0, "#FFFFFF"), (0.5, "#D3D9E2"), (1, "#7F8897")]
GOLD = [(0, "#FFE9A0"), (0.5, "#E0B044"), (1, "#8E6516")]
IN = 10

par = comp.null("lozenge", anchor=(W / 2, CY), position=(W / 2, CY),
                scale=anim([(0, [0, 100], SNAP_OUT), (16, [100, 100])]),
                opacity=anim([(0, 0, EASE_OUT), (3, 100)]))

flash = anim([(0, 0, HOLD), (40, 0, EASE_OUT), (42, 70, EASE_OUT), (52, 0, HOLD),
              (75, 0, EASE_OUT), (77, 70, EASE_OUT), (88, 0)])
comp.layer("flash", [group([hexagon(IN), fill("#FFFFFF")], "flash")], parent=par, opacity=flash)
comp.layer("sheen", [group([hexagon(IN), gradient_fill(
    [(0, "#FFFFFF", 0.0), (0.2, "#FFFFFF", 0.04), (0.5, "#FFFFFF", 0.20), (0.8, "#FFFFFF", 0.04),
     (1, "#000000", 0.18)], (0, CY - HH), (0, CY + HH))], "sheen")], parent=par)
comp.layer("correct", [group([hexagon(IN), fill(slot="accent")], "fill")], parent=par,
           opacity=anim([(0, 0, HOLD), (75, 100, HOLD), (79, 0, HOLD), (83, 100, HOLD), (87, 0, HOLD),
                         (91, 100, HOLD), (F, 100)]))
comp.layer("selected", [group([hexagon(IN), fill(slot="secondary")], "fill")], parent=par,
           opacity=anim([(0, 0, HOLD), (40, 0, EASE_OUT), (42, 100, HOLD), (F, 100)]))
comp.layer("base", [group([hexagon(IN), fill(slot="primary")], "fill")], parent=par)
comp.layer("gold pin", [group([hexagon(6.5), gradient_fill(GOLD, (0, CY - HH), (0, CY + HH))], "gold")],
           parent=par)
comp.layer("silver", [group([hexagon(1.5), gradient_fill(SILVER, (0, CY - HH), (0, CY + HH))], "silver")],
           parent=par)
comp.layer("edge", [group([hexagon(0), fill("#2B3140")], "edge")], parent=par)

for side, (a, b) in {"left": (X0 + 2, 6), "right": (X1 - 2, W - 6)}.items():
    comp.layer(f"line {side}", [
        group([polyline([(a, CY), (b, CY)]), stroke("#DDE3EA", 5, cap="butt"),
               trim(end=anim([(8, 0, SNAP_OUT), (22, 100)]))], "line"),
        group([polyline([(a, CY + 1.5), (b, CY + 1.5)]), stroke("#6B7482", 2, cap="butt"),
               trim(end=anim([(8, 0, SNAP_OUT), (22, 100)]))], "line shade"),
    ])

finish(comp, "broadcast", "game-show-answer-lozenge", "Game Show Answer Lozenge",
       "Quiz-show answer bar with hexagon ends, metallic border and connector lines. Animates in, "
       "lights up orange when selected, then flashes green for the correct answer.",
       ["quiz", "game show", "answer", "trivia", "millionaire", "lozenge"], "intro-hold",
       text_area=[240, 44, 920, 92], thumb_t=0.5)
