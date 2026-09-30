import random

from _gaming2 import *

W, H, F = 420, 760, 60
CX, GY = W / 2, 650          # beam centre x, ground y
TOP = 20


def beam_matte(comp, top=TOP, bottom=GY + 10, name="beam matte"):
    comp.layer(name, [group([rect((W, bottom - top), (CX, (top + bottom) / 2)),
                             gradient_fill([(0, "#FFFFFF", 0), (0.45, "#FFFFFF", 0.55), (0.9, "#FFFFFF", 1), (1, "#FFFFFF", 1)],
                                           (0, top), (0, bottom))], "m")])


def wobble(a, k=1, ph=0.0):
    return lambda t: a * math.sin(TAU * (k * t / F + ph))


def rising(comp, n, shapes, seed, x_spread, y0, rise, life_rng=(26, 44), sway=0, hold=False, step=1, spin=False):
    rng = random.Random(seed)
    for i in range(n):
        t0 = rng.uniform(0, F)
        life = rng.randint(*life_rng)
        x = CX + rng.uniform(-x_spread, x_spread)
        y = y0 + rng.uniform(-10, 10)
        r = rise * rng.uniform(0.6, 1.0)
        s = rng.uniform(55, 110)
        ph = rng.uniform(0, TAU)

        def fn(u, x=x, y=y, r=r, s=s, life=life, ph=ph):
            k = u / life
            px = x + sway * math.sin(ph + k * TAU * 0.8) * (1 - 0.5 * k)
            py = y - r * ease_out(k, 1.6)
            if hold:
                px, py = snap(px, 6), snap(py, 6)
            sc = s * (1 - k) if not hold else s
            d = {"position": [px, py], "scale": [sc, sc], "opacity": 100 * bump(k, 0, 1) ** 0.5}
            if spin:
                d["rotation"] = 180 * k
            return d
        particle(comp, f"mote {i}", shapes, round(t0), life, F, fn, step=step, hold=hold)


def rings(comp, n, slot, w0, w1, stroke_w, ratio=0.3, y=GY, name="ring"):
    for k in range(n):
        t0 = k * F / n

        def fn(u):
            e = ease_out(u / F, 2)
            d = lerp(w0, w1, e)
            return {"scale": [d, d], "opacity": 100 * (1 - u / F) ** 1.5}
        particle(comp, name, [group([ellipse((100, 100 * ratio)), stroke(slot=slot, width=stroke_w * 60 / w0)], "r")],
                 round(t0), F, F, fn, step=3, position=(CX, y))


# ---------------------------------------------------------------- modern (legendary)

def modern():
    comp = Comp("loot-beam", W, H, frames=F)
    comp.slot("primary", "#FFA126")
    comp.slot("secondary", "#FFE7A8")
    rising(comp, 22, [group([spark(15), fill(slot="secondary")], "s"), glow(30, "#FFE7A8", 0.5)], 3, 44, GY - 20, 500, sway=12)
    rising(comp, 10, [group([rect((3, 22), (0, 0), 1.5), fill("#FFFFFF", 80)], "s")], 8, 26, GY - 40, 560,
           life_rng=(16, 26))
    # beam
    beam_matte(comp)
    comp.layer("beam", [
        group([rect((10, GY - TOP), (0, 0), 5), fill("#FFFFFF")], "core",
              scale=loop(F, [[100, 100], [70, 100], [110, 100], [85, 100]])),
        group([rect((34, GY - TOP), (0, 0), 0), fill(slot="secondary", opacity=85)], "mid",
              scale=loop(F, [[100, 100], [118, 100], [92, 100], [110, 100]])),
        group([rect((80, GY - TOP), (0, 0), 0), fill(slot="primary", opacity=55)], "outer",
              scale=loop(F, [[100, 100], [88, 100], [112, 100], [95, 100]])),
        group([rect((170, GY - TOP), (0, 0), 0), fill(slot="primary", opacity=18)], "haze",
              scale=loop(F, [[100, 100], [115, 100]])),
    ], matte="alpha", position=(CX, (TOP + GY) / 2))
    # ground
    comp.layer("flare", [glow(120, "#FFFFFF", 0.9), group([ellipse((260, 8)), gradient_fill([(0, "#FFFFFF", 1), (1, "#FFFFFF", 0)], (0, 0), (130, 0), radial=True)], "streak")],
               position=(CX, GY), scale=loop(F, [[100, 100], [120, 120], [90, 90], [112, 112]]))
    rings(comp, 3, "primary", 60, 330, 4)
    comp.layer("pool", [glow(300, "#FFA126", 0.7, name="pool")], position=(CX, GY), scale=(100, 30))
    comp.layer("pool ring", [group([ellipse((160, 48)), stroke(slot="secondary", width=3, opacity=80)], "r"),
                             group([ellipse((220, 66)), stroke(slot="primary", width=2, opacity=50)], "r2")],
               position=(CX, GY), opacity=loop(F, [100, 60]))
    return comp


