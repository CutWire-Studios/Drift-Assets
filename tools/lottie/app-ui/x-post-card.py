import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 105


def post(media):
    W = 920
    body_h = 300
    my, mh = 0, 0
    top = 190
    H = top + body_h + (mh := 480 if media else 0) + (30 if media else 0) + 330
    comp = Comp("x-post-card", W, H, frames=F)
    comp.slot("background", "#000000")
    comp.slot("icon", "#E7E9EA")
    comp.slot("outline", "#71767B")
    comp.slot("primary", "#1D9BF0")
    comp.slot("accent", "#F91880")
    comp.slot("secondary", "#2F3336")
    areas = {"name": (150, 38, 400, 40), "handle": (150, 84, 400, 34), "text": (32, top, W - 64, body_h - 20)}
    sh = []
    ry = H - 80
    xs = [70, 230, 390, 550]
    # metrics row
    sh += [glyph("share", 36, W - 56, ry, slot="outline"), glyph("bookmark", 36, W - 136, ry, slot="outline", opacity=0) if False else
           group([polyline([(W - 160, ry - 18), (W - 160, ry + 18), (W - 144, ry + 6), (W - 128, ry + 18), (W - 128, ry - 18), (W - 160, ry - 18)], closed=True),
                  stroke(slot="outline", width=3, join="round")], "save")]
    sh += [glyph("chart", 38, 550, ry, slot="outline")]
    sh += [group([glyph("heart", 40, 390, ry, slot="accent")], "liked", anchor=(390, ry), position=(390, ry),
                 scale=Anim([(38, [0, 0], OVERSHOOT), (50, [100, 100])]), opacity=Anim([(0, 0, HOLD), (38, 100, HOLD), (F, 100)])),
           group(svg_shapes("M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3z", 40 / 24, (390 - 20, ry - 20)) +
                 [stroke(slot="outline", width=2.4, join="round")], "like", opacity=Anim([(0, 100, HOLD), (38, 0, HOLD), (F, 0)])),
           glyph("repost", 40, 230, ry, slot="outline"), glyph("comment", 36, 70, ry, slot="outline")]
    sh += [group([polyline([(32, ry - 60), (W - 32, ry - 60)]), stroke(slot="secondary", width=2)], "divider")]
    areas["time"] = (32, ry - 150, 520, 36)
    # media window
    if media:
        my = top + body_h + 8
        areas["media"] = (32, my, W - 64, mh)
        hole = rrect_path(32, my, W - 64, mh, 32, 32, 32, 32, "media")
        sh += [group(hole + [stroke(slot="secondary", width=2)], "media-edge")]
    # header
    sh += [glyph("more", 38, W - 50, 78, slot="outline"),
           group(svg_shapes("M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91c-1.31.67-2.2 1.91-2.2 3.34s.89 2.67 2.2 3.34c-.46 1.39-.21 2.9.8 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.45 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34zm-11.71 4.2L6.8 12.46l1.41-1.42 2.26 2.26 4.8-5.23 1.47 1.36-6.2 6.77z",
                              22 / 24 * 1.0, (150 + 0, 100 - 11)) and [], "x") if False else group([], "none"),
           avatar(72, 78, 96, slot="secondary", fg="outline", fg_opacity=100)]
    sh += [group([rect_tl(0, 0, W, H, 0)] + (rrect_path(32, my, W - 64, mh, 32, 32, 32, 32, "hole") if media else []) +
                 [fill(slot="background", even_odd=bool(media))], "card")]
    comp.layer("post", sh, position=Anim([(0, [0, 50], EXPO_OUT), (16, [0, 0])]), opacity=fade(0, 8))
    return comp, areas


vs = []
for vid, media, nm, desc in (("text", False, "Text Post", "Post with avatar, name and handle, a big text area, timestamp and the reply / repost / like / views / share row. The like turns pink."),
                             ("media", True, "Post With Media", "Same post with a rounded cut-out under the text for an image or video clip.")):
    c, a = post(media)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["text"], text_areas=a, thumb_t=0.95, bg="e8e8ee", description=desc))
build_asset(CAT, "x-post-card", "X Post Card",
            "Dark-mode X (Twitter) post card: avatar, name, handle, post text, optional media window and the action "
            "row, with an animated like. Type the name, handle and post text in the text areas.",
            ["twitter", "x", "tweet", "post", "social", "like", "card", "mockup", "thread"], vs)
