"""Shared parts for the retro_a retrofit batch (variants added to older call-to-action assets).

follow_extras(p) returns the platform pack's second look (glass card or outline pill) and its icon-pop
variant for an older follow button whose own design stays the default, so those buttons match the
newer platform follow buttons in _platforms.py. `chroma` adds TikTok's cyan/red offset copies of the
glyph to the platform icon.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _platforms as P  # noqa: E402
from _common import glyph  # noqa: E402
from drift_lottie import Variant  # noqa: E402
from lottie_kit import anim, fill, group, SNAP_OUT, HOLD  # noqa: E402

_icon_shapes = P.icon_shapes


def chroma(offset=2.4, colors=("#FE2C55", "#25F4EE")):
    """Patch _platforms' icon so tile icons get two offset tinted glyph copies under the white one."""
    def shapes(p, size=P.IS, t0=6):
        items = _icon_shapes(p, size, t0)
        s = size * p.icon_scale
        gs = s * p.glyph_size
        pop = dict(scale=anim([(t0, [0, 0], P.SPRING), (t0 + 14, [100, 100])]),
                   rotation=anim([(t0, -30, SNAP_OUT), (t0 + 16, 0)]))
        extra = []
        for sign, col in zip((1, -1), colors):
            d = offset * s / 128 * sign
            jit = anim([(t0 + 2, [d * 5, -d * 2], HOLD), (t0 + 5, [-d * 3, d * 3], HOLD), (t0 + 8, [d * 2, d], HOLD),
                        (t0 + 11, [d, d])])
            extra.append(group([group(glyph(p.glyph, gs) + [fill(col)], "glyph", position=jit)], f"chroma{sign}", **pop))
        return items[:1] + extra + items[1:]
    P.icon_shapes = shapes


def follow_extras(p):
    """[second look, icon-pop] Variants for Platform p (p.second picks glass or outline)."""
    if p.second == "glass":
        second = Variant("glass", "Glass Card", P.glass(p), "intro-hold-outro", thumb_t=0.3, bg=p.glass_bg,
                         text_area=(P.ICON[0] + P.IS / 2 + 30, P.Y - 50, P.W - 40 - P.IS - 90, 100),
                         description="Frosted glass card with the app icon; a sheen sweeps across and a check "
                                     "pops on the icon after the click.")
    else:
        second = Variant("outline", "Outline", P.outline(p), "intro-hold-outro", thumb_t=0.3, bg=p.bg,
                         text_area=P.PILL_TEXT,
                         description="The app icon springs in and a white outline draws on around the pill; the "
                                     "click floods it with the brand colour.")
    pop = Variant("icon-pop", "Icon Pop", P.icon_pop(p), "intro-hold-outro", thumb_t=0.8, bg=p.bg,
                  description="Just the app icon with a plus badge that flips to a check when clicked; no text area.")
    return [second, pop]
