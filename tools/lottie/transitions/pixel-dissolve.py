from _common import *

PIX = {"primary": "#1D1A2F", "secondary": "#7B4DFF", "accent": "#2EE6D6"}


def grid(px):
    cols, rows = math.ceil(W / px), math.ceil(H / px)
    ox, oy = (W - cols * px) / 2, (H - rows * px) / 2
    return [(c, r, (ox + (c + 0.5) * px, oy + (r + 0.5) * px)) for c in range(cols) for r in range(rows)], cols, rows


def cell(px, pos, slot, on, off, n, name):
    """Square that is hidden, pops on at `on`, pops off at `off` (hold keys: crisp pixels)."""
    op = Anim([(0, 0, HOLD), (on, 100, HOLD), (off, 0, HOLD), (n, 0)])
    return group([rect((px + 12, px + 12), position=pos), fill(slot=slot)], name, opacity=op)


def rand_order(tm, px, seed, slot="primary"):
    a0, a1, b0, b1 = tm
    r = random.Random(seed)
    cells, _, _ = grid(px)
    return [cell(px, p, slot, r.randint(a0 + 1, a1), r.randint(b0 + 1, b1), b1 + 1, f"p{c}-{rw}")
            for c, rw, p in cells]


def random_():
    t = Timing(14, 10, 14)
    comp = base("pixel-dissolve", t, "violet", ("primary",))
    comp.layer("pixels", rand_order(t.tm, 120, 5))
    return comp, t


def wave():
    """Pixels resolve in a diagonal wave, flicking accent -> secondary -> primary as they land."""
    t = Timing(16, 10, 16)
    comp = base("pixel-dissolve--wave", t, PIX, ("primary", "secondary", "accent"))
    a0, a1, b0, b1 = t.tm
    r = random.Random(9)
    cells, cols, rows = grid(96)
    layers = {"primary": [], "secondary": [], "accent": []}
    for c, rw, p in cells:
        u = (c / cols) * 0.75 + (rw / rows) * 0.25
        u = min(max(u + r.uniform(-0.12, 0.12), 0), 1)
        on = a0 + 1 + round(u * (a1 - a0 - 5))
        off = b0 + 1 + round(u * (b1 - b0 - 5))
        for k, s in enumerate(("accent", "secondary", "primary")):
            # accent lands first and leaves last; primary lands last and leaves first
            layers[s].append(cell(96, p, s, on + k * 2, off + (2 - k) * 2, b1 + 1, f"{s[0]}{c}-{rw}"))
    for s in ("primary", "secondary", "accent"):
        comp.layer(s, layers[s])
    return comp, t


def scan():
    """Raster scan: rows of chunky pixels fill left to right with a ragged accent frontier."""
    t = Timing(14, 8, 14)
    comp = base("pixel-dissolve--scan", t, {"primary": "#C6FF3D", "accent": "#FF3D7F"}, ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    r = random.Random(4)
    px = 160
    cells, cols, rows = grid(px)
    top, front = [], []
    for c, rw, p in cells:
        u = min(max((rw + c / cols) / rows + r.uniform(-0.05, 0.05), 0), 1)
        on = a0 + 2 + round(u * (a1 - a0 - 4))
        off = b0 + 2 + round(u * (b1 - b0 - 4))
        top.append(cell(px, p, "primary", on, off, b1 + 1, f"p{c}-{rw}"))
        front.append(cell(px, p, "accent", on - 1, off + 1, b1 + 1, f"f{c}-{rw}"))
    comp.layer("pixels", top)
    comp.layer("frontier", front)
    return comp, t


VARIANTS = [
    ("random", "Random Dissolve", random_, "Square pixels pop on in random order until the frame is solid, then pop "
                                           "off at random."),
    ("wave", "Colour Wave", wave, "Small pixels resolve in a ragged wave from left to right, flicking through accent "
                                  "and secondary before landing.", {"bg": "e8e8ee"}),
    ("scan", "Raster Scan", scan, "Chunky pixels fill row by row like a retro raster scan, with an accent "
                                  "frontier."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"random": 0.5, "wave": 0.55, "scan": 0.45}

build("pixel-dissolve", "Pixel Dissolve",
      "Pixel transition: square pixels fill in to cover the shot, hold for the cut, then dissolve away to reveal "
      "the next clip.",
      ["pixel", "dissolve", "8-bit", "retro", "transition", "digital"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
