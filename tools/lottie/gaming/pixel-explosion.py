import random

from _gaming2 import *

W = H = 440
C = (W / 2, H / 2)


def blob(r, n, seed, hole=0.0, lob=0.2):
    """Cells of a lumpy disc (radius r cells) in an n x n grid, optionally with a ragged hole."""
    rng = random.Random(seed)
    ph = [rng.uniform(0, TAU) for _ in range(4)]

    def inside(x, y):
        d = math.hypot(x, y)
        a = math.atan2(y, x)
        rr = r * (1 + lob * math.sin(5 * a + ph[0]) + lob * 0.6 * math.sin(9 * a + ph[1]) + 0.05 * math.sin(13 * a + ph[2]))
        hh = hole * r * (1 + 0.25 * math.sin(6 * a + ph[3]))
        return hh <= d < rr
    return pix_cells(inside, n)


def stage_layers(r, n, seed, fracs, colors, hole=0.0):
    """Concentric colour bands of one sprite frame; top band first."""
    out = []
    for f, col in zip(fracs, colors):
        cells = blob(r * f, n, seed, hole=hole / f if f else 0, lob=0.2)
        out.append(pix_group(cells, P, (-n * P / 2, -n * P / 2), col, "band"))
    return out


P = 10


def show(t0, t1):
    return dict(ip=t0, op=t1)


def sparks(comp, n, seed, t0, cols, r1=190, life=(12, 18), size=P, grav=0.0):
    rng = random.Random(seed)
    for i in range(n):
        a = rng.uniform(0, 360)
        r = rng.uniform(r1 * 0.5, r1)
        lf = rng.randint(*life)
        col = cols[i % len(cols)]

        def fn(u, a=a, r=r, lf=lf):
            k = u / lf
            p = pt(r * ease_out(k, 2), a, C)
            y = p[1] + grav * k * k
            return {"position": [snap(p[0], P / 2), snap(y, P / 2)], "scale": [100 if k < 0.6 else 50] * 2}
        sh = box(-size / 2, -size / 2, size, size, slot=col[1]) if isinstance(col, tuple) else box(-size / 2, -size / 2, size, size, col)
        particle(comp, "spark", [sh], t0 + rng.randint(0, 3), lf, 999, fn,
                 step=2, wrap=False, hold=True)


# ---------------------------------------------------------------- fireball (classic 8-bit)

def fireball():
    F = 36
    comp = Comp("pixel-explosion", W, H, frames=F)
    comp.slot("primary", "#FFE14D")
    comp.slot("secondary", "#FF8A1F")
    comp.slot("accent", "#E8283C")
    comp.slot("outline", INK)
    n = 40
    Y, O, R_, K = ("slot", "primary"), ("slot", "secondary"), ("slot", "accent"), ("slot", "outline")
    stages = [
        (0, 3, 3.5, 0.0, [0.55, 1.0, 1.25], ["#FFFFFF", Y, K]),
        (3, 6, 7, 0.0, [0.4, 0.7, 1.0, 1.15], ["#FFFFFF", Y, O, K]),
        (6, 10, 11, 0.0, [0.35, 0.62, 0.85, 1.0, 1.1], ["#FFFFFF", Y, O, R_, K]),
        (10, 15, 14, 0.0, [0.45, 0.72, 0.9, 1.0], [Y, O, R_, K]),
        (15, 20, 16, 0.35, [0.62, 0.82, 1.0], [O, R_, K]),
        (20, 25, 17, 0.6, [0.8, 1.0], [R_, K]),
    ]
    sparks(comp, 14, 3, 6, [Y, O, "#FFFFFF"], r1=200)
    for i, (t0, t1, r, hole, fr, cols) in enumerate(stages):
        comp.layer(f"frame {i}", stage_layers(r, n, 10 + i, fr, cols, hole), position=C, **show(t0, t1))
    # smoke puffs after the fire
    rng = random.Random(8)
    for k in range(7):
        a = k * 360 / 7 + rng.uniform(-15, 15)
        p0 = pt(rng.uniform(80, 130), a, C)
        cells = pix_cells(lambda x, y: x * x + y * y <= 2.6 ** 2, 6)
        for s_i, (sc, t0) in enumerate(((100, 22), (70, 27), (40, 31))):
            comp.layer("smoke", [pix_group(cells, P, (-3 * P, -3 * P), ("#9A94A8", 100), "puff"),
                                 pix_group(pix_cells(lambda x, y: x * x + y * y <= 3.4 ** 2, 8), P, (-4 * P, -4 * P), K, "o")],
                       position=(snap(p0[0], P), snap(p0[1] - s_i * 20, P)), scale=[sc, sc], ip=t0, op=t0 + 5)
    return comp


