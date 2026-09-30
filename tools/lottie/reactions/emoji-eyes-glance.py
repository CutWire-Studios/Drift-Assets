"""Eyes: a pair of big eyeballs dart left, right and back with a hop, then blink (loop)."""

from _reactions2 import *

T = 90
W, H = 460, 340
EW, EH = 150, 196
PUPIL = "#1B1B24"

# pupil gaze keys: (frame, x, y); darts snap with overshoot
GAZE = [(0, 0, 6), (10, 0, 6), (15, -40, 4), (36, -40, 4), (41, 40, 2), (62, 40, 2), (68, 0, 6),
        (90, 0, 6)]
BLINK = 76


def gaze(t):
    for (t0, x0, y0), (t1, x1, y1) in zip(GAZE, GAZE[1:]):
        if t0 <= t <= t1:
            if x0 == x1 and y0 == y1:
                return x0, y0
            u = (t - t0) / (t1 - t0)
            k = back_out(u, 2.2)
            return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return GAZE[-1][1:]


def dart(t):
    return sum(bump(t, a, a + 8) for a in (10, 36, 62))


def blink(t):
    return bump(t, BLINK, BLINK + 7) ** 0.6


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-eyes-glance", W, H, frames=T)
    comp.slot("primary", WHITE if not st.outline else "#FFFFFF")
    comp.slot("secondary", PUPIL)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    pair = comp.null("pair", position=sampled(lambda t: (W / 2 + 0.15 * gaze(t)[0], 176 - 10 * dart(t)), 0, T),
                     rotation=sampled(lambda t: 0.08 * gaze(t)[0] * (1 - blink(t)), 0, T))
    for side in (-1, 1):
        eye = comp.null(f"eye{side}", parent=pair, position=(side * 84, 0), anchor=(0, EH / 2),
                        scale=sampled(lambda t: [100 + 4 * dart(t), 100 - 5 * dart(t) - 88 * blink(t)], 0, T))
        eye_d = f"M 0 {-EH / 2} A {EW / 2} {EH / 2} 0 1 1 0 {EH / 2} A {EW / 2} {EH / 2} 0 1 1 0 {-EH / 2} Z"
        comp.layer(f"pupil{side}", [
            group([ellipse((20, 22)), fill(WHITE)], position=(-14, -18)),
            group([ellipse((9, 9)), fill(WHITE, 80)], position=(12, 14)),
            group([ellipse((70, 84)), fill(PUPIL, slot="secondary")]),
        ], parent=eye, position=sampled(lambda t, s=side: (gaze(t)[0] + s * 2, EH / 2 + gaze(t)[1]), 0, T))
        comp.layer(f"ball{side}", [group(S(eye_d) + st.paint(WHITE, "primary", (-EW / 2, -EH / 2, EW / 2, EH / 2),
                                                             sil=True, gloss=0.55))] +
                   ([group(S(eye_d) + [fill("#B9C3D6", 60)], position=(8, 10), name="shade")]
                    if st.glossy else []) + st.shadow(S(eye_d)),
                   parent=eye, position=(0, EH / 2))
    return comp


build3("emoji-eyes-glance", "Emoji Eyes Glance",
       "A pair of big cartoon eyes that dart left, right and back with a little hop, then blink; "
       "for side-eye and 'look at this' moments. Seamless loop.",
       ["emoji", "eyes", "side eye", "looking", "glance", "watching", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.25, "Shaded glassy eyeballs with bright highlights."),
           ("flat", "Flat Sticker", "loop", 0.25, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.25, "Cartoon line art with bold black outlines."),
       ])
