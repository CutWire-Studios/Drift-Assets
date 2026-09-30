from _common import *

FULL = 2 * HALF_DIAG + 60  # a centred circle this wide covers the corners


def sz(v):
    return [v, v]


def disc(comp, slot, tm, ease=SMOOTH, name="disc", center=C):
    """Circle grows from nothing to cover the frame, then a hole grows from the middle to reveal."""
    a0, a1, b0, b1 = tm
    comp.layer(name + "-in", [group([ellipse(anim([(a0, sz(0), ease), (a1, sz(FULL))])), fill(slot=slot)], "disc")],
               position=center, op=b0 + 1)
    comp.layer(name + "-out", [hole_group([ellipse(anim([(b0, sz(0), ease), (b1, sz(FULL + 200))]))], slot)],
               position=center, ip=b0)


def iris(comp, slot, tm, ring=None, ease=SNAPPY, center=C):
    """Classic iris: a sheet with a round hole that closes to a point, then reopens."""
    a0, a1, b0, b1 = tm
    far = 2 * math.hypot(max(center[0], W - center[0]), max(center[1], H - center[1])) + 80
    hole = io(tm, sz(far), sz(0), sz(far), ease)
    if ring:
        comp.layer("ring", [group([ellipse(hole), stroke(slot=ring, width=io(tm, 44, 0, 44, ease))], "ring")],
                   position=center)
    comp.layer("iris", [hole_group([ellipse(hole)], slot)], position=center)


def bloom():
    t = Timing()
    comp = base("circle-iris", t, "ocean")
    disc(comp, "primary", t.tm)
    return comp, t


def rings():
    t = Timing(15, 10, 15)
    comp = base("circle-iris--rings", t, "ocean", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        disc(comp, s, tm, name=s)
    return comp, t


def classic():
    t = Timing.snappy()
    comp = base("circle-iris--iris", t, "ocean", ("primary", "accent"))
    iris(comp, "primary", t.tm, ring="accent")
    return comp, t


VARIANTS = [
    ("bloom", "Bloom", bloom, "A circle blooms out of the centre to fill the frame, then a round hole opens from the "
                              "middle to reveal the next shot."),
    ("rings", "Stacked Rings", rings, "Three coloured circles bloom one after another, then open in reverse like "
                                      "ripples."),
    ("iris", "Classic Iris", classic, "Old-film iris: the frame closes to a point behind an accent rim and snaps back "
                                      "open."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"bloom": 0.5, "rings": 0.5, "iris": 0.55}

build("circle-iris", "Circle Iris",
      "Round iris transition: a circle closes over the shot, holds on a solid frame for the cut, then opens "
      "onto the next clip.",
      ["iris", "circle", "round", "transition", "reveal", "zoom"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
