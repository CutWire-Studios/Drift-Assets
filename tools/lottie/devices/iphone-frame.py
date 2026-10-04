import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

TITANIUM = dict(sw=720, sh=1560, rs=96, bt=14, bs=14, bb=14, band=9, rim="#4B4B50",
                buttons=[(260, 70, "l"), (360, 110, "l"), (500, 110, "l"), (400, 170, "r")])
NOTCH = dict(sw=720, sh=1560, rs=88, bt=14, bs=14, bb=14, band=9, rim="#B8B8BE",
             buttons=[(240, 60, "l"), (330, 100, "l"), (460, 100, "l"), (380, 160, "r")])
HOME = dict(sw=680, sh=1210, rs=14, bt=170, bs=34, bb=170, band=9, rim="#D9D9DE", cam="home",
            buttons=[(190, 60, "l"), (270, 90, "l"), (370, 90, "l"), (300, 140, "r")])


def island_status(sx, sy, sw, sh):
    out = [group([rect_tl(sx + sw / 2 - 110, sy + sh - 28, 220, 9, 4.5), fill(slot="icon")], "home-indicator")]
    base = sy + 62
    out += [time_text("9:41", sx + 78, base, 32, 600)]
    b, bw = battery(sx + sw - 68 - 46, base - 22, 46, 22, 0.8)
    wf, _ = wifi(sx + sw - 68 - 46 - 36, base, 32)
    cb, _ = cell_bars(sx + sw - 68 - 46 - 36 - 16 - 20 - 34, base, 22)
    return out + b + wf + cb


vs = []
for vid, nm, spec, cam, orient, status, desc in (
        ("island", "Dynamic Island", TITANIUM, "island", "portrait", None,
         "Modern iPhone with a Dynamic Island, titanium rim and side buttons."),
        ("island-status", "Island + Status Bar", TITANIUM, "island", "portrait", island_status,
         "Dynamic Island iPhone with 9:41, signal, Wi-Fi, battery and the home indicator drawn on the screen."),
        ("island-landscape", "Island, Landscape", TITANIUM, "island", "landscape", None,
         "The Dynamic Island iPhone turned sideways for horizontal video."),
        ("notch", "Notch", NOTCH, "notch", "portrait", None, "iPhone X-to-14 style with a notch and a silver rim."),
        ("home-button", "Home Button", HOME, "home", "portrait", None,
         "Classic iPhone with a home button, speaker slot and front camera.")):
    spec = dict(spec, cam=cam)
    c, scr = phone_variant("iphone-frame", spec, orient, status)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "iphone-frame", "iPhone Frame",
            "iPhone mockup that pops in with a real screen cut-out for your video: Dynamic Island, with status bar, "
            "landscape, notch and home-button models.",
            ["iphone", "apple", "ios", "phone", "mockup", "frame", "device", "smartphone", "dynamic island", "screen recording"], vs)
