from _gaming2 import *

W, H, F = 820, 250, 120
OUT = 96
RH = 54
YS = [44, 120, 196]
T0 = [4, 22, 40]
RX0, RX1 = 20, 800
KX, KW = 40, 262           # killer name area
WX = 360                   # weapon icon centre
SX = 436                   # skull icon centre
VX, VW = 476, 304          # victim name area

RIFLE = [(-44, -4), (-18, -10), (24, -10), (24, -7), (44, -7), (44, -3), (24, -3), (24, 0), (9, 0), (7, 12), (-1, 12),
         (1, 0), (-12, 0), (-16, 4), (-44, 9)]
PISTOL = [(-20, -10), (22, -10), (22, -2), (-2, -2), (-5, 4), (-8, 4), (-12, 14), (-22, 14), (-17, -2), (-20, -2)]
KNIFE_BLADE = [(-2, -5), (26, -5), (40, 1), (26, 5), (-2, 5)]


def weapon(kind, s=1.0):
    sc = lambda pts: [(x * s, y * s) for x, y in pts]
    if kind == "rifle":
        return [poly(sc(RIFLE))]
    if kind == "pistol":
        return [poly(sc(PISTOL)), rect((10 * s, 3 * s), (-8 * s, -1 * s))]
    return [poly(sc(KNIFE_BLADE)), rect((5 * s, 20 * s), (-6 * s, 0), 1.5 * s), rect((22 * s, 9 * s), (-20 * s, 0), 4 * s)]


KINDS = ["rifle", "knife", "pistol"]


def row_anim(i, dx=70, e=SNAP_OUT, dur=12):
    t0 = T0[i]
    to = OUT + i * 5
    pos = anim([(t0, [dx, 0], e), (t0 + dur, [0, 0], HOLD), (to, [0, 0], ANTICIPATE), (to + 12, [dx * 1.6, 0])])
    op = anim([(t0, 0, EASE_OUT), (t0 + 5, 100, HOLD), (to + 4, 100, EASE_IN), (to + 12, 0)])
    return pos, op


def row_layer(comp, i, name, shapes, parent, op, **kw):
    comp.layer(name, shapes, parent=parent, opacity=op, ip=T0[i], op=OUT + i * 5 + 13, **kw)


def base(name):
    comp = Comp(name, W, H, frames=F)
    comp.marker("intro", 0, T0[-1] + 16)
    comp.marker("outro", OUT, F - OUT)
    return comp


# ---------------------------------------------------------------- modern

def modern():
    comp = base("kill-feed-skulls")
    comp.slot("background", "#0E1117")
    comp.slot("primary", "#FF3B47")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FFC83D")
    for i, y in enumerate(YS):
        pos, op = row_anim(i)
        rig = comp.null(f"row {i}", position=pos, ip=T0[i])
        t0 = T0[i]
        # skull pop (+ headshot ring on the middle row)
        skull = [group(skull_teeth(0.82) + [fill(slot="background")], "teeth"),
                 group(skull_d(0.82) + [fill(slot="primary", even_odd=True)], "skull")]
        if i == 1:
            skull = [group([ellipse((56, 56)), stroke(slot="accent", width=3)], "ring"),
                     group([seg((-34, 0), (-22, 0)), seg((22, 0), (34, 0)), seg((0, -34), (0, -22)), seg((0, 22), (0, 34)),
                            stroke(slot="accent", width=3, cap="butt")], "ticks")] + skull
        row_layer(comp, i, "skull", skull, rig, op, position=(SX, y),
                  scale=anim([(t0 + 4, [0, 0], SPRING), (t0 + 16, [100, 100])]),
                  rotation=anim([(t0 + 4, -30, SNAP_OUT), (t0 + 16, 0)]))
        row_layer(comp, i, "weapon", [group(weapon(KINDS[i], 1.2) + [fill(slot="icon")], "w")], rig, op,
                  position=anim([(t0 + 2, [WX - 24, y], SNAP_OUT), (t0 + 14, [WX, y])]))
        row_layer(comp, i, "stripe", [group([rect(anim([(t0 + 2, [0, RH], SNAP_OUT), (t0 + 14, [6, RH])]), (RX0 + 3, y)),
                                             fill(slot="primary")], "s")], rig, op)
        row_layer(comp, i, "bar", [
            group([rect((RX1 - RX0, RH), ((RX0 + RX1) / 2, y), 4), sheen(RX1 - RX0, RH, 0.08, 0.2)], "gloss"),
            group([rect((RX1 - RX0, RH), ((RX0 + RX1) / 2, y), 4), fill(slot="background", opacity=82)], "bar"),
            group([rect((RX1 - RX0, RH), ((RX0 + RX1) / 2, y + 4), 4), fill("#000000", 22)], "shadow"),
        ] + ([group([rect((RX1 - RX0 + 4, RH + 4), ((RX0 + RX1) / 2, y), 6), stroke(slot="accent", width=2)], "you")]
             if i == 0 else []), rig, op)
    return comp


