import math
import random

from _gaming2 import *

W, H, F = 900, 170, 75
BY = 96                 # bar centre y
LVL = 44                # level-up moment
K = [(8, 0.32, EASE_IN_OUT), (LVL, 1.0, HOLD), (LVL + 8, 0.0, SNAP_OUT), (LVL + 26, 0.2, HOLD), (F, 0.2, HOLD)]


def frac_at(t):
    if t < K[0][0]:
        return K[0][1]
    for (t0, v0, e), (t1, v1, _) in zip(K, K[1:]):
        if t0 <= t <= t1:
            if e == HOLD:
                return v0 if t < t1 else v1
            u = (t - t0) / (t1 - t0)
            u = smooth(u) if e == EASE_IN_OUT else ease_out(u, 4)
            return lerp(v0, v1, u)
    return K[-1][1]


def edge_keys(x0, w, y):
    return anim([(t, [x0 + w * v, y], e) for t, v, e in K])


def trail(comp, x0, w, y, shapes, n=14, seed=3, hold=False, step=1, spread=10):
    rng = random.Random(seed)
    for i in range(n):
        t0 = rng.uniform(10, LVL - 4)
        life = rng.randint(10, 16)
        x = x0 + w * frac_at(t0)
        yy = y + rng.uniform(-spread, spread)
        dx, dy = -rng.uniform(20, 60), rng.uniform(-26, 14)
        s = rng.uniform(55, 100)

        def fn(u, x=x, yy=yy, dx=dx, dy=dy, s=s, life=life):
            k = u / life
            return {"position": [x + dx * ease_out(k), yy + dy * ease_out(k)],
                    "scale": [s * (1 - k), s * (1 - k)], "opacity": 100 * (1 - ease_in(k))}
        particle(comp, f"mote {i}", shapes, round(t0), life, F, fn, step=step, wrap=False, hold=hold)


