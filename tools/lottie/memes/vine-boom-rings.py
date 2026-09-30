"""Full-frame bass-drop boom: an impact flash and shockwave rings punch out from the centre."""

from _memes2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 45
HIT = 3


def rings_layer(comp, name, t0, dur, d0, d1, width, slot=None, color="#FFFFFF", op=100, offset=(0, 0), dashes=None,
                glow=True):
    size = keys((t0, [d0, d0], EXPO_OUT), (t0 + dur, [d1, d1]))
    wk = lambda m: keys((t0, width * m, LINEAR), (t0 + dur, width * m * 0.3))
    items = [group([ellipse(size), stroke(color, slot=slot, width=wk(1), dashes=dashes)], "ring")]
    if glow:
        items.append(group([ellipse(size), stroke(color, slot=slot, width=wk(3.2), opacity=18, dashes=dashes)], "glow"))
    comp.layer(name, items, position=(C[0] + offset[0], C[1] + offset[1]),
               opacity=keys((t0, op, EASE_IN), (t0 + dur, 0)), ip=t0, op=t0 + dur + 1)


def edge_shake(comp, color, width, op):
    """A dark frame border that jolts with the hit, like a camera shake."""
    comp.layer("shake", [vignette(W, H, op / 100, 0.35)],
               anchor=C, position=keys(*shake_keys(HIT, HIT + 16, 26, 5, step=2, pivot=C)),
               scale=keys((HIT, [112, 112], EXPO_OUT), (HIT + 14, [100, 100])),
               opacity=keys((0, 0, HOLD), (HIT, 100, HOLD), (HIT + 12, 100, EASE_IN), (F - 6, 0)))


def classic():
    """White impact flash, three expanding shockwave rings and a shaking dark vignette."""
    comp = base("vine-boom-rings", W, H, F, HIT + 3, HIT + 8)
    comp.slot("primary", "#FFFFFF")
    for i, (t, w) in enumerate([(HIT, 40), (HIT + 4, 24), (HIT + 8, 14)]):
        rings_layer(comp, f"ring{i}", t, 26, 200, 2300 - i * 300, w, slot="primary")
    comp.layer("core", [group([ellipse((420, 420), C), fill(slot="primary")], "core")],
               anchor=C, position=C, scale=keys((HIT, [30, 30], EXPO_OUT), (HIT + 8, [130, 130])),
               opacity=keys((HIT, 90, EASE_IN), (HIT + 8, 0)), ip=HIT, op=HIT + 9)
    comp.layer("flash", [group([rect((W, H), C), fill(slot="primary")], "flash")],
               opacity=keys((0, 0, HOLD), (HIT, 85, EASE_OUT), (HIT + 7, 0)), ip=0, op=HIT + 8)
    edge_shake(comp, "#000000", 0, 70)
    return comp


def chroma():
    """Bass-speaker rings split into cyan and magenta with a coloured flash, like a TV-glitch boom."""
    comp = base("vine-boom-rings--chroma", W, H, F, HIT + 3, HIT + 8)
    comp.slot("primary", "#FF2BD6")
    comp.slot("secondary", "#23E5FF")
    for i, t in enumerate([HIT, HIT + 5, HIT + 10]):
        rings_layer(comp, f"m{i}", t, 24, 240, 2100 - i * 260, 30 - i * 6, slot="primary", offset=(-14, 0))
        rings_layer(comp, f"c{i}", t, 24, 240, 2100 - i * 260, 30 - i * 6, slot="secondary", offset=(14, 0))
        rings_layer(comp, f"w{i}", t, 24, 240, 2100 - i * 260, 10 - i * 2, color="#FFFFFF", op=90)
    comp.layer("flash-m", [group([rect((W, H), C), fill(slot="primary")], "flash")],
               opacity=keys((0, 0, HOLD), (HIT, 55, EASE_OUT), (HIT + 8, 0)), op=HIT + 9, blend=2)
    comp.layer("flash-c", [group([rect((W, H), C), fill(slot="secondary")], "flash")],
               opacity=keys((0, 0, HOLD), (HIT + 2, 40, EASE_OUT), (HIT + 10, 0)), op=HIT + 11, blend=2)
    for i, (y, h, dx) in enumerate([(300, 60, 90), (620, 34, -140), (820, 80, 60)]):
        comp.layer(f"slice{i}", [group([rect((W, h), (W / 2, y)), fill(slot="secondary" if i % 2 else "primary",
                                                                       opacity=35)], "s")],
                   position=keys((HIT, [dx, 0], HOLD), (HIT + 3, [-dx, 0], HOLD), (HIT + 6, [0, 0])),
                   ip=HIT, op=HIT + 7)
    edge_shake(comp, "#000000", 0, 60)
    return comp


