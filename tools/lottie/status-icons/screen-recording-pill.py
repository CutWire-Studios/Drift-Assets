import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

def ios(F=75):
    comp = Comp("screen-recording-pill", 330, 130, frames=F)
    comp.slot("primary", "#FF3B30")
    comp.slot("icon", "#FFFFFF")
    cx, cy = 165, 65
    comp.layer("dot", [group([ellipse((18, 18), (62, cy)), fill(slot="icon")], "dot")],
               opacity=Anim([(14, 100, HOLD), (44, 25, EASE_IN_OUT), (F, 100)]))
    comp.layer("pill", [group([rect((230, 72), (cx, cy), 36), fill(slot="primary")], "pill")], anchor=(cx, cy), position=(cx, cy),
               scale=Anim([(0, [30, 30], OVERSHOOT), (14, [100, 100])]), opacity=Anim([(0, 0, HOLD), (1, 100)]))
    return comp, (92, 44, 110, 42)


def android(F=75):
    comp = Comp("screen-recording-pill", 440, 130, frames=F)
    comp.slot("background", "#202124")
    comp.slot("primary", "#FF3B30")
    comp.slot("icon", "#FFFFFF")
    cx, cy = 220, 65
    comp.layer("dot", [group([ellipse((18, 18), (82, cy)), fill(slot="primary")], "dot")],
               opacity=Anim([(14, 100, HOLD), (44, 30, EASE_IN_OUT), (F, 100)]))
    comp.layer("text", [label("Recording", 112, cy + 10, 30, 600)], opacity=fade(10, 20))
    comp.layer("pill", [group([rect((330, 72), (cx, cy), 36), fill(slot="background")], "pill")], anchor=(cx, cy),
               position=(cx, cy), scale=Anim([(0, [30, 30], OVERSHOOT), (14, [100, 100])]), opacity=Anim([(0, 0, HOLD), (1, 100)]))
    return comp, None


c1, a1 = ios()
c2, _ = android()
build_asset(CAT, "screen-recording-pill", "Screen Recording Pill",
            "The red 'screen recording' pill from the iPhone status bar with a blinking dot, and the dark Android "
            "recording chip with its own label.",
            ["screen recording", "rec", "recording", "ios", "android", "status bar", "tutorial", "pill"], [
    Variant("ios", "iPhone Pill", c1, "intro-hold", text_area=a1, thumb_t=0.95, bg="1c1c22"),
    Variant("android", "Android Chip", c2, "intro-hold", thumb_t=0.95, bg="6a7087"),
])
