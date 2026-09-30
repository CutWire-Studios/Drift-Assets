"""Full-width flames licking up from the bottom edge: the "this is fine" room-on-fire loop."""

from _memes2 import *

W, H = 1920, 540
F = 60


def flame_row(n, base_y, peak, amp, seed, sway=24, valley_amp=10, tip=0.12, phase=0.0, sharp=True):
    """Anim of closed flame-row paths (n tongues across the width) that loops over F frames."""
    rng = random.Random(seed)
    tw = (W + 200) / n
    ph = [(rng.uniform(0, TAU), rng.uniform(0, TAU), rng.choice((1, 2)), rng.uniform(0.75, 1.25)) for _ in range(n)]

    def shape(t):
        v, it, ot = [], [], []
        u = TAU * t / F
        for i in range(n):
            a, b, k, sc = ph[i]
            x0 = -100 + i * tw
            vy = base_y + valley_amp * math.sin(u * k + b)
            hv = peak * 0.42
            v.append((x0, vy)); it.append((-tw * 0.06, -hv)); ot.append((tw * 0.06, -hv))
            h = peak * sc + amp * math.sin(u * k + a + phase)
            px = x0 + tw / 2 + sway * math.sin(u * k + a + 1.3)
            py = base_y - h
            if sharp:
                v.append((px, py))
                hx = min(tw * 0.26, h * 0.4)
                it.append((-hx - sway * 0.3, h * 0.28)); ot.append((hx - sway * 0.3, h * 0.28))
            else:
                v.append((px, py)); it.append((-tw * 0.18, 0)); ot.append((tw * 0.18, 0))
        v.append((W + 100, base_y)); it.append((-tw * 0.22, 0)); ot.append((0, 0))
        v.append((W + 100, H + 40)); it.append((0, 0)); ot.append((0, 0))
        v.append((-100, H + 40)); it.append((0, 0)); ot.append((0, 0))
        return bezier(v, it, ot, closed=True)

    ks = [(t, shape(t), LINEAR) for t in range(0, F, 3)] + [(F, shape(0), LINEAR)]
    return path(Anim(ks), "flames")


def embers(comp, n, seed, color=None, slot=None, size=(6, 12), life=(30, 50), rise=(260, 420), square=False):
    rng = random.Random(seed)
    for i in range(n):
        x = rng.uniform(40, W - 40)
        s0 = rng.uniform(0, F)
        lf = rng.uniform(*life)
        rs = rng.uniform(*rise)
        sz = rng.uniform(*size)
        dr = rng.uniform(-60, 60)
        wob = rng.uniform(0, TAU)

        def fn(u, x=x, lf=lf, rs=rs, dr=dr, wob=wob):
            p = u / lf
            return {"position": [x + dr * p + 14 * math.sin(p * 6 + wob), H - 60 - rs * p],
                    "opacity": 100 * clamp(p * 5) * clamp((1 - p) * 2.5),
                    "scale": [100 * (1 - 0.6 * p), 100 * (1 - 0.6 * p)]}
        shp = rect((sz, sz)) if square else ellipse((sz, sz))
        particle(comp, f"ember{i}", [group([shp, fill(color or "#FFFFFF", slot=slot)], "e")], s0, lf, F, fn, step=3)


def cartoon():
    """Three layers of toothy cartoon flames in red, orange and yellow with drifting embers."""
    comp = base("everything-is-fine-flames", W, H, F)
    comp.slot("primary", "#FF4A1C")
    comp.slot("secondary", "#FF9A1F")
    comp.slot("accent", "#FFE14D")
    embers(comp, 22, 4, slot="accent")
    comp.layer("front", [group([flame_row(22, H - 30, 90, 36, 3, phase=2.0), fill(slot="accent")], "f")])
    comp.layer("mid", [group([flame_row(16, H - 20, 180, 50, 2, phase=1.0), fill(slot="secondary")], "f")])
    comp.layer("back", [group([flame_row(12, H - 10, 300, 70, 1), fill(slot="primary")], "f")])
    comp.layer("glow", [group([rect((W, 260), (W / 2, H - 130)),
                               gradient_fill([(0, "#FF4A1C", 0), (1, "#FF4A1C", 0.22)], (0, H - 260), (0, H))], "g")])
    return comp


