import random

from _gaming2 import *

W, H, F = 1920, 1080, 60
IMP = (1010, 420)
HIT = 3
TA = (560, 640, 800, 150)


def crack_lines(seed=5, n=13, reach=(420, 1100), step=(40, 95), jitter=22, branches=True):
    rng = random.Random(seed)
    lines = []
    for i in range(n):
        a = i * 360 / n + rng.uniform(-10, 10)
        L = rng.uniform(*reach)
        p = pt(rng.uniform(10, 30), a, IMP)
        pts = [p]
        d = 0
        heading = a
        while d < L:
            heading += rng.uniform(-jitter, jitter)
            heading = a + clamp(heading - a, -28, 28)
            s = rng.uniform(*step)
            p = pt(s, heading, p)
            pts.append(p)
            d += s
            if branches and rng.random() < 0.22 and d > 80:
                bh = heading + rng.choice((-1, 1)) * rng.uniform(25, 50)
                bp = [p]
                q = p
                for _ in range(rng.randint(2, 4)):
                    bh += rng.uniform(-15, 15)
                    q = pt(rng.uniform(30, 70), bh, q)
                    bp.append(q)
                lines.append((bp, d / L, True))
        lines.append((pts, 0.0, False))
    return lines


def rings(seed=9, radii=(70, 150, 260)):
    rng = random.Random(seed)
    out = []
    for r in radii:
        k = 13
        pts = [pt(r * rng.uniform(0.85, 1.12), i * 360 / k + rng.uniform(-8, 8), IMP) for i in range(k)]
        # break the ring into partial segments
        for j in range(k):
            if rng.random() < 0.65:
                out.append([pts[j], pts[(j + 1) % k]])
    return out


def draw_on(t0, frac, dur=7):
    s = t0 + frac * 6
    return trim(end=anim([(s, 0, EASE_OUT), (s + dur, 100)]))


def shake(amp=18):
    keys = [(0, [0, 0], HOLD)]
    for i, (dx, dy) in enumerate(((amp, -amp * 0.6), (-amp * 0.8, amp * 0.5), (amp * 0.5, -amp * 0.3), (-amp * 0.3, amp * 0.2),
                                  (amp * 0.12, 0), (0, 0))):
        keys.append((HIT + i * 2, [dx, dy], EASE_IN_OUT))
    keys.append((F, [0, 0], HOLD))
    return anim(keys)


def shard_polys(seed=3, n=9):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a = i * 360 / n + rng.uniform(-15, 15)
        r0, r1 = rng.uniform(30, 90), rng.uniform(120, 220)
        w = rng.uniform(14, 26)
        p0, p1, p2 = pt(r0, a - w), pt(r1, a), pt(r0 * 1.2, a + w)
        c = ((p0[0] + p1[0] + p2[0]) / 3, (p0[1] + p1[1] + p2[1]) / 3)
        out.append(([(x - c[0], y - c[1]) for x, y in (p0, p1, p2)], c, rng.uniform(-1, 1)))
    return out


def falling_shards(comp, paint, seed=3, hold=False):
    for pts, c, spin in shard_polys(seed):
        t0 = HIT + 4 + int(abs(spin) * 6)
        life = 40

        def fn(u, c=c, spin=spin, life=life):
            s = u / 30
            x = IMP[0] + c[0] * (1 + 0.6 * s) + spin * 60 * s
            y = IMP[1] + c[1] * (1 + 0.3 * s) + 0.5 * 2200 * s * s
            if hold:
                x, y = snap(x, 12), snap(y, 12)
            return {"position": [x, y], "rotation": spin * 260 * s if not hold else 90 * round(spin * 3 * s),
                    "opacity": 100 * (1 - ease_in(u / life, 2))}
        comp.layer("shard still", [group([poly(pts)] + paint, "s")], position=(IMP[0] + c[0], IMP[1] + c[1]), ip=HIT, op=t0)
        particle(comp, "shard", [group([poly(pts)] + paint, "s")], t0, life, F, fn, wrap=False, hold=hold,
                 step=2 if hold else 1)


def overlay(comp, grey="#2A2A30", grey_op=45, vig="#000000", vig_op=0.85, t0=HIT, dur=24, tint=None):
    if tint:
        comp.layer("tint", [group([rect((W, H), (W / 2, H / 2)), fill(tint[0], tint[1])], "t")],
                   opacity=anim([(t0, 0, EASE_OUT), (t0 + dur, 100)]))
    comp.layer("vignette", [group([rect((W, H), (W / 2, H / 2)),
                                   gradient_fill([(0, vig, 0), (0.45, vig, 0.05), (0.8, vig, vig_op * 0.7), (1, vig, vig_op)],
                                                 (W / 2, H / 2), (W / 2 + 1150, H / 2), radial=True)], "v")],
               opacity=anim([(t0, 0, EASE_OUT), (t0 + dur, 100)]))
    comp.layer("desaturate", [group([rect((W, H), (W / 2, H / 2)), fill(slot="background")], "g")],
               opacity=anim([(t0, 0, EASE_OUT), (t0 + dur, grey_op)]))


