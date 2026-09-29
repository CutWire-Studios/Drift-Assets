"""Shocked face: winds up, jolts back with pinprick pupils and a gasping mouth, shivers, then
relaxes (loop)."""

from _reactions2 import *

T = 60
W, H = 460, 460
R = 150
CX, CY = 230, 252


def shock(t):
    """0 calm -> 1 shocked (snappy rise with overshoot, hold, relax)."""
    if t < 11:
        return 0.0
    if t < 18:
        return back_out((t - 11) / 7, 2.4)
    if t < 42:
        return 1.0
    return 1 - smooth((t - 42) / 16)


def wind(t):
    return bump(t, 3, 12)


def jolt(t):
    return bump(t, 11, 24)


def shiver(t):
    return 2.4 * math.sin(TAU * t / 4) * (1.0 if 18 <= t < 44 else 0.0) * shock(t)


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-shocked", W, H, frames=T)
    comp.slot("primary", st.face)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (shiver(t) * 1.5, 5 * wind(t) - 30 * jolt(t)),
                     drot=lambda t: shiver(t) - 3 * jolt(t),
                     dscale=lambda t: (100 + 6 * wind(t) - 6 * jolt(t), 100 - 7 * wind(t) + 9 * jolt(t)))

    # surprise marks bursting off the top of the head
    marks = []
    for k, a in enumerate((-128, -90, -52)):
        p0, p1 = rot((R + 22, 0), a), rot((R + 62, 0), a)
        marks.append(group([path(bezier([p0, p1], closed=False)),
                            trim(end=sampled(lambda t: 100 * smooth((t - 13) / 5), 12, 20)),
                            stroke(WHITE, 10)] + ([stroke(st.ink, 20)] if st.outline else []),
                           name=f"mark{k}"))
    comp.layer("marks", marks, parent=face,
               opacity=sampled(lambda t: 100 * (1 if 13 <= t < 40 else 0) *
                               (1 - smooth((t - 32) / 8)), 0, T))

    for side in (-1, 1):
        eye = comp.null(f"eye{side}", parent=face, position=(side * 52, -30),
                        scale=sampled(lambda t: [100 + 10 * shock(t), 100 + 14 * shock(t)], 0, T))
        pw = 30
        comp.layer(f"pupil{side}", [
            group([ellipse((pw * 0.36, pw * 0.36)), fill(WHITE)], position=(-5, -6)),
            group([ellipse((pw, pw * 1.1)), fill(st.ink)])],
            parent=eye, position=(side * 3, 2),
            scale=sampled(lambda t: [100 - 45 * shock(t)] * 2, 0, T))
        comp.layer(f"white{side}", [group([ellipse((66, 80))] + st.paint(WHITE, lw=FLINE - 1))],
                   parent=eye)
        comp.layer(f"brow{side}", st.brow("M -26 6 C -14 -6 14 -6 26 6", 11), parent=face,
                   rotation=side * 10,
                   position=sampled(lambda t, s=side: (s * 56, -92 - 20 * shock(t)), 0, T))

    o_d = "M -30 0 A 30 38 0 1 0 30 0 A 30 38 0 1 0 -30 0 Z"
    add_mouth(comp, st, o_d, face, tongue=((40, 24), (0, 34)), position=(0, 72),
              scale=sampled(lambda t: [80 + 30 * shock(t), 60 + 60 * shock(t)], 0, T))

    # blue gloom washing down the forehead
    gr = R - (LINE / 2 if st.outline else 0)
    comp.layer("gloom", [group([ellipse((2 * gr, 2 * gr)),
                               gradient_fill([(0, "#2F66FF", 0.7), (0.55, "#2F66FF", 0.2),
                                              (1, "#2F66FF", 0)], (0, -R), (0, 10))])],
               parent=face, opacity=sampled(lambda t: 100 * clamp(shock(t)), 0, T))
    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-shocked", "Emoji Shocked",
       "Face that winds up and jolts back in shock, pupils shrinking to pinpricks, mouth gasping and "
       "a cold blue wash over the forehead, then relaxes. Seamless loop.",
       ["emoji", "shocked", "surprised", "omg", "gasp", "wow", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.45, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.45, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.45, "Cartoon line art with bold black outlines."),
       ])
