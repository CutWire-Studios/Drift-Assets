"""Text as vector outlines, so Lottie assets can carry real words without text layers or fonts.

    from text_paths import text, text_width
    shapes = text("Message", x=40, y=100, size=34, weight=500)   # baseline-left at (x, y)
    group(shapes + [fill(slot="icon")], "label")

Glyphs come from Inter (SIL OFL 1.1, tools/lottie/fonts/). Every glyph path ends up inside one
group, so counters (the hole in "o") work with a plain non-zero fill. No kerning, tracking is
optional. Use it for UI chrome words ("Message", "Reply", "5G"); leave content text to the user.
"""

import os
from functools import lru_cache

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from lottie_kit import svg_path, path

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


@lru_cache(maxsize=None)
def _font(weight):
    f = TTFont(os.path.join(FONT_DIR, f"Inter-{weight}.woff"))
    return f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm


def text_width(s, size, weight=400, tracking=0.0):
    f, _, cmap, upm = _font(weight)
    hmtx = f["hmtx"]
    return sum(hmtx[cmap.get(ord(c), cmap[ord("?")])][0] for c in s) * size / upm + tracking * size * len(s)


def text(s, x, y, size, weight=400, anchor="l", tracking=0.0, name="text"):
    """Path shapes for `s` with its baseline at y. anchor: l / c / r about x. tracking in em."""
    f, gs, cmap, upm = _font(weight)
    hmtx = f["hmtx"]
    k = size / upm
    w = text_width(s, size, weight, tracking)
    pen_x = x - (w / 2 if anchor == "c" else w if anchor == "r" else 0)
    shapes = []
    for ch in s:
        g = cmap.get(ord(ch), cmap[ord("?")])
        if ch != " ":
            sp = SVGPathPen(gs)
            gs[g].draw(TransformPen(sp, (k, 0, 0, -k, pen_x, y)))
            d = sp.getCommands()
            if d:
                shapes += [path(b, f"{name}-{ch}") for b in svg_path(d)]
        pen_x += hmtx[g][0] * k + tracking * size
    return shapes
