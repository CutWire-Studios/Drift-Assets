from _lt2 import *


def paper(comp, name, shape, slot, pivot, t0, t2, sx=False, parent=None, depth=1.0):
    """Paper layer with a soft stacked shadow, springing up from `pivot`."""
    sc = keys((0, [100 if not sx else 0, 0], HOLD), (t0, [100 if not sx else 0, 0], SPRING),
              (t0 + 16, [100, 100], HOLD), (t2, [100, 100], BACK_IN), (t2 + 14, [100 if not sx else 0, 0]))
    items = [group([shape, fill(slot=slot)], "paper"),
             group([shape, stroke("#FFFFFF", width=1.5, opacity=22)], "edge")]
    for i, (dy, op, sc_) in enumerate(((4, 16, 100), (9, 9, 101), (15, 6, 102))):
        items.append(group([shape, fill("#000000", op)], f"shadow{i}", position=(0, dy * depth)))
    return lay(comp, name, items, pivot, scale=sc, parent=parent)


def wave_top(x, y, w, h, amp, waves, phase=0.0, name="hill"):
    """Filled shape: wavy top edge from x to x+w at y, flat bottom at y+h."""
    n = waves * 4
    pts = [(x + w * i / n, y + amp * math.sin(phase + 2 * math.pi * waves * i / n)) for i in range(n + 1)]
    step = w / n
    it, ot = [], []
    for i, (px, py) in enumerate(pts):
        d = amp * 2 * math.pi * waves / w * math.cos(phase + 2 * math.pi * waves * i / n)
        it.append((-step / 3, -d * step / 3))
        ot.append((step / 3, d * step / 3))
    v = pts + [(x + w, y + h), (x, y + h)]
    it += [(0, 0), (0, 0)]
    ot += [(0, 0), (0, 0)]
    it[0] = (0, 0)
    ot[n] = (0, 0)
    return path(bezier(v, it, ot, True), name)


def layers():
    W, H = 1100, 260
    comp = base("lower-third-paper-cut", W, H, 36)
    comp.slot("primary", "#FFF8EC")
    comp.slot("secondary", "#2E86AB")
    comp.slot("accent", "#F6AE2D")
    bot = 216
    specs = [("front", (100, 92, 800, 124), "primary", 12, 118),
             ("middle", (78, 62, 850, 154), "accent", 6, 122),
             ("back", (56, 32, 900, 184), "secondary", 0, 126)]
    for nm, (x, y, w, h), slot, t0, t2 in specs:
        paper(comp, nm, rrect(x, y, w, h, 20), slot, (x + w / 2, bot), t0, t2)
    return comp, (140, 104, 720, 58), (140, 166, 560, 32)


def wavy():
    W, H = 1100, 270
    comp = base("lower-third-paper-cut--wavy", W, H, 40)
    comp.slot("primary", "#FDF6E3")
    comp.slot("secondary", "#6A994E")
    comp.slot("accent", "#A7C957")
    x, w, bot = 50, 960, 236
    specs = [("front", 110, 16, 2, 1.2, "primary", 14, 116),
             ("middle", 76, 16, 3, 0.2, "accent", 7, 120),
             ("back", 40, 18, 2, 2.6, "secondary", 0, 124)]
    for nm, y, amp, waves, ph, slot, t0, t2 in specs:
        paper(comp, nm, wave_top(x, y, w, bot - y, amp, waves, ph), slot, (x + w / 2, bot), t0, t2)
    return comp, (x + 80, 134, w - 160, 54), (x + 80, 192, w - 300, 30)


def tag_shape(x, y, w, h, notch):
    return poly([(x + notch, y), (x + w, y), (x + w, y + h), (x + notch, y + h), (x, y + h / 2)], name="tag")


def ribbon_shape(x, y, w, h, fork):
    return poly([(x, y), (x + w, y), (x + w - fork, y + h / 2), (x + w, y + h), (x, y + h)], name="ribbon")


def tags():
    W, H = 1100, 270
    comp = base("lower-third-paper-cut--tags", W, H, 38)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#E76F51")
    comp.slot("accent", "#264653")
    hx, hy, hw, hh = 60, 40, 860, 116
    rx, ry, rw, rh = 150, 170, 480, 56
    # punched hole on the tag
    lay(comp, "hole", [ellipse((20, 20), (hx + 42, hy + hh / 2)), fill(slot="accent")], (hx + 42, hy + hh / 2),
        scale=pop(18, 28, 118, 126))
    r1 = rig(comp, "head-rig", (hx, hy + hh / 2), rotation=keys((0, -8, SPRING), (18, 0, HOLD), (122, 0, EXPO_IN),
                                                                  (136, 6)))
    paper(comp, "head", tag_shape(hx, hy, hw, hh, 44), "primary", (hx, hy + hh / 2), 0, 122, sx=True, parent=r1)
    paper(comp, "head-back", tag_shape(hx + 10, hy + 10, hw, hh, 44), "secondary", (hx, hy + hh / 2), 4, 124,
          sx=True, parent=r1)
    r2 = rig(comp, "rib-rig", (rx, ry + rh / 2), rotation=keys((10, 6, SPRING), (26, 0, HOLD), (116, 0, EXPO_IN),
                                                                 (130, -5)))
    paper(comp, "ribbon", ribbon_shape(rx, ry, rw, rh, 26), "accent", (rx, ry + rh / 2), 10, 116, sx=True, parent=r2)
    return comp, (hx + 80, hy + 20, hw - 120, hh - 40), (rx + 30, ry + 12, rw - 90, rh - 24)


a, ah, asub = layers()
b, bh, bs = wavy()
c, chd, cs = tags()
build("lower-third-paper-cut", "Paper Cut Lower Third",
      "Layered paper-cut lower third: stacked card shapes with soft shadows pop up one after another. Your "
      "name goes on the front layer with a subtitle under it.",
      ["lower third", "paper", "papercut", "layered", "craft", "soft", "shadow"], [
          V("layers", "Stacked Layers", a, ah, asub,
            description="Three rounded paper layers spring up from the bottom, back to front."),
          V("wavy", "Wavy Hills", b, bh, bs,
            description="Paper layers with wavy, hill-like top edges that rise in like a pop-up book."),
          V("tags", "Tag and Ribbon", c, chd, cs,
            description="A notched paper tag and a forked ribbon unfold sideways with a little swing."),
      ])
