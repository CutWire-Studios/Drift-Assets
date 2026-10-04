import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *
from os_icons import *

CAT = "status-icons"

W, H = 1080, 100


def dot_icons(x, base, n, r=9, slot="icon"):
    return [group([ellipse((r * 2, r * 2), (x + i * (r * 2 + 14), base - 15)), fill(slot=slot, opacity=85)], f"n{i}")
            for i in range(n)]


def pixel(F=60):
    comp = Comp("android-status-bar", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    base = 64
    sh = [time_text("12:30", 56, base, 36, 500)]
    sh += dot_icons(220, base, 3)
    x = W - 56
    b, bw = battery(x - 30, base - 28, 30, 28, 0.7)
    sh += b
    # slanted signal triangle + wifi wedge
    tx = x - 30 - 34 - 30
    sh += [group([polyline([(tx, base), (tx + 28, base), (tx + 28, base - 28)], closed=True), fill(slot="icon")], "signal")]
    wf, ww = wifi(tx - 52, base, 40)
    sh += wf
    comp.layer("bar", sh, position=Anim([(0, [0, -30], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 10))
    return comp


def samsung(F=60):
    comp = Comp("android-status-bar", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    base = 64
    sh = [time_text("12:30", 56, base, 36, 500)]
    sh += dot_icons(212, base, 2, r=8)
    x = W - 56
    b, bw = battery(x - 40, base - 26, 40, 26, 0.7)
    sh += b
    sh += [label("70%", x - 40 - 16, base, 28, 500, anchor="r")]
    cb, cw = cell_bars(x - 40 - 16 - 62 - 88, base, 28)
    sh += cb
    wf, ww = wifi(x - 40 - 16 - 62 - 28, base, 38)
    sh += []
    sh += wf
    comp.layer("bar", sh, position=Anim([(0, [0, -30], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 10))
    return comp


build_asset(CAT, "android-status-bar", "Android Status Bar",
            "Android status bar with time, notification dots, Wi-Fi, signal and battery. 'Pixel' uses the slanted "
            "signal triangle; 'Galaxy' shows signal bars and a battery percentage. Slides in from the top.",
            ["status bar", "android", "pixel", "samsung", "galaxy", "battery", "wifi", "phone", "screen recording"], [
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.95, bg="1c1c22", region=(0, 0, W, H), pad=0.03),
    Variant("galaxy", "Galaxy", samsung(), "intro-hold", thumb_t=0.95, bg="1c1c22", region=(0, 0, W, H), pad=0.03),
])