def pixel():
    """Blocky 8-bit flames: stair-stepped columns that flicker in held frames, with square embers."""
    comp = base("everything-is-fine-flames--pixel", W, H, F)
    comp.slot("primary", "#E83B1A")
    comp.slot("secondary", "#FF9A1F")
    comp.slot("accent", "#FFE14D")
    P = 24
    cols = W // P
    rng = random.Random(6)

    def stairs(maxh, amp, seed):
        r = random.Random(seed)
        base_h = [maxh * (0.55 + 0.45 * abs(math.sin(i * 0.37 + r.uniform(0, 1)))) for i in range(cols)]
        ph = [r.uniform(0, TAU) for _ in range(cols)]
        step = 4
        ks = []
        for s in range(F // step):
            t = s * step
            v = []
            for i in range(cols):
                h = base_h[i] + amp * math.sin(TAU * t / F * 2 + ph[i])
                h = max(P, round(h / P) * P)
                v += [(i * P, H - h), ((i + 1) * P, H - h)]
            v += [(W, H + P), (0, H + P)]
            ks.append((t, bezier(v, closed=True), HOLD))
        ks.append((F, ks[0][1], HOLD))
        return path(Anim(ks), "stairs")
    embers(comp, 18, 9, slot="accent", size=(12, 16), square=True)
    comp.layer("front", [group([stairs(110, 40, 3), fill(slot="accent")], "f")])
    comp.layer("mid", [group([stairs(220, 60, 2), fill(slot="secondary")], "f")])
    comp.layer("back", [group([stairs(340, 80, 1), fill(slot="primary")], "f")])
    return comp


def inferno():
    """Tall wispy gradient flames with a hot glowing base and many sparks: the realistic look."""
    comp = base("everything-is-fine-flames--inferno", W, H, F)
    embers(comp, 40, 12, color="#FFD27A", size=(4, 9), life=(24, 44), rise=(300, 480))
    comp.layer("core", [group([flame_row(26, H - 20, 110, 50, 13, sway=30, tip=0.08, phase=2.4),
                               gradient_fill([(0, "#FFF4C2"), (0.6, "#FFD04A"), (1, "#FF9A1F", 0.0)], (0, H), (0, H - 240))],
                              "f")])
    comp.layer("mid", [group([flame_row(20, H - 10, 230, 80, 12, sway=40, tip=0.07, phase=1.2),
                              gradient_fill([(0, "#FFB02E"), (0.55, "#FF6A1A"), (1, "#E0301A", 0.0)], (0, H), (0, H - 380))],
                             "f")])
    comp.layer("back", [group([flame_row(16, H, 350, 100, 11, sway=50, tip=0.06),
                               gradient_fill([(0, "#FF5A1A"), (0.5, "#C8201A", 0.85), (1, "#7A0A10", 0.0)], (0, H),
                                             (0, H - 520))], "f")])
    comp.layer("heat", [group([rect((W, H), (W / 2, H / 2)),
                               gradient_fill([(0, "#FF6A1A", 0), (1, "#FF6A1A", 0.3)], (0, 0), (0, H))], "g")],
               opacity=loop(F, [100, 70, 100, 80], SINE))
    return comp


build_asset(CAT, "everything-is-fine-flames", "Everything Is Fine Flames",
            "A full-width wall of flames licking up from the bottom edge on a seamless loop, for when everything "
            "is definitely fine. Lay it along the bottom of the frame.",
            ["fire", "flames", "this is fine", "burning", "chaos", "meme", "loop"], [
    Variant("cartoon", "Cartoon", cartoon(), "loop", thumb_t=0.3, region=(560, 0, 800, 540),
            description="Three layers of toothy cartoon flames in red, orange and yellow with drifting embers."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.3, region=(560, 0, 800, 540),
            description="Blocky 8-bit flames that flicker in held frames, with square embers."),
    Variant("inferno", "Inferno", inferno(), "loop", thumb_t=0.3, region=(560, 0, 800, 540),
            description="Tall wispy gradient flames with a hot glowing base and lots of sparks (fixed colours)."),
])
