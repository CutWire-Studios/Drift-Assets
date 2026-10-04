import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

W, H = 1720, 1080
WX, WY, WW, WH = 60, 40, 1600, 960
R = 20
RED, YEL, GRN = "#FF5F57", "#FEBC2E", "#28C840"


def build(kind, F=60):
    comp = device_comp("browser-window", W, H, F)
    comp.slot("background", "#DEE1E6")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("icon", "#5F6368")
    comp.slot("primary", "#1A73E8")
    comp.slot("outline", "#C4C7CC")
    areas = {}
    if kind == "tabs":
        tb = 120
        cy = WY + 30
        chrome = [group([ellipse((20, 20), (WX + 34 + i * 30, cy)), fill(c)], f"light{i}") for i, c in enumerate((RED, YEL, GRN))]
        tx = WX + 140
        chrome += [group(rrect_path(tx, WY + 8, 270, 50, tl=14, tr=14) + [fill(slot="secondary")], "tab-active"),
                   group([ellipse((20, 20), (tx + 34, cy)), fill(slot="primary")], "favicon"),
                   cross(tx + 238, cy, 6, w=2.2), plus(tx + 308, cy, 10, w=2.6)]
        chrome += [group([rect_tl(tx + 270, WY + 18, 2, 30, 1), fill(slot="outline", opacity=0)], "gap")]
        ty = WY + 88
        chrome += [chevron(WX + 34, ty, 9, "left", w=2.8), chevron(WX + 78, ty, 9, "right", w=2.8, opacity=45),
                   reload(WX + 122, ty, 10, w=2.6)]
        pill = (WX + 170, ty - 22, WW - 330, 44)
        chrome += [group([rect_tl(*pill, 22), fill(slot="secondary")], "address")]
        l1, l2 = lock(pill[0] + 34, ty, 11)
        chrome += [l1, l2, star_icon(pill[0] + pill[2] - 34, ty, 11, w=2.4),
                   group([ellipse((34, 34), (WX + WW - 84, ty)), fill(slot="primary")], "profile"),
                   dots3(WX + WW - 34, ty, 9, 2.8)]
        # the tab merges into the toolbar
        chrome += [group([rect_tl(tx, WY + 56, 270, 8, 0), fill(slot="secondary")], "tab-join")]
        areas["tab"] = (tx + 56, WY + 16, 150, 34)
        areas["address"] = (pill[0] + 64, pill[1] + 6, pill[2] - 128, pill[3] - 12)
        bar_bg = "background"
    else:
        tb = 76
        cy = WY + tb / 2
        chrome = [group([ellipse((20, 20), (WX + 34 + i * 30, cy)), fill(c)], f"light{i}") for i, c in enumerate((RED, YEL, GRN))]
        pill = (WX + WW / 2 - 330, cy - 23, 660, 46)
        chrome += [group([rect_tl(*pill, 23), fill(slot="secondary")], "address"),
                   group([rect_tl(*pill, 23), stroke(slot="outline", width=1.5)], "address-edge")]
        chrome += [magnifier(pill[0] + 36, cy, 10, w=2.4), reload(pill[0] + pill[2] - 36, cy, 10, w=2.6),
                   chevron(WX + 190, cy, 9, "left", w=2.8), chevron(WX + 236, cy, 9, "right", w=2.8, opacity=45),
                   share(WX + WW - 100, cy, 13, w=2.6), plus(WX + WW - 48, cy, 12, w=2.6)]
        areas["address"] = (pill[0] + 72, pill[1] + 7, pill[2] - 144, pill[3] - 14)
    areas["screen"] = window_shell(comp, WX, WY, WW, WH, R, tb, chrome)
    return comp, areas


vs = []
for vid, nm, desc in (("tabs", "Tabbed Browser", "Chrome-style window with a tab strip, back / forward / reload, address pill, bookmark star and profile button."),
                      ("minimal", "Minimal Address Bar", "Compact browser toolbar with traffic lights and a centred rounded address bar.")):
    c, a = build(vid)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["address"], text_areas=a, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "browser-window", "Browser Window",
            "Web browser window with a tab strip and address bar, or a minimal address-bar toolbar. Pops in with a "
            "transparent body so a website recording shows through; type the URL in the address text area.",
            ["browser", "chrome", "website", "url", "address bar", "tabs", "web", "window", "frame", "screen recording"], vs)
