from _lt2 import *

W, H = 1100, 250


def slots(comp, a="#FFFFFF", b="#111827", c="#22C55E"):
    comp.slot("primary", a)
    comp.slot("secondary", b)
    comp.slot("accent", c)


def stagger():
    comp = base("lower-third-stacked-bars", W, H, 34)
    slots(comp)
    x = 60
    bars = [("head", (x, 36, 840, 92), "primary", 0, 128),
            ("sub", (x + 30, 134, 560, 46), "secondary", 6, 122),
            ("accent", (x + 60, 186, 240, 14), "accent", 12, 116)]
    for nm, box, slot, t0, t2 in bars:
        bx, by, bw, bh = box
        lay(comp, f"{nm}-cap", [rrect(bx, by, 10, bh), fill(slot="accent")], (bx, by + bh / 2),
            off=slide(-40, 0, t0, t0 + 18, t2, t2 + 14), opacity=fade(t0, t0 + 4, t2 + 10, t2 + 14))
        wipe(comp, nm, [rrect(*box), fill(slot=slot)], box, t0 + 2, t0 + 24, t2, t2 + 16, "left")
    comp.layer("shadow", [rrect(x + 6, 44, 840, 92), rrect(x + 36, 142, 560, 46), fill("#000000", 22)],
               opacity=fade(20, 30, 118, 126))
    return comp, (x + 36, 50, 780, 64), (x + 58, 142, 510, 30)


def drop():
    comp = base("lower-third-stacked-bars--drop", W, H, 40)
    slots(comp, "#FFE66D", "#1A1A2E", "#FF6B6B")
    x = 60
    bars = [("head", (x, 34, 820, 96), "primary", 16, 118),
            ("sub", (x, 138, 560, 50), "secondary", 8, 122),
            ("accent", (x, 196, 300, 16), "accent", 0, 126)]
    for nm, box, slot, t0, t2 in bars:
        bx, by, bw, bh = box
        fall = -70
        lay(comp, nm, [rrect(*box, 6), fill(slot=slot)], (bx + bw / 2, by + bh),
            off=keys((0, [0, fall], HOLD), (t0, [0, fall], (0.55, 0, 0.9, 0.5)), (t0 + 10, [0, 0], EASE_OUT),
                     (t0 + 15, [0, -12], EASE_IN), (t0 + 20, [0, 0], HOLD), (t2, [0, 0], BACK_IN),
                     (t2 + 14, [0, 60])),
            scale=keys((t0 + 9, [100, 100], EASE_OUT), (t0 + 11, [104, 86], EASE_OUT), (t0 + 16, [100, 100])),
            opacity=keys((0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 5, 100, HOLD), (t2 + 8, 100, EASE_IN), (t2 + 14, 0)))
    return comp, (x + 30, 50, 760, 64), (x + 30, 148, 500, 30)


def centred():
    comp = base("lower-third-stacked-bars--centred", W, H, 36)
    slots(comp, "#FFFFFF", "#3A0CA3", "#F72585")
    cx = W / 2
    bars = [("accent", (cx - 70, 28, 140, 12), "accent", 0, 128),
            ("head", (cx - 420, 50, 840, 92), "primary", 5, 124),
            ("sub", (cx - 280, 150, 560, 50), "secondary", 11, 118)]
    for nm, (bx, by, bw, bh), slot, t0, t2 in bars:
        comp.layer(nm, [rect_grow(bx, by, bw, bh, 4, t0, t0 + 22, t2, t2 + 16, "centre", start=0), fill(slot=slot)])
    return comp, (cx - 390, 64, 780, 64), (cx - 250, 160, 500, 30)


a, ah, asub = stagger()
b, bh, bs = drop()
c, chd, cs = centred()
build("lower-third-stacked-bars", "Stacked Bars Lower Third",
      "Three staggered bars (headline, subtitle and a thin accent) that stack in one after another. Type the "
      "name in the big bar and a subtitle in the second.",
      ["lower third", "bars", "stacked", "stagger", "name", "clean", "corporate"], [
          V("stagger", "Staggered Slide", a, ah, asub,
            description="Left-aligned bars wipe in from the left in quick succession behind accent caps."),
          V("drop", "Drop Stack", b, bh, bs, bg="e8e8ee",
            description="Bars fall in from above, bottom first, each landing with a squash and bounce."),
          V("centred", "Centred Stack", c, chd, cs,
            description="Centred bars open outward from the middle, accent first."),
      ])
