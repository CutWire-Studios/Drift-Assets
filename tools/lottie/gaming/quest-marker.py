from _gaming2 import *

W, H, F = 300, 420, 60
CX, CY = W / 2, 176
SH = 372           # shadow y
BAR = [(-30, -95), (30, -95), (19, 30), (-19, 30)]
QHOOK = "M -40 -52 C -40 -104 40 -104 40 -52 C 40 -16 0 -18 0 22"


def bob(amp=16, base=(CX, CY)):
    return sampled(lambda t: [base[0], base[1] - amp * (0.5 + 0.5 * math.sin(TAU * t / F - math.pi / 2))], 0, F, 2)


def squash():
    # slight squash at the bottom of the bob, stretch going up
    return sampled(lambda t: [100 + 4 * math.cos(TAU * t / F), 100 - 4 * math.cos(TAU * t / F)], 0, F, 2)


def shadow(comp, w=110):
    comp.layer("shadow", [group([ellipse((w, w * 0.22)), fill("#000000", 35)], "s")], position=(CX, SH),
               scale=sampled(lambda t: [100 - 18 * (0.5 + 0.5 * math.sin(TAU * t / F - math.pi / 2))] * 2, 0, F, 2))


def twinkles(comp, pts, shapes):
    for i, (x, y, ph) in enumerate(pts):
        comp.layer("twinkle", shapes, position=(x, y),
                   scale=sampled(lambda t, ph=ph: [100 * max(0, math.sin(TAU * (t / F * 2 + ph))) ** 3] * 2, 0, F, 2),
                   rotation=sampled(lambda t: t * 3, 0, F, 6))


def exclaim(paint_body, paint_dot, s=1.0):
    sc = lambda pts: [(x * s, y * s) for x, y in pts]
    return [group([ellipse((52 * s, 52 * s), (0, 72 * s))] + paint_dot, "dot"),
            group([poly(sc(BAR)), round_corners(12 * s)] + paint_body, "bar")]


def glossy_exclaim(slot):
    hi = [group([poly([(-19, -86), (-6, -86), (-8, 10), (-14, 10)]), round_corners(4), fill("#FFFFFF", 55)], "hi bar"),
          group([ellipse((14, 10), (-10, 62)), fill("#FFFFFF", 60)], "hi dot")]
    body = exclaim([fill(slot=slot)], [fill(slot=slot)])
    shade = [group([ellipse((52, 52), (0, 72)), gradient_fill([(0, "#000000", 0), (0.6, "#000000", 0), (1, "#000000", 0.22)],
                                                              (-10, 62), (16, 98))], "dot shade"),
             group([poly([(8, -95), (30, -95), (19, 30), (4, 30)]), fill("#000000", 16)], "bar shade")]
    outline = exclaim([stroke(slot="outline", width=14, join="round")], [stroke(slot="outline", width=14)])
    return hi + shade + body + outline


def glossy_question(slot):
    hook = svg_shapes(QHOOK)
    return [
        group([*svg_shapes("M -30 -60 C -28 -86 0 -92 18 -80"), stroke("#FFFFFF", width=9, opacity=55)], "hi"),
        group([ellipse((14, 10), (-10, 64)), fill("#FFFFFF", 60)], "hi dot"),
        group([ellipse((50, 50), (0, 74)), fill(slot=slot)], "dot"),
        group(hook + [stroke(slot=slot, width=34, cap="round")], "hook"),
        group([ellipse((50, 50), (0, 74)), stroke(slot="outline", width=14)], "dot o"),
        group(hook + [stroke(slot="outline", width=48, cap="round")], "hook o"),
    ]


def glow_pulse(comp, color, d=260):
    comp.layer("glow", [glow(d, color, 0.55)], position=bob(), scale=loop(F, [[100, 100], [115, 115]]))


# ---------------------------------------------------------------- classic !

def classic():
    comp = Comp("quest-marker", W, H, frames=F)
    comp.slot("primary", "#FFC21A")
    comp.slot("outline", "#3A2200")
    twinkles(comp, [(64, 90, 0.0), (238, 150, 0.35), (80, 260, 0.7)], [group([spark(14), fill("#FFFFFF")], "s")])
    comp.layer("marker", glossy_exclaim("primary"), position=bob(), scale=squash())
    glow_pulse(comp, "#FFD65A")
    shadow(comp)
    return comp


# ---------------------------------------------------------------- question ?

def question():
    comp = Comp("quest-marker--question", W, H, frames=F)
    comp.slot("primary", "#3FB8FF")
    comp.slot("outline", "#0B2A4A")
    twinkles(comp, [(62, 100, 0.1), (240, 140, 0.45), (230, 280, 0.8)], [group([spark(14), fill("#FFFFFF")], "s")])
    comp.layer("marker", glossy_question("primary"), position=bob(), scale=squash())
    glow_pulse(comp, "#7FD3FF")
    shadow(comp, 100)
    return comp


