from _common import *

W, H = 1400, 246
X0, X1 = 30, 1370
TAG_Y, TAG_H, TAG_W = 30, 62, 340
LINE_Y, LINE_H = TAG_Y + TAG_H, 4
BAR_Y, BAR_H = LINE_Y + LINE_H, 86
STRIP_Y, STRIP_H = BAR_Y + BAR_H, 38
BW = X1 - X0
POP = (0.34, 1.35, 0.64, 1.0)

comp = Comp("breaking-news-lower-third", W, H, fps=FPS, frames=FRAMES)
comp.slot("accent", "#CC0000")
comp.slot("primary", "#FFFFFF")
comp.slot("secondary", "#0A1A3A")


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

comp.layer("tag-matte", [rect((TAG_W + 40, TAG_H + 30 + LINE_H), (X0 + TAG_W / 2 + 20, TAG_Y + (TAG_H + LINE_H) / 2 - 15)),
                         fill("#FFFFFF")])
comp.layer("tag", [rect((TAG_W, TAG_H + 20), (X0 + TAG_W / 2, TAG_Y + TAG_H / 2 + 10)), fill(slot="accent")],
           matte="alpha",
           position=io([0, TAG_H + 4], [0, 0], 12, 26, 120, 130, POP, EXPO_IN))

from_left("bar", BAR_Y, BAR_H, "primary", 0, 18, 128, 142)
from_left("strip", STRIP_Y, STRIP_H, "secondary", 5, 23, 124, 138)

build(comp, "breaking-news-lower-third", "Breaking News Lower Third",
      "TV news lower third: red tag block for the label, white headline bar and a dark strip, with a glint sweep.",
      ["breaking news", "news", "lower third", "headline", "tv", "broadcast", "live"],
      {"headline": [X0 + 26, BAR_Y + 10, BW - 52, BAR_H - 20],
       "subtitle": [X0 + 26, STRIP_Y + 5, BW - 52, STRIP_H - 10],
       "tag": [X0 + 20, TAG_Y + 10, TAG_W - 40, TAG_H - 20]},
      thumb_t=0.5, intro_end=26)
