import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

W, H = 1080, 1920
F = 150


def build():
    comp = Comp("youtube-shorts-overlay", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF0000")
    comp.slot("secondary", "#6A6A70")
    x = 980
    comp.layer("progress", [group([grow_rect(0, H - 8, W, 8, 0, F, 0), fill(slot="primary")], "bar"),
                            group([rect_tl(0, H - 8, W, 8), fill(slot="icon", opacity=35)], "track")])
    items = [("like", "thumb", 82, 800, False), ("dislike", "thumb", 82, 960, True), ("comment", "comment", 72, 1120, False),
             ("share", "share", 72, 1280, False), ("remix", "repost", 72, 1440, False)]
    for i, (nm, g, sz, y, flip) in enumerate(items):
        t = 10 + i * 4
        comp.layer(nm, [glyph(g, sz, x, y, slot="icon", rotation=180 if flip else 0)], anchor=(x, y), position=(x, y),
                   scale=Anim([(t, [0, 0], OVERSHOOT), (t + 12, [100, 100])]), opacity=Anim([(0, 0, HOLD), (t, 100)]))
    comp.layer("sound-disc", [group([rect_tl(x - 36, 1560, 72, 72, 14), fill(slot="secondary")], "d"),
                              glyph("music", 36, x, 1596, slot="icon")], anchor=(x, 1596), position=(x, 1596),
               scale=Anim([(32, [0, 0], OVERSHOOT), (44, [100, 100])]))
    by = 1730
    comp.layer("channel", [
        group([rect_tl(272, by - 34, 190, 68, 34), fill(slot="icon")], "sub-pill"),
        label("Subscribe", 367, by + 11, 32, 700, color="#0F0F0F", anchor="c"),
        avatar(100, by, 76, slot="secondary", fg="icon", fg_opacity=70)],
        position=Anim([(18, [0, 40], EXPO_OUT), (34, [0, 0])]), opacity=fade(18, 30))
    comp.layer("scrim", [group([rect_tl(0, H - 560, W, 560), gradient_fill([(0, "#000000", 0), (1, "#000000", 0.55)], (0, H - 560), (0, H))], "g")],
               opacity=fade(0, 14))
    return comp, {"channel": (156, 1696, 100, 36), "caption": (36, 1782, 780, 110), "likes": (x - 70, 856, 140, 34),
                  "comments": (x - 70, 1176, 140, 34)}


c, a = build()
build_asset(CAT, "youtube-shorts-overlay", "YouTube Shorts Overlay",
            "Vertical-video player overlay in the style of YouTube Shorts: right rail (like, dislike, comment, share, "
            "remix), channel avatar with a white Subscribe pill, caption area and a red progress line.",
            ["youtube shorts", "shorts", "overlay", "subscribe", "vertical", "social", "ui", "like"], [
    Variant("shorts", "Shorts Feed", c, "intro-hold", text_area=a["caption"], text_areas=a, thumb_t=0.7, bg="3a5a8a"),
])
