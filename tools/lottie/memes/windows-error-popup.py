from _common import *

W, H, F = 700, 330, 30
comp = Comp("windows-error-popup", W, H, fps=30, frames=F)
comp.slot("background", "#C0C0C0")
comp.slot("primary", "#E2231A")

P = 2
WX, WY, WW, WH = 30, 30, 640, 270


def box(x, y, w, h, color=None, slot=None, name="box"):
    return group([rect((w, h), (x + w / 2, y + h / 2)), fill(color or "#FFFFFF", slot=slot)], name)


def bevel(x, y, w, h, sunken=False):
    """Classic two-pixel 3D edge, face on top (returned top-first)."""
    dark, light, mid, hi = "#0A0A0A", "#DFDFDF", "#808080", "#FFFFFF"
    if sunken:
        dark, light, mid, hi = hi, mid, light, dark
    return [box(x + 2 * P, y + 2 * P, w - 4 * P, h - 4 * P, slot="background", name="face"),
            box(x + P, y + P, w - 3 * P, h - 3 * P, hi, name="hi"),
            box(x + P, y + P, w - 2 * P, h - 2 * P, mid, name="mid"),
            box(x, y, w - P, h - P, light, name="light"),
            box(x, y, w, h, dark, name="dark")]


def cross(cx, cy, r, color, width):
    return group([polyline([(cx - r, cy - r), (cx + r, cy + r)]), polyline([(cx - r, cy + r), (cx + r, cy - r)]),
                  stroke(color, width, cap="butt")], "cross")


# title bar
TX, TY, TW, TH = WX + 3 * P, WY + 3 * P, WW - 6 * P, 38
title = [group([rect((TW, TH), (TX + TW / 2, TY + TH / 2)),
                gradient_fill([(0, "#000080"), (1, "#1084D0")], (TX, 0), (TX + TW, 0))], "title bar")]
CBW, CBH = 34, 30
CBX, CBY = TX + TW - CBW - 4, TY + (TH - CBH) / 2
close = [cross(CBX + CBW / 2 - 1, CBY + CBH / 2 - 1, 7, "#000000", 4.5)] + bevel(CBX, CBY, CBW, CBH)

# error icon
IX, IY = WX + 78, WY + 118
icon = [cross(IX, IY, 14, "#FFFFFF", 7.5),
        group([ellipse((64, 64), (IX, IY)),
               gradient_fill([(0, "#FFFFFF", 0.45), (1, "#FFFFFF", 0)], (IX - 16, IY - 18), (IX + 30, IY + 30),
                             radial=True)], "shine"),
        group([ellipse((64, 64), (IX, IY)), fill(slot="primary"), stroke("#6E0B08", 2.5)], "disc"),
        group([ellipse((64, 64), (IX + 5, IY + 5)), fill("#000000", 45)], "shadow")]

# default OK button: black frame, raised bevel, dotted focus rectangle
BW, BH = 156, 48
BX, BY = WX + (WW - BW) / 2, WY + WH - BH - 26
button = [group([rect((BW - 22, BH - 22), (BX + BW / 2, BY + BH / 2)),
                 stroke("#000000", 2, cap="butt", join="miter", dashes=[2, 2])], "focus")]
button += bevel(BX + P, BY + P, BW - 2 * P, BH - 2 * P) + [box(BX, BY, BW, BH, "#000000", name="frame")]

shapes = close + title + icon + button + bevel(WX, WY, WW, WH)
comp.layer("dialog", shapes, anchor=(W / 2, H / 2), position=(W / 2, H / 2),
           scale=anim([(0, [55, 55], EASE_OUT), (7, [104, 104], EASE_IN_OUT), (11, [98.5, 98.5], EASE_IN_OUT),
                       (15, [100, 100])]),
           opacity=anim([(0, 0, EASE_OUT), (4, 100)]))

build(comp, "memes", "windows-error-popup", "Retro Error Popup",
      "Retro late-90s desktop error dialog with a gradient title bar, red error icon and an OK "
      "button that pops in with a small bounce. Put your message beside the icon.",
      ["error", "popup", "dialog", "retro", "windows", "90s", "meme", "computer"], "intro-hold",
      thumb_t=1.0, text_area=[WX + 128, WY + 70, WW - 150, 104])
