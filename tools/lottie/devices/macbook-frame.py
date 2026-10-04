import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *


def macbook(rim, bezel, notch, F=60):
    M = 40
    sw, sh = 1440, 900
    bs, bt, band = bezel, bezel + (6 if notch else 4), 8
    lid_w, lid_h = sw + 2 * (bs + band), sh + bt + bs + 2 * band
    W, H = lid_w + 2 * M + 120, lid_h + 2 * M + 36
    comp = device_comp("macbook-frame", W, H, F)
    comp.slot("primary", rim)
    comp.slot("secondary", "#0A0A0C")
    lx, ly = (W - lid_w) / 2, M
    sx, sy = lx + band + bs, ly + band + bt
    cx = sx + sw / 2
    screen = rrect_path(sx, sy, sw, sh, 6, 6, 6, 6, "screen")
    bez_out = (sx - bs, sy - bt, sw + 2 * bs, sh + bt + bs)
    shapes = []
    if notch:
        shapes.append(group(rrect_path(cx - 110, sy, 220, 34, br=16, bl=16) + [fill(slot="secondary")], "notch"))
    else:
        shapes.append(group([ellipse((10, 10), (cx, sy - bt / 2 + 2)), fill("#1F1F24")], "webcam"))
    shapes.append(group(rrect_path(*bez_out, 22, 22, 6, 6, "bez-out") + screen + [fill(slot="secondary", even_odd=True)], "bezel"))
    lid = (lx, ly, lid_w, lid_h)
    shapes.append(group(rrect_path(*lid, 30, 30, 12, 12, "lid-out") + rrect_path(*bez_out, 22, 22, 6, 6, "lid-in") +
                        [fill(slot="primary", even_odd=True)], "lid"))
    by = ly + lid_h
    base_w = lid_w + 120
    bx = (W - base_w) / 2
    shapes.append(group(rrect_path(cx - 120, by, 240, 12, bl=14, br=14) + [fill("#000000", 18)], "groove-shade"))
    shapes.append(group(rrect_path(bx, by, base_w, 24, 0, 0, 22, 22, "base") + [fill(slot="primary")], "base"))
    shapes.append(group(rrect_path(cx - 110, by, 220, 11, bl=12, br=12) + [fill("#000000", 28)], "groove"))
    body = (lx, ly, lid_w, lid_h + 24)
    finish_device(comp, shapes, body, 30, screen)
    return comp, (sx, sy, sw, sh)


vs = []
for vid, nm, rim, bezel, notch, desc in (
        ("pro", "MacBook Pro", "#5A5B60", 20, True, "Space-grey MacBook Pro with a notch and thin bezels."),
        ("air", "MacBook Air", "#CDCFD3", 22, True, "Silver MacBook Air with a notch."),
        ("classic", "Classic Webcam", "#C9CACE", 34, False, "Older MacBook with thick bezels and a webcam dot.")):
    c, scr = macbook(rim, bezel, notch)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "macbook-frame", "MacBook Frame",
            "MacBook laptop mockup (front view) with a real screen cut-out for your video: Pro, Air and a classic "
            "webcam-bezel model.",
            ["macbook", "laptop", "mac", "apple", "notebook", "mockup", "frame", "device", "screen recording"], vs)
