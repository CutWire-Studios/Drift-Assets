from _common import *

W, H, F = 1920, 1080, 30
comp = Comp("rec-camera-frame", W, H, fps=30, frames=F)
comp.slot("icon", "#FFFFFF")
comp.slot("primary", "#F0201B")

M, ARM, SW = 90, 170, 10
brackets = [
    [(M, M + ARM), (M, M), (M + ARM, M)],
    [(W - M - ARM, M), (W - M, M), (W - M, M + ARM)],
    [(W - M, H - M - ARM), (W - M, H - M), (W - M - ARM, H - M)],
    [(M + ARM, H - M), (M, H - M), (M, H - M - ARM)],
]
cx, cy = W / 2, H / 2
cross = [[(cx - 70, cy), (cx - 22, cy)], [(cx + 22, cy), (cx + 70, cy)],
         [(cx, cy - 70), (cx, cy - 22)], [(cx, cy + 22), (cx, cy + 70)]]

bx, by, bw, bh = 1680, 170, 104, 50  # battery centre / size


def hud(color, slot=None):
    g = [group([*(polyline(p) for p in brackets), stroke(color, SW, slot=slot, cap="butt", join="miter")],
               "brackets"),
         group([*(polyline(p) for p in cross), stroke(color, 5, slot=slot, cap="butt")], "crosshair"),
         group([ellipse((10, 10), (cx, cy)), fill(color, slot=slot)], "centre"),
         group([rect((bw, bh), (bx, by), 7), stroke(color, 5, slot=slot)], "battery"),
         group([rect((10, 22), (bx + bw / 2 + 7, by), 3), fill(color, slot=slot)], "terminal")]
    for i in range(3):
        g.append(group([rect((24, 32), (bx - 31 + i * 31, by), 2), fill(color, slot=slot)], f"cell{i}"))
    return g


blink = anim([(0, 100, HOLD), (14, 100, EASE_IN_OUT), (17, 0, HOLD), (27, 0, EASE_IN_OUT), (F, 100)])
comp.layer("rec dot", [group([ellipse((52, 52), (200, 170)), fill(slot="primary")], "dot")], opacity=blink)
comp.layer("hud", hud("#FFFFFF", "icon"))
comp.layer("rec dot shadow", [group([ellipse((52, 52), (203, 173)), fill("#000000", 35)], "dot")],
           opacity=blink)
comp.layer("hud shadow", hud("#000000"), position=(3, 3), opacity=35)

finish(comp, "broadcast", "rec-camera-frame", "REC Camera Frame",
       "Camcorder viewfinder overlay: corner brackets, blinking red REC dot, battery and crosshair. "
       "Add REC next to the dot with the text tool.",
       ["rec", "camera", "camcorder", "viewfinder", "recording", "overlay"], "loop",
       text_area=[240, 138, 260, 64], thumb_t=0.1)