def burst_sparks(comp, cx, cy, shapes, n=12, r0=20, r1=110, seed=5, t=LVL, hold=False, step=1, yscale=0.6):
    rng = random.Random(seed)
    for i in range(n):
        a = i * 360 / n + rng.uniform(-10, 10)
        r = rng.uniform(r1 * 0.6, r1)
        life = rng.randint(14, 20)
        p0 = pt(r0, a)
        p1 = pt(r, a)
        s = rng.uniform(60, 110)

        def fn(u, p0=p0, p1=p1, s=s, life=life):
            k = u / life
            e = ease_out(k)
            return {"position": [cx + lerp(p0[0], p1[0], e), cy + lerp(p0[1], p1[1], e) * yscale],
                    "scale": [s * (1 - ease_in(k)), s * (1 - ease_in(k))], "rotation": 90 * k}
        particle(comp, f"burst {i}", shapes, t + rng.randint(0, 2), life, F, fn, step=step, wrap=False,
                 hold=hold)


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("xp-bar-fill", W, H, frames=F)
    comp.slot("primary", CYAN)
    comp.slot("secondary", "#B8F5FF")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    BX, BW, BH, SK = 150, 720, 30, 16
    HX = 76
    rig = comp.null("rig", position=anim([(0, [-40, 0], SNAP_OUT), (14, [0, 0])]))

    # level-up flare
    comp.layer("hex ring", [group([ngon(6, 60, 30), stroke(slot="primary", width=anim([(LVL, 10, EASE_OUT), (LVL + 18, 1)]))], "r")],
               position=(HX, BY - 6), ip=LVL, op=LVL + 19, scale=anim([(LVL, [100, 100], DECEL), (LVL + 18, [190, 190])]),
               opacity=anim([(LVL, 100, EASE_IN), (LVL + 18, 0)]))
    burst_sparks(comp, BX + BW - 30, BY, [group([spark(12), fill(slot="secondary")], "s")], n=10, r1=90)
    # leading edge sparkle
    edge = comp.null("edge", position=edge_keys(BX, BW, BY), parent=rig)
    comp.layer("edge spark", [group([spark(10), fill("#FFFFFF")], "s2", rotation=45,
                                    scale=sampled(lambda t: [60 + 40 * math.sin(t * 0.7)] * 2, 0, F, 2)),
                              group([spark(24), fill("#FFFFFF")], "s"), glow(70, "#FFFFFF", 0.55)], parent=edge,
               ip=8, op=LVL + 2,
               scale=anim([(8, [0, 0], SPRING), (16, [100, 100], HOLD), (LVL - 2, [100, 100], EASE_OUT), (LVL + 2, [220, 220])]),
               opacity=anim([(LVL - 1, 100, EASE_OUT), (LVL + 2, 0)]))
    comp.layer("edge spark 2", [group([spark(12), fill("#FFFFFF")], "s"), glow(40, "#FFFFFF", 0.5)], parent=edge,
               ip=LVL + 10,
               scale=pop(LVL + 10, 10))
    trail(comp, BX, BW, BY, [group([spark(6), fill(slot="secondary")], "m")], spread=12)

    # badge
    badge = comp.null("badge", parent=rig, position=(HX, BY - 6),
                      scale=anim([(0, [0, 0], SPRING), (12, [100, 100], HOLD), (LVL, [100, 100], EASE_OUT),
                                  (LVL + 3, [118, 118], SPRING), (LVL + 16, [100, 100])]))
    comp.layer("badge flash", [group([ngon(6, 52, 30), fill("#FFFFFF")], "f")], parent=badge,
               opacity=anim([(LVL, 0, HOLD), (LVL + 1, 90, EASE_OUT), (LVL + 12, 0)]))
    comp.layer("badge", [
        group([ngon(6, 48, 30), stroke(slot="primary", width=3)], "inner rim"),
        group([ngon(6, 52, 30), sheen(100, 104, 0.18, 0.25)], "gloss"),
        group([ngon(6, 52, 30), fill(slot="background", opacity=92)], "plate"),
        group([ngon(6, 58, 30), fill(slot="primary")], "rim"),
        group([ngon(6, 60, 30, (0, 6)), fill("#000000", 30)], "shadow"),
    ], parent=badge)

    # bar
    comp.layer("ticks", [group([seg((BX + BW * i / 10 + SK / 2 - 0.1, BY - BH / 2), (BX + BW * i / 10 - SK / 2, BY + BH / 2))
                                for i in range(1, 10)] + [stroke(slot="background", width=3, opacity=70)], "t")], parent=rig,
               opacity=fade(0, 8))
    comp.layer("bar matte", [group([skew_rect(BW, BH, SK, (BX + BW / 2, BY)), fill()], "m")], parent=rig)
    comp.layer("bar fill", [
        group([rect((BW, BH), (BX + BW / 2, BY)), fill("#FFFFFF")], "flash",
              opacity=anim([(LVL - 1, 0, HOLD), (LVL, 100, HOLD), (LVL + 3, 100, EASE_OUT), (LVL + 14, 0)])),
        group([rect((BW, BH), (0, 0)), sheen(BW, BH, 0.4, 0.3)], "gloss", position=(BX + BW / 2, BY)),
        group([lbar(BX, BY - BH / 2, BW, BH, K), fill(slot="primary")], "fill"),
        group([lbar(BX, BY - BH / 2, BW, BH, [(t, min(v + 0.012, 1) if v else 0, e) for t, v, e in K]),
               fill(slot="secondary")], "edge"),
    ], parent=rig, matte="alpha", opacity=fade(0, 8))
    comp.layer("track", [
        group([skew_rect(BW, BH, SK, (BX + BW / 2, BY)), fill(slot="background", opacity=85)], "track"),
        group([skew_rect(BW + 10, BH + 10, SK + 1, (BX + BW / 2, BY)), stroke(slot="outline", width=2, opacity=45),
               fill("#000000", 35)], "rim"),
    ], parent=rig, opacity=fade(0, 8))
    comp.layer("label line", [group([seg((BX + 6, BY - 36), (BX + 150, BY - 36)), trim(end=anim([(6, 0, SNAP_OUT), (22, 100)])), stroke(slot="primary", width=3, cap="butt")], "l")], parent=rig)
    return comp


# ---------------------------------------------------------------- pixel

BADGE_PIX = [
    "...KKKKKKKK...",
    "..KYYYYYYYYK..",
    ".KYWYYYYYYYOK.",
    "KYWDDDDDDDDYOK",
    "KYYDDDDDDDDYOK",
    "KYYDDDDDDDDYOK",
    "KYYDDDDDDDDYOK",
    "KYYDDDDDDDDYOK",
    "KYYDDDDDDDDYOK",
    "KYYDDDDDDDDOOK",
    ".KYYYYYYYYOOK.",
    "..KOOOOOOOOK..",
    "...KKKKKKKK...",
]
SPARK_PIX = [
    "...W...",
    "...W...",
    "..WYW..",
    "WWYWYWW",
    "..WYW..",
    "...W...",
    "...W...",
]
SPARK_PIX2 = [
    ".......",
    "...W...",
    "..WYW..",
    ".WYWYW.",
    "..WYW..",
    "...W...",
    ".......",
]