def comic():
    """Cartoon impact: a jagged starburst outline and radial strokes blast out with dashed rings."""
    comp = base("vine-boom-rings--comic", W, H, F, HIT + 3, HIT + 8)
    comp.slot("primary", "#FFD23F")
    comp.slot("outline", INK)
    rng = random.Random(9)
    pts = []
    n = 14
    for i in range(2 * n):
        a = TAU * i / (2 * n) + rng.uniform(-0.05, 0.05)
        r = (440 if i % 2 == 0 else 250) * rng.uniform(0.9, 1.1)
        pts.append((r * math.cos(a), r * math.sin(a)))
    burst = polyline(pts, closed=True)
    grow = keys((HIT, [20, 20], EXPO_OUT), (HIT + 8, [110, 110], LINEAR), (HIT + 22, [125, 125], EASE_IN),
                (HIT + 30, [140, 140]))
    fade_k = keys((HIT, 100, HOLD), (HIT + 20, 100, EASE_IN), (HIT + 30, 0))
    comp.layer("burst", [group([burst, fill("#FFFFFF")], "inner", scale=(58, 58)),
                         group([burst, stroke(slot="outline", width=18), fill(slot="primary")], "b")],
               position=C, scale=grow, opacity=fade_k, rotation=keys((HIT, -8, EXPO_OUT), (HIT + 30, 6)),
               ip=HIT, op=HIT + 31)
    lines = []
    for i in range(16):
        a = TAU * (i + 0.5) / 16
        lines.append(polyline([(math.cos(a) * 520, math.sin(a) * 520), (math.cos(a) * 760, math.sin(a) * 760)]))
    comp.layer("rays", [group(lines + [trim(start=keys((HIT + 2, 0, EASE_IN), (HIT + 16, 100)),
                                            end=keys((HIT, 0, EXPO_OUT), (HIT + 8, 100))),
                                       stroke(slot="outline", width=18)], "rays")],
               position=C, scale=keys((HIT, [80, 80], EXPO_OUT), (HIT + 16, [150, 150])), ip=HIT, op=HIT + 17)
    for i, t in enumerate([HIT + 2, HIT + 7]):
        rings_layer(comp, f"ring{i}", t, 24, 500, 2200 - i * 300, 20, slot="outline", dashes=[60, 40], glow=False)
    comp.layer("flash", [group([rect((W, H), C), fill("#FFFFFF")], "flash")],
               opacity=keys((0, 0, HOLD), (HIT, 75, EASE_OUT), (HIT + 5, 0)), op=HIT + 6)
    return comp


build_asset(CAT, "vine-boom-rings", "Boom Impact Rings",
            "Full-frame bass-drop boom: a quick impact flash and shockwave rings punch out from the centre while "
            "the edges jolt. Sync it to the hit in your audio.",
            ["boom", "impact", "shockwave", "bass", "flash", "meme", "shake"], [
    Variant("classic", "Shockwave", classic(), "intro-hold-outro", thumb_t=0.26,
            description="White impact flash, three shockwave rings and a shaking dark vignette."),
    Variant("chroma", "Chroma Split", chroma(), "intro-hold-outro", thumb_t=0.24,
            description="Rings split into magenta and cyan with a coloured flash and glitch slices."),
    Variant("comic", "Comic Burst", comic(), "intro-hold-outro", thumb_t=0.22, bg="e8e8ee",
            description="Cartoon starburst with ink rays and dashed rings blasting outward."),
])
