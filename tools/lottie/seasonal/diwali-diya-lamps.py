"""Diwali diya lamps: clay oil lamps with flickering flames and rangoli-inspired motifs (seamless loops)."""

from _common import *

T = 60
CLAY, CLAY_DK = "#C9562B", "#8E3417"
MAGENTA, ORANGE, YELLOW, TEAL = "#E0287A", "#FF8A1F", "#FFC93C", "#16A99A"
BOWL = "M -66 -6 C -62 30 -30 46 4 46 C 42 46 66 26 78 -16 C 52 -2 -30 2 -66 -6 Z"
OIL = "M -66 -6 C -42 -20 40 -24 78 -16 C 52 -4 -30 2 -66 -6 Z"
FOOT = "M -26 40 L 30 40 L 24 54 L -20 54 Z"
WICK = (66, -18)


def diya_items(style="clay", ink=None):
    """Shape items for one diya centred on the bowl; flame goes at WICK (added separately)."""
    if style == "brass":
        body_paint = [gradient_fill([(0, "#FFF0B0"), (0.35, "#E8B347"), (0.75, "#A8701C"), (1, "#6E4410")],
                                    (-40, -10), (40, 50))]
        rim_col = "#5A3508"
        deco_col = "#FFF3C4"
    else:
        body_paint = [fill(CLAY, slot="primary")]
        rim_col = "#4A1A08"
        deco_col = YELLOW
    items = []
    # painted band: dots and little petals along the belly
    dots = [ellipse((6, 6), (x, 22 + 0.004 * x * x)) for x in range(-44, 60, 13)]
    petals = []
    for x in (-32, 4, 40):
        for a in (0, 72, 144, 216, 288):
            p = rot((0, -5), a)
            petals.append(ellipse((6, 6), (x + p[0], 8 + p[1] + 0.004 * x * x)))
    items.append(group(dots + [fill(WHITE if style != "brass" else deco_col, slot="secondary"
                                    if style != "brass" else None)], "dots"))
    items.append(group(petals + [fill(deco_col, slot="accent" if style != "brass" else None)], "petals"))
    items.append(group(S(OIL) + [fill("#E9A93B" if style != "brass" else "#FFD86A")], "oil"))
    items.append(group(S(OIL) + [stroke(rim_col, 3)], "rim"))
    if style != "brass":
        items.append(group(S(BOWL) + [gradient_fill([(0, WHITE, 0.22), (0.45, WHITE, 0), (1, "#000000", 0.35)],
                                                     (-30, -6), (40, 46))], "shade"))
    items.append(group(S(BOWL) + body_paint, "bowl"))
    items.append(group(S(FOOT) + ([fill(CLAY_DK)] if style != "brass" else [fill("#8A5A14")]), "foot"))
    return items


def diya(comp, name, pos, seed, style="clay", scale=100, halo=True, flame_h=58):
    n = comp.null(name, position=pos, scale=(scale, scale))
    flame_layers(comp, name + "-flame", T, h=flame_h, w=15, seed=seed, parent=n, position=WICK,
                 halo_r=110 if style == "brass" else 80, halo_opacity=70 if style == "brass" else 55)
    comp.layer(name + "-body", diya_items(style), parent=n)
    return n


def flower(r, n, col, slot, petal=(0.55, 0.3), rot0=0, opacity=100):
    items = []
    for i in range(n):
        a = rot0 + 360 * i / n
        items.append(group([ellipse((r * petal[0], r * petal[1] * 2))], f"p{i}", rotation=a,
                           position=rot((0, -r * 0.62), a)))
    return group(items + [fill(col, opacity, slot=slot)], "flower")


def classic():
    W, H = 1040, 380
    comp = Comp("diwali-diya-lamps", W, H, frames=T)
    comp.slot("primary", CLAY)
    comp.slot("secondary", WHITE)
    comp.slot("accent", YELLOW)
    comp.slot("icon", MAGENTA)
    xs = [W / 2 + (i - 2) * 200 for i in range(5)]
    for i, x in enumerate(xs):
        diya(comp, f"diya{i}", (x, 220), seed=i * 5 + 2)
    # rangoli border: alternating flowers and dotted arcs, twinkling
    for i in range(6):
        x = W / 2 + (i - 2.5) * 200
        comp.layer(f"motif{i}", [
            group([ellipse((10, 10)), fill(YELLOW, slot="accent")], "c"),
            flower(34, 8, MAGENTA, "icon"),
            group([ellipse((d, d), rot((0, -32), a)) for a, d in zip(range(0, 360, 30), [6] * 12)] +
                  [fill(ORANGE)], "ring", rotation=15),
        ], position=(x, 318), rotation=looped(lambda t, i=i: 360 / 8 * t / T * (1 if i % 2 else -1), T, 2),
            scale=looped(lambda t, i=i: [100 + 6 * wave(t, T, 1, i * 0.17)] * 2, T, 3))
    for i in range(5):
        x = xs[i]
        comp.layer(f"arc{i}", [group([ellipse((7, 7), (math.cos(math.radians(a)) * 60, 318 - 290 + 290 +
                                                       math.sin(math.radians(a)) * 20 - 318 + 18))
                                      for a in range(20, 161, 20)] + [fill(TEAL)], "arc")],
                   position=(x, 318), opacity=looped(lambda t, i=i: 70 + 30 * wave(t, T, 1, i * 0.2), T, 3))
    return comp


