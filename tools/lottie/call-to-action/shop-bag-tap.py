from _cta_actions import *

W, H = 660, 264
N = 105
B = (124, 146)  # bag centre
CLICK = 40
LX, LW, LH = 250, 386, 108
BADGE = (B[0] + 76, B[1] - 50)
BD = 60


def bag():
    return [shape([(-64, -34), (64, -34), (74, 78), (-74, 78)], [12, 12, 20, 20], name="bag")]


def handle(slot, width):
    return [group([path(arc_pts(34, 180, 360, (0, -34))), stroke(slot=slot, width=width)], "handle")]


def make(style):
    comp = Comp(f"shop-bag-tap--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#00B894")
    comp.slot("accent", "#FF3B5C")
    comp.slot("outline" if style == "outline" else "background", "#FFFFFF")
    tip = [B[0] + 20, B[1] + 34]
    cursor(comp, [(16, [W * 0.5, H + 80], DECEL), (34, tip, EASE_IN_OUT), (CLICK + 16, tip, EASE_IN),
                  (CLICK + 34, [W * 0.5, H + 80])], [CLICK], ip=16, op=CLICK + 36, scale=3.8)
    # cart badge: pops in on the corner after the click
    bz = comp.null("badge", position=BADGE, scale=anim([(CLICK + 4, [0, 0], SPRING), (CLICK + 18, [100, 100])]))
    burst(comp, BADGE, CLICK + 6, BD * 0.62, BD * 0.95, count=8, slot="accent", width=5, dots=False)
    if style == "outline":
        body(comp, "badge-dot", [ellipse((BD, BD))], "classic", slot="accent", parent=bz, shadow=False, ip=CLICK + 4)
    else:
        body(comp, "badge-dot", [ellipse((BD, BD))], style, slot="accent", parent=bz, depth=5, shadow=False,
             ip=CLICK + 4, position=(0, -2))
        comp.layer("badge-rim", [ellipse((BD + 12, BD + 12)), fill(slot="background")], parent=bz, ip=CLICK + 4)
    tr = label(comp, style, LX, B[1], LW, LH, 10, depth=10)
    sq = [(0, [0, 0], SPRING), (16, [120, 120], LINEAR)] + squash(CLICK, s=120, amt=14, settle=20)
    bg = comp.null("bag", position=(B[0], B[1] + 94), scale=anim(sq),
                   rotation=anim([(0, -16, SNAP_OUT), (18, 0, HOLD), (CLICK, 0, EASE_OUT), (CLICK + 6, -6, EASE_IN_OUT),
                                  (CLICK + 14, 4, EASE_IN_OUT), (CLICK + 22, 0)]))
    ico = "primary"
    if style != "outline":
        comp.layer("bag-fold", [group([path(arc_pts(20, 20, 160, (0, -28))), stroke("#FFFFFF", width=8, opacity=80)],
                                      "smile")], parent=bg, position=(0, -78))
    body(comp, "bag-body", bag(), style, slot="primary", parent=bg, position=(0, -78), depth=12, line=6,
         line_slot="primary")
    comp.layer("bag-handle", handle(ico, 12 if style == "outline" else 14), parent=bg, position=(0, -78))
    return comp, tr


def variant(s):
    comp, tr = make(s)
    badge = (BADGE[0] - BD * 0.3, BADGE[1] - BD * 0.3, BD * 0.6, BD * 0.6)
    return Variant(s, STYLE_NAMES[s], comp, "intro-hold", thumb_t=0.9, text_area=tr,
                   text_areas={"label": tr, "count": badge}, description=STYLE_DESC[s])


build_asset(CATEGORY, "shop-bag-tap", "Shop Bag Tap",
            "Shopping bag icon that a pointer taps; a cart badge pops onto its corner. Type \"Shop now\" in "
            "the pill and a count in the badge (the \"count\" text area).",
            ["shop", "shopping", "bag", "cart", "store", "buy", "click"], [variant(s) for s in STYLES])
