import random

from _gaming2 import *

W, H, F = 620, 620, 66
CX, CY = W / 2, 262
LAND = 11
BY = 478                      # banner centre
BW, BHt = 380, 74
TA = (CX - 150, BY - 26, 300, 52)
CONF_COLORS = ["#FFD23F", "#FF4D7A", "#35E0FF", "#7CFF6B", "#B98CFF", "#FFFFFF"]

CROWN = [(-118, 58), (-132, -58), (-66, -2), (0, -88), (66, -2), (132, -58), (118, 58)]


def slam_keys():
    """Crown drops in, squashes on landing and springs back."""
    pos = anim([(0, [CX, CY - 330], EASE_IN), (LAND, [CX, CY + 10], EASE_OUT), (LAND + 4, [CX, CY - 12], EASE_IN_OUT),
                (LAND + 10, [CX, CY], HOLD), (F, [CX, CY])])
    scale = anim([(0, [80, 120], EASE_IN), (LAND, [100, 100], LINEAR), (LAND + 2, [122, 78], EASE_OUT),
                  (LAND + 7, [92, 108], EASE_IN_OUT), (LAND + 12, [102, 98], EASE_IN_OUT), (LAND + 16, [100, 100], HOLD),
                  (F, [100, 100])])
    op = anim([(0, 0, HOLD), (1, 100, HOLD), (F, 100)])
    return pos, scale, op


