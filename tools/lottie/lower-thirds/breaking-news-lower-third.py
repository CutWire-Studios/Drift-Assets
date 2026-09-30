from _common import *
from _lt2 import rrect, para, chamfer, lay, slide, fade, rect_grow, sheen, SPRING, BACK_IN
from drift_lottie import Variant, build_asset

W, H = 1400, 246
X0, X1 = 30, 1370
TAG_Y, TAG_H, TAG_W = 30, 62, 340
LINE_Y, LINE_H = TAG_Y + TAG_H, 4
BAR_Y, BAR_H = LINE_Y + LINE_H, 86
STRIP_Y, STRIP_H = BAR_Y + BAR_H, 38
BW = X1 - X0
POP = (0.34, 1.35, 0.64, 1.0)
AREAS = {"headline": [X0 + 26, BAR_Y + 10, BW - 52, BAR_H - 20],
         "subtitle": [X0 + 26, STRIP_Y + 5, BW - 52, STRIP_H - 10],
         "tag": [X0 + 20, TAG_Y + 10, TAG_W - 40, TAG_H - 20]}


def base(name, intro_end):
    comp = Comp(name, W, H, fps=FPS, frames=FRAMES)
    comp.slot("accent", "#CC0000")
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#0A1A3A")
    comp.marker("intro", 0, intro_end)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    return comp


def classic():
    """Red tag, white headline bar and dark strip wipe in from the left, with a glint."""
    comp = base("breaking-news-lower-third", 26)

    def from_left(name, y, h, slot, t0, t1, t2, t3, w=BW, ein=EXPO_OUT, eout=INOUT):
        comp.layer(name, [rect((w, h), (w / 2, 0)), fill(slot=slot)], anchor=(0, 0), position=(X0, y + h / 2),
                   scale=io([0, 100], [100, 100], t0, t1, t2, t3, ein, eout))

    # glint over the tag and the strip
    comp.layer("glint-matte", [rect((TAG_W, TAG_H), (X0 + TAG_W / 2, TAG_Y + TAG_H / 2)),
                               rect((BW, STRIP_H), (X0 + BW / 2, STRIP_Y + STRIP_H / 2)), fill("#FFFFFF")])
    sweep = (0.45, 0.0, 0.35, 1.0)
    comp.layer("glint", [group([rect((90, 420)),
                                gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.5), (1, "#FFFFFF", 0)],
                                              (-45, 0), (45, 0))], rotation=22)],
               matte="alpha",
               position=keys((24, [-120, H / 2], sweep), (60, [W + 120, H / 2], HOLD),
                             (84, [-120, H / 2], sweep), (120, [W + 120, H / 2])))

    from_left("line", LINE_Y, LINE_H, "accent", 2, 20, 130, 144)

    comp.layer("tag-matte", [rect((TAG_W + 40, TAG_H + 30 + LINE_H),
                                  (X0 + TAG_W / 2 + 20, TAG_Y + (TAG_H + LINE_H) / 2 - 15)),
                             fill("#FFFFFF")])
    comp.layer("tag", [rect((TAG_W, TAG_H + 20), (X0 + TAG_W / 2, TAG_Y + TAG_H / 2 + 10)), fill(slot="accent")],
               matte="alpha",
               position=io([0, TAG_H + 4], [0, 0], 12, 26, 120, 130, POP, EXPO_IN))

    from_left("bar", BAR_Y, BAR_H, "primary", 0, 18, 128, 142)
    from_left("strip", STRIP_Y, STRIP_H, "secondary", 5, 23, 124, 138)
    return comp


# ---------------------------------------------------------------- centre split
SX0, SX1 = 60, 1340
S_TAG = (W / 2 - 180, 24, 360, 62)
S_BAR = (SX0, 92, SX1 - SX0, 84)
S_STRIP = (W / 2 - 460, 176, 920, 40)


