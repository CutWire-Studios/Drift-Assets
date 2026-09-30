import random

from _gaming2 import *

F = 90
HITS = [12, 28, 42, 54, 64]
MAXT = HITS[-1]


def level_keys(steps=5, e=SPRING, dur=8, lo=0.0, hi=1.0):
    keys = [(0, lo, HOLD)]
    for i, h in enumerate(HITS):
        keys.append((h, lo + (hi - lo) * i / steps, e))
        keys.append((h + dur, lo + (hi - lo) * (i + 1) / steps, HOLD))
    keys.append((F, hi, HOLD))
    return keys


def punch(base=100, amp=14, intro=(0, 10)):
    def f(t):
        if t < intro[1]:
            return [base * back_out(clamp((t - intro[0]) / (intro[1] - intro[0])))] * 2
        v = 0.0
        for i, h in enumerate(HITS):
            d = t - h
            a = amp * (1.6 if i == len(HITS) - 1 else 1)
            if 0 <= d < 2:
                v = max(v, a * d / 2)
            elif d >= 2:
                v = max(v, a * math.exp(-(d - 2) / 3.5) * math.cos((d - 2) / 3))
        return [base + v] * 2
    return sampled(f, 0, F, 1)


def hit_flash(peak=100, dur=8):
    def f(t):
        v = 0
        for h in HITS:
            d = t - h
            if 0 <= d < dur:
                v = max(v, peak * (1 - d / dur))
        return v
    return sampled(f, 0, F, 1)


