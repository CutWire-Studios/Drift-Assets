import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *


def watch(band_on, F=60):
    M = 30
    sw, sh, rs = 396, 484, 78
    bez, case = 14, 16
    cw, ch = sw + 2 * (bez + case), sh + 2 * (bez + case)
    strap_h = 300 if band_on else 0
    W, H = cw + 2 * M + 30, ch + 2 * M + 2 * strap_h
    comp = device_comp("apple-watch-frame", W, H, F)
    comp.slot("primary", "#C5C7CC")      # case
    comp.slot("secondary", "#050506")     # bezel
    comp.slot("accent", "#2E2E33")        # strap
    cx0, cy0 = (W - cw) / 2 - 12, M + strap_h
    sx, sy = cx0 + case + bez, cy0 + case + bez
    screen = rrect_path(sx, sy, sw, sh, rs, rs, rs, rs, "screen")
    bez_out = (sx - bez, sy - bez, sw + 2 * bez, sh + 2 * bez)
    shapes = [
        group([rect_tl(cx0 + cw - 2, cy0 + 150, 20, 76, 10), fill(slot="primary")], "crown"),
        group([rect_tl(cx0 + cw - 2, cy0 + 260, 10, 90, 5), fill(slot="primary")], "button"),
        group(rrect_path(*bez_out, rs + bez, rs + bez, rs + bez, rs + bez, "bez-out") + screen + [fill(slot="secondary", even_odd=True)], "bezel"),
        group(rrect_path(cx0, cy0, cw, ch, rs + bez + case, rs + bez + case, rs + bez + case, rs + bez + case, "case-out") +
              rrect_path(*bez_out, rs + bez, rs + bez, rs + bez, rs + bez, "case-in") + [fill(slot="primary", even_odd=True)], "case"),
    ]
    if band_on:
        sw2 = cw - 70
        sxx = cx0 + 35
        shapes += [group(rrect_path(sxx, cy0 + ch - 20, sw2, strap_h + 20, 0, 0, 26, 26, "strap-b") + [fill(slot="accent")], "strap-bottom"),
                   group(rrect_path(sxx, cy0 - strap_h + 20, sw2, strap_h, 26, 26, 0, 0, "strap-t") + [fill(slot="accent")], "strap-top")]
        # straps sit behind the case
        shapes = shapes[:2] + shapes[4:] + shapes[2:4]
        # holes for the strap pegs are not drawn; the case overlaps the strap ends
    body = (cx0, cy0, cw, ch)
    finish_device(comp, shapes, body, rs + bez + case, screen, spread=26, dy=16)
    return comp, (sx, sy, sw, sh)


vs = []
for vid, nm, band, desc in (("case", "Case Only", False, "Watch case with a digital crown and side button."),
                            ("strap", "With Strap", True, "Watch with a strap above and below.")):
    c, scr = watch(band)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "apple-watch-frame", "Smartwatch Frame",
            "Smartwatch mockup with a real screen cut-out for a watch-face recording, with or without the strap.",
            ["apple watch", "smartwatch", "wearable", "watch", "mockup", "frame", "device"], vs)
