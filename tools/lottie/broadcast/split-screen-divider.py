import math

from _broadcast2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 90
INTRO, OUTRO = 30, 72
BADGE = (C[0] - 90, C[1] - 64, 180, 128)


def base(name):
    c = Comp(name, W, H, fps=30, frames=F)
    c.marker("intro", 0, INTRO)
    c.marker("outro", OUTRO, F - OUTRO)
    return c


def badge_scale(t0=10):
    return keys((t0, [0, 0], SPRING), (t0 + 16, [100, 100], HOLD), (OUTRO, [100, 100], BACK_IN), (OUTRO + 10, [0, 0]))


def draw(t0, t1, t2=OUTRO + 4, t3=F - 4):
    return keys((t0, 0, EXPO_OUT), (t1, 50, HOLD), (t2, 50, EXPO_IN), (t3, 0))


def vertical():
    """Glowing vertical divider draws from both ends to the centre, where a round VS badge pops."""
    comp = base("split-screen-divider")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", "#FF2E5B")
    comp.slot("icon", "#FFFFFF")
    top = polyline([(C[0], 0), (C[0], C[1])])
    bot = polyline([(C[0], H), (C[0], C[1])])
    comp.layer("badge", [group([ellipse((190, 190), C), fill(slot="primary")], "disc"),
                         group([ellipse((190, 190), C), stroke(slot="icon", width=8)], "rim"),
                         group([ellipse((226, 226), C), fill("#000000", 30)], "shadow")],
               anchor=C, position=C, scale=badge_scale(12),
               rotation=keys((12, -30, EXPO_OUT), (30, 0)))
    comp.layer("badge ring", [group([ellipse((190, 190), C), stroke(slot="primary", width=6)], "ring")],
               anchor=C, position=C, ip=16, op=40,
               scale=keys((16, [100, 100], EXPO_OUT), (40, [190, 190])), opacity=keys((16, 90, EASE_IN), (40, 0)))
    for nm, ln in (("top", top), ("bottom", bot)):
        tr = trim(end=keys((0, 0, EXPO_OUT), (18, 100, HOLD), (OUTRO + 6, 100, EXPO_IN), (F - 2, 0)))
        comp.layer(nm, glow_strokes([ln], slot="outline", width=10, extra=[tr], cap="butt"))
    comp.layer("shade", [box(C[0] - 30, 0, 60, H, "#000000", opacity=18)],
               opacity=keys((0, 0, EASE_OUT), (18, 100, HOLD), (OUTRO + 6, 100, EASE_IN), (F - 2, 0)))
    return comp


def diagonal():
    """Slanted double-line divider with a light streak running along it and a diamond badge."""
    comp = base("split-screen-divider--diagonal")
    comp.slot("outline", "#FFFFFF")
    comp.slot("accent", "#FFC21A")
    comp.slot("primary", "#1D1D24")
    dx = 240  # horizontal lean
    a, b = (C[0] + dx, -20), (C[0] - dx, H + 20)
    ln = polyline([a, b])
    ln2 = polyline([(a[0] + 22, a[1]), (b[0] + 22, b[1])])
    tr = trim(start=keys((0, 0, HOLD), (OUTRO, 0, EXPO_IN), (F - 2, 100)), end=keys((0, 0, EXPO_OUT), (20, 100)))
    tr2 = trim(start=keys((0, 0, HOLD), (OUTRO + 3, 0, EXPO_IN), (F, 100)), end=keys((4, 0, EXPO_OUT), (24, 100)))
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) - 90
    comp.layer("badge", [group([rect((190, 190), C, 18), fill(slot="primary")], "d", anchor=C, position=C, rotation=45),
                         group([rect((190, 190), C, 18), stroke(slot="accent", width=7)], "rim", anchor=C,
                               position=C, rotation=45)],
               anchor=C, position=C, scale=badge_scale(14), rotation=keys((14, -90, EXPO_OUT), (32, 0)))
    comp.layer("streak", [group([polyline([(0, -120), (0, 120)]), stroke("#FFFFFF", width=10, opacity=90)], "s"),
                          group([polyline([(0, -120), (0, 120)]), stroke(slot="accent", width=34, opacity=25)], "g")],
               rotation=ang, position=keys((22, list(a), EASE_IN_OUT), (52, list(b))), ip=22, op=53)
    comp.layer("line", glow_strokes([ln], slot="outline", width=10, extra=[tr], cap="butt"))
    comp.layer("line2", [group([ln2, tr2, stroke(slot="accent", width=6, cap="butt")], "l2")])
    return comp


def framed():
    """Two rounded picture frames slide in from the sides with a gap between them and a pill badge."""
    comp = base("split-screen-divider--framed")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", "#6C4DFF")
    comp.slot("background", "#101016")
    g, m = 36, 40
    fw, fh = (W - 2 * m - g) / 2, H - 2 * m
    L = rect_tl(m, m, fw, fh, 36)
    R = rect_tl(m + fw + g, m, fw, fh, 36)
    comp.layer("badge", [group([rect((210, 120), C, 60), fill(slot="primary")], "pill"),
                         group([rect((210, 120), C, 60), stroke(slot="outline", width=6)], "rim"),
                         group([rect((240, 150), C, 75), fill(slot="background")], "gap")],
               anchor=C, position=C, scale=badge_scale(16))
    for nm, shp, sgn in (("left", L, -1), ("right", R, 1)):
        pos = keys((0, [sgn * 140, 0], EXPO_OUT), (22, [0, 0], HOLD), (OUTRO, [0, 0], EXPO_IN), (F - 2, [sgn * 140, 0]))
        op = fade(0, 8, OUTRO + 8, F - 2)
        comp.layer(nm, [group([shp, stroke(slot="outline", width=8)], "frame")], position=pos, opacity=op)
    # background fills everything outside the two frames (even-odd)
    comp.layer("surround", [group([rect((W + 4, H + 4), C), L, R, fill(slot="background", even_odd=True)], "bg")],
               opacity=fade(0, 10, OUTRO + 6, F - 2))
    return comp


build_asset(CAT, "split-screen-divider", "Split Screen Divider",
            "Full-frame split-screen overlay: an animated divider between two halves with a centre badge ready "
            "for VS or OR. It animates in, holds (stretchable) and animates out.",
            ["split screen", "divider", "versus", "vs", "comparison", "side by side", "before after", "reaction"], [
    V("vertical", "Vertical", vertical(), "intro-hold-outro", text_area=BADGE, thumb_t=0.5, bg="5d6780",
      description="Glowing vertical line draws in from both ends; a round badge spins in at the centre."),
    V("diagonal", "Diagonal", diagonal(), "intro-hold-outro", text_area=(C[0] - 70, C[1] - 50, 140, 100),
      thumb_t=0.5, bg="5d6780",
      description="Slanted double line with a light streak running along it and a diamond badge."),
    V("framed", "Framed Panels", framed(), "intro-hold-outro", text_area=(C[0] - 80, C[1] - 44, 160, 88),
      thumb_t=0.5, bg="5d6780",
      description="Two rounded frames slide in side by side on a dark surround, with a pill badge between them."),
])
