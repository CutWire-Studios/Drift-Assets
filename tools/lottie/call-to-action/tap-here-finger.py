from _cta_actions import *

W, H = 560, 372
N = 60
T = (104, 108)  # tap target
TAPS = (16, 40)
LX, LW, LH = 214, 326, 96


def make(style):
    comp = Comp(f"tap-here-finger--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#FF3D71")
    if style != "outline":
        comp.slot("background", "#FFFFFF")
    hand_slots(comp, style)
    # hand: hover above the target, press down on each tap
    up = [T[0] + 16, T[1] + 30]
    down = [T[0] + 4, T[1] + 6]
    pos, sc = [(0, up, EASE_IN_OUT)], [(0, [100, 100], EASE_IN_OUT)]
    for t in TAPS:
        pos += [(t - 6, up, EASE_IN), (t, down, EASE_OUT), (t + 3, down, EASE_IN_OUT), (t + 12, up, EASE_IN_OUT)]
        sc += [(t - 6, [100, 100], EASE_IN), (t, [93, 93], EASE_OUT), (t + 3, [93, 93], EASE_IN_OUT),
               (t + 12, [100, 100], EASE_IN_OUT)]
    pos.append((N, up))
    sc.append((N, [100, 100]))
    hand(comp, style, position=anim(pos), scale=anim(sc), rotation=-14)
    for t in TAPS:
        tap(comp, T, t, size=120)
        ripple(comp, T, t + 5, size=170)
    # target: a pulsing dot with a ring
    ring = anim([(0, [100, 100], EASE_IN_OUT)] + sum(([(t, [100, 100], SNAP_OUT), (t + 5, [78, 78], EASE_IN_OUT),
                                                      (t + 14, [100, 100], EASE_IN_OUT)] for t in TAPS), []) +
                [(N, [100, 100])])
    if style == "outline":
        body(comp, "target", [ellipse((46, 46))], style, position=T, scale=ring, line=6, line_slot="primary")
        body(comp, "target-ring", [ellipse((96, 96))], style, position=T, scale=ring, line=3, line_slot="primary")
        body(comp, "label", [pill(LW, LH)], style, position=(LX + LW / 2, T[1]), line=5)
    else:
        body(comp, "target", [ellipse((52, 52))], style, position=T, scale=ring, depth=8)
        comp.layer("target-ring", [ellipse((100, 100)), stroke(slot="primary", width=6, opacity=60)],
                   position=T, scale=ring)
        body(comp, "label", [pill(LW, LH)], style, slot="background", position=(LX + LW / 2, T[1]), depth=9)
    return comp


build_asset(CATEGORY, "tap-here-finger", "Tap Here Finger",
            "Cartoon finger tapping a target with ripples, next to a label pill; seamless loop. "
            "Type your \"Tap here\" text inside the pill.",
            ["tap", "finger", "hand", "click", "touch", "cta", "loop"], [
    Variant(s, STYLE_NAMES[s], make(s), "loop", thumb_t=0.45, text_area=text_rect(LX, T[1], LW, LH),
            description=STYLE_DESC[s]) for s in STYLES])
