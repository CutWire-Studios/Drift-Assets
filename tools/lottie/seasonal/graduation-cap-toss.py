"""Graduation cap toss: mortarboards flung into the air with swinging tassels (seamless loops)."""

from _common import *

T = 90
CAP, GOLD = "#1E2233", "#FFC53A"
BOARD = S("M 0 -32 L 94 0 L 0 32 L -94 0 Z")
EDGE = S("M -94 0 L 0 32 L 94 0 L 94 9 L 0 41 L -94 9 Z")
SKULL = S("M -52 8 L 52 8 L 48 54 C 22 64 -22 64 -48 54 Z")


def tassel(t0, t1, ph, style):
    """Cord from the button to the front-right corner, then the swinging tassel."""
    ink = style == "doodle"
    paint_line = stroke(INK if ink else GOLD, 4, slot="outline" if ink else "accent")
    cord = group(S("M 0 0 C 30 6 60 4 84 3") + [stroke(GOLD, 4, slot="accent")], "cord")
    hang = [group(S("M 0 0 L 0 40") + [stroke(GOLD, 4, slot="accent")], "string"),
            group([rect((10, 8), (0, 42), 2), fill("#E0A020")], "knot"),
            group(S("M -8 46 L 8 46 L 11 76 L -11 76 Z") + ([stroke(INK, 3.5, slot="outline")] if ink else []) +
                  [fill(GOLD, slot="accent")], "tuft"),
            group(S("M -4 50 L -5 74 M 0 50 L 0 75 M 4 50 L 5 74") + [stroke("#C88A10", 2)], "strands")]
    swing = group(hang, "swing")
    swing["it"][-1] = transform(shape=True, position=(84, 3), rotation=osc_keys(t0, t1, 22, -26, 26, ph))
    return [swing, cord] + ([paint_line] if False else [])


def cap_items(t0, t1, ph=0.0, style="flat"):
    ink = style == "doodle"
    line = [stroke(INK, 5, slot="outline")] if ink else []
    items = tassel(t0, t1, ph, style)
    items.append(group([ellipse((16, 10)), fill(GOLD, slot="accent")] + line[:0], "button"))
    if not ink:
        items.append(group(S("M -60 -12 L 0 -32 L 30 -22 L -30 -2 Z") + [fill(WHITE, 14)], "sheen"))
    items.append(group(BOARD + line + [fill(CAP, slot="primary")], "board"))
    items.append(group(EDGE + line + [fill("#000000", 100 if not ink else 0)] +
                       ([] if ink else []), "edge-dark"))
    items.append(group(EDGE + [fill(CAP, slot="primary")], "edge"))
    if not ink:
        items.append(group(SKULL + [gradient_fill([(0, WHITE, 0.14), (0.5, WHITE, 0), (1, "#000000", 0.35)],
                                                  (-52, 0), (52, 0))], "skull-shade"))
    items.append(group(SKULL + line + [fill(CAP, slot="primary")], "skull"))
    return items


def toss_particle(comp, name, T_, t0, life, x0, x1, apex, floor, sz, spin, ph, style, flip=True):
    if style == "doodle":
        flip = False
    def fn(u):
        k = u / life
        y = floor - (floor - apex) * 4 * k * (1 - k)
        return {"position": (lerp(x0, x1, k), y), "rotation": spin * (k - 0.5),
                "scale": [100 * sz * (math.cos(TAU * k * 1.0) * 0.35 + 0.65 if flip else 1), 100 * sz]}
    starts = [t0] + ([t0 - T_] if t0 + life > T_ else [])
    for s in starts:
        keys = {k: sampled(lambda t, k=k, s=s: fn(min(max(t - s, 0), life))[k], s, s + life, 2)
                for k in ("position", "rotation", "scale")}
        comp.layer(name, cap_items(s, s + life, ph, style), ip=s, op=s + life, **keys)


def toss():
    W, H = 1920, 1080
    comp = Comp("graduation-cap-toss", W, H, frames=T)
    comp.slot("primary", CAP)
    comp.slot("accent", GOLD)
    r = rng(7)
    n = 11
    for i in range(n):
        t0 = (i * T / n + r.uniform(0, 4)) % T
        x0 = 140 + (W - 280) * ((i * 5) % n + 0.5) / n
        toss_particle(comp, f"cap{i}", T, t0, T, x0, x0 + r.uniform(-200, 200), r.uniform(120, 420), H + 110,
                      r.uniform(1.1, 1.8), r.uniform(-260, 260), r.random(), "flat")
    return comp


