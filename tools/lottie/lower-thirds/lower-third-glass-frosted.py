from _lt2 import *

HIGHLIGHT = [(0, "#FFFFFF", 0.42), (0.55, "#FFFFFF", 0.06), (1, "#FFFFFF", 0.0)]


def pane(comp, name, x, y, w, h, r, t0, t1, t2, t3, side="left", sweep=None, parent=None, start=None):
    """Frosted pane that grows from `side`: rim, top highlight, sheen, tint, frost and shadow."""
    g = lambda: rect_grow(x, y, w, h, r, t0, t1, t2, t3, side, start=start)
    comp.layer(f"{name}-rim", [g(), stroke(slot="outline", width=2.5, opacity=75)], parent=parent)
    comp.layer(f"{name}-rim-inner", [rect_grow(x + 3, y + 3, w - 6, h - 6, r - 3, t0, t1, t2, t3, side,
                                               start=None if start is None else start - 6),
                                     stroke("#FFFFFF", width=1.2, opacity=22)], parent=parent)
    comp.layer(f"{name}-hi", [g(), gradient_fill(HIGHLIGHT, (0, y), (0, y + h * 0.7))], parent=parent)
    if sweep:
        sheen(comp, [rrect(x, y, w, h, r)], x, x + w, y, y + h, *sweep, parent=parent, width=110, op=22)
    comp.layer(f"{name}-tint", [g(), fill(slot="primary", opacity=24)], parent=parent)
    comp.layer(f"{name}-frost", [g(), fill("#0B0B1A", opacity=16)], parent=parent)
    comp.layer(f"{name}-shadow", [group([g(), fill("#000000", 10)], "s0", position=(0, 10)),
                                  group([g(), fill("#000000", 8)], "s1", position=(0, 18))], parent=parent)


def bar():
    W, H = 1100, 250
    x, y, w, h, r = 50, 44, 920, 156, 30
    comp = base("lower-third-glass-frosted", W, H, 34)
    comp.slot("primary", "#FFFFFF")
    comp.slot("outline", "#FFFFFF")
    comp.slot("accent", "#7CF2FF")
    lay(comp, "accent", [rrect(x + 26, y + 30, 8, h - 60, 4), fill(slot="accent")], (x + 30, y + h / 2),
        scale=grow_y(10, 26, 118, 128))
    lay(comp, "divider", [rrect(x + 58, y + 102, 420, 2, 1), fill(slot="outline", opacity=40)], (x + 58, 0),
        scale=grow_x(16, 36, 116, 128))
    rg = rig(comp, "rig", (x, y + h / 2), off=slide(0, 26, 0, 20, 124, 146, EXPO_OUT, EXPO_IN, ody=18),
             opacity=fade(0, 8, 136, 146))
    pane(comp, "card", x, y, w, h, r, 0, 26, 122, 144, "left", sweep=(22, 52), parent=rg)
    return comp, (x + 58, y + 26, w - 100, 66), (x + 58, y + 112, w - 100, 30)


def pill():
    W, H = 1000, 200
    w, h = 800, 100
    x, y = (W - w) / 2, (H - h) / 2
    comp = base("lower-third-glass-frosted--pill", W, H, 30)
    comp.slot("primary", "#FFFFFF")
    comp.slot("outline", "#FFFFFF")
    comp.slot("accent", "#FF8AD8")
    for i, (dx, s) in enumerate(((x + 50, 18), (x + w - 50, 18))):
        lay(comp, f"dot{i}", [group([ellipse((s * 2.2, s * 2.2), (dx, H / 2)), fill(slot="accent", opacity=25)], "halo"),
                              group([ellipse((s, s), (dx, H / 2)), fill(slot="accent")], "dot")], (dx, H / 2),
            scale=pop(12 + 3 * i, 26 + 3 * i, 118, 128))
    rg = rig(comp, "rig", (W / 2, H / 2),
             scale=keys((0, [60, 60], SPRING), (18, [100, 100], HOLD), (124, [100, 100], EXPO_IN), (142, [70, 70])),
             opacity=fade(0, 6, 134, 142))
    pane(comp, "pill", x, y, w, h, h / 2, 2, 24, 122, 140, "centre", sweep=(20, 50), parent=rg)
    return comp, (x + 90, y + 18, w - 180, h - 36)


def stacked():
    W, H = 1080, 250
    comp = base("lower-third-glass-frosted--stacked", W, H, 38)
    comp.slot("primary", "#FFFFFF")
    comp.slot("outline", "#FFFFFF")
    comp.slot("accent", "#FFD36E")
    a = (48, 36, 860, 104)
    b = (48, 152, 520, 58)
    lay(comp, "accent", [rrect(a[0] + 26, a[1] + a[3] - 14, 140, 4, 2), fill(slot="accent")], (a[0] + 26, 0),
        scale=grow_x(18, 36, 114, 124))
    r1 = rig(comp, "rig-a", (0, 0), off=slide(0, 44, 0, 22, 126, 144, EXPO_OUT, EXPO_IN, ody=-30),
             opacity=fade(0, 8, 134, 144))
    pane(comp, "headline", *a, 24, 0, 20, 128, 144, "middle", sweep=(20, 46), parent=r1, start=a[3] * 0.4)
    r2 = rig(comp, "rig-b", (0, 0), off=slide(0, 44, 7, 29, 120, 138, EXPO_OUT, EXPO_IN, ody=-30),
             opacity=fade(7, 15, 128, 138))
    pane(comp, "subtitle", *b, 18, 7, 27, 122, 138, "middle", sweep=(26, 52), parent=r2, start=b[3] * 0.4)
    return comp, (a[0] + 30, a[1] + 16, a[2] - 60, a[3] - 38), (b[0] + 26, b[1] + 12, b[2] - 52, b[3] - 24)


c, hd, sb = bar()
p, ph = pill()
s, sh, ss = stacked()
BG = "3b2a55"
build("lower-third-glass-frosted", "Frosted Glass Lower Third",
      "Translucent frosted-glass lower third with a bright rim and a light sheen sweeping across. Your name "
      "goes in the headline row and a role or caption in the subtitle row.",
      ["lower third", "glass", "frosted", "glassmorphism", "modern", "clean", "name"], [
          V("bar", "Glass Card", c, hd, sb, bg=BG,
            description="Two-line frosted card that grows from the left with an accent tick and divider."),
          V("pill", "Glass Pill", p, ph, bg=BG,
            description="Single-line centred glass capsule that springs open from the middle."),
          V("stacked", "Stacked Panes", s, sh, ss, bg=BG,
            description="Separate headline and subtitle glass panes that rise in one after the other."),
      ])
