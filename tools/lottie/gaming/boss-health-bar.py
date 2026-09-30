import random

from _gaming2 import *

W, H, F = 1400, 190, 120
HITS = [52, 70, 88]
LV = [1.0, 0.8, 0.61, 0.42]
FILL = [(16, 0, EASE_IN_OUT), (40, 1, HOLD)] + [(h, v, HOLD) for h, v in zip(HITS, LV[1:])] + [(F, LV[-1], HOLD)]
TRAIL = [(16, 0, EASE_IN_OUT), (40, 1, HOLD)]
for h, v0, v1 in zip(HITS, LV, LV[1:]):
    TRAIL += [(h + 8, v0, EASE_IN_OUT), (h + 16, v1, HOLD)]
TRAIL += [(F, LV[-1], HOLD)]


def shake_keys(c, amp=8):
    keys = [(0, list(c), HOLD)]
    for h in HITS:
        for i, (dx, dy) in enumerate(((amp, -amp / 3), (-amp * 0.8, amp / 3), (amp * 0.5, 0), (-amp * 0.3, 0), (0, 0))):
            keys.append((h + i, [c[0] + dx, c[1] + dy], LINEAR))
    keys.append((F, list(c), HOLD))
    return anim(keys)


def span(x, y, w, h, v0, v1):
    return rect((w * (v1 - v0), h), (x + w * (v0 + v1) / 2, y + h / 2))


def chunk_flashes(comp, x, y, w, h, parent=None, name="chunk", hold=False):
    for h_, v0, v1 in zip(HITS, LV, LV[1:]):
        comp.layer(name, [group([span(x, y, w, h, v1, v0), fill("#FFFFFF")], "c")], parent=parent,
                   opacity=anim([(h_ - 1, 0, HOLD), (h_, 100, HOLD), (h_ + 3, 100, HOLD if hold else EASE_OUT),
                                 (h_ + (4 if hold else 12), 0)]), ip=h_ - 1, op=h_ + 13)


def hit_sparks(comp, x, y, w, parent=None, shapes=None, hold=False, seed=1):
    rng = random.Random(seed)
    for h_, v in zip(HITS, LV[1:]):
        ex = x + w * v
        for k in range(7):
            a = rng.uniform(-80, 80) + (0 if k % 2 else 180)
            r = rng.uniform(40, 90)
            life = rng.randint(10, 15)
            p1 = pt(r, a)

            def fn(u, p1=p1, life=life, ex=ex):
                e = ease_out(u / life)
                return {"position": [ex + p1[0] * e, y + p1[1] * e * 0.6], "scale": [100 * (1 - u / life)] * 2}
            particle(comp, "spark", shapes, h_, life, F, fn, step=2 if hold else 1, wrap=False, hold=hold,
                     parent=parent)



# ---------------------------------------------------------------- fantasy (ornate)

HORN_L = "M-30 -10 C-50 -18 -62 -40 -58 -66 C-50 -46 -38 -36 -20 -30 Z"