# ---------------------------------------------------------------- glass

def glass():
    comp = Comp("defeat-screen-crack", W, H, frames=F)
    comp.slot("primary", "#FFFFFF")
    comp.slot("background", "#3A3A42")
    comp.slot("accent", "#C8202C")
    rig = comp.null("rig", position=shake())
    falling_shards(comp, [fill("#FFFFFF", 22), stroke(slot="primary", width=2.5, opacity=90)])
    comp.layer("impact flash", [glow(520, "#FFFFFF", 0.9)], position=IMP, ip=HIT, op=HIT + 12,
               scale=anim([(HIT, [20, 20], SNAP_OUT), (HIT + 5, [100, 100])]), opacity=anim([(HIT, 100, EASE_IN), (HIT + 11, 0)]))
    lines = crack_lines()
    items = []
    for k, (pts, frac, br) in enumerate(lines):
        w = 3 if br else 5
        items.append(group([polyline(pts), draw_on(HIT, frac), stroke(slot="primary", width=w, join="miter", cap="butt")], f"c{k}"))
        items.append(group([polyline(pts), draw_on(HIT, frac), stroke("#000000", width=w + 4, opacity=45, join="miter", cap="butt")],
                           f"cs{k}"))
    ring_items = [group([polyline(seg_), trim(end=anim([(HIT + 2, 0, EASE_OUT), (HIT + 8, 100)])),
                         stroke(slot="primary", width=2, opacity=85)], f"r{k}") for k, seg_ in enumerate(rings())]
    comp.layer("cracks", items + ring_items, parent=rig)
    comp.layer("impact", [group([ellipse((70, 70)), fill("#FFFFFF", 30), stroke(slot="primary", width=3)], "hole"),
                          group([star(9, 60, 26), fill("#FFFFFF", 18)], "star")], parent=rig, position=IMP,
               ip=HIT, scale=pop(HIT, 6))
    comp.layer("red edge", [group([rect((W, H), (W / 2, H / 2)),
                                   gradient_fill([(0, "#C8202C", 0), (0.62, "#C8202C", 0), (1, "#C8202C", 0.55)],
                                                 (W / 2, H / 2), (W / 2 + 1100, H / 2), radial=True)], "r")],
               opacity=anim([(HIT, 0, EASE_OUT), (HIT + 4, 100, EASE_IN_OUT), (HIT + 30, 45)]))
    overlay(comp)
    return comp


# ---------------------------------------------------------------- pixel