# ---------------------------------------------------------------- pixel

def pixel():
    comp = Comp("loot-beam--pixel", W, H, frames=F)
    comp.slot("primary", "#3FA9FF")
    comp.slot("secondary", "#C8F0FF")
    P = 8
    rising(comp, 22, [box(-6, -6, 12, 12, slot="secondary")], 4, 48, GY - 16, 520, hold=True, step=3, sway=12)
    rising(comp, 10, [box(-6, -6, 12, 12, "#FFFFFF")], 9, 20, GY - 16, 560, hold=True, step=3)
    # stepped beam: stacked columns with a dithered top
    H_ = GY - TOP
    cols = [(0, 16, "#FFFFFF", 100), (0, 40, ("slot", "secondary"), 100), (0, 72, ("slot", "primary"), 100),
            (0, 104, ("slot", "primary"), 45)]
    shapes = []
    for i, (_, w, col, op) in enumerate(cols):
        f = fill(col, op) if isinstance(col, str) else fill(slot=col[1], opacity=op)
        # the column breaks into dashes toward the top
        parts = [rect((w, H_ * 0.62), (0, H_ * 0.19))]
        y = -H_ * 0.12
        size = 48
        while y > -H_ / 2 + 10:
            parts.append(rect((w, size), (0, y - size / 2)))
            y -= size + 16 + (40 - size)
            size = max(8, size - 8)
        shapes.append(group(parts + [f], f"col{i}"))
    comp.layer("beam", shapes, position=(CX, (TOP + GY) / 2),
               scale=stepped(lambda t: [[100, 100], [112, 100], [100, 100], [88, 100]][int(t // 5) % 4], 0, F, 5),
               opacity=100)
    # scrolling highlight dashes inside the beam
    for k in range(4):
        comp.layer("dash", [box(-4, -12, 8, 24, "#FFFFFF")],
                   position=stepped(lambda t, k=k: [CX, GY - 40 - ((t / F + k / 4) % 1) * 420], 0, F, 3),
                   opacity=stepped(lambda t, k=k: 100 if ((t / F + k / 4) % 1) < 0.85 else 0, 0, F, 3))
    # pixel ground ring: dithered ellipse
    ring_cells = []
    rx, ry = 11, 3.2
    for r in range(-5, 6):
        for c in range(-14, 15):
            d = (c / rx) ** 2 + (r / ry) ** 2
            if 0.7 <= d <= 1.25:
                ring_cells.append((c + 14, r + 5))
    inner = [(c + 14, r + 5) for r in range(-5, 6) for c in range(-14, 15) if (c / (rx - 2.5)) ** 2 + (r / (ry - 1)) ** 2 < 1]
    origin = (-14.5 * P, -5.5 * P)
    comp.layer("ground", [pix_group(ring_cells, P, origin, ("slot", "secondary"), "ring"),
                          pix_group(inner, P, origin, ("slot", "primary", 60), "pool")],
               position=(CX, GY), scale=stepped(lambda t: [[100, 100], [110, 110]][int(t // 10) % 2], 0, F, 10))
    comp.layer("ground outer", [pix_group(ring_cells, P, origin, ("slot", "primary"), "ring")],
               position=(CX, GY), scale=stepped(lambda t: [100 + 50 * ((t % 30) // 6) / 4] * 2, 0, F, 6),
               opacity=stepped(lambda t: 100 - 90 * ((t % 30) // 6) / 4, 0, F, 6))
    return comp


# ---------------------------------------------------------------- fantasy (epic)

def fantasy():
    comp = Comp("loot-beam--fantasy", W, H, frames=F)
    comp.slot("primary", "#A35BFF")
    comp.slot("secondary", "#F1DBFF")
    comp.slot("accent", GOLD)
    # swirling sparkles spiralling up the beam
    rng = random.Random(12)
    for i in range(14):
        t0 = i * F / 14
        life = F
        ph = rng.uniform(0, TAU)
        s = rng.uniform(60, 110)

        def fn(u, ph=ph, s=s):
            k = u / life
            a = ph + k * TAU * 1.5
            x = CX + math.sin(a) * (58 - 30 * k)
            y = GY - 20 - k * 560
            front = math.cos(a)
            return {"position": [x, y], "scale": [s * (0.7 + 0.3 * front) * (1 - 0.5 * k)] * 2,
                    "opacity": 100 * bump(k, 0, 1) ** 0.6}
        particle(comp, "swirl", [group([spark(15), fill(slot="secondary")], "s"), glow(36, "#E6C8FF", 0.6)],
                 round(t0), life, F, fn, step=2)
    beam_matte(comp)
    comp.layer("beam", [
        group([rect((12, GY - TOP), (0, 0), 6), fill("#FFFFFF")], "core"),
        group([rect((40, GY - TOP), (0, 0), 0), fill(slot="secondary", opacity=70)], "mid",
              scale=loop(F, [[100, 100], [120, 100], [95, 100]])),
        group([rect((96, GY - TOP), (0, 0), 0), fill(slot="primary", opacity=55)], "outer",
              scale=loop(F, [[100, 100], [86, 100], [110, 100]])),
        group([rect((190, GY - TOP), (0, 0), 0), fill(slot="primary", opacity=16)], "haze"),
    ], matte="alpha", position=(CX, (TOP + GY) / 2))
    comp.layer("flare", [glow(140, "#FFFFFF", 0.85)], position=(CX, GY),
                         scale=loop(F, [[100, 100], [125, 125], [95, 95]]))
    # rune circle on the ground (squashed for perspective)
    rc = comp.null("rune circle", position=(CX, GY), scale=(100, 32))
    runes = []
    for k in range(12):
        a = k * 30
        p = pt(118, a)
        # abstract rune marks: small tick + diamond pairs (no letters)
        runes.append(group([ngon(4, 6, 0, p) if k % 2 else seg(pt(110, a), pt(126, a))], f"rune{k}"))
    comp.layer("runes", [group(runes + [stroke(slot="accent", width=4), fill(slot="accent")], "runes")], parent=rc,
               rotation=sampled(lambda t: t * 360 / F / 2, 0, F, 3), opacity=loop(F, [100, 70]))
    comp.layer("circle", [
        group([ellipse((280, 280)), stroke(slot="accent", width=5)], "outer"),
        group([ellipse((212, 212)), stroke(slot="accent", width=3)], "inner"),
        group([star(6, 104, 60), stroke(slot="primary", width=4, join="miter")], "hex"),
        group([ellipse((280, 280)), fill(slot="primary", opacity=28)], "pool"),
    ], parent=rc, rotation=sampled(lambda t: -t * 360 / F / 2, 0, F, 3))
    comp.layer("pool glow", [glow(380, "#A35BFF", 0.7)], position=(CX, GY), scale=(100, 32))
    return comp


build_asset(CAT, "loot-beam", "Loot Beam",
            "Rarity light pillar shooting up from the ground with a glowing pool, rings and rising sparkles, "
            "on a loop. Place it over a dropped item in your footage.",
            ["loot", "beam", "drop", "rarity", "legendary", "item", "gaming", "light"], [
    Variant("modern", "Legendary", modern(), "loop", thumb_t=0.3,
            description="Smooth orange legendary beam with a flare, ground rings and rising sparks."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.3, bg="1c1c22",
            description="8-bit stepped beam that breaks into dashes, with pixel motes and a dithered ground ring."),
    Variant("fantasy", "Epic Rune", fantasy(), "loop", thumb_t=0.3,
            description="Purple epic beam over a rotating golden rune circle, with sparkles spiralling up."),
])
