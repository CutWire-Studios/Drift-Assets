import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

PIN = ("M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5"
       " 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z")


def drop():
    F = 75
    comp = Comp("location-pin", 320, 380, frames=F)
    comp.slot("primary", "#FF3B30")
    comp.slot("icon", "#FFFFFF")
    comp.layer("ripple", [group([ellipse((190, 60), (160, 330)), stroke(slot="primary", width=6)], "r",
                                anchor=(160, 330), position=(160, 330),
                                scale=Anim([(16, [20, 20], EASE_OUT), (44, [100, 100])]),
                                opacity=Anim([(16, 80, EASE_OUT), (44, 0)]))])
    s = 230 / 24
    pin = svg_shapes(PIN, s, (160 - 12 * s, 0))
    comp.layer("pin", [group(pin + [fill(slot="primary")], "pin")], anchor=(160, 22 * s), position=Anim([
        (0, [160, -200 + 22 * s], EASE_IN), (14, [160, 330], HOLD), (14, [160, 330], EASE_OUT), (20, [160, 300], EASE_IN),
        (26, [160, 330], HOLD), (F, [160, 330])]),
        scale=Anim([(0, [100, 100], HOLD), (13, [100, 100], EASE_OUT), (14, [118, 78], EASE_OUT), (19, [92, 108], EASE_IN_OUT),
                    (26, [100, 100])]))
    comp.layer("shadow", [group([ellipse((120, 26), (160, 330)), fill("#000000", 28)], "shadow")],
               anchor=(160, 330), position=(160, 330),
               scale=Anim([(0, [20, 20], EASE_IN), (14, [100, 100], EASE_OUT), (20, [80, 80], EASE_IN), (26, [100, 100])]))
    return comp


def pulse():
    F = 60
    comp = Comp("location-pin", 320, 380, frames=F)
    comp.slot("primary", "#2F80FF")
    comp.slot("icon", "#FFFFFF")
    cx, cy = 160, 190
    comp.layer("dot", [group([ellipse((70, 70), (cx, cy)), fill(slot="primary")], "dot"),
                       group([ellipse((92, 92), (cx, cy)), fill(slot="icon")], "ring"),
                       ])
    comp.layer("accuracy", [group([ellipse((300, 300), (cx, cy)), fill(slot="primary", opacity=22)], "acc",
                                  anchor=(cx, cy), position=(cx, cy),
                                  scale=Anim([(0, [60, 60], EASE_IN_OUT), (30, [100, 100], EASE_IN_OUT), (F, [60, 60])]))])
    comp.layer("ring2", [group([ellipse((300, 300), (cx, cy)), stroke(slot="primary", width=4)], "r2",
                               anchor=(cx, cy), position=(cx, cy),
                               scale=Anim([(0, [30, 30], EASE_OUT), (F, [100, 100])]),
                               opacity=Anim([(0, 80, EASE_OUT), (F, 0)]))])
    return comp


build_asset(CAT, "location-pin", "Location Pin",
            "Map location marker: a pin that drops in, squashes and ripples, or the blue 'you are here' dot with a "
            "pulsing accuracy circle.",
            ["location", "map", "pin", "gps", "marker", "place", "travel", "maps"], [
    Variant("drop", "Pin Drop", drop(), "intro-hold", thumb_t=0.95, bg="e8e8ee"),
    Variant("pulse", "You Are Here", pulse(), "loop", thumb_t=0.3, bg="e8e8ee"),
])
