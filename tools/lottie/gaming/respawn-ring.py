import random

from _gaming2 import *

W = H = 400
F = 108
C = (W / 2, H / 2)
T0, T1 = 12, 90            # countdown
END = 104
SECS = [T0, T0 + 26, T0 + 52]
R = 120
TA = (C[0] - 62, C[1] - 44, 124, 88)


def remaining(t):
    return 1 - clamp((t - T0) / (T1 - T0))


def tick_punch(base=100, amp=8):
    def f(t):
        if t < 12:
            return [base * back_out(t / 12)] * 2
        v = 0
        for s in SECS:
            d = t - s
            if d >= 0:
                v = max(v, amp * math.exp(-d / 4) * (1 if d > 1.5 else d / 1.5))
        if t >= T1:
            d = t - T1
            v = amp * 2.5 * bump(d, 0, 8) - (base + amp) * ease_in(clamp((d - 4) / 10), 2)
        return [max(base + v, 0)] * 2
    return sampled(f, 0, F, 1)


def outro_burst(comp, shapes, n=14, r0=R, r1=R + 70, seed=3, hold=False):
    rng = random.Random(seed)
    for i in range(n):
        a = i * 360 / n + rng.uniform(-6, 6)
        life = rng.randint(12, 16)

        def fn(u, a=a, life=life):
            e = ease_out(u / life)
            p = pt(lerp(r0, r1, e), a, C)
            if hold:
                p = (snap(p[0], 6), snap(p[1], 6))
            return {"position": list(p), "scale": [100 * (1 - u / life)] * 2, "rotation": a}
        particle(comp, "burst", shapes, T1 + 1, life, F, fn, wrap=False, hold=hold, step=2 if hold else 1)


def flash_ring(comp, slot, width=10, d0=2 * R, d1=2 * R + 140):
    comp.layer("shock", [group([ellipse(anim([(T1, [d0, d0], DECEL), (T1 + 16, [d1, d1])])),
                                stroke(slot=slot, width=anim([(T1, width, EASE_OUT), (T1 + 16, 1)]))], "r")],
               position=C, ip=T1, op=T1 + 17, opacity=anim([(T1, 100, EASE_IN), (T1 + 16, 0)]))
    comp.layer("flash", [glow(2 * R + 60, "#FFFFFF", 0.9)], position=C, ip=T1, op=T1 + 14,
               scale=anim([(T1, [50, 50], SNAP_OUT), (T1 + 6, [110, 110])]), opacity=anim([(T1, 100, EASE_IN), (T1 + 13, 0)]))


def fade_out():
    return anim([(0, 100, HOLD), (T1 + 2, 100, EASE_IN), (T1 + 12, 0)])


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("respawn-ring", W, H, frames=F)
    comp.slot("primary", "#35E0FF")
    comp.slot("background", PANEL)
    comp.slot("outline", "#FFFFFF")
    outro_burst(comp, [group([spark(10), fill("#FFFFFF")], "s")])
    flash_ring(comp, "primary")
    head = sampled(lambda t: list(pt(R, 360 * remaining(t), C)), 0, F, 1)
    comp.layer("head", [group([ellipse((14, 14)), fill("#FFFFFF")], "d"), glow(50, "#BFF6FF", 0.8)], position=head,
               ip=T0, op=T1 + 1, scale=pop(T0, 8))
    rig = comp.null("rig", position=C, scale=tick_punch(100, 5))
    trim_end = anim([(T0, 100, LINEAR), (T1, 0)])
    comp.layer("arc", [
        group([ellipse((2 * R, 2 * R)), trim(end=trim_end), stroke("#FFFFFF", width=4)], "core"),
        group([ellipse((2 * R, 2 * R)), trim(end=trim_end), stroke(slot="primary", width=12)], "arc"),
        group([ellipse((2 * R, 2 * R)), trim(end=trim_end), stroke(slot="primary", width=30, opacity=16)], "glow"),
    ], parent=rig, opacity=fade_out())
    comp.layer("track", [
        group([ellipse((2 * R, 2 * R)), stroke(slot="outline", width=12, opacity=14)], "track"),
        group([ellipse((2 * R + 34, 2 * R + 34)), stroke(slot="outline", width=2, opacity=40, dashes=[4, 14])], "dash",
              rotation=sampled(lambda t: t * 1.5, 0, F, 6)),
    ], parent=rig, opacity=fade_out())
    disc = comp.null("disc", position=C, scale=tick_punch(100, 10))
    comp.layer("disc", [
        group([ellipse((2 * R - 44, 2 * R - 44)), stroke(slot="primary", width=2, opacity=60)], "inner"),
        group([ellipse((2 * R - 30, 2 * R - 30)), sheen(2 * R, 2 * R, 0.12, 0.25)], "gloss"),
        group([ellipse((2 * R - 30, 2 * R - 30)), fill(slot="background", opacity=90)], "disc"),
    ], parent=disc, opacity=fade_out())
    return comp


# ---------------------------------------------------------------- pixel

