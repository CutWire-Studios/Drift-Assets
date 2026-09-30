"""Ghost float: a cute little ghost bobbing in the air with a waving hem (seamless loop)."""

from _common import *

T = 90
W, H = 460, 560
C = (W / 2, 250)


def body_pts(t, wob=1.0, hem_y=110, n_hem=9, R=100):
    """Dome head, slightly flared sides and a wavy hem whose scallops travel sideways."""
    pts = []
    for i in range(9):  # dome from left (180 deg) over the top to the right (360 deg)
        a = math.radians(180 + 180 * i / 8)
        pts.append((R * math.cos(a), -20 + R * 1.02 * math.sin(a)))
    pts.append((R * 1.04, 40))
    for i in range(n_hem + 1):  # hem right to left
        k = i / n_hem
        x = lerp(R * 1.1, -R * 1.1, k)
        edge = math.sin(math.pi * k) ** 0.5
        y = hem_y + (16 if i % 2 == 0 else -4) * (0.4 + 0.6 * edge) + 7 * wob * edge * math.sin(TAU * (t / T * 2 + k * 1.5))
        x += 6 * wob * edge * math.sin(TAU * (t / T * 2 + k))
        pts.append((x, y))
    pts.append((-R * 1.04, 40))
    return pts


def blink(t0, dur=6):
    return Anim([(0, [100, 100], HOLD), (t0, [100, 100], EASE_IN), (t0 + dur / 2, [100, 8], EASE_OUT),
                 (t0 + dur, [100, 100], HOLD), (T, [100, 100])])


def bob(t, amp=16):
    return (C[0], C[1] + amp * wave(t, T, 1, 0.25))


def cute():
    comp = Comp("ghost-float", W, H, frames=T)
    comp.slot("primary", "#FFFFFF")
    comp.slot("secondary", "#2B2340")
    g = comp.null("ghost", position=looped(bob, T, 2), rotation=looped(lambda t: 4 * wave(t, T, 1), T, 3),
                  scale=(125, 125))
    face = comp.null("face", parent=g, position=looped(lambda t: (5 * wave(t, T, 1), 0), T, 3))
    comp.layer("eyes", [group([ellipse((20, 28)), fill("#2B2340", slot="secondary")], "l", position=(-30, -18)),
                        group([ellipse((20, 28)), fill("#2B2340", slot="secondary")], "r", position=(30, -18)),
                        group([ellipse((7, 8), (-27, -24)), ellipse((7, 8), (33, -24)), fill(WHITE)], "catch")],
               parent=face, scale=blink(52), anchor=(0, -18), position=(0, -18))
    comp.layer("mouth", [group([ellipse((16, 20)), fill("#2B2340", slot="secondary")], "o"),
                         group([ellipse((8, 7), (0, 5)), fill("#FF7FA8")], "tongue")], parent=face,
               position=(0, 16), scale=looped(lambda t: [100, 100 + 18 * wave(t, T, 2)], T, 3))
    comp.layer("blush", [ellipse((26, 13), (-56, 6)), ellipse((26, 13), (56, 6)), fill("#FF8FB0", 55)], parent=face)
    for side in (-1, 1):  # little arms waving
        comp.layer(f"arm{side}", [group([ellipse((34, 44)), fill(WHITE, slot="primary")], "arm"),
                                  group([ellipse((34, 44)), fill("#6C7FC7", 16)], "arm-shade", position=(0, 2))],
                   parent=g, position=(side * 90, 40), anchor=(-side * 8, 14),
                   rotation=looped(lambda t, side=side: side * (30 + 18 * wave(t, T, 2, 0.1 if side > 0 else 0.35)),
                                   T, 2))
    body = lambda t: smooth_closed(body_pts(t))
    comp.layer("shade", [group([morph(body, 0, T, 2),
                                gradient_fill([(0, "#6C7FC7", 0), (0.6, "#6C7FC7", 0.05), (1, "#6C7FC7", 0.35)],
                                              (-40, -80), (60, 130))], "shade")], parent=g)
    comp.layer("shine", [group([ellipse((22, 44)), fill(WHITE)], "s", position=(-56, -62), rotation=30)], parent=g,
               opacity=0)
    comp.layer("body", [group([morph(body, 0, T, 2), fill(WHITE, slot="primary")], "body")], parent=g)
    comp.layer("shadow", [ellipse((200, 28)), fill("#000000", 22)], position=(C[0], 515),
               scale=looped(lambda t: [100 - 18 * wave(t, T, 1, 0.25)] * 2, T, 3),
               opacity=looped(lambda t: 100 - 30 * wave(t, T, 1, 0.25), T, 3))
    return comp


