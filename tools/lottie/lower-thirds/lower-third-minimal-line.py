from _common import *

W, H = 790, 200
LX, LY0, LY1 = 26, 30, 170       # accent line
PX, PY, PW, PH = 34, 40, 720, 120  # plate
DIV_Y = 106

comp = Comp("lower-third-minimal-line", W, H, fps=FPS, frames=FRAMES)
comp.slot("accent", "#E8B04B")
comp.slot("background", "#0E1116")
comp.slot("secondary", "#FFFFFF")

comp.layer("line", [
    polyline([(LX, LY0), (LX, LY1)]),
    stroke(slot="accent", width=4, cap="butt"),
    trim(start=keys((0, 0, HOLD), (134, 0, EXPO_IN), (148, 100)),
         end=keys((0, 0, EXPO_OUT), (18, 100))),
])

comp.layer("divider", [
    polyline([(PX + 30, DIV_Y), (PX + 330, DIV_Y)]),
    stroke(slot="secondary", width=1.5, opacity=35, cap="butt"),
    trim(start=keys((0, 0, HOLD), (120, 0, INOUT), (132, 100)),
         end=keys((0, 0, HOLD), (24, 0, EXPO_OUT), (46, 100))),
])

comp.layer("plate-matte", [rect((PW, PH), (PW / 2, PH / 2)), fill("#FFFFFF")],
           anchor=(0, 0), position=(PX, PY),
           scale=io([0, 100], [100, 100], 10, 38, 122, 140, EXPO_OUT, INOUT))
comp.layer("plate", [rect((PW, PH), (PW / 2, PH / 2)), fill(slot="background", opacity=60)],
           matte="alpha", anchor=(0, 0),
           position=io([PX - 60, PY], [PX, PY], 10, 40, 122, 140, EXPO_OUT, INOUT))

build(comp, "lower-third-minimal-line", "Minimal Line Lower Third",
      "Elegant minimal lower third: a thin accent line draws on, then a translucent plate reveals beside it.",
      ["lower third", "name", "title", "minimal", "elegant", "line", "clean"],
      {"name": [PX + 30, PY + 12, PW - 60, 50], "subtitle": [PX + 30, DIV_Y + 10, PW - 60, 34]},
      thumb_t=0.5, bg="e8e8ee", intro_end=46)
