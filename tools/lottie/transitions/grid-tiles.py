from _common import *

CELL = 240
COLS, ROWS = 8, 5
Y0 = (H - ROWS * CELL) / 2  # rows overhang top and bottom evenly


def cells():
    for c in range(COLS):
        for r in range(ROWS):
            yield c, r, ((c + 0.5) * CELL, Y0 + (r + 0.5) * CELL)


def tiles(comp, slot, tm, order, dur=7, shape="square", flip=False, ease=SMOOTH, spin=90, name="tiles"):
    """Grid tiles that grow in by `order` (0..1 per cell) and shrink out in the same order."""
    a0, a1, b0, b1 = tm
    groups = []
    for c, r, p in cells():
        u = order(c, r)
        ti = a0 + u * (a1 - a0 - dur)
        to = b0 + u * (b1 - b0 - dur)
        s_in = [0, 100] if flip else [0, 0]
        s_out = [100, 0] if flip else [0, 0]
        sc = Anim([(ti, s_in, ease), (ti + dur, [100, 100], LINEAR), (to, [100, 100], ease), (to + dur, s_out)])
        rt = 0 if flip else Anim([(ti, -spin, ease), (ti + dur, 0, LINEAR), (to, 0, ease), (to + dur, spin)])
        if shape == "square":
            item = rect((CELL + 14, CELL + 14))
        else:
            d = CELL * math.sqrt(2) + 12
            item = ellipse((d, d))
        groups.append(group([item, fill(slot=slot)], f"t{c}-{r}", position=p, scale=sc, rotation=rt))
    comp.layer(name, groups)


def diag(c, r):
    return (c + r) / (COLS + ROWS - 2)


def centre_out(c, r):
    d = math.hypot((c + 0.5) * CELL - CX, Y0 + (r + 0.5) * CELL - CY)
    return d / math.hypot(CX - CELL / 2, CY - Y0 - CELL / 2)


def squares():
    t = Timing(16, 10, 16)
    comp = base("grid-tiles", t, {"primary": "#12B8A6"})
    tiles(comp, "primary", t.tm, diag)
    return comp, t


def flip():
    t = Timing(16, 10, 16)
    comp = base("grid-tiles--flip", t, "mint", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=2):
        tiles(comp, s, tm, lambda c, r: 1 - diag(c, r), dur=6, flip=True, name=s)
    return comp, t


def dots():
    t = Timing(12, 8, 12)
    comp = base("grid-tiles--dots", t, {"primary": "#12B8A6", "accent": "#F7D35C"}, ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    tiles(comp, "primary", (a0 + 2, a1, b0, b1 - 2), centre_out, dur=6, shape="dot", ease=BACK, spin=0,
          name="dots")
    tiles(comp, "accent", (a0, a1 - 2, b0 + 2, b1), centre_out, dur=6, shape="dot", ease=BACK, spin=0,
          name="dots-under")
    return comp, t


VARIANTS = [
    ("squares", "Square Ripple", squares, "Square tiles spin and grow in a diagonal wave until the grid closes, then "
                                          "shrink away in the same direction."),
    ("flip", "Colour Flip", flip, "Tiles flip over in a diagonal wave, in accent, secondary then primary layers."),
    ("dots", "Dot Pop", dots, "Round dots pop out from the centre with a springy overshoot, an accent dot leading "
                              "each one."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"squares": 0.5, "flip": 0.55, "dots": 0.35}

build("grid-tiles", "Grid Tiles",
      "Tile grid transition: tiles pop in across the frame to cover the shot, hold for the cut, then pop away to "
      "reveal the next clip.",
      ["grid", "tiles", "squares", "mosaic", "transition", "geometric"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