def spirit_pts(t, R=92):
    """Head plus a tapering tail that curls and sways."""
    pts = []
    for i in range(9):
        a = math.radians(180 + 180 * i / 8)
        pts.append((R * math.cos(a), -20 + R * math.sin(a)))
    sw = lambda k: 34 * k * math.sin(TAU * (t / T * 2 - k * 0.9))
    rt = [(R * 0.98, 30), (R * 0.8, 90), (R * 0.45, 150), (8, 200)]
    lt = [(-R * 0.35, 150), (-R * 0.75, 90), (-R * 0.98, 30)]
    for (x, y) in rt:
        k = (y + 20) / 220
        pts.append((x + sw(k), y))
    pts.append((sw(1.05) + 14, 222))
    for (x, y) in lt:
        k = (y + 20) / 220
        pts.append((x + sw(k), y))
    return pts


def spirit():
    comp = Comp("ghost-float--spirit", W, H, frames=T)
    comp.slot("primary", "#BFFFF1")
    teal = "#5FF2D3"
    g = comp.null("ghost", position=looped(lambda t: (C[0] + 10 * wave(t, T, 1), C[1] - 30 + 20 * wave(t, T, 1, 0.25)),
                                            T, 2), rotation=looped(lambda t: -5 * wave(t, T, 1), T, 3), scale=(115, 115))
    comp.layer("eyes", [group([ellipse((24, 34), (-30, -18)), ellipse((24, 34), (30, -18)), fill("#0C3B3A")], "e")],
               parent=g, scale=blink(40, 8), anchor=(0, -18), position=(0, -18))
    comp.layer("mouth", [group([ellipse((20, 30)), fill("#0C3B3A")], "o")], parent=g, position=(0, 26),
               scale=looped(lambda t: [100, 90 + 20 * wave(t, T, 2)], T, 3))
    body = lambda t: smooth_closed(spirit_pts(t))
    comp.layer("core", [group([morph(body, 0, T, 2), gradient_fill(
        [(0, WHITE, 0.95), (0.5, "#DFFFF8", 0.75), (1, teal, 0.0)], (0, -40), (0, 230))], "core")], parent=g)
    comp.layer("body", [group([morph(body, 0, T, 2), fill("#BFFFF1", 80, slot="primary")], "body")], parent=g,
               opacity=looped(lambda t: 82 + 12 * wave(t, T, 3), T, 3))
    comp.layer("aura", [glow(210, teal, 100, falloff=((0, 0.5), (0.5, 0.2), (1, 0)), position=(0, 30))], parent=g,
               opacity=looped(lambda t: 70 + 25 * wave(t, T, 2), T, 3))
    # wisps rising off the ghost
    r = rng(3)
    for i in range(7):
        t0 = i * T / 7
        x = r.uniform(-80, 80)

        def fn(u, x=x):
            k = u / 50
            return {"position": (C[0] + x + 14 * math.sin(k * 5), C[1] + 90 - 220 * k),
                    "opacity": 80 * bump(k, 0, 1), "scale": [lerp(100, 40, k)] * 2}
        particle(comp, f"wisp{i}", [ellipse((12, 12)), fill("#DFFFF8")], t0, 50, T, fn, step=2)
    return comp


