from _common import *


def streak_shape(L, h, taper):
    if taper:
        T = taper
        return path(bezier([(-L / 2, 0), (-L / 2 + T, -h / 2), (L / 2 - T, -h / 2), (L / 2, 0),
                            (L / 2 - T, h / 2), (-L / 2 + T, h / 2)], closed=True), "streak")
    return rect((L, h), roundness=h / 2)


def streaks(comp, slot, tm, seed, taper=0, ein=ACCEL, eout=DECEL, spread=5, flecks=10, name="streaks"):
    """Rows of speed streaks whoosh in from the left with ragged fronts, then whoosh off to the right."""
    a0, a1, b0, b1 = tm
    r = random.Random(seed)
    groups = []
    y = -30
    while y < H + 30:
        h = r.uniform(34, 120)
        off = r.uniform(-250, 250)
        tip = taper or h / 2
        L = W + 2 * tip + 2 * abs(off) + 120
        cy = y + h / 2
        ti = a0 + r.uniform(0, spread)
        to = b0 + r.uniform(0, spread)
        pos = Anim([(ti, [-L / 2 - 60, cy], ein), (a1, [CX + off, cy], LINEAR), (to, [CX + off, cy], eout),
                    (b1, [W + L / 2 + 60, cy])])
        # tapered streaks are drawn fatter so neighbouring rows still overlap where they narrow
        groups.append(group([streak_shape(L, h * 2.2 if taper else h + 14, taper), fill(slot=slot)],
                            f"row{len(groups)}", position=pos))
        y += h
    # thin fast flecks that lead the whoosh in and trail it out
    for k in range(flecks):
        h = r.uniform(5, 14)
        L = r.uniform(300, 900)
        cy = r.uniform(40, H - 40)
        ti = a0 + r.uniform(0, 3)
        to = b0 + r.uniform(2, 6)
        pos = Anim([(ti, [-L / 2 - 20, cy], ein), (ti + (a1 - a0) * 0.55, [W + L / 2 + 20, cy], HOLD),
                    (to, [-L / 2 - 20, cy], eout), (b1, [W + L / 2 + 20, cy])])
        groups.append(group([rect((L, h), roundness=h / 2), fill(slot=slot)], f"fleck{k}", position=pos))
    comp.layer(name, groups)


def whoosh():
    t = Timing(13, 10, 13)
    comp = base("speed-lines-whoosh", t, {"primary": "#F5F5F7"}, ("primary",))
    streaks(comp, "primary", t.tm, 2)
    return comp, t


def stacked():
    t = Timing(15, 10, 15)
    comp = base("speed-lines-whoosh--stacked", t, "ocean", ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        streaks(comp, s, tm, 5 + i, spread=4, flecks=6, name=s)
    return comp, t


def taper():
    t = Timing.snappy()
    comp = base("speed-lines-whoosh--taper", t, "sunset", ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    streaks(comp, "primary", (a0 + 2, a1, b0, b1 - 2), 9, taper=420, ein=SNAPPY, eout=SNAPPY, spread=3,
            name="primary")
    streaks(comp, "accent", (a0, a1 - 2, b0 + 2, b1), 12, taper=420, ein=SNAPPY, eout=SNAPPY, spread=3, flecks=0,
            name="accent")
    return comp, t


VARIANTS = [
    ("whoosh", "Whoosh", whoosh, "Round-ended speed streaks of mixed thickness rush in with a ragged front and "
                                 "whoosh off to the right."),
    ("stacked", "Stacked Streaks", stacked, "Three colour passes of speed streaks rush in one after another and "
                                            "leave in reverse."),
    ("taper", "Tapered Streaks", taper, "Needle-pointed streaks whip across with snappy timing and an accent echo."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"whoosh": 0.75, "stacked": 0.7, "taper": 0.6}

build("speed-lines-whoosh", "Speed Lines Whoosh",
      "Speed-line transition: streaks rush across to cover the shot, hold for the cut, then whoosh away to reveal "
      "the next clip.",
      ["speed", "lines", "whoosh", "motion", "transition", "fast"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
