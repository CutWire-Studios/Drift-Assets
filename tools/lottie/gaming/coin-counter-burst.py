import random

from _gaming2 import *

W, H, F = 640, 440, 66
SRC = (170, 330)
ICON = (402, 72)
PX0, PW, PH = 402, 210, 66      # counter pill: starts under the icon centre
N = 10


def coin_paths(seed=4):
    rng = random.Random(seed)
    out = []
    for i in range(N):
        a = -90 + (i - (N - 1) / 2) * 17 + rng.uniform(-6, 6)
        r = rng.uniform(110, 170)
        p1 = pt(r, a + 90, SRC)
        p1 = (p1[0], p1[1] - 20)
        t0 = 4 + rng.uniform(0, 3)
        ta = 26 + i * 2.2 + rng.uniform(0, 1.5)
        out.append((t0, ta, p1, rng.uniform(0, 1)))
    return out


PATHS = coin_paths()
ARRIVE = sorted(round(p[1]) for p in PATHS)


def coin_fn(t0, ta, p1, ph, spin=True, hold=False):
    def fn(u):
        T = ta - t0
        k = clamp(u / T)
        burst = 0.36
        if k < burst:
            e = ease_out(k / burst, 2.5)
            x, y = lerp(SRC[0], p1[0], e), lerp(SRC[1], p1[1], e)
            s = lerp(40, 100, ease_out(k / burst))
        else:
            e = ease_in((k - burst) / (1 - burst), 2.2)
            # curve from p1 toward the icon with a little lift
            c = (lerp(p1[0], ICON[0], 0.3), min(p1[1], ICON[1]) - 30)
            x = (1 - e) ** 2 * p1[0] + 2 * (1 - e) * e * c[0] + e * e * ICON[0]
            y = (1 - e) ** 2 * p1[1] + 2 * (1 - e) * e * c[1] + e * e * ICON[1]
            s = lerp(100, 55, e)
        d = {"position": [x, y], "scale": [s * (abs(math.cos((u / 9 + ph) * math.pi)) * 0.8 + 0.2 if spin else 1), s]}
        if hold:
            d["position"] = [snap(x, 4), snap(y, 4)]
        return d
    return fn


def kick(t):
    """Sum of little punches at each coin arrival (0..~1)."""
    v = 0.0
    for ta in ARRIVE:
        d = t - ta
        if 0 <= d < 2:
            v = max(v, d / 2)
        elif d >= 2:
            v = max(v, math.exp(-(d - 2) / 3))
    return v


def pulse_keys(base=100, amp=18):
    def f(t):
        if t < 10:
            return [base * back_out(t / 10)] * 2
        return [base + amp * kick(t)] * 2
    return sampled(f, 0, F, 1)


