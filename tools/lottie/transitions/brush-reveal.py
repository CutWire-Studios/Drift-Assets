from _common import *

ROWS = 4
GAP = 300
WIDTH = 420
X0, X1 = -330, W + 330


def zigzag(dy=0, rows=ROWS, gap=GAP, tilt=110, wave=26):
    """Back-and-forth wavy brush path; the turns happen off-canvas. tilt: rise over each pass (px)."""
    y0 = CY - gap * (rows - 1) / 2
    pts = []
    for i in range(rows):
        y = y0 + i * gap + dy
        xs = [X0 + (X1 - X0) * k / 12 for k in range(13)]
        if i % 2:
            xs = xs[::-1]
        for x in xs:
            pts.append((x, y + tilt * (0.5 - x / W) + wave * math.sin(x / 230 + i * 1.7)))
    return path(smooth_open(pts), "zigzag")


def pass_trim(tm, ease=SMOOTH, lag=(0, 0)):
    a0, a1, b0, b1 = tm
    return trim(end=anim([(a0 + lag[0], 0, ease), (a1 - lag[1], 100)]),
                start=anim([(b0 + lag[0], 0, ease), (b1 - lag[1], 100)]))


def brush(comp, slot, tm, ease=SMOOTH, name="brush"):
    comp.layer(name, [group([zigzag(), stroke(slot=slot, width=WIDTH, cap="round", join="round"),
                             pass_trim(tm, ease)], "stroke")])


def zig():
    t = Timing(16, 10, 16)
    comp = base("brush-reveal", t, {"primary": "#FF5A36"})
    brush(comp, "primary", t.tm)
    return comp, t


def layered():
    t = Timing(17, 8, 17)
    comp = base("brush-reveal--layered", t, "violet", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        brush(comp, s, tm, name=s)
    return comp, t


def dry():
    """Dry brush: a solid core plus bristle streaks that trail and fray at the tip and edges."""
    t = Timing(16, 10, 16)
    comp = base("brush-reveal--dry-brush", t, {"primary": "#141414"}, ("primary",))
    r = random.Random(8)
    groups = [group([zigzag(), stroke(slot="primary", width=WIDTH - 60, cap="round"), pass_trim(t.tm)], "core")]
    for k in range(26):
        dy = r.uniform(-1, 1) * (WIDTH / 2 + 10)
        w = r.uniform(8, 34) if abs(dy) > WIDTH / 2 - 40 else r.uniform(30, 70)
        lag = (r.randint(0, 3), r.randint(0, 2))
        groups.append(group([zigzag(dy), stroke(slot="primary", width=w, cap="round"),
                             pass_trim(t.tm, lag=lag)], f"bristle{k}"))
    comp.layer("dry-brush", groups)
    return comp, t


VARIANTS = [
    ("zigzag", "Brush Zigzag", zig, "One fat round brush paints back and forth across the frame, then the paint "
                                    "is wiped off in the same path."),
    ("layered", "Layered Paint", layered, "Accent, secondary and primary coats are painted one after another and "
                                          "wiped off in reverse."),
    ("dry-brush", "Dry Brush", dry, "Ink dry brush with frayed bristle streaks trailing at the tip and edges.",
     {"bg": "e8e8ee"}),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"zigzag": 0.3, "layered": 0.55, "dry-brush": 0.5}

build("brush-reveal", "Brush Reveal",
      "Paint brush transition: a thick brush stroke paints over the shot, holds on solid paint for the cut, then "
      "is wiped away to reveal the next clip.",
      ["brush", "paint", "stroke", "reveal", "transition", "art"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
