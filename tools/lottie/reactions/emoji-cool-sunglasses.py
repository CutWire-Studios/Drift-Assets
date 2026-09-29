"""Cool face in shades: nods to the beat with a smirk while a glint sweeps across the lenses
(loop)."""

from _reactions2 import *

T = 60
BEAT = 30
W, H = 460, 460
R = 150
CX, CY = 230, 240
LENS = "#1D2030"

LENS_D = ("M -48 -24 L 42 -24 C 48 -24 50 -20 49 -14 C 46 10 30 28 4 28 "
          "C -24 28 -44 12 -49 -12 C -50 -20 -48 -24 -48 -24 Z")


def nod(t):
    u = (t % BEAT) / BEAT
    return math.sin(math.pi * u) ** 2


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-cool-sunglasses", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("secondary", LENS)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (3 * wave(t, T), 12 * nod(t)),
                     drot=lambda t: 5 * wave(t, T) - 2 * nod(t),
                     dscale=lambda t: (100 + 2.5 * nod(t), 100 - 3 * nod(t)))

    # shades lag a touch behind the head on each nod
    shades = comp.null("shades", parent=face, position=sampled(lambda t: (0, -30 - 5 * nod(t - 3)), 0, T))

    lens_l = S(LENS_D, offset=(-56, 0))
    lens_r = mirror(S(LENS_D), 56)
    lenses = lens_l + lens_r

    # glint band sweeping across the lenses (matted to them)
    comp.layer("glint-matte", [group(lenses + [fill(WHITE)])], parent=shades)
    comp.layer("glint", [group([rect((26, 160)), fill(WHITE, 85)], position=(30, 0)),
                         group([rect((10, 160)), fill(WHITE, 70)])],
               parent=shades, matte="alpha", rotation=24,
               position=sampled(lambda t: (-150 + 300 * smooth((t - 30) / 16), 0), 28, 48))

    refl = []
    if not st.flat:
        refl.append(group([path(bezier([(-86, -12), (-70, -20)], closed=False)),
                           path(bezier([(26, -12), (42, -20)], closed=False)),
                           stroke(WHITE, 6, 45)], name="reflection"))
    frame = [rect((282, 14), (0, -26), roundness=7)] + [rect((30, 10), (0, -16), roundness=5)]
    comp.layer("shades-art", refl + [
        group(lenses + st.paint(LENS, "secondary", (-110, -24, 110, 28), sil=False, lw=FLINE,
                                gloss=0.8), name="lenses"),
        group(frame + st.paint(LENS, "secondary", sil=False, lw=FLINE - 2), name="frame"),
    ] + ([group(lenses + frame + [fill(WHITE), stroke(WHITE, 2 * BORDER, slot="outline")],
                 name="diecut")] if st.flat else []) + st.shadow(lenses + frame, offset=(0, 7) if st.flat else (4, 6)), parent=shades)

    # smirk with a dimple
    comp.layer("mouth", [group(S("M -52 4 C -24 30 22 28 48 -8") + st.line(12), name="smirk"),
                         group(S("M 42 -14 C 50 -10 54 -4 54 2") + st.line(8), name="dimple")],
               parent=face, position=(6, 66),
               scale=sampled(lambda t: [100 + 6 * nod(t + 6), 100 + 10 * nod(t + 6)], 0, T))

    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-cool-sunglasses", "Emoji Cool Sunglasses",
       "Smirking face in dark shades that nods to the beat while a glint sweeps across the lenses. "
       "Seamless loop.",
       ["emoji", "cool", "sunglasses", "shades", "chill", "swag", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.63, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.63, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.63, "Cartoon line art with bold black outlines."),
       ])
