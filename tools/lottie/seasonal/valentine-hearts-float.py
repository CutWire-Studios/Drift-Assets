"""Valentine hearts float: hearts rising and swaying upward (seamless loops)."""

from _common import *

T = 120
RED, PINK, ROSE = "#FF2E5F", "#FF8FB1", "#E0115F"


def glossy_heart(col, sid, s=1.0):
    box = (-54, -51, 54, 38)
    return [
        group([ellipse((16, 10)), fill(WHITE, 85)], "spec", position=(-30 * s, -30 * s), rotation=-40,
              scale=(100 * s, 100 * s)),
        group([ellipse((26, 14)), fill(WHITE, 35)], "sheen", position=(-28 * s, -22 * s), rotation=-40,
              scale=(100 * s, 100 * s)),
        group(S(HEART_D, s) + [shade_overlay(tuple(v * s for v in box), 0.9, dark="#5A0020")], "shade"),
        group(S(HEART_D, s) + [fill(col, slot=sid)], "heart"),
    ]


def rise():
    W, H = 1920, 1080
    comp = Comp("valentine-hearts-float", W, H, frames=T)
    comp.slot("primary", RED)
    comp.slot("secondary", PINK)

    def shapes(i, d):
        sid, col = ("primary", RED) if i % 3 else ("secondary", PINK)
        return glossy_heart(col, sid)

    fall(comp, "heart", 36, T, W, H, shapes, seed=21, speed=(5.6, 8.8), sway=(20, 60), sway_period=(60, 120),
         size=(0.35, 0.95), opacity=(70, 100), rise=True, margin=80, flip=0.25, flip_period=(40, 60))
    return comp


def beat():
    W = H = 600
    comp = Comp("valentine-hearts-float--beat", W, H, frames=60)
    TT = 60
    comp.slot("primary", RED)
    comp.slot("secondary", PINK)
    c = (W / 2, 330)

    def pulse(t):
        # lub-dub: two quick beats then rest
        u = t / TT
        v = 0.0
        for t0, amp in ((0.0, 1.0), (0.18, 0.7)):
            k = (u - t0) / 0.16
            if 0 <= k <= 1:
                v = max(v, amp * math.sin(math.pi * k) ** 2)
        return v

    comp.layer("heart", glossy_heart(RED, "primary"), position=c,
               scale=looped(lambda t: [260 * (1 + 0.14 * pulse(t))] * 2, TT, 1))
    for j, t0 in enumerate((0, 11)):
        comp.layer(f"ring{j}", [group(S(HEART_D) + [stroke(PINK, 5, slot="secondary")], "ring")], position=c,
                   ip=t0, op=t0 + 26, scale=Anim([(t0, [260, 260], EASE_OUT), (t0 + 26, [380, 380])]),
                   opacity=Anim([(t0, 80, LINEAR), (t0 + 26, 0)]))
    # small hearts streaming up out of the big one
    r = rng(2)
    for i in range(9):
        t0 = i * TT / 9
        dx = r.uniform(-150, 150)
        sz = r.uniform(0.28, 0.5)
        sid, col = ("secondary", PINK) if i % 2 else ("primary", RED)

        def fn(u, dx=dx, sz=sz):
            k = u / 50
            return {"position": (c[0] + dx * ease_out(k, 2) + 16 * math.sin(k * 9), c[1] - 40 - 250 * ease_out(k, 1.6)),
                    "scale": [100 * sz * min(1, k * 5)] * 2, "opacity": 100 * smooth((1 - k) / 0.35),
                    "rotation": dx * 0.12 * k}
        particle(comp, f"mini{i}", glossy_heart(col, sid), t0, 50, TT, fn, step=2)
    comp.layer("glow", [glow(200, "#FF5C8A", 100, position=(0, -10))], position=c,
               opacity=looped(lambda t: 35 + 45 * pulse(t), TT, 1))
    return comp


def doodle():
    W, H = 720, 960
    comp = Comp("valentine-hearts-float--doodle", W, H, frames=T)
    comp.slot("outline", INK)
    comp.slot("primary", RED)
    comp.slot("secondary", PINK)
    hp = heart_pts(1.0, 16)
    r = rng(8)

    def shapes(i, d):
        sid, col = ("primary", RED) if i % 2 else ("secondary", PINK)
        jit = [(x + r.uniform(-3, 3), y + r.uniform(-3, 3)) for x, y in hp]
        items = [group([path(smooth_closed(jit)), stroke(INK, 6, slot="outline")], "line"),
                 group(S("M -26 -26 Q -34 -14 -30 -2") + [stroke(WHITE, 5, 90)], "shine")]
        if i % 4 == 0:  # an outline-only heart now and then
            return items
        items.append(group([path(smooth_closed(hp)), fill(col, slot=sid)], "fill", position=(7, 6)))
        return items

    fall(comp, "heart", 18, T, W, H, shapes, seed=4, speed=(7.0, 9.6), sway=(25, 60), sway_period=(60, 120),
         size=(0.75, 1.25), rise=True, margin=90, x_range=(90, W - 90))
    for j, (p, t0) in enumerate((((120, 260), 0), ((600, 520), 40), ((150, 760), 80), ((560, 180), 20))):
        sparkle(comp, f"spark{j}", p, T, 16, INK, "outline", t0=t0, period=60)
    return comp


build("valentine-hearts-float", "Valentine Hearts Float",
      "Hearts floating up and swaying for Valentine's Day, anniversaries and love notes; seamless loops.",
      ["valentine", "hearts", "love", "romantic", "floating", "anniversary"], [
          Variant("rise", "Rising Hearts", rise(), "loop", thumb_t=0.5, region=(610, 190, 700, 700), pad=0,
                  description="Full-frame transparent overlay of glossy hearts drifting up in three depths."),
          Variant("beat", "Heartbeat", beat(), "loop", thumb_t=0.75,
                  description="One big glossy heart beating lub-dub, releasing little hearts and pulse rings."),
          Variant("doodle", "Doodle", doodle(), "loop", thumb_t=0.5, bg="f3ece0",
                  description="Hand-drawn ink hearts with off-register fills rising in a column, with twinkles."),
      ])
