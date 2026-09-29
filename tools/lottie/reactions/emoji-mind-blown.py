"""Mind blown: pressure builds, the top of the head blasts off on a mushroom cloud, then drops back
into place with a bounce (loop)."""

from _reactions2 import *

T = 90
W, H = 500, 560
R = 140
CX, CY = 250, 380
CUT = -46
BOOM = 16
FIRE, GLOW, SMOKE = "#FF7A2E", "#FFD24D", "#B7A9C9"

X0 = math.sqrt(R * R - CUT * CUT)
TEETH = [(-X0, CUT)] + [(-X0 + (2 * X0) * (i + 1) / 8, CUT + (12 if i % 2 == 0 else -10)) for i in range(7)] + [(X0, CUT)]
ZIG = " ".join(f"L {x:.2f} {y:.2f}" for x, y in TEETH[1:])
LOWER_D = f"M {-X0:.2f} {CUT} {ZIG} A {R} {R} 0 1 1 {-X0:.2f} {CUT} Z"
CAP_D = f"M {-X0:.2f} {CUT} {ZIG} A {R} {R} 0 0 0 {-X0:.2f} {CUT} Z"


def pressure(t):
    return smooth(t / BOOM) if t < BOOM else 1 - smooth((t - BOOM) / 30)


def jolt(t):
    return bump(t, BOOM, BOOM + 12)


def dazed(t):
    return smooth((t - BOOM) / 4) * (1 - smooth((t - 70) / 14))


def cap_off(t):
    """Cap transform relative to its seat: (dx, dy, rotation, opacity)."""
    if t < BOOM:
        return 0, 0, 0, 100
    if t < 38:
        u = (t - BOOM) / 22
        return (110 * u, -190 * ease_out(u, 2) + 50 * u * u, 60 * u,
                100 * (1 - smooth((u - 0.35) / 0.5)))
    if t < 60:
        return 0, -150, 0, 0
    u = (t - 60) / 12
    if u < 1:
        return 0, -150 * (1 - ease_in(u, 2)), 0, 100 * smooth(u * 3)
    b = (t - 72) / 14
    return 0, -22 * bump(b, 0, 0.5) - 6 * bump(b, 0.5, 1), 0, 100


