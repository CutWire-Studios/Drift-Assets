"""Christmas lights string: a garland of twinkling bulbs on a swagged wire for the top of the frame."""

from _common import *

T = 60
BULBS = [("primary", "#E8332E"), ("secondary", "#27A452"), ("accent", "#FFC23D"), ("icon", "#2F80F6")]
WIRE = "#1F3A28"
BULB_D = "M 0 46 C 7 38 15 25 15 12 C 15 2 8 -3 0 -3 C -8 -3 -15 2 -15 12 C -15 25 -7 38 0 46 Z"


def swags(W, y, n, sag, lead=0):
    """Hook points for n swags spanning the width (starting slightly off-canvas)."""
    xs = [-lead + (W + 2 * lead) * i / n for i in range(n + 1)]
    return [((xs[i], y), (xs[i + 1], y), sag) for i in range(n)]


def wire_layers(comp, segs, width=4.5, color=WIRE, slot="outline", twist=True, name="wire"):
    items = []
    for j, (p0, p1, sag) in enumerate(segs):
        pts = sag_pts(p0, p1, sag, 24)
        items.append(group([path(smooth_open(pts)), stroke(color, width, slot=slot)], f"swag{j}"))
        if twist:  # second strand twisted around the first
            p2 = [(x, y + 3.2 * math.sin(i * 1.7)) for i, (x, y) in enumerate(sag_pts(p0, p1, sag, 48))]
            items.append(group([path(smooth_open(p2)), stroke(color, width * 0.55, slot=slot)], f"twist{j}"))
    comp.layer(name, items)


def along(segs, per_swag, inset=0.08):
    """(position, slope angle) of evenly spaced bulbs on each swag."""
    out = []
    for p0, p1, sag in segs:
        for i in range(per_swag):
            k = inset + (1 - 2 * inset) * (i + 0.5) / per_swag
            out.append((sag_at(p0, p1, sag, k), sag_slope(p0, p1, sag, k)))
    return out


# ---------------------------------------------------------------- classic C9 bulbs, chase

def classic():
    W, H = 1920, 220
    comp = Comp("christmas-lights-string", W, H, frames=T)
    for sid, c in BULBS:
        comp.slot(sid, c)
    comp.slot("outline", WIRE)
    segs = swags(W, 26, 4, 70, lead=20)
    r = rng(4)
    for i, ((x, y), ang) in enumerate(along(segs, 7)):
        sid, col = BULBS[i % 4]
        tilt = ang * 0.35 + r.uniform(-8, 8)
        phase = (i % 4) / 4

        def lit(t, phase=phase):
            # two chase steps per loop: each colour glows in turn with a soft ease
            u = (t / T * 2 - phase) % 1
            return 0.5 + 0.5 * math.cos(TAU * u)

        on = lambda t, lit=lit: 20 + 80 * lit(t) ** 2
        items = [
            group([ellipse((7, 14)), fill(WHITE, 75)], "spec", position=(-6, 12), rotation=18),
            group(S(BULB_D) + [fill("#000000", 100)], "dim", opacity=looped(lambda t: 34 - 34 * lit(t), T, 2)),
            group(S(BULB_D) + [shade_overlay((-15, -3, 15, 46), 0.8, dark="#000000")], "shade"),
            group(S(BULB_D) + [fill(col, slot=sid)], "bulb"),
            group([rect((16, 16), (0, -8), 3), fill("#2A4A33")], "socket"),
            group([rect((16, 4), (0, -4), 1), fill("#000000", 30)], "rim"),
            group([slot_glow(60, sid, col, 75, rings=9, position=(0, 20))], "halo",
                  opacity=looped(on, T, 2), scale=looped(lambda t: [80 + 25 * lit(t)] * 2, T, 2)),
        ]
        comp.layer(f"bulb{i}", items, position=(x, y), rotation=tilt, anchor=(0, -14), scale=(120, 120))
    wire_layers(comp, segs, 5)
    return comp


# ---------------------------------------------------------------- fairy lights: warm micro LEDs, twinkle

