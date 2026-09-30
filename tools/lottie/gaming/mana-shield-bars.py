from _gaming2 import *

W, H, F = 660, 170, 90
Y1, Y2 = 60, 114            # shield bar, mana bar
BX, BW = 104, 420
VX = BX + BW + 22          # value text column

# fraction keys (loop: last == first)
SHIELD = [(0, 1.0, HOLD), (12, 0.52, HOLD), (40, 0.52, EASE_IN_OUT), (78, 1.0, HOLD), (F, 1.0, HOLD)]
MANA = [(0, 0.86, HOLD), (26, 0.34, HOLD), (32, 0.34, LINEAR), (F, 0.86, HOLD)]
TRAIL_S = [(0, 1.0, HOLD), (18, 1.0, EASE_IN_OUT), (30, 0.52, HOLD), (40, 0.52, EASE_IN_OUT), (78, 1.0, HOLD), (F, 1.0, HOLD)]
TRAIL_M = [(0, 0.86, HOLD), (30, 0.86, EASE_IN_OUT), (42, 0.34, HOLD), (42.01, 0.34, LINEAR), (F, 0.86, HOLD)]
HIT_S, HIT_M = 12, 26


def val(keys, t):
    for (t0, v0, e), (t1, v1, _) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            if e == HOLD:
                return v0 if t < t1 else v1
            u = (t - t0) / (t1 - t0)
            return lerp(v0, v1, smooth(u) if e == EASE_IN_OUT else u)
    return keys[-1][1]


def flash(t):
    return anim([(0, 0, HOLD), (t, 100, HOLD), (t + 2, 100, EASE_OUT), (t + 10, 0, HOLD), (F, 0)])


def regen_opacity(keys, t0, t1):
    """Edge glow visible while regenerating."""
    return anim([(0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 6, 100, HOLD), (t1 - 6, 100, EASE_IN), (t1, 0, HOLD), (F, 0)])


SHIELD_D = "M0 -21 L17 -14 L15 5 C13 14 5 19 0 22 C-5 19 -13 14 -15 5 L-17 -14 Z"
DROP_D = "M0 -22 C6 -12 16 -2 16 8 C16 17 9 22 0 22 C-9 22 -16 17 -16 8 C-16 -2 -6 -12 0 -22 Z"
BOLT_D = "M3 -24 L-11 3 L-1 3 L-4 24 L11 -5 L1 -5 Z"


def icon(d, s, *paint):
    return group([*svg_shapes(d, s), *paint], "icon")


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("mana-shield-bars", W, H, frames=F)
    comp.slot("primary", "#46A6FF")     # mana
    comp.slot("secondary", "#E9F4FF")   # shield
    comp.slot("background", PANEL)
    comp.slot("accent", "#FF4D5E")
    BH, SK = 22, 12
    for y, keys, trail_k, slot, hit, regen, d, segs in (
            (Y1, SHIELD, TRAIL_S, "secondary", HIT_S, (40, 78), SHIELD_D, 4),
            (Y2, MANA, TRAIL_M, "primary", HIT_M, (32, F), DROP_D, 0)):
        # edge glow
        edge = anim([(t, [BX + BW * v, y], e) for t, v, e in keys])
        comp.layer("regen edge", [glow(46, "#FFFFFF", 0.7), group([rect((4, BH + 8)), fill("#FFFFFF")], "line")],
                   position=edge, opacity=regen_opacity(keys, *regen) if slot == "secondary" else
                   anim([(0, 60, HOLD), (hit, 0, HOLD), (hit + 8, 0, EASE_OUT), (hit + 14, 60, HOLD), (F, 60)]))
        if segs:
            comp.layer("ticks", [group([seg((BX + BW * i / segs + SK / 2, y - BH / 2), (BX + BW * i / segs - SK / 2, y + BH / 2))
                                        for i in range(1, segs)] + [stroke(slot="background", width=4)], "t")])
        comp.layer("matte", [group([skew_rect(BW, BH, SK, (BX + BW / 2, y)), fill()], "m")])
        comp.layer("bar", [
            group([lbar(BX, y - BH / 2, BW, BH, keys), fill("#FFFFFF")], "hit flash", opacity=flash(hit)),
            group([rect((BW, BH), (0, 0)), sheen(BW, BH, 0.45, 0.25)], "gloss", position=(BX + BW / 2, y)),
            group([lbar(BX, y - BH / 2, BW, BH, keys), fill(slot=slot)], "fill"),
            group([lbar(BX, y - BH / 2, BW, BH, trail_k), fill(slot="accent")], "trail"),
            group([rect((BW, BH), (BX + BW / 2, y)), fill(slot="background", opacity=90)], "track"),
        ], matte="alpha")
        comp.layer("rim", [group([skew_rect(BW + 8, BH + 8, SK + 1, (BX + BW / 2, y)), stroke("#FFFFFF", width=1.5, opacity=35),
                                  fill("#000000", 40)], "rim")])
        # icon tile
        comp.layer("icon", [icon(d, 0.8, fill(slot=slot))], position=(58, y),
                   scale=anim([(0, [100, 100], HOLD), (hit, [100, 100], EASE_OUT), (hit + 3, [125, 125], SPRING),
                               (hit + 14, [100, 100], HOLD), (F, [100, 100])]))
        comp.layer("tile", [group([skew_rect(52, 44, SK, (58, y)), fill(slot="background", opacity=92),
                                   stroke("#FFFFFF", width=1.5, opacity=35)], "tile")])
        comp.layer("value line", [group([seg((VX, y + 14), (VX + 90, y + 14)), stroke(slot=slot, width=2, opacity=60)], "l")])
    return comp


