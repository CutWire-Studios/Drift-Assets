from _lt2 import *


def pin_path(cx, cy, r, name="pin"):
    """Map-pin teardrop: circle of radius r centred on (cx, cy) with its point at cy + 1.95 r."""
    k = 0.56 * r
    v = [(cx, cy + 1.95 * r), (cx - r, cy), (cx, cy - r), (cx + r, cy)]
    it = [(0.32 * r, -0.55 * r), (0, 0.62 * r), (-k, 0), (0, -k)]
    ot = [(-0.32 * r, -0.55 * r), (0, -k), (k, 0), (0, 0.62 * r)]
    return path(bezier(v, it, ot, True), name)


def pin_items(cx, cy, r):
    return [group([ellipse((r * 0.8, r * 0.8), (cx, cy)), fill(slot="icon")], "hole"),
            group([pin_path(cx, cy, r), fill(slot="accent")], "pin"),
            group([pin_path(cx, cy, r), fill("#000000", 18)], "pin-shade", position=(4, 5))]


def unroll(comp, x, y, w, h, t0, t1, t2, t3, r=10, slot="primary", roller=True):
    """Bar that unrolls to the right; a darker roller rides the growing edge."""
    if roller:
        rw = 18
        comp.layer("roller", [rrect(x - rw / 2, y - 4, rw, h + 8, rw / 2), fill(slot="secondary")],
                   position=keys((t0, [0, 0], EXPO_OUT), (t1, [w, 0], HOLD), (t2, [w, 0], EXPO_IN), (t3, [0, 0])),
                   opacity=keys((0, 0, HOLD), (t0, 100, HOLD), (t1, 100, EASE_IN), (t1 + 6, 0, HOLD),
                                (t2, 100, HOLD), (t3, 100, HOLD), (t3 + 1, 0)))
    comp.layer("bar", [rect_grow(x, y, w, h, r, t0, t1, t2, t3, "left", start=0), fill(slot=slot)])
    comp.layer("bar-shadow", [rect_grow(x, y + 8, w, h, r, t0, t1, t2, t3, "left", start=0), fill("#000000", 22)])


def pin_drop(comp, cx, cy, r, t0, t_out, ground=True):
    base_y = cy + 1.95 * r
    p = rig(comp, "pin", (cx, base_y),
            opacity=keys((0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 5, 100, HOLD), (t_out + 8, 100, EASE_IN), (t_out + 14, 0)),
            off=keys((0, [0, -110], HOLD), (t0, [0, -110], (0.55, 0, 0.9, 0.5)), (t0 + 10, [0, 0], EASE_OUT),
                     (t0 + 15, [0, -22], EASE_IN), (t0 + 20, [0, 0], HOLD), (t_out, [0, 0], EASE_OUT),
                     (t_out + 6, [0, -30], EASE_IN), (t_out + 14, [0, -110])),
            scale=keys((t0 + 9, [100, 100], EASE_OUT), (t0 + 11, [120, 78], EASE_OUT), (t0 + 16, [96, 104], EASE_IN_OUT),
                       (t0 + 21, [100, 100])))
    comp.layer("pin", pin_items(cx, cy, r), parent=p)
    if ground:
        lay(comp, "ground", [ellipse((r * 1.6, r * 0.4), (cx, base_y + 3)), fill("#000000", 30)], (cx, base_y + 3),
            scale=keys((0, [0, 0], HOLD), (t0, [20, 20], EASE_IN), (t0 + 10, [100, 100], HOLD), (t_out, [100, 100]),
                       (t_out + 12, [0, 0])))


def drop():
    W, H = 1150, 250
    comp = base("lower-third-location-pin", W, H, 40)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#D8DEE9")
    comp.slot("accent", "#EF4444")
    comp.slot("icon", "#FFFFFF")
    cx, cy, r = 84, 88, 46
    pin_drop(comp, cx, cy, r, 0, 128)
    x, y, w, h = 150, 92, 920, 112
    unroll(comp, x, y, w, h, 16, 40, 118, 136)
    return comp, (x + 40, y + 12, w - 80, 58), (x + 40, y + 72, w - 200, 28)