def pixel():
    comp = Comp("xp-bar-fill--pixel", W, H, frames=F)
    comp.slot("primary", "#3CD66A")
    comp.slot("secondary", "#FFD23F")
    comp.slot("outline", INK)
    comp.slot("background", "#2B2140")
    PX = 6
    HX = 74
    N = 20
    SW = 34                     # segment pitch
    BX = 160
    BW = N * SW
    BH = 36
    # badge
    badge = comp.null("badge", position=(HX, BY - 6), scale=stepped(
        lambda t: [(0 if t < 2 else 60 if t < 4 else 115 if t < 6 else 100)] * 2 if t < LVL else
        ([130, 130] if LVL <= t < LVL + 4 else [100, 100]), 0, F, 2))
    comp.layer("badge flash", pix(BADGE_PIX, {"W": "#FFFFFF", "Y": "#FFFFFF", "O": "#FFFFFF", "D": "#FFFFFF", "K": "#FFFFFF"},
                                  PX, order=list("WYODK"), name="f"), parent=badge,
               opacity=stepped(lambda t: 100 if LVL <= t < LVL + 10 and (t - LVL) % 4 < 2 else 0, 0, F, 1))
    comp.layer("badge", pix(BADGE_PIX, {"W": ("#FFFFFF", 80), "O": ("#000000", 30), "Y": ("slot", "secondary"),
                                        "D": ("slot", "background"), "K": ("slot", "outline")},
                            PX, order=list("WOYDK"), name="b"), parent=badge)

    # frame
    fr = [box(BX - 6, BY - BH / 2 - 6, BW + 12, 6, slot="outline"), box(BX - 6, BY + BH / 2, BW + 12, 6, slot="outline"),
          box(BX - 12, BY - BH / 2, 6, BH, slot="outline"), box(BX + BW + 6, BY - BH / 2, 6, BH, slot="outline"),
          box(BX - 6, BY - BH / 2, 6, BH, "#FFFFFF", opacity=90), box(BX + BW, BY - BH / 2, 6, BH, "#FFFFFF", opacity=90),
          box(BX, BY - BH / 2, BW, 4, "#FFFFFF", opacity=90), box(BX, BY + BH / 2 - 4, BW, 4, "#FFFFFF", opacity=90),
          box(BX, BY - BH / 2, BW, BH, slot="background"),
          box(BX - 6, BY - BH / 2, BW + 12, BH + 12, "#000000", opacity=35)]
    # spark following the edge (stepped), two sprite frames
    edge_pos = stepped(lambda t: [BX + BW * frac_at(t), BY], 8, F, 2)
    for k, spr in enumerate((SPARK_PIX, SPARK_PIX2)):
        comp.layer(f"spark {k}", pix(spr, {"W": "#FFFFFF", "Y": ("slot", "secondary")}, PX, order=list("YW")),
                   position=edge_pos, ip=10, op=LVL + 2,
                   opacity=stepped(lambda t, k=k: 100 if (t // 4) % 2 == k else 0, 0, F, 2))
    trail(comp, BX, BW, BY, [box(-4, -4, 8, 8, slot="secondary")], hold=True, step=2, spread=14)
    burst_sparks(comp, BX + BW - 40, BY, [box(-5, -5, 10, 10, slot="secondary"), box(-8, -8, 16, 16, "#FFFFFF")], n=12,
                 r1=100, hold=True, step=2)
    burst_sparks(comp, HX, BY - 6, pix(SPARK_PIX2, {"W": "#FFFFFF", "Y": ("slot", "secondary")}, 4, order=list("YW")),
                 n=8, r0=50, r1=95, seed=9, hold=True, step=2, yscale=1.0)
    # segments

    for i in range(N):
        x = BX + i * SW + SW / 2
        on = lambda t, i=i: t >= 4 and (i + 1) / N <= frac_at(t) + 0.5 / N
        comp.layer(f"flash {i}", [box(x - SW / 2 + 4, BY - BH / 2 + 4, SW - 8, BH - 8, "#FFFFFF")],
                   opacity=stepped(lambda t, i=i: 100 if LVL <= t < LVL + 10 and ((t - LVL) // 2 + i) % 2 == 0 else 0,
                                   0, F, 1))
        comp.layer(f"seg {i}", [
            box(x - SW / 2 + 4, BY - BH / 2 + 4, SW - 8, 6, "#FFFFFF", opacity=45, name="hi"),
            box(x - SW / 2 + 4, BY + BH / 2 - 10, SW - 8, 6, "#000000", opacity=25, name="lo"),
            box(x - SW / 2 + 4, BY - BH / 2 + 4, SW - 8, BH - 8, slot="primary", name="seg"),
        ], opacity=stepped(lambda t, on=on: 100 if on(t) else 0, 0, F, 1))
    comp.layer("frame", [group(fr, "frame")], opacity=stepped(lambda t: 0 if t < 2 else 100, 0, 4, 2))
    # label underline dashes
    comp.layer("label", [box(BX + i * 18, BY - BH / 2 - 26, 10, 6, slot="secondary") for i in range(6)],
               opacity=stepped(lambda t: 0 if t < 6 else 100, 0, 8, 2))
    return comp


# ---------------------------------------------------------------- fantasy

def fantasy():
    comp = Comp("xp-bar-fill--fantasy", W, H, frames=F)
    comp.slot("primary", PURPLE)
    comp.slot("secondary", GOLD)
    comp.slot("background", "#1B1030")
    comp.slot("accent", "#E7D2FF")
    BX, BW, BH = 160, 680, 26
    MX, MR = 78, 56
    rig = comp.null("rig", opacity=fade(0, 10))

    # rays from medallion at level up
    rays = [group([poly([(0, -MR - 4), (-9, -MR - 60), (9, -MR - 60)])], f"ray{i}", rotation=i * 30) for i in range(12)]
    comp.layer("rays", [group(rays + [fill(slot="secondary", opacity=80)], "rays")], position=(MX, BY - 8), ip=LVL,
               op=LVL + 24, rotation=anim([(LVL, -10, EASE_OUT), (LVL + 24, 30)]),
               scale=anim([(LVL, [40, 40], SNAP_OUT), (LVL + 12, [110, 110], EASE_OUT), (LVL + 24, [120, 120])]),
               opacity=anim([(LVL, 100, HOLD), (LVL + 10, 100, EASE_IN), (LVL + 24, 0)]))
    comp.layer("ring", [group([ellipse((MR * 2, MR * 2)), stroke(slot="secondary", width=anim([(LVL, 8, EASE_OUT), (LVL + 20, 1)]))], "r")],
               position=(MX, BY - 8), ip=LVL, op=LVL + 21,
               scale=anim([(LVL, [100, 100], DECEL), (LVL + 20, [200, 200])]), opacity=anim([(LVL, 100, EASE_IN), (LVL + 20, 0)]))
    burst_sparks(comp, BX + BW - 20, BY, [group([spark(13), fill(slot="accent")], "s")], n=10, r1=90, seed=11)

    edge = comp.null("edge", position=edge_keys(BX, BW, BY), parent=rig)
    comp.layer("edge star", [group([spark(20), fill("#FFFFFF")], "s"), group([spark(11, rot=45), fill(slot="secondary")], "s2"),
                             glow(80, GOLD_L, 0.6)],
               parent=edge, rotation=sampled(lambda t: -t * 5, 0, F, 5), ip=8, op=LVL + 2,
               scale=anim([(8, [0, 0], SPRING), (16, [100, 100], HOLD), (LVL - 2, [100, 100], EASE_OUT), (LVL + 2, [220, 220])]),
               opacity=anim([(LVL - 1, 100, EASE_OUT), (LVL + 2, 0)]))
    comp.layer("edge star 2", [group([spark(12), fill("#FFFFFF")], "s"), glow(46, GOLD_L, 0.5)], parent=edge,
               rotation=sampled(lambda t: -t * 5, 0, F, 5), ip=LVL + 10, scale=pop(LVL + 10, 10))
    trail(comp, BX, BW, BY, [group([ellipse((7, 7)), fill(slot="accent")], "m"), glow(18, "#E7D2FF", 0.4)], seed=4,
          spread=8)

    # medallion
    med = comp.null("med", position=(MX, BY - 8), parent=rig,
                    scale=anim([(0, [0, 0], SPRING), (14, [100, 100], HOLD), (LVL, [100, 100], EASE_OUT),
                                (LVL + 3, [116, 116], SPRING), (LVL + 16, [100, 100])]),
                    rotation=anim([(0, -60, SNAP_OUT), (16, 0)]))
    comp.layer("med flash", [group([ellipse((MR * 2 - 16, MR * 2 - 16)), fill("#FFFFFF")], "f")], parent=med,
               opacity=anim([(LVL, 0, HOLD), (LVL + 1, 90, EASE_OUT), (LVL + 14, 0)]))
    studs = [group([ngon(4, 7, 0, pt(MR - 4, a)), fill(slot="accent")], f"stud{a}") for a in range(0, 360, 45)]
    comp.layer("medallion", studs + [
        group([ellipse((MR * 2 - 22, MR * 2 - 22)), stroke(GOLD_D, width=3)], "inner line"),
        group([ellipse((MR * 2 - 16, MR * 2 - 16)), sheen(MR * 2, MR * 2, 0.15, 0.35)], "gloss"),
        group([ellipse((MR * 2 - 16, MR * 2 - 16)), fill(slot="background")], "face"),
        group([ellipse((MR * 2, MR * 2)), sheen(MR * 2, MR * 2, 0.45, 0.35)], "gold sheen"),
        group([ellipse((MR * 2, MR * 2)), fill(slot="secondary")], "gold"),
        group([ellipse((MR * 2 + 6, MR * 2 + 6)), fill(GOLD_D)], "edge"),
        group([ellipse((MR * 2 + 6, MR * 2 + 6), (0, 6)), fill("#000000", 30)], "shadow"),
    ], parent=med)

    # bar fill
    comp.layer("bar matte", [group([rect((BW, BH), (BX + BW / 2, BY), BH / 2), fill()], "m")], parent=rig)
    comp.layer("bar fill", [
        group([rect((BW, BH), (BX + BW / 2, BY)), fill("#FFFFFF")], "flash",
              opacity=anim([(LVL - 1, 0, HOLD), (LVL, 100, HOLD), (LVL + 3, 100, EASE_OUT), (LVL + 16, 0)])),
        group([rect((BW, BH), (0, 0)), sheen(BW, BH, 0.45, 0.3)], "gloss", position=(BX + BW / 2, BY)),
        group([lbar(BX, BY - BH / 2, BW, BH, K), fill(slot="primary")], "fill"),
        group([lbar(BX, BY - BH / 2, BW, BH, [(t, min(v + 0.015, 1) if v else 0, e) for t, v, e in K]),
               fill(slot="accent")], "edge"),
    ], parent=rig, matte="alpha", opacity=fade(0, 10))
    # gold frame with a spear tip on the right
    tipx = BX + BW + 14
    frame_pts = [(BX - 30, BY - BH / 2 - 8), (BX + BW, BY - BH / 2 - 8), (tipx + 26, BY), (BX + BW, BY + BH / 2 + 8),
                 (BX - 30, BY + BH / 2 + 8)]
    gems = [group([ngon(4, 9, 0, (BX + BW * i / 4, BY - BH / 2 - 8)), fill(slot="primary"), stroke(GOLD_D, width=2)],
                  f"gem{i}") for i in (1, 2, 3)]
    comp.layer("frame", gems + [
        group([ngon(4, 13, 0, (tipx + 6, BY)), fill(slot="primary"), stroke(GOLD_D, width=2.5)], "tip gem"),
        group([rect((BW, BH), (BX + BW / 2, BY), BH / 2), fill(slot="background")], "track"),
        group([poly(frame_pts), sheen(BW, BH + 16, 0.5, 0.3)], "gold sheen", ),
        group([poly(frame_pts), fill(slot="secondary"), stroke(GOLD_D, width=3, join="miter")], "gold"),
        group([poly([(x, y + 6) for x, y in frame_pts]), fill("#000000", 30)], "shadow"),
    ], parent=rig)
    return comp


build_asset(CAT, "xp-bar-fill", "XP Bar Fill",
            "Experience bar that fills up with a sparkle riding its leading edge, flashes on level-up and "
            "starts the next level. Put the level number in the badge and a label above the bar.",
            ["xp", "experience", "level up", "progress", "bar", "gaming", "hud", "rpg"], [
    Variant("modern", "Modern HUD", modern(), "intro-hold", thumb_t=0.21, region=(20, 16, 440, 150),
            text_area=(46, BY - 30, 60, 48), text_areas={"level": (46, BY - 30, 60, 48), "label": (160, BY - 66, 520, 26)},
            description="Sleek skewed cyan bar with a hexagon level badge and a glossy sheen."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.21, bg="e8e8ee", region=(20, 16, 440, 150),
            text_area=(44, BY - 36, 60, 48), text_areas={"level": (44, BY - 36, 60, 48), "label": (160, BY - 66, 520, 24)},
            description="8-bit segmented bar that lights up block by block, with a blinking pixel badge."),
    Variant("fantasy", "Fantasy", fantasy(), "intro-hold", thumb_t=0.21, region=(20, 16, 440, 150),
            text_area=(46, BY - 34, 64, 52), text_areas={"level": (46, BY - 34, 64, 52), "label": (170, BY - 62, 520, 26)},
            description="Ornate gold frame with gems, a purple magic fill and a medallion that flares with rays."),
])
