"""Facepalm: the hand winds up, smacks onto the face, drags down while the head shakes in
disbelief, then lifts for the next one (loop)."""

from _reactions2 import *

T = 90
W, H = 480, 480
R = 150
CX, CY = 236, 244
SLEEVE = "#4C7DFF"
HAND_EDGE = "#C27A00"

LIFT = (96, -74, -4)   # (x, y, rotation) of the hand wound up
ON = (-4, -52, -30)      # on the face


def hand_state(t):
    """Blend 0 = lifted, 1 = on the face."""
    if t < 8:
        return 0.0
    if t < 13:
        return ease_in((t - 8) / 5, 2)
    if t < 70:
        return 1.0
    if t < 86:
        return 1 - smooth((t - 70) / 16)
    return 0.0


def impact(t):
    return bump(t, 12, 24)


def drag(t):
    return 18 * smooth((t - 14) / 50) * (1 - smooth((t - 70) / 12))


def shake(t):
    env = smooth((t - 22) / 8) * (1 - smooth((t - 60) / 10))
    return 7 * math.sin(TAU * (t - 22) / 24) * env


def hand_shapes():
    """Open palm, fingers up, thumb out to the left: one union silhouette."""
    palm = [rect((116, 112), (0, 6), roundness=48)]
    fingers = []
    for x, h, lean in ((-40, 76, -6), (-13, 92, -2), (15, 88, 2), (42, 70, 6)):
        fingers += capsule((x, -20), (x + lean, -30 - h), 14)
    thumb = capsule((-40, 30), (-86, -14), 16)
    return palm + fingers + thumb


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-facepalm", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("secondary", SLEEVE)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (0.6 * shake(t), 8 * impact(t)),
                     drot=shake,
                     dscale=lambda t: (100 + 5 * impact(t), 100 - 6 * impact(t)))

    # smack lines at the moment of impact
    lines = []
    for k, a in enumerate((-70, -40, -10)):
        p0, p1 = rot((96, 0), a), rot((140, 0), a)
        lines.append(group([path(bezier([p0, p1], closed=False)),
                            trim(start=sampled(lambda t: 100 * smooth((t - 16) / 7), 12, 24),
                                 end=sampled(lambda t: 100 * ease_out((t - 12) / 5), 12, 24)),
                            stroke(WHITE, 9)] + ([stroke(st.ink, 18)] if st.outline else []),
                           name=f"line{k}"))
    comp.layer("smack", lines, parent=face, position=(40, -60), ip=11, op=26)

    def hp(t):
        b = hand_state(t)
        return (LIFT[0] + (ON[0] - LIFT[0]) * b, LIFT[1] + (ON[1] - LIFT[1]) * b + drag(t) * b)

    fingers_sep = group([path(bezier([(x, -30), (x, -64)], closed=False)) for x in (-27, 1, 28)] +
                        [stroke(st.ink if st.outline else HAND_EDGE, 5 if st.outline else 4,
                                100 if st.outline else 70)], name="finger-lines")
    items = [fingers_sep]
    if st.glossy:
        items.append(group([ellipse((46, 18)), fill(WHITE, 45)], position=(-18, -8), rotation=-20))
    items += [
        group(hand_shapes() + st.paint(st.face, "primary", (-100, -124, 60, 62), sil=True,
                                       under=True, edge=HAND_EDGE), name="hand"),
        group([rect((96, 60), (0, 84), roundness=14)] +
              st.paint(SLEEVE, "secondary", (-48, 54, 48, 114), sil=True), name="sleeve"),
    ]
    if st.glossy:  # soft contact shadow on the face
        items.append(group(hand_shapes() + [fill("#8A4A00", 28)], position=(8, 10), name="shadow"))
    comp.layer("hand", items, parent=face,
               position=sampled(hp, 0, T),
               rotation=sampled(lambda t: LIFT[2] + (ON[2] - LIFT[2]) * hand_state(t), 0, T),
               scale=sampled(lambda t: [100 + 4 * (1 - hand_state(t)) - 4 * impact(t)] * 2, 0, T))

    # tired eyes, frown
    for side in (-1, 1):
        comp.layer(f"eye{side}", st.brow("M -24 0 C -10 8 10 8 24 0", 11), parent=face,
                   position=(side * 54, -24))
    comp.layer("mouth", st.brow("M -40 10 C -20 -8 20 -8 40 10", 12), parent=face,
               position=(4, 76), scale=sampled(lambda t: [100, 100 + 40 * hand_state(t)], 0, T))

    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-facepalm", "Emoji Facepalm",
       "Face that winds up and smacks a hand onto its forehead, drags it down while shaking its head "
       "in disbelief, then does it again. Seamless loop.",
       ["emoji", "facepalm", "smh", "cringe", "disbelief", "fail", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.3, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.3, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.3, "Cartoon line art with bold black outlines."),
       ])
