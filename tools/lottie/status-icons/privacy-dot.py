import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

MIC = "M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"
CAM = "M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"


def dot(F=60):
    comp = Comp("privacy-dot", 200, 200, frames=F)
    comp.slot("primary", "#FF9F0A")
    cx = cy = 100
    comp.layer("dot", [group([ellipse((52, 52), (cx, cy)), fill(slot="primary")], "dot")], anchor=(cx, cy), position=(cx, cy),
               scale=Anim([(0, [100, 100], EASE_IN_OUT), (30, [112, 112], EASE_IN_OUT), (F, [100, 100])]))
    comp.layer("halo", [group([ellipse((52, 52), (cx, cy)), fill(slot="primary", opacity=40)], "halo",
                              anchor=(cx, cy), position=(cx, cy), scale=Anim([(0, [100, 100], EASE_OUT), (F, [320, 320])]),
                              opacity=Anim([(0, 100, EASE_OUT), (F, 0)]))])
    return comp


def chip(F=75):
    comp = Comp("privacy-dot", 300, 160, frames=F)
    comp.slot("primary", "#34C759")
    comp.slot("icon", "#FFFFFF")
    comp.layer("glyph", icon(CAM, 56, (150, 80)) and [group(icon(CAM, 56, (150, 80)) + [fill(slot="icon")], "cam")],
               opacity=fade(8, 16))
    comp.layer("pill", [group([grow_rect(150 - 70, 80 - 34, 140, 68, 0, 12, 34, EXPO_OUT) if False else rect((140, 68), (150, 80), 34),
                               fill(slot="primary")], "pill")],
               anchor=(150, 80), position=(150, 80), scale=Anim([(0, [20, 20], OVERSHOOT), (14, [100, 100])]),
               opacity=Anim([(0, 0, HOLD), (1, 100)]))
    return comp


def mic_chip(F=75):
    comp = Comp("privacy-dot", 300, 160, frames=F)
    comp.slot("primary", "#FF9F0A")
    comp.slot("icon", "#FFFFFF")
    comp.layer("glyph", [group(icon(MIC, 56, (150, 80)) + [fill(slot="icon")], "mic")], opacity=fade(8, 16))
    comp.layer("pill", [group([rect((140, 68), (150, 80), 34), fill(slot="primary")], "pill")],
               anchor=(150, 80), position=(150, 80), scale=Anim([(0, [20, 20], OVERSHOOT), (14, [100, 100])]),
               opacity=Anim([(0, 0, HOLD), (1, 100)]))
    return comp


build_asset(CAT, "privacy-dot", "Mic & Camera Indicator",
            "The recording indicators phones show when the microphone or camera is in use: a pulsing dot (orange by "
            "default, recolour it green for camera), and Android-style capsule chips with a mic or camera glyph.",
            ["microphone", "camera", "privacy", "recording", "indicator", "dot", "orange dot", "green dot", "status bar"], [
    Variant("dot", "Pulsing Dot", dot(), "loop", thumb_t=0.0, bg="1c1c22"),
    Variant("mic-chip", "Mic Chip", mic_chip(), "intro-hold", thumb_t=0.95, bg="1c1c22"),
    Variant("camera-chip", "Camera Chip", chip(), "intro-hold", thumb_t=0.95, bg="1c1c22"),
])
