from _cta_actions import *

W, H = 660, 320
N = 90
C = (136, 178)
D = 176
LAND = 44
LX, LW, LH = 262, 374, 104


def coin_face(comp, style, parent, d, ip=0, op=None, name="coin", heart_k=0.52):
    """Coin: heart on top, inner ring, disc. Returns nothing; layers parent to `parent`."""
    hs = heart(d * heart_k)
    if style == "outline":
        k = max(0.45, d / 176)
        body(comp, name + "-heart", hs, style, slot="accent", parent=parent, line=4 * k, line_slot="accent", ip=ip, op=op)
        comp.layer(name + "-ring", [ellipse((d * 0.74, d * 0.74)), stroke(slot="primary", width=3 * k)], parent=parent,
                   ip=ip, op=op)
        body(comp, name + "-disc", [ellipse((d, d))], style, parent=parent, line=5 * k, line_slot="primary", ip=ip,
             op=op)
    else:
        body(comp, name + "-heart", hs, "classic", slot="accent", parent=parent, shadow=False, ip=ip, op=op)
        comp.layer(name + "-ring", [ellipse((d * 0.76, d * 0.76)), stroke("#000000", width=d * 0.035, opacity=16),
                                    fill("#FFFFFF", 14)], parent=parent, ip=ip, op=op)
        body(comp, name + "-disc", [ellipse((d, d))], style, slot="primary", parent=parent, depth=d * 0.08,
             ip=ip, op=op)


def make(style):
    comp = Comp(f"super-thanks-coin-pop--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#FFC21A")
    comp.slot("accent", "#FF4D6D")
    comp.slot("outline" if style == "outline" else "background", "#FFFFFF")
    tr = label(comp, style, LX, C[1], LW, LH, 12, depth=10)
    # mini coins pop out when the big coin lands
    for i, (dx, dy, t, s) in enumerate(((-96, -112, 0, 38), (-30, -140, 2, 44), (44, -126, 1, 36), (100, -92, 3, 32),
                                        (-118, -52, 4, 28))):
        t0 = LAND + 2 + t
        pos = anim([(t0, list(C), EASE_OUT), (t0 + 12, [C[0] + dx * 0.8, C[1] + dy], EASE_IN),
                    (t0 + 26, [C[0] + dx, C[1] + dy + 70], LINEAR)])
        mc = comp.null(f"mini{i}", position=pos, ip=t0, op=t0 + 27,
                       scale=anim([(t0, [20, 20], SPRING), (t0 + 8, [100, 100], EASE_IN), (t0 + 26, [60, 60])]),
                       rotation=anim([(t0, 0, LINEAR), (t0 + 26, 160 if dx > 0 else -160)]))
        coin_face(comp, "classic" if style == "classic" else style, mc, s, ip=t0, op=t0 + 27, name=f"mini{i}")
    burst(comp, C, LAND + 1, D * 0.62, D * 0.84, count=10, slot="primary", width=8, rotation=0)
    # big coin: pops in, hops while flipping twice, lands with a squash
    flip = comp.null("flip", position=anim([(0, list(C), HOLD), (14, list(C), EASE_OUT), (28, [C[0], C[1] - 58], EASE_IN),
                                            (LAND, list(C))]),
                     scale=anim([(0, [0, 0], SPRING), (12, [100, 100], EASE_IN_OUT), (21, [0, 100], EASE_IN_OUT),
                                 (28, [-100, 100], EASE_IN_OUT), (35, [0, 100], EASE_IN_OUT), (LAND - 2, [100, 100], EASE_IN),
                                 (LAND, [110, 88], SNAP_OUT), (LAND + 6, [96, 106], EASE_IN_OUT), (LAND + 14, [100, 100])]))
    coin_face(comp, style, flip, D)
    return comp, tr


def variant(s):
    comp, tr = make(s)
    return Variant(s, STYLE_NAMES[s], comp, "intro-hold", thumb_t=0.68, text_area=tr, description=STYLE_DESC[s])


build_asset(CATEGORY, "super-thanks-coin-pop", "Super Thanks Coin Pop",
            "Gold coin with a heart flips, lands and pops a shower of little coins, beside a text pill. "
            "Type \"Thanks!\" or a tip amount inside the pill.",
            ["thanks", "tip", "donate", "coin", "support", "heart", "super thanks"], [variant(s) for s in STYLES])
