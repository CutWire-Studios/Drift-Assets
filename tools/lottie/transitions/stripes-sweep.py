from _common import *


def stripes(comp, slot, tm, count, angle=0, dur=None, lag_order=None, alternate=True, round_ends=False,
            ease=SMOOTH, name="stripes"):
    """`count` parallel stripes (rotated by `angle`) sliding in along their length, staggered.

    In the rotated frame the stripes run along x; `angle` 0 = horizontal stripes.
    """
    a0, a1, b0, b1 = tm
    a = math.radians(angle)
    across = abs(CX * math.sin(a)) + abs(CY * math.cos(a))  # frame half-extent across the stripes
    along = abs(CX * math.cos(a)) + abs(CY * math.sin(a))   # frame half-extent along them
    sh = 2 * across / count
    length = 2 * along + 120 + (sh if round_ends else 0)
    dur = dur or (a1 - a0) * 0.6
    groups = []
    for i in range(count):
        v = -across + (i + 0.5) * sh
        u = (lag_order(i) if lag_order else i / max(count - 1, 1))
        ti = a0 + u * (a1 - a0 - dur)
        to = b0 + u * (b1 - b0 - dur)
        sgn = -1 if (alternate and i % 2) else 1
        far = length + 40
        pos = Anim([(ti, [-sgn * far, v], ease), (ti + dur, [0, v], LINEAR), (to, [0, v], ease),
                    (to + dur, [sgn * far, v])])
        groups.append(group([rect((length, sh + 12), roundness=(sh / 2 if round_ends else 0)), fill(slot=slot)],
                            f"s{i}", position=pos))
    comp.layer(name, [group(groups, "set", rotation=angle)], position=C)


def horizontal():
    t = Timing(15, 10, 15)
    comp = base("stripes-sweep", t, "ocean", ("primary",))
    stripes(comp, "primary", t.tm, 6)
    return comp, t


def vertical():
    t = Timing(16, 10, 16)
    comp = base("stripes-sweep--tricolor", t, "sunset", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        stripes(comp, s, tm, 8, angle=90, alternate=False, dur=8, name=s)
    return comp, t


def capsules():
    t = Timing(13, 8, 13)
    comp = base("stripes-sweep--capsules", t, "violet", ("primary", "secondary"))
    a0, a1, b0, b1 = t.tm
    mid = lambda i: abs(i - 3.5) / 3.5  # centre stripes first
    stripes(comp, "primary", (a0 + 2, a1, b0, b1 - 2), 8, angle=-35, dur=7, lag_order=mid, round_ends=True,
            ease=SNAPPY, name="primary")
    stripes(comp, "secondary", (a0, a1 - 2, b0 + 2, b1), 8, angle=-35, dur=7, lag_order=mid, round_ends=True,
            ease=SNAPPY, name="secondary")
    return comp, t


VARIANTS = [
    ("horizontal", "Horizontal", horizontal, "Six horizontal stripes slide in from alternating sides, top to "
                                             "bottom, and carry on out."),
    ("tricolor", "Tri-Colour Drop", vertical, "Vertical stripes drop from the top in three colour passes, left to "
                                              "right."),
    ("capsules", "Diagonal Capsules", capsules, "Round-ended diagonal capsules whip in from the centre outwards "
                                                "with a secondary echo."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"horizontal": 0.52, "tricolor": 0.55, "capsules": 0.45}

build("stripes-sweep", "Stripes Sweep",
      "Striped wipe transition: bands slide in one after another to cover the shot, hold for the cut, then slide "
      "on out to reveal the next clip.",
      ["stripes", "bands", "sweep", "wipe", "transition", "slide"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