def single():
    W, H = 600, 720
    comp = Comp("graduation-cap-toss--hero", W, H, frames=T)
    comp.slot("primary", CAP)
    comp.slot("accent", GOLD)
    # tossed up from a resting spot with anticipation, a full flip at the top, then caught with a bounce
    def y(t):
        u = t / T
        if u < 0.12:
            return 560 + 30 * math.sin(math.pi * u / 0.12)
        if u < 0.82:
            k = (u - 0.12) / 0.7
            return 560 - 360 * 4 * k * (1 - k)
        k = (u - 0.82) / 0.18
        return 560 + 26 * math.sin(math.pi * k) * (1 - k)

    def flipx(t):
        u = t / T
        if 0.12 < u < 0.82:
            k = (u - 0.12) / 0.7
            return math.cos(TAU * ease_in_out(k))
        return 1

    def squash(t):
        u = t / T
        if u < 0.12:
            return 1 - 0.18 * math.sin(math.pi * u / 0.12)
        if u > 0.82:
            return 1 - 0.14 * math.sin(math.pi * (u - 0.82) / 0.18)
        return 1

    comp.layer("cap", cap_items(0, T, 0.1, "flat"),
               position=looped(lambda t: (W / 2, y(t)), T, 1),
               rotation=looped(lambda t: -12 * math.sin(TAU * t / T), T, 2),
               scale=looped(lambda t: [210 * (0.35 + 0.65 * abs(flipx(t))) * (2 - squash(t)),
                                       210 * squash(t)], T, 1))
    comp.layer("shadow", [ellipse((260, 30)), fill("#000000", 26)], position=(W / 2, 690),
               scale=looped(lambda t: [100 * (0.45 + 0.55 * (y(t) - 200) / 360)] * 2, T, 1))
    cols = ["#FFC53A", "#FFFFFF", "#7CC8FF", "#FF7AA8"]
    for j in range(6):
        a = -90 + (j - 2.5) * 34
        p = (W / 2 + 230 * math.cos(math.radians(a)), 220 + 150 * math.sin(math.radians(a)) + 40)
        sparkle(comp, f"spark{j}", p, T, 18 + (j % 3) * 6, cols[j % 4], t0=22 + j * 3, period=T)
    return comp


def doodle():
    W, H = 900, 720
    comp = Comp("graduation-cap-toss--doodle", W, H, frames=T)
    comp.slot("primary", "#3A3F66")
    comp.slot("accent", GOLD)
    comp.slot("outline", INK)
    for i, (x, dx, apex, t0, sz, sp) in enumerate(((220, 60, 190, 0, 1.3, 60), (450, -30, 130, 30, 1.45, -50),
                                                   (680, -70, 210, 60, 1.25, 45))):
        toss_particle(comp, f"cap{i}", T, t0, T, x, x + dx, apex, H + 110, sz, sp, i * 0.3, "doodle")
    for j, (p, t0) in enumerate((((120, 140), 0), ((780, 110), 25), ((450, 330), 50), ((820, 420), 70),
                                  ((80, 420), 40))):
        comp.layer(f"star{j}", [group(S(star_d(20, 0.45)) + [stroke(INK, 4.5, slot="outline"),
                                                             fill(GOLD, slot="accent")], "s")], position=p,
                   scale=looped(lambda t, t0=t0: [100 * (0.75 + 0.25 * wave(t, T, 2, t0 / T))] * 2, T, 3),
                   rotation=looped(lambda t, t0=t0: 14 * wave(t, T, 1, t0 / T), T, 3))
    return comp


build("graduation-cap-toss", "Graduation Cap Toss",
      "Mortarboards tossed into the air with swinging gold tassels to celebrate graduation; seamless loops.",
      ["graduation", "cap", "mortarboard", "tassel", "school", "celebration", "class of"], [
          Variant("toss", "Cap Toss", toss(), "loop", thumb_t=0.5, region=(480, 100, 960, 900), pad=0,
                  description="Full-frame transparent overlay of caps flung up from the bottom edge, tumbling and falling back."),
          Variant("hero", "Hero Cap", single(), "loop", thumb_t=0.47,
                  description="One big cap flipping up into view with twinkling sparkles, then dropping away."),
          Variant("doodle", "Doodle", doodle(), "loop", thumb_t=0.5, bg="f3ece0",
                  description="Hand-drawn ink caps tossed in turn among bobbing doodle stars."),
      ])