def max_burst(comp, c, shapes, n=12, r0=40, r1=170, seed=2, hold=False):
    rng = random.Random(seed)
    for i in range(n):
        a = i * 360 / n + rng.uniform(-8, 8)
        r = rng.uniform(r1 * 0.7, r1)
        life = rng.randint(14, 20)

        def fn(u, a=a, r=r, life=life):
            e = ease_out(u / life)
            p = pt(lerp(r0, r, e), a, c)
            if hold:
                p = (snap(p[0], 5), snap(p[1], 5))
            return {"position": list(p), "scale": [100 * (1 - ease_in(u / life))] * 2, "rotation": 120 * u / life}
        particle(comp, "max spark", shapes, MAXT + 2, life, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


# ---------------------------------------------------------------- modern: radial gauge

def modern():
    W = H = 420
    C = (W / 2, H / 2 + 14)
    R = 150
    A0, A1 = -125, 125
    comp = Comp("combo-meter", W, H, frames=F)
    comp.slot("primary", "#FF7A1A")
    comp.slot("secondary", "#FFD23F")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    lv = level_keys()
    max_burst(comp, C, [group([spark(14), fill(slot="secondary")], "s")], r0=R - 20, r1=R + 60)
    # arc head spark
    def head(t):
        for (t0, v0, e), (t1, v1, _) in zip(lv, lv[1:]):
            if t0 <= t <= t1:
                u = 0 if e == HOLD else back_out((t - t0) / (t1 - t0), 1.6)
                return pt(R, A0 + (A1 - A0) * clamp(lerp(v0, v1, u), 0, 1.02), C)
        return pt(R, A1, C)
    comp.layer("head", [group([spark(18), fill("#FFFFFF")], "s"), glow(70, "#FFE2B0", 0.7)],
               position=sampled(lambda t: list(head(t)), 0, F, 1), ip=HITS[0] + 1,
               opacity=hit_flash(100, 14))
    ring = comp.null("ring", position=C, scale=punch(100, 5))
    comp.layer("arc flash", [group([arc(R, A0, A1, 64), trim(end=anim([(t, v * 100, e) for t, v, e in lv])),
                                    stroke("#FFFFFF", width=26, cap="butt")], "f")], parent=ring, opacity=hit_flash(80, 7))
    comp.layer("arc fill", [
        group([arc(R, A0, A1, 64), trim(end=anim([(t, v * 100, e) for t, v, e in lv])),
               stroke(slot="secondary", width=8, cap="butt")], "hi", scale=(96.5, 96.5)),
        group([arc(R, A0, A1, 64), trim(end=anim([(t, v * 100, e) for t, v, e in lv])),
               stroke(slot="primary", width=26, cap="butt")], "fill"),
    ], parent=ring)
    ticks = [group([seg(pt(R - 13, a), pt(R + 13, a))], f"t{i}") for i, a in
             enumerate(A0 + (A1 - A0) * k / 5 for k in range(1, 5))]
    comp.layer("ticks", [group(ticks + [stroke(slot="background", width=4, cap="butt")], "ticks")], parent=ring)
    comp.layer("track", [
        group([arc(R, A0, A1, 64), stroke(slot="background", width=26, cap="butt", opacity=88)], "track"),
        group([arc(R, A0, A1, 64), stroke(slot="outline", width=32, cap="butt", opacity=22)], "rim"),
    ], parent=ring, opacity=fade(0, 8))
    # centre disc
    disc = comp.null("disc", position=C, scale=punch(100, 12))
    comp.layer("max ring", [group([ellipse((212, 212)), stroke(slot="secondary", width=anim([(MAXT, 10, EASE_OUT), (MAXT + 20, 1)]))], "r")],
               parent=disc, ip=MAXT, op=MAXT + 21, scale=anim([(MAXT, [100, 100], DECEL), (MAXT + 20, [170, 170])]),
               opacity=anim([(MAXT, 100, EASE_IN), (MAXT + 20, 0)]))
    comp.layer("disc flash", [group([ellipse((196, 196)), fill("#FFFFFF")], "f")], parent=disc, opacity=hit_flash(16, 6))
    comp.layer("disc", [
        group([ellipse((184, 184)), stroke(slot="primary", width=3)], "inner"),
        group([ellipse((196, 196)), sheen(196, 196, 0.16, 0.25)], "gloss"),
        group([ellipse((196, 196)), fill(slot="background", opacity=92)], "disc"),
        group([ellipse((196, 196), (0, 8)), fill("#000000", 30)], "shadow"),
    ], parent=disc)
    return comp, (C[0] - 70, C[1] - 42, 140, 84)


# ---------------------------------------------------------------- pixel: block bar

FIST = [
    ".....K.....",
    "....KYK....",
    "....KWK....",
    "KKKKYWYKKKK",
    "KYYYWYYYYOK",
    ".KYYYYYYOK.",
    "..KYYYYOK..",
    "..KYYKYOK..",
    ".KYYK.KYOK.",
    ".KYK...KOK.",
    ".KK.....KK.",
]
BOLT_PIX = [
    ".....KKK",
    "....KYYK",
    "...KYYK.",
    "..KYYKKK",
    ".KYYYYYK",
    "KKKKYYK.",
    "...KYK..",
    "..KYK...",
    "..KK....",
]


def pixel():
    W, H = 580, 200
    comp = Comp("combo-meter--pixel", W, H, frames=F)
    comp.slot("primary", "#FF5A36")
    comp.slot("secondary", "#FFD23F")
    comp.slot("outline", INK)
    comp.slot("background", "#2B2140")
    PX = 7
    Y = 118
    BX, SW, BH = 138, 58, 44
    shake = lambda t: [snap(4 * ((-1) ** int(t)) if any(0 <= t - h < 4 for h in HITS) else 0, 1), 0]
    rig = comp.null("rig", position=stepped(shake, 0, F, 1))
    max_burst(comp, (BX + 5 * SW / 2, Y), [box(-6, -6, 12, 12, slot="secondary")], r0=30, r1=200, hold=True)
    for i, h in enumerate(HITS):
        x = BX + i * SW
        hh = BH * (0.55 + 0.45 * i / 4)
        on = stepped(lambda t, h=h: [0, 0] if t < h else [140, 140] if t < h + 2 else [85, 85] if t < h + 4 else [100, 100],
                     0, F, 1)
        fl = stepped(lambda t, h=h: 100 if h <= t < h + 4 or (t >= MAXT and (t - MAXT) % 6 < 2 and t < MAXT + 18) else 0, 0, F, 1)
        comp.layer("flash", [box(-SW / 2 + 5, -hh, SW - 10, hh, "#FFFFFF")], parent=rig, position=(x + SW / 2, Y + BH / 2),
                   scale=on, opacity=fl)
        comp.layer("block", [box(-SW / 2 + 5, -hh, SW - 10, 6, "#FFFFFF", opacity=55),
                             box(-SW / 2 + 5, -8, SW - 10, 6, "#000000", opacity=25),
                             box(-SW / 2 + 5, -hh, SW - 10, hh, slot="secondary" if i == 4 else "primary"),
                             box(-SW / 2, -hh - 5, SW, hh + 10, slot="outline")],
                   parent=rig, position=(x + SW / 2, Y + BH / 2), scale=on)
        comp.layer("slot", [box(-SW / 2 + 5, -hh, SW - 10, hh, slot="background"),
                            box(-SW / 2, -hh - 5, SW, hh + 10, slot="outline")], parent=rig,
                   position=(x + SW / 2, Y + BH / 2), opacity=stepped(lambda t, i=i: 0 if t < 2 + i * 2 else 100, 0, 14, 1))
    comp.layer("icon", pix(FIST, {"W": "#FFFFFF", "O": ("slot", "primary"), "Y": ("slot", "secondary"), "K": ("slot", "outline")},
                           PX, order=list("WOYK")), parent=rig, position=(66, Y - 4),
               scale=stepped(lambda t: [0, 0] if t < 2 else [120, 120] if t < 4 or any(0 <= t - h < 3 for h in HITS)
                             else [100, 100], 0, F, 1))
    comp.layer("bolt", pix(BOLT_PIX, {"Y": ("slot", "secondary"), "K": ("slot", "outline")}, 5, order=list("YK")),
               parent=rig, position=(BX + 5 * SW + 30, Y - 50),
               opacity=stepped(lambda t: 0 if t < MAXT else 100 if (t - MAXT) % 8 < 5 or t > MAXT + 24 else 0, 0, F, 1))
    return comp, (BX, 18, 5 * SW, 44)


# ---------------------------------------------------------------- neon: rising skewed bars

def neon_v():
    W, H = 560, 300
    comp = Comp("combo-meter--neon", W, H, frames=F)
    comp.slot("primary", MAGENTA)
    comp.slot("secondary", NCYAN)
    BASE = 250
    X0, SW = 70, 58
    max_burst(comp, (X0 + 2 * SW + 20, 150), [group([spark(12), fill("#FFFFFF")], "s")], r0=40, r1=220, seed=6)
    for i, h in enumerate(HITS):
        hh = 60 + i * 38
        x = X0 + i * SW
        shape = [skew_rect(36, hh, 16, (x, BASE - hh / 2))]
        slot = "primary" if i < 4 else "secondary"
        flick = anim([(0, 0, HOLD), (h, 100, HOLD), (h + 1, 30, HOLD), (h + 2, 100, HOLD), (h + 3, 50, HOLD), (h + 4, 100, HOLD),
                      (F, 100)])
        comp.layer("bar", [group(shape + [fill("#FFFFFF", 90)], "core", opacity=anim([(0, 0, HOLD), (h, 100, EASE_OUT), (h + 8, 0, HOLD), (F, 0)])),
                           group(shape + [fill(slot=slot, opacity=55)], "fill")] + neon(shape, slot=slot, w=3.5),
                   opacity=flick, anchor=(x, BASE), position=(x, BASE),
                   scale=anim([(h, [100, 20], SPRING), (h + 10, [100, 100])]))
        comp.layer("ghost", neon(shape, slot=slot, w=1.5, core=False, glow_a=0.2), opacity=anim([(0, 0, EASE_OUT), (8, 45, HOLD),
                                                                                                (h, 45, HOLD), (h + 1, 0)]))
    comp.layer("base", neon([seg((30, BASE + 14), (X0 + 4 * SW + 50, BASE + 14))], slot="secondary", w=3),
               scale=anim([(0, [0, 100], SNAP_OUT), (12, [100, 100])]), anchor=(30, 0), position=(30, 0))
    return comp, (340, 40, 200, 90)


m, mta = modern()
p, pta = pixel()
n, nta = neon_v()
build_asset(CAT, "combo-meter", "Combo Meter",
            "Combo gauge that pumps up with every hit and bursts when it maxes out. Put the combo multiplier in the "
            "text area.",
            ["combo", "multiplier", "streak", "hits", "meter", "gaming", "hud", "fighting"], [
    Variant("modern", "Radial", m, "intro-hold", thumb_t=0.8, text_area=mta,
            description="Radial arc gauge with a dark centre for the multiplier; the arc springs forward with each hit."),
    Variant("pixel", "Pixel", p, "intro-hold", thumb_t=0.8, bg="e8e8ee", text_area=pta,
            description="8-bit star icon and five blocks that pop in one per hit, with a lightning bolt at max."),
    Variant("neon", "Neon Bars", n, "intro-hold", thumb_t=0.8, text_area=nta,
            description="Rising skewed neon bars, like a signal meter, that flicker on hit by hit."),
])
