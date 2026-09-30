from _cta_actions import *

W, H = 780, 270
N = 84
Y = 112
GAP = 142
XS = [W / 2 + (i - 2) * GAP for i in range(5)]
R = 62
FILL0, STEP = 22, 7


def star_geom(k=1.0):
    return [shape(star_pts(R * k, R * 0.5 * k), 9 * k, name="star")]


def make(style):
    comp = Comp(f"rate-five-stars--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#FFC531")
    if style == "outline":
        comp.slot("outline", "#FFFFFF")
    else:
        comp.slot("secondary", "#4A4A58")
    last = FILL0 + 4 * STEP
    burst(comp, (XS[4], Y), last + 3, R * 1.2, R * 1.65, count=8, slot="primary", width=7, rotation=22.5)
    for i, x in enumerate(XS):
        t_in, t_fill = i * 3, FILL0 + i * STEP
        n = comp.null(f"star{i}", position=(x, Y),
                      scale=anim([(t_in, [0, 0], SPRING), (t_in + 14, [100, 100], HOLD), (t_fill - 2, [100, 100], EASE_OUT),
                                  (t_fill + 3, [124, 124], EASE_IN_OUT), (t_fill + 10, [94, 94], EASE_IN_OUT),
                                  (t_fill + 16, [100, 100])]),
                      rotation=anim([(t_in, -40, SNAP_OUT), (t_in + 16, 0, HOLD), (t_fill, 0, EASE_OUT),
                                     (t_fill + 8, 12, EASE_IN_OUT), (t_fill + 18, 0)]))
        sc = anim([(t_fill, [20, 20], SPRING), (t_fill + 12, [100, 100])])
        if style == "outline":
            body(comp, f"gold{i}", star_geom(0.8), "classic", slot="primary", parent=n, ip=t_fill, scale=sc,
                 shadow=False)
            body(comp, f"empty{i}", star_geom(), style, parent=n, line=5)
        else:
            body(comp, f"gold{i}", star_geom(), style, slot="primary", parent=n, ip=t_fill, scale=sc, depth=9)
            body(comp, f"empty{i}", star_geom(), style, slot="secondary", parent=n, op=t_fill + 4, depth=9)
    return comp


TEXT = (XS[0] - R, Y + R + 26, XS[4] - XS[0] + 2 * R, 56)

build_asset(CATEGORY, "rate-five-stars", "Rate Five Stars",
            "Five stars pop in empty, then fill with gold one by one; the last one bursts. Type a rating "
            "prompt or review line underneath.",
            ["rating", "stars", "review", "rate", "five stars", "feedback"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold", thumb_t=0.95, text_area=TEXT, description=STYLE_DESC[s])
    for s in STYLES])
