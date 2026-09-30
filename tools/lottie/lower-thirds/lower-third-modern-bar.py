from _common import *
from _lt2 import rrect, lay, slide, fade, rect_grow, SPRING, BACK_IN
from drift_lottie import Variant, build_asset

W, H = 1000, 212
AX, AW = 24, 16            # accent block
TOP, MH = 40, 88           # main bar
SUB_Y, SH = 132, 40        # secondary bar
BX = AX + AW
MW, SW = 920, 600


def base(name, intro_end):
    comp = Comp(name, W, H, fps=FPS, frames=FRAMES)
    comp.slot("accent", "#2E7CF6")
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#14213D")
    comp.marker("intro", 0, intro_end)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    return comp


def classic():
    """Accent block wipes in and the name and subtitle bars extend from it."""
    comp = base("lower-third-modern-bar", 32)
    full_h = SUB_Y + SH - TOP
    cy = TOP + full_h / 2

    comp.layer("accent", [rect((AW, full_h), (AW / 2, 0)), fill(slot="accent")],
               anchor=(0, 0), position=(AX, cy),
               scale=keys((0, [0, 100], EXPO_OUT), (8, [420, 100], INOUT), (20, [100, 100], HOLD),
                          (132, [100, 100], INOUT), (140, [420, 100], EXPO_IN), (149, [0, 100])))

    comp.layer("main", [rect((MW, MH), (MW / 2, 0)), fill(slot="primary")],
               anchor=(0, 0), position=(BX, TOP + MH / 2),
               scale=io([0, 100], [100, 100], 7, 27, 122, 138, EXPO_OUT, INOUT))

    comp.layer("sub", [rect((SW, SH), (SW / 2, 0)), fill(slot="secondary")],
               anchor=(0, 0), position=(BX, SUB_Y + SH / 2),
               scale=io([0, 100], [100, 100], 14, 32, 120, 133, EXPO_OUT, INOUT))
    return comp


def rounded():
    """A round accent badge pops, then rounded bars slide out from behind it."""
    comp = base("lower-third-modern-bar--rounded", 36)
    cy = 106
    d = 150
    c = (30 + d / 2, cy)
    mx, my, mw, mh = c[0], 26, 860, 94
    sx, sy, sw, sh = c[0], 128, 580, 50
    badge = keys((0, [0, 0], SPRING), (14, [100, 100], HOLD), (128, [100, 100], EASE_OUT), (133, [108, 108], EXPO_IN),
                 (144, [0, 0]))
    comp.layer("badge-core", [ellipse((d - 56, d - 56), c), fill(slot="primary")], anchor=c, position=c,
               scale=keys((5, [0, 0], SPRING), (18, [100, 100], HOLD), (124, [100, 100], EXPO_IN), (134, [0, 0])))
    comp.layer("badge", [ellipse((d, d), c), fill(slot="accent")], anchor=c, position=c, scale=badge,
               rotation=keys((0, -40, EXPO_OUT), (16, 0)))
    comp.layer("badge-shadow", [ellipse((d, d), (c[0], c[1] + 6)), fill("#000000", 20)], anchor=c, position=c,
               scale=badge)
    comp.layer("main", [rect_grow(mx, my, mw, mh, 22, 8, 30, 120, 138, "left", start=0, eout=INOUT),
                        fill(slot="primary")])
    comp.layer("sub", [rect_grow(sx, sy, sw, sh, sh / 2, 14, 36, 116, 132, "left", start=0, eout=INOUT),
                       fill(slot="secondary")])
    comp.layer("shadow", [rrect(mx + 4, my + 6, mw, mh, 22), rrect(sx + 4, sy + 6, sw, sh, sh / 2),
                          fill("#000000", 16)], opacity=fade(26, 36, 116, 124))
    tx = c[0] + d / 2 + 26
    return comp, {"name": [tx, my + 12, mx + mw - tx - 30, mh - 24], "subtitle": [tx, sy + 8, sx + sw - tx - 30, sh - 16]}


def rise():
    """An accent baseline wipes across; the name bar and a subtitle chip rise up out of it."""
    comp = base("lower-third-modern-bar--rise", 34)
    x0, base_y = 30, 178
    lw = 940
    mx, my, mw, mh = x0, 80, 900, 90
    sx, sy, sw, sh = x0, 34, 420, 42
    comp.layer("baseline", [rect_grow(x0, base_y, lw, 8, 0, 0, 16, 132, 146, "left", start=0, eout=INOUT),
                            fill(slot="accent")])
    comp.layer("main-matte", [rrect(x0 - 20, 0, lw + 40, base_y - 4), fill("#FFFFFF")])
    lay(comp, "main", [rrect(mx, my, mw, mh), fill(slot="primary")],
        off=keys((0, [0, mh + 12], HOLD), (8, [0, mh + 12], SPRING), (26, [0, 0], HOLD), (124, [0, 0], EXPO_IN),
                 (136, [0, mh + 12])),
        matte="alpha")
    comp.layer("sub-matte", [rrect(x0 - 20, 0, lw + 40, my), fill("#FFFFFF")])
    lay(comp, "sub", [rrect(sx, sy, sw, sh), fill(slot="secondary")],
        off=keys((0, [0, sh + 8], HOLD), (16, [0, sh + 8], SPRING), (32, [0, 0], HOLD), (118, [0, 0], EXPO_IN),
                 (128, [0, sh + 8])),
        matte="alpha")
    comp.layer("tick", [rrect(sx + sw - 12, sy, 12, sh), fill(slot="accent")],
               opacity=keys((0, 0, HOLD), (28, 0, EASE_OUT), (32, 100, HOLD), (116, 100, EASE_IN), (120, 0)))
    return comp, {"name": [mx + 26, my + 10, mw - 52, mh - 20], "subtitle": [sx + 22, sy + 5, sw - 56, sh - 10]}


rc, ra = rounded()
uc, ua = rise()
build_asset("lower-thirds", "lower-third-modern-bar", "Modern Bar Lower Third",
            "Clean corporate lower third with a name bar, a subtitle bar and a colour accent.",
            ["lower third", "name", "title", "corporate", "youtube", "clean", "bar"], [
    Variant("classic", "Classic", classic(), "intro-hold-outro",
            text_area=[BX + 24, TOP + 8, MW - 48, MH - 16],
            text_areas={"name": [BX + 24, TOP + 8, MW - 48, MH - 16], "subtitle": [BX + 24, SUB_Y + 4, SW - 48, SH - 8]},
            thumb_t=0.5,
            description="An accent block wipes in and a name bar and subtitle bar extend from it."),
    Variant("rounded", "Rounded Badge", rc, "intro-hold-outro", text_area=ra["name"], text_areas=ra, thumb_t=0.5,
            description="A round accent badge pops in and rounded bars slide out from behind it."),
    Variant("rise", "Rise Up", uc, "intro-hold-outro", text_area=ua["name"], text_areas=ua, thumb_t=0.5,
            description="An accent baseline wipes across and the name bar and a subtitle chip spring up out of it."),
])
