from _common import *

PITCH = 250                # gap between coils
WIDTH = PITCH + 40         # stroke width (coils overlap)
R_OUT = HALF_DIAG + PITCH / 2 + 70


def spiral(r_out=R_OUT, pitch=PITCH, step=12, turn0=0):
    """Archimedean spiral from r_out (angle turn0) inward to the centre, as a smooth open path."""
    pts = []
    th = 0.0
    total = 2 * math.pi * r_out / pitch
    while th < total:
        r = r_out - pitch * th / (2 * math.pi)
        a = th + math.radians(turn0)
        pts.append((math.cos(a) * r, math.sin(a) * r))
        th += math.radians(step) * (1 if r > 300 else 0.6)
    pts.append((0, 0))
    return path(smooth_open(pts), "spiral")


def coil(comp, slot, tm, ease=SMOOTH, spin=(-120, 120), name="coil"):
    a0, a1, b0, b1 = tm
    # while the coil is complete, a disc patches the pinch where the stroke curls tighter than its width
    comp.layer(name + "-core", [group([ellipse((800, 800)), fill(slot=slot)], "core")], position=C,
               ip=a1, op=b0 + 1)
    comp.layer(name, [group([spiral(), stroke(slot=slot, width=WIDTH, cap="round"),
                             trim(end=anim([(a0, 0, ease), (a1, 100)]), start=anim([(b0, 0, ease), (b1, 100)]))],
                            "spiral")],
               position=C, rotation=io(tm, spin[0], 0, spin[1], ease))


def flat():
    t = Timing(16, 10, 16)
    comp = base("swirl-spiral", t, {"primary": "#FF4F8B"})
    coil(comp, "primary", t.tm)
    return comp, t


def layered():
    t = Timing(17, 8, 17)
    comp = base("swirl-spiral--layered", t, "ocean", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        coil(comp, s, tm, name=s)
    return comp, t


def blade_shape(base_a, width, twist, R=1600, n=14):
    """Curved blade from the centre out: its edges bend by `twist` degrees at the rim."""
    left, right = [], []
    for i in range(n + 1):
        r = R * i / n
        a = base_a + twist * (r / R) ** 0.8
        left.append((math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r))
        b = a + width
        right.append((math.cos(math.radians(b)) * r, math.sin(math.radians(b)) * r))
    return bezier(left + right[::-1][:-1], closed=True)


def vortex():
    """Curved blades twist in from the rim, widen until they close up, then twist away."""
    t = Timing(13, 8, 13)
    comp = base("swirl-spiral--vortex", t, "violet", ("primary", "secondary"))
    a0, a1, b0, b1 = t.tm
    N = 8
    full = 360 / N + 1.5

    def blade_anim(i, off):
        keys = []
        for f in list(range(a0, a1, 2)) + [a1]:
            u = ease_at(SNAPPY, (f - a0) / (a1 - a0))
            keys.append((f, blade_shape(i * 360 / N + off - 60 * (1 - u), full * u, 150 - 90 * u), LINEAR))
        for f in list(range(b0, b1, 2)) + [b1]:
            u = ease_at(SNAPPY, (f - b0) / (b1 - b0))
            keys.append((f, blade_shape(i * 360 / N + off + full * u + 60 * u, full * (1 - u), 60 + 90 * u), LINEAR))
        return Anim(keys)

    for slot, off, lagf in (("primary", 0, 0), ("secondary", 360 / N / 2, 1)):
        blades = [path(blade_anim(i, off), f"blade{i}") for i in range(N)]
        comp.layer(slot, [group(blades + [fill(slot=slot)], "blades")], position=C)
    return comp, t


VARIANTS = [
    ("spiral", "Spiral Coil", flat, "A fat spiral coils in from the rim while turning until the frame is filled, then "
                                    "unwinds into the centre."),
    ("layered", "Layered Coils", layered, "Accent, secondary and primary spirals coil in one after another and "
                                          "unwind in reverse."),
    ("vortex", "Vortex Blades", vortex, "Two sets of curved blades twist in and widen into a vortex, then twist away."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"spiral": 0.7, "layered": 0.6, "vortex": 0.42}

build("swirl-spiral", "Swirl Spiral",
      "Spiral transition: a swirl coils in to cover the shot, holds for the cut, then unwinds to reveal the next "
      "clip.",
      ["swirl", "spiral", "twist", "vortex", "transition", "hypnotic"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
