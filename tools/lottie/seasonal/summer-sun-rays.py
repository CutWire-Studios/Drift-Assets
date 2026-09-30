"""Summer sun rays: a stylised sun (no face) with rotating rays and heat shimmer (seamless loops)."""

from _common import *

T = 120
W, H = 600, 640
C = (W / 2, 280)
SUN, RAY, HOT = "#FFC93C", "#FF9A1F", "#FF5A36"


def spin(deg):
    return anim([(0, 0, LINEAR), (T, deg)])


def shimmer(comp, y0, width, color, slot, n=3, amp=7, opacity=70):
    """Wavy heat lines travelling sideways, with a fading pulse."""
    for j in range(n):
        y = y0 + j * 26
        w = width * (1 - j * 0.22)

        def line(t, w=w, j=j):
            pts = [(lerp(-w / 2, w / 2, i / 10), amp * math.sin(TAU * (i / 10 * 2 + t / T * 2 + j * 0.3)))
                   for i in range(11)]
            return smooth_open(pts)
        comp.layer(f"heat{j}", [group([morph(line, 0, T, 3), stroke(color, 6 - j, slot=slot)], "wave")],
                   position=(C[0], y), opacity=looped(lambda t, j=j: opacity * (0.55 + 0.45 * wave(t, T, 2, j * 0.33)),
                                                      T, 3))


def flat():
    comp = Comp("summer-sun-rays", W, H, frames=T)
    comp.slot("primary", SUN)
    comp.slot("secondary", RAY)
    shimmer(comp, 520, 300, RAY, "secondary")
    comp.layer("core-hi", [ellipse((150, 150)), fill("#FFE27A", 80)], position=(C[0] - 18, C[1] - 18))
    comp.layer("core", [ellipse((230, 230)), fill(SUN, slot="primary")], position=C,
               scale=looped(lambda t: [100 + 2.5 * wave(t, T, 2)] * 2, T, 3))
    comp.layer("rim", [ellipse((250, 250)), stroke("#FFE27A", 6)], position=C,
               scale=looped(lambda t: [100 + 2.5 * wave(t, T, 2)] * 2, T, 3))
    for k, (n, r0, r1, w, off, col, sid) in enumerate(((12, 148, 236, 44, 0, RAY, "secondary"),
                                                       (12, 148, 192, 28, 15, SUN, "primary"))):
        rays = []
        for i in range(n):
            a = 360 * i / n + off
            tip = rot((0, -r1), a)
            b1, b2 = rot((-w / 2, -r0), a), rot((w / 2, -r0), a)
            rays.append(path(bezier([b1, tip, b2], closed=True)))
        comp.layer(f"rays{k}", [group(rays + [round_corners(8), fill(col, slot=sid)], "r")],
                   position=C, rotation=spin(30),
                   scale=looped(lambda t, k=k: [100 + 6 * wave(t, T, 4, k * 0.5)] * 2, T, 2))
    return comp


def glow_sun():
    comp = Comp("summer-sun-rays--glow", W, H, frames=T)
    comp.slot("primary", "#FFE07A")
    comp.slot("secondary", "#FFB02E")
    shimmer(comp, 540, 340, "#FFD27A", None, amp=5, opacity=45)
    comp.layer("core", [ellipse((200, 200)), gradient_fill([(0, "#FFFFFF"), (0.55, "#FFF3B8"), (1, "#FFD04A")],
                                                            (0, 0), (100, 0), radial=True)], position=C)
    comp.layer("corona", [ellipse((236, 236)), fill("#FFE07A", slot="primary")], position=C,
               scale=looped(lambda t: [100 + 5 * wave(t, T, 3)] * 2, T, 3))
    rays = []
    for i in range(24):
        a = 360 * i / 24
        L = 250 if i % 2 == 0 else 196
        rays += S(capsule_d(rot((0, -140), a), rot((0, -L), a), 5 if i % 2 == 0 else 4))
    comp.layer("rays", [group(rays + [fill("#FFB02E", slot="secondary")], "r")], position=C, rotation=spin(15),
               opacity=looped(lambda t: 80 + 20 * wave(t, T, 3), T, 3))
    for j in range(3):  # shimmer rings spreading out
        t0 = j * T / 3

        def fn(u):
            k = u / T
            return {"scale": [lerp(100, 180, k)] * 2, "opacity": 45 * bump(k, 0, 1)}
        particle(comp, f"wave{j}", [ellipse((260, 260)), stroke("#FFD27A", 3)], t0, T, T, fn, step=3,
                 position=C)
    comp.layer("bloom", [glow(300, "#FFC94A", 100, falloff=((0, 0.6), (0.4, 0.3), (1, 0)))], position=C,
               opacity=looped(lambda t: 70 + 20 * wave(t, T, 2), T, 3))
    return comp


