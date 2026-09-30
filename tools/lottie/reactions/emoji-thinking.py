"""Thinking face: hand on chin tapping, eyes drifting up in thought, one brow arching (loop)."""

from _reactions2 import *

T = 90
W, H = 460, 480
R = 150
CX, CY = 230, 218
HAND_EDGE = "#C27A00"


def tap(t):
    return sum(bump(t, a, a + 6) for a in (10, 17, 52, 59))


def arch(t):
    return smooth((t - 18) / 8) * (1 - smooth((t - 44) / 10)) + \
        0.6 * smooth((t - 62) / 6) * (1 - smooth((t - 78) / 8))


def glance(t):
    return (8 * math.sin(TAU * t / T) + 3, -6 - 3 * math.cos(TAU * t / T))


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-thinking", W, H, frames=T)
    comp.slot("primary", st.face)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (4 * wave(t, T), 3 * wave(t, T, 2)),
                     drot=lambda t: -7 + 3 * wave(t, T) - 1.2 * tap(t),
                     step=2)

    # hand under the chin: fist low-left, index finger lying along the chin, thumb tucked below
    fist = [rect((92, 76), (0, 0), roundness=32)]
    finger = [rect((100, 30), (0, 0), roundness=15)]
    thumb = [rect((66, 26), (0, 0), roundness=13)]
    knuckles = group([path(bezier([(-30, y), (-10, y + 2)], closed=False)) for y in (-10, 10)] +
                     [stroke(st.ink if st.outline else HAND_EDGE, 5 if st.outline else 4,
                             100 if st.outline else 60)], name="knuckles")
    hand_items = [
        group(finger + st.paint(st.face, "primary", (-50, -15, 50, 15), sil=True, edge=HAND_EDGE),
              position=(40, -34), rotation=-16, name="finger"),
        group(thumb + st.paint(st.face, "primary", (-33, -13, 33, 13), sil=True, edge=HAND_EDGE),
              position=(26, 2), rotation=-8, name="thumb"),
        knuckles,
        group(fist + st.paint(st.face, "primary", (-46, -38, 46, 38), sil=True, edge=HAND_EDGE),
              name="fist"),
    ]
    if st.glossy:
        hand_items.insert(0, group([ellipse((30, 12)), fill(WHITE, 50)], position=(-18, -24),
                                   rotation=-10, name="spec"))
    comp.layer("hand", hand_items, parent=face, anchor=(-10, 20), position=(-50, 176),
               rotation=sampled(lambda t: -4 * tap(t), 0, T))
    comp.layer("hand-shadow", [group([rect((96, 80), roundness=34), fill("#7A3A00", 22)])],
               parent=face, position=(-50, 150), opacity=0 if st.outline else 100)

    # eyes glancing up and to the side
    for side, (ex, ey) in ((-1, (-50, -26)), (1, (50, -34))):
        comp.layer(f"eye{side}", st.eye(30, 42), parent=face,
                   position=sampled(lambda t, ex=ex, ey=ey: (ex + glance(t)[0], ey + glance(t)[1]), 0, T, 2))
    comp.layer("brow-l", st.brow("M -28 10 C -18 -8 12 -12 28 -2", 11), parent=face,
               position=sampled(lambda t: (-54, -84 - 16 * arch(t)), 0, T, 2),
               rotation=sampled(lambda t: -6 * arch(t), 0, T, 2))
    comp.layer("brow-r", st.brow("M -26 -2 L 26 4", 11), parent=face, position=(56, -80), rotation=6)

    comp.layer("mouth", st.brow("M -34 4 C -14 8 12 2 34 -8", 11), parent=face, position=(14, 56),
               scale=sampled(lambda t: [100 - 12 * arch(t), 100], 0, T, 2))

    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-thinking", "Emoji Thinking",
       "Pondering face with a hand on its chin: it taps thoughtfully while its eyes drift up and one "
       "brow arches. Seamless loop; room above it for your question.",
       ["emoji", "thinking", "hmm", "pondering", "wonder", "question", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.25, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.25, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.25, "Cartoon line art with bold black outlines."),
       ])
