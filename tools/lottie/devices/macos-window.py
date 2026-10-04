import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from devices_kit import *

W, H = 1720, 1080
WX, WY, WW, WH = 60, 40, 1600, 960
TB = 56
R = 22
RED, YEL, GRN = "#FF5F57", "#FEBC2E", "#28C840"


def lights(y):
    return [group([ellipse((20, 20), (WX + 34 + i * 30, y)), fill(c)], f"light{i}") for i, c in enumerate((RED, YEL, GRN))]


def window(kind, F=60):
    comp = device_comp("macos-window", W, H, F)
    comp.slot("background", "#ECECEC")
    comp.slot("icon", "#5A5A5F")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("outline", "#C8C8CC")
    tb = TB if kind != "safari" else 76
    cy = WY + tb / 2
    chrome = lights(cy)
    areas = {}
    if kind == "classic":
        chrome += [group([rect_tl(WX + WW / 2 - 160, cy - 10, 320, 20, 6), fill(slot="outline", opacity=0)], "title-area")]
        areas["title"] = (WX + WW / 2 - 200, WY + 8, 400, TB - 16)
    elif kind == "safari":
        chrome += [chevron(WX + 200, cy, 9, "left", w=3.2), chevron(WX + 244, cy, 9, "right", w=3.2, opacity=60)]
        pill = (WX + 330, cy - 22, WW - 660, 44)
        chrome += [group([rect_tl(*pill, 12), fill(slot="secondary")], "address"),
                   group([rect_tl(*pill, 12), stroke(slot="outline", width=1.5)], "address-edge")]
        l1, l2 = lock(pill[0] + 34, cy, 12)
        chrome += [l1, l2, reload(pill[0] + pill[2] - 34, cy, 10, w=2.8),
                   share(WX + WW - 130, cy, 14, w=2.8), plus(WX + WW - 70, cy, 13, w=2.8),
                   square(WX + 140, cy, 11, w=2.8, r=4)]
        areas["address"] = (pill[0] + 62, pill[1] + 6, pill[2] - 124, pill[3] - 12)
    else:  # terminal
        chrome += [group([rect_tl(WX + WW / 2 - 200, cy - 10, 400, 20, 6), fill(slot="outline", opacity=0)], "title-area")]
        areas["title"] = (WX + WW / 2 - 240, WY + 8, 480, TB - 16)
    screen = (WX, WY + tb, WW, WH - tb)
    body_shapes = []
    if kind == "terminal":
        comp.slots["background"]["p"]["k"] = hex_color("#2B2B2E")
        comp.slots["icon"]["p"]["k"] = hex_color("#C9C9CE")
        comp.slot("primary", "#0B0B0D")
        comp.slot("accent", "#7EE787")
        px, py = WX + 36, WY + tb + 60
        prompt = "user@mac ~ %"
        body_shapes += [label(prompt, px, py, 34, 500, slot="accent"),
                        group([rect_tl(px + text_width(prompt, 34, 500) + 18, py - 30, 18, 38, 2), fill(slot="icon")], "cursor",
                              opacity=Anim([(0, 100, HOLD), (30, 0, HOLD), (60, 100)]))]
        body = group([rect_tl(*screen, 0), fill(slot="primary")], "body")
    else:
        body = None
    tbar = group([rect_tl(WX, WY, WW, tb, 0), fill(slot="background")], "titlebar")
    edge = group([polyline([(WX, WY + tb), (WX + WW, WY + tb)]), stroke(slot="outline", width=1.5)], "sep")
    # clip the chrome to the rounded window: build the window as outer-rounded fill, hole for the screen
    if kind == "terminal":
        shell = [group([rect_tl(WX, WY, WW, WH, R), fill(slot="primary")], "window")]
        top = [tbar]
        # titlebar needs rounded top corners: draw rounded window, then a rect covering lower part of titlebar
        top = [group([rect_tl(WX, WY, WW, tb + 30, R), fill(slot="background")], "titlebar-rounded"),
               group([rect_tl(WX, WY + tb, WW, 30, 0), fill(slot="primary")], "titlebar-cover")]
        layers_shapes = chrome + body_shapes + top + shell
    else:
        # real hole: titlebar + border ring around transparent screen
        ring_outer = (WX, WY, WW, WH)
        ring = group([rect_tl(*ring_outer, R)] + rrect_path(*screen, bl=R - 2, br=R - 2, name="screen") +
                     [fill(slot="background", even_odd=True)], "window")
        layers_shapes = chrome[::-1] + [edge, ring]
    pop_layer(comp, "window", layers_shapes, W / 2, H / 2)
    hole = None if kind == "terminal" else rrect_path(*screen, bl=R - 2, br=R - 2, name="screen")
    comp.layer("shadow", soft_shadow(WX, WY, WW, WH, R, hole=hole), anchor=(W / 2, H / 2), position=(W / 2, H / 2), opacity=fade(0, 14))
    areas["screen"] = screen
    return comp, areas


vs = []
for vid, nm, desc in (("classic", "Finder Style", "Light titlebar with traffic lights and a transparent window body for your footage; type a title in the title area."),
                      ("safari", "Safari Toolbar", "Toolbar with navigation arrows, a centred address pill with lock and reload, share and tab buttons; footage shows through the body."),
                      ("terminal", "Terminal", "Dark Terminal window with a blinking prompt cursor; the body is solid, type commands in the screen text area.")):
    c, a = window(vid)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a.get("title") or a.get("address"), text_areas=a, thumb_t=0.95, bg="6a7087",
                      description=desc))
build_asset(CAT, "macos-window", "macOS Window",
            "macOS window frame with traffic-light buttons that pops in. The window body is a real cut-out so your "
            "screen recording or footage shows through; Terminal has a solid body.",
            ["macos", "mac", "window", "desktop", "finder", "safari", "terminal", "frame", "screen recording", "mockup"], vs)
