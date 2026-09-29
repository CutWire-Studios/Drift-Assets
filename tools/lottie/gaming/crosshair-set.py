from _gaming2 import *

W = H = 240
F = 45
C = (W / 2, H / 2)
HIT = 8


def bloom(amp):
    """0 -> 1 -> 0: spread right after the shot, easing back."""
    return lambda t: amp * (ease_out(clamp((t - HIT) / 2)) if t < HIT + 2 else 1 - smooth(clamp((t - HIT - 2) / 18)))


def hit_ticks(comp, r0=22, r1=40, w=5):
    ticks = []
    for a in (45, 135, 225, 315):
        ticks.append(group([seg(pt(r0, a), pt(r1, a)), stroke(slot="accent", width=w, cap="butt")], f"t{a}"))
        ticks.append(group([seg(pt(r0 - 2, a), pt(r1 + 2, a)), stroke(slot="outline", width=w + 4, opacity=60, cap="butt")], f"o{a}"))
    comp.layer("hit ticks", ticks, position=C, ip=HIT, op=HIT + 14,
               scale=anim([(HIT, [150, 150], SNAP_OUT), (HIT + 4, [100, 100], HOLD), (HIT + 6, [100, 100], EASE_OUT), (HIT + 13, [115, 115])]),
               opacity=anim([(HIT, 100, HOLD), (HIT + 6, 100, EASE_IN), (HIT + 13, 0)]))


def recoil():
    return sampled(lambda t: [C[0], C[1] - 6 * bump(t, HIT, HIT + 10)], 0, F, 1)


def idle_breath(amp=3):
    return lambda t: amp * (0.5 - 0.5 * math.cos(TAU * t / F))


def base(name):
    comp = Comp(name, W, H, frames=F)
    comp.slot("primary", "#FFFFFF")
    comp.slot("accent", "#FF3B47")
    comp.slot("outline", "#000000")
    return comp


def outlined(shapes, w, slot="primary", cap="butt"):
    return [group(shapes + [stroke(slot=slot, width=w, cap=cap)], "line"),
            group(shapes + [stroke(slot="outline", width=w + 4, opacity=55, cap=cap)], "edge")]


# ---------------------------------------------------------------- cross

def cross():
    comp = base("crosshair-set")
    hit_ticks(comp, 30, 48)
    b = bloom(14)
    for a in (0, 90, 180, 270):
        comp.layer(f"arm {a}", outlined([seg(pt(0, a), pt(22, a))], 5),
                   position=sampled(lambda t, a=a: list(pt(14 + b(t) + idle_breath(2)(t), a, C)), 0, F, 1),
                   rotation=0)
        # the arm path above starts at the layer origin and runs outward
    comp.layer("dot", [group([ellipse((5, 5)), fill(slot="primary")], "d"), group([ellipse((9, 9)), fill(slot="outline", opacity=55)], "o")],
               position=recoil(), opacity=anim([(0, 100, HOLD), (HIT, 0, HOLD), (HIT + 6, 0, EASE_OUT), (HIT + 12, 100, HOLD), (F, 100)]))
    return comp


# ---------------------------------------------------------------- dot

def dot():
    comp = base("crosshair-set--dot")
    hit_ticks(comp, 18, 32, 4)
    comp.layer("pulse", [group([ellipse(anim([(HIT, [14, 14], DECEL), (HIT + 14, [70, 70])])), stroke(slot="primary", width=3)], "r")],
               position=C, ip=HIT, op=HIT + 15, opacity=anim([(HIT, 90, EASE_IN), (HIT + 14, 0)]))
    comp.layer("dot", [group([ellipse((10, 10)), fill(slot="primary")], "d"), group([ellipse((16, 16)), fill(slot="outline", opacity=55)], "o")],
               position=recoil(), scale=sampled(lambda t: [100 + 60 * bump(t, HIT, HIT + 8) + 10 * idle_breath(1)(t)] * 2, 0, F, 1))
    comp.layer("hit dot", [group([ellipse((10, 10)), fill(slot="accent")], "d")], position=recoil(),
               opacity=anim([(0, 0, HOLD), (HIT, 100, HOLD), (HIT + 5, 100, EASE_IN), (HIT + 12, 0, HOLD), (F, 0)]),
               scale=sampled(lambda t: [100 + 60 * bump(t, HIT, HIT + 8)] * 2, 0, F, 1))
    return comp


# ---------------------------------------------------------------- circle-dot

def circle_dot():
    comp = base("crosshair-set--circle-dot")
    hit_ticks(comp, 44, 60)
    b = bloom(12)
    comp.layer("dot", [group([ellipse((6, 6)), fill(slot="primary")], "d"), group([ellipse((10, 10)), fill(slot="outline", opacity=55)], "o")],
               position=recoil())
    r = lambda t: 34 + b(t) + idle_breath(2)(t)
    ring = [group([arc(1, a0, a0 + 70, 16)], f"a{a0}") for a0 in (10, 100, 190, 280)]
    comp.layer("ring", [group(ring + [stroke(slot="primary", width=3 / 34, cap="butt")], "line"),
                        group(ring + [stroke(slot="outline", width=7 / 34, opacity=55, cap="butt")], "edge")],
               position=C, scale=sampled(lambda t: [r(t) * 100] * 2, 0, F, 1),
               rotation=sampled(lambda t: 90 * smooth(clamp((t - HIT) / 16)), 0, F, 1))
    for a in (0, 90, 180, 270):
        comp.layer(f"tick {a}", outlined([seg((0, 0), (0, -8))], 3), position=sampled(lambda t, a=a: list(pt(r(t) + 8, a, C)), 0, F, 1),
                   rotation=a)
    return comp


build_asset(CAT, "crosshair-set", "Crosshair Set",
            "FPS crosshair that blooms outward on a shot, kicks with recoil and flashes red hit ticks, then settles, "
            "on a loop. Each variant is a different reticle style.",
            ["crosshair", "reticle", "aim", "fps", "shooter", "hitmarker", "gaming", "hud"], [
    Variant("cross", "Cross", cross(), "loop", thumb_t=0.28, region=(40, 40, 160, 160), pad=0,
            description="Classic four-arm cross with a centre dot; the arms spread on each shot."),
    Variant("dot", "Dot", dot(), "loop", thumb_t=0.24, region=(60, 60, 120, 120), pad=0,
            description="Minimal centre dot that pulses red with an expanding ring on a hit."),
    Variant("circle-dot", "Circle Dot", circle_dot(), "loop", thumb_t=0.3, region=(20, 20, 200, 200), pad=0,
            description="Segmented circle around a dot with cardinal ticks; the ring widens and twists on a shot."),
])
