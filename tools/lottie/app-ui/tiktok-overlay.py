import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

W, H = 1080, 1920
F = 150
SHADOW = "#000000"


def rail(comp, x, y0, step, t0=10):
    """Right-hand action rail: follow avatar, like, comment, bookmark, share, spinning sound disc."""
    sh = []
    y = y0
    items = []
    # avatar with red plus
    items.append(("avatar", [group([ellipse((30, 30), (x, y + 52)), fill("#FE2C55")], "plus-bg"),
                             plus(x, y + 52, 9, slot="icon", w=4),
                             avatar(x, y, 108, slot="secondary", fg="icon", fg_opacity=70),
                             group([ellipse((116, 116), (x, y)), stroke(slot="icon", width=4)], "ring")], (x, y)))
    y += step + 36
    items.append(("heart", [glyph("heart", 84, x, y, slot="icon")], (x, y)))
    y += step
    items.append(("comment", [glyph("comment", 76, x, y, slot="icon")], (x, y)))
    y += step
    items.append(("bookmark", [glyph("bookmark", 74, x, y, slot="icon")], (x, y)))
    y += step
    items.append(("share", [glyph("share", 74, x, y, slot="icon")], (x, y)))
    out = []
    for i, (nm, shapes, piv) in enumerate(items):
        t = t0 + i * 4
        out.append((nm, shapes, piv, t))
    return out, y


def disc(x, y):
    items = [group([ellipse((26, 26), (x, y)), fill(slot="primary")], "label"),
             group([ellipse((92, 92), (x, y)), stroke("#FFFFFF", 4, 18)], "groove"),
             group([ellipse((110, 110), (x, y)), fill("#161616")], "vinyl")]
    return items


def build(kind):
    comp = Comp("tiktok-overlay", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FE2C55")
    comp.slot("secondary", "#6A6A70")
    comp.slot("outline", "#25F4EE")
    x = 976
    areas = {}
    # sound disc (spins)
    dy = 1650
    comp.layer("disc", [group(disc(x, dy), "d", anchor=(x, dy), position=(x, dy), rotation=Anim([(0, 0, LINEAR), (F, 720)]))], opacity=fade(30, 38))
    comp.layer("note", [glyph("music", 30, x - 62, dy + 66, slot="icon")], opacity=fade(34, 44))
    items, ylast = rail(comp, x, 780, 150)
    for nm, shapes, piv, t in reversed(items):
        if nm == "heart":
            comp.layer(nm, [group([glyph("heart", 84, x, piv[1], color="#FE2C55")], "red", anchor=piv, position=piv,
                                  scale=Anim([(60, [0, 0], OVERSHOOT), (72, [100, 100])]), opacity=Anim([(0, 0, HOLD), (60, 100, HOLD), (F, 100)])),
                              group([ellipse((140, 140), piv), stroke("#FE2C55", 5)], "burst", anchor=piv, position=piv,
                                    scale=Anim([(60, [40, 40], EASE_OUT), (80, [130, 130])]), opacity=Anim([(60, 80, EASE_OUT), (80, 0)]))])
            comp.layer(nm + "-w", shapes, anchor=piv, position=piv, scale=Anim([(t, [0, 0], OVERSHOOT), (t + 12, [100, 100])]),
                       opacity=Anim([(0, 0, HOLD), (t, 100, HOLD), (60, 100, HOLD), (60, 0)]))
        else:
            comp.layer(nm, shapes, anchor=piv, position=piv, scale=Anim([(t, [0, 0], OVERSHOOT), (t + 12, [100, 100])]),
                       opacity=Anim([(0, 0, HOLD), (t, 0, HOLD), (t + 2, 100)]))
        areas[nm if nm != "heart" else "likes"] = (x - 70, piv[1] + 52, 140, 34)
    # counts' text areas, shifted to sit below each icon
    areas = {"likes": (x - 70, 1014, 140, 34), "comments": (x - 70, 1164, 140, 34),
             "saves": (x - 70, 1314, 140, 34), "shares": (x - 70, 1464, 140, 34)}
    if kind == "feed":
        # bottom info
        by = 1700
        sh = [group([polyline([(0, 0), (0, 0)]), stroke(slot="icon", width=1, opacity=0)], "nil")] if False else []
        sh += [glyph("music", 34, 60, by + 58, slot="icon"), group([rect_tl(0, 0, 0, 0)], "n") if False else group([], "n")]
        comp.layer("sound", sh, position=Anim([(18, [0, 30], EXPO_OUT), (34, [0, 0])]), opacity=fade(18, 30))
        areas.update({"username": (36, by - 196, 560, 44), "caption": (36, by - 134, 780, 110), "sound": (108, by + 36, 600, 44)})
        # top tabs
        comp.layer("tabs", [label("Following", 340, 112, 36, 500, opacity=70, anchor="r"), label("For You", 410, 112, 40, 700),
                            group([rect_tl(410, 128, 112, 6, 3), fill(slot="icon")], "underline"),
                            group([polyline([(388, 90), (388, 124)]), stroke(slot="icon", width=2.5, opacity=40)], "sep"),
                            glyph("chart", 0, 0, 0, slot="icon", opacity=0) if False else magnifier(1000, 100, 22, slot="icon", w=5)],
                   position=Anim([(0, [0, -40], EXPO_OUT), (16, [0, 0])]), opacity=fade(0, 10))
        comp.layer("scrim", [group([rect_tl(0, H - 520, W, 520), gradient_fill([(0, "#000000", 0), (1, "#000000", 0.55)], (0, H - 520), (0, H))], "bottom")],
                   opacity=fade(0, 14))
        comp.layer("progress", [group([rect_tl(0, H - 6, W, 6), fill(slot="icon", opacity=35)], "track"),
                                group([grow_rect(0, H - 6, W * 0.62, 6, 0, F, 0), fill(slot="icon")], "bar")])
    return comp, areas


c, a = build("feed")
d, b = build("rail")
build_asset(CAT, "tiktok-overlay", "TikTok Video Overlay",
            "Short-video app overlay for 9:16 clips: Following / For You tabs, the right-hand rail (follow, like, comment, "
            "save, share) with a heart that pops red and a spinning sound disc, plus a progress line. Add username, caption "
            "and sound name in the text areas.",
            ["tiktok", "short video", "reels", "overlay", "social", "like", "ui", "vertical", "for you"], [
    Variant("for-you", "For You Feed", c, "intro-hold", text_area=a["caption"], text_areas=a, thumb_t=0.7, bg="6a7087"),
])