def rays(comp, slot, n=16, L=300, w=22, opacity=60, hold=False):
    rs = [group([poly([(0, -40), (-w * (1 if i % 2 == 0 else 0.6), -L * (1 if i % 2 == 0 else 0.75)),
                       (w * (1 if i % 2 == 0 else 0.6), -L * (1 if i % 2 == 0 else 0.75))])], f"ray{i}", rotation=i * 360 / n)
          for i in range(n)]
    comp.layer("rays falloff", [glow(2 * L, "#FFFFFF", 1.0, mid=0.4)], position=(CX, CY + 10),
               scale=anim([(LAND, [0, 0], SNAP_OUT), (LAND + 12, [100, 100])]), ip=LAND)
    rot = (stepped(lambda t: 15 * ((t - LAND) // 6), LAND, F, 6) if hold else anim([(LAND, 0, LINEAR), (F, 40)]))
    comp.layer("rays", [group(rs + [fill(slot=slot, opacity=opacity)], "rays")], matte="alpha", position=(CX, CY + 10),
               rotation=rot, scale=anim([(LAND, [0, 0], SNAP_OUT), (LAND + 12, [100, 100])]), ip=LAND)


def confetti(comp, n=30, seed=4, hold=False, shapes_fn=None):
    rng = random.Random(seed)
    for i in range(n):
        a = rng.uniform(-80, 80) + (0 if i % 3 else rng.choice((-1, 1)) * 30)
        v = rng.uniform(520, 900)
        vx, vy = math.sin(math.radians(a)) * v, -math.cos(math.radians(a)) * v
        g = 900
        life = rng.randint(34, 50)
        col = CONF_COLORS[i % len(CONF_COLORS)]
        w, h = rng.uniform(10, 16), rng.uniform(18, 28)
        spin = rng.uniform(300, 700) * rng.choice((-1, 1))
        flip = rng.uniform(3, 6)
        shapes = shapes_fn(col, i) if shapes_fn else [group([rect((w, h), (0, 0), 2), fill(col)], "c")]

        def fn(u, vx=vx, vy=vy, spin=spin, flip=flip, life=life):
            s = u / 30
            drag = 1 - math.exp(-2.2 * s)
            x = CX + vx * drag / 2.2
            y = CY + vy * drag / 2.2 + 0.5 * g * s * s * 0.6
            if hold:
                x, y = snap(x, 6), snap(y, 6)
            return {"position": [x, y], "rotation": spin * s if not hold else 90 * round(spin * s / 90),
                    "scale": [100 * abs(math.cos(flip * s)) if not hold else 100, 100],
                    "opacity": 100 * (1 - ease_in(u / life, 3))}
        particle(comp, "confetti", shapes, LAND + rng.randint(0, 3), life, F, fn, wrap=False, hold=hold,
                 step=2 if hold else 1)


def banner(comp, fill_slot, dark, t0=LAND + 8, edge=None, pixel=False):
    tail = [(-BW / 2 + 10, -BHt / 2 + 14), (-BW / 2 - 70, -BHt / 2 + 14), (-BW / 2 - 44, 14), (-BW / 2 - 70, BHt / 2 + 14),
            (-BW / 2 + 10, BHt / 2 + 14)]
    fold = [(-BW / 2, BHt / 2), (-BW / 2 + 10, BHt / 2 + 14), (-BW / 2 + 10, BHt / 2 - 2)]
    mirror = lambda pts: [(-x, y) for x, y in pts]
    shapes = []
    if edge:
        shapes.append(group([rect((BW - 16, BHt - 16), (0, 0))] + [stroke(edge, width=3, opacity=70)], "inner"))
    shapes += [
        group([rect((BW, BHt), (0, 0)), sheen(BW, BHt, 0.25, 0.25)], "sheen"),
        group([rect((BW, BHt), (0, 0)), fill(slot=fill_slot)], "front"),
        group([poly(fold), poly(mirror(fold)), fill(dark)], "folds"),
        group([poly(tail), poly(mirror(tail)), fill(slot=fill_slot)], "tails"),
        group([poly(tail), poly(mirror(tail)), fill("#000000", 30)], "tails shade"),
    ]
    sc = (stepped(lambda t: [0 if t < t0 else 60 if t < t0 + 2 else 110 if t < t0 + 4 else 100, 100], 0, F, 1) if pixel
          else anim([(t0, [0, 100], SPRING), (t0 + 12, [100, 100])]))
    comp.layer("banner", shapes, position=(CX, BY), scale=sc, ip=t0)


def shock(comp, slot, d0=200, d1=560, w=14):
    comp.layer("shock", [group([ellipse(anim([(LAND, [d0, d0 * 0.4], DECEL), (LAND + 18, [d1, d1 * 0.4])])),
                                stroke(slot=slot, width=anim([(LAND, w, EASE_OUT), (LAND + 18, 1)]))], "r")],
               position=(CX, CY + 70), ip=LAND, op=LAND + 19, opacity=anim([(LAND, 100, EASE_IN), (LAND + 18, 0)]))


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("victory-crown-burst", W, H, frames=F)
    comp.slot("primary", "#FFC21A")
    comp.slot("secondary", "#E0282E")
    comp.slot("accent", "#35A8FF")
    banner(comp, "secondary", "#7A0F14")
    pos, scale, op = slam_keys()
    crown = comp.null("crown", position=pos, scale=scale)
    band_gems = [group([ngon(4, 13, 0, (x, 62)), fill(slot="accent" if x else "secondary"), stroke("#FFFFFF", width=2, opacity=50)],
                       f"g{x}") for x in (-70, 0, 70)]
    comp.layer("crown", band_gems + [
        group([ellipse((20, 20), (-132, -66)), ellipse((22, 22), (0, -98)), ellipse((20, 20), (132, -66)), fill("#FFFFFF", 80)],
              "ball hi"),
        group([ellipse((28, 28), (-132, -62)), ellipse((30, 30), (0, -94)), ellipse((28, 28), (132, -62)), fill(slot="primary"),
               stroke("#A8650A", width=3)], "balls"),
        group([rect((250, 40), (0, 62), 6), sheen(250, 40, 0.35, 0.3)], "band sheen"),
        group([rect((250, 40), (0, 62), 6), fill(slot="primary"), stroke("#A8650A", width=4)], "band"),
        group([poly([(-40, -20), (0, -70), (0, 40), (-90, 40)]), fill("#FFFFFF", 22)], "shine"),
        group([poly(CROWN), fill(slot="primary"), stroke("#A8650A", width=4, join="round")], "body"),
        group([poly([(x, y + 12) for x, y in CROWN]), rect((250, 40), (0, 74), 6), fill("#000000", 25)], "shadow"),
    ], parent=crown)
    confetti(comp)
    shock(comp, "primary")
    comp.layer("impact", [glow(300, "#FFF3C4", 1)], position=(CX, CY + 40), ip=LAND, op=LAND + 16,
               scale=anim([(LAND, [30, 20], SNAP_OUT), (LAND + 8, [120, 70])]), opacity=anim([(LAND, 100, EASE_IN), (LAND + 15, 0)]))
    rays(comp, "primary")
    return comp


# ---------------------------------------------------------------- pixel

CROWN_PIX = [
    ".KK......KK......KK.",
    "KWRK....KWBK....KWRK",
    "KRRK....KBBK....KRRK",
    ".KK......KK......KK.",
    ".KYK....KYYK....KYK.",
    ".KYYK..KYYYYK..KYYK.",
    ".KYWYK.KYYYYK.KYYYK.",
    ".KYWYYKYYYYYYKYYYYK.",
    ".KYWYYYYYYYYYYYYYYK.",
    ".KYYYYYYYYYYYYYYYOK.",
    ".KKKKKKKKKKKKKKKKKK.",
    ".KYYRRYYYBBYYYRRYYK.",
    ".KYYRRYYYBBYYYRRYOK.",
    ".KOOOOOOOOOOOOOOOOK.",
    ".KKKKKKKKKKKKKKKKKK.",
]


def pixel():
    comp = Comp("victory-crown-burst--pixel", W, H, frames=F)
    comp.slot("primary", "#FFD23F")
    comp.slot("secondary", "#3F7CFF")
    comp.slot("accent", "#FF4D5E")
    comp.slot("outline", INK)
    P = 13
    banner(comp, "secondary", "#1A3570", pixel=True)
    # stepped slam
    ys = [CY - 320, CY - 220, CY - 110, CY + 10]
    pos = stepped(lambda t: [CX, ys[min(3, int(t // 3))] if t < LAND else CY + (8 if t < LAND + 2 else -8 if t < LAND + 4 else 0)],
                  0, F, 1)
    scale = stepped(lambda t: [100, 100] if t < LAND else [115, 85] if t < LAND + 3 else [95, 108] if t < LAND + 6 else [100, 100],
                    0, F, 1)
    comp.layer("crown", pix(CROWN_PIX, {"W": "#FFFFFF", "R": ("slot", "accent"), "B": ("slot", "secondary"),
                                        "O": ("#000000", 25), "Y": ("slot", "primary"), "K": ("slot", "outline")}, P,
                            order=list("WRBOYK")), position=pos, scale=scale)
    confetti(comp, n=26, hold=True, shapes_fn=lambda col, i: [box(-7, -7, 14, 14, col)])
    # pixel star burst: plus-shaped rays of squares
    for k in range(8):
        a = k * 45
        blocks = [box(*[v - 8 for v in pt(r, a)], 16, 16, "#FFFFFF" if k % 2 else ("#FFD23F")) for r in (170, 200, 230)]
        comp.layer("ray", blocks, position=(CX, CY + 10), ip=LAND, op=LAND + 18,
                   scale=stepped(lambda t: [70 + 15 * ((t - LAND) // 3)] * 2, LAND, LAND + 18, 3),
                   opacity=stepped(lambda t: 100 if (t - LAND) < 12 or (t - LAND) % 4 < 2 else 0, LAND, LAND + 18, 1))
    comp.layer("shock", [box(-200, -6, 400, 12, "#FFFFFF")], position=(CX, CY + 100), ip=LAND, op=LAND + 8,
               scale=stepped(lambda t: [60 + 30 * (t - LAND) // 2 * 1.0, 100], LAND, LAND + 8, 2))
    return comp


# ---------------------------------------------------------------- fantasy (laurel)

def leaf(L=46, w=16):
    return [path(bezier([(0, 0), (0, -L)], [(0, 0), (-w, L * 0.45)], [(-w, -L * 0.45), (0, 0)], True), "leafL"),
            path(bezier([(0, -L), (0, 0)], [(0, 0), (w, -L * 0.45)], [(w, L * 0.45), (0, 0)], True), "leafR")]


def fantasy():
    comp = Comp("victory-crown-burst--fantasy", W, H, frames=F)
    comp.slot("primary", GOLD)
    comp.slot("secondary", "#6B2FB8")
    comp.slot("accent", "#3FCB7A")
    banner(comp, "secondary", "#2E1156", edge=GOLD)
    pos, scale, op = slam_keys()
    crown = comp.null("crown", position=pos, scale=scale)
    # crown with trefoil tips
    tips = []
    for x, y, s in ((-128, -64, 0.8), (0, -96, 1.0), (128, -64, 0.8)):
        tips.append(group([ellipse((18 * s, 18 * s), (x, y - 14 * s)), ellipse((16 * s, 16 * s), (x - 13 * s, y)),
                           ellipse((16 * s, 16 * s), (x + 13 * s, y)), fill(slot="primary"), stroke(GOLD_D, width=3)], "tip"))
    arches = [group([arc(58, -70, 70, 20, (x, 30))], f"arch{x}") for x in (-62, 62)]
    comp.layer("crown", [
        group([ngon(4, 16, 0, (0, 62)), fill(slot="accent"), stroke(GOLD_L, width=2)], "gem c"),
        group([ellipse((20, 26), (-78, 62)), ellipse((20, 26), (78, 62)), fill(slot="secondary"), stroke(GOLD_L, width=2)], "gems"),
        group([ellipse((10, 10), (x, 62)) for x in (-40, 40, -110, 110)] + [fill("#FFFFFF", 85)], "pearls"),
        group([rect((256, 44), (0, 62), 8), sheen(256, 44, 0.45, 0.3)], "band sheen"),
        group([rect((256, 44), (0, 62), 8), fill(slot="primary"), stroke(GOLD_D, width=4)], "band"),
        group(arches + [stroke(GOLD_D, width=3)], "arches"),
        group([ngon(4, 12, 0, (0, -30)), fill(slot="secondary"), stroke(GOLD_L, width=2)], "body gem"),
    ] + tips + [
        group([poly(CROWN), sheen(260, 150, 0.4, 0.35)], "body sheen"),
        group([poly(CROWN), fill(slot="primary"), stroke(GOLD_D, width=4)], "body"),
    ], parent=crown)
    confetti(comp, n=28, seed=7, shapes_fn=lambda col, i: [group([spark(12 + (i % 3) * 3), fill(GOLD_L if i % 2 else "#FFFFFF")], "s")])
    # laurel wreath behind, unfurling
    leaves = []
    for side in (-1, 1):
        for k in range(8):
            a = 180 + side * (34 + k * 16)
            p = pt(190, a, (0, 20))
            leaves.append(group(leaf() + [fill(slot="accent"), stroke("#1E6B3E", width=2)], f"leaf{side}{k}", position=p,
                                rotation=a + side * 70, scale=anim([(LAND + 2 + k, [0, 0], SPRING), (LAND + 12 + k, [100, 100])])))
    stems = [group([arc(190, 150, 30, 30, (0, 20)), arc(190, 210, 330, 30, (0, 20)), trim(end=anim([(LAND, 0, SNAP_OUT), (LAND + 16, 100)])),
                    stroke("#1E6B3E", width=5)], "stems")]
    comp.layer("wreath", leaves + stems,
               position=(CX, CY + 20))
    shock(comp, "primary", w=10)
    rays(comp, "primary", n=24, L=290, w=12, opacity=50)
    return comp


build_asset(CAT, "victory-crown-burst", "Victory Crown Burst",
            "A crown slams down with light rays, a shockwave and a confetti burst, then a ribbon banner unfurls "
            "beneath it. Put your victory text on the banner.",
            ["victory", "crown", "winner", "win", "champion", "confetti", "gaming", "reward"], [
    Variant("modern", "Modern", modern(), "intro-hold", thumb_t=0.5, text_area=TA,
            description="Glossy gold crown with gems, spinning rays and colourful confetti over a red ribbon."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.5, bg="e8e8ee", text_area=TA,
            description="8-bit crown that drops in steps, with blocky star rays and square pixel confetti."),
    Variant("fantasy", "Royal", fantasy(), "intro-hold", thumb_t=0.5, text_area=TA,
            description="Ornate crown with trefoil tips and jewels, a laurel wreath unfurling behind it and golden sparkles."),
])
