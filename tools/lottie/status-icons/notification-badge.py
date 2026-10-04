import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

BELL = ("M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68"
        "C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z")


def wiggle(t, a=10):
    return [(t, 0, EASE_IN_OUT), (t + 4, -a, EASE_IN_OUT), (t + 8, a, EASE_IN_OUT), (t + 12, -a / 2, EASE_IN_OUT),
            (t + 16, 0, EASE_IN_OUT)]


def bubble(wide, F=75):
    comp = Comp("notification-badge", 240 if wide else 200, 200, frames=F)
    comp.slot("primary", "#FF3B30")
    comp.slot("icon", "#FFFFFF")
    w, h = (170, 86) if wide else (96, 96)
    cx, cy = comp.w / 2, 100
    comp.layer("badge", [group([rect((w, h), (cx, cy), h / 2), fill(slot="primary")], "badge")], anchor=(cx, cy),
               position=(cx, cy), scale=Anim([(0, [0, 0], OVERSHOOT), (14, [100, 100])]))
    return comp, (cx - w / 2 + 14, cy - h / 2 + 12, w - 28, h - 24)


def on_bell(F=75):
    comp = Comp("notification-badge", 300, 300, frames=F)
    comp.slot("primary", "#FF3B30")
    comp.slot("icon", "#FFFFFF")
    comp.layer("badge", [group([ellipse((76, 76), (212, 82)), fill(slot="primary")], "badge")], anchor=(212, 82),
               position=(212, 82), scale=Anim([(14, [0, 0], OVERSHOOT), (26, [100, 100])]))
    comp.layer("bell", [group(icon(BELL, 190, (140, 160)) + [fill(slot="icon")], "bell")], anchor=(140, 80),
               position=(140, 80), rotation=Anim(wiggle(2, 14) + [(F, 0)]))
    return comp, (176, 52, 72, 60)


b1, a1 = bubble(False)
b2, a2 = bubble(True)
b3, a3 = on_bell()
build_asset(CAT, "notification-badge", "Notification Badge",
            "Red unread-count badge that pops in: a round bubble, a wide pill for big counts, and one stuck to a "
            "wiggling bell. Type the number in the text area.",
            ["notification", "badge", "unread", "count", "alert", "red dot", "bell", "inbox"], [
    Variant("bubble", "Bubble", b1, "intro-hold", text_area=a1, thumb_t=0.95, bg="e8e8ee"),
    Variant("pill", "Pill", b2, "intro-hold", text_area=a2, thumb_t=0.95, bg="e8e8ee"),
    Variant("bell", "On a Bell", b3, "intro-hold", text_area=a3, thumb_t=0.95, bg="6a7087"),
])
