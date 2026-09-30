from _cta_actions import *

W = H = 480
N = 60
C = (W / 2, H / 2 + 10)
POP = 8
OUT = 42
HS = 250


def make(style):
    comp = Comp(f"double-tap-heart--{style}", W, H, fps=30, frames=N)
    comp.marker("intro", 0, 26)
    comp.marker("outro", OUT, N - OUT)
    comp.slot("primary", "#FFFFFF" if style == "classic" else "#FF2D55")
    comp.slot("accent", "#FF2D55")
    if style == "outline":
        comp.slot("outline", "#FFFFFF")
    burst(comp, C, POP + 2, HS * 0.52, HS * 0.7, count=10, slot="accent", width=9, rotation=18)
    # little hearts drifting up and out
    for i, (dx, dy, s, t) in enumerate(((-150, -120, 52, 0), (150, -96, 44, 2), (-104, -190, 34, 4), (118, -176, 30, 5))):
        t0 = POP + 4 + t
        comp.layer(f"mini{i}", [group(heart(s) + [fill(slot="accent")], "h")], ip=t0, op=t0 + 26,
                   position=anim([(t0, list(C), SNAP_OUT), (t0 + 24, [C[0] + dx, C[1] + dy])]),
                   scale=anim([(t0, [0, 0], SPRING), (t0 + 8, [100, 100], EASE_IN), (t0 + 25, [0, 0])]),
                   rotation=anim([(t0, 0, EASE_OUT), (t0 + 24, -25 if dx < 0 else 25)]))
    sc = anim([(POP, [0, 0], SPRING), (POP + 8, [118, 118], EASE_IN_OUT), (POP + 14, [94, 94], EASE_IN_OUT),
               (POP + 20, [100, 100], HOLD), (OUT, [100, 100], EASE_OUT), (OUT + 5, [112, 112], EASE_IN),
               (N - 2, [0, 0], LINEAR), (N, [0, 0])])
    pos = anim([(0, list(C), HOLD), (OUT, list(C), EASE_IN), (N - 2, [C[0], C[1] - 70])])
    rot = anim([(POP, -18, SNAP_OUT), (POP + 16, 0, HOLD), (OUT, 0, EASE_IN), (N - 2, 8)])
    hn = comp.null("heart", position=pos, scale=sc, rotation=rot)
    if style == "outline":
        body(comp, "heart-core", heart(HS * 0.6), "classic", slot="primary", parent=hn, shadow=False,
             scale=anim([(POP + 4, [0, 0], SPRING), (POP + 16, [100, 100])]))
        body(comp, "heart", heart(HS), style, parent=hn, line=10)
    else:
        body(comp, "heart", heart(HS), style, slot="primary", parent=hn, depth=18)
    # two quick taps
    for t in (0, 6):
        tap(comp, (C[0], C[1] + 10), t + 1, size=130)
    return comp


build_asset(CATEGORY, "double-tap-heart", "Double Tap Heart",
            "A big heart bursts in where a photo is double-tapped, throws off little hearts, then floats away. "
            "Place it over your clip; no text area.",
            ["heart", "like", "double tap", "love", "reaction", "instagram style"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold-outro", thumb_t=0.4, description=STYLE_DESC[s])
    for s in STYLES])
