"""Pixel-art "deal with it" sunglasses drop in from the top and snap into place (intro-hold)."""

from _common import *

T = 45
W, H = 600, 200
P = 16
BLACK, WHITE = "#000000", "#FFFFFF"

GRID = [
    "################################",
    "  ############################  ",
    "  ##WW#W######    ##WW#W######  ",
    "  ###WW#W#####    ###WW#W#####  ",
    "  ############    ############  ",
    "   ##########      ##########   ",
    "    ########        ########    ",
]

comp = Comp("thug-life-sunglasses-drop", W, H, fps=30, frames=T)
comp.slot("primary", BLACK)
comp.slot("secondary", WHITE)

cols, rows = len(GRID[0]), len(GRID)
ox, oy = -cols * P / 2, -rows * P / 2


Y = 104
comp.layer("glasses", [
    group(pixel_outline(GRID, lambda ch: ch == "W", P, (ox, oy)) + [fill(WHITE, slot="secondary")],
          name="shine"),
    group(pixel_outline(GRID, lambda ch: ch != " ", P, (ox, oy)) + [fill(BLACK, slot="primary")],
          name="frame"),
],
    position=anim([(0, (W / 2, -80), EASE_IN), (13, (W / 2, Y), EASE_OUT), (18, (W / 2, Y - 16), EASE_IN),
                   (23, (W / 2, Y), EASE_OUT), (26, (W / 2, Y - 4), EASE_IN), (29, (W / 2, Y))]),
    rotation=anim([(0, -7, EASE_IN), (13, 0, EASE_OUT), (18, 1.5, EASE_IN_OUT), (26, 0)]),
    scale=anim([(0, (100, 100), HOLD), (12, (100, 100), EASE_OUT), (14, (104, 94), EASE_IN_OUT),
                (19, (99, 102), EASE_IN_OUT), (24, (100, 100))]),
    anchor=(0, rows * P / 2))

comp.layers[-1]["ks"]["p"] = anim([(0, (W / 2, -80 + rows * P / 2), EASE_IN),
                                  (13, (W / 2, Y + rows * P / 2), EASE_OUT),
                                  (18, (W / 2, Y - 16 + rows * P / 2), EASE_IN),
                                  (23, (W / 2, Y + rows * P / 2), EASE_OUT),
                                  (26, (W / 2, Y - 4 + rows * P / 2), EASE_IN),
                                  (29, (W / 2, Y + rows * P / 2))]).lottie()

build(comp, "memes", "thug-life-sunglasses-drop", "Deal With It Sunglasses",
      "Black pixel-art sunglasses drop from the top and snap into place with a tiny bounce, then "
      "hold. Place over a face.",
      ["sunglasses", "deal with it", "thug life", "pixel", "meme", "cool", "glasses"],
      "intro-hold", 1.0, bg="e8e8ee")