def pixel():
    comp = Comp("defeat-screen-crack--pixel", W, H, frames=F)
    comp.slot("primary", "#FFFFFF")
    comp.slot("background", "#2A2238")
    comp.slot("outline", INK)
    P = 12
    rig = comp.null("rig", position=stepped(lambda t: [[0, 0], [24, -12], [-24, 12], [12, 0], [0, 0]][min(4, max(0, int((t - HIT) // 2)))]
                                            if t >= HIT else [0, 0], 0, F, 1))
    falling_shards(comp, [fill("#FFFFFF", 70), stroke(slot="outline", width=4, join="miter")], hold=True)
    lines = crack_lines(seed=6, n=11, step=(50, 110), branches=True)
    # rasterise each crack into grid cells, revealed in 3 stepped waves
    waves = [[], [], []]
    for pts, frac, br in lines:
        cells = []
        for a, b in zip(pts, pts[1:]):
            n = int(math.dist(a, b) / (P * 0.5)) + 1
            for i in range(n + 1):
                x = lerp(a[0], b[0], i / n)
                y = lerp(a[1], b[1], i / n)
                cells.append((int(x // P), int(y // P)))
        for c in cells:
            d = math.dist((c[0] * P, c[1] * P), IMP)
            waves[0 if d < 260 else 1 if d < 560 else 2].append(c)
    for k, cells in enumerate(waves):
        cells = sorted(set(cells))
        shadow = sorted(set((c + 1, r + 1) for c, r in cells) - set(cells))
        comp.layer(f"wave {k}", [pix_group(cells, P, (0, 0), ("slot", "primary"), "crack"),
                                 pix_group(shadow, P, (0, 0), ("slot", "outline"), "shadow")], parent=rig,
                   opacity=stepped(lambda t, k=k: 100 if t >= HIT + k * 2 else 0, 0, F, 1))
    # stepped vignette: concentric frames getting darker toward the edge
    frames = []
    for i in range(6):
        inset = i * 60
        op = [70, 50, 34, 22, 12, 6][i]
        pts_o = [(inset, inset), (W - inset, inset), (W - inset, H - inset), (inset, H - inset)]
        pts_i = [(inset + 60, inset + 60), (inset + 60, H - inset - 60), (W - inset - 60, H - inset - 60), (W - inset - 60, inset + 60)]
        frames.append(group([poly(pts_o), poly(pts_i), fill("#000000", op)], f"band{i}"))
    comp.layer("vignette", frames, opacity=stepped(lambda t: min(100, max(0, (t - HIT) // 3 * 25)), 0, F, 3))
    comp.layer("desaturate", [group([rect((W, H), (W / 2, H / 2)), fill(slot="background")], "g")],
               opacity=stepped(lambda t: min(50, max(0, (t - HIT) // 3 * 10)), 0, F, 3))
    comp.layer("flash", [group([rect((W, H), (W / 2, H / 2)), fill("#FFFFFF")], "f")], ip=HIT, op=HIT + 4,
               opacity=stepped(lambda t: 60 if t < HIT + 2 else 25, HIT, HIT + 4, 1))
    return comp


# ---------------------------------------------------------------- grim

def grim():
    comp = Comp("defeat-screen-crack--grim", W, H, frames=F)
    comp.slot("primary", "#B3121F")
    comp.slot("background", "#1A0C10")
    comp.slot("secondary", "#000000")
    rig = comp.null("rig", position=shake(12))
    lines = crack_lines(seed=11, n=15, jitter=26)
    items = []
    for k, (pts, frac, br) in enumerate(lines):
        w = 3.5 if br else 6
        items.append(group([polyline(pts), draw_on(HIT, frac, 10), stroke("#140608", width=w, join="miter", cap="butt")], f"c{k}"))
        items.append(group([polyline(pts), draw_on(HIT, frac, 10), stroke(slot="primary", width=w + 8, opacity=55, join="miter",
                                                                          cap="butt")], f"g{k}"))
    comp.layer("cracks", items, parent=rig)
    comp.layer("ember", [glow(420, "#FF3B2F", 0.8)], position=IMP, ip=HIT,
               scale=anim([(HIT, [20, 20], SNAP_OUT), (HIT + 8, [100, 100], EASE_OUT), (F, [70, 70])]),
               opacity=anim([(HIT, 100, EASE_OUT), (F, 35)]))
    # black band behind the text, sliding open
    band_h = 230
    comp.layer("band edge", [group([rect((W, 3), (W / 2, TA[1] + TA[3] / 2 - band_h / 2)), rect((W, 3), (W / 2, TA[1] + TA[3] / 2 + band_h / 2)),
                                    fill(slot="primary", opacity=80)], "e")],
               scale=anim([(14, [0, 100], SNAP_OUT), (40, [100, 100])]), anchor=(W / 2, 0), position=(W / 2, 0))
    comp.layer("band", [group([rect((W, band_h), (W / 2, TA[1] + TA[3] / 2)),
                               gradient_fill([(0, "#000000", 0), (0.2, "#000000", 0.85), (0.8, "#000000", 0.85), (1, "#000000", 0)],
                                             (0, TA[1] + TA[3] / 2 - band_h / 2), (0, TA[1] + TA[3] / 2 + band_h / 2))], "b")],
               opacity=anim([(10, 0, EASE_OUT), (34, 100)]))
    overlay(comp, grey_op=40, vig="#140306", vig_op=0.92, dur=30, tint=("#5A0A12", 22))
    return comp


build_asset(CAT, "defeat-screen-crack", "Defeat Screen Crack",
            "Full-frame game-over overlay: the screen cracks from an impact point, shards fall away and a dark, "
            "desaturating vignette closes in. Put \"Defeat\" or your message in the centre.",
            ["defeat", "game over", "crack", "broken", "screen", "lose", "gaming", "overlay"], [
    Variant("glass", "Glass", glass(), "intro-hold", thumb_t=0.6, bg="7a8a9a", text_area=TA,
            description="White cracked-glass lines with a red-edged vignette and falling glass shards."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.6, bg="7a8a9a", text_area=TA,
            description="8-bit cracks that spread in three stepped waves with blocky falling shards and a banded vignette."),
    Variant("grim", "Grim", grim(), "intro-hold", thumb_t=0.8, bg="7a8a9a", text_area=TA,
            description="Dark cracks with a smouldering red glow, a blood-tinted vignette and a black band for the text."),
])