def fantasy():
    comp = Comp("boss-health-bar", W, H, frames=F)
    comp.slot("primary", "#D1202F")
    comp.slot("secondary", GOLD)
    comp.slot("accent", "#FFB347")
    comp.slot("background", "#1A0D12")
    BX, BW, BY, BH = 170, 1130, 112, 30
    CX = 104
    rig = comp.null("rig", position=shake_keys((0, 0), 7))
    hit_sparks(comp, BX, BY + BH / 2, BW, rig, [group([spark(10), fill(slot="accent")], "s")])
    chunk_flashes(comp, BX, BY, BW, BH, rig)
    # crest: horned skull in a gold shield at the left end
    crest = comp.null("crest", parent=rig, position=(CX, BY + BH / 2 - 6),
                      scale=anim([(4, [0, 0], SPRING), (18, [100, 100], HOLD)] +
                                 sum([[(h, [100, 100], EASE_OUT), (h + 2, [110, 110], SPRING), (h + 12, [100, 100], HOLD)]
                                      for h in HITS], []) + [(F, [100, 100])]))
    comp.layer("skull", [group(skull_teeth(1.2) + [fill(slot="background")], "teeth"),
                         group(skull_d(1.2) + [fill("#F1E6D0", even_odd=True)], "skull")], parent=crest, position=(0, 4))
    horns = [group([*svg_shapes(HORN_L), fill("#F1E6D0"), stroke("#3A2A1A", width=3)], "hornL"),
             group([*svg_shapes(HORN_L), fill("#F1E6D0"), stroke("#3A2A1A", width=3)], "hornR", scale=(-100, 100))]
    shield = "M0 -56 L50 -38 L46 18 C40 42 16 56 0 64 C-16 56 -40 42 -46 18 L-50 -38 Z"
    comp.layer("shield", [
        group([*svg_shapes(shield, 0.82), fill(slot="primary")], "field"),
        group([*svg_shapes(shield), sheen(100, 120, 0.4, 0.35)], "sheen"),
        group([*svg_shapes(shield), fill(slot="secondary"), stroke(GOLD_D, width=3)], "gold"),
    ] + horns, parent=crest)
    # bar
    comp.layer("matte", [group([rect((BW, BH), (BX + BW / 2, BY + BH / 2)), fill()], "m")], parent=rig)
    comp.layer("bar", [
        group([rect((BW, BH), (0, 0)), sheen(BW, BH, 0.35, 0.35)], "gloss", position=(BX + BW / 2, BY + BH / 2)),
        group([rect((BW, 4), (BX + BW / 2, BY + 6)), fill("#FFFFFF", 20)], "hi"),
        group([lbar(BX, BY, BW, BH, FILL), fill(slot="primary")], "fill"),
        group([lbar(BX, BY, BW, BH, TRAIL), fill(slot="accent")], "trail"),
        group([rect((BW, BH), (BX + BW / 2, BY + BH / 2)), fill(slot="background")], "track"),
    ], parent=rig, matte="alpha", opacity=fade(10, 16))
    # gold frame with notches and pointed right end
    y0, y1 = BY - 9, BY + BH + 9
    frame = [(BX - 40, y0), (BX + BW + 6, y0), (BX + BW + 40, BY + BH / 2), (BX + BW + 6, y1), (BX - 40, y1)]
    studs = [group([ngon(4, 8, 0, (BX + BW * k / 4, y0)), fill(slot="secondary"), stroke(GOLD_D, width=2)], f"stud{k}")
             for k in (1, 2, 3)]
    studs += [group([ngon(4, 8, 0, (BX + BW * k / 4, y1)), fill(slot="secondary"), stroke(GOLD_D, width=2)], f"studb{k}")
              for k in (1, 2, 3)]
    comp.layer("frame", studs + [
        group([ngon(4, 13, 0, (BX + BW + 18, BY + BH / 2)), fill(slot="primary"), stroke(GOLD_D, width=2.5)], "gem"),
        group([poly(frame), sheen(BW, BH + 18, 0.5, 0.35)], "sheen"),
        group([poly(frame), fill(slot="secondary"), stroke(GOLD_D, width=3, join="miter")], "gold"),
        group([poly([(x, y + 7) for x, y in frame]), fill("#000000", 35)], "shadow"),
    ], parent=rig, scale=anim([(0, [0, 100], SNAP_OUT), (16, [100, 100])]), anchor=(W / 2, 0), position=(W / 2, 0))
    # name underline flourish
    comp.layer("flourish", [group([seg((BX, BY - 26), (BX + 520, BY - 26)), trim(end=anim([(14, 0, SNAP_OUT), (36, 100)])), stroke(slot="secondary", width=2)], "l"),
                            group([ngon(4, 6, 0, (BX + 530, BY - 26)), fill(slot="secondary")], "d",
                                  opacity=anim([(30, 0, EASE_OUT), (36, 100)]))], parent=rig)
    return comp


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("boss-health-bar--modern", W, H, frames=F)
    comp.slot("primary", "#FF2D3F")
    comp.slot("accent", "#FFE2E4")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    BX, BW, BY, BH, SK = 130, 1160, 110, 26, 20
    rig = comp.null("rig", position=shake_keys((0, 0), 5))
    hit_sparks(comp, BX, BY + BH / 2, BW, rig, [group([rect((14, 3)), fill("#FFFFFF")], "s")], seed=3)
    chunk_flashes(comp, BX, BY, BW, BH, rig)
    # phase notches
    comp.layer("notches", [group([poly([(BX + BW * p - 7, BY - 12), (BX + BW * p + 7, BY - 12), (BX + BW * p, BY - 3)])
                                  for p in (1 / 3, 2 / 3)] + [fill(slot="outline", opacity=80)], "n")], parent=rig,
               opacity=fade(30, 38))
    comp.layer("ticks", [group([seg((BX + BW * i / 20 + SK / 2, BY), (BX + BW * i / 20 - SK / 2, BY + BH)) for i in range(1, 20)]
                               + [stroke(slot="background", width=2, opacity=55)], "t")], parent=rig, opacity=fade(10, 16))
    comp.layer("matte", [group([skew_rect(BW, BH, SK, (BX + BW / 2, BY + BH / 2)), fill()], "m")], parent=rig)
    comp.layer("bar", [
        group([rect((BW, BH), (0, 0)), sheen(BW, BH, 0.3, 0.3)], "gloss", position=(BX + BW / 2, BY + BH / 2)),
        group([lbar(BX, BY, BW, BH, FILL), fill(slot="primary")], "fill"),
        group([lbar(BX, BY, BW, BH, TRAIL), fill(slot="accent")], "trail"),
        group([rect((BW, BH), (BX + BW / 2, BY + BH / 2)), fill(slot="background", opacity=85)], "track"),
    ], parent=rig, matte="alpha", opacity=fade(10, 16))
    comp.layer("rim", [group([skew_rect(BW + 12, BH + 12, SK + 2, (BX + BW / 2, BY + BH / 2)),
                              stroke(slot="outline", width=2, opacity=40), fill("#000000", 45)], "rim")], parent=rig,
               scale=anim([(0, [0, 100], SNAP_OUT), (14, [100, 100])]), anchor=(W / 2, 0), position=(W / 2, 0))
    # boss icon diamond + corner brackets
    comp.layer("icon", [group([ngon(4, 14, 0), fill(slot="primary")], "core"),
                        group([ngon(4, 26, 0), stroke(slot="outline", width=3)], "ring"),
                        group([ngon(4, 34, 0), stroke(slot="primary", width=2, opacity=60)], "ring2")],
               parent=rig, position=(BX - 56, BY + BH / 2),
               scale=anim([(2, [0, 0], SPRING), (14, [100, 100])]),
               rotation=anim([(2, -90, SNAP_OUT), (18, 0)]))
    comp.layer("name line", [group([seg((BX - 8, BY - 22), (BX + 420, BY - 22)), trim(end=anim([(10, 0, SNAP_OUT), (30, 100)])), stroke(slot="primary", width=3, cap="butt")], "l"),
                             group([seg((BX + 432, BY - 22), (BX + 450, BY - 22)), stroke(slot="primary", width=3, cap="butt")],
                                   "d", opacity=fade(28, 32))], parent=rig)
    return comp


