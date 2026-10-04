import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"

W, H = 240, 150


def bars_comp():
    comp = Comp("cellular-signal", W, H, frames=75)
    comp.slot("icon", "#FFFFFF")
    comp.layer("bars", signal_bars(34, 118, n=4, bar_w=34, gap=14, h0=34, step=24, t0=4, stagger=6, r=8))
    return comp


def dots_comp():
    comp = Comp("cellular-signal", W, H, frames=75)
    comp.slot("icon", "#FFFFFF")
    sh = []
    for i in range(5):
        cx = 30 + i * 45
        t = 4 + i * 5
        sh.append(group([ellipse((30, 30), (cx, 75)), fill(slot="icon", opacity=30 if i == 4 else 100)], f"dot{i}",
                        anchor=(cx, 75), position=(cx, 75),
                        scale=Anim([(t, [0, 0], OVERSHOOT), (t + 9, [100, 100])])))
    comp.layer("dots", sh)
    return comp


def searching():
    F = 60
    comp = Comp("cellular-signal", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    sh = []
    for i in range(4):
        h = 34 + 24 * i
        x = 34 + i * 48
        on = Anim([(0, 28, HOLD), (6 + 11 * i, 100, HOLD), (52, 28, HOLD), (F, 28)])
        sh.append(group([rect_tl(x, 118 - h, 34, h, 8), fill(slot="icon")], f"bar{i}", opacity=on))
    comp.layer("bars", sh)
    return comp


build_asset(CAT, "cellular-signal", "Cellular Signal Bars",
            "Phone reception indicator: four rising bars that pop up, the older five-dot style, or a looping "
            "searching sweep.",
            ["signal", "cellular", "reception", "bars", "dots", "status bar", "phone", "network"], [
    Variant("bars", "Rising Bars", bars_comp(), "intro-hold", thumb_t=0.95, bg="6a7087"),
    Variant("dots", "Dots", dots_comp(), "intro-hold", thumb_t=0.95, bg="6a7087"),
    Variant("searching", "Searching", searching(), "loop", thumb_t=0.35, bg="6a7087"),
])
