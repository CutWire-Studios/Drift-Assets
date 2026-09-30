import random

from _gaming2 import *

W, H, F = 720, 240, 75
FX, FY = 104, 128          # flame base centre
HITS = [14, 23, 32, 41, 50]
BX, SW, SH_ = 206, 66, 34  # bar start, segment pitch, height
BY = 138
TA = (BX + 5 * SW + 18, BY - 34, W - (BX + 5 * SW + 18) - 14, 68)


def flame_path(t, s=1.0, ph=0.0, amp=1.0):
    tx = 8 * amp * math.sin(t * 0.55 + ph) + 4 * amp * math.sin(t * 1.3 + ph)
    lb = 42 + 3 * amp * math.sin(t * 0.8 + ph + 1)
    rb = 40 + 3 * amp * math.sin(t * 0.9 + ph + 2)
    ty = -80 - 6 * amp * math.sin(t * 0.7 + ph + 0.5)
    lx = -34 + 5 * amp * math.sin(t * 0.9 + ph + 3)
    ly = -34 - 5 * amp * math.sin(t * 1.1 + ph)
    v = [(0, 52), (-lb, 14), (lx, ly), (-14, -18), (tx, ty), (rb, 6)]
    it = [(24, 0), (0, 22), (-8, 16), (-6, 4), (-4 - tx * 0.3, 32), (0, -30)]
    ot = [(-24, 0), (0, -18), (4, 8), (6, -14), (6 - tx * 0.3, 30), (0, 26)]
    sc = lambda pts: [(x * s, y * s) for x, y in pts]
    return bezier(sc(v), sc(it), sc(ot), True)


def flame_anim(s, ph, amp=1.0, step=2):
    ts = list(range(0, F + 1, step))
    return path(Anim([(t, flame_path(t, s, ph, amp), EASE_IN_OUT) for t in ts]), "flame")


def grow():
    """Flame scale: pops in, then steps up with each streak hit, with a flare at the end."""
    def f(t):
        if t < 8:
            return [60 * back_out(t / 8)] * 2
        lv = 60 + sum(10 for h in HITS if t >= h)
        v = 0
        for h in HITS:
            d = t - h
            if 0 <= d:
                v = max(v, 16 * math.exp(-d / 4) * min(1, d / 1.5))
        return [lv + v] * 2
    return sampled(f, 0, F, 1)