# ---------------------------------------------------------------- pixel

BOSS_SKULL = [
    "K.............K",
    "KK...KKKKK...KK",
    "KHK.KWWWWWK.KHK",
    ".KHKWWWWWWWKHK.",
    "..KWWWWWWWWWK..",
    "..KWKKWWWKKWK..",
    "..KWKRWWWKRWK..",
    "..KWWWWKWWWWK..",
    "...KWWWWWWWK...",
    "...KWKWKWKWK...",
    "....KKKKKKK....",
]


def pixel():
    comp = Comp("boss-health-bar--pixel", W, H, frames=F)
    comp.slot("primary", "#E8283C")
    comp.slot("accent", "#FFD23F")
    comp.slot("background", "#2B2140")
    comp.slot("outline", INK)
    PX = 8
    BX, BW, BY, BH = 176, 1136, 104, 40
    N = 71
    SW = BW / N
    rig = comp.null("rig", position=stepped(lambda t: [8 * ((1 if (t - h) % 2 == 0 else -1) if any(h <= t < h + 6 for h in HITS)
                                                           else 0), 0], 0, F, 1))
    hit_sparks(comp, BX, BY + BH / 2, BW, rig, [box(-6, -6, 12, 12, slot="accent")], hold=True, seed=5)
    chunk_flashes(comp, BX, BY, BW, BH, rig, hold=True)

    def val(keys, t):
        if t < keys[0][0]:
            return keys[0][1]
        for (t0, v0, e), (t1, v1, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                if e == HOLD:
                    return v0 if t < t1 else v1
                return lerp(v0, v1, smooth((t - t0) / (t1 - t0)))
        return keys[-1][1]
    q = lambda v: round(v * N) / N
    qk = lambda keys: [(t, q(val(keys, t)), HOLD) for t in range(0, F + 1, 2)]
    comp.layer("fill", [group([lbar(BX, BY + 6, BW, 6, qk(FILL)), fill("#FFFFFF", 45)], "hi"),
                        group([lbar(BX, BY + BH - 10, BW, 6, qk(FILL)), fill("#000000", 25)], "lo"),
                        group([lbar(BX, BY, BW, BH, qk(FILL)), fill(slot="primary")], "fill"),
                        group([lbar(BX, BY, BW, BH, qk(TRAIL)), fill(slot="accent")], "trail")], parent=rig)
    # segment grid lines every 4 cells
    comp.layer("grid", [group([rect((4, BH), (BX + BW * i / 16, BY + BH / 2)) for i in range(1, 16)] +
                              [fill(slot="background", opacity=60)], "g")], parent=rig,
               opacity=stepped(lambda t: 0 if t < 4 else 100, 0, 6, 2))
    fr = [box(BX - 8, BY - 8, BW + 16, 8, slot="outline"), box(BX - 8, BY + BH, BW + 16, 8, slot="outline"),
          box(BX - 16, BY, 8, BH, slot="outline"), box(BX + BW + 8, BY, 8, BH, slot="outline"),
          box(BX - 8, BY, 8, BH, "#FFFFFF"), box(BX + BW, BY, 8, BH, "#FFFFFF"),
          box(BX, BY, BW, BH, slot="background"),
          box(BX - 8, BY + 8, BW + 24, BH + 8, "#000000", opacity=30)]
    comp.layer("frame", [group(fr, "f")], opacity=stepped(lambda t: 0 if t < 4 else 100, 0, 6, 2))
    comp.layer("skull", pix(BOSS_SKULL, {"R": ("slot", "primary"), "H": ("slot", "accent"), "W": "#F4F0E6",
                                         "K": ("slot", "outline")}, PX, order=list("RHWK")),
               position=(96, BY + BH / 2 - 4),
               scale=stepped(lambda t: [0, 0] if t < 2 else [60, 60] if t < 4 else [120, 120] if t < 6 else
                             [115, 115] if any(h <= t < h + 4 for h in HITS) else [100, 100], 0, F, 1))
    comp.layer("name", [box(BX + i * 24, BY - 30, 14, 8, slot="accent") for i in range(8)],
               opacity=stepped(lambda t: 0 if t < 8 else 100, 0, 10, 2))
    return comp


NAME = {"modern": (130, 38, 700, 46), "fantasy": (170, 34, 700, 46), "pixel": (176, 20, 700, 46)}
build_asset(CAT, "boss-health-bar", "Boss Health Bar",
            "Wide boss health bar that draws in, fills up and then drains in three chunks with a white flash and a "
            "delayed damage trail. Put the boss name above the bar.",
            ["boss", "health", "hp", "bar", "damage", "gaming", "hud", "rpg"], [
    Variant("fantasy", "Ornate", fantasy(), "intro-hold", thumb_t=0.617, text_area=NAME["fantasy"],
            text_areas={"name": NAME["fantasy"]}, region=(10, 0, 1090, 190),
            description="Gold ornate frame with a horned-skull crest, studs and a gem-tipped end."),
    Variant("modern", "Modern", modern(), "intro-hold", thumb_t=0.617, text_area=NAME["modern"],
            text_areas={"name": NAME["modern"]}, region=(10, 0, 1090, 190),
            description="Sleek skewed red bar with phase notches, tick marks and a diamond boss icon."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.617, bg="e8e8ee", text_area=NAME["pixel"],
            text_areas={"name": NAME["pixel"]}, region=(10, 0, 1090, 190),
            description="Chunky 8-bit bar with a pixel horned skull; drains in stepped blocks."),
])
