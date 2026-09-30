"""Heart-eyes face: sways dreamily while the heart eyes beat and little hearts drift up (loop)."""

from _reactions2 import *

T = 60
W, H = 460, 460
R = 150
CX, CY = 230, 250


def beat(t):
    """Lub-dub heartbeat, twice per loop."""
    u = t % 30
    return 0.22 * bump(u, 0, 7) + 0.14 * bump(u, 7, 14)


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-heart-eyes", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("accent", RED)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # small hearts floating up behind/around the head
    for i, (x0, delay, s, side) in enumerate([(-150, 0, 0.42, -1), (160, 20, 0.36, 1),
                                              (-120, 40, 0.3, 1)]):
        life = 44

        def fn(u, x0=x0, s=s, side=side):
            k = u / life
            sc = 100 * s * (back_out(min(1, u / 8)) if u < 8 else 1) * (1 - 0.3 * k)
            return {"position": (CX + x0 + side * 14 * math.sin(TAU * k), CY - 40 - 150 * k),
                    "rotation": side * 12 * math.cos(TAU * k),
                    "scale": (sc, sc), "opacity": 100 if k < 0.65 else 100 * (1 - k) / 0.35}

        particle(comp, f"float{i}", st.body(S(HEART_D), RED, "accent", (-54, -51, 54, 38)), delay,
                 life, T, fn, step=2)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (8 * wave(t, T), -6 * abs(wave(t, T, 2))),
                     drot=lambda t: 7 * wave(t, T),
                     dscale=lambda t: (100 + 2 * wave(t, T, 2, 0.25), 100 - 2 * wave(t, T, 2, 0.25)))

    # heart eyes
    for side in (-1, 1):
        heart = st.body(S(HEART_D), RED, "accent", (-54, -51, 54, 38), shadow=False)
        comp.layer(f"eye{side}", heart, parent=face, position=(side * 58, -32),
                   rotation=side * -8,
                   scale=sampled(lambda t: [100 * 0.76 * (1 + beat(t))] * 2, 0, T))

    comp.layer("cheeks", [group(blush(), position=(-96, 34)), group(blush(), position=(96, 34))],
               parent=face, opacity=70 if st.glossy else 55)

    # grin: wide D mouth with a teeth band
    mouth_d = "M -76 34 C -30 46 30 46 76 34 C 70 84 38 108 0 108 C -38 108 -70 84 -76 34 Z"
    teeth_d = "M -84 20 C -30 40 30 40 84 20 L 84 58 C 30 70 -30 70 -84 58 Z"
    add_mouth(comp, st, mouth_d, face, tongue=((70, 44), (0, 104)), teeth=teeth_d,
              anchor=(0, 40), position=(0, 40),
               scale=sampled(lambda t: [100, 94 + 8 * abs(wave(t, T, 2))], 0, T))

    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-heart-eyes", "Emoji Heart Eyes",
       "Smiling face with beating heart eyes that sways dreamily while little hearts drift up. "
       "Seamless loop; place your text above or beside it.",
       ["emoji", "heart eyes", "love", "crush", "in love", "reaction", "cute"], make, [
           ("glossy", "Glossy", "loop", 0.2, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.2, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.2, "Cartoon line art with bold black outlines."),
       ])
