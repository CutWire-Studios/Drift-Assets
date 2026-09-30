from _cta_actions import *

W, H = 380, 440
N = 60
X = W / 2
YS = (236, 164, 92)  # chevrons, bottom to top
P = (X, 360)  # capsule centre
PW, PH = 320, 100


def chevron():
    return [shape([(-70, 20), (0, -44), (70, 20), (70, 50), (0, -12), (-70, 50)], [12, 14, 12, 10, 8, 10],
                  name="chevron")]


def wave(i, lo, hi):
    """Value keys for chevron i: a pulse that travels up the stack once per loop."""
    t = 6 + i * 9
    return [(0, lo, HOLD), (t, lo, EASE_OUT), (t + 8, hi, EASE_IN_OUT), (t + 24, lo, HOLD), (N, lo, LINEAR)]


def make(style):
    comp = Comp(f"swipe-up-chevrons--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#FFFFFF")
    if style == "outline":
        comp.slot("outline", "#FFFFFF")
    else:
        comp.slot("background", "#FF4F5E")
    for i, y in enumerate(YS):
        op = anim([(t, v, e) for t, v, e in wave(i, 35, 100)])
        pos = anim([(t, [X, y - (v - 35) / 65 * 16], e) for t, v, e in wave(i, 35, 100)])
        sc = anim([(t, [100 + (v - 35) / 65 * 8] * 2, e) for t, v, e in wave(i, 35, 100)])
        body(comp, f"chev{i}", chevron(), style, slot="primary", position=pos, scale=sc, opacity=op, depth=10,
             line=6, line_slot="primary")
    # capsule: nudges up in time with the wave
    nudge = anim([(0, [P[0], P[1]], HOLD), (4, [P[0], P[1]], EASE_OUT), (10, [P[0], P[1] - 10], EASE_IN_OUT),
                  (24, [P[0], P[1]], HOLD), (N, [P[0], P[1]])])
    cap = comp.null("capsule", position=nudge)
    if style != "outline":
        shine(comp, [pill(PW, PH)], (0, 0), 14, 40, PW / 2 + 80, N, parent=cap)
    body(comp, "pill", [pill(PW, PH)], style, slot="background", parent=cap, depth=10, line=6)
    return comp


TEXT = text_rect(P[0] - PW / 2, P[1], PW, PH)

build_asset(CATEGORY, "swipe-up-chevrons", "Swipe Up Chevrons",
            "Stacked chevrons that pulse upwards in a wave above a capsule; seamless loop. "
            "Type \"Swipe up\" or your call to action inside the capsule.",
            ["swipe up", "chevron", "arrow", "stories", "link", "loop", "cta"], [
    Variant(s, STYLE_NAMES[s], make(s), "loop", thumb_t=0.4, text_area=TEXT, description=STYLE_DESC[s])
    for s in STYLES])
