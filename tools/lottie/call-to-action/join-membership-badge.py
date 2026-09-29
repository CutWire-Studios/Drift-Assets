from _cta_actions import *

W, H = 660, 280
N = 90
B = (124, 124)  # badge centre
LX, LW, LH = 238, 398, 104


def seal(r=84):
    return [shape(star_pts(r, r * 0.9, n=16), 5, name="seal")]


def tails(cut=False):
    """Ribbon tails; cut=True starts them at the seal's rim (for line art, where nothing hides them)."""
    top = [(-66, 60), (-14, 80)] if cut else [(-58, 20), (-6, 40)]
    out = []
    for sx, nm in ((1, "tailL"), (-1, "tailR")):
        pts = top + [(-30, 140), (-46, 112), (-80, 124)]
        out.append(shape([(x * sx, y) for x, y in pts], [4, 4, 3, 3, 3], name=nm))
    return out


def sparkle(comp, pos, t, size=26, slot="accent"):
    comp.layer("sparkle", [group([shape(star_pts(size / 2, size / 7, n=4), 1.5), fill(slot=slot)], "s")],
               position=pos, ip=t, op=t + 22,
               scale=anim([(t, [0, 0], SPRING), (t + 8, [100, 100], EASE_IN), (t + 20, [0, 0])]),
               rotation=anim([(t, -40, EASE_OUT), (t + 20, 40)]))


def make(style):
    comp = Comp(f"join-membership-badge--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#7B4DFF")
    comp.slot("accent", "#FFD34D")
    comp.slot("secondary", "#4B2CB8")
    comp.slot("outline" if style == "outline" else "background", "#FFFFFF")
    for i, (dx, dy, t) in enumerate(((-86, -78, 44), (92, -54, 52), (-96, 58, 60), (78, 84, 50))):
        sparkle(comp, (B[0] + dx, B[1] + dy), t, 28 if i % 2 == 0 else 20)
    spin = comp.null("badge", position=B,
                     scale=anim([(0, [0, 0], SPRING), (18, [100, 100], LINEAR), (40, [100, 100], EASE_IN_OUT),
                                 (46, [108, 108], EASE_IN_OUT), (54, [100, 100])]),
                     rotation=anim([(0, -200, SNAP_OUT), (22, 0)]))
    body(comp, "star", [shape(star_pts(46, 21), 5)], style, slot="accent", parent=spin, depth=6, line=5,
         line_slot="accent", shadow=False, position=(0, 2),
         scale=anim([(8, [0, 0], SPRING), (22, [100, 100])]))
    if style == "outline":
        body(comp, "ring", [ellipse((128, 128))], style, parent=spin, line=3, line_slot="primary")
    else:
        comp.layer("ring", [ellipse((132, 132)), stroke("#FFFFFF", width=4, opacity=35)], parent=spin)
        shine(comp, seal(), (0, 0), 30, 48, 150, N, parent=spin, width=46, opacity=38)
    body(comp, "seal", seal(), style, slot="primary", parent=spin, depth=12, line=5, line_slot="primary")
    body(comp, "tails", tails(style == "outline"), style, slot="secondary", position=B, depth=8, line=5, line_slot="secondary",
         scale=anim([(10, [0, 0], OVERSHOOT), (24, [100, 100])]))
    tr = label(comp, style, LX, B[1], LW, LH, 14, depth=10)
    return comp, tr


def variant(s):
    comp, tr = make(s)
    return Variant(s, STYLE_NAMES[s], comp, "intro-hold", thumb_t=0.95, text_area=tr, description=STYLE_DESC[s])


build_asset(CATEGORY, "join-membership-badge", "Join Membership Badge",
            "Rosette badge with a star spins in, a shine sweeps across it and sparkles twinkle, beside a "
            "text pill. Type \"Join\" or your membership tier inside the pill.",
            ["join", "membership", "member", "badge", "star", "subscribe", "vip"], [variant(s) for s in STYLES])
