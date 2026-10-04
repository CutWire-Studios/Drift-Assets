import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *


def flat(F=60):
    M = 40
    sw, sh, bez = 1600, 900, 12
    bw, bh = sw + 2 * bez, sh + 2 * bez + 8
    W, H = bw + 2 * M, bh + 2 * M + 70
    comp = device_comp("tv-frame", W, H, F)
    comp.slot("primary", "#17171B")
    comp.slot("secondary", "#2A2A30")
    bx, by = M, M
    sx, sy = bx + bez, by + bez
    screen = rrect_path(sx, sy, sw, sh, 4, 4, 4, 4, "screen")
    shapes = [group([ellipse((8, 8), (W / 2, by + bh - 9)), fill("#4A4A52")], "led"),
              group(rrect_path(bx, by, bw, bh, 12, 12, 12, 12, "out") + screen + [fill(slot="primary", even_odd=True)], "bezel"),
              group(rrect_path(bx + 160, by + bh, 90, 54, 0, 0, 10, 10) + [fill(slot="secondary")], "foot-l"),
              group(rrect_path(bx + bw - 250, by + bh, 90, 54, 0, 0, 10, 10) + [fill(slot="secondary")], "foot-r")]
    shapes = shapes[:1] + shapes[2:] + shapes[1:2]
    finish_device(comp, shapes, (bx, by, bw, bh), 12, screen)
    return comp, (sx, sy, sw, sh)


def crt(F=60):
    M = 40
    W, H = 1620, 1180
    comp = device_comp("tv-frame", W, H, F)
    comp.slot("primary", "#7A4B2A")     # cabinet
    comp.slot("secondary", "#1B1B1F")   # bezel
    comp.slot("accent", "#C9B78F")      # control panel
    comp.slot("icon", "#2A2A2E")
    bx, by, bw, bh = M, M + 120, W - 2 * M, H - 2 * M - 120 - 40
    sw, sh = 1080, 780
    sx, sy = bx + 70, by + (bh - sh) / 2
    screen = rrect_path(sx, sy, sw, sh, 120, 120, 120, 120, "screen")
    bez_out = (sx - 36, sy - 36, sw + 72, sh + 72)
    px = sx + sw + 70
    pw_ = bx + bw - 30 - px
    shapes = []
    # knobs and speaker slots on the control panel
    for i, ky in enumerate((sy + 110, sy + 250)):
        shapes.append(group([polyline([(px + pw_ / 2, ky), (px + pw_ / 2 + 22, ky - 22)]), stroke(slot="accent", width=6)], f"knob-mark{i}"))
        shapes.append(group([ellipse((70, 70), (px + pw_ / 2, ky)), fill(slot="icon")], f"knob{i}"))
    for k in range(7):
        shapes.append(group([rect_tl(px + 24, sy + 400 + k * 30, pw_ - 48, 8, 4), fill(slot="icon", opacity=70)], f"slot{k}"))
    shapes += [group(rrect_path(px, sy - 20, pw_, sh + 40, 20, 20, 20, 20) + [fill(slot="accent")], "panel"),
               group(rrect_path(*bez_out, 150, 150, 150, 150) + screen + [fill(slot="secondary", even_odd=True)], "bezel"),
               group(rrect_path(bx, by, bw, bh, 50, 50, 50, 50) + screen + [fill(slot="primary", even_odd=True)], "cabinet"),
               group(rrect_path(bx + 120, by + bh, 90, 36, 0, 0, 12, 12) + [fill(slot="icon")], "foot-l"),
               group(rrect_path(bx + bw - 210, by + bh, 90, 36, 0, 0, 12, 12) + [fill(slot="icon")], "foot-r")]
    # antenna behind the cabinet
    ax = bx + bw / 2 - 40
    ant = [group([polyline([(ax, by + 6), (ax - 200, by - 112)]), stroke(slot="icon", width=9)], "ant-l"),
           group([polyline([(ax, by + 6), (ax + 220, by - 112)]), stroke(slot="icon", width=9)], "ant-r"),
           group([ellipse((60, 36), (ax, by + 4)), fill(slot="icon")], "ant-base")]
    shapes = ant + shapes
    shapes = shapes[:3] + shapes[3:]
    finish_device(comp, shapes, (bx, by, bw, bh), 50, screen)
    return comp, (sx, sy, sw, sh)


vs = []
for vid, nm, fn, desc in (("flat", "Flat TV", flat, "Modern flat-screen TV with a thin bezel and two feet."),
                          ("retro-crt", "Retro CRT", crt, "Wood-grain CRT television with rabbit-ear antenna, knobs and a rounded screen.")):
    c, scr = fn()
    vs.append(Variant(vid, nm, c, "intro-hold", text_areas={"screen": scr}, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "tv-frame", "TV Frame",
            "Television mockup with a real screen cut-out for your video: a modern flat TV and a retro CRT with "
            "antenna and knobs.",
            ["tv", "television", "crt", "retro", "screen", "mockup", "frame", "device", "broadcast", "vintage"], vs)
