import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 75


def base():
    comp = Comp("touch-gesture", 300, 520, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#3D8BFF")
    return comp


def dot(cx, cy, d=84):
    return [group([ellipse((d, d), (cx, cy)), fill(slot="icon", opacity=55)], "touch"),
            group([ellipse((d, d), (cx, cy)), stroke(slot="icon", width=4, opacity=90)], "touch-edge")]


def tap():
    c = base()
    cx, cy = 150, 260
    c.layer("ripple", [group([ellipse((220, 220), (cx, cy)), stroke(slot="accent", width=8)], "r", anchor=(cx, cy), position=(cx, cy),
                             scale=Anim([(10, [20, 20], EASE_OUT), (40, [100, 100])]), opacity=Anim([(0, 0, HOLD), (10, 90, EASE_OUT), (40, 0)]))])
    c.layer("finger", dot(cx, cy), anchor=(cx, cy), position=(cx, cy),
            scale=Anim([(0, [0, 0], OVERSHOOT), (8, [100, 100], EASE_IN), (10, [78, 78], EASE_OUT), (18, [100, 100]), (F - 10, [100, 100], EASE_IN), (F, [0, 0])]))
    return c


def double_tap():
    c = base()
    cx, cy = 150, 260
    for k, t in enumerate((8, 26)):
        c.layer(f"ripple{k}", [group([ellipse((220, 220), (cx, cy)), stroke(slot="accent", width=8)], "r", anchor=(cx, cy), position=(cx, cy),
                                     scale=Anim([(t, [20, 20], EASE_OUT), (t + 26, [100, 100])]), opacity=Anim([(0, 0, HOLD), (t, 90, EASE_OUT), (t + 26, 0)]))])
    c.layer("finger", dot(cx, cy), anchor=(cx, cy), position=(cx, cy),
            scale=Anim([(0, [0, 0], OVERSHOOT), (6, [100, 100], EASE_IN), (8, [78, 78], EASE_OUT), (14, [100, 100], EASE_IN), (26, [78, 78], EASE_OUT),
                        (32, [100, 100]), (F - 10, [100, 100], EASE_IN), (F, [0, 0])]))
    return c


def swipe_up():
    c = base()
    cx = 150
    trail = [group([polyline([(cx, 420), (cx, 110)]), stroke(slot="icon", width=70, opacity=22),
                    trim(Anim([(8, 100, LINEAR), (40, 0)]) if False else 0, Anim([(8, 0, EASE_IN_OUT), (40, 100)]))], "trail")]
    c.layer("finger", dot(cx, 0), position=Anim([(0, [0, 420], HOLD), (8, [0, 420], EASE_IN_OUT), (40, [0, 110], HOLD), (F, [0, 110])]),
            scale=Anim([(0, [0, 0], OVERSHOOT), (8, [100, 100]), (F - 10, [100, 100], EASE_IN), (F, [0, 0])]))
    c.layer("chev", [group([polyline([(cx - 26, 70), (cx, 40), (cx + 26, 70)]), stroke(slot="icon", width=8)], "chev")],
            opacity=Anim([(36, 0, EASE_OUT), (44, 90, HOLD), (F - 14, 90, EASE_IN), (F - 4, 0)]))
    return c


def long_press():
    c = base()
    cx, cy = 150, 260
    c.layer("progress", [group([ellipse((190, 190), (cx, cy)), stroke(slot="accent", width=10), trim(0, Anim([(10, 0, EASE_IN_OUT), (50, 100)])),],
                                "arc", rotation=-90, anchor=(cx, cy), position=(cx, cy))])
    c.layer("finger", dot(cx, cy), anchor=(cx, cy), position=(cx, cy),
            scale=Anim([(0, [0, 0], OVERSHOOT), (8, [100, 100], EASE_IN), (10, [88, 88], EASE_OUT), (F - 10, [88, 88], EASE_IN), (F, [0, 0])]))
    return c


build_asset(CAT, "touch-gesture", "Touch Gestures",
            "Finger-touch indicators for phone tutorials: a tap with a ripple, a double tap, a swipe up with a trail "
            "and a long press that fills a progress ring.",
            ["tap", "touch", "swipe", "gesture", "finger", "mobile", "tutorial", "long press", "screen recording"], [
    Variant("tap", "Tap", tap(), "intro-hold", thumb_t=0.45, bg="6a7087"),
    Variant("double-tap", "Double Tap", double_tap(), "intro-hold", thumb_t=0.45, bg="6a7087"),
    Variant("swipe-up", "Swipe Up", swipe_up(), "intro-hold", thumb_t=0.4, bg="6a7087"),
    Variant("long-press", "Long Press", long_press(), "intro-hold", thumb_t=0.6, bg="6a7087")])
