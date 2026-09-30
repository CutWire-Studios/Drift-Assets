from _common import *

OVER = 40  # doors overlap at the seam by this much each


def doors(comp, slot, tm, vertical=False, ein=BACK, eout=SMOOTH, name="door"):
    """Two doors slide in from opposite edges, meet in the middle, then slide back out."""
    a0, a1, b0, b1 = tm
    for k, sgn in enumerate((-1, 1)):
        if vertical:
            size = (W + 200, CY + OVER + 100)
            home = [CX, CY + sgn * (size[1] / 2 - OVER)]
            away = [CX, CY + sgn * (size[1] / 2 + CY + 40)]
        else:
            size = (CX + OVER + 100, H + 200)
            home = [CX + sgn * (size[0] / 2 - OVER), CY]
            away = [CX + sgn * (size[0] / 2 + CX + 40), CY]
        comp.layer(f"{name}-{k}", [group([rect(size), fill(slot=slot)], "door")],
                   position=io(tm, away, home, away, ein, eout))


def sliding():
    t = Timing(14, 10, 14)
    comp = base("split-doors", t, "night", ("primary",))
    doors(comp, "primary", t.tm)
    return comp, t


def vertical():
    t = Timing(16, 10, 16)
    comp = base("split-doors--vertical", t, "sunset", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        doors(comp, s, tm, vertical=True, ein=SMOOTH, name=s)
    return comp, t


def shutter():
    """Four corner panels with accent outlines snap into the middle like a camera shutter."""
    t = Timing.snappy()
    comp = base("split-doors--shutter", t, "mint", ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    qw, qh = CX + OVER + 80, CY + OVER + 80
    for k, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))):
        home = [CX + sx * (qw / 2 - OVER), CY + sy * (qh / 2 - OVER)]
        away = [CX + sx * (qw / 2 + CX + 60), CY + sy * (qh / 2 + CY + 60)]
        d = k % 2  # alternate panels lead by a frame
        tm = (a0 + d, a1 - 1 + d, b0 + d, b1 - 1 + d)
        comp.layer(f"panel-{k}", [group([rect((qw, qh)), stroke(slot="accent", width=io(tm, 22, 0, 22, SNAPPY)),
                                         fill(slot="primary")], "panel")],
                   position=io(tm, away, home, away, SNAPPY))
    return comp, t


VARIANTS = [
    ("sliding", "Sliding Doors", sliding, "Two doors slide in from the sides, meet in the middle with a little bounce, "
                                          "then slide back open.", {"bg": "e8e8ee"}),
    ("vertical", "Stacked Vertical", vertical, "Top and bottom doors close in three colour layers and open in "
                                               "reverse."),
    ("shutter", "Four-Way Shutter", shutter, "Four corner panels with accent outlines snap into the centre like a "
                                             "camera shutter.", {"bg": "e8e8ee"}),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"sliding": 0.4, "vertical": 0.55, "shutter": 0.55}

build("split-doors", "Split Doors",
      "Door transition: panels slide in from the edges and meet in the middle to cover the shot, hold for the cut, "
      "then slide open onto the next clip.",
      ["doors", "split", "slide", "shutter", "transition", "open"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
