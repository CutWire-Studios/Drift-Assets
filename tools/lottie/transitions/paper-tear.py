from _common import *

PAPER = {"primary": "#EFE7D6", "secondary": "#C9B391", "accent": "#FFFFFF"}
TONES = {"primary": "#F2ECDF", "secondary": "#E85D4A", "accent": "#2F3A56"}


def jag(seed, a, b, step=34, amp=26, wave=36, axis_len=None):
    """Torn-paper offsets from coordinate a to b: fine random teeth over a slow wave."""
    r = random.Random(seed)
    ph = r.uniform(0, 6.28)
    n = int(abs(b - a) / step) + 1
    out = []
    for i in range(n + 1):
        s = a + (b - a) * i / n
        out.append((s, r.uniform(-amp, amp) * (0.4 if i % 2 else 1) + wave * math.sin(s / 170 + ph)))
    return out


def torn_sheet(seed, width, height=1320):
    """Sheet centred on (0,0) with torn left and right edges."""
    right = [(width / 2 + d, y) for y, d in jag(seed, -height / 2, height / 2)]
    left = [(-width / 2 + d, y) for y, d in jag(seed + 1, height / 2, -height / 2)]
    return path(bezier(right + left, closed=True), "sheet")


SHEET_W = 2 * (CX + 90)


def slide(comp, slot, tm, seed, ease=SMOOTH, name="sheet"):
    d = SHEET_W / 2 + 90
    comp.layer(name, [group([torn_sheet(seed, SHEET_W), fill(slot=slot)], "paper")],
               position=io(tm, [-d, CY], [CX, CY], [W + d, CY], ease),
               rotation=io(tm, -3, 0, 3, ease))


def sheet():
    t = Timing(15, 10, 15)
    comp = base("paper-tear", t, PAPER, ("primary",))
    slide(comp, "primary", t.tm, 3)
    return comp, t


def layered():
    t = Timing(16, 10, 16)
    comp = base("paper-tear--layered", t, TONES, ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        slide(comp, s, tm, 10 + i * 7, name=s)
    return comp, t


def rip():
    """Two halves meet along a torn line; the outro rips them apart, showing white fibre edges."""
    t = Timing(14, 10, 16)
    comp = base("paper-tear--rip", t, PAPER, ("primary", "secondary", "accent"))
    a0, a1, b0, b1 = t.tm
    X = CX + 160
    tear = [(x, d * 1.6) for x, d in jag(41, -X, X, step=30, amp=24, wave=40)]
    fr = random.Random(5)
    backs = []
    for i, sgn in enumerate((-1, 1)):
        edge = [(x, y - sgn * 4) for x, y in tear]  # overlap the other half by a few px
        fib = [(x, y - sgn * fr.uniform(10, 24)) for x, y in tear]
        far = [(X, sgn * 1400), (-X, sgn * 1400)]  # tear runs -X -> X, then round the far side
        half = group([path(bezier(edge + far, closed=True)), fill(slot="primary")], "half")
        fibre = group([path(bezier(fib + far, closed=True)), fill(slot="accent")], "fibre")
        shade = group([path(bezier([(x, y + sgn * 10) for x, y in fib] + far, closed=True)),
                       fill(slot="secondary")], "shadow")
        off = sgn * (CY + 320)
        tm = (a0 + i * 2, a1 - 2 + i * 2, b0 + i * 2, b1 - 2 + i * 2)
        motion = dict(position=io(tm, [CX, CY + off], [CX, CY], [CX + sgn * 60, CY + off * 1.1], SNAPPY, ACCEL),
                      rotation=io(tm, -sgn * 5, 0, sgn * 6, SNAPPY, ACCEL))
        comp.layer(f"half-{i}", [half], **motion)
        backs.append((f"edge-{i}", [fibre, shade], motion))
    # torn fibre edges sit under both halves, so they only show once the halves part
    for name, items, motion in backs:
        comp.layer(name, items, **motion)
    return comp, t


VARIANTS = [
    ("sheet", "Torn Sheet", sheet, "A sheet of paper with torn edges slides across, holds, then slides off the far "
                                   "side."),
    ("layered", "Layered Strips", layered, "Three torn paper strips in different colours slide in one after "
                                           "another and peel off in reverse."),
    ("rip", "Rip Apart", rip, "Two paper halves snap together along a torn line, then rip apart with white fibre "
                              "edges showing."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"sheet": 0.5, "layered": 0.55, "rip": 0.5}

build("paper-tear", "Paper Tear",
      "Torn paper transition: a paper sheet with ragged edges covers the shot, holds for the cut, then tears away "
      "to reveal the next clip.",
      ["paper", "tear", "rip", "craft", "transition", "collage"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