# ---------------------------------------------------------------- debris (16-bit)

def debris():
    F = 45
    comp = Comp("pixel-explosion--debris", W, H, frames=F)
    comp.slot("primary", "#FFD23F")
    comp.slot("secondary", "#FF6A2B")
    comp.slot("outline", "#2A1B2E")
    comp.slot("background", "#7C7390")
    Y, O, K, S = ("slot", "primary"), ("slot", "secondary"), ("slot", "outline"), ("slot", "background")
    n = 44
    # shockwave ring (pixel)
    for k, (t0, r) in enumerate(((2, 8), (4, 12), (6, 16), (8, 19), (10, 21))):
        ring = pix_cells(lambda x, y, r=r: (r - 1.3) ** 2 <= x * x + y * y < r * r, n)
        comp.layer("ring", [pix_group(ring, P, (-n * P / 2, -n * P / 2), ("slot", "primary", 100 - k * 18), "r")], position=C, ip=t0, op=t0 + 2)
    # fire core frames
    frames = [(0, 3, 5, 0, [0.6, 1.0, 1.2], ["#FFFFFF", Y, K]), (3, 7, 10, 0, [0.4, 0.75, 1.0, 1.1], ["#FFFFFF", Y, O, K]),
              (7, 12, 13, 0.2, [0.55, 0.85, 1.0], [Y, O, K]), (12, 16, 13, 0.5, [0.8, 1.0], [O, K])]
    for i, (t0, t1, r, hole, fr, cols) in enumerate(frames):
        comp.layer(f"core {i}", stage_layers(r, 34, 30 + i, fr, cols, hole), position=C, ip=t0, op=t1)
    # debris chunks with gravity
    rng = random.Random(5)
    for i in range(12):
        a = rng.uniform(-150, 150)
        v = rng.uniform(170, 260)
        lf = rng.randint(22, 30)
        sz = rng.choice((2, 3))
        cells = [(c, r) for c in range(sz) for r in range(sz)]

        def fn(u, a=a, v=v, lf=lf):
            s = u / 30
            p = pt(v * s, a, C)
            y = p[1] + 520 * s * s
            return {"position": [snap(p[0], 5), snap(y, 5)], "rotation": 90 * int(u // 4)}
        particle(comp, "chunk", [pix_group(cells, 6, (-sz * 3, -sz * 3), "#4A3F55", "c"),
                                 pix_group([(c, r) for c in range(-1, sz + 1) for r in range(-1, sz + 1)], 6, (-sz * 3, -sz * 3), K, "o")],
                 6 + rng.randint(0, 2), lf, F, fn, step=2, wrap=False, hold=True)
    # rising smoke column: puffs that grow then shrink
    rng = random.Random(11)
    for i in range(9):
        x = C[0] + rng.uniform(-70, 70)
        y0 = C[1] + rng.uniform(-30, 40)
        t0 = 10 + rng.randint(0, 8)
        lf = rng.randint(22, 30)
        r = rng.uniform(3, 4.5)
        disc = pix_cells(lambda x_, y_, r=r: x_ * x_ + y_ * y_ <= r * r, 10)
        rim = pix_cells(lambda x_, y_, r=r: x_ * x_ + y_ * y_ <= (r + 1) ** 2, 12)
        hi = [(c, rr) for c, rr in disc if rr < 4 and c < 5]

        def fn(u, x=x, y0=y0, lf=lf):
            k = u / lf
            s = [100, 100] if k < 0.5 else [75, 75] if k < 0.8 else [45, 45]
            return {"position": [snap(x, 5), snap(y0 - 90 * ease_out(k), 5)], "scale": s}
        particle(comp, "smoke", [pix_group(hi, 6, (-30, -30), ("#FFFFFF", 30), "hi"), pix_group(disc, 6, (-30, -30), S, "s"),
                                 pix_group(rim, 6, (-36, -36), K, "o")], t0, lf, F, fn, step=3, wrap=False, hold=True)
    sparks(comp, 10, 6, 3, [Y, "#FFFFFF"], r1=170, size=8, grav=60)
    return comp


# ---------------------------------------------------------------- mono (handheld green)

def mono():
    F = 30
    comp = Comp("pixel-explosion--mono", W, H, frames=F)
    comp.slot("primary", "#9BBC0F")
    comp.slot("secondary", "#8BAC0F")
    comp.slot("accent", "#306230")
    comp.slot("outline", "#0F380F")
    L1, L2, D1, D2 = ("slot", "primary"), ("slot", "secondary"), ("slot", "accent"), ("slot", "outline")
    n = 40

    def starburst(r, spikes, inner, hole=0.0, rot=0):
        def f(x, y):
            d = math.hypot(x, y)
            a = math.atan2(y, x) + rot
            rr = inner + (r - inner) * max(0, math.cos(spikes * a / 2)) ** 6
            return hole <= d < rr
        return pix_cells(f, n)
    o = (-n * P / 2, -n * P / 2)
    frames = [
        (0, 3, [(starburst(5, 8, 2.5), L1), (starburst(6, 8, 3.5), D2)]),
        (3, 6, [(starburst(9, 8, 3.5, rot=0.2), L1), (starburst(10.5, 8, 5, rot=0.2), D1), (starburst(11.5, 8, 6, rot=0.2), D2)]),
        (6, 10, [(starburst(12, 8, 5, rot=0.4), L1), (starburst(14, 8, 7, rot=0.4), D1), (starburst(15, 8, 8, rot=0.4), D2)]),
        (10, 14, [(starburst(15, 8, 6, 3, rot=0.6), L2), (starburst(17, 8, 8, 2.5, rot=0.6), D1), (starburst(18, 8, 9, 2, rot=0.6), D2)]),
        (14, 18, [(starburst(17, 8, 7, 8, rot=0.8), D1), (starburst(18.5, 8, 9, 7, rot=0.8), D2)]),
        (18, 22, [(starburst(18.5, 16, 11, 14, rot=1.0), D1), (starburst(19.5, 16, 12, 13, rot=1.0), D2)]),
    ]
    for i, (t0, t1, bands) in enumerate(frames):
        comp.layer(f"frame {i}", [pix_group(cells, P, o, col, "b") for cells, col in bands], position=C, ip=t0, op=t1)
    # 4 plus-sparkles blinking at the corners
    PLUS = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    for k, a in enumerate((45, 135, 225, 315)):
        p = pt(170, a, C)
        comp.layer("twinkle", [pix_group(PLUS, P, (-1.5 * P, -1.5 * P), L1, "p"),
                               pix_group([(c + dc, r + dr) for c, r in PLUS for dc, dr in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))],
                                         P, (-1.5 * P, -1.5 * P), D2, "o")],
                   position=(snap(p[0], P), snap(p[1], P)), ip=8 + k % 2 * 3, op=22 + k % 2 * 3,
                   opacity=stepped(lambda t: 100 if (t // 3) % 2 == 0 else 0, 0, F, 1))
    return comp


build_asset(CAT, "pixel-explosion", "Pixel Explosion",
            "Pixel-art explosion burst that plays out sprite by sprite and ends empty. Drop it on a hit, a kill or "
            "a jump cut.",
            ["explosion", "pixel", "8-bit", "retro", "boom", "blast", "gaming", "sprite"], [
    Variant("fireball", "Fireball", fireball(), "intro-hold", thumb_t=0.28, bg="e8e8ee",
            description="Classic 8-bit fireball: white core, yellow-orange-red bands, sparks and smoke puffs."),
    Variant("debris", "Debris", debris(), "intro-hold", thumb_t=0.24, bg="e8e8ee",
            description="16-bit blast with a pixel shockwave ring, tumbling debris chunks and a rising smoke column."),
    Variant("mono", "Handheld", mono(), "intro-hold", thumb_t=0.3, bg="e8e8ee",
            description="Four-shade green handheld-console starburst with blinking corner twinkles."),
])
