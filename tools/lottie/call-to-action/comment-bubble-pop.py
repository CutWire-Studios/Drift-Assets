from _cta_actions import *

W, H = 640, 244
N = 90
AV = (62, 166)  # avatar placeholder
BL, BB = 118, 206  # bubble left edge / bottom
W0, H0 = 156, 100
W1, H1 = 490, 160
GROW = 48


def bubble_geom():
    ks = [(4, 0, HOLD), (GROW, 0, OVERSHOOT), (GROW + 16, 1, LINEAR)]
    size = anim([(t, [W0 + (W1 - W0) * v, H0 + (H1 - H0) * v], e) for t, v, e in ks])
    pos = anim([(t, [BL + (W0 + (W1 - W0) * v) / 2, BB - (H0 + (H1 - H0) * v) / 2], e) for t, v, e in ks])
    return [rect(size, position=pos, roundness=46),
            shape([(BL + 6, BB - 44), (BL + 44, BB - 2), (BL - 16, BB + 8)], [6, 4, 6], name="tail")]


def make(style):
    comp = Comp(f"comment-bubble-pop--{style}", W, H, fps=30, frames=N)
    if style == "outline":
        comp.slot("outline", "#FFFFFF")
        comp.slot("accent", "#FFFFFF")
    else:
        comp.slot("background", "#FFFFFF")
        comp.slot("accent", "#3A3A46")
    comp.slot("secondary", "#8E7CFF")
    # typing dots: bounce in turn, then fade as the bubble opens up
    dc = (BL + W0 / 2, BB - H0 / 2)
    for i, dx in enumerate((-30, 0, 30)):
        keys = [(0, [0, 0], LINEAR)]
        for c in (12, 28):
            t = c + i * 4
            keys += [(t, [0, 0], EASE_OUT), (t + 5, [0, -14], EASE_IN), (t + 10, [0, 0], LINEAR)]
        comp.layer(f"dot{i}", [group([ellipse((18, 18)), fill(slot="accent")], "d", position=anim(keys + [(N, [0, 0])]))],
                   position=(dc[0] + dx, dc[1]), ip=8, op=GROW + 8,
                   scale=anim([(8 + i * 2, [0, 0], SPRING), (18 + i * 2, [100, 100], HOLD),
                               (GROW - 2, [100, 100], EASE_IN), (GROW + 6, [0, 0])]))
    sc = anim([(4, [0, 0], SPRING), (20, [100, 100], LINEAR)])
    bub = comp.null("bubble-pop", position=(BL, BB), scale=sc)
    body(comp, "bubble", bubble_geom(), style, slot="background", parent=bub, position=(-BL, -BB), depth=12, line=6)
    person = fill(slot="secondary") if style == "outline" else fill("#FFFFFF", 85)
    comp.layer("avatar-head", [group([ellipse((30, 30), (0, -10)), rect((48, 26), (0, 22), roundness=13),
                                      person], "person")],
               position=AV, scale=anim([(4, [0, 0], SPRING), (16, [100, 100])]))
    body(comp, "avatar", [ellipse((84, 84))], style, slot="secondary", position=AV, depth=10, line=6,
         line_slot="secondary", scale=anim([(0, [0, 0], SPRING), (14, [100, 100])]))
    return comp


TEXT = (BL + 40, BB - H1 / 2 - 50, W1 - 80, 100)

build_asset(CATEGORY, "comment-bubble-pop", "Comment Bubble Pop",
            "Chat bubble pops in beside an avatar placeholder, shows bouncing typing dots, then opens up "
            "into a wide comment box. Type your comment inside the bubble.",
            ["comment", "chat", "bubble", "typing", "reply", "social"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold", thumb_t=0.9, text_area=TEXT, description=STYLE_DESC[s])
    for s in STYLES])
