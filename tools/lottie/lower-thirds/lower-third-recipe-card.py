from _lt2 import *


def whisk(cx, cy, s, slot="icon"):
    """Whisk centred on (cx, cy), s px tall: three wire loops over a handle, pointing up."""
    top, neck = cy - s * 0.5, cy + s * 0.12
    wires = []
    for i, f in enumerate((0.5, 0.33, 0.14)):
        hw = s * f / 2
        # a teardrop loop: meets at the neck, bulges out and rounds over the top
        v = [(cx, neck), (cx - hw, top + s * 0.28), (cx, top), (cx + hw, top + s * 0.28)]
        it = [(hw * 0.4, -s * 0.05), (0, s * 0.16), (-hw * 0.56, 0), (0, -s * 0.16)]
        ot = [(-hw * 0.4, -s * 0.05), (0, -s * 0.16), (hw * 0.56, 0), (0, s * 0.16)]
        wires.append(path(bezier(v, it, ot, True), f"wire{i}"))
    return [group(wires + [stroke(slot=slot, width=s * 0.04)], "wires"),
            group([rrect(cx - s * 0.06, neck - s * 0.02, s * 0.12, s * 0.4, s * 0.06), fill(slot=slot)], "handle")]


def dotted(x0, x1, y, slot="accent", width=5, gap=14, opacity=100):
    return [poly([(x0, y), (x1, y)], False, "dots"),
            dstroke(0.5, gap, slot=slot, width=width, cap="round", opacity=opacity)]


def stir(t0, t_out, amp=14):
    """Whisking wobble during the hold."""
    k = [(t0, -40, EXPO_OUT), (t0 + 14, 0, EASE_IN_OUT)]
    t, s = t0 + 24, 1
    while t < t_out - 8:
        k.append((t, amp * s, EASE_IN_OUT))
        s = -s
        t += 10
    k += [(t_out - 2, 0, EXPO_IN), (t_out + 12, 40)]
    return keys(*k)


def card():
    W, H = 1100, 250
    comp = base("lower-third-recipe-card", W, H, 38)
    comp.slot("background", "#FFF8EE")
    comp.slot("accent", "#E07A5F")
    comp.slot("icon", "#FFFFFF")
    comp.slot("secondary", "#3D405B")
    x, y, w, h = 60, 30, 940, 186
    cx, cy, R = x + 90, y + h / 2, 58
    b = rig(comp, "badge", (cx, cy), scale=pop(8, 22, 124, 136))
    lay(comp, "whisk", whisk(cx, cy, 80), (cx, cy + 10), parent=b, rotation=stir(8, 120, 10))
    comp.layer("disc", [ellipse((R * 2, R * 2), (cx, cy)), fill(slot="accent")], parent=b)
    d = dotted(x + 180, x + w - 40, y + 118, "accent")
    comp.layer("divider", [d[0], draw(16, 40, 116, 132), d[1]])
    c = rig(comp, "card", (x + w / 2, y + h), off=slide(0, 60, 0, 22, 126, 144), opacity=fade(0, 8, 136, 144))
    comp.layer("edge", [rrect(x + 10, y + 10, w - 20, h - 20, 12), dstroke(10, 8, slot="secondary", width=2,
                                                                          opacity=25)], parent=c)
    comp.layer("face", [rrect(x, y, w, h, 18), fill(slot="background")], parent=c)
    comp.layer("shadow", shadow(x, y, w, h, 18, dy=10, n=4, spread=5, op=7), parent=c)
    return comp, (x + 180, y + 34, w - 230, 66), (x + 180, y + 132, w - 230, 32)


def spoon_fork(cx, cy, s, slot="icon"):
    sp = [group([ellipse((s * 0.26, s * 0.36), (cx, cy - s * 0.3)),
                 rrect(cx - s * 0.035, cy - s * 0.14, s * 0.07, s * 0.62, s * 0.035), fill(slot=slot)], "spoon")]
    tines = [rrect(cx + dx - s * 0.02, cy - s * 0.48, s * 0.04, s * 0.2, s * 0.02) for dx in (-s * 0.08, 0, s * 0.08)]
    fk = [group(tines + [rrect(cx - s * 0.12, cy - s * 0.3, s * 0.24, s * 0.1, s * 0.05),
                         rrect(cx - s * 0.035, cy - s * 0.24, s * 0.07, s * 0.72, s * 0.035), fill(slot=slot)],
                "fork")]
    return [group(sp, "spoon-rot", anchor=(cx, cy), position=(cx, cy), rotation=-28),
            group(fk, "fork-rot", anchor=(cx, cy), position=(cx, cy), rotation=28)]