# ---------------------------------------------------------------- pixel

SHIELD_PIX = [
    "KKKKKKKKK",
    "KWWWSSSSK",
    "KWSSSSSDK",
    "KWSSSSSDK",
    "KWSSSSSDK",
    ".KSSSSDK.",
    ".KSSSSDK.",
    "..KSSDK..",
    "...KDK...",
    "....K....",
]
DROP_PIX = [
    "....K....",
    "...KMK...",
    "..KMMMK..",
    ".KMWMMMK.",
    "KMWMMMMMK",
    "KMWMMMMMK",
    "KMMMMMMDK",
    ".KMMMMDK.",
    "..KKKKK..",
]


def pixel():
    comp = Comp("mana-shield-bars--pixel", W, H, frames=F)
    comp.slot("primary", "#3F7CFF")
    comp.slot("secondary", "#FFD23F")
    comp.slot("outline", INK)
    comp.slot("background", "#2B2140")
    comp.slot("accent", "#FF4D5E")
    N, SW, BH = 14, 30, 30
    for y, keys, slot, hit, rows, ch in ((Y1, SHIELD, "secondary", HIT_S, SHIELD_PIX, "S"),
                                         (Y2, MANA, "primary", HIT_M, DROP_PIX, "M")):
        for i in range(N):
            x = BX + i * SW
            on = lambda t, i=i, keys=keys: (i + 1) / N <= val(keys, t) + 0.5 / N
            # the next cell to regenerate blinks
            nxt = lambda t, i=i, keys=keys: (i + 1) / N > val(keys, t) + 0.5 / N and i / N <= val(keys, t) + 0.5 / N
            comp.layer("blink", [box(x + 3, y - BH / 2 + 3, SW - 6, BH - 6, slot=slot, opacity=45)],
                       opacity=stepped(lambda t, n=nxt: 100 if n(t) and (t // 4) % 2 == 0 else 0, 0, F, 1))
            comp.layer("flash", [box(x + 3, y - BH / 2 + 3, SW - 6, BH - 6, "#FFFFFF")],
                       opacity=stepped(lambda t, on=on: 100 if hit <= t < hit + 8 and (t - hit) % 4 < 2 and
                                       not on(t) and on(hit - 1) else 0, 0, F, 1))
            comp.layer("cell", [box(x + 3, y - BH / 2 + 3, SW - 6, 5, "#FFFFFF", opacity=50, name="hi"),
                                box(x + 3, y + BH / 2 - 8, SW - 6, 5, "#000000", opacity=25, name="lo"),
                                box(x + 3, y - BH / 2 + 3, SW - 6, BH - 6, slot=slot)],
                       opacity=stepped(lambda t, on=on: 100 if on(t) else 0, 0, F, 1))
        comp.layer("track", [box(BX, y - BH / 2, BW, BH, slot="background"),
                             box(BX - 5, y - BH / 2 - 5, BW + 10, BH + 10, slot="outline"),
                             box(BX - 5, y - BH / 2 + 1, BW + 10, BH + 10, "#000000", opacity=25)])
        comp.layer("icon", pix(rows, {"W": ("#FFFFFF", 85), "D": ("#000000", 30), ch: ("slot", slot), "K": ("slot", "outline")},
                               5, order=["W", "D", ch, "K"]), position=(62, y),
                   scale=stepped(lambda t: [125, 125] if hit <= t < hit + 4 else [100, 100], 0, F, 1))
        comp.layer("value", [box(VX + i * 16, y + 10, 10, 5, slot=slot) for i in range(5)])
    return comp


# ---------------------------------------------------------------- neon

def neon_v():
    comp = Comp("mana-shield-bars--neon", W, H, frames=F)
    comp.slot("primary", NCYAN)
    comp.slot("secondary", MAGENTA)
    comp.slot("accent", "#FFFFFF")
    BH = 18
    for y, keys, slot, hit, regen, d in ((Y1, SHIELD, "secondary", HIT_S, (40, 78), SHIELD_D),
                                         (Y2, MANA, "primary", HIT_M, (32, F), DROP_D)):
        edge = anim([(t, [BX + BW * v, y], e) for t, v, e in keys])
        comp.layer("spark", [group([spark(12), fill("#FFFFFF")], "s"), glow(40, "#FFFFFF", 0.6)], position=edge,
                   opacity=regen_opacity(keys, *regen) if slot == "secondary" else
                   anim([(0, 100, HOLD), (hit, 0, HOLD), (hit + 8, 0, EASE_OUT), (hit + 14, 100, HOLD), (F, 100)]))
        comp.layer("fill", [
            group([lbar(BX, y - BH / 2, BW, BH, keys, BH / 2), fill("#FFFFFF")], "flash", opacity=flash(hit)),
            group([lbar(BX, y - 3, BW, 6, keys, 3), fill("#FFFFFF", 80)], "core"),
            group([lbar(BX, y - BH / 2, BW, BH, keys, BH / 2), fill(slot=slot)], "fill"),
            group([lbar(BX, y - BH / 2, BW, BH, keys, BH / 2), stroke(slot=slot, width=10, opacity=30)], "glow1"),
            group([lbar(BX, y - BH / 2, BW, BH, keys, BH / 2), stroke(slot=slot, width=24, opacity=12)], "glow2"),
        ], opacity=anim([(0, 100, HOLD), (hit, 100, LINEAR), (hit + 1, 40, LINEAR), (hit + 2, 100, LINEAR),
                         (hit + 3, 50, LINEAR), (hit + 5, 100, HOLD), (F, 100)]))
        comp.layer("tube", neon([rect((BW + 16, BH + 16), (BX + BW / 2, y), (BH + 16) / 2)], slot=slot, w=3, core=False,
                                glow_a=0.8))
        comp.layer("ticks", [group([seg((BX + BW * i / 10, y + BH / 2 + 12), (BX + BW * i / 10, y + BH / 2 + 16))
                                    for i in range(11)] + [stroke(slot=slot, width=2, opacity=60)], "t")])
        comp.layer("icon", neon(svg_shapes(d, 0.85), slot=slot, w=3.5), position=(56, y),
                   scale=anim([(0, [100, 100], HOLD), (hit, [100, 100], EASE_OUT), (hit + 3, [125, 125], SPRING),
                               (hit + 14, [100, 100], HOLD), (F, [100, 100])]))
    return comp


TA = {"shield": (VX, Y1 - 18, W - VX - 10, 36), "mana": (VX, Y2 - 18, W - VX - 10, 36)}
build_asset(CAT, "mana-shield-bars", "Mana Shield Bars",
            "Stacked shield and mana bars on a loop: the shield takes a hit and recharges while mana is spent "
            "and regenerates. Put the values to the right of each bar.",
            ["mana", "shield", "energy", "bars", "regen", "gaming", "hud", "rpg"], [
    Variant("modern", "Modern HUD", modern(), "loop", thumb_t=0.2, text_area=TA["mana"], text_areas=TA,
            region=(20, 20, 620, 130),
            description="Skewed glossy bars with a red damage trail and a glowing regen edge."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.5, bg="e8e8ee", text_area=TA["mana"], text_areas=TA,
            region=(20, 20, 620, 130),
            description="8-bit block bars with pixel icons; cells blink back one by one as they regenerate."),
    Variant("neon", "Neon", neon_v(), "loop", thumb_t=0.2, text_area=TA["mana"], text_areas=TA,
            region=(20, 20, 620, 130),
            description="Glowing neon tubes that flicker when hit and refill with a spark."),
])