def retro():
    comp = Comp("summer-sun-rays--retro", W, H, frames=T)
    comp.slot("primary", SUN)
    comp.slot("secondary", RAY)
    comp.slot("accent", HOT)
    shimmer(comp, 530, 320, HOT, "accent", amp=8)

    def wavy(r, n, amp, ph):
        pts = []
        for i in range(n * 4):
            a = TAU * i / (n * 4)
            rr = r * (1 + amp * math.sin(n * a + ph))
            pts.append((rr * math.sin(a), -rr * math.cos(a)))
        return smooth_closed(pts)

    rings = [(118, SUN, "primary"), (140, RAY, "secondary"), (160, HOT, "accent")]
    for j, (r, col, sid) in enumerate(rings):
        comp.layer(f"band{j}", [ellipse((2 * r, 2 * r)), fill(col, slot=sid)], position=C)
    # two wavy ray crowns turning in opposite directions and breathing
    for j, (r, n, amp, col, sid, deg) in enumerate(((236, 14, 0.1, RAY, "secondary", 360 / 14),
                                                    (206, 14, 0.12, SUN, "primary", -360 / 14))):
        comp.layer(f"crown{j}", [group([morph(lambda t, r=r, n=n, amp=amp, j=j: wavy(r, n, amp * (1 + 0.25 * wave(t, T, 2, j * 0.5)),
                                                                                     j * 0.5), 0, T, 4),
                                        fill(col, slot=sid)], "c")], position=C, rotation=spin(deg))
    # sunset stripes across the core
    comp.layer("stripes-matte", [ellipse((236, 236)), fill(WHITE)], position=C)
    comp.layer("stripes", [group([rect((260, 10 + 3 * k), (0, 30 + 26 * k)) for k in range(4)] +
                                 [fill(HOT, slot="accent")], "s")], position=C, matte="alpha")
    comp.layer("core-hi", [ellipse((180, 180)), fill("#FFE27A")], position=(C[0], C[1] - 22))
    # swap draw order: bands must sit above the crowns
    bands = [l for l in comp.layers if l["nm"].startswith("band")]
    crowns = [l for l in comp.layers if l["nm"].startswith("crown")]
    rest = [l for l in comp.layers if l not in bands and l not in crowns]
    hi = [l for l in rest if l["nm"] == "core-hi"]
    heat = [l for l in rest if l["nm"].startswith("heat")]
    stripes = [l for l in rest if l["nm"].startswith("stripes")]
    comp.layers = heat + stripes + hi + bands + crowns
    for i, l in enumerate(comp.layers):
        l["ind"] = i + 1
    return comp


build("summer-sun-rays", "Summer Sun Rays",
      "A bold stylised summer sun with slowly rotating rays and wavy heat shimmer underneath; a seamless loop.",
      ["summer", "sun", "sunshine", "hot", "heat", "beach", "sunny"], [
          Variant("flat", "Flat", flat(), "loop", thumb_t=0.2,
                  description="Flat modern sun with two counter-rotating crowns of rounded triangle rays."),
          Variant("glow", "Glow", glow_sun(), "loop", thumb_t=0.2,
                  description="Radiant glowing sun with long needle rays, a pulsing corona and spreading heat rings."),
          Variant("retro", "Retro", retro(), "loop", thumb_t=0.2,
                  description="Seventies-style banded sun with wavy ray crowns and sunset stripes."),
      ])
