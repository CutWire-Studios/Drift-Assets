import math
from _common import *

W, H = 820, 280
CX, CY = 405, 135
PW, PH, R = 680, 170, 34
OUT = 6
SH = 14

comp = Comp("title-plate-bold", W, H, fps=FPS, frames=FRAMES)
comp.slot("primary", "#FFD23F")
comp.slot("secondary", "#1B1B2F")
comp.slot("accent", "#FF5A5F")

# sparks off the top-left corner
corner = (CX - PW / 2 + 6, CY - PH / 2 + 6)
sparks = []
for i, ang in enumerate((200, 225, 250)):
    a = math.radians(ang)
    p0 = (corner[0] + math.cos(a) * 24, corner[1] + math.sin(a) * 24)
    p1 = (corner[0] + math.cos(a) * 52, corner[1] + math.sin(a) * 52)
    sparks.append(polyline([p0, p1], name=f"spark{i}"))
comp.layer("sparks", sparks + [
    stroke(slot="accent", width=7, cap="round"),
    trim(start=keys((0, 0, HOLD), (18, 0, EXPO_OUT), (32, 100, HOLD), (34, 0)),
         end=keys((0, 0, HOLD), (14, 0, EXPO_OUT), (24, 100))),
], ip=0, op=34)

rig = comp.null("rig", anchor=(0, 0), position=(CX, CY),
                scale=keys((0, [0, 0], (0.3, 0.9, 0.5, 1)), (8, [112, 112], EASE_IN_OUT),
                           (13, [96, 96], EASE_IN_OUT), (18, [101.5, 101.5], EASE_IN_OUT),
                           (23, [100, 100], HOLD), (120, [100, 100], EASE_OUT),
                           (126, [106, 106], (0.6, 0, 0.9, 0.4)), (136, [0, 0])),
                rotation=keys((0, -7, (0.3, 0.9, 0.4, 1)), (18, 0, HOLD), (126, 0, EASE_IN), (136, 5)))

plate = [rect((PW, PH), roundness=R), fill(slot="primary"), stroke(slot="secondary", width=OUT, join="round")]
comp.layer("plate", plate, parent=rig)
comp.layer("shadow", [rect((PW, PH), roundness=R), fill(slot="secondary"),
                      stroke(slot="secondary", width=OUT, join="round")], parent=rig,
           position=keys((0, [0, 0], HOLD), (9, [0, 0], OVERSHOOT), (20, [SH, SH], HOLD),
                         (120, [SH, SH], EASE_IN), (127, [0, 0])))

build(comp, "title-plate-bold", "Bold Title Plate",
      "Chunky rounded title plate with an offset drop shadow that pops in with overshoot; for section titles.",
      ["title", "section", "plate", "bold", "pop", "chapter", "badge"],
      {"title": [CX - PW / 2 + 40, CY - PH / 2 + 28, PW - 80, PH - 56]},
      thumb_t=0.5, bg="e8e8ee", intro_end=24)
