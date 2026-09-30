from _common import *

TILT = 20  # slashes lean this far from vertical
U_REACH = CX * math.cos(math.radians(TILT)) + CY * math.sin(math.radians(TILT))
V_REACH = CX * math.sin(math.radians(TILT)) + CY * math.cos(math.radians(TILT))
BANDS = 3
BW = 2 * U_REACH / BANDS + 70
BL = 2 * V_REACH + 120


def bands(comp, slot, tm, lag=2, ease=SNAPPY, name="band"):
    """Three leaning bands slashing in alternately from the top and the bottom."""
    a0, a1, b0, b1 = tm
    for i in range(BANDS):
        u = lerp(-(U_REACH - BW / 2 + 30), U_REACH - BW / 2 + 30, i / (BANDS - 1))
        sgn = -1 if i % 2 == 0 else 1
        d = BL + 60
        # stagger inside the layer's own window: outer bands first in, first out
        o = (0, 2, 1)[i] * lag
        t = (a0 + o, a1 - (2 * lag - o), b0 + o, b1 - (2 * lag - o))
        comp.layer(f"{name}-{i}", [group([rect((BW, BL)), fill(slot=slot)], "band",
                                         position=io(t, [u, sgn * d], [u, 0], [u, -sgn * d], ease))],
                   position=C, rotation=TILT)


def flat():
    t = Timing(12, 10, 12)
    comp = base("slash-cut", t, "sunset")
    bands(comp, "primary", t.tm)
    return comp, t


def layered():
    t = Timing(15, 10, 15)
    comp = base("slash-cut--layered", t, "sunset", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        bands(comp, s, tm, lag=2, name=s)
    return comp, t


ANG = -28  # blade seam angle
SV = CX * abs(math.sin(math.radians(ANG))) + CY * math.cos(math.radians(ANG))  # frame extent across the seam


def blade():
    """A thin accent slash zips across, the two halves slam shut along it, then split apart."""
    t = Timing(14, 10, 12)
    comp = base("slash-cut--blade", t, "sunset", ("primary", "secondary", "accent"))
    a0, a1, b0, b1 = t.tm
    L = 4400
    seam_t = (a0, a0 + 6, b0 + 2, b1 - 4)
    comp.layer("seam", [group([rect((L, 14)), fill(slot="accent")], "line", anchor=(-L / 2, 0), position=(-L / 2, 0),
                              scale=io(seam_t, [0, 100], [100, 100], [100, 0], DECEL, ACCEL))],
               position=C, rotation=ANG)
    ph = SV + 60
    for i, (slot, sgn) in enumerate((("primary", -1), ("secondary", 1))):
        far = [0, sgn * (ph / 2 + SV + 40)]
        near = [0, sgn * ph / 2]
        comp.layer(f"half-{i}", [group([rect((L, ph)), fill(slot=slot)], "half",
                                       position=io((a0 + 4, a1, b0 + 2, b1), far, near, far, SNAPPY))],
                   position=C, rotation=ANG)
    return comp, t


VARIANTS = [
    ("flat", "Flat Slashes", flat, "Three leaning bands slash in from the top and bottom in turn and carry on through."),
    ("layered", "Layered Slashes", layered, "Accent, secondary and primary slashes follow each other in and peel away "
                                            "in reverse."),
    ("blade", "Blade Split", blade, "A thin accent blade line zips across, two halves slam shut along it, then the "
                                    "frame splits open."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"flat": 0.6, "layered": 0.6, "blade": 0.65}

build("slash-cut", "Slash Cut",
      "Sharp slash transition: leaning bands cut across the shot to cover it, hold for the cut, then slice away "
      "to reveal the next clip.",
      ["slash", "cut", "diagonal", "transition", "sharp", "action"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