def arrival_sparks(comp, shapes, hold=False):
    for j, ta in enumerate(ARRIVE[::2]):
        for k in range(4):
            a = 45 + k * 90 + j * 20

            def fn(u, a=a):
                e = ease_out(u / 10)
                p = pt(28 + 34 * e, a, ICON)
                return {"position": list(p), "scale": [100 * (1 - u / 10)] * 2}
            particle(comp, "spark", shapes, ta, 10, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


def burst_flash(comp, color="#FFFFFF"):
    comp.layer("source flash", [glow(160, color, 0.8)], position=SRC, ip=2, op=16,
               scale=anim([(2, [30, 30], SNAP_OUT), (8, [110, 110], EASE_OUT), (16, [130, 130])]),
               opacity=anim([(2, 100, EASE_IN), (16, 0)]))


# ---------------------------------------------------------------- modern

def coin_shapes(r=26):
    return [
        group([rect((r * 0.34, r * 0.9), (0, 0), r * 0.17), fill("#FFFFFF", 70)], "mark"),
        group([ellipse((r * 1.35, r * 1.35)), stroke(slot="secondary", width=r * 0.12)], "ring"),
        group([ellipse((r * 2, r * 2)), sheen(r * 2, r * 2, 0.4, 0.25)], "sheen"),
        group([ellipse((r * 2, r * 2)), fill(slot="primary")], "face"),
        group([ellipse((r * 2, r * 2), (0, r * 0.14)), fill(slot="secondary")], "edge"),
    ]


def modern():
    comp = Comp("coin-counter-burst", W, H, frames=F)
    comp.slot("primary", "#FFC42E")
    comp.slot("secondary", "#D9861A")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    arrival_sparks(comp, [group([spark(10), fill("#FFFFFF")], "s")])
    for i, (t0, ta, p1, ph) in enumerate(PATHS):
        particle(comp, f"coin {i}", coin_shapes(22), round(t0), round(ta - t0), F, coin_fn(t0, ta, p1, ph), wrap=False)
    burst_flash(comp, "#FFE39A")
    comp.layer("icon", coin_shapes(30), position=ICON, scale=pulse_keys())
    comp.layer("pill flash", [group([rect((PW, PH), (PX0 - PH / 2 + PW / 2, ICON[1]), PH / 2), fill("#FFFFFF")], "f")],
               opacity=sampled(lambda t: 20 * kick(t), 0, F, 1))
    grow = [(4, 0, SNAP_OUT), (18, 1, HOLD), (F, 1, HOLD)]
    comp.layer("pill", [
        group([rect(anim([(t, [PH + (PW - PH) * v, PH], e) for t, v, e in grow]),
                    anim([(t, [PX0 + (PH + (PW - PH) * v) / 2 - PH / 2 + 0.01, ICON[1]], e) for t, v, e in grow]), PH / 2),
               stroke(slot="outline", width=2, opacity=30), fill(slot="background", opacity=88)], "pill")])
    return comp


# ---------------------------------------------------------------- pixel

COIN_PIX = [
    "..KKKK..",
    ".KYYYYK.",
    "KYWYYYOK",
    "KYWYYYOK",
    "KYWYYYOK",
    "KYYYYYOK",
    ".KOOOOK.",
    "..KKKK..",
]
COIN_EDGE = [
    "KK",
    "YK",
    "YK",
    "YK",
    "YK",
    "YK",
    "OK",
    "KK",
]


def pixel():
    comp = Comp("coin-counter-burst--pixel", W, H, frames=F)
    comp.slot("primary", "#FFD23F")
    comp.slot("secondary", "#E08A1E")
    comp.slot("outline", INK)
    comp.slot("background", "#2B2140")
    PX = 5
    colors = {"W": "#FFFFFF", "O": ("slot", "secondary"), "Y": ("slot", "primary"), "K": ("slot", "outline")}
    full = pix(COIN_PIX, colors, PX, order=list("WOYK"))
    edge = pix(COIN_EDGE, colors, PX, order=list("OYK"))
    arrival_sparks(comp, [box(-5, -5, 10, 10, "#FFFFFF")], hold=True)
    for i, (t0, ta, p1, ph) in enumerate(PATHS):
        fn = coin_fn(t0, ta, p1, ph, spin=False, hold=True)
        # two sprite frames: face and edge-on, toggling every 3 frames
        for k, spr in enumerate((full, edge)):
            def f2(u, k=k, fn=fn, ph=ph):
                d = fn(u)
                on = (int(u / 3 + ph * 4) % 3 == 2) == (k == 1)
                s = snap(d["scale"][1], 25)
                return {"position": d["position"], "scale": [s, s], "opacity": 100 if on else 0}
            particle(comp, f"coin {i}.{k}", spr, round(t0), round(ta - t0), F, f2, step=1, wrap=False, hold=True)
    comp.layer("source", [box(-12, -12, 24, 24, "#FFFFFF"), box(-24, -4, 48, 8, "#FFFFFF"), box(-4, -24, 8, 48, "#FFFFFF")],
               position=SRC, ip=3, op=9, scale=stepped(lambda t: [100 + (t - 3) * 30] * 2, 3, 9, 2))
    comp.layer("icon", pix(COIN_PIX, colors, 7, order=list("WOYK")), position=ICON,
               scale=stepped(lambda t: [0, 0] if t < 2 else [60, 60] if t < 4 else [120, 120] if t < 6 else
                             [125, 125] if any(ta <= t < ta + 2 for ta in ARRIVE) else [100, 100], 0, F, 1))
    cnt = [(t, min(1, max(0, (t - 4) / 12)), HOLD) for t in range(0, F + 1, 2)]
    x0 = PX0 - 6
    comp.layer("pill", [
        group([lbar(x0, ICON[1] - PH / 2 + 6, PW - 6, 6, cnt), fill("#FFFFFF", 25)], "hi"),
        group([lbar(x0, ICON[1] - PH / 2 + 6, PW - 6, PH - 12, cnt), fill(slot="background")], "bg"),
        group([lbar(x0, ICON[1] - PH / 2, PW, PH, cnt), fill(slot="outline")], "rim"),
    ])
    return comp


# ---------------------------------------------------------------- fantasy (gems into a pouch)

GEM = [(0, -18), (14, -6), (0, 20), (-14, -6)]
GEM_TOP = [(-8, -12), (8, -12), (14, -6), (-14, -6)]


def gem_shapes(s=1.0, slot="primary"):
    sc = lambda pts: [(x * s, y * s) for x, y in pts]
    return [
        group([poly(sc([(0, -18), (0, 20), (-14, -6)])), fill("#FFFFFF", 25)], "facet L"),
        group([poly(sc([(-8, -12), (8, -12), (0, -6)])), fill("#FFFFFF", 55)], "table"),
        group([poly(sc([(0, -18), (14, -6), (0, 20)])), fill("#000000", 22)], "facet R"),
        group([poly(sc(GEM)), fill(slot=slot), stroke(GOLD_L, width=1.5 * s, opacity=70)], "gem"),
    ]


POUCH = "M-22 -18 C-30 -6 -34 10 -30 22 C-26 32 26 32 30 22 C34 10 30 -6 22 -18 Z"
POUCH_TOP = "M-22 -18 C-26 -26 -20 -32 -10 -28 C-4 -34 4 -34 10 -28 C20 -32 26 -26 22 -18 Z"


def fantasy():
    comp = Comp("coin-counter-burst--fantasy", W, H, frames=F)
    comp.slot("primary", "#2BD48F")
    comp.slot("secondary", GOLD)
    comp.slot("accent", "#FF4D7A")
    comp.slot("background", "#1D1226")
    arrival_sparks(comp, [group([spark(12), fill(slot="secondary")], "s")])
    for i, (t0, ta, p1, ph) in enumerate(PATHS):
        fn = coin_fn(t0, ta, p1, ph, spin=False)

        def f2(u, fn=fn, i=i, ph=ph):
            d = fn(u)
            d["rotation"] = (u * 14 + ph * 360) * (1 if i % 2 else -1)
            return d
        particle(comp, f"gem {i}", gem_shapes(1.3, "primary" if i % 3 else "accent") if i % 2 == 0 else coin_shapes_f(),
                 round(t0), round(ta - t0), F, f2, wrap=False)
    burst_flash(comp, "#C8FFE6")
    comp.layer("pouch", [
        group([seg((-18, -18), (18, -18)), stroke(slot="secondary", width=5)], "tie"),
        group([*svg_shapes(POUCH_TOP), fill("#8A5A2B"), stroke("#3B2412", width=3)], "top"),
        group([*svg_shapes(POUCH), sheen(64, 52, 0.25, 0.3)], "sheen"),
        group([*svg_shapes(POUCH), fill("#A86B34"), stroke("#3B2412", width=3)], "bag"),
        group([ellipse((96, 96)), fill(slot="background")], "disc"),
        group([ellipse((106, 106)), fill(slot="secondary"), stroke(GOLD_D, width=3)], "gold"),
    ], position=ICON, scale=pulse_keys(amp=14))
    grow = [(4, 0, SNAP_OUT), (18, 1, HOLD), (F, 1, HOLD)]
    size = anim([(t, [PH + (PW - PH) * v, PH - 8], e) for t, v, e in grow])
    pos = anim([(t, [PX0 + (PH + (PW - PH) * v) / 2 - PH / 2 + 0.01, ICON[1]], e) for t, v, e in grow])
    comp.layer("plate", [
        group([rect(size, pos, 10), fill(slot="background")], "inner"),
        group([rect(size, pos, 12), stroke(slot="secondary", width=10), stroke(GOLD_D, width=14)], "frame"),
    ])
    return comp


def coin_shapes_f():
    return [
        group([star(5, 8, 3.5), fill(GOLD_D)], "star"),
        group([ellipse((30, 30)), stroke(GOLD_D, width=2.5)], "ring"),
        group([ellipse((40, 40)), sheen(40, 40, 0.4, 0.25)], "sheen"),
        group([ellipse((40, 40)), fill(slot="secondary")], "face"),
    ]


TA = (PX0 + PH / 2 + 10, ICON[1] - 22, PW - PH / 2 - 26, 44)
build_asset(CAT, "coin-counter-burst", "Coin Counter Burst",
            "A burst of coins arcs through the air and flies into a counter badge, which pulses as each one lands. "
            "Put the count inside the counter.",
            ["coins", "gold", "counter", "currency", "reward", "loot", "gaming", "hud"], [
    Variant("modern", "Modern", modern(), "intro-hold", thumb_t=0.42, region=(100, 10, 540, 340), text_area=TA,
            description="Glossy spinning gold coins and a dark translucent counter pill."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.42, region=(100, 10, 540, 340), bg="e8e8ee", text_area=TA,
            description="8-bit coins flipping between face and edge sprites, into a pixel counter box."),
    Variant("fantasy", "Treasure", fantasy(), "intro-hold", thumb_t=0.42, region=(100, 10, 540, 340), text_area=TA,
            description="Tumbling gems and star coins fly into a leather pouch on a gold-framed plate."),
])
