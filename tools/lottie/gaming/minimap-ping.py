import random

from _gaming2 import *

W = H = 440
F = 90
C = (W / 2, H / 2)
R = 176
BLIPS = [(-80, -70), (96, -30), (-40, 92), (60, 110)]
PING = (70, -92)


def blip_angle(p):
    return math.degrees(math.atan2(p[0], -p[1])) % 360


def sweep_hit(p):
    """Frame at which the sweep (starting up, clockwise, one turn per loop) passes p."""
    return blip_angle(p) / 360 * F


def blip_opacity(p, lo=15, hold=False):
    th = sweep_hit(p)

    def f(t):
        d = (t - th) % F
        return lo + (100 - lo) * (1 - d / F) ** 2.2 if d < F else lo
    return (stepped if hold else sampled)(f, 0, F, 2 if hold else 1)


def wedge_shapes(n=12, span=64, color=None, slot=None, amax=55, r=R):
    out = []
    for k in range(n):
        a0 = -span * (k + 1) / n
        a1 = -span * k / n + 0.6
        pts = [(0, 0)] + arc_pts(r, a0, a1, 6)
        op = amax * (1 - k / n) ** 1.6
        out.append(group([poly(pts), fill(color or "#FFFFFF", op, slot=slot)], f"w{k}"))
    return out


def ping_rings(comp, shapes_fn, pos, n=2, d0=10, d1=120, hold=False):
    for k in range(n):
        t0 = k * F / n

        def fn(u):
            e = ease_out(u / (F / n), 2)
            d = lerp(d0, d1, e)
            if hold:
                d = snap(d, 12)
            return {"scale": [d, d], "opacity": 100 * (1 - u / (F / n))}
        particle(comp, "ping ring", shapes_fn(), round(t0), round(F / n), F, fn, step=2 if hold else 1, hold=hold,
                 position=(C[0] + pos[0], C[1] + pos[1]))


def terrain(slot_fill, op=18):
    rng = random.Random(3)
    blocks = []
    for i in range(14):
        x, y = rng.uniform(-150, 150), rng.uniform(-150, 150)
        w, h = rng.uniform(26, 70), rng.uniform(20, 60)
        blocks.append(rect((w, h), (x, y), 4))
    roads = [seg((-R, 30), (R, -10)), seg((-20, -R), (10, R)), seg((-R, -120), (40, 150))]
    return [group(blocks + [fill(slot=slot_fill, opacity=op)], "blocks"),
            group(roads + [stroke(slot=slot_fill, width=10, opacity=op * 0.8)], "roads")]


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("minimap-ping", W, H, frames=F)
    comp.slot("primary", "#35E0FF")
    comp.slot("secondary", "#FFC83D")
    comp.slot("accent", "#FF4555")
    comp.slot("background", "#0E141C")
    comp.slot("outline", "#FFFFFF")
    # ping pin (bobbing diamond)
    pp = (C[0] + PING[0], C[1] + PING[1])
    comp.layer("pin", [group([poly([(0, -28), (14, -14), (0, 6), (-14, -14)]), fill(slot="secondary"),
                              stroke("#000000", width=2, opacity=40)], "pin"),
                       group([ellipse((10, 10), (0, -14)), fill(slot="background")], "dot")],
               position=loop(F, [[pp[0], pp[1] - 2], [pp[0], pp[1] - 10]] * 2, EASE_IN_OUT))
    ping_rings(comp, lambda: [group([ellipse((100, 100)), stroke(slot="secondary", width=3)], "r"),
                              group([ellipse((100, 100)), fill(slot="secondary", opacity=12)], "f")], PING, n=3, d0=8, d1=110)
    # player arrow
    comp.layer("player", [group([poly([(0, -16), (12, 12), (0, 5), (-12, 12)]), fill("#FFFFFF"),
                                 stroke(slot="background", width=3)], "arrow"),
                          glow(60, "#FFFFFF", 0.35)],
               position=C, rotation=loop(F, [0, 8, 0, -8]))
    for i, b in enumerate(BLIPS):
        comp.layer("blip", [glow(34, "#FF4555", 0.6), group([ellipse((13, 13)), fill(slot="accent")], "d")],
                   position=(C[0] + b[0], C[1] + b[1]), opacity=blip_opacity(b))
    comp.layer("sweep", [group([seg((0, 0), (0, -R)), stroke(slot="primary", width=3)], "line")] +
               wedge_shapes(slot="primary", amax=45), position=C,
               rotation=anim([(0, 0, LINEAR), (F, 360)]))
    # map content clipped to the disc
    comp.layer("map matte", [group([ellipse((2 * R, 2 * R)), fill()], "m")], position=C)
    comp.layer("map", terrain("primary", 7) + [
        group([seg((-R, y), (R, y)) for y in range(-160, 170, 40)] + [seg((x, -R), (x, R)) for x in range(-160, 170, 40)] +
              [stroke(slot="primary", width=1, opacity=14)], "grid")], matte="alpha", position=C)
    ticks = [group([seg(pt(R + 6, a), pt(R + (18 if a % 90 == 0 else 12), a))], f"t{a}") for a in range(0, 360, 15)]
    comp.layer("bezel", [
        group([poly([pt(R + 30, 0), pt(R + 16, -5), pt(R + 16, 5)]), fill(slot="primary")], "north"),
        group(ticks + [stroke(slot="outline", width=2, opacity=50, cap="butt")], "ticks"),
        group([ellipse((2 * R + 4, 2 * R + 4)), stroke(slot="primary", width=3)], "rim"),
        group([ellipse((2 * R + 44, 2 * R + 44)), stroke(slot="outline", width=1.5, opacity=25)], "outer"),
        group([ellipse((2 * R + 40, 2 * R + 40)), fill("#000000", 40)], "bezel"),
        group([ellipse((2 * R, 2 * R)), fill(slot="background", opacity=88)], "disc"),
    ], position=C)
    return comp


