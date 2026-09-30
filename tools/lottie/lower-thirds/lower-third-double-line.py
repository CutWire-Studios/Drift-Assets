from _lt2 import *

W, H = 1100, 230
X0, X1 = 60, 1040
YT, YB = 36, 196
LW = 5


def slots(comp, a="#FFFFFF", b="#FFB400"):
    comp.slot("primary", a)
    comp.slot("accent", b)


def lines():
    comp = base("lower-third-double-line", W, H, 36)
    slots(comp)
    comp.layer("top", [rect_grow(X0, YT - LW / 2, X1 - X0, LW, 0, 0, 28, 120, 142, "left", start=0, ein=INOUT,
                                 eout=INOUT), fill(slot="primary")])
    comp.layer("bottom", [rect_grow(X0, YB - LW / 2, 620, LW, 0, 6, 32, 116, 136, "left", start=0, ein=INOUT,
                                    eout=INOUT), fill(slot="primary")])
    comp.slot("background", "#000000")
    comp.layer("backdrop", [rect_grow(X0, YT + LW, X1 - X0, YB - YT - 2 * LW, 0, 10, 34, 114, 134, "left", start=0),
                            fill(slot="background", opacity=35)])
    for i, y in enumerate((YT, YB)):
        lay(comp, f"cap{i}", [rrect(X0 - 4, y - 12, 8, 24), fill(slot="accent")], (X0, y),
            scale=grow_y(i * 4, 12 + i * 4, 136 - i * 4, 146 - i * 4))
    return comp, (X0 + 20, YT + 20, X1 - X0 - 40, 76), (X0 + 20, YT + 104, X1 - X0 - 200, 36)


def centred():
    comp = base("lower-third-double-line--centred", W, H, 36)
    slots(comp, "#FFFFFF", "#7DD3FC")
    cx = (X0 + X1) / 2
    for i, (y, w) in enumerate(((YT, 760), (YB, 460))):
        lay(comp, f"dot{i}", [ellipse((12, 12), (cx, y)), fill(slot="accent")], (cx, y),
            scale=keys((i * 4, [0, 0], SPRING), (i * 4 + 8, [100, 100], HOLD), (i * 4 + 10, [100, 100], EASE_IN),
                       (i * 4 + 16, [0, 0], HOLD), (130 + i * 2, [0, 0], EASE_OUT), (134 + i * 2, [100, 100], EASE_IN),
                       (144, [0, 0])))
        comp.layer(f"line{i}", [rect_grow(cx - w / 2, y - LW / 2, w, LW, 2, 6 + i * 4, 32 + i * 4, 116 - i * 4,
                                          134 - i * 4, "centre", start=0, ein=INOUT, eout=INOUT),
                                fill(slot="primary")])
    return comp, (cx - 380, YT + 20, 760, 76), (cx - 300, YT + 104, 600, 36)


def crossing():
    comp = base("lower-third-double-line--crossing", W, H, 38)
    slots(comp, "#FFFFFF", "#FF5470")
    L = X1 - X0
    for i, (y, side, t0, t2) in enumerate(((YT, "left", 0, 120), (YB, "right", 4, 116))):
        comp.layer(f"line{i}", [rect_grow(X0, y - LW / 2, L, LW, 0, t0, t0 + 30, t2, t2 + 22, side, start=0,
                                          ein=INOUT, eout=INOUT), fill(slot="primary")])
        start, end = (X0, X1) if side == "left" else (X1, X0)
        lay(comp, f"head{i}", [ellipse((16, 16), (0, y)), fill(slot="accent")], (0, y),
            off=keys((t0, [start, 0], INOUT), (t0 + 30, [end, 0], HOLD), (t2, [end, 0], INOUT), (t2 + 22, [start, 0])),
            scale=keys((t0, [0, 0], EASE_OUT), (t0 + 6, [100, 100], HOLD), (t2 + 16, [100, 100], EASE_IN),
                       (t2 + 22, [0, 0])))
    return comp, (X0 + 20, YT + 20, L - 40, 76), (X0 + 20, YT + 104, L - 40, 36)


a, ah, asub = lines()
b, bh, bs = centred()
c, chd, cs = crossing()
build("lower-third-double-line", "Double Line Lower Third",
      "Minimal lower third: two parallel lines draw on above and below your text. Put a name on the first row "
      "and a subtitle on the second.",
      ["lower third", "lines", "minimal", "clean", "elegant", "underline", "simple"], [
          V("lines", "Left Lines", a, ah, asub,
            description="Left-aligned lines draw from the left over a soft dark band, with accent caps and a shorter bottom line."),
          V("centred", "Centred", b, bh, bs,
            description="Centred lines grow outward from glowing dots in the middle."),
          V("crossing", "Crossing", c, chd, cs,
            description="Lines draw in opposite directions, each led by an accent dot that parks at the end."),
      ])
