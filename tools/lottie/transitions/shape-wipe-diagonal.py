from _common import *

ANGLE = 22  # tilt of the wipe edge from vertical, degrees
DIR = (math.cos(math.radians(ANGLE)), math.sin(math.radians(ANGLE)))
REACH = CX * DIR[0] + CY * DIR[1]  # canvas half-extent along the travel direction


def slab(comp, slot, tm, width=2 * REACH + 80, ease=SMOOTH, name="slab"):
    """Tilted slab that slides across along its normal: covers at the hold, exits the far side."""
    d = width / 2 + REACH + 40
    start = [CX - DIR[0] * d, CY - DIR[1] * d]
    end = [CX + DIR[0] * d, CY + DIR[1] * d]
    comp.layer(name, [group([rect((width, 5200)), fill(slot=slot)], "slab", rotation=ANGLE)],
               position=io(tm, start, [CX, CY], end, ease))


def chevron(comp, slot, tm, body, point=460, height=1500, ease=SNAPPY, name="chevron", outline=None):
    """Arrow-shaped slab pointing right: pointed nose, notched tail."""
    L, P, Y = body, point, height / 2
    pts = [(-L / 2, -Y), (L / 2, -Y), (L / 2 + P, 0), (L / 2, Y), (-L / 2, Y), (-L / 2 + P, 0)]
    items = [poly(pts), fill(slot=slot)]
    if outline:
        items.insert(1, stroke(slot=outline, width=26, join="miter"))
    d = L / 2 + P + CX + 60
    comp.layer(name, [group(items, "shape")], position=io(tm, [CX - d, CY], [CX, CY], [CX + d, CY], ease))


def flat():
    t = Timing()
    comp = base("shape-wipe-diagonal", t, "violet")
    slab(comp, "primary", t.tm)
    return comp, t


def stacked():
    t = Timing(15, 10, 15)
    comp = base("shape-wipe-diagonal--stacked", t, "violet", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        slab(comp, s, tm, name=s)
    return comp, t


def arrow():
    t = Timing.snappy()
    comp = base("shape-wipe-diagonal--arrow", t, "violet", ("primary", "accent"))
    # a thin accent chevron leads the big one in and trails it out
    a0, a1, b0, b1 = t.tm
    L = W + 2 * 460 + 200
    chevron(comp, "primary", (a0 + 2, a1, b0, b1 - 2), L, outline="accent")
    chevron(comp, "accent", (a0, a1 - 2, b0 + 2, b1), L + 120, name="accent-chevron")
    return comp, t


VARIANTS = [
    ("flat", "Flat Slab", flat, "One solid slab slides across at a tilt, holds, then carries on off the far side."),
    ("stacked", "Stacked Colours", stacked, "Three tilted slabs in accent, secondary and primary follow each other in "
                                           "and peel away in reverse."),
    ("arrow", "Arrow", arrow, "Snappy arrow-shaped chevron with an accent rim and a trailing accent echo."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"flat": 0.5, "stacked": 0.5, "arrow": 0.6}

build("shape-wipe-diagonal", "Shape Wipe Diagonal",
      "Full-frame diagonal wipe: a tilted slab slides across to cover the shot, holds for the cut and "
      "slides off to reveal the next clip.",
      ["wipe", "diagonal", "slide", "transition", "cover", "swipe"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
