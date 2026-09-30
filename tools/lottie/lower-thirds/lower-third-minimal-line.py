from _common import *
from _lt2 import rrect, lay, slide, fade, rect_grow, pop, SPRING
from drift_lottie import Variant, build_asset

W, H = 790, 200
LX, LY0, LY1 = 26, 30, 170       # accent line
PX, PY, PW, PH = 34, 40, 720, 120  # plate
DIV_Y = 106


def base(name, intro_end):
    comp = Comp(name, W, H, fps=FPS, frames=FRAMES)
    comp.slot("accent", "#E8B04B")
    comp.slot("background", "#0E1116")
    comp.slot("secondary", "#FFFFFF")
    comp.marker("intro", 0, intro_end)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    return comp


def classic():
    """Thin vertical accent line draws on, then a translucent plate reveals beside it."""
    comp = base("lower-third-minimal-line", 46)
    comp.layer("line", [
        polyline([(LX, LY0), (LX, LY1)]),
        stroke(slot="accent", width=4, cap="butt"),
        trim(start=keys((0, 0, HOLD), (134, 0, EXPO_IN), (148, 100)),
             end=keys((0, 0, EXPO_OUT), (18, 100))),
    ])

    comp.layer("divider", [
        polyline([(PX + 30, DIV_Y), (PX + 330, DIV_Y)]),
        stroke(slot="secondary", width=1.5, opacity=35, cap="butt"),
        trim(start=keys((0, 0, HOLD), (120, 0, INOUT), (132, 100)),
             end=keys((0, 0, HOLD), (24, 0, EXPO_OUT), (46, 100))),
    ])

    comp.layer("plate-matte", [rect((PW, PH), (PW / 2, PH / 2)), fill("#FFFFFF")],
               anchor=(0, 0), position=(PX, PY),
               scale=io([0, 100], [100, 100], 10, 38, 122, 140, EXPO_OUT, INOUT))
    comp.layer("plate", [rect((PW, PH), (PW / 2, PH / 2)), fill(slot="background", opacity=60)],
               matte="alpha", anchor=(0, 0),
               position=io([PX - 60, PY], [PX, PY], 10, 40, 122, 140, EXPO_OUT, INOUT))
    return comp


def underline():
    """A dot pops, the underline shoots right from it, and both text bands rise out of the line."""
    comp = base("lower-third-minimal-line--underline", 44)
    x0, x1, ly = 40, 740, 112
    nx, ny, nw, nh = 56, 44, 684, 62       # name band above the line
    sx, sy, sw, sh = 56, 120, 470, 40      # subtitle band below it
    comp.layer("dot", [ellipse((14, 14), (x0, ly)), fill(slot="accent")], anchor=(x0, ly), position=(x0, ly),
               scale=keys((0, [0, 0], SPRING), (10, [100, 100], HOLD), (136, [100, 100], EXPO_IN), (146, [0, 0])))
    comp.layer("line", [polyline([(x0 + 10, ly), (x1, ly)]),
                        trim(end=keys((4, 0, EXPO_OUT), (26, 100)), start=keys((0, 0, HOLD), (128, 0, INOUT), (142, 100))),
                        stroke(slot="accent", width=3, cap="round")])
    comp.layer("tick", [polyline([(x1, ly - 9), (x1, ly + 9)]), stroke(slot="accent", width=3, cap="round")],
               anchor=(x1, ly), position=(x1, ly),
               scale=keys((0, [100, 0], HOLD), (22, [100, 0], SPRING), (32, [100, 100], HOLD), (124, [100, 100], EASE_IN),
                          (130, [100, 0])))
    # name band rises out of the line, subtitle band drops out of it
    comp.layer("name-matte", [rrect(nx - 16, 0, nw + 32, ly - 3), fill("#FFFFFF")])
    lay(comp, "name", [rrect(nx - 16, ny, nw + 16, nh, 4), fill(slot="background", opacity=55)],
        off=slide(0, nh + 8, 14, 36, 118, 134, EXPO_OUT, EXPO_IN), matte="alpha")
    comp.layer("sub-matte", [rrect(sx - 16, ly + 3, sw + 32, 80), fill("#FFFFFF")])
    lay(comp, "sub", [rrect(sx - 16, sy, sw + 16, sh, 4), fill(slot="background", opacity=35)],
        off=slide(0, -sh - 8, 20, 42, 114, 130, EXPO_OUT, EXPO_IN), matte="alpha")
    return comp, {"name": [nx + 8, ny + 8, nw - 24, nh - 16], "subtitle": [sx + 8, sy + 6, sw - 24, sh - 12]}