def embers(comp, shapes, n=14, seed=2, hold=False):
    rng = random.Random(seed)
    for i in range(n):
        t0 = rng.randint(6, F - 18)
        life = rng.randint(14, 22)
        x = FX + rng.uniform(-26, 26)
        dx = rng.uniform(-30, 30)
        rise = rng.uniform(80, 130)

        def fn(u, x=x, dx=dx, rise=rise, life=life):
            k = u / life
            px, py = x + dx * k + 6 * math.sin(k * 9), FY - 30 - rise * ease_out(k, 1.5)
            if hold:
                return {"position": [snap(px, 6), snap(py, 6)], "opacity": 100 if k < 0.75 else 0}
            return {"position": [px, py], "scale": [100 * (1 - k)] * 2, "opacity": 100 * (1 - k)}
        particle(comp, "ember", shapes, t0, life, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


def seg_on(i, hold=False):
    h = HITS[i]
    if hold:
        return stepped(lambda t: [0, 0] if t < h else [130, 130] if t < h + 2 else [100, 100], 0, F, 1)
    return anim([(h, [0, 0], SPRING), (h + 10, [100, 100])])


def seg_flash(i):
    h = HITS[i]
    return anim([(0, 0, HOLD), (h, 100, EASE_OUT), (h + 9, 0, HOLD), (F, 0)])


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("streak-flame", W, H, frames=F)
    comp.slot("primary", "#FF5A1F")
    comp.slot("secondary", "#FFC21A")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    embers(comp, [group([ellipse((8, 8)), fill(slot="secondary")], "e"), glow(20, "#FFC21A", 0.6)])
    fl = comp.null("flame", position=(FX, FY + 40), scale=grow(), anchor=(0, 40))
    comp.layer("core", [group([flame_anim(0.42, 2.0, 0.6), fill("#FFFFFF", 92)], "c")], parent=fl, position=(0, 14))
    comp.layer("mid", [group([flame_anim(0.7, 1.0, 0.8), fill(slot="secondary")], "m")], parent=fl, position=(0, 6))
    comp.layer("outer", [group([flame_anim(1.0, 0.0), fill(slot="primary")], "o")], parent=fl)
    comp.layer("glow", [glow(190, "#FF7A2A", 0.5)], parent=fl, position=(0, 0),
               opacity=sampled(lambda t: 70 + 30 * math.sin(t * 0.9), 0, F, 3))
    for i in range(5):
        x = BX + i * SW + SW / 2
        comp.layer("flash", [group([skew_rect(SW - 10, SH_, 12), fill("#FFFFFF")], "f")], position=(x, BY), opacity=seg_flash(i))
        comp.layer("seg", [group([skew_rect(SW - 10, SH_, 12), sheen(SW, SH_, 0.4, 0.25)], "g"),
                           group([skew_rect(SW - 10, SH_, 12), fill(slot="secondary" if i == 4 else "primary")], "s")],
                   position=(x, BY), scale=seg_on(i))
        comp.layer("slot", [group([skew_rect(SW - 10, SH_, 12), fill(slot="background", opacity=85),
                                   stroke(slot="outline", width=1.5, opacity=25)], "s")], position=(x, BY),
                   opacity=fade(2 + i * 2, 8 + i * 2))
    comp.layer("line", [group([seg((BX, BY + 32), (BX + 5 * SW, BY + 32)), trim(end=anim([(4, 0, SNAP_OUT), (22, 100)])),
                               stroke(slot="primary", width=3, cap="butt")], "l")])
    return comp


# ---------------------------------------------------------------- pixel

FLAME_FRAMES = [
    ["....K.......", "...KRK......", "...KRRK..K..", "..KRRRK.KRK.", "..KROORKKRRK", ".KROOOORRRRK", ".KROYYOORRK.",
     "KROOYYYOORK.", "KROYYWYYORRK", "KROYWWWYYORK", "KROYYWWYYORK", ".KROYYYYORK.", "..KKRRRRKK..", "....KKKK...."],
    [".......K....", "......KRK...", "..K..KRRK...", ".KRK.KRRRK..", "KRRKKROORK..", "KRRRROOOORK.", ".KRROOYYORK.",
     ".KROOYYYOORK", "KRROYYWYYORK", "KROYYWWWYORK", "KROYYWWYYORK", ".KROYYYYORK.", "..KKRRRRKK..", "....KKKK...."],
]


def pixel():
    comp = Comp("streak-flame--pixel", W, H, frames=F)
    comp.slot("primary", "#E8283C")
    comp.slot("secondary", "#FF8A1F")
    comp.slot("accent", "#FFD23F")
    comp.slot("outline", INK)
    comp.slot("background", "#2B2140")
    P = 8
    cols = {"W": "#FFFFFF", "Y": ("slot", "accent"), "O": ("slot", "secondary"), "R": ("slot", "primary"), "K": ("slot", "outline")}
    embers(comp, [box(-5, -5, 10, 10, slot="accent")], hold=True)
    size = stepped(lambda t: [0, 0] if t < 2 else [60 + sum(10 for h in HITS if t >= h) + (12 if any(0 <= t - h < 3 for h in HITS) else 0)] * 2,
                   0, F, 1)
    for k, fr in enumerate(FLAME_FRAMES):
        comp.layer(f"flame {k}", pix(fr, cols, P, (0, -56), order=list("WYORK")), position=(FX, FY + 56), scale=size,
                   opacity=stepped(lambda t, k=k: 100 if (t // 5) % 2 == k else 0, 0, F, 1))
    for i in range(5):
        x = BX + i * SW
        comp.layer("flash", [box(x + 6, BY - SH_ / 2 + 6, SW - 12, SH_ - 12, "#FFFFFF")],
                   opacity=stepped(lambda t, h=HITS[i]: 100 if h <= t < h + 4 and (t - h) % 4 < 2 else 0, 0, F, 1))
        comp.layer("seg", [box(x + 6, BY - SH_ / 2 + 6, SW - 12, 6, "#FFFFFF", opacity=45),
                           box(x + 6, BY - SH_ / 2 + 6, SW - 12, SH_ - 12, slot="accent" if i == 4 else "secondary")],
                   opacity=stepped(lambda t, h=HITS[i]: 0 if t < h else 100, 0, F, 1))
        comp.layer("slot", [box(x + 6, BY - SH_ / 2 + 6, SW - 12, SH_ - 12, slot="background"),
                            box(x, BY - SH_ / 2, SW, SH_, slot="outline")],
                   opacity=stepped(lambda t, i=i: 0 if t < 2 + i * 2 else 100, 0, 14, 1))
    return comp


# ---------------------------------------------------------------- neon

def neon_v():
    comp = Comp("streak-flame--neon", W, H, frames=F)
    comp.slot("primary", "#FF3DAE")
    comp.slot("secondary", "#FFB02E")
    comp.slot("accent", NCYAN)
    embers(comp, [group([spark(8), fill("#FFFFFF")], "e"), glow(22, "#FFB02E", 0.7)], seed=5)
    fl = comp.null("flame", position=(FX, FY + 40), scale=grow(), anchor=(0, 40))
    comp.layer("inner", neon([flame_anim(0.55, 1.5, 0.7)], slot="secondary", w=3.5), parent=fl, position=(0, 12))
    comp.layer("outer", neon([flame_anim(1.0, 0.0)], slot="primary", w=4.5), parent=fl)
    for i in range(5):
        x = BX + i * SW + SW / 2
        h = HITS[i]
        flick = anim([(0, 0, HOLD), (h, 100, HOLD), (h + 1, 30, HOLD), (h + 2, 100, HOLD), (h + 3, 50, HOLD), (h + 4, 100, HOLD), (F, 100)])
        comp.layer("seg", [group([skew_rect(SW - 16, SH_ - 8, 12), fill(slot="secondary" if i == 4 else "primary", opacity=55)], "f")] +
                   neon([skew_rect(SW - 16, SH_ - 8, 12)], slot="secondary" if i == 4 else "primary", w=3), position=(x, BY), opacity=flick)
        comp.layer("ghost", [group([skew_rect(SW - 16, SH_ - 8, 12), stroke(slot="accent", width=1.5, opacity=45)], "g")], position=(x, BY),
                   opacity=anim([(0, 0, EASE_OUT), (8, 100, HOLD), (h, 100, HOLD), (h + 1, 0)]))
    comp.layer("frame", neon([rect((5 * SW + 10, SH_ + 22), (BX + 5 * SW / 2, BY), 8)], slot="accent", w=2.2, core=False, glow_a=0.7),
               opacity=anim([(0, 0, HOLD), (2, 80, HOLD), (3, 10, HOLD), (5, 100)]))
    return comp


build_asset(CAT, "streak-flame", "Streak Flame",
            "A flickering flame grows with each hit while a streak bar ignites segment by segment. Put the streak "
            "count to the right of the bar.",
            ["streak", "flame", "fire", "combo", "on fire", "hot", "gaming", "hud"], [
    Variant("modern", "Modern", modern(), "intro-hold", thumb_t=0.75, region=(10, 10, 560, 220), text_area=TA,
            description="Layered orange flame with a white-hot core, glowing embers and skewed glossy bar segments."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.75, region=(10, 10, 560, 220), bg="e8e8ee", text_area=TA,
            description="Two-frame 8-bit flame sprite that grows in steps, with blinking block segments."),
    Variant("neon", "Neon", neon_v(), "intro-hold", thumb_t=0.75, region=(10, 10, 560, 220), text_area=TA,
            description="Neon outline flame with flickering glowing segments in a cyan frame."),
])