# ---------------------------------------------------------------- pixel

EXCL_PIX = [
    ".KKKKKK.",
    "KWWYYYOK",
    "KWYYYYOK",
    "KWYYYYOK",
    "KWYYYYOK",
    ".KYYYOK.",
    ".KYYYOK.",
    ".KYYYOK.",
    ".KYYYOK.",
    "..KYOK..",
    "..KKKK..",
    "........",
    "..KKKK..",
    ".KWYYOK.",
    ".KYYYOK.",
    ".KYOOOK.",
    "..KKKK..",
]


def pixel():
    comp = Comp("quest-marker--pixel", W, H, frames=F)
    comp.slot("primary", "#FFD23F")
    comp.slot("secondary", "#E08A1E")
    comp.slot("outline", INK)
    P = 12
    cols = {"W": "#FFFFFF", "O": ("slot", "secondary"), "Y": ("slot", "primary"), "K": ("slot", "outline")}
    pos = stepped(lambda t: [CX, CY - [0, 6, 12, 18, 12, 6][int(t // 10) % 6]], 0, F, 2)
    comp.layer("marker", pix(EXCL_PIX, cols, P, order=list("WOYK")), position=pos)
    for k, (x, y) in enumerate(((58, 80), (244, 130), (70, 250))):
        comp.layer("twinkle", [box(-4, -12, 8, 24, slot="secondary"), box(-12, -4, 24, 8, slot="secondary")], position=(x, y),
                   opacity=stepped(lambda t, k=k: 100 if (t // 10 + k) % 3 == 0 else 0, 0, F, 2))
    comp.layer("shadow", [box(-48, -8, 96, 16, "#000000", opacity=30), box(-36, -12, 72, 24, "#000000", opacity=0)],
               position=(CX, SH), scale=stepped(lambda t: [[100, 100], [92, 100], [84, 100], [76, 100], [84, 100], [92, 100]][int(t // 10) % 6],
                                                0, F, 2))
    return comp


# ---------------------------------------------------------------- hud waypoint

def hud():
    comp = Comp("quest-marker--hud", W, H, frames=F)
    comp.slot("primary", "#FFC83D")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    y0 = CY - 20
    # pulse ring
    comp.layer("pulse", [group([ngon(4, 70, 0), stroke(slot="primary", width=3)], "p")], position=bob(10, (CX, y0)),
               scale=anim([(0, [100, 100], DECEL), (30, [170, 170], HOLD), (30.01, [100, 100], DECEL), (F, [170, 170])]),
               opacity=anim([(0, 0, EASE_OUT), (3, 90, EASE_IN), (30, 0, HOLD), (30.01, 0, EASE_OUT), (33, 90, EASE_IN), (F, 0)]))
    comp.layer("waypoint", exclaim([fill(slot="primary")], [fill(slot="primary")], 0.42) + [
        group([ngon(4, 62, 0), stroke(slot="primary", width=5, join="miter")], "rim"),
        group([ngon(4, 62, 0), fill(slot="background", opacity=85)], "plate"),
        group([ngon(4, 76, 0), stroke(slot="outline", width=2, opacity=40)], "outer"),
    ], position=bob(10, (CX, y0)))
    comp.layer("stem", [group([seg((0, 0), (0, 90)), trim(end=100), stroke(slot="primary", width=3, dashes=[6, 8])], "s"),
                        group([ellipse((16, 16), (0, 96)), stroke(slot="primary", width=3)], "foot")],
               position=(CX, y0 + 80), scale=sampled(lambda t: [100, 100 - 10 * (0.5 + 0.5 * math.sin(TAU * t / F - math.pi / 2))], 0, F, 2))
    comp.layer("label bg", [group([rect((180, 40), (0, 0), 6), fill(slot="background", opacity=80),
                                   stroke(slot="outline", width=1.5, opacity=30)], "l")], position=(CX, SH + 6))
    return comp


build_asset(CAT, "quest-marker", "Quest Marker",
            "Floating RPG quest marker built from shapes: it bobs over a soft shadow with twinkles, on a loop. Place "
            "it above a character or spot in your footage.",
            ["quest", "marker", "exclamation", "question", "npc", "rpg", "gaming", "waypoint"], [
    Variant("classic", "Exclamation", classic(), "loop", thumb_t=0.5,
            description="Glossy gold exclamation mark with a dark outline, glow and ground shadow."),
    Variant("question", "Question", question(), "loop", thumb_t=0.5,
            description="Glossy blue question mark (quest turn-in) with the same bob and glow."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.5, bg="e8e8ee",
            description="8-bit exclamation sprite that bobs in pixel steps with blinking twinkles."),
    Variant("hud", "HUD Waypoint", hud(), "loop", thumb_t=0.2, text_area=(CX - 80, SH - 12, 160, 36),
            description="Modern diamond waypoint with a small exclamation, a pulse and a label for the distance."),
])
