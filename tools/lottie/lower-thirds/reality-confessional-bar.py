from _common import *
from _lt2 import rrect, lay, slide, fade, sparkle, rect_grow, SPRING, BACK_IN
from drift_lottie import Variant, build_asset

W, H = 900, 200
LX, LW = 30, 8
BX = LX + LW
TOP, NH = 40, 78
SUB_Y, SH = TOP + NH, 42
NW, SW = 800, 470
SOFT = (0.25, 0.8, 0.3, 1.0)
AWAY = (0.6, 0.0, 0.9, 0.5)


def base(name, intro_end):
    comp = Comp(name, W, H, fps=FPS, frames=FRAMES)
    comp.slot("accent", "#FF6F61")
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#FF8FA3")
    comp.marker("intro", 0, intro_end)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    return comp


def classic():
    """Soft translucent name bar and pink subtitle plate glide in beside a coral accent line."""
    comp = base("reality-confessional-bar", 36)
    full = SUB_Y + SH - TOP
    comp.layer("line", [rect((LW, full), (LW / 2, 0), roundness=LW / 2), fill(slot="accent")],
               anchor=(0, 0), position=(LX, TOP + full / 2),
               scale=io([100, 0], [100, 100], 0, 16, 134, 148, EXPO_OUT, INOUT))

    def soft_bar(name, y, w, h, slot, opacity, t0, t2, r):
        comp.layer(f"{name}-clip", [rect((W, h + 4), (BX + W / 2, y + h / 2)), fill("#FFFFFF")])
        comp.layer(name, [rect((w + r, h), (BX + (w - r) / 2, y + h / 2), roundness=r), fill(slot=slot)],
                   matte="alpha",
                   position=io([-140, 0], [0, 0], t0, t0 + 26, t2, t2 + 16, SOFT, AWAY),
                   opacity=io(0, opacity, t0, t0 + 14, t2 + 4, t2 + 16, EASE_OUT, EASE_IN))

    soft_bar("name", TOP, NW, NH, "primary", 86, 5, 124, 14)
    soft_bar("sub", SUB_Y, SW, SH, "secondary", 100, 10, 120, SH / 2)
    return comp


def bubble():
    """Speech-bubble name plate springs out of its tail; the subtitle chip pops after it, slightly tilted."""
    comp = base("reality-confessional-bar--bubble", 34)
    bx, by, bw, bh, r = 40, 22, 780, 88, 30
    tail = [(bx + 46, by + bh - 2), (bx + 38, by + bh + 26), (bx + 84, by + bh - 2)]
    piv = (bx + 40, by + bh + 24)
    sx, sy, sw, sh = 110, 136, 440, 44
    grow = keys((2, [0, 0], OVERSHOOT), (20, [100, 100], HOLD), (122, [100, 100], EASE_OUT), (127, [104, 104], BACK_IN),
                (138, [0, 0]))
    lay(comp, "bubble", [rrect(bx, by, bw, bh, r), polyline(tail, closed=True), fill(slot="primary", opacity=92)],
        piv, scale=grow, rotation=keys((2, -8, SPRING), (22, 0)))
    lay(comp, "bubble-shadow", [rrect(bx, by + 6, bw, bh, r), polyline([(x, y + 6) for x, y in tail], closed=True),
                                fill("#000000", 14)], piv, scale=grow, rotation=keys((2, -8, SPRING), (22, 0)))
    c = (sx + sw / 2, sy + sh / 2)
    lay(comp, "dot", [ellipse((16, 16), (sx + 26, c[1])), fill(slot="primary")], c,
        scale=keys((14, [0, 0], SPRING), (28, [100, 100], HOLD), (116, [100, 100], BACK_IN), (128, [0, 0])),
        rotation=keys((10, 10, SPRING), (26, -2, HOLD)))
    lay(comp, "chip", [rrect(sx, sy, sw, sh, sh / 2), fill(slot="secondary")], c,
        scale=keys((10, [0, 0], SPRING), (26, [100, 100], HOLD), (116, [100, 100], BACK_IN), (128, [0, 0])),
        rotation=keys((10, 10, SPRING), (26, -2, HOLD)))
    lay(comp, "chip-accent", [rrect(sx - 8, sy + 6, sw, sh, sh / 2), fill(slot="accent")], c,
        scale=keys((13, [0, 0], SPRING), (29, [100, 100], HOLD), (113, [100, 100], BACK_IN), (125, [0, 0])),
        rotation=keys((13, 10, SPRING), (29, -2, HOLD)))
    return comp, {"name": [bx + 34, by + 14, bw - 68, bh - 28], "subtitle": [sx + 46, sy + 6, sw - 80, sh - 12]}