def rangoli():
    W = H = 720
    comp = Comp("diwali-diya-lamps--rangoli", W, H, frames=T * 2)
    TT = T * 2
    comp.slot("primary", CLAY)
    comp.slot("secondary", MAGENTA)
    comp.slot("accent", YELLOW)
    comp.slot("icon", TEAL)
    c = (W / 2, H / 2 + 20)
    n = diya(comp, "diya", (c[0] - 10, c[1] - 10), seed=3, scale=165)
    rings = [
        (flower(120, 8, YELLOW, "accent", (0.34, 0.33)), 45, 0.6),
        (flower(170, 16, MAGENTA, "secondary", (0.24, 0.3)), -22.5, 0.0),
        (group(dots_ring(220, 32, 10, WHITE), "dots"), 11.25, 0.3),
        (flower(262, 24, TEAL, "icon", (0.18, 0.24)), 15, 0.8),
        (group(dots_ring(300, 48, 9, ORANGE), "dots2"), -7.5, 0.5),
    ]
    for j, (g, deg, ph) in enumerate(rings):
        comp.layer(f"ring{j}", [g], position=c, rotation=anim([(0, 0, LINEAR), (TT, deg)]),
                   scale=looped(lambda t, ph=ph: [100 + 2.5 * wave(t, TT, 2, ph)] * 2, TT, 3))
    comp.layer("base", [ellipse((300, 300)), fill(ORANGE, 90)], position=c)
    comp.layer("base2", [ellipse((250, 250)), fill("#7A1E4A", 100)], position=c)
    return comp


def glow_row():
    W, H = 880, 420
    comp = Comp("diwali-diya-lamps--glow", W, H, frames=T * 2)
    TT = T * 2
    comp.slot("primary", "#FFD27A")
    for i, x in enumerate((W / 2 - 250, W / 2, W / 2 + 250)):
        diya(comp, f"diya{i}", (x, 270 - (20 if i == 1 else 0)), seed=i * 9 + 4, style="brass",
             scale=150 if i == 1 else 125, flame_h=58)
    r = rng(1)
    for j in range(16):
        x = r.uniform(80, W - 80)
        t0 = r.uniform(0, TT)
        life = r.uniform(50, 80)

        def fn(u, x=x, life=life):
            k = u / life
            return {"position": (x + 20 * math.sin(k * 6), 300 - 260 * k),
                    "opacity": 100 * bump(k, 0, 1), "scale": [lerp(100, 40, k)] * 2}
        particle(comp, f"spark{j}", [ellipse((6, 6)), fill("#FFE9A8", slot="primary"), glow(12, "#FFC24A", 90)],
                 t0, life, TT, fn, step=3)
    comp.layer("floor-glow", [glow(420, "#FFB347", 100, falloff=((0, 0.35), (0.6, 0.12), (1, 0)), sy=0.3)],
               position=(W / 2, 330), opacity=looped(lambda t: 70 + 20 * flicker(t, TT, 3), TT, 3))
    return comp


build("diwali-diya-lamps", "Diwali Diya Lamps",
      "Clay diya oil lamps with gently flickering flames for Diwali greetings, with rangoli-inspired "
      "flower and dot motifs; seamless loops.",
      ["diwali", "deepavali", "diya", "lamp", "rangoli", "festival of lights", "flame"], [
          Variant("classic", "Diya Row", classic(), "loop", thumb_t=0.3, region=(220, 90, 600, 300),
                  description="A row of five painted terracotta diyas above a turning rangoli flower border."),
          Variant("rangoli", "Rangoli", rangoli(), "loop", thumb_t=0.3,
                  description="One diya at the centre of a circular rangoli of petal and dot rings slowly turning."),
          Variant("glow", "Golden Glow", glow_row(), "loop", thumb_t=0.4,
                  description="Three polished brass diyas with a strong warm bloom and sparks drifting up."),
      ])