PUFFS = [(-74, -8, 62), (-38, -44, 70), (10, -54, 74), (58, -34, 66), (84, 4, 54), (-18, 6, 60),
         (36, 10, 58)]


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-mind-blown", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("accent", FIRE)
    comp.slot("secondary", GLOW)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (2.5 * math.sin(TAU * t / 3) * pressure(t) * (t < BOOM), 16 * jolt(t)),
                     drot=lambda t: 2 * math.sin(TAU * t / 4) * pressure(t) * (t < BOOM),
                     dscale=lambda t: (100 + 7 * pressure(t) * (t < BOOM) + 8 * jolt(t),
                                       100 + 5 * pressure(t) * (t < BOOM) - 12 * jolt(t)))

    # the cap (drawn above the cloud's stem, flies off and drops back)
    cap_items = st.face_disc(R, shapes=S(CAP_D), shade=False, shadow=False)
    if st.flat:  # die-cut border only along the dome, so no white seam across the forehead
        for g in cap_items:
            g["it"] = [x for x in g["it"] if x.get("nm") != "diecut"]
        cap_items.append(group(S(f"M {-X0:.2f} {CUT} A {R} {R} 0 0 1 {X0:.2f} {CUT}") +
                               [stroke(WHITE, 2 * BORDER, slot="outline")], name="diecut"))
    comp.layer("cap", cap_items, parent=face,
                     position=sampled(lambda t: cap_off(t)[:2], 0, T),
                     rotation=sampled(lambda t: cap_off(t)[2], 0, T),
                     opacity=sampled(lambda t: cap_off(t)[3], 0, T))

    # mushroom cloud
    top = (CX, CY + CUT - 150)

    def puff_fn(i, x, y, r):
        def fn(u):
            k = u / 50
            grow = back_out(clamp(u / 10), 1.6) if u < 10 else 1 + 0.15 * (u - 10) / 40
            fade = 1 - smooth((k - 0.55) / 0.45)
            s = 100 * grow * (0.7 + 0.3 * fade)
            return {"position": (top[0] + x * (0.6 + 0.4 * grow), top[1] + y - 40 * k),
                    "scale": (s, s), "opacity": 100 * fade}
        return fn

    for i, (x, y, r) in enumerate(PUFFS):
        core = [group([ellipse((r * 0.8, r * 0.8)), fill(GLOW, slot="secondary")],
                      position=(-r * 0.12, -r * 0.14), name="core")]
        particle(comp, f"puff{i}", core + [group([ellipse((r * 1.6, r * 1.6))] +
                                                  st.paint(FIRE, "accent", (-r * .8, -r * .8, r * .8, r * .8),
                                                           sil=True, under=True), name="puff")],
                 BOOM + i * 0.8, 50, T, puff_fn(i, x, y, r), step=2, wrap=False)
    # stem
    def stem_fn(u):
        k = u / 44
        fade = 1 - smooth((k - 0.45) / 0.55)
        return {"position": (CX, CY + CUT - 10 - 30 * k), "scale": (100 * (0.6 + 0.4 * fade), 100 * ease_out(u / 8) * fade + 1),
                "opacity": 100 * clamp(fade * 1.5)}
    particle(comp, "stem", [group([rect((34, 130), (0, -70), roundness=17), fill(GLOW, slot="secondary")]),
                            group([rect((76, 150), (0, -75), roundness=36)] +
                                  st.paint(FIRE, "accent", (-38, -150, 38, 0), sil=True, under=True))],
             BOOM, 44, T, stem_fn, step=2, wrap=False)
    # debris sparks
    r = rng(3)
    for i in range(10):
        a = math.radians(-90 + r.uniform(-75, 75))
        sp = r.uniform(9, 15)

        def fn(u, a=a, sp=sp):
            d = sp * u * (1 - u / 40)
            return {"position": (CX + math.cos(a) * d, CY + CUT - 20 + math.sin(a) * d + 0.2 * u * u),
                    "rotation": u * 20, "scale": [100 * (1 - u / 22)] * 2}
        particle(comp, f"spark{i}", [group(S(star_d(12, 0.45)) + [fill(GLOW, slot="secondary")])],
                 BOOM, 20, T, fn, step=2, wrap=False)

    # the blown-open top: dark hole under where the cap sits
    comp.layer("hole", [group([ellipse((2 * X0 - 30, 34)), fill("#5A2310")])], parent=face,
               position=(0, CUT + 4),
               opacity=sampled(lambda t: 100 * (1 - smooth(abs(cap_off(t)[1]) < 3 and 1 or 0)), 0, T))

    # stunned features
    for side in (-1, 1):
        eye = comp.null(f"eye{side}", parent=face, position=(side * 48, 6),
                        scale=sampled(lambda t: [100 + 8 * dazed(t), 100 - 60 * pressure(t) * (t < BOOM) + 10 * dazed(t)], 0, T))
        comp.layer(f"pupil{side}", [group([ellipse((10, 10)), fill(WHITE)], position=(-4, -5)),
                                    group([ellipse((26, 28)), fill(st.ink)])], parent=eye,
                   scale=sampled(lambda t: [100 - 40 * dazed(t)] * 2, 0, T))
        comp.layer(f"white{side}", [group([ellipse((56, 64))] + st.paint(WHITE, lw=FLINE - 1))], parent=eye)
    o_d = "M -26 0 A 26 32 0 1 0 26 0 A 26 32 0 1 0 -26 0 Z"
    add_mouth(comp, st, o_d, face, tongue=((34, 20), (0, 28)), position=(0, 82),
              scale=sampled(lambda t: [70 + 40 * dazed(t), 40 + 70 * dazed(t)], 0, T))

    gr = R - (LINE / 2 if st.outline else 0)
    comp.layer("flush", [group([ellipse((2 * gr, 2 * gr)),
                                gradient_fill([(0, "#FF2A1F", 0.8), (0.7, "#FF2A1F", 0.3),
                                               (1, "#FF2A1F", 0)], (0, R), (0, -R * 0.2))])],
               parent=face, opacity=sampled(lambda t: 100 * pressure(t) * (t < BOOM + 8), 0, T))
    # the highlights sit on the cap, so drop them from the lower head
    lower = [g for g in st.face_disc(R, shapes=S(LOWER_D)) if g["nm"] not in ("highlight", "glint")]
    comp.layer("face-base", lower, parent=face)
    return comp


build3("emoji-mind-blown", "Emoji Mind Blown",
       "Face that builds up pressure until the top of its head blasts off on a mushroom cloud, then "
       "the lid drops back on with a bounce. Seamless loop.",
       ["emoji", "mind blown", "exploding head", "shocked", "wow", "omg", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.44, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.44, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.44, "Cartoon line art with bold black outlines."),
       ])