def sparkle_bars():
    """Rounded bars glide in from the right in a soft stagger while little sparkles twinkle on the corner."""
    comp = base("reality-confessional-bar--sparkle", 40)
    nx, ny, nw, nh = 60, 42, 740, 76
    sx, sy, sw, sh = 60, 126, 450, 40
    # sparkles twinkle in and out around the top-right corner of the name bar
    for i, (x, y, rr, t) in enumerate(((nx + nw + 22, ny - 4, 24, 18), (nx + nw + 60, ny + 26, 14, 24),
                                       (nx + nw - 16, ny - 24, 11, 30))):
        tw = [(0, [0, 0], HOLD), (t, [0, 0], SPRING), (t + 10, [100, 100], EASE_IN_OUT)]
        for k in range(t + 22, 110, 24):
            tw += [(k, [100, 100], EASE_IN_OUT), (k + 6, [55, 55], EASE_IN_OUT), (k + 12, [100, 100], EASE_IN_OUT)]
        tw += [(116 + i * 2, [100, 100], BACK_IN), (126 + i * 2, [0, 0])]
        lay(comp, f"sparkle{i}", [sparkle(x, y, rr), fill(slot="accent" if i != 1 else "secondary")], (x, y),
            scale=keys(*tw), rotation=keys((t, -90, EXPO_OUT), (t + 16, 0)))
    lay(comp, "heart-dot", [ellipse((20, 20), (nx + 34, ny + nh / 2)), fill(slot="accent")], (nx + 34, ny + nh / 2),
        scale=keys((14, [0, 0], SPRING), (26, [100, 100], HOLD), (120, [100, 100], EASE_IN), (128, [0, 0])))
    for nm, box, slot, op, t0, t2, r in (("name", (nx, ny, nw, nh), "primary", 88, 4, 122, nh / 2),
                                         ("sub", (sx, sy, sw, sh), "secondary", 100, 11, 116, sh / 2)):
        x, y, w, h = box
        lay(comp, nm, [rrect(x, y, w, h, r), fill(slot=slot, opacity=op)],
            off=slide(160, 0, t0, t0 + 28, t2, t2 + 18, SOFT, AWAY, odx=-60),
            opacity=fade(t0, t0 + 12, t2 + 6, t2 + 18))
    return comp, {"name": [nx + 60, ny + 12, nw - 96, nh - 24], "subtitle": [sx + 24, sy + 5, sw - 48, sh - 10]}


bc, ba = bubble()
sc, sa = sparkle_bars()
build_asset("lower-thirds", "reality-confessional-bar", "Reality Confessional Bar",
            "Reality-TV confessional lower third: a soft light name plate with a coral accent and a pink subtitle "
            "plate.",
            ["lower third", "reality tv", "confessional", "name", "interview", "soft", "pink"], [
    Variant("classic", "Soft Glide", classic(), "intro-hold-outro",
            text_area=[BX + 24, TOP + 10, NW - 48, NH - 20],
            text_areas={"name": [BX + 24, TOP + 10, NW - 48, NH - 20], "subtitle": [BX + 24, SUB_Y + 5, SW - 48, SH - 10]},
            thumb_t=0.5,
            description="A soft semi-transparent white name bar with a coral accent line and a pink subtitle plate."),
    Variant("bubble", "Speech Bubble", bc, "intro-hold-outro", text_area=ba["name"], text_areas=ba, thumb_t=0.5,
            description="Speech-bubble name plate springs out of its tail and a tilted two-tone subtitle chip pops "
                        "in under it."),
    Variant("sparkle", "Sparkle", sc, "intro-hold-outro", text_area=sa["name"], text_areas=sa, thumb_t=0.5,
            description="Rounded capsules glide in from the right in a soft stagger while little sparkles twinkle "
                        "on the corner."),
])
