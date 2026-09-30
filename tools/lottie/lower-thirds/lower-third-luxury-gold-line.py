from _lt2 import *

GOLD_OUT = [(0, "#8A6A1F", 0.0), (0.35, "#B8902F"), (0.7, "#F9E79F"), (0.88, "#D4AF37"), (1, "#FFF6CF")]
GOLD = [(0, "#9C7A28"), (0.3, "#F4DC8A"), (0.55, "#C9A13B"), (0.8, "#FFF1B8"), (1, "#A8822C")]


def gold_line(comp, name, xa, xb, y, t0, t1, t2, t3, h=4, grad=GOLD_OUT):
    """Line from xa (anchored, drawn first) toward xb; gradient fades out toward xb."""
    x, w = min(xa, xb), abs(xb - xa)
    side = "left" if xa < xb else "right"
    comp.layer(name, [rect_grow(x, y - h / 2, w, h, 0, t0, t1, t2, t3, side, start=0, ein=INOUT, eout=INOUT),
                      gradient_fill(grad, (xb, y), (xa, y))])


def gem(comp, name, cx, cy, r, t0, t1, t2, t3, spin=True):
    shapes = [group([diamond(cx, cy, r * 0.55), gradient_fill(GOLD, (cx - r, cy - r), (cx + r, cy + r))], "core"),
              group([diamond(cx, cy, r), stroke(slot="accent", width=2.5, join="miter")], "ring")]
    lay(comp, name, shapes, (cx, cy), scale=pop(t0, t1, t2, t3, ein=OVERSHOOT),
        rotation=keys((t0, -180 if spin else 0, EXPO_OUT), (t1, 0, HOLD), (t2, 0, EXPO_IN), (t3, 90)))


def centre():
    W, H = 1200, 250
    cx = W / 2
    comp = base("lower-third-luxury-gold-line", W, H, 40)
    comp.slot("accent", "#E8C66A")
    gem(comp, "gem", cx, 44, 20, 0, 16, 130, 146)
    gold_line(comp, "top-l", cx - 32, cx - 420, 44, 8, 34, 120, 138)
    gold_line(comp, "top-r", cx + 32, cx + 420, 44, 8, 34, 120, 138)
    gold_line(comp, "bot-l", cx, cx - 170, 212, 18, 40, 116, 132, h=3)
    gold_line(comp, "bot-r", cx, cx + 170, 212, 18, 40, 116, 132, h=3)
    for i, x in enumerate((cx - 180, cx + 180)):
        lay(comp, f"dot{i}", [diamond(x, 212, 7), fill(slot="accent")], (x, 212), scale=pop(34, 44, 114, 124))
    return comp, (cx - 400, 70, 800, 74), (cx - 300, 152, 600, 40)


def framed():
    W, H = 1100, 250
    x0, x1, ya, yb = 70, 1030, 40, 210
    comp = base("lower-third-luxury-gold-line--framed", W, H, 44)
    comp.slot("accent", "#E8C66A")
    comp.slot("background", "#0E0B06")
    gem(comp, "gem-r", x1 + 14, ya, 12, 22, 36, 124, 138)
    gem(comp, "gem-l", x0 - 14, yb, 12, 26, 40, 120, 134)
    gold_line(comp, "top", x0 - 14, x1 + 4, ya, 0, 28, 120, 140, grad=GOLD)
    gold_line(comp, "bottom", x1 + 14, x0 - 4, yb, 4, 32, 118, 138, grad=GOLD)
    lay(comp, "backdrop", [rrect(x0, ya + 4, x1 - x0, yb - ya - 8), fill(slot="background", opacity=62)],
        opacity=fade(16, 36, 114, 132))
    return comp, (x0 + 60, ya + 24, x1 - x0 - 120, 72), (x0 + 120, ya + 104, x1 - x0 - 240, 42)


def left():
    W, H = 1100, 230
    gx, gy = 70, 146
    comp = base("lower-third-luxury-gold-line--left", W, H, 40)
    comp.slot("accent", "#E8C66A")
    gem(comp, "gem", gx, gy, 18, 0, 18, 128, 144)
    gold_line(comp, "line", gx + 30, 980, gy, 10, 38, 118, 138)
    gold_line(comp, "stub", gx - 30, 20, gy, 12, 30, 124, 136, h=3)
    return comp, (gx + 20, 50, 880, 78), (gx + 40, gy + 18, 700, 38)


a, ah, asub = centre()
b, bh, bs = framed()
c, chd, cs = left()
build("lower-third-luxury-gold-line", "Luxury Gold Line Lower Third",
      "Elegant lower third of thin gold-gradient lines drawing out from a faceted diamond. Put a name or title "
      "on the headline row and a subtitle beneath it.",
      ["lower third", "gold", "luxury", "elegant", "wedding", "premium", "minimal"], [
          V("centre", "Centred Lines", a, ah, asub,
            description="Centred: a diamond spins in and gold lines draw outward above and below the text."),
          V("framed", "Framed Band", b, bh, bs,
            description="Lines sweep across in opposite directions with gems on the ends and a dark band between."),
          V("left", "Left Underline", c, chd, cs,
            description="Left-aligned: a diamond at the start and one long gold line under the headline."),
      ])
