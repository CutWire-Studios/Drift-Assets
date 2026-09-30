from _common import *
from _lt2 import rrect, poly, lay, slide, fade, SPRING, BACK_IN
from drift_lottie import Variant, build_asset

W, H = 1080, 220
K = 0.26  # horizontal slant per px of height


def para(x, y, w, h):
    """Parallelogram leaning right; (x, y+h) is the bottom-left corner."""
    s = h * K
    return path(bezier([(x + s, y), (x + w + s, y), (x + w, y + h), (x, y + h)]))


def x_at(x_bottom, y_bottom, y):
    return x_bottom + (y_bottom - y) * K


TOP, MH = 36, 100
SUB_Y, SH = TOP + MH + 6, 44
BOT = SUB_Y + SH
AX, AW = 26, 120                                   # accent block, full height, bottom-left x
MX = x_at(AX + AW + 14, BOT, TOP + MH)
MW = 820
SX = x_at(AX + AW + 14, BOT, BOT)
SW = 540


def slots(comp):
    comp.slot("accent", "#FFD100")
    comp.slot("primary", "#12161F")
    comp.slot("secondary", "#E4002B")


def classic():
    """Slanted bars slam in with a staggered diagonal wipe and a glint."""
    comp = Comp("lower-third-slant-sports", W, H, fps=FPS, frames=FRAMES)
    slots(comp)
    comp.marker("intro", 0, 42)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)

    def wiped(name, x, y, w, h, slot, t_in, t_out, dur_in=14, dur_out=12, slide=70, opacity=100):
        far = -(w + h * K + 140)
        comp.layer(f"{name}-matte", [para(x - 200, y, w + 200, h), fill("#FFFFFF")],
                   position=io([far, 0], [0, 0], t_in, t_in + dur_in, t_out, t_out + dur_out, EXPO_OUT, EXPO_IN))
        comp.layer(name, [para(x, y, w, h), fill(slot=slot, opacity=opacity)], matte="alpha",
                   position=io([-slide, 0], [0, 0], t_in, t_in + dur_in + 4, t_out, t_out + dur_out,
                               EXPO_OUT, EXPO_IN))

    wiped("accent", AX, TOP, AW, BOT - TOP, "accent", 0, 136, 14, 12)

    # glint across the name bar
    comp.layer("glint-matte", [para(MX, TOP, MW, MH), fill("#FFFFFF")])
    comp.layer("glint", [para(0, TOP, 70, MH), para(90, TOP, 16, MH), fill("#FFFFFF", opacity=14)],
               matte="alpha",
               position=keys((16, [MX - 160, 0], (0.45, 0, 0.3, 1)), (42, [MX + MW + 40, 0])))

    comp.layer("stripe", [para(MX + MH * K - 6 * K, TOP - 6, 180, 6), fill(slot="accent")],
               anchor=(MX, 0), position=(MX, 0),
               opacity=io(0, 100, 12, 13, 124, 125, HOLD, HOLD),
               scale=io([0, 100], [100, 100], 12, 28, 124, 132, EXPO_OUT, EXPO_IN))

    wiped("main", MX, TOP, MW, MH, "primary", 4, 128, 16, 12)
    wiped("sub", SX, SUB_Y, SW, SH, "secondary", 9, 122, 16, 12)
    return comp


def arrow(x, y, w, h, p, notch=0, name="arrow"):
    """Right-pointing arrow block (tip depth p); notch cuts a matching chevron into the left side."""
    return poly([(x, y), (x + w - p, y), (x + w, y + h / 2), (x + w - p, y + h), (x, y + h), (x + notch, y + h / 2)],
                name=name)


def chevron():
    """Arrow-tipped blocks rush in from the left one after another, each trailing two ghost copies."""
    comp = Comp("lower-third-slant-sports--chevron", W, H, fps=FPS, frames=FRAMES)
    slots(comp)
    comp.marker("intro", 0, 34)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    top, bot = 34, 190
    ax, aw = 26, 150
    mx, my, mw, mh = 196, 34, 800, 100
    sx, sy, sw, sh = 196, 142, 540, 48
    parts = [("accent", lambda: [arrow(ax, top, aw, bot - top, 40, 0)], "accent", 0, 134, ax + aw),
             ("main", lambda: [arrow(mx - 34, my, mw + 34, mh, 34, 34)], "primary", 5, 128, mx + mw),
             ("sub", lambda: [arrow(sx - 24, sy, sw + 24, sh, 24, 24)], "secondary", 10, 122, sx + sw)]
    for nm, geo, slot, t0, t2, right in parts:
        far = -(right + 40)
        rush = keys((0, [far, 0], HOLD), (t0, [far, 0], EXPO_OUT), (t0 + 16, [0, 0], HOLD), (t2, [0, 0], EXPO_IN),
                    (t2 + 14, [W - right + 300, 0]))
        lay(comp, nm, geo() + [fill(slot=slot)], off=rush)
        # ghosts lag behind the block only while it moves
        for g, (lag, op) in enumerate(((3, 45), (6, 22))):
            lay(comp, f"{nm}-ghost{g}", geo() + [fill(slot=slot, opacity=op)],
                off=keys((0, [far, 0], HOLD), (t0 + lag, [far, 0], EXPO_OUT), (t0 + 16 + lag, [0, 0], HOLD),
                         (t2 + lag, [0, 0], EXPO_IN), (t2 + 14 + lag, [W - right + 300, 0])),
                opacity=keys((0, 0, HOLD), (t0, 100, HOLD), (t0 + 16 + lag, 0, HOLD), (t2, 100, HOLD),
                             (t2 + 14 + lag, 0, HOLD)), ip=0, op=FRAMES)
    comp.layer("shadow", [arrow(mx - 34 + 5, my + 7, mw + 34, mh, 34, 34), arrow(sx - 24 + 5, sy + 7, sw + 24, sh, 24, 24),
                          fill("#000000", 18)], opacity=fade(22, 32, 118, 124))
    return comp, {"name": [mx + 26, my + 14, mw - 90, mh - 28], "subtitle": [sx + 22, sy + 6, sw - 70, sh - 12],
                  "badge": [ax + 20, top + 30, aw - 80, bot - top - 60]}


