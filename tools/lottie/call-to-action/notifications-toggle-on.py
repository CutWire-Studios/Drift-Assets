from _cta_actions import *

W, H = 724, 236
N = 105
CY = 112
CW, CH = 644, 156
CX = W / 2
BELL = (CX - CW / 2 + 88, CY + 4)
TG = (CX + CW / 2 - 96, CY)
TW, TH, KD = 132, 78, 64
TAP = 42


def make(style):
    comp = Comp(f"notifications-toggle-on--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#FFB800")
    comp.slot("accent", "#34C759")
    if style != "outline":
        comp.slot("secondary", "#8E8E93")
    comp.slot("outline" if style == "outline" else "background", "#FFFFFF")
    card = comp.null("card", position=(CX, CY), scale=anim([(0, [0, 0], OVERSHOOT), (16, [100, 100])]))
    rel = lambda p: (p[0] - CX, p[1] - CY)
    # sound waves once the bell rings
    for side, (a0, a1) in (("r", (-40, 10)), ("l", (170, 220))):
        items = []
        for i, r in enumerate((58, 76)):
            d = i * 3
            t = TAP + 8 + d
            items.append(group([path(arc_pts(r, a0, a1)), trim(start=anim([(t, 50, SNAP_OUT), (t + 10, 0)]),
                                                                end=anim([(t, 50, SNAP_OUT), (t + 10, 100)])),
                                stroke(slot="primary", width=7, opacity=anim([(t + 16, 100, EASE_IN), (t + 28, 0)]))],
                               f"{side}{i}"))
        comp.layer("waves-" + side, items, parent=card, position=rel(BELL), ip=TAP + 8, op=TAP + 42)
    # bell swings from its top
    swing = anim([(0, 0, HOLD), (TAP + 6, 0, EASE_OUT), (TAP + 10, 22, EASE_IN_OUT), (TAP + 16, -18, EASE_IN_OUT),
                  (TAP + 22, 13, EASE_IN_OUT), (TAP + 28, -8, EASE_IN_OUT), (TAP + 34, 4, EASE_IN_OUT), (TAP + 40, 0)])
    bell = comp.null("bell", parent=card, position=(rel(BELL)[0], rel(BELL)[1] - 44), rotation=swing,
                     scale=anim([(4, [0, 0], SPRING), (18, [100, 100])]))
    s = 0.52
    if style == "outline":
        comp.layer("bell-dot", [ellipse((20, 20), (0, 0)), fill(slot="accent")], parent=bell, ip=TAP + 6,
                   position=(36, 12), scale=anim([(TAP + 6, [0, 0], SPRING), (TAP + 18, [100, 100])]))
        body(comp, "clapper", bell_clapper(s), style, parent=bell, line=4, line_slot="primary")
        body(comp, "bell-body", bell_body(s), style, parent=bell, line=4, line_slot="primary")
    else:
        comp.layer("bell-dot", [ellipse((22, 22), (0, 0)), fill(slot="accent"), stroke(slot="background", width=4)],
                   parent=bell, ip=TAP + 6, position=(36, 12),
                   scale=anim([(TAP + 6, [0, 0], SPRING), (TAP + 18, [100, 100])]))
        body(comp, "bell-body", bell_body(s), style, parent=bell, depth=6, shadow=False)
        body(comp, "clapper", bell_clapper(s), style, parent=bell, depth=4, shadow=False)
    # toggle
    tap(comp, (TG[0] - 10, TG[1] + 14), TAP, size=100)
    tg = comp.null("toggle", parent=card, position=rel(TG),
                   scale=anim([(8, [0, 0], SPRING), (22, [100, 100], LINEAR)] + squash(TAP, amt=8, settle=16)))
    kx = (TW - KD) / 2 - 7
    knob = anim([(0, [-kx, 0], HOLD), (TAP, [-kx, 0], OVERSHOOT), (TAP + 10, [kx, 0])])
    stretch = anim([(0, [100, 100], HOLD), (TAP, [100, 100], EASE_OUT), (TAP + 4, [124, 92], EASE_IN_OUT),
                    (TAP + 12, [100, 100])])
    if style == "outline":
        body(comp, "knob", [ellipse((KD - 8, KD - 8))], "classic", slot="outline", parent=tg, position=knob,
             scale=stretch, shadow=False)
        comp.layer("track-on", [group([rect((TW, TH), roundness=TH / 2), fill(slot="accent")], "on")], parent=tg,
                   opacity=anim([(TAP + 2, 0, EASE_OUT), (TAP + 10, 100)]), ip=TAP)
        body(comp, "track", [rect((TW, TH), roundness=TH / 2)], style, parent=tg, line=4)
        body(comp, "card-body", [rect((CW, CH), roundness=40)], style, parent=card, line=5)
    else:
        body(comp, "knob", [ellipse((KD, KD))], style, slot="background", parent=tg, position=knob, scale=stretch,
             depth=5)
        click_wipe(comp, [rect((TW, TH), roundness=TH / 2)], (-kx, 0), TAP + 1, "accent", parent=tg, dur=10, reach=300)
        body(comp, "track", [rect((TW, TH), roundness=TH / 2)], style, slot="secondary", parent=tg, depth=6,
             shadow=False)
        body(comp, "card-body", [rect((CW, CH), roundness=40)], style, slot="background", parent=card, depth=12,
             opacity=100)
    return comp


TEXT = (BELL[0] + 70, CY - 40, TG[0] - TW / 2 - 28 - (BELL[0] + 70), 80)

build_asset(CATEGORY, "notifications-toggle-on", "Notifications Toggle On",
            "Settings-style card with a bell and a switch; a tap flips the switch on and the bell rings. "
            "Type \"Turn on notifications\" between the bell and the switch.",
            ["notifications", "toggle", "switch", "bell", "alerts", "turn on", "subscribe"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold", thumb_t=0.62, text_area=TEXT, description=STYLE_DESC[s])
    for s in STYLES])