def split():
    """Headline bar splits open from the centre; the tag drops in on a spring with a pulsing live dot."""
    comp = base("breaking-news-lower-third--split", 34)
    bx, by, bw, bh = S_BAR
    tx, ty, tw, th = S_TAG
    sx, sy, sw, sh = S_STRIP
    # live dot in the tag: pulses twice a second through the hold
    dot = (tx + 40, ty + th / 2)
    pulse = [(0, 100, HOLD)] + [(t + d, v, EASE_IN_OUT) for t in range(32, 110, 16) for d, v in ((0, 100), (8, 30))]
    tag_off = keys((0, [0, -90], HOLD), (14, [0, -90], SPRING), (30, [0, 0], HOLD), (118, [0, 0], BACK_IN),
                   (132, [0, -90]))
    tag_op = keys((0, 0, HOLD), (14, 0, EASE_OUT), (18, 100, HOLD), (126, 100, EASE_IN), (132, 0))
    tag_tilt = keys((14, -6, EASE_OUT), (30, 0, HOLD), (118, 0, EASE_IN), (132, -6))
    lay(comp, "live-ring", [ellipse((18, 18), dot), stroke(slot="primary", width=2.5)], dot, off=tag_off,
        opacity=keys((0, 0, HOLD), *[(t + d, v, EASE_OUT) for t in range(32, 118, 16) for d, v in ((0, 90), (15, 0))],
                     (120, 0, HOLD)),
        scale=keys(*[(t + d, v, EASE_OUT) for t in range(32, 118, 16) for d, v in ((0, [100, 100]), (15, [260, 260]))]))
    lay(comp, "live-dot", [ellipse((16, 16), dot), fill(slot="primary")], (tx + tw / 2, ty + th), off=tag_off,
        rotation=tag_tilt, opacity=keys(*pulse[:1], *pulse[1:], (118, 100, HOLD), (126, 100, EASE_IN), (132, 0)))
    lay(comp, "tag", [chamfer(tx, ty, tw, th, 18, (1, 1, 0, 0)), fill(slot="accent")], (tx + tw / 2, ty + th), off=tag_off,
        rotation=tag_tilt, opacity=tag_op)
    lay(comp, "tag-shadow", [chamfer(tx, ty, tw, th, 18, (1, 1, 0, 0)), fill("#000000", 18)], (tx + tw / 2, ty + th),
        off=keys((0, [0, -84], HOLD), (14, [0, -84], SPRING), (30, [0, 6], HOLD), (118, [0, 6], BACK_IN),
                 (132, [0, -84])), rotation=tag_tilt, opacity=tag_op)
    # accent hairlines frame the bar, drawn outward from the centre
    for nm, y in (("line-top", by - 7), ("line-bot", sy + sh + 3)):
        comp.layer(nm, [rect_grow(bx, y, bw, 4, 0, 0, 18, 132, 146, "centre", start=0), fill(slot="accent")])
    sheen(comp, [rrect(bx, by, bw, bh)], bx, bx + bw, by, by + bh, 26, 60)
    comp.layer("bar", [rect_grow(bx, by, bw, bh, 0, 4, 24, 126, 142, "centre", start=0), fill(slot="primary")])
    # strip slides down from behind the bar
    comp.layer("strip-matte", [rrect(sx, by + bh, sw, sh + 8), fill("#FFFFFF")])
    lay(comp, "strip", [rrect(sx, sy, sw, sh), fill(slot="secondary")],
        off=slide(0, -sh - 6, 16, 32, 116, 128, EXPO_OUT, EXPO_IN), matte="alpha")
    lay(comp, "shadow", [rrect(bx, by + 8, bw, bh), rrect(sx, sy + 6, sw, sh), fill("#000000", 16)],
        opacity=fade(18, 30, 120, 132))
    areas = {"headline": [bx + 30, by + 10, bw - 60, bh - 20], "subtitle": [sx + 26, sy + 5, sw - 52, sh - 10],
             "tag": [tx + 64, ty + 12, tw - 100, th - 20]}
    return comp, areas


# ---------------------------------------------------------------- slanted slam
K = 0.26
G_TAG = (40, 30, 290, 170)      # full-height tag block on the left (x = bottom-left)
G_BAR = (364, 30, 970, 104)
G_STRIP = (346, 140, 740, 44)
G_LINE = (342, 190, 420, 10)


