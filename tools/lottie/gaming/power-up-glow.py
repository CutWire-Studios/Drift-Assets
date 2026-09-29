import random

from _gaming2 import *

W, H, F = 480, 560, 60
C = (W / 2, 250)
ABS = 20          # absorb starts
GONE = 27         # orb gone, flash
RING_T = [24, 31, 38]
BOLT = "M4 -30 L-16 4 L-2 4 L-6 30 L16 -6 L2 -6 Z"


def orb_scale(base=100):
    def f(t):
        if t < 10:
            return [base * back_out(t / 10)] * 2
        if t < ABS:
            return [base * (1 + 0.05 * math.sin((t - 10) * 0.8))] * 2
        if t < ABS + 3:
            return [base * (1 + 0.18 * ease_out((t - ABS) / 3))] * 2
        return [base * 1.18 * (1 - ease_in(clamp((t - ABS - 3) / (GONE - ABS - 3)), 2.5))] * 2
    return sampled(f, 0, GONE, 1)


def orb_pos():
    return sampled(lambda t: [C[0], C[1] - 8 * math.sin(t / 6)] if t < ABS else [C[0], C[1] - 8 * math.sin(ABS / 6)], 0, GONE, 2)


def rising_rings(comp, shapes_fn, y0=470, y1=90, dur=24, hold=False):
    for k, t0 in enumerate(RING_T):
        def fn(u):
            e = u / dur
            y = lerp(y0, y1, ease_out(e, 1.6))
            s = lerp(120, 70, e)
            if hold:
                y, s = snap(y, 10), snap(s, 10)
            return {"position": [C[0], y], "scale": [s, s], "opacity": 100 * bump(e, 0, 1) ** 0.5}
        particle(comp, "ring", shapes_fn(k), t0, dur, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


def inward(comp, shapes, n=12, seed=2, hold=False):
    """Motes sucked into the orb while it's absorbed... then shot upward."""
    rng = random.Random(seed)
    for i in range(n):
        a = rng.uniform(0, 360)
        r = rng.uniform(120, 200)
        t0 = rng.randint(4, ABS - 2)
        life = GONE - t0

        def fn(u, a=a, r=r, life=life):
            e = ease_in(u / life, 2)
            p = pt(r * (1 - e), a + 90 * e, C)
            if hold:
                p = (snap(p[0], 8), snap(p[1], 8))
            return {"position": list(p), "scale": [lerp(60, 110, e)] * 2, "opacity": 100 * min(1, u / 4)}
        particle(comp, "mote in", shapes, t0, life, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


def upward(comp, shapes, n=16, seed=5, hold=False):
    rng = random.Random(seed)
    for i in range(n):
        x = C[0] + rng.uniform(-110, 110)
        y = rng.uniform(380, 470)
        t0 = GONE + rng.randint(-2, 16)
        life = rng.randint(16, 24)
        rise = rng.uniform(180, 320)

        def fn(u, x=x, y=y, life=life, rise=rise):
            k = u / life
            yy = y - rise * ease_out(k, 1.5)
            if hold:
                return {"position": [snap(x, 8), snap(yy, 8)], "opacity": 100 if k < 0.8 else 0}
            return {"position": [x, yy], "scale": [100 * (1 - k)] * 2, "opacity": 100 * bump(k, 0, 1) ** 0.4}
        particle(comp, "mote up", shapes, t0, life, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


def flash(comp, color, d=380):
    comp.layer("flash", [glow(d * 1.3, color, 1.0)], position=C, ip=GONE - 2, op=GONE + 14,
               scale=anim([(GONE - 2, [20, 20], SNAP_OUT), (GONE + 4, [110, 110], EASE_OUT), (GONE + 14, [130, 130])]),
               opacity=anim([(GONE - 2, 100, EASE_IN), (GONE + 14, 0)]))


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("power-up-glow", W, H, frames=F)
    comp.slot("primary", "#35E0FF")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("accent", "#FFE14D")
    upward(comp, [group([spark(12), fill(slot="secondary")], "s"), glow(28, "#9CF0FF", 0.6)])
    rising_rings(comp, lambda k: [group([ellipse((260, 70)), stroke(slot="primary", width=6)], "r"),
                                  group([ellipse((260, 70)), stroke(slot="primary", width=22, opacity=18)], "g"),
                                  group([ellipse((260, 70)), fill(slot="primary", opacity=10)], "f")])
    flash(comp, "#BFF6FF")
    inward(comp, [group([spark(9), fill(slot="secondary")], "s")])
    orb = comp.null("orb", position=orb_pos(), scale=orb_scale(145), op=GONE)
    comp.layer("bolt", [group([*svg_shapes(BOLT, 1.4), fill(slot="accent"), stroke("#FFFFFF", width=3)], "b")], parent=orb,
               op=GONE, rotation=sampled(lambda t: 6 * math.sin(t / 4), 0, GONE, 2))
    comp.layer("orbit", [group([ellipse((170, 50)), trim(start=0, end=40, offset=anim([(0, 0, LINEAR), (GONE, 360)])),
                                stroke("#FFFFFF", width=4)], "o1", rotation=-20),
                         group([ellipse((170, 50)), trim(start=0, end=30, offset=anim([(0, 180, LINEAR), (GONE, -180)])),
                                stroke(slot="primary", width=3)], "o2", rotation=25)], parent=orb, op=GONE)
    comp.layer("orb", [
        group([ellipse((46, 30), (-22, -32)), fill("#FFFFFF", 60)], "spec"),
        group([ellipse((120, 120)), gradient_fill([(0, "#FFFFFF", 0.9), (0.45, "#BFF6FF", 0.55), (1, "#35E0FF", 0.0)], (0, 0), (60, 0),
                                                  radial=True)], "core"),
        group([ellipse((120, 120)), fill(slot="primary", opacity=70)], "body"),
        group([ellipse((120, 120)), stroke("#FFFFFF", width=3, opacity=80)], "rim"),
        glow(260, "#35E0FF", 0.55),
    ], parent=orb, op=GONE)
    return comp


# ---------------------------------------------------------------- pixel

ORB_PIX = [
    "....KKKKKK....",
    "..KKOOOOOOKK..",
    ".KOOWWOOOOOOK.",
    ".KOWWOOOOOOOK.",
    "KOOWOOOYYOOOOK",
    "KOOOOOYYYYOOOK",
    "KOOOYYYYYYYYOK",
    "KOOOOYYYYYYOOK",
    "KOOOOOYYYYOOOK",
    "KOOOOYYOOYYOOK",
    ".KOOOYOOOOYOK.",
    ".KDOOOOOOOODK.",
    "..KKDDDDDDKK..",
    "....KKKKKK....",
]


def pixel():
    comp = Comp("power-up-glow--pixel", W, H, frames=F)
    comp.slot("primary", "#FF4D9A")
    comp.slot("secondary", "#FFD23F")
    comp.slot("outline", INK)
    P = 10
    upward(comp, [box(-5, -5, 10, 10, slot="secondary")], hold=True)
    rising_rings(comp, lambda k: [pix_group(pix_cells(lambda x, y: 0.5 <= (x / 13) ** 2 + (y / 3.6) ** 2 < 1.0, 28), P, (-14 * P, -14 * P),
                                            ("slot", "primary" if k % 2 == 0 else "secondary"), "r")], hold=True)
    comp.layer("flash", [pix_group(pix_cells(lambda x, y: x * x + y * y <= 12 ** 2, 26), P, (-13 * P, -13 * P), "#FFFFFF", "f")],
               position=C, ip=GONE - 1, op=GONE + 6, scale=stepped(lambda t: [60 + 30 * (t - GONE + 1) // 2] * 2, GONE - 1, GONE + 6, 2))
    inward(comp, [box(-5, -5, 10, 10, "#FFFFFF")], hold=True)
    orb_pos_ = stepped(lambda t: [C[0], C[1] - (P if (t // 8) % 2 else 0)], 0, GONE, 2)
    comp.layer("orb", pix(ORB_PIX, {"W": "#FFFFFF", "Y": ("slot", "secondary"), "D": ("#000000", 30), "O": ("slot", "primary"),
                                    "K": ("slot", "outline")}, 14, order=list("WYDOK")),
               position=orb_pos_, op=GONE,
               scale=stepped(lambda t: [0, 0] if t < 2 else [60, 60] if t < 4 else [115, 115] if t < 6 else [100, 100] if t < ABS
                             else [120, 120] if t < ABS + 2 else [80, 80] if t < ABS + 4 else [50, 50] if t < GONE - 1 else [25, 25],
                             0, GONE, 1))
    comp.layer("halo", [pix_group(pix_cells(lambda x, y: 11 ** 2 <= x * x + y * y < 12.2 ** 2, 26), P, (-13 * P, -13 * P),
                                  ("slot", "secondary"), "h")], position=orb_pos_, op=ABS,
               opacity=stepped(lambda t: 100 if (t // 4) % 2 else 0, 0, ABS, 1))
    return comp


# ---------------------------------------------------------------- fantasy

def fantasy():
    comp = Comp("power-up-glow--fantasy", W, H, frames=F)
    comp.slot("primary", "#39E08A")
    comp.slot("secondary", GOLD)
    comp.slot("accent", "#E9FFF3")
    upward(comp, [group([spark(13), fill(slot="secondary")], "s"), glow(30, "#FFE9A3", 0.6)], seed=8)
    runes = lambda k: [group([ellipse((250, 64)), stroke(slot="secondary", width=4)], "r"),
                       group([ellipse((220, 54)), stroke(slot="primary", width=2, dashes=[10, 12])], "d"),
                       group([ellipse((250, 64)), stroke(slot="primary", width=18, opacity=16)], "g")]
    rising_rings(comp, runes)
    flash(comp, "#C8FFE0")
    # spiralling motes
    rng = random.Random(4)
    for i in range(10):
        ph = i * 36
        t0 = rng.randint(0, 6)

        def fn(u, ph=ph):
            e = clamp(u / (GONE - t0))
            r = 120 * (1 - ease_in(e, 1.5))
            p = pt(r, ph + 400 * e, C)
            return {"position": [p[0], C[1] + (p[1] - C[1]) * 0.5], "scale": [lerp(60, 110, e)] * 2}
        particle(comp, "spiral", [group([spark(10), fill(slot="accent")], "s")], t0, GONE - t0, F, fn, wrap=False)
    orb = comp.null("orb", position=orb_pos(), scale=orb_scale(145), op=GONE)
    comp.layer("rune", [group([ngon(4, 26, 0), stroke(slot="secondary", width=4, join="miter")], "d"),
                        group([ngon(4, 10, 0), fill(slot="secondary")], "c"),
                        group([seg((0, -40), (0, -30)), seg((0, 30), (0, 40)), seg((-40, 0), (-30, 0)), seg((30, 0), (40, 0)),
                               stroke(slot="secondary", width=4)], "ticks")], parent=orb, op=GONE,
               rotation=sampled(lambda t: t * 3, 0, GONE, 3))
    comp.layer("orb", [
        group([ellipse((40, 24), (-24, -34)), fill("#FFFFFF", 55)], "spec"),
        group([ellipse((130, 130)), gradient_fill([(0, "#FFFFFF", 0.7), (0.5, "#9BFFC8", 0.3), (1, "#39E08A", 0)], (0, 0), (65, 0),
                                                  radial=True)], "core"),
        group([ellipse((130, 130)), fill(slot="primary", opacity=75)], "body"),
        group([ellipse((138, 138)), stroke(slot="secondary", width=5)], "gold rim"),
        group([ellipse((138, 138)), stroke(GOLD_D, width=9)], "rim edge"),
        glow(280, "#39E08A", 0.5),
    ], parent=orb, op=GONE)
    return comp


build_asset(CAT, "power-up-glow", "Power-Up Glow",
            "A glowing power-up orb hovers, gets absorbed in a flash and sends rings of energy rising up, like a "
            "character powering up. One-shot that ends empty.",
            ["power up", "powerup", "orb", "buff", "energy", "glow", "gaming", "boost"], [
    Variant("modern", "Energy", modern(), "intro-hold", thumb_t=0.2,
            description="Cyan energy orb with a lightning bolt and orbiting streaks; glowing rings rise after the flash."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.2, bg="e8e8ee",
            description="8-bit orb with a star inside that shrinks in steps, then pixel rings and motes rise."),
    Variant("fantasy", "Magic", fantasy(), "intro-hold", thumb_t=0.2,
            description="Green magic orb in a gold rim with a rune, spiralling sparkles and golden rune rings rising."),
])
