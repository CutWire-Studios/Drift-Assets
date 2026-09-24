from _common import *

W, H, F = 700, 90, 75
comp = Comp("health-bar", W, H, fps=30, frames=F)
comp.slot("primary", "#3BD45B")
comp.slot("secondary", "#F5C518")
comp.slot("accent", "#E8322E")
comp.slot("outline", "#0B0B10")
comp.slot("background", "#23232B")
comp.slot("icon", "#FFFFFF")

CY = H / 2
FX, FW, FH = 84, 602, 46          # frame
TX, TW, TH = FX + 5, FW - 10, FH - 10  # inner track
HIT1, HIT2 = 24, 48
P1, P2 = 45, 15                   # health after each hit (%)


def bar(keys):
    """Left-anchored rect whose width follows [(frame, percent, easing)]."""
    size = anim([(t, [TW * p / 100, TH], e) for t, p, e in keys])
    pos = anim([(t, [TX + TW * p / 200, CY], e) for t, p, e in keys])
    return rect(size, pos, 5)


def span(p0, p1):
    x0, x1 = TX + TW * p0 / 100, TX + TW * p1 / 100
    return rect((x1 - x0, TH), ((x0 + x1) / 2, CY), 0)


fill_keys = [(4, 0, SNAP_OUT), (18, 100, HOLD), (HIT1, P1, HOLD), (HIT2, P2, HOLD), (F, P2, HOLD)]
trail_keys = [(4, 0, SNAP_OUT), (18, 100, HOLD), (HIT1 + 7, 100, EASE_IN_OUT), (HIT1 + 18, P1, HOLD),
              (HIT2 + 7, P1, EASE_IN_OUT), (HIT2 + 18, P2, HOLD), (F, P2, HOLD)]

shake = []
for h in (HIT1, HIT2):
    for i, dx in enumerate((7, -6, 4, -2, 0)):
        shake.append((h + i, [W / 2 + dx, CY + (2 if i % 2 == 0 and i < 3 else 0)], LINEAR))
rig = comp.null("rig", anchor=(W / 2, CY),
                position=anim([(0, [W / 2, CY + 8], SNAP_OUT), (10, [W / 2, CY], HOLD)] + shake + [(F, [W / 2, CY])]),
                opacity=anim([(0, 0, EASE_OUT), (6, 100)]))

# icon cap: medical cross
comp.layer("icon", [
    group([rect((12, 36), (0, 0), 2), rect((36, 12), (0, 0), 2), fill(slot="icon")], "cross"),
], parent=rig, position=(45, CY),
    scale=anim([(2, [0, 0], OVERSHOOT), (12, [100, 100], HOLD), (HIT1, [125, 125], SNAP_OUT),
                (HIT1 + 8, [100, 100], HOLD), (HIT2, [125, 125], SNAP_OUT), (HIT2 + 8, [100, 100])]))
comp.layer("icon plate", [
    group([rect((62, 62), (45, CY), 12),
           gradient_fill([(0, "#FFFFFF", 0.14), (0.5, "#FFFFFF", 0.0), (1, "#000000", 0.0)],
                         (0, CY - 31), (0, CY + 31))], "gloss"),
    box(19, CY - 26, 52, 52, r=8, slot="accent", name="plate"),
    box(14, CY - 31, 62, 62, r=12, slot="outline", name="rim"),
], parent=rig)

# top gloss and segment dividers over the fill
comp.layer("gloss", [
    group([rect((TW, TH), (TX + TW / 2, CY), 5),
           gradient_fill([(0, "#FFFFFF", 0.35), (0.45, "#FFFFFF", 0.08), (0.5, "#FFFFFF", 0.0),
                          (1, "#000000", 0.18)], (0, CY - TH / 2), (0, CY + TH / 2))], "gloss"),
], parent=rig)
comp.layer("segments", [
    group([rect((3, TH), (TX + TW * i / 10, CY)) for i in range(1, 10)] +
          [fill(slot="outline", opacity=55)], "dividers"),
], parent=rig)

for h, p0, p1 in ((HIT1, P1, 100), (HIT2, P2, P1)):
    comp.layer(f"flash {h}", [group([span(p0, p1), fill("#FFFFFF")], "chunk")], parent=rig,
               opacity=anim([(h - 1, 0, HOLD), (h, 100, HOLD), (h + 2, 100, EASE_OUT), (h + 9, 0)]))
    comp.layer(f"fill flash {h}", [group([bar(fill_keys), fill("#FFFFFF")], "flash")], parent=rig,
               opacity=anim([(h - 1, 0, HOLD), (h, 70, EASE_OUT), (h + 6, 0)]))

comp.layer("fill red", [group([bar(fill_keys), fill(slot="accent")], "fill")], parent=rig,
           opacity=anim([(HIT2 - 1, 0, HOLD), (HIT2, 100)]))
comp.layer("fill yellow", [group([bar(fill_keys), fill(slot="secondary")], "fill")], parent=rig,
           opacity=anim([(HIT1 - 1, 0, HOLD), (HIT1, 100)]))
comp.layer("fill green", [group([bar(fill_keys), fill(slot="primary")], "fill")], parent=rig)
comp.layer("trail", [group([bar(trail_keys),
                            fill(anim([(HIT1, hex_color("#FF5A36"), HOLD), (HIT2, hex_color("#FFD84A"), HOLD), (F, hex_color("#FFD84A"))]))],
                           "trail")], parent=rig)

comp.layer("frame", [
    box(TX, CY - TH / 2, TW, TH, r=5, slot="background", name="track"),
    box(FX + 2, CY - FH / 2 + 2, FW - 4, FH - 4, "#FFFFFF", r=9, opacity=10, name="bevel"),
    box(FX, CY - FH / 2, FW, FH, r=10, slot="outline", name="frame"),
], parent=rig)

finish(comp, "health-bar", "Health Bar",
       "Game HP bar with a medical-cross icon cap: fills up, takes two hits that flash white and drain "
       "with a delayed damage trail, turning from green to yellow to red.",
       ["health", "hp", "bar", "damage", "life", "gaming", "hud"], "intro-hold",
       thumb_t=0.44, region=(6, 0, 440, 90))