def pixel():
    comp = Comp("respawn-ring--pixel", W, H, frames=F)
    comp.slot("primary", "#FF4D5E")
    comp.slot("secondary", "#FFD23F")
    comp.slot("background", "#2B2140")
    comp.slot("outline", INK)
    P = 8
    N = 16
    outro_burst(comp, [box(-7, -7, 14, 14, slot="secondary")], hold=True)
    comp.layer("flash", [pix_group(pix_cells(lambda x, y: x * x + y * y <= 17 ** 2, 36), P, (-18 * P, -18 * P), "#FFFFFF", "f")],
               position=C, ip=T1, op=T1 + 8, opacity=stepped(lambda t: 100 if (t - T1) % 4 < 2 else 0, T1, T1 + 8, 1))
    pscale = stepped(lambda t: [0, 0] if t < 2 else [60, 60] if t < 4 else [115, 115] if t < 6 else
                     [110, 110] if any(0 <= t - s < 3 for s in SECS[1:]) else [100, 100] if t < T1 + 6 else [0, 0], 0, F, 1)
    for k in range(N):
        a = k * 360 / N + 360 / N / 2
        p = pt(R, a)
        p = (snap(p[0], P), snap(p[1], P))
        off_t = T0 + (T1 - T0) * (N - k) / N
        comp.layer("block", [box(-P, -P, 2 * P, P, "#FFFFFF", opacity=45),
                             box(-P, -P, 2 * P, 2 * P, slot="primary"),
                             box(-2 * P, -2 * P, 4 * P, 4 * P, slot="outline")],
                   position=(C[0] + p[0], C[1] + p[1]),
                   opacity=stepped(lambda t, o=off_t: 0 if t >= o and not (o <= t < o + 6 and (t - o) % 4 < 2) else 100, 0, F, 1),
                   scale=pscale)
        comp.layer("slot", [box(-P, -P, 2 * P, 2 * P, slot="background"), box(-2 * P, -2 * P, 4 * P, 4 * P, slot="outline")],
                   position=(C[0] + p[0], C[1] + p[1]), scale=pscale)
    disc = pix_cells(lambda x, y: x * x + y * y <= 10.5 ** 2, 22)
    rim = pix_cells(lambda x, y: x * x + y * y <= 11.5 ** 2, 24)
    comp.layer("disc", [pix_group([(c, r) for c, r in disc if r <= 2], P, (-11 * P, -11 * P), ("#FFFFFF", 12), "hi"),
                        pix_group(disc, P, (-11 * P, -11 * P), ("slot", "background"), "d"),
                        pix_group(rim, P, (-12 * P, -12 * P), ("slot", "outline"), "r")], position=C, scale=pscale)
    return comp


# ---------------------------------------------------------------- neon

def neon_v():
    comp = Comp("respawn-ring--neon", W, H, frames=F)
    comp.slot("primary", MAGENTA)
    comp.slot("secondary", NCYAN)
    outro_burst(comp, [group([spark(12), fill("#FFFFFF")], "s")], seed=8)
    flash_ring(comp, "secondary", 8)
    head = sampled(lambda t: list(pt(R, 360 * remaining(t), C)), 0, F, 1)
    comp.layer("comet", [group([spark(16), fill("#FFFFFF")], "s"), glow(60, "#FF9CEB", 0.9)], position=head, ip=T0,
               op=T1 + 1, scale=pop(T0, 8), rotation=sampled(lambda t: t * 12, 0, F, 3))
    trim_end = anim([(T0, 100, LINEAR), (T1, 0)])
    rig = comp.null("rig", position=C, scale=tick_punch(100, 4))
    comp.layer("arc", [group([ellipse((2 * R, 2 * R)), trim(end=trim_end), s], f"n{k}")
                       for k, s in enumerate([stroke("#FFFFFF", width=2.5, opacity=90), stroke(slot="primary", width=7),
                                              stroke(slot="primary", width=18, opacity=30),
                                              stroke(slot="primary", width=36, opacity=12)])],
               parent=rig, opacity=fade_out())
    comp.layer("inner", neon([ellipse((2 * R - 50, 2 * R - 50))], slot="secondary", w=2.5, core=False, glow_a=0.7),
               parent=rig, opacity=anim([(0, 0, HOLD)] + sum([[(s, 60, EASE_OUT), (s + 2, 100, EASE_OUT), (s + 16, 60)]
                                                              for s in SECS], []) + [(T1 + 2, 60, EASE_IN), (T1 + 10, 0)]))
    comp.layer("hex", neon([ngon(6, R + 28, 0)], slot="secondary", w=2, core=False, glow_a=0.5), parent=rig,
               rotation=sampled(lambda t: -t * 1.2, 0, F, 6), opacity=fade_out(), scale=(100, 100))
    comp.layer("track", [group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=7, opacity=18)], "t")], parent=rig,
               opacity=fade_out())
    return comp


build_asset(CAT, "respawn-ring", "Respawn Ring",
            "Circular respawn timer: the ring counts down around a centre badge, pulses each second and bursts when "
            "it runs out. Put the countdown or label in the centre. One-shot that ends empty.",
            ["respawn", "timer", "countdown", "ring", "cooldown", "gaming", "hud", "revive"], [
    Variant("modern", "Modern", modern(), "intro-hold", thumb_t=0.4, text_area=TA,
            description="Glowing cyan arc with a bright head, a dashed outer ring and a dark glass centre."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.4, bg="e8e8ee", text_area=TA,
            description="Sixteen 8-bit blocks around a pixel disc that blink out one by one."),
    Variant("neon", "Neon", neon_v(), "intro-hold", thumb_t=0.4, text_area=TA,
            description="Magenta neon ring with a spinning comet head inside a rotating cyan hexagon."),
])
