from _common import *

R = 2600  # ray length: well past the corners


def pol(a, r=R):
    a = math.radians(a)
    return (math.cos(a) * r, math.sin(a) * r)


def wedge_anim(tm, base, full, ease, spin):
    """Wedge whose leading edge opens to `full` degrees, then whose trailing edge closes it off."""
    a0, a1, b0, b1 = tm
    keys = []
    for f in range(a0, a1 + 1):
        u = ease_at(ease, (f - a0) / (a1 - a0))
        s = base + spin * (1 - u)
        keys.append((f, bezier([(0, 0), pol(s), pol(s + full * u)], closed=True), LINEAR))
    for f in range(b0, b1 + 1):
        u = ease_at(ease, (f - b0) / (b1 - b0))
        s = base - spin * u
        keys.append((f, bezier([(0, 0), pol(s + full * u), pol(s + full)], closed=True), LINEAR))
    return Anim(keys)


def rays(comp, slot, tm, count=16, ease=SMOOTH, spin=25, offset=0, name="rays"):
    step = 360 / count
    shapes = [path(wedge_anim(tm, offset + i * step, step + 1.2, ease, spin), f"ray{i}") for i in range(count)]
    comp.layer(name, [group(shapes + [fill(slot=slot)], "rays")], position=C)


def flat():
    t = Timing(14, 10, 14)
    comp = base("zoom-burst-lines", t, "sunset", ("primary",))
    rays(comp, "primary", t.tm)
    return comp, t


def stacked():
    t = Timing(16, 10, 16)
    comp = base("zoom-burst-lines--stacked", t, "sunset", ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        rays(comp, s, tm, count=12, offset=i * 10, name=s)
    return comp, t


def star_path(spikes, r_out, r_in, rot, seed):
    r = random.Random(seed)
    pts = []
    for i in range(spikes * 2):
        a = rot + 180 * i / spikes
        rr = r_out * r.uniform(0.82, 1.12) if i % 2 == 0 else r_in
        pts.append(pol(a, rr))
    return pts


def starburst():
    """A spiky comic burst zooms out of the centre and spins; a burst-shaped hole blows it open."""
    t = Timing.snappy()
    comp = base("zoom-burst-lines--starburst", t, "sunset", ("primary", "secondary", "accent"))
    a0, a1, b0, b1 = t.tm
    inner = HALF_DIAG + 80  # the burst's valleys alone reach the corners
    burst = bezier(star_path(22, inner * 1.45, inner, 0, 3), closed=True)
    comp.layer("burst", [group([path(burst), fill(slot="primary")], "burst", scale=anim(
        [(a0 + 2, [0, 0], SNAPPY), (a1, [100, 100])]), rotation=anim([(a0 + 2, -40, SNAPPY), (a1, 0)]))],
        position=C, op=b0 + 1)
    comp.layer("burst-2", [group([path(burst), fill(slot="secondary")], "burst", scale=anim(
        [(a0 + 1, [0, 0], SNAPPY), (a1 - 1, [100, 100])]), rotation=anim([(a0 + 1, -50, SNAPPY), (a1 - 1, 5)]))],
        position=C, op=a1 + 1)
    comp.layer("burst-3", [group([path(burst), fill(slot="accent")], "burst", scale=anim(
        [(a0, [0, 0], SNAPPY), (a1 - 2, [100, 100])]), rotation=anim([(a0, -60, SNAPPY), (a1 - 2, 10)]))],
        position=C, op=a1 + 1)
    hole = bezier(star_path(22, inner * 1.45, inner, 8, 9), closed=True)
    zc = zoom_curve(GENTLE, 4.0)  # even zoom rate for the hole
    comp.layer("burst-out", [group([rect((8000, 8000)), group([path(hole)], "hole", scale=Anim(
        [(f, [115 * zc((f - b0) / (b1 - b0))] * 2, LINEAR) for f in range(b0, b1 + 1)]),
        rotation=anim([(b0, 0, SNAPPY), (b1, 40)])),
        fill(slot="primary", even_odd=True)], "sheet")], position=C, ip=b0)
    return comp, t


VARIANTS = [
    ("rays", "Sun Rays", flat, "Sixteen rays fan open while turning until they close up the frame, then sweep "
                               "shut to reveal."),
    ("stacked", "Stacked Rays", stacked, "Three offset sets of rays in accent, secondary and primary fan in one "
                                         "after another."),
    ("starburst", "Starburst", starburst, "A spiky comic starburst zooms out of the centre in three colours, then a "
                                          "burst-shaped hole blows it open."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"rays": 0.5, "stacked": 0.5, "starburst": 0.4}

build("zoom-burst-lines", "Zoom Burst Lines",
      "Radial burst transition: rays fan out from the centre to cover the shot, hold for the cut, then sweep away "
      "to reveal the next clip.",
      ["burst", "rays", "zoom", "radial", "transition", "comic"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