def ripple():
    W, H = 1100, 220
    comp = base("lower-third-location-pin--ripple", W, H, 32)
    comp.slot("primary", "#0F172A")
    comp.slot("secondary", "#1E293B")
    comp.slot("accent", "#38BDF8")
    comp.slot("icon", "#0F172A")
    cx, cy, R = 116, 110, 66
    for i, t in enumerate((16, 44, 72, 100)):
        lay(comp, f"ring{i}", [ellipse((R * 2, R * 2), (cx, cy)), stroke(slot="accent", width=4)], (cx, cy),
            scale=keys((t, [100, 100], EASE_OUT), (t + 28, [165, 165])),
            opacity=keys((t, 70, EASE_OUT), (t + 28, 0)), ip=t, op=t + 29)
    b = rig(comp, "badge", (cx, cy), scale=pop(0, 16, 126, 140))
    comp.layer("pin", pin_items(cx, cy - 16, 24), parent=b)
    comp.layer("disc", [ellipse((R * 2, R * 2), (cx, cy)), fill(slot="primary"),
                        stroke(slot="accent", width=5)], parent=b)
    x, y, w, h = cx, cy - 44, 900, 88
    comp.layer("bar", [rect_grow(x, y, w, h, h / 2, 8, 30, 120, 138, "left", start=0), fill(slot="secondary")])
    return comp, (cx + R + 30, y + 16, w - R - 80, h - 32)


def route():
    W, H = 1200, 250
    comp = base("lower-third-location-pin--route", W, H, 44)
    comp.slot("primary", "#FFF7E6")
    comp.slot("secondary", "#E9D8B4")
    comp.slot("accent", "#2A9D8F")
    comp.slot("icon", "#FFF7E6")
    cx, cy, r = 240, 84, 40
    tip = (cx, cy + 1.95 * r)
    trail = path(bezier([(24, 200), (120, 150), tip], [(0, 0), (-50, 30), (-40, 10)], [(40, -20), (50, -30), (0, 0)],
                        False), "trail")
    comp.layer("trail", [trail, trim(end=keys((0, 0, INOUT), (18, 100)), start=keys((120, 0, INOUT), (136, 100))),
                         dstroke(0.5, 13, slot="accent", width=6)])
    lay(comp, "start", [ellipse((16, 16), (24, 200)), fill(slot="accent")], (24, 200), scale=pop(0, 8, 130, 140))
    b = rig(comp, "pin", tip, scale=keys((0, [0, 0], HOLD), (16, [0, 0], SPRING), (28, [100, 100], HOLD),
                                         (124, [100, 100], EXPO_IN), (136, [0, 0])))
    comp.layer("pin", pin_items(cx, cy, r), parent=b)
    x, y, w, h = cx + 60, 70, 880, 110
    unroll(comp, x, y, w, h, 24, 48, 116, 134, r=h / 2)
    return comp, (x + 50, y + 12, w - 100, 56), (x + 50, y + 70, w - 220, 28)


a, ah, asub = drop()
b, bh = ripple()
c, chd, cs = route()
build("lower-third-location-pin", "Location Pin Lower Third",
      "Place-name lower third: a map pin drops in and a bar unrolls beside it. Put the place in the headline "
      "row and a region or country beneath it.",
      ["lower third", "location", "map", "pin", "place", "travel", "vlog"], [
          V("drop", "Pin Drop", a, ah, asub,
            description="The pin falls in with a squash and bounce, then a bar unrolls to the right."),
          V("ripple", "Ripple Badge", b, bh,
            description="Single line: a round pin badge sends out sonar ripples while a capsule extends."),
          V("route", "Dashed Route", c, chd, cs,
            description="A dashed travel route draws up to the pin before the bar unrolls from it."),
      ])