# ---------------------------------------------------------------- pixel

def pixel():
    comp = Comp("minimap-ping--pixel", W, H, frames=F)
    comp.slot("primary", "#4DFF7A")
    comp.slot("secondary", "#FFD23F")
    comp.slot("accent", "#FF4D5E")
    comp.slot("background", "#1B2A24")
    comp.slot("outline", INK)
    P = 8
    n = 44
    rad = 21
    o = (C[0] - n * P / 2, C[1] - n * P / 2)
    ring = lambda r0, r1: pix_cells(lambda x, y: r0 ** 2 <= x * x + y * y < r1 ** 2, n)
    # pixel pin + stepped ping
    pp = (C[0] + snap(PING[0], P), C[1] + snap(PING[1], P))
    PIN = ["..KKK..", ".KYYYK.", "KYWYYYK", "KYYYYYK", ".KYYYK.", "..KYK..", "...K..."]
    comp.layer("pin", pix(PIN, {"W": "#FFFFFF", "Y": ("slot", "secondary"), "K": ("slot", "outline")}, 5, order=list("WYK")),
               position=stepped(lambda t: [pp[0], pp[1] - 16 - (5 if (t // 15) % 2 else 0)], 0, F, 15))
    for k in range(3):
        rr = 3 + k * 3
        cells = pix_cells(lambda x, y, rr=rr: (rr - 1) ** 2 <= x * x + y * y < rr ** 2, 2 * rr)
        comp.layer("ping", [pix_group(cells, 6, (-rr * 6, -rr * 6), ("slot", "secondary"), "r")], position=pp,
                   opacity=stepped(lambda t, k=k: 100 if ((t // 5) % 6) == k else 0, 0, F, 1))
    comp.layer("player", pix(["...W...", "..WWW..", ".WWWWW.", "WWW.WWW", "WW...WW"], {"W": "#FFFFFF"}, 5),
               position=C)
    for b in BLIPS:
        bp = (C[0] + snap(b[0], P), C[1] + snap(b[1], P))
        comp.layer("blip", [box(-P, -P, 2 * P, 2 * P, slot="accent")], position=bp, opacity=blip_opacity(b, 0, hold=True))
    # sweep: 16 stepped positions
    comp.layer("sweep", [group([rect((P, R - 8), (0, -(R - 8) / 2)), fill(slot="primary")], "line")] +
               wedge_shapes(n=4, span=45, slot="primary", amax=40, r=R - 8),
               position=C, rotation=stepped(lambda t: 360 * math.floor(t / F * 16) / 16, 0, F, 1))
    grid = [(c, r) for c, r in ring(0, rad - 1) if (c % 8 == 2 or r % 8 == 2)]
    comp.layer("map", [pix_group(grid, P, o, ("slot", "primary", 12), "grid"),
                       pix_group(ring(rad - 1, rad), P, o, ("slot", "primary"), "rim"),
                       pix_group(ring(rad, rad + 1.5), P, o, ("slot", "outline"), "rim2"),
                       pix_group(ring(0, rad), P, o, ("slot", "background"), "disc")])
    comp.layer("north", [box(-P, -P, 2 * P, 2 * P, slot="secondary"), box(-2 * P, -2 * P, 4 * P, 4 * P, slot="outline")],
               position=(C[0], C[1] - (rad + 0.5) * P))
    return comp


# ---------------------------------------------------------------- radar (phosphor)

def radar():
    comp = Comp("minimap-ping--radar", W, H, frames=F)
    comp.slot("primary", "#3DFF8B")
    comp.slot("secondary", "#FFE45C")
    comp.slot("background", "#04140B")
    pp = (C[0] + PING[0], C[1] + PING[1])
    ping_rings(comp, lambda: [group([ellipse((100, 100)), stroke(slot="secondary", width=2.5)], "r"),
                              group([ellipse((100, 100)), stroke(slot="secondary", width=8, opacity=20)], "g")],
               PING, n=2, d0=10, d1=150)
    comp.layer("ping core", [glow(40, "#FFE45C", 0.8), group([ellipse((10, 10)), fill(slot="secondary")], "d")],
               position=pp, scale=loop(F, [[100, 100], [140, 140]] * 3))
    for b in BLIPS:
        comp.layer("blip", [glow(40, "#3DFF8B", 0.7), group([ellipse((11, 11)), fill("#DFFFE9")], "d")],
                   position=(C[0] + b[0], C[1] + b[1]), opacity=blip_opacity(b, 0))
    comp.layer("sweep", [group([seg((0, 0), (0, -R)), stroke("#DFFFE9", width=2.5)], "line"),
                         group([seg((0, 0), (0, -R)), stroke(slot="primary", width=10, opacity=35)], "glow")] +
               wedge_shapes(n=16, span=110, slot="primary", amax=40), position=C,
               rotation=anim([(0, 0, LINEAR), (F, 360)]))
    rings_ = [group([ellipse((d, d))], f"r{d}") for d in (2 * R / 4, 2 * R / 2, 2 * R * 3 / 4)]
    ticks = [group([seg(pt(R - 8, a), pt(R, a))], f"t{a}") for a in range(0, 360, 10)]
    comp.layer("scope", [
        group(rings_ + [seg((-R, 0), (R, 0)), seg((0, -R), (0, R)), stroke(slot="primary", width=1.5, opacity=35)], "grid"),
        group(ticks + [stroke(slot="primary", width=2, opacity=60)], "ticks"),
        group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=3)], "rim"),
        group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=14, opacity=14)], "rim glow"),
        group([ellipse((2 * R, 2 * R)), gradient_fill([(0, "#0B3A20", 0.9), (1, "#04140B", 0.95)], (0, 0), (R, 0), radial=True)],
              "disc"),
    ], position=C)
    return comp


build_asset(CAT, "minimap-ping", "Minimap Ping",
            "Circular minimap with a radar sweep that lights up blips as it passes and a ping marker rippling on the "
            "map, on a loop.",
            ["minimap", "radar", "map", "ping", "sweep", "gaming", "hud", "marker"], [
    Variant("modern", "Modern", modern(), "loop", thumb_t=0.3,
            description="Dark translucent map with a cyan sweep, compass bezel, player arrow and a bobbing ping pin."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.3, bg="e8e8ee",
            description="8-bit round map with a sweep that ticks round in 16 steps and stepped ping rings."),
    Variant("radar", "Radar", radar(), "loop", thumb_t=0.3,
            description="Green phosphor radar scope with range rings, a glowing sweep trail and a yellow ping."),
])
