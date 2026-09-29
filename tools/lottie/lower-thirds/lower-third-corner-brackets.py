from _lt2 import *

W, H = 1100, 250
X0, Y0, X1, Y1 = 80, 40, 1020, 210
CX, CY = (X0 + X1) / 2, (Y0 + Y1) / 2
CORNERS = [(X0, Y0, 1, 1), (X1, Y0, -1, 1), (X1, Y1, -1, -1), (X0, Y1, 1, -1)]


def corner(x, y, sx, sy, arm, name="corner"):
    return poly([(x, y + sy * arm), (x, y), (x + sx * arm, y)], False, name)


def expand():
    comp = base("lower-third-corner-brackets", W, H, 34)
    comp.slot("outline", "#FFFFFF")
    comp.slot("background", "#000000")
    comp.slot("accent", "#FFD23F")
    lay(comp, "rule", [rrect(X0 + 50, CY + 22, 240, 3), fill(slot="accent")], (X0 + 50, 0),
        scale=grow_x(20, 38, 114, 126))
    for i, (x, y, sx, sy) in enumerate(CORNERS):
        dx, dy = (CX - x) * 0.92, (CY - y) * 0.6
        lay(comp, f"c{i}", [corner(x, y, sx, sy, 46), stroke(slot="outline", width=6, cap="square", join="miter")],
            off=keys((0, [dx, dy], (0.2, 0, 0.1, 1)), (26, [0, 0], HOLD), (122, [0, 0], (0.7, 0, 0.9, 0.6)),
                     (142, [dx, dy])),
            opacity=keys((0, 0, EASE_OUT), (4, 100, HOLD), (138, 100, EASE_IN), (142, 0)))
    lay(comp, "backdrop", [rrect(X0, Y0, X1 - X0, Y1 - Y0), fill(slot="background", opacity=40)],
        (CX, CY), scale=grow(8, 30, 118, 138, (0.2, 0, 0.1, 1), (0.7, 0, 0.9, 0.6)))
    return comp, (X0 + 50, Y0 + 26, X1 - X0 - 100, 70), (X0 + 50, CY + 34, X1 - X0 - 100, 34)


def draw_corners():
    comp = base("lower-third-corner-brackets--draw", W, H, 40)
    comp.slot("outline", "#7DF9FF")
    comp.slot("primary", "#7DF9FF")
    for i, (x, y, sx, sy) in enumerate(CORNERS):
        t0 = 2 + i * 3
        # two arms from the corner outward so it draws from the corner point
        arms = [poly([(x, y), (x + sx * 120, y)], False, "h"), poly([(x, y), (x, y + sy * 60)], False, "v")]
        comp.layer(f"c{i}", arms + [trim(end=keys((t0, 0, EXPO_OUT), (t0 + 22, 100, HOLD), (118 + i * 2, 100, INOUT),
                                                   (136 + i * 2, 0))),
                                    stroke(slot="outline", width=5, cap="butt")])
        lay(comp, f"dot{i}", [rect((12, 12), (x, y)), fill(slot="outline")], (x, y),
            scale=pop(t0, t0 + 10, 126 + i * 2, 136 + i * 2), rotation=45)
    comp.layer("fill", [rrect(X0 + 12, Y0 + 12, X1 - X0 - 24, Y1 - Y0 - 24), fill(slot="primary", opacity=12)],
               opacity=keys((0, 0, HOLD), (18, 0, EASE_OUT), (34, 100, HOLD), (116, 100, EASE_IN), (128, 0)))
    return comp, (X0 + 50, Y0 + 26, X1 - X0 - 100, 70), (X0 + 50, CY + 30, X1 - X0 - 100, 34)


def two_corner():
    comp = base("lower-third-corner-brackets--two-corner", W, H, 32)
    comp.slot("accent", "#FF4D4D")
    comp.slot("outline", "#FFFFFF")
    x0, y0, x1, y1 = 70, 44, 900, 206
    for i, (x, y, sx, sy, dx, dy) in enumerate(((x0, y0, 1, 1, -60, -40), (x1, y1, -1, -1, 60, 40))):
        lay(comp, f"c{i}", [corner(x, y, sx, sy, 70), stroke(slot="accent", width=12, cap="square", join="miter")],
            off=slide(dx, dy, 2 * i, 24 + 2 * i, 122 - 2 * i, 138 - 2 * i, SPRING, BACK_IN),
            opacity=fade(2 * i, 6 + 2 * i, 134, 138))
    lay(comp, "divider", [rrect(x0 + 44, (y0 + y1) / 2 + 12, 300, 2), fill(slot="outline", opacity=80)],
        (x0 + 44, 0), scale=grow_x(14, 34, 116, 128))
    return comp, (x0 + 44, y0 + 26, x1 - x0 - 88, 64), (x0 + 44, (y0 + y1) / 2 + 24, x1 - x0 - 120, 34)


a, ah, asub = expand()
b, bh, bs = draw_corners()
c, chd, cs = two_corner()
build("lower-third-corner-brackets", "Corner Brackets Lower Third",
      "Minimal lower third: corner brackets frame your text. Put a name on the first row and a subtitle on "
      "the second.",
      ["lower third", "corner", "brackets", "frame", "minimal", "clean", "viewfinder"], [
          V("expand", "Expand", a, ah, asub,
            description="Four corners burst out from the centre over a subtle dark backdrop, with an accent rule."),
          V("draw", "Draw Corners", b, bh, bs,
            description="Long corner arms draw out from each corner in turn with a faint tinted fill."),
          V("two-corner", "Two Corners", c, chd, cs,
            description="Bold top-left and bottom-right brackets spring in diagonally around left-aligned text."),
      ])
