from _common import *

CELL = 200


def layout(seed, cell=CELL):
    """Jittered bubble grid whose circles always cover the frame, plus a few oversized ones."""
    r = random.Random(seed)
    cols, rows = math.ceil(W / cell) + 1, math.ceil(H / cell) + 1
    ox, oy = (W - (cols - 1) * cell) / 2, (H - (rows - 1) * cell) / 2
    out = []
    j = cell * 0.18
    for c in range(cols):
        for rw in range(rows):
            x = ox + c * cell + r.uniform(-j, j)
            y = oy + rw * cell + r.uniform(-j, j)
            # must reach the far corners of its cell neighbourhood despite the jitter
            d = 2 * (cell * math.sqrt(2) / 2 + j * math.sqrt(2) + 16) * r.uniform(1.0, 1.35)
            out.append((x, y, d))
    r.shuffle(out)
    return out


def bubbles(comp, slot, tm, seed, dur=7, ein=POP, name="bubbles"):
    """Bubbles pop in (random order, springy) and burst out (grow a touch, then vanish)."""
    a0, a1, b0, b1 = tm
    groups = []
    lay = layout(seed)
    for k, (x, y, d) in enumerate(lay):
        u = k / (len(lay) - 1)
        ti = a0 + u * (a1 - a0 - dur)
        to = b0 + (1 - u) * (b1 - b0 - dur * 0.6)
        sc = Anim([(ti, [0, 0], ein), (ti + dur, [100, 100], LINEAR), (to, [100, 100], EASE_OUT),
                   (to + dur * 0.3, [112, 112], EASE_IN), (to + dur * 0.6, [0, 0])])
        groups.append(group([ellipse((d, d)), fill(slot=slot)], f"b{k}", position=(x, y), scale=sc))
    comp.layer(name, groups[::-1])  # later pops draw on top


def pop():
    t = Timing(15, 10, 12)
    comp = base("bubble-pop", t, {"primary": "#18C8E8"})
    bubbles(comp, "primary", t.tm, 3)
    return comp, t


def layered():
    t = Timing(16, 10, 14)
    comp = base("bubble-pop--layered", t, "cherry", ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        bubbles(comp, s, tm, 10 + i, dur=6, name=s)
    return comp, t


def glossy():
    """Glossy bubbles with highlights rise from below, wobbling, and float off the top."""
    t = Timing(16, 10, 16)
    comp = base("bubble-pop--rise", t, {"primary": "#7B4DFF", "accent": "#FFFFFF"}, ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    r = random.Random(7)
    lay = layout(21, cell=220)
    lay.sort(key=lambda b: -b[1])  # bottom rows arrive first
    items = []
    for k, (x, y, d) in enumerate(lay):
        u = k / (len(lay) - 1)
        ti = a0 + u * (a1 - a0 - 8)
        to = b0 + u * (b1 - b0 - 8)
        rise = H + d
        pos = Anim([(ti, [x + r.uniform(-60, 60), y + rise], SNAP_OUT), (ti + 8, [x, y], LINEAR),
                    (to, [x, y], EASE_IN), (to + 8, [x + r.uniform(-60, 60), y - rise])])
        sc = Anim([(ti, [40, 40], SNAP_OUT), (ti + 8, [100, 100], LINEAR), (to, [100, 100], EASE_IN),
                   (to + 8, [70, 70])])
        op = Anim([(0, 100, LINEAR), (a1 - 3, 100, EASE_IN), (a1, 0, HOLD), (b0, 0, EASE_OUT), (b0 + 3, 100)])
        items.append(group([ellipse((d * 0.2, d * 0.12), position=(-d * 0.2, -d * 0.25)), fill(slot="accent")],
                           f"g{k}", position=pos, scale=sc, rotation=-35, opacity=op))
        items.append(group([ellipse((d, d)), fill(slot="primary")], f"b{k}", position=pos, scale=sc))
    comp.layer("bubbles", items)
    return comp, t


VARIANTS = [
    ("pop", "Bubble Pop", pop, "Round bubbles of different sizes pop in with a springy overshoot until the frame "
                               "is filled, then burst away."),
    ("layered", "Layered Bubbles", layered, "Three waves of bubbles in accent, secondary and primary pop in over each "
                                            "other and burst in reverse."),
    ("rise", "Rising Bubbles", glossy, "Glossy bubbles with highlights float up from the bottom, pack together, then "
                                       "float off the top."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"pop": 0.35, "layered": 0.45, "rise": 0.4}

build("bubble-pop", "Bubble Pop",
      "Bubble transition: round bubbles pop in to fill the shot, hold for the cut, then burst away to reveal the "
      "next clip.",
      ["bubbles", "circles", "pop", "playful", "transition", "kids"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
