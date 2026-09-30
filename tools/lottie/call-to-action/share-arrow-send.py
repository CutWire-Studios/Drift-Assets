from _cta_actions import *

W, H = 640, 300
N = 90
B = (112, 162)  # button centre
BS = 164
TAP = 36
LX, LW, LH = 218, 396, 100
# paper plane (Material "send" silhouette), centred, 24 box
PLANE = [(2, 21), (23, 12), (2, 3), (2, 10), (16, 12), (2, 14)]


def plane(size=94):
    k = size / 24
    return [shape([((x - 11) * k, (y - 12) * k) for x, y in PLANE], [1.4 * k, 1.2 * k, 1.4 * k, 0.6 * k, 0.4 * k, 0.6 * k],
                  name="plane")]


def make(style):
    comp = Comp(f"share-arrow-send--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#2F7BFF")
    comp.slot("icon" if style != "outline" else "outline", "#FFFFFF")
    if style != "outline":
        comp.slot("background", "#FFFFFF")
    ico = "outline" if style == "outline" else "icon"
    # flight trail
    t0, t1 = TAP + 4, TAP + 20
    trail = bezier([(0, 0), (330, -196)], [(0, 0), (-150, 30)], [(120, 40), (0, 0)], closed=False)
    comp.layer("trail", [path(trail), trim(start=anim([(t0 + 6, 0, EASE_IN_OUT), (t1 + 12, 100)]),
                                         end=anim([(t0, 0, EASE_IN), (t1, 100)])),
                         stroke(slot=ico, width=6, opacity=70)],
               position=B, ip=t0, op=t1 + 14)
    # the plane that flies away, then a fresh one pops back into the button
    fly = comp.null("fly", position=anim([(0, list(B), HOLD), (TAP, list(B), EASE_OUT), (TAP + 4, [B[0] - 14, B[1] + 8], EASE_IN),
                                          (t1, [B[0] + 330, B[1] - 196])]),
                    rotation=anim([(TAP, -18, EASE_OUT), (TAP + 4, -10, EASE_IN), (t1, -38)]),
                    scale=anim([(0, [0, 0], SPRING), (18, [100, 100], HOLD), (TAP, [100, 100], EASE_IN), (t1, [60, 60])]))
    body(comp, "plane", plane(), style if style != "outline" else "outline", slot=ico, parent=fly, depth=7,
         line=5, op=t1 + 1, shadow=False)
    body(comp, "plane2", plane(), style, slot=ico, position=B, rotation=-18, ip=TAP + 24, depth=7, line=5,
         shadow=False, scale=anim([(TAP + 24, [0, 0], SPRING), (TAP + 38, [100, 100])]))
    tap(comp, (B[0] + 10, B[1] + 18), TAP, size=130)
    btn = anim([(0, [0, 0], SPRING), (16, [100, 100], LINEAR)] + squash(TAP, amt=12, settle=18))
    body(comp, "button", [ellipse((BS, BS))], style, position=B, scale=btn, depth=14, line=6, line_slot="primary")
    tr = label(comp, style, LX, B[1], LW, LH, 10, depth=10)
    return comp, tr


def variant(s):
    comp, tr = make(s)
    return Variant(s, STYLE_NAMES[s], comp, "intro-hold", thumb_t=0.95, text_area=tr, description=STYLE_DESC[s])


build_asset(CATEGORY, "share-arrow-send", "Share Arrow Send",
            "Round share button with a paper plane that is tapped and flies off on a swooping trail, "
            "beside a label pill. Type your \"Share\" text inside the pill.",
            ["share", "send", "paper plane", "button", "tap", "social"], [variant(s) for s in STYLES])