def drop():
    """Back-slanted bars drop in from above one by one and land with a squash; the badge spins in."""
    comp = Comp("lower-third-slant-sports--drop", W, H, fps=FPS, frames=FRAMES)
    slots(comp)
    comp.marker("intro", 0, 40)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    k = -0.26

    def bpara(x, y, w, h):
        s = h * k
        return poly([(x + s, y), (x + w + s, y), (x + w, y + h), (x, y + h)])

    bx, by, bs = 100, 108, 132          # badge square centre / size
    mx, my, mw, mh = 214, 30, 820, 100
    sx, sy, sw, sh = 190, 138, 560, 46
    c = (bx, by)
    comp.layer("badge-core", [rect((bs * 0.46, bs * 0.46), c), fill(slot="primary")], anchor=c, position=c,
               rotation=keys((4, 135, EXPO_OUT), (22, 45, HOLD), (126, 45, EXPO_IN), (138, 180)),
               scale=keys((4, [0, 0], SPRING), (18, [100, 100], HOLD), (126, [100, 100], EXPO_IN), (136, [0, 0])))
    comp.layer("badge", [rect((bs, bs), c, 14), fill(slot="accent")], anchor=c, position=c,
               rotation=keys((0, -135, EXPO_OUT), (18, 45, HOLD), (130, 45, EXPO_IN), (142, 225)),
               scale=keys((0, [0, 0], SPRING), (14, [100, 100], HOLD), (130, [100, 100], EXPO_IN), (142, [0, 0])))

    def fall(name, shapes, pivot, t0, t2, lift):
        lay(comp, name, shapes, pivot,
            off=keys((0, [0, -lift], HOLD), (t0, [0, -lift], (0.55, 0, 0.9, 0.5)), (t0 + 9, [0, 0], EASE_OUT),
                     (t0 + 14, [0, -10], EASE_IN), (t0 + 19, [0, 0], HOLD), (t2, [0, 0], BACK_IN), (t2 + 12, [0, lift])),
            scale=keys((t0 + 8, [100, 100], EASE_OUT), (t0 + 10, [103, 88], EASE_OUT), (t0 + 16, [100, 100])),
            opacity=keys((0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 4, 100, HOLD), (t2 + 6, 100, EASE_IN), (t2 + 12, 0)))

    fall("sub", [bpara(sx, sy, sw, sh), fill(slot="secondary")], (sx + sw / 2, sy + sh), 6, 120, 120)
    fall("main", [bpara(mx, my, mw, mh), fill(slot="primary")], (mx + mw / 2, my + mh), 12, 124, 160)
    fall("chip", [bpara(sx + sw + 16, sy, 110, sh), fill(slot="accent")], (sx + sw + 70, sy + sh), 18, 116, 90)
    return comp, {"name": [mx + 20, my + 14, mw - 70, mh - 28], "subtitle": [sx + 14, sy + 6, sw - 50, sh - 12],
                  "badge": [bx - 30, by - 30, 60, 60]}


cc, ca = chevron()
dc, da = drop()
AREAS = {"name": [MX + 44, TOP + 14, MW - 70, MH - 28], "subtitle": [SX + 30, SUB_Y + 6, SW - 50, SH - 12],
         "badge": [AX + 36, TOP + 30, AW - 36, BOT - TOP - 60]}
build_asset("lower-thirds", "lower-third-slant-sports", "Slant Sports Lower Third",
            "Energetic sports lower third with a name bar, a subtitle bar and an accent badge block for a number "
            "or logo.",
            ["lower third", "sports", "slant", "name", "player", "dynamic", "broadcast"], [
    Variant("classic", "Slant Wipe", classic(), "intro-hold-outro", text_area=AREAS["name"], text_areas=AREAS,
            thumb_t=0.5, bg="e8e8ee",
            description="Slanted bars slam in with a staggered diagonal wipe and a glint."),
    Variant("chevron", "Chevron Rush", cc, "intro-hold-outro", text_area=ca["name"], text_areas=ca, thumb_t=0.5,
            bg="e8e8ee",
            description="Arrow-tipped chevron blocks rush in from the left one after another, trailing ghost "
                        "copies, and fly off to the right."),
    Variant("drop", "Stack Drop", dc, "intro-hold-outro", text_area=da["name"], text_areas=da, thumb_t=0.5,
            bg="e8e8ee",
            description="Back-slanted bars drop in from above and land with a squash while a diamond badge spins "
                        "in."),
])