# ---------------------------------------------------------------- pixel

SWORD = [
    "....K.............",
    "...KYK............",
    "KKKKYKKKKKKKKKKKK.",
    "KBBBYWWWWWWWWWWWWK",
    "KBBBYSSSSSSSSSSSSK",
    "KKKKYKKKKKKKKKKKK.",
    "...KYK............",
    "....K.............",
]
ARROW = [
    "FF.............H..",
    ".FF............HH.",
    "..SSSSSSSSSSSSSSHH",
    ".FF............HH.",
    "FF.............H..",
]
BOMB = [
    ".......Y.",
    "......YKY",
    "...KKKK..",
    "..KGGGGK.",
    ".KGWGGGGK",
    ".KGWGGGGK",
    ".KGGGGGDK",
    ".KGGGGDDK",
    "..KDDDDK.",
    "...KKKK..",
]


def pixel():
    comp = base("kill-feed-skulls--pixel")
    comp.slot("background", "#241A36")
    comp.slot("primary", "#FF4D5E")
    comp.slot("outline", INK)
    comp.slot("accent", "#FFD23F")
    PX = 5
    icons = [
        pix(SWORD, {"W": "#F4F4FF", "S": "#A9B3C9", "Y": ("slot", "accent"), "B": "#8A5A2B", "K": ("slot", "outline")}, PX,
            order=list("WSYBK")),
        pix(ARROW, {"F": ("slot", "primary"), "S": "#C9A06A", "H": "#E6EAF5"}, PX, order=list("FSH")),
        pix(BOMB, {"Y": ("slot", "accent"), "W": "#FFFFFF", "D": "#2E2A3E", "G": "#5A5670", "K": ("slot", "outline")}, PX,
            order=list("YWDGK")),
    ]
    for i, y in enumerate(YS):
        t0 = T0[i]
        # stepped slide
        pos = stepped(lambda t, t0=t0, i=i: [0 if t >= t0 + 8 else snap(80 * (1 - (t - t0) / 8), 8) if t >= t0 else 80,
                                            0] if t < OUT + i * 5 else [snap(min(120, (t - OUT - i * 5) * 12), 8), 0],
                      0, F, 2)
        op = stepped(lambda t, t0=t0, i=i: 0 if t < t0 or t >= OUT + i * 5 + 10 else 100, 0, F, 1)
        rig = comp.null(f"row {i}", position=pos)
        row_layer(comp, i, "skull", pix(SKULL_PIX, {"W": ("slot", "primary") if i != 1 else "#FFFFFF", "K": ("slot", "outline")},
                                        5, order=list("WK")), rig, op, position=(SX, y),
                  scale=stepped(lambda t, t0=t0: [0, 0] if t < t0 + 6 else [140, 140] if t < t0 + 9 else [100, 100], 0, F, 1))
        if i == 1:
            row_layer(comp, i, "headshot", [box(-35, -35, 70, 5, slot="accent"), box(-35, 30, 70, 5, slot="accent"),
                                            box(-35, -35, 5, 70, slot="accent"), box(30, -35, 5, 70, slot="accent")],
                      rig, stepped(lambda t, t0=t0: 0 if t < t0 + 9 or t >= OUT + 15 or (t0 + 9 <= t < t0 + 20 and (t // 3) % 2)
                                      else 100, 0, F, 1), position=(SX, y))
        row_layer(comp, i, "weapon", icons[i], rig, op, position=(WX, y))
        row_layer(comp, i, "bar", [
            box(RX0 + 4, y - RH / 2 + 4, RX1 - RX0 - 8, 4, "#FFFFFF", opacity=18, name="hi"),
            box(RX0 + 4, y - RH / 2 + 4, 6, RH - 8, slot="primary" if i == 0 else "background", name="tag"),
            box(RX0 + 4, y - RH / 2 + 4, RX1 - RX0 - 8, RH - 8, slot="background"),
            box(RX0, y - RH / 2, RX1 - RX0, RH, slot="outline" if i else "accent"),
            box(RX0 + 4, y - RH / 2 + 4, RX1 - RX0, RH, "#000000", opacity=30),
        ], rig, op)
    return comp


# ---------------------------------------------------------------- neon

def neon_v():
    comp = base("kill-feed-skulls--neon")
    comp.slot("primary", MAGENTA)
    comp.slot("secondary", NCYAN)
    comp.slot("background", "#0A0612")
    for i, y in enumerate(YS):
        t0 = T0[i]
        pos, _ = row_anim(i, dx=0)
        to = OUT + i * 5
        flick = anim([(t0, 0, HOLD), (t0 + 1, 80, HOLD), (t0 + 2, 10, HOLD), (t0 + 4, 100, HOLD), (t0 + 5, 30, HOLD),
                      (t0 + 7, 100, HOLD), (to, 100, HOLD), (to + 2, 20, HOLD), (to + 3, 80, HOLD), (to + 5, 0, HOLD), (F, 0)])
        rig = comp.null(f"row {i}")
        skull = neon(skull_d(0.78), slot="primary", w=2.6)
        if i == 1:
            skull = neon([ellipse((56, 56))], slot="secondary", w=2.4, core=False) + skull
        row_layer(comp, i, "skull", skull, rig, flick, position=(SX, y),
                  scale=anim([(t0 + 4, [60, 60], SPRING), (t0 + 14, [100, 100])]))
        row_layer(comp, i, "weapon", neon(weapon(KINDS[i], 1.1), slot="secondary", w=2.6), rig, flick, position=(WX, y))
        row_layer(comp, i, "frame", neon([skew_rect(RX1 - RX0 - 20, RH - 6, 18, ((RX0 + RX1) / 2, y))],
                                         slot="primary" if i == 0 else "secondary", w=2.2, glow_a=0.7, core=i == 0), rig,
                  flick)
        row_layer(comp, i, "wipe", [group([skew_rect(RX1 - RX0 - 20, RH - 6, 18, ((RX0 + RX1) / 2, y)),
                                           fill(slot="background", opacity=80)], "bg")], rig,
                  anim([(t0, 0, EASE_OUT), (t0 + 6, 100, HOLD), (to, 100, EASE_IN), (to + 6, 0)]))
        row_layer(comp, i, "scan", [group([rect((RX1 - RX0 - 40, 2), ((RX0 + RX1) / 2, 0)), fill(slot="secondary", opacity=60)],
                                          "line")], rig, anim([(t0, 100, EASE_IN), (t0 + 12, 0)]),
                  position=anim([(t0, [0, y - RH / 2], EASE_OUT), (t0 + 12, [0, y + RH / 2])]))
    return comp


def areas():
    out = {}
    for i, y in enumerate(YS):
        out[f"killer{i + 1}"] = (KX, y - 18, KW, 36)
        out[f"victim{i + 1}"] = (VX, y - 18, VW, 36)
    return out


TA = areas()
build_asset(CAT, "kill-feed-skulls", "Kill Feed Skulls",
            "Shooter-style kill feed: three rows slide in, each with a weapon icon and a skull (the middle one "
            "a headshot). Put the player names left and right of the icons in each row.",
            ["kill feed", "killfeed", "skull", "elimination", "fps", "shooter", "gaming", "hud"], [
    Variant("modern", "Modern", modern(), "intro-hold-outro", thumb_t=0.45, region=(170, 10, 480, 230), text_area=TA["killer1"], text_areas=TA,
            description="Dark translucent rows with red accent stripes, rifle/knife/pistol silhouettes and red skulls."),
    Variant("pixel", "Pixel", pixel(), "intro-hold-outro", thumb_t=0.45, region=(170, 10, 480, 230), bg="e8e8ee", text_area=TA["killer1"],
            text_areas=TA, description="8-bit rows with a pixel sword, arrow and bomb, and blinking pixel skulls."),
    Variant("neon", "Neon", neon_v(), "intro-hold-outro", thumb_t=0.45, region=(170, 10, 480, 230), text_area=TA["killer1"], text_areas=TA,
            description="Skewed neon outline rows that flicker on, with glowing weapon and skull outlines."),
])