def fairy():
    W, H = 1920, 250
    warm = "#FFD580"
    comp = Comp("christmas-lights-string--fairy", W, H, frames=T * 2)
    TT = T * 2
    comp.slot("primary", "#FFF1C9")
    comp.slot("outline", "#8A6A3A")
    segs_a = swags(W, 20, 3, 120, lead=10)
    segs_b = [((p0[0], p0[1] + 4), (p1[0], p1[1] + 4), sag * 0.62) for p0, p1, sag in swags(W, 20, 3, 120, lead=10)]
    r = rng(9)
    pts = along(segs_a, 16, 0.02) + along(segs_b, 12, 0.03)
    for i, ((x, y), ang) in enumerate(pts):
        seed = r.randint(0, 999)
        base = r.uniform(0.35, 0.75)

        def lv(t, seed=seed, base=base):
            return clamp(base + 0.55 * flicker(t, TT, seed))

        comp.layer(f"led{i}", [
            group([ellipse((5, 5)), fill(WHITE)], "core"),
            group([ellipse((10, 10)), fill("#FFF1C9", slot="primary")], "led"),
            glow(30, warm, 100, position=(0, 0), name="bloom"),
        ], position=(x, y + 3), opacity=looped(lambda t, lv=lv: 30 + 70 * lv(t), TT, 3),
            scale=looped(lambda t, lv=lv: [70 + 45 * lv(t)] * 2, TT, 3))
    wire_layers(comp, segs_a, 2.2, "#8A6A3A", twist=False, name="wire-a")
    wire_layers(comp, segs_b, 2.2, "#8A6A3A", twist=False, name="wire-b")
    return comp


# ---------------------------------------------------------------- doodle: hand-drawn, blinking in pairs

def doodle():
    W, H = 960, 300
    comp = Comp("christmas-lights-string--doodle", W, H, frames=T)
    for sid, c in BULBS:
        comp.slot(sid, c)
    comp.slot("outline", INK)
    segs = swags(W, 34, 2, 110, lead=10)
    pts = along(segs, 4, 0.1)
    for i, ((x, y), ang) in enumerate(pts):
        sid, col = BULBS[i % 4]
        tilt = ang * 0.5
        blink = i % 2  # alternate halves blink

        def on(t, blink=blink):
            u = (t / T + blink * 0.5) % 1
            return 100 if u < 0.5 else 0

        bulb_pts = [(0, 50), (12, 36), (17, 16), (13, 2), (0, -2), (-13, 2), (-17, 16), (-12, 36)]
        rays = "M -30 14 L -44 10 M 30 14 L 44 10 M -24 42 L -34 52 M 24 42 L 34 52 M 0 62 L 0 74"
        items = [
            group(S(rays) + [stroke(INK, 4, slot="outline")], "rays",
                  opacity=Anim([(0, on(0), HOLD), (T / 2, on(T / 2), HOLD), (T, on(0), HOLD)])),
            group([boil_pts(bulb_pts, T, every=4, amp=1.6, seed=i + 1), stroke(INK, 5, slot="outline")], "line"),
            group([path(smooth_closed([(0, 44), (6, 20), (-4, 14)])), fill(WHITE, 80)], "spec",
                  position=(-4, 0)),
            group([path(smooth_closed(bulb_pts)), fill(col, slot=sid)], "bulb", position=(4, 4),
                  opacity=Anim([(0, 35 + 0.65 * on(0), HOLD), (T / 2, 35 + 0.65 * on(T / 2), HOLD),
                                (T, 35 + 0.65 * on(0), HOLD)])),
            group([boil_pts([(-9, -2), (9, -2), (9, -16), (-9, -16)], T, every=4, amp=1.2, seed=i + 50),
                   stroke(INK, 5, slot="outline")], "socket"),
            group([rect((18, 14), (1, -8)), fill("#6E8C5A")], "socket-fill"),
        ]
        comp.layer(f"bulb{i}", items, position=(x, y), rotation=tilt, anchor=(0, -14), scale=(150, 150))
    items = []
    for j, (p0, p1, sag) in enumerate(segs):
        pts2 = sag_pts(p0, p1, sag, 10)
        items.append(group([boil_pts(pts2, T, closed=False, every=4, amp=2.0, seed=90 + j),
                            stroke(INK, 5, slot="outline")], f"swag{j}"))
    comp.layer("wire", items)
    return comp


build("christmas-lights-string", "Christmas Lights String",
      "A string of twinkling Christmas lights swagged across the top of the frame; a seamless loop that "
      "sits over the top edge of your video.",
      ["christmas", "lights", "garland", "holiday", "festive", "border", "twinkle"], [
          Variant("classic", "Classic Bulbs", classic(), "loop", thumb_t=0.12, region=(700, 0, 520, 220),
                  description="Multicolour glass bulbs on a twisted green wire, glowing in a chase pattern."),
          Variant("fairy", "Fairy Lights", fairy(), "loop", thumb_t=0.3, region=(640, 0, 640, 250),
                  description="Two strands of warm-white micro lights that twinkle softly with a golden bloom."),
          Variant("doodle", "Doodle", doodle(), "loop", thumb_t=0.2, bg="f3ece0",
                  description="Hand-drawn bulbs on a wobbly ink wire that blink in alternating pairs."),
      ])
