from _cta_actions import *

W, H = 240, 640
N = 90
X = 120
YS = (96, 290, 484)  # icon centres: like, comment, share
IS = 96
TAP = 40
# forward/share arrow (24x24 box)
SHARE = "M13.5 4.2 22 12l-8.5 7.8v-4.6C8 15.2 4.4 16.8 2 20.6 2.9 14.4 6.4 9.6 13.5 8.8Z"


def bubble():
    return [ellipse((IS, IS * 0.86), (0, -4)),
            shape([(-34, 14), (-8, 30), (-40, 44)], 4, name="tail")]


def dots():
    return [ellipse((13, 13), (dx, -4)) for dx in (-24, 0, 24)]


def counts():
    return {k: (X - 90, y + 64, 180, 40) for k, y in zip(("likes", "comments", "shares"), YS)}


def make(style):
    comp = Comp(f"like-comment-share-bar--{style}", W, H, fps=30, frames=N)
    comp.slot("accent", "#FE2C55")
    comp.slot("outline" if style == "outline" else "icon", "#FFFFFF")
    slot = "outline" if style == "outline" else "icon"
    liked = "3d-pop" if style == "3d-pop" else "classic"
    starts = (0, 7, 14)

    def enter(i):
        t = starts[i]
        return dict(scale=anim([(t, [0, 0], SPRING), (t + 16, [100, 100], LINEAR)]),
                    rotation=anim([(t, -24, SNAP_OUT), (t + 18, 0)]))

    # like
    burst(comp, (X, YS[0]), TAP + 3, 66, 92, count=8, slot="accent", width=7, rotation=22.5)
    tap(comp, (X + 10, YS[0] + 16), TAP, size=110)
    like = comp.null("like", position=(X, YS[0]), scale=anim([(0, [0, 0], SPRING), (16, [100, 100], LINEAR)] +
                                                            squash(TAP, amt=18, settle=20)))
    body(comp, "heart-red", heart(IS * 1.04), liked, slot="accent", parent=like, ip=TAP, depth=9,
         scale=anim([(TAP, [30, 30], SPRING), (TAP + 12, [100, 100])]))
    body(comp, "heart", heart(IS * 1.04), style, slot=slot, parent=like, op=TAP + 2, depth=9, line=6,
         rotation=anim([(0, -24, SNAP_OUT), (18, 0)]))
    # comment: bubble with three dots
    cm = comp.null("comment", position=(X, YS[1]), **enter(1))
    if style == "outline":
        comp.layer("dots", [group(dots() + [fill(slot="outline")], "dots")], parent=cm)
        body(comp, "bubble", bubble(), style, parent=cm, line=6)
    else:
        comp.layer("dots", [group(dots() + [fill("#1B1B22", 85)], "dots")], parent=cm)
        body(comp, "bubble", bubble(), style, slot="icon", parent=cm, depth=9)
    # share arrow
    body(comp, "share", glyph(SHARE, IS * 0.98, (4, -2)), style, slot=slot, position=(X, YS[2]), depth=9, line=6,
         **enter(2))
    return comp


build_asset(CATEGORY, "like-comment-share-bar", "Like Comment Share Bar",
            "Short-video style sidebar: like, comment and share icons pop in one by one, then the like "
            "is tapped and fills red with a burst. Type your counts under each icon.",
            ["like", "comment", "share", "sidebar", "reels", "shorts", "social"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold", thumb_t=0.75, text_area=counts()["likes"],
            text_areas=counts(), description=STYLE_DESC[s]) for s in STYLES])
