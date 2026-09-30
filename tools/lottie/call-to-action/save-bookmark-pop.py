from _cta_actions import *

W = H = 400
N = 54
C = (W / 2, H / 2 - 6)
TAP = 22


def mark(k=1.0):
    return [shape([(-62 * k, -88 * k), (62 * k, -88 * k), (62 * k, 92 * k), (0, 48 * k), (-62 * k, 92 * k)],
                  [24 * k, 24 * k, 10 * k, 6 * k, 10 * k], name="bookmark")]


def make(style):
    comp = Comp(f"save-bookmark-pop--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#FFC53D")
    comp.slot("outline" if style == "outline" else "icon", "#FFFFFF")
    tip = (C[0] + 14, C[1] + 20)
    burst(comp, C, TAP + 3, 128, 168, count=10, slot="primary", width=9, rotation=18)
    tap(comp, tip, TAP, size=120)
    bm = comp.null("bookmark", position=C, scale=anim(
        [(0, [0, 0], SPRING), (15, [100, 100], LINEAR)] + squash(TAP, amt=16, settle=22)),
        rotation=anim([(0, -20, SNAP_OUT), (16, 0, HOLD), (TAP, 0, EASE_OUT), (TAP + 6, 7, EASE_IN_OUT),
                       (TAP + 13, -4, EASE_IN_OUT), (TAP + 20, 0)]))
    local = (tip[0] - C[0], tip[1] - C[1])
    if style == "classic":
        click_wipe(comp, mark(), local, TAP, "primary", parent=bm, dur=10, reach=460)
        body(comp, "base", mark(), style, slot="icon", parent=bm, depth=12)
    elif style == "outline":
        # line art: the fill rises from the bottom inside the outline
        body(comp, "line", mark(), style, parent=bm, line=9)
        comp.layer("fill-matte", [group(mark(0.9) + [fill()], "matte")], parent=bm, ip=TAP)
        comp.layer("fill", [rect((200, 240)), fill(slot="primary")], parent=bm, ip=TAP, matte="alpha",
                   position=anim([(TAP, [0, 210], DECEL), (TAP + 14, [0, 0])]))
    else:
        body(comp, "filled", mark(), style, slot="primary", parent=bm, ip=TAP, depth=16,
             scale=anim([(TAP, [60, 60], SPRING), (TAP + 12, [100, 100])]))
        body(comp, "base", mark(), style, slot="icon", parent=bm, op=TAP + 1, depth=16)
    return comp


build_asset(CATEGORY, "save-bookmark-pop", "Save Bookmark Pop",
            "Bookmark icon that springs in and fills with colour when tapped, with a sparkle burst. "
            "A \"save this post\" sticker; no text area.",
            ["save", "bookmark", "saved", "tap", "reaction", "social"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold", thumb_t=0.6, description=STYLE_DESC[s]) for s in STYLES])
