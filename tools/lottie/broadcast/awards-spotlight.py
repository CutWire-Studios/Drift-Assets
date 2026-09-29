import math
import random

from _broadcast2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 120


def cone(length, spread, soft=(1.0, 0.7, 0.4), ops=(10, 12, 16), slot="primary", tip=6):
    """Light cone pointing down (+y) from (0, 0): stacked soft layers, brightest in the middle."""
    out = []
    for k, o in zip(soft, ops):
        half = length * math.tan(math.radians(spread * k / 2))
        out.append(group([path(bezier([(-tip * k, 0), (tip * k, 0), (half, length), (-half, length)],
                                      [(0, 0), (0, 0), (0, 0), (half * 0.55, half * 0.25)],
                                      [(0, 0), (0, 0), (-half * 0.55, half * 0.25), (0, 0)])),
                          fill(slot=slot, opacity=o)], f"cone{k}"))
    return out


def twinkles(comp, rng, n, area, slot, size=(40, 90), name="sparkles", drift=0):
    """Four-point sparkles, each twinkling twice per loop at its own phase (seamless)."""
    items = []
    for i in range(n):
        x, y = rng.uniform(area[0], area[2]), rng.uniform(area[1], area[3])
        s = rng.uniform(*size)
        ph = rng.uniform(0, 1)
        vals = []
        for k in range(24):
            u = (k / 24 + ph) % 0.5 / 0.5  # two twinkles per loop
            v = max(0.0, math.sin(u * math.pi * 3)) if u < 1 / 3 else 0.0
            vals.append([100 * v, 100 * v])
        pos = (x, y) if not drift else keys((0, [x, y], LINEAR), (F, [x, y + drift]))
        items.append(group([sparkle(s, 0, 0, 0.16), fill(slot=slot)], f"s{i}", position=pos,
                           scale=wave_keys(F, vals, EASE_IN_OUT), rotation=rng.uniform(-15, 15)))
    comp.layer(name, items)


def stage_glow(comp, color="#FFD99A", w=1600, h=320, y=H - 60, op=0.6):
    comp.layer("stage glow", [group([ellipse((w, h), (C[0], y)), gradient_fill(
        [(0, "#FFFFFF", op), (0.35, color, op * 0.6), (1, color, 0)], (C[0], y), (C[0] + w / 2, y),
        radial=True)], "glow")])


def classic():
    """Twin warm spotlights from the top corners sweep and cross over a glowing stage, with twinkling sparkles."""
    comp = Comp("awards-spotlight", W, H, fps=30, frames=F)
    comp.slot("primary", "#FFE2A6")
    comp.slot("accent", "#FFD55A")
    rng = random.Random(7)
    twinkles(comp, rng, 22, (120, 80, W - 120, H - 200), "accent")
    for nm, org, a0, a1 in (("left", (260, -60), -46, -18), ("right", (W - 260, -60), 46, 18)):
        comp.layer(f"beam {nm}", cone(1500, 22), position=org,
                   rotation=wave_keys(F, [a0, a1], SINE))
        comp.layer(f"lamp {nm}", [group([ellipse((90, 90)), fill(slot="primary", opacity=70)], "lamp"),
                                  group([ellipse((200, 200)), fill(slot="primary", opacity=18)], "halo")],
                   position=(org[0], 0))
    stage_glow(comp)
    return comp


def searchlights():
    """Premiere searchlights: four slim beams sweep up from the floor through haze, with rising glitter."""
    comp = Comp("awards-spotlight--searchlights", W, H, fps=30, frames=F)
    comp.slot("primary", "#CFE6FF")
    comp.slot("accent", "#FFFFFF")
    rng = random.Random(3)
    twinkles(comp, rng, 26, (80, 60, W - 80, H - 120), "accent", size=(26, 56), drift=-60)
    for i, (x, phase, amp) in enumerate(((330, 0, 24), (780, 1, 18), (1140, 0, 18), (1590, 1, 24))):
        base_a = 180 + (-16 if x < C[0] else 16)
        vals = [base_a - amp, base_a + amp] if phase == 0 else [base_a + amp, base_a - amp]
        comp.layer(f"beam{i}", cone(1500, 7, soft=(1.0, 0.55), ops=(12, 18), tip=10), position=(x, H + 30),
                   rotation=wave_keys(F, vals, SINE))
        comp.layer(f"source{i}", [group([ellipse((140, 60)), fill(slot="primary", opacity=40)], "src")],
                   position=(x, H - 8))
    comp.layer("haze", [box(0, H - 380, W, 380, "#000000", opacity=0),
                        group([rect_tl(0, H - 380, W, 380), gradient_fill(
                            [(0, "#FFFFFF", 0), (1, "#FFFFFF", 0.18)], (0, H - 380), (0, H))], "haze")])
    return comp


def center_stage():
    """A single spotlight from above opens onto a pool of light centre-stage, dust glinting in the beam."""
    comp = Comp("awards-spotlight--center-stage", W, H, fps=30, frames=F)
    comp.slot("primary", "#FFF1CF")
    comp.slot("accent", "#FFE08A")
    comp.slot("background", "#000000")
    rng = random.Random(5)
    # dust motes drifting in the beam
    motes = []
    for i in range(30):
        y = rng.uniform(80, H - 200)
        spread = 60 + (y / H) * 330
        x = C[0] + rng.uniform(-spread, spread)
        d = rng.uniform(40, 120)
        motes.append(group([ellipse((rng.uniform(4, 9),) * 2), fill(slot="accent", opacity=rng.uniform(40, 90))],
                           f"m{i}", position=wave_keys(F, [[x, y], [x + rng.uniform(-20, 20), y + d * 0.5]], SINE)))
    comp.layer("motes", motes)
    twinkles(comp, rng, 10, (C[0] - 500, H - 330, C[0] + 500, H - 120), "accent", size=(40, 80))
    breathe = wave_keys(F, [100, 86], SINE)
    comp.layer("pool", [group([ellipse((1300, 300), (C[0], H - 150)), gradient_fill(
        [(0, "#FFFFFF", 0.75), (0.45, "#FFE7B8", 0.45), (1, "#FFE7B8", 0)], (C[0], H - 150), (C[0] + 650, H - 150),
        radial=True)], "pool")], opacity=breathe)
    comp.layer("beam", cone(1180, 34, soft=(1.0, 0.8, 0.55), ops=(10, 12, 16), tip=40), position=(C[0], -40),
               opacity=breathe)
    comp.layer("darkness", [vignette(W, H, 0.75, 0.3)])
    return comp


build_asset(CAT, "awards-spotlight", "Awards Spotlight",
            "Full-frame awards-show lighting overlay: sweeping spotlights, stage glow and twinkling sparkles "
            "that loop behind a winner reveal or a title.",
            ["awards", "spotlight", "stage", "winner", "premiere", "sparkles", "celebration", "light"], [
    V("classic", "Twin Spots", classic(), "loop", thumb_t=0.5, bg="23232e",
      description="Two warm spotlights from the top corners sweep and cross over a glowing stage with sparkles."),
    V("searchlights", "Searchlights", searchlights(), "loop", thumb_t=0.25, bg="1a2233",
      description="Premiere searchlights sweeping up from the floor through haze, with rising glitter."),
    V("center-stage", "Center Stage", center_stage(), "loop", thumb_t=0.5, bg="2c2c36",
      description="One spotlight from above opens onto a pool of light, dust glinting in the beam."),
])