def doodle():
    comp = Comp("ghost-float--doodle", W, H, frames=T)
    comp.slot("outline", INK)
    comp.slot("primary", "#FFFFFF")
    every = 3

    def boiled(fn, seed, amp=2.2):
        keys = []
        for j in range(T // every):
            r = random.Random(seed * 100 + j)
            pts = [(x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)) for x, y in fn(j * every)]
            keys.append((j * every, smooth_closed(pts), HOLD))
        keys.append((T, keys[0][1], HOLD))
        return path(Anim(keys))

    g = comp.null("ghost", position=looped(lambda t: bob(t, 20), T, 2),
                  rotation=looped(lambda t: 5 * wave(t, T, 1), T, 3), scale=(118, 118))
    comp.layer("lines", [group(S("M -150 -60 L -128 -54 M -156 -20 L -132 -20 M 150 -60 L 128 -54 M 156 -20 L 132 -20")
                               + [stroke(INK, 5, slot="outline")], "motion")], parent=g,
               opacity=looped(lambda t: 100 * clamp(wave(t, T, 1, 0.25) * 2 + 0.5), T, 2))
    comp.layer("face", [
        group([boiled(lambda t: circle_pts(11, 8, sy=1.35), 7, 1.0), fill(INK, slot="outline")], "l",
              position=(-30, -20)),
        group([boiled(lambda t: circle_pts(11, 8, sy=1.35), 8, 1.0), fill(INK, slot="outline")], "r",
              position=(30, -20)),
        group(S("M -18 16 Q -9 26 0 16 Q 9 26 18 16") + [stroke(INK, 5, slot="outline")], "mouth"),
        group([ellipse((24, 12), (-56, 8)), ellipse((24, 12), (56, 8)), fill("#FF8FB0", 70)], "blush"),
    ], parent=g, scale=blink(48), anchor=(0, -20), position=(0, -20))
    for side in (-1, 1):
        comp.layer(f"arm{side}", [group([boiled(lambda t: circle_pts(18, 8, sy=1.3), 20 + side, 1.2),
                                         stroke(INK, 5.5, slot="outline"), fill(WHITE, slot="primary")], "arm")],
                   parent=g, position=(side * 94, 44), anchor=(-side * 8, 14),
                   rotation=looped(lambda t, side=side: side * (26 + 20 * wave(t, T, 2, 0.1 if side > 0 else 0.4)),
                                   T, 2))
    comp.layer("line", [group([boiled(body_pts, 1), stroke(INK, 6.5, slot="outline")], "line")], parent=g)
    comp.layer("body", [group([boiled(body_pts, 2, 1.0), fill(WHITE, slot="primary")], "body", position=(8, 7))],
               parent=g)
    comp.layer("shadow", [group([boiled(lambda t: circle_pts(80, 12, sy=0.16), 9, 1.5), stroke(INK, 4, slot="outline")],
                                "s")], position=(C[0], 505),
               scale=looped(lambda t: [100 - 20 * wave(t, T, 1, 0.25)] * 2, T, 3))
    return comp


build("ghost-float", "Ghost Float",
      "A friendly little ghost bobbing in mid-air with a waving hem; a seamless Halloween loop to place "
      "anywhere in the frame.",
      ["ghost", "halloween", "spooky", "cute", "boo", "floating"], [
          Variant("cute", "Cute", cute(), "loop", thumb_t=0.2,
                  description="Soft white cartoon ghost with blushing cheeks, waving arms and a rippling hem."),
          Variant("spirit", "Glowing Spirit", spirit(), "loop", thumb_t=0.3,
                  description="Translucent glowing spirit with a curling tail, a pulsing aura and rising wisps."),
          Variant("doodle", "Doodle", doodle(), "loop", thumb_t=0.2, bg="f3ece0",
                  description="Hand-drawn ink ghost with a boiling line, off-register fill and motion ticks."),
      ])
