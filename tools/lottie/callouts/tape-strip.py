"""A strip of tape that slaps on at an angle."""
import math
import random

from _callouts2 import *

W, H = 400, 220
N = 30
C = (W / 2, H / 2)
TW, TH = 300, 78
TILT = -7
TEXT = (C[0] - 110, C[1] - 24, 220, 48)


def torn(seed, teeth=7, depth=7, ragged=False):
    """Tape outline centred on (0, 0) with torn zigzag ends."""
    rnd = random.Random(seed)
    h, w = TH / 2, TW / 2

    def end(x, sign):
        pts = []
        for i in range(teeth + 1):
            y = -h + TH * i / teeth
            dx = (depth if i % 2 else 0) + rnd.uniform(-2, 2)
            if ragged:
                dx = rnd.uniform(0, depth * 1.8)
            pts.append((x + sign * dx, y))
        return pts

    right = end(w, -1)
    left = end(-w, 1)[::-1]
    return right + left


def slap(t=6):
    return dict(anchor=(0, 0), position=anim([(0, [C[0] + 40, C[1] - 60], (0.55, 0.0, 0.9, 0.6)), (t, list(C))]),
                scale=anim([(0, [150, 150], (0.55, 0.0, 0.9, 0.6)), (t, [94, 94], SETTLE), (t + 4, [102, 102], SETTLE),
                            (t + 9, [100, 100])]),
                rotation=anim([(0, TILT - 22, (0.55, 0.0, 0.9, 0.6)), (t, TILT + 2, SETTLE), (t + 8, TILT)]))


def make(style):
    comp = Comp(f"tape-strip--{style}", W, H, frames=N)
    shape = [path(bezier(torn(3 if style != "duct" else 8, 9 if style == "duct" else 7,
                               8 if style != "clear" else 5, ragged=style == "duct"), closed=True))]
    items = []
    if style == "washi":
        comp.slot("primary", "#FF8FB1")
        comp.slot("secondary", "#FFFFFF")
        # stripes live in a matte of the tape shape
        comp.layer("stripes-matte", [group(shape + [fill()], "m")], **slap())
        stripes = [group([rect((14, TH * 2), (x, 0)), fill(slot="secondary", opacity=45)], f"s{i}", rotation=30)
                   for i, x in enumerate(range(-170, 180, 34))]
        comp.layer("stripes", stripes, matte="alpha", **slap())
        items = [group(shape + [fill(slot="primary", opacity=90)], "tape")]
    elif style == "clear":
        comp.slot("primary", "#FFFFFF")
        h = TH / 2
        items = [group([P([(-TW / 2 + 16, -h + 4), (TW / 2 - 16, -h + 4)]), stroke(slot="primary", width=3,
                                                                              opacity=70)], "edge-top"),
                 group([P([(-TW / 2 + 16, h - 4), (TW / 2 - 16, h - 4)]), stroke(slot="primary", width=2,
                                                                            opacity=45)], "edge-bottom"),
                 group(shape + [fill(slot="primary", opacity=34)], "tape")]
        comp.layer("sheen-matte", [group(shape + [fill()], "m")], **slap())
        comp.layer("sheen", [group([rect((40, TH * 2)), fill("#FFFFFF", 45)], "band", rotation=24,
                                   position=anim([(6, [-TW, 0], EASE_IN_OUT), (22, [TW, 0])]))],
                   matte="alpha", **slap())
    else:
        comp.slot("primary", "#B9BEC7")
        rnd = random.Random(5)
        fibres = [group([P([(-TW / 2 + 16, y), (TW / 2 - 16, y + rnd.uniform(-1, 1))]),
                         stroke("#000000", 1.4, opacity=10)], f"f{k}")
                  for k, y in enumerate(range(-int(TH / 2) + 8, int(TH / 2) - 4, 7))]
        items = fibres + [group([P([(-TW / 2 + 18, -TH / 2 + 3), (TW / 2 - 18, -TH / 2 + 3)]),
                                 stroke("#FFFFFF", 3, opacity=40)], "hi"),
                          group(shape + [fill(slot="primary")], "tape")]
    comp.layer("tape", items, **slap())
    comp.layer("shadow", [group(shape + [fill("#000000", 8 if style == "clear" else 22)], "s", position=(3, 6))],
               **slap(),
               opacity=anim([(4, 0, EASE_OUT), (7, 100)]))
    return comp


build_asset(CATEGORY, "tape-strip", "Tape Strip",
            "A piece of tape that slaps on at an angle; stick it over a corner of a photo or use it as "
            "a label with your text on it.",
            ["tape", "washi", "sticker", "scrapbook", "label", "paper", "collage"], [
    Variant("washi", "Washi", make("washi"), "intro-hold", thumb_t=0.99, text_area=TEXT, region=(30, 20, 340, 180), pad=0.03,
            description="Pink semi-transparent washi tape with white diagonal stripes."),
    Variant("clear", "Clear", make("clear"), "intro-hold", thumb_t=0.99, text_area=TEXT, region=(30, 20, 340, 180), pad=0.03, bg="3b3b48",
            description="Frosted clear sticky tape with bright edges and a sheen that glints across."),
    Variant("duct", "Duct Tape", make("duct"), "intro-hold", thumb_t=0.99, text_area=TEXT, region=(30, 20, 340, 180), pad=0.03,
            description="Silver duct tape with fibre texture and ragged hand-torn ends."),
])