def index_card():
    W, H = 1100, 270
    comp = base("lower-third-recipe-card--index", W, H, 36)
    comp.slot("background", "#FFFFFF")
    comp.slot("accent", "#D62828")
    comp.slot("icon", "#D62828")
    comp.slot("secondary", "#8ECAE6")
    x, y, w, h = 70, 40, 920, 190
    c = rig(comp, "card", (x + w / 2, y + h / 2),
            off=keys((0, [0, -60], EXPO_OUT), (18, [0, 0], HOLD), (124, [0, 0], EXPO_IN), (140, [0, 60])),
            rotation=keys((0, -7, SPRING), (20, -1.2, HOLD), (124, -1.2, EXPO_IN), (140, 4)),
            opacity=fade(0, 6, 134, 140))
    ic = (x + w - 80, y + 100)
    lay(comp, "utensils", spoon_fork(*ic, 100), ic, parent=c, scale=pop(14, 28, 118, 128),
        rotation=keys((14, -60, EXPO_OUT), (30, 0)))
    comp.layer("dots", dotted(x + 40, x + w - 170, y + 124, "icon", 4, 12), parent=c)
    rules = [rrect(x + 20, y + 58 + i * 36, w - 40, 2) for i in (0, 2, 3)]
    comp.layer("rules", rules + [fill(slot="secondary", opacity=70)], parent=c)
    comp.layer("margin", [rrect(x + 26, y + 30, 3, h - 40), fill(slot="accent", opacity=45)], parent=c)
    comp.layer("stripe", [rrect(x, y, w, 30, 0), fill(slot="accent")], parent=c)
    comp.layer("face", [rrect(x, y, w, h, 6), fill(slot="background")], parent=c)
    comp.layer("shadow", shadow(x, y, w, h, 6, dy=10, n=4, spread=5, op=7), parent=c)
    return comp, (x + 44, y + 50, w - 230, 64), (x + 44, y + 134, w - 230, 36)


def pill():
    W, H = 1100, 230
    comp = base("lower-third-recipe-card--pill", W, H, 36)
    comp.slot("background", "#2F3E46")
    comp.slot("accent", "#F4A261")
    comp.slot("icon", "#2F3E46")
    comp.slot("secondary", "#F4A261")
    cx, cy, R = 104, 100, 62
    b = rig(comp, "badge", (cx, cy), scale=pop(0, 16, 126, 140), rotation=keys((0, -200, EXPO_OUT), (20, 0)))
    lay(comp, "whisk", whisk(cx, cy, 80), (cx, cy + 10), parent=b, rotation=stir(20, 120, 12))
    comp.layer("disc", [ellipse((R * 2, R * 2), (cx, cy)), fill(slot="accent")], parent=b)
    d = dotted(cx + R + 20, cx + 700, cy + 76, "secondary", 6, 16)
    comp.layer("dots", [d[0], draw(18, 44, 114, 132), d[1]])
    x, y, w, h = cx, cy - 46, 900, 92
    comp.layer("bar", [rect_grow(x, y, w, h, h / 2, 6, 28, 120, 138, "left", start=0), fill(slot="background")])
    return comp, (cx + R + 30, y + 16, w - R - 80, h - 32), (cx + R + 20, cy + 88, 680, 30)


a, ah, asub = card()
b, bh, bs = index_card()
c, chd, cs = pill()
build("lower-third-recipe-card", "Recipe Card Lower Third",
      "Cooking lower third: a recipe card with a whisk or utensil icon and a dotted divider. Put the dish name "
      "on top and a detail such as time or servings under the divider.",
      ["lower third", "recipe", "cooking", "food", "kitchen", "whisk", "chef"], [
          V("card", "Whisk Card", a, ah, asub,
            description="Cream card rises in, a whisk badge pops and keeps whisking, and a dotted divider draws on."),
          V("index", "Index Card", b, bh, bs, bg="e8e8ee",
            description="A tilted ruled index card with a red header stripe and crossed spoon and fork."),
          V("pill", "Whisk Pill", c, chd, cs,
            description="Compact capsule with a spinning whisk badge and a dotted underline for the detail."),
      ])
