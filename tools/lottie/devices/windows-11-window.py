import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

W, H = 1720, 1080
WX, WY, WW, WH = 60, 40, 1600, 960
R = 16


def controls(y, tb):
    cx = WX + WW
    return [minus(cx - 138, y, 9, w=2.4), square(cx - 92, y, 8.5, w=2.4, r=2), cross(cx - 46, y, 9, w=2.4)]


def app_icon(x, y):
    # four-pane window glyph as a stand-in app icon
    return [group([rect_tl(x + (i % 2) * 15, y - 15 + (i // 2) * 15, 13, 13, 2), fill(slot="primary")], f"pane{i}")
            for i in range(4)]


def build(kind, F=60):
    comp = device_comp("windows-11-window", W, H, F)
    comp.slot("background", "#F3F3F3")
    comp.slot("icon", "#1B1B1B")
    comp.slot("primary", "#0067C0")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("outline", "#DADADA")
    areas = {}
    if kind == "classic":
        tb = 48
        cy = WY + tb / 2
        chrome = app_icon(WX + 22, cy) + controls(cy, tb)
        areas["title"] = (WX + 70, WY + 8, 520, tb - 16)
    elif kind == "explorer":
        tb = 128
        cy = WY + 26
        chrome = app_icon(WX + 22, cy) + controls(cy, tb)
        # tab
        chrome += [group(rrect_path(WX + 62, WY + 8, 260, 40, tl=10, tr=10) + [fill(slot="secondary")], "tab")]
        chrome += [cross(WX + 296, cy, 6, w=2), plus(WX + 350, cy, 9, w=2.4)]
        ty = WY + 88
        chrome += [chevron(WX + 34, ty, 9, "left", w=2.8), chevron(WX + 80, ty, 9, "right", w=2.8, opacity=45),
                   group([polyline([(WX + 126, ty + 8), (WX + 126, ty - 8)]), polyline([(WX + 118, ty), (WX + 126, ty - 10), (WX + 134, ty)]),
                          stroke(slot="icon", width=2.8)], "up"),
                   reload(WX + WW - 520, ty, 10, w=2.6)]
        pill = (WX + 170, ty - 20, WW - 770, 40)
        chrome += [group([rect_tl(*pill, 6), fill(slot="secondary")], "address"),
                   group([rect_tl(*pill, 6), stroke(slot="outline", width=1.5)], "address-edge")]
        sb = (WX + WW - 480, ty - 20, 440, 40)
        chrome += [group([rect_tl(*sb, 6), fill(slot="secondary")], "search"),
                   group([rect_tl(*sb, 6), stroke(slot="outline", width=1.5)], "search-edge"),
                   magnifier(sb[0] + sb[2] - 26, ty, 10, w=2.4)]
        areas["address"] = (pill[0] + 14, pill[1] + 5, pill[2] - 28, pill[3] - 10)
        areas["search"] = (sb[0] + 14, sb[1] + 5, sb[2] - 60, sb[3] - 10)
    else:  # edge-style browser
        tb = 112
        cy = WY + 26
        chrome = [group(rrect_path(WX + 14, WY + 8, 300, 40, tl=10, tr=10) + [fill(slot="secondary")], "tab"),
                  cross(WX + 286, cy, 6, w=2), plus(WX + 346, cy, 9, w=2.4)] + controls(cy, tb)
        chrome += [group([ellipse((18, 18), (WX + 42, cy)), fill(slot="primary")], "favicon")]
        ty = WY + 78
        chrome += [chevron(WX + 34, ty, 9, "left", w=2.8), chevron(WX + 80, ty, 9, "right", w=2.8, opacity=45),
                   reload(WX + 128, ty, 10, w=2.6)]
        pill = (WX + 176, ty - 21, WW - 340, 42)
        chrome += [group([rect_tl(*pill, 21), fill(slot="secondary")], "address"),
                   group([rect_tl(*pill, 21), stroke(slot="outline", width=1.5)], "address-edge")]
        l1, l2 = lock(pill[0] + 30, ty, 11)
        chrome += [l1, l2, star_icon(pill[0] + pill[2] - 34, ty, 11, w=2.4), dots3(WX + WW - 40, ty, 9, 2.6, slot="icon")]
        areas["address"] = (pill[0] + 60, pill[1] + 6, pill[2] - 120, pill[3] - 12)
    areas["screen"] = window_shell(comp, WX, WY, WW, WH, R, tb, chrome)
    return comp, areas


vs = []
for vid, nm, desc in (("classic", "Windows Title Bar", "Windows 11 title bar with app icon, title area and minimise / maximise / close buttons; transparent body."),
                      ("explorer", "File Explorer", "File Explorer style window: a tab, back / forward / up arrows, address bar and search box."),
                      ("browser", "Browser", "Edge-style browser window with a tab, navigation buttons and a rounded address bar.")):
    c, a = build(vid)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a.get("address") or a.get("title"), text_areas=a, thumb_t=0.95,
                      bg="6a7087", description=desc))
build_asset(CAT, "windows-11-window", "Windows 11 Window",
            "Windows 11 window frame with Mica-style title bar and caption buttons that pops in. The body is a real "
            "cut-out for your screen recording or footage.",
            ["windows", "windows 11", "window", "desktop", "explorer", "edge", "frame", "screen recording", "mockup", "pc"], vs)
