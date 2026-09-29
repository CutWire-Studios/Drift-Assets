from _lt2 import *


def tube(comp, name, shapes, slot, t_on, t_off, width=6, trim_item=None, parent=None, pattern=None):
    items = glow_strokes(shapes, slot=slot, width=width)
    if trim_item:
        items = [group(g["it"][:-2] + [trim_item] + g["it"][-2:-1], g["nm"]) for g in items]
    return comp.layer(name, items, opacity=flicker(t_on, t_off, pattern), parent=parent)


def frame():
    W, H = 1100, 260
    x, y, w, h = 60, 50, 860, 116
    comp = base("lower-third-neon-outline", W, H, 34)
    comp.slot("primary", "#FF3DCB")
    comp.slot("accent", "#3DF2FF")
    # subtitle underline tube in the accent colour, then the main frame
    tube(comp, "underline", [poly([(x + 30, y + h + 42), (x + 460, y + h + 42)], closed=False)], "accent", 16, 124,
         width=5, pattern=[(0, 0), (2, 100), (3, 0), (6, 100), (8, 40), (9, 100)])
    tube(comp, "frame", [rrect(x, y, w, h, 22)], "primary", 4, 120)
    comp.layer("inner-wash", [rrect(x, y, w, h, 22), fill(slot="primary", opacity=7)],
               opacity=flicker(4, 120, v=100))
    return comp, (x + 36, y + 22, w - 72, h - 44), (x + 30, y + h + 6, 520, 30)


def draw_on():
    W, H = 1100, 250
    x, y, w, h = 60, 60, 880, 108
    comp = base("lower-third-neon-outline--draw", W, H, 44)
    comp.slot("primary", "#39FF88")
    comp.slot("accent", "#FFE14D")
    # a spark rides the drawing head; the tube itself draws on with trim then flickers once
    shapes = [rrect(x, y, w, h, h / 2)]
    tr = trim(end=keys((0, 0, INOUT), (34, 100)), offset=keys((0, -25, INOUT), (34, 0)),
              start=keys((122, 0, INOUT), (144, 100)))
    items = glow_strokes(shapes, slot="primary", width=6)
    items = [group(g["it"][:-2] + [tr] + g["it"][-2:-1], g["nm"]) for g in items]
    comp.layer("tube", items, opacity=keys((0, 100, HOLD), (36, 30, HOLD), (38, 100, HOLD), (40, 50, HOLD),
                                             (41, 100, HOLD), (120, 100)))
    # accent end-caps pop when the draw completes
    for i, cx in enumerate((x - 26, x + w + 26)):
        lay(comp, f"cap{i}", glow_strokes([ellipse((12, 12), (cx, y + h / 2))], slot="accent", width=5,
                                          widths=(22, 12, 8), ops=(10, 18, 30)),
            (cx, y + h / 2), scale=pop(32 + 2 * i, 44 + 2 * i, 116, 126))
    return comp, (x + 60, y + 20, w - 120, h - 40)


def split():
    W, H = 1100, 260
    comp = base("lower-third-neon-outline--split", W, H, 40)
    comp.slot("primary", "#FF4D6D")
    comp.slot("accent", "#4DB8FF")
    a = (190, 40, 720, 104)
    b = (340, 170, 420, 54)
    tube(comp, "sub", [rrect(*b, 12)], "accent", 18, 122, width=5,
         pattern=[(0, 0), (1, 100), (3, 0), (7, 100), (9, 30), (11, 100)])
    tube(comp, "head", [chamfer(*a, 22, (1, 1, 1, 1))], "primary", 2, 126)
    for i, xx in enumerate((a[0] - 48, a[0] + a[2] + 48)):
        pts = [(xx - 14, a[1] + a[3] / 2), (xx + 14, a[1] + a[3] / 2)]
        tube(comp, f"dash{i}", [poly(pts, closed=False)], "primary", 12 + 2 * i, 118, width=5)
    return comp, (a[0] + 44, a[1] + 20, a[2] - 88, a[3] - 40), (b[0] + 24, b[1] + 10, b[2] - 48, b[3] - 20)


f, fh, fs = frame()
d, dh = draw_on()
s, sh, ss = split()
build("lower-third-neon-outline", "Neon Outline Lower Third",
      "Glowing neon-tube outline that flickers on like a sign. Type your name inside the tube and an optional "
      "caption on the second row.",
      ["lower third", "neon", "glow", "outline", "night", "retro", "sign"], [
          V("frame", "Neon Frame", f, fh, fs,
            description="Rounded neon frame that flickers on with a second-colour underline for the subtitle."),
          V("draw", "Draw-On Tube", d, dh,
            description="Single-line capsule tube that draws itself on, with glowing end caps."),
          V("split", "Split Tubes", s, sh, ss,
            description="Centred cut-corner headline tube and a separate subtitle tube, each flickering in turn."),
      ])
