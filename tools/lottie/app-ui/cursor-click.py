import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 75
ARROW = "M0 0 L0 30 L8 23 L14 36 L20 33 L14 21 L25 21 Z"
HAND = ("M12 2c-1.1 0-2 .9-2 2v8.5l-1.3-1.3c-.8-.8-2.1-.8-2.8 0-.6.6-.7 1.5-.2 2.2l4 6.1c.9 1.4 2.4 2.2 4 2.2h3.3c2.8 0 5-2.2 5-5v-5c0-1.1-.9-2-2-2-.3 0-.6.1-.8.2-.3-.7-1-1.2-1.8-1.2-.4 0-.8.1-1.1.3-.4-.6-1-1-1.8-1-.2 0-.4 0-.5.1V4c0-1.1-.9-2-2-2z")


def cursor(kind):
    W, H = 360, 360
    comp = Comp("cursor-click", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#3D8BFF")
    comp.slot("outline", "#111111")
    tip = (120, 110)
    ring = [group([ellipse((130, 130), tip), stroke(slot="accent", width=8)], "ripple", anchor=tip, position=tip,
                  scale=Anim([(34, [10, 10], EASE_OUT), (60, [100, 100])]), opacity=Anim([(0, 0, HOLD), (34, 90, EASE_OUT), (60, 0)])),
            group([ellipse((130, 130), tip), fill(slot="accent", opacity=25)], "ripple-fill", anchor=tip, position=tip,
                  scale=Anim([(34, [10, 10], EASE_OUT), (60, [100, 100])]), opacity=Anim([(0, 0, HOLD), (34, 90, EASE_OUT), (60, 0)]))]
    if kind == "arrow":
        sh = [group(svg_shapes(ARROW, 4.2, (0, 0)) + [fill(slot="icon")], "arrow"),
              group(svg_shapes(ARROW, 4.2, (0, 0)) + [stroke(slot="outline", width=5, join="round")], "outline")]
        sh = [sh[1], sh[0]]
        sh = [group(svg_shapes(ARROW, 4.2) + [fill(slot="icon"), stroke(slot="outline", width=6, join="round")], "arrow")]
        pos = Anim([(0, [210, 230], EASE_IN_OUT), (28, [tip[0], tip[1]], EASE_IN_OUT), (34, [tip[0] + 3, tip[1] + 3], EASE_OUT), (40, [tip[0], tip[1]], EASE_IN_OUT), (F, [tip[0], tip[1]])])
        sc = Anim([(0, [100, 100], HOLD), (30, [100, 100], EASE_IN), (34, [88, 88], EASE_OUT), (42, [100, 100])])
        comp.layer("cursor", sh, position=pos, scale=sc, anchor=(0, 0))
    else:
        sh = [group(svg_shapes(HAND, 7.6, (-10 * 7.6 / 2, -1.5 * 7.6)) + [fill(slot="icon"), stroke(slot="outline", width=3, join="round")], "hand")]
        pos = Anim([(0, [220, 250], EASE_IN_OUT), (28, [tip[0], tip[1]], EASE_IN_OUT), (F, [tip[0], tip[1]])])
        sc = Anim([(0, [100, 100], HOLD), (30, [100, 100], EASE_IN), (34, [86, 86], EASE_OUT), (42, [100, 100])])
        comp.layer("cursor", sh, position=pos, scale=sc, anchor=(0, 0))
    comp.layer("click", ring)
    return comp


build_asset(CAT, "cursor-click", "Cursor Click",
            "A mouse pointer glides to a spot and clicks, with a ripple at the click point: arrow cursor or "
            "pointing-hand cursor. Drop it over a screen recording to show where to click.",
            ["cursor", "mouse", "click", "pointer", "tutorial", "screen recording", "hand", "tap", "ui"], [
    Variant("arrow", "Arrow", cursor("arrow"), "intro-hold", thumb_t=0.6, bg="6a7087"),
    Variant("hand", "Hand", cursor("hand"), "intro-hold", thumb_t=0.6, bg="6a7087")])