def capsule():
    """An accent ring pops on the left and a frosted capsule stretches out of it."""
    comp = base("lower-third-minimal-line--capsule", 40)
    cy, ch = 100, 128
    x0, cw = 30, 720
    r = ch / 2
    ring = (x0 + r, cy)
    comp.layer("ring", [ellipse((ch - 26, ch - 26), ring), stroke(slot="accent", width=4)],
               anchor=ring, position=ring,
               scale=keys((0, [0, 0], SPRING), (14, [100, 100], HOLD), (132, [100, 100], EXPO_IN), (146, [0, 0])),
               rotation=keys((0, -120, EXPO_OUT), (18, 0)))
    comp.layer("core", [ellipse((30, 30), ring), fill(slot="accent")], anchor=ring, position=ring,
               scale=keys((4, [0, 0], SPRING), (16, [100, 100], HOLD), (128, [100, 100], EXPO_IN), (138, [0, 0])))
    div_x0, div_x1 = x0 + ch + 10, x0 + ch + 330
    comp.layer("divider", [polyline([(div_x0, cy + 4), (div_x1, cy + 4)]),
                           trim(end=keys((0, 0, HOLD), (22, 0, EXPO_OUT), (42, 100)),
                                start=keys((0, 0, HOLD), (118, 0, INOUT), (128, 100))),
                           stroke(slot="secondary", width=1.5, opacity=40, cap="butt")])
    comp.layer("capsule", [rect_grow(x0, cy - r, cw, ch, r, 8, 34, 120, 140, "left", start=ch, ein=EXPO_OUT, eout=INOUT),
                           fill(slot="background", opacity=62)],
               opacity=keys((0, 0, HOLD), (8, 0, EASE_OUT), (12, 100, HOLD), (136, 100, EASE_IN), (140, 0)))
    tx = x0 + ch + 10
    return comp, {"name": [tx, cy - r + 12, x0 + cw - tx - 40, 50], "subtitle": [tx, cy + 12, x0 + cw - tx - 40, 34]}


uc, ua = underline()
cc, ca = capsule()
build_asset("lower-thirds", "lower-third-minimal-line", "Minimal Line Lower Third",
            "Elegant minimal lower third built from a thin accent line and a translucent plate, with room for a "
            "name and a subtitle.",
            ["lower third", "name", "title", "minimal", "elegant", "line", "clean"], [
    Variant("classic", "Side Line", classic(), "intro-hold-outro",
            text_area=[PX + 30, PY + 12, PW - 60, 50],
            text_areas={"name": [PX + 30, PY + 12, PW - 60, 50], "subtitle": [PX + 30, DIV_Y + 10, PW - 60, 34]},
            thumb_t=0.5, bg="e8e8ee",
            description="A thin vertical accent line draws on, then a translucent plate reveals beside it."),
    Variant("underline", "Underline", uc, "intro-hold-outro", text_area=ua["name"], text_areas=ua, thumb_t=0.5,
            bg="e8e8ee",
            description="A dot pops and an underline shoots out of it; the name band rises out of the line and "
                        "the subtitle band drops below it."),
    Variant("capsule", "Capsule", cc, "intro-hold-outro", text_area=ca["name"], text_areas=ca, thumb_t=0.5,
            bg="e8e8ee",
            description="An accent ring spins in on the left and a rounded frosted capsule stretches out of it."),
])
