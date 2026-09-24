from _common import *

W, H = 900, 200
LX, LW = 30, 8
BX = LX + LW
TOP, NH = 40, 78
SUB_Y, SH = TOP + NH, 42
NW, SW = 800, 470
SOFT = (0.25, 0.8, 0.3, 1.0)
AWAY = (0.6, 0.0, 0.9, 0.5)

comp = Comp("reality-confessional-bar", W, H, fps=FPS, frames=FRAMES)
comp.slot("accent", "#FF6F61")
comp.slot("primary", "#FFFFFF")
comp.slot("secondary", "#FF8FA3")

full = SUB_Y + SH - TOP
comp.layer("line", [rect((LW, full), (LW / 2, 0), roundness=LW / 2), fill(slot="accent")],
           anchor=(0, 0), position=(LX, TOP + full / 2),
           scale=io([100, 0], [100, 100], 0, 16, 134, 148, EXPO_OUT, INOUT))


def soft_bar(name, y, w, h, slot, opacity, t0, t2, r):
    comp.layer(f"{name}-clip", [rect((W, h + 4), (BX + W / 2, y + h / 2)), fill("#FFFFFF")])
    comp.layer(name, [rect((w + r, h), (BX + (w - r) / 2, y + h / 2), roundness=r), fill(slot=slot)], matte="alpha",
               position=io([-140, 0], [0, 0], t0, t0 + 26, t2, t2 + 16, SOFT, AWAY),
               opacity=io(0, opacity, t0, t0 + 14, t2 + 4, t2 + 16, EASE_OUT, EASE_IN))


soft_bar("name", TOP, NW, NH, "primary", 86, 5, 124, 14)
soft_bar("sub", SUB_Y, SW, SH, "secondary", 100, 10, 120, SH / 2)

build(comp, "reality-confessional-bar", "Reality Confessional Bar",
      "Reality-TV confessional lower third: a soft semi-transparent white name bar with a coral accent line and pink subtitle plate.",
      ["lower third", "reality tv", "confessional", "name", "interview", "soft", "pink"],
      {"name": [BX + 24, TOP + 10, NW - 48, NH - 20], "subtitle": [BX + 24, SUB_Y + 5, SW - 48, SH - 10]},
      thumb_t=0.5, intro_end=36)