def slant():
    """Slanted blocks: the tag slams in from the left, the bars shoot in from the right, streaks trail them."""
    comp = base("breaking-news-lower-third--slant", 30)
    tx, ty, tw, th = G_TAG
    bx, by, bw, bh = G_BAR
    sx, sy, sw, sh = G_STRIP
    lx, ly, lw, lh = G_LINE

    # speed streaks ahead of the bars
    for i, (y, w, t0) in enumerate(((by + 22, 260, 6), (by + 70, 180, 9), (sy + 18, 220, 13))):
        comp.layer(f"streak{i}", [rrect(0, y, w, 5, 2.5), fill(slot="primary", opacity=70)],
                   ip=t0, op=t0 + 16,
                   position=keys((t0, [W + 40, 0], EXPO_OUT), (t0 + 16, [bx - 40, 0])),
                   opacity=keys((t0, 100, EASE_IN), (t0 + 16, 0)))
    # glint on the tag
    sheen(comp, [para(tx, ty, tw, th, K)], tx, tx + tw + 60, ty, ty + th, 30, 58, width=70, op=30)

    land = 12
    lay(comp, "tag", [para(tx, ty, tw, th, K), fill(slot="accent")], (tx, ty + th),
        off=keys((0, [-tw - 120, 0], (0.5, 0, 0.9, 0.6)), (land, [0, 0], HOLD), (128, [0, 0], BACK_IN),
                 (142, [-tw - 120, 0])),
        scale=keys((land - 1, [100, 100], EASE_OUT), (land + 3, [90, 106], EASE_IN_OUT), (land + 9, [103, 98], EASE_IN_OUT),
                   (land + 14, [100, 100])))

    def shoot(name, box, slot, t0, t2, op=100):
        x, y, w, h = box
        away = W - x + 80
        lay(comp, name, [para(x, y, w, h, K), fill(slot=slot, opacity=op)],
            off=keys((0, [away, 0], HOLD), (t0, [away, 0], EXPO_OUT), (t0 + 18, [0, 0], HOLD), (t2, [0, 0], EXPO_IN),
                     (t2 + 14, [away, 0])))

    shoot("bar", G_BAR, "primary", 4, 126)
    shoot("strip", G_STRIP, "secondary", 9, 122)
    lay(comp, "line", [para(lx, ly, lw, lh, K), fill(slot="accent")], (lx, ly + lh),
        scale=io([0, 100], [100, 100], 18, 34, 118, 130, EXPO_OUT, EXPO_IN))
    comp.layer("shadow", [para(bx + 6, by + 8, bw, bh, K), para(sx + 6, sy + 8, sw, sh, K), fill("#000000", 16)],
               opacity=fade(20, 32, 118, 128))
    areas = {"headline": [bx + 50, by + 14, bw - 80, bh - 28], "subtitle": [sx + 34, sy + 6, sw - 60, sh - 12],
             "tag": [tx + 50, ty + 50, tw - 60, th - 100]}
    return comp, areas


sc, sa = split()
lc, la = slant()
build_asset("lower-thirds", "breaking-news-lower-third", "Breaking News Lower Third",
            "TV news lower third with a red tag block for the label, a headline bar and a dark subtitle strip.",
            ["breaking news", "news", "lower third", "headline", "tv", "broadcast", "live"], [
    Variant("classic", "Classic", classic(), "intro-hold-outro", text_area=AREAS["headline"], text_areas=AREAS,
            thumb_t=0.5, description="Red tag block, white headline bar and a dark strip wipe in from the left, "
                                     "with a glint sweep."),
    Variant("split", "Centre Split", sc, "intro-hold-outro", text_area=sa["headline"], text_areas=sa, thumb_t=0.5,
            description="Centred layout: the headline bar splits open from the middle between red hairlines, the "
                        "strip slides out below and the tag drops in on a spring with a pulsing live dot."),
    Variant("slant", "Slanted Slam", lc, "intro-hold-outro", text_area=la["headline"], text_areas=la, thumb_t=0.5,
            bg="e8e8ee",
            description="Slanted blocks: a tall red tag slams in from the left while the bars shoot in from the "
                        "right behind speed streaks."),
])
