import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"
S = 320
C = S / 2


def fill_glyph(d, size, cx, cy, slot="icon"):
    return [group(icon(d, size, (cx, cy)) + [fill(slot=slot)], "glyph")]


def stroke_glyph(points, size, cx, cy, width, slot="icon"):
    k = size / 24
    pts = [(cx + (x - 12) * k, cy + (y - 12) * k) for x, y in points]
    return [group([polyline(pts), stroke(slot=slot, width=width * k, join="round")], "glyph")]


def glyph_only(glyph, ripple=False):
    comp = Comp("toggle", S, S, frames=60)
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#0A84FF")
    comp.layer("ripple", [group([ellipse((260, 260), (C, C)), stroke(slot="accent", width=8)], "ring",
                                anchor=(C, C), position=(C, C), scale=Anim([(6, [55, 55], EASE_OUT), (30, [115, 115])]),
                                opacity=Anim([(6, 90, EASE_OUT), (30, 0)]))])
    comp.layer("glyph", glyph(190, C, C), anchor=(C, C), position=(C, C),
               scale=Anim([(0, [0, 0], OVERSHOOT), (14, [100, 100])]),
               rotation=Anim([(0, -25, OVERSHOOT), (14, 0)]))
    return comp


def button(glyph):
    comp = Comp("toggle", S, S, frames=75)
    comp.slot("primary", "#0A84FF")
    comp.slot("secondary", "#3A3A44")
    comp.slot("icon", "#FFFFFF")
    comp.layer("glyph", glyph(138, C, C), anchor=(C, C), position=(C, C),
               scale=Anim([(0, [100, 100], EASE_IN_OUT), (14, [100, 100], EASE_IN_OUT), (22, [118, 118], EASE_OUT),
                           (32, [100, 100])]))
    comp.layer("active", [group([ellipse((260, 260), (C, C)), fill(slot="primary")], "on")], anchor=(C, C), position=(C, C),
               opacity=Anim([(14, 0, HOLD), (16, 100)]),
               scale=Anim([(14, [78, 78], EASE_OUT), (30, [100, 100])]))
    comp.layer("inactive", [group([ellipse((260, 260), (C, C)), fill(slot="secondary")], "off")])
    return comp


def build_toggle(asset_id, name, desc, tags, glyph, color):
    g, b = glyph_only(glyph), button(glyph)
    g.slots["accent"]["p"]["k"] = hex_color(color)
    b.slots["primary"]["p"]["k"] = hex_color(color)
    build_asset(CAT, asset_id, name, desc, tags, [
        Variant("button", "Control Button", b, "intro-hold", thumb_t=0.95, bg="e8e8ee"),
        Variant("glyph", "Glyph Pop", g, "intro-hold", thumb_t=0.95, bg="6a7087"),
    ])
