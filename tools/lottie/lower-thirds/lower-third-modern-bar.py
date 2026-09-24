from _common import *

W, H = 1000, 212
AX, AW = 24, 16            # accent block
TOP, MH = 40, 88           # main bar
SUB_Y, SH = 132, 40        # secondary bar
BX = AX + AW
MW, SW = 920, 600

comp = Comp("lower-third-modern-bar", W, H, fps=FPS, frames=FRAMES)
comp.slot("accent", "#2E7CF6")
comp.slot("primary", "#FFFFFF")
comp.slot("secondary", "#14213D")

full_h = SUB_Y + SH - TOP
cy = TOP + full_h / 2

comp.layer("accent", [rect((AW, full_h), (AW / 2, 0)), fill(slot="accent")],
           anchor=(0, 0), position=(AX, cy),
           scale=keys((0, [0, 100], EXPO_OUT), (8, [420, 100], INOUT), (20, [100, 100], HOLD),
                      (132, [100, 100], INOUT), (140, [420, 100], EXPO_IN), (149, [0, 100])))

comp.layer("main", [rect((MW, MH), (MW / 2, 0)), fill(slot="primary")],
           anchor=(0, 0), position=(BX, TOP + MH / 2),
           scale=io([0, 100], [100, 100], 7, 27, 122, 138, EXPO_OUT, INOUT))

comp.layer("sub", [rect((SW, SH), (SW / 2, 0)), fill(slot="secondary")],
           anchor=(0, 0), position=(BX, SUB_Y + SH / 2),
           scale=io([0, 100], [100, 100], 14, 32, 120, 133, EXPO_OUT, INOUT))

build(comp, "lower-third-modern-bar", "Modern Bar Lower Third",
      "Clean corporate lower third: an accent block wipes in and a name bar and subtitle bar extend from it.",
      ["lower third", "name", "title", "corporate", "youtube", "clean", "bar"],
      {"name": [BX + 24, TOP + 8, MW - 48, MH - 16], "subtitle": [BX + 24, SUB_Y + 4, SW - 48, SH - 8]},
      thumb_t=0.5, intro_end=32)
