import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

W, H = 1080, 120


def modern(F=60):
    comp = Comp("ios-status-bar", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    base = 76
    sh = [time_text("9:41", 96, base, 44, 600)]
    x = W - 88
    b, bw = battery(x - 62, base - 30, 62, 30, 0.8)
    sh += b
    x = x - 62 - 30
    wf, ww = wifi(x - 20, base, 44)
    sh += wf
    cb, cw = cell_bars(x - 44 - 24 - 44, base, 30)
    sh += cb
    comp.layer("bar", sh, position=Anim([(0, [0, -30], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 10))
    return comp


def classic(F=60):
    comp = Comp("ios-status-bar", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    base = 72
    sh = []
    cb, cw = cell_bars(24, base, 26, filled=4)
    sh += cb
    for i in range(1):
        pass
    sh += [label("Carrier", 24 + cw + 14, base, 28, 500)]
    wf, ww = wifi(24 + cw + 14 + text_width("Carrier", 28, 500) + 40, base, 36)
    sh += wf
    sh += [time_text("9:41", W / 2, base, 30, 600, "c")]
    b, bw = battery(W - 24 - 50 - 16, base - 24, 50, 24, 1.0)
    sh += b
    sh += [label("100%", W - 24 - 50 - 16 - 14, base, 26, 500, anchor="r")]
    comp.layer("bar", sh, position=Anim([(0, [0, -30], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 10))
    return comp


build_asset(CAT, "ios-status-bar", "iPhone Status Bar",
            "iPhone status bar with time, signal bars, Wi-Fi and battery. 'Modern' is the notch/Dynamic Island layout "
            "(time left, icons right); 'Classic' is the home-button layout with carrier, centred time and battery "
            "percentage. Slides in from the top; place it over a phone screen recording.",
            ["status bar", "iphone", "ios", "battery", "wifi", "time", "9:41", "phone", "screen recording"], [
    Variant("modern", "Notch / Island", modern(), "intro-hold", thumb_t=0.95, bg="1c1c22",
            region=(0, 0, W, H), pad=0.03),
    Variant("classic", "Home Button", classic(), "intro-hold", thumb_t=0.95, bg="1c1c22",
            region=(0, 0, W, H), pad=0.03),
])
