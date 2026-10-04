import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *


def monitor(kind, F=60):
    M = 40
    sw, sh = 1600, 900
    if kind == "studio":
        bez, chin, band, rim = 16, 16, 6, "#C9CBD0"
    elif kind == "imac":
        bez, chin, band, rim = 24, 120, 0, "#E8E8EC"
    else:
        bez, chin, band, rim = 8, 8, 8, "#1A1A1F"
    bw, bh = sw + 2 * (bez + band), sh + bez + band * 2 + chin
    stand_h = 260
    W, H = bw + 2 * M + 80, bh + 2 * M + stand_h
    comp = device_comp("monitor-frame", W, H, F)
    comp.slot("primary", rim)
    comp.slot("secondary", "#0A0A0C")
    comp.slot("accent", "#2F6BFF" if kind == "imac" else "#8E9096")
    bx, by = (W - bw) / 2, M
    sx, sy = bx + band + bez, by + band + bez
    cx = W / 2
    screen = rrect_path(sx, sy, sw, sh, 8, 8, 8, 8, "screen")
    bez_out = (sx - bez, sy - bez, sw + 2 * bez, sh + bez + chin)
    shapes = []
    sy_b = by + bh
    if kind == "gaming":
        shapes += [group(rrect_path(cx - 60, sy_b - 4, 120, stand_h - 40) + [fill(slot="primary")], "neck"),
                   group(polyline([(cx - 230, sy_b + stand_h), (cx, sy_b + stand_h - 90), (cx + 230, sy_b + stand_h)], closed=False) and
                         [polyline([(cx - 240, sy_b + stand_h), (cx - 30, sy_b + stand_h - 60), (cx + 30, sy_b + stand_h - 60), (cx + 240, sy_b + stand_h)], closed=True), fill(slot="primary")], "foot")]
    elif kind == "studio":
        shapes += [group(rrect_path(cx - 90, sy_b - 4, 180, stand_h - 36, 0, 0, 10, 10) + [fill(slot="primary")], "neck"),
                   group(rrect_path(cx - 190, sy_b + stand_h - 40, 380, 16, 8, 8, 8, 8) + [fill(slot="primary")], "foot")]
    else:
        shapes += [group(rrect_path(cx - 70, sy_b - 4, 140, stand_h - 30, 0, 0, 0, 0) + [fill(slot="primary")], "neck"),
                   group(rrect_path(cx - 170, sy_b + stand_h - 34, 340, 22, 11, 11, 11, 11) + [fill(slot="primary")], "foot")]
    if kind == "imac":
        shapes.append(group([ellipse((12, 12), (cx, by + bez / 2 + 1)), fill("#1F1F24")], "cam"))
    shapes.append(group(rrect_path(*bez_out, 16, 16, 16 if kind != "imac" else 0, 16 if kind != "imac" else 0, "bez-out") + screen +
                        [fill(slot="secondary", even_odd=True)], "bezel"))
    body = (bx, by, bw, bh)
    out_r = 24
    shapes.append(group(rrect_path(*body, out_r, out_r, out_r, out_r, "out") + rrect_path(*bez_out, 16, 16, 16 if kind != "imac" else 0, 16 if kind != "imac" else 0, "in") +
                        [fill(slot="primary", even_odd=True)], "shell") if band else group([], "none"))
    if kind == "imac":
        shapes.append(group(rrect_path(bx, sy + sh + 0, bw, chin + band * 0 + bez - 0 + 0, 0, 0, 24, 24, "chin") + [fill(slot="accent", opacity=0)], "chin-tint"))
    finish_device(comp, shapes, body, out_r, screen)
    return comp, (sx, sy, sw, sh)


vs = []
for vid, nm, desc in (("studio", "Studio Display", "Slim-bezel desktop display on an aluminium stand."),
                      ("imac", "All-in-One", "All-in-one desktop with a thick chin and a stand."),
                      ("gaming", "Gaming Monitor", "Near-borderless dark monitor on a wide V-stand.")):
    c, scr = monitor(vid)
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "monitor-frame", "Desktop Monitor Frame",
            "Desktop monitor mockup with a real screen cut-out for your video: a slim-bezel studio display, an "
            "all-in-one desktop with a chin, and a borderless gaming monitor.",
            ["monitor", "display", "desktop", "imac", "pc", "mockup", "frame", "device", "screen recording"], vs)
