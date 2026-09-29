from _common import *


def splat_points(seed, n=26, spikes=7):
    """Unit ink splat outline: a lumpy disc with a few long tapered arms (min radius ~0.8)."""
    r = random.Random(seed)
    arms = set(r.sample(range(n), spikes))
    pts = []
    for i in range(n):
        a = 2 * math.pi * (i + r.uniform(-0.2, 0.2)) / n
        rr = r.uniform(1.25, 1.55) if i in arms else r.uniform(0.85, 1.0)
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    return pts


def splat_items(seed, radius, drops=6):
    """Splat path plus a few satellite droplets, sized so its inner radius is ~radius*0.85."""
    r = random.Random(seed + 100)
    pts = [(x * radius, y * radius) for x, y in splat_points(seed)]
    items = [path(smooth_closed(pts, tension=0.9), "splat")]
    for k in range(drops):
        a = r.uniform(0, 2 * math.pi)
        d = radius * r.uniform(1.6, 2.1)
        s = radius * r.uniform(0.08, 0.2)
        items.append(ellipse((s, s), position=(math.cos(a) * d, math.sin(a) * d), name=f"drop{k}"))
    return items


def reach(center):
    """Distance from center to the farthest frame corner."""
    return max(math.hypot(x - center[0], y - center[1]) for x in (0, W) for y in (0, H))


def splash(comp, slot, tm, center=C, seed=1, ein=POP, eout=SMOOTH, name="splat"):
    """A splat bursts open over the frame; a splat-shaped hole then blows it away."""
    a0, a1, b0, b1 = tm
    rad = reach(center) / 0.8 + 40
    comp.layer(name + "-in", [group(splat_items(seed, rad) + [fill(slot=slot)], "ink",
                                    scale=anim([(a0, [0, 0], ein), (a1, [100, 100])]),
                                    rotation=anim([(a0, -25, SNAP_OUT), (a1, 0)]))],
               position=center, op=b0 + 1)
    hole = splat_items(seed + 50, reach(center) / 0.8 + 40, drops=0)
    comp.layer(name + "-out", [group([rect((8000, 8000))] + [group(hole, "hole", scale=anim(
        [(b0, [0, 0], eout), (b1, [140, 140])]), rotation=anim([(b0, 20, eout), (b1, 0)]))]
        + [fill(slot=slot, even_odd=True)], "sheet")], position=center, ip=b0)


def flat():
    t = Timing(12, 10, 14)
    comp = base("ink-splash", t, "night", ("primary",))
    splash(comp, "primary", t.tm, seed=4)
    return comp, t


def multi():
    t = Timing(15, 10, 15)
    comp = base("ink-splash--multi", t, "violet", ("primary", "secondary", "accent"))
    spots = {"primary": (CX + 40, CY + 20), "secondary": (CX + 520, CY + 260), "accent": (CX - 560, CY - 240)}
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        splash(comp, s, tm, center=spots[s], seed=7 + i * 13, name=s)
    return comp, t


def spatter():
    """Many small splats pop across the frame in quick succession, then dry up in reverse."""
    t = Timing(14, 10, 14)
    comp = base("ink-splash--spatter", t, "violet", ("primary", "secondary"))
    a0, a1, b0, b1 = t.tm
    r = random.Random(21)
    cols, rows = 5, 3
    cw, ch = W / cols, H / rows
    cells = [(c, rw) for c in range(cols) for rw in range(rows)]
    r.shuffle(cells)
    need = math.hypot(cw, ch) * 0.75 + 60  # splat inner radius must reach the cell corners from the jittered centre
    for k, (c, rw) in enumerate(cells):
        cx = (c + 0.5) * cw + r.uniform(-50, 50)
        cy = (rw + 0.5) * ch + r.uniform(-40, 40)
        u = k / (len(cells) - 1)
        tin = a0 + round(u * (a1 - a0 - 6))
        tout = b0 + round((1 - u) * (b1 - b0 - 6))
        slot = "secondary" if k % 3 == 0 else "primary"
        rad = need / 0.8
        comp.layer(f"spot{k}", [group(splat_items(30 + k, rad, drops=4) + [fill(slot=slot)], "ink",
                                      rotation=r.uniform(0, 360),
                                      scale=anim([(tin, [0, 0], BACK), (tin + 6, [100, 100], LINEAR),
                                                  (tout, [100, 100], ACCEL), (tout + 6, [0, 0])]))],
                   position=(cx, cy))
    # layers added first draw on top, so later pops would hide under earlier ones; flip the order
    comp.layers.reverse()
    return comp, t


VARIANTS = [
    ("splat", "Single Splat", flat, "One big ink splat bursts out of the centre with a little overshoot, then a "
                                    "splat-shaped hole blows it away.", {"bg": "e8e8ee"}),
    ("multi", "Colour Splats", multi, "Accent, secondary and primary splats land from different spots and clear in "
                                      "reverse."),
    ("spatter", "Spatter", spatter, "Fifteen small splats pop across the frame one after another, then shrink "
                                    "away in reverse order."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"splat": 0.25, "multi": 0.4, "spatter": 0.3}

build("ink-splash", "Ink Splash",
      "Ink splash transition: a splat of paint bursts over the shot, holds on solid colour for the cut, then "
      "splashes away to reveal the next clip.",
      ["ink", "splash", "splat", "paint", "transition", "grunge"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
