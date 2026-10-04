import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 105
RING = [(0, "#FEDA75"), (0.35, "#FA7E1E"), (0.65, "#D62976"), (1, "#962FBF")]


def tap_heart(cx, cy, size, t0):
    """Big white heart over the photo: pops at t0 and fades away."""
    return group([glyph("heart", size, cx, cy, color="#FFFFFF")], "double-tap", anchor=(cx, cy), position=(cx, cy),
                 scale=Anim([(t0, [0, 0], OVERSHOOT), (t0 + 10, [100, 100], EASE_IN_OUT), (t0 + 24, [100, 100], EASE_IN), (t0 + 32, [140, 140])]),
                 opacity=Anim([(0, 0, HOLD), (t0, 100, HOLD), (t0 + 24, 100, EASE_IN), (t0 + 32, 0)]))


def post(kind):
    W = 900
    if kind == "feed":
        H = 1470
        hy = 70
        my, mh = 150, 900
        comp = Comp("instagram-post-card", W, H, frames=F)
    else:
        H = 1200
        hy = 70
        my, mh = 150, 640
        comp = Comp("instagram-post-card", W, H, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("icon", "#262626")
    comp.slot("primary", "#ED4956")
    comp.slot("outline", "#8E8E8E")
    comp.slot("secondary", "#DBDBDB")
    ay = my + mh + 56
    areas = {"username": (140, hy - 26, 440, 38), "media": (0, my, W, mh)}
    sh = []
    # actions row
    sh += [glyph("bookmark", 46, W - 50, ay, slot="icon", opacity=0) if False else
           group([polyline([(W - 72, ay - 26), (W - 72, ay + 26), (W - 48, ay + 8), (W - 24, ay + 26), (W - 24, ay - 26), (W - 72, ay - 26)], closed=True),
                  stroke(slot="icon", width=4, join="round")], "save")]
    sh += [group([polyline([(272, ay + 6), (322, ay - 22)]), polyline([(322, ay - 22), (290, ay + 26), (278, ay + 4), (254, ay - 12), (322, ay - 22)]),
                  stroke(slot="icon", width=4, join="round")], "send"),
           group([ellipse((46, 46), (166, ay)), stroke(slot="icon", width=4)], "comment")]
    sh += [group(svg_shapes(HEART_OUT, 46 / 24 * 1.0, (60 - 23, ay - 23), "heart-out") + [stroke(slot="icon", width=4 / (46 / 24) * 1.0 * (46 / 24), join="round")], "like",
                 opacity=Anim([(0, 100, HOLD), (24, 0, HOLD), (F, 0)])),
           group([glyph("heart", 52, 60, ay, slot="primary")], "liked", anchor=(60, ay), position=(60, ay),
                 scale=Anim([(24, [0, 0], OVERSHOOT), (36, [100, 100])]), opacity=Anim([(0, 0, HOLD), (24, 100, HOLD), (F, 100)]))]
    # header
    sh += [glyph("more", 40, W - 50, hy, slot="icon"), avatar(70, hy, 76, slot="secondary", fg="outline", fg_opacity=100, ring=None)]
    sh += [group([ellipse((92, 92), (70, hy)), stroke("#D62976", 5)], "ring")]
    # media cut-out + card
    hole = rrect_path(0, my, W, mh, 0, 0, 0, 0, "media")
    sh += [tap_heart(W / 2, my + mh / 2, 210, 30)]
    sh += [group([rect_tl(0, 0, W, H, 0)] + hole + [fill(slot="background", even_odd=True)], "card")]
    comp.layer("post", sh, position=Anim([(0, [0, 50], EXPO_OUT), (16, [0, 0])]), opacity=fade(0, 8))
    areas.update({"likes": (24, ay + 58, 500, 36), "caption": (24, ay + 106, W - 48, 130)} if kind == "feed" else
                 {"likes": (24, ay + 58, 500, 36), "caption": (24, ay + 106, W - 48, 100)})
    return comp, areas


HEART_OUT = ("M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3z"
             "M12.1 18.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z")

vs = []
for vid, nm, desc in (("feed", "Feed Post", "Square photo post: avatar with a story ring, username, the photo as a cut-out, action icons, likes and caption. A double-tap heart pops over the photo and the like fills red."),
                      ("short", "Short Post", "Shorter card with a less tall photo window for 16:9-ish footage.")):
    c, a = post(vid)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["caption"], text_areas=a, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "instagram-post-card", "Instagram Post Card",
            "Instagram-style feed post with a real cut-out for your photo or video, a story-ring avatar, action icons "
            "and a double-tap heart that likes the post. Type the username, likes and caption in the text areas.",
            ["instagram", "post", "feed", "social", "like", "photo", "card", "mockup", "ig"], vs)
