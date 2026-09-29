"""Clapping hands: two hands swing together four times a loop, squashing on each clap with a burst
of impact lines (loop)."""

from _reactions2 import *

T = 60
BEAT = 15
W, H = 460, 460
PIV = 214                     # both wrists pivot near the bottom centre
HAND_EDGE = "#C27A00"


def phase(t):
    return (t % BEAT) / BEAT


def openness(t):
    """0 at the clap, 1 fully open; fast snap into the clap, eased opening."""
    u = phase(t)
    return math.sin(math.pi * u) ** 0.7


def hit(t):
    u = t % BEAT
    return bump(u, -0.01, 5) + bump(u, BEAT - 2, BEAT + 0.01) * 0.3


def hand_shapes():
    palm = [rect((118, 132), (0, -92), roundness=50)]
    fingers = []
    for x, h, lean in ((-40, 72, -8), (-14, 88, -3), (14, 84, 3), (40, 66, 8)):
        fingers += capsule((x, -130), (x + lean, -140 - h), 14)
    thumb = capsule((-46, -76), (-94, -124), 16)
    return palm + fingers + thumb


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-clap", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("accent", "#FFB020")
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # impact lines on each clap
    for c in range(4):
        t0 = c * BEAT
        lines = []
        for k, a in enumerate((-150, -120, -90, -60, -30)):
            p0, p1 = rot((150, 0), a), rot((200, 0), a)
            lines.append(group([path(bezier([p0, p1], closed=False)),
                                trim(start=anim([(t0, 0, EASE_IN), (t0 + 9, 100)]),
                                     end=anim([(t0, 10, SNAP_OUT), (t0 + 5, 100)])),
                                stroke("#FFB020", 11, slot="accent")] +
                               ([stroke(st.ink, 20)] if st.outline else []), name=f"line{k}"))
        comp.layer(f"burst{c}", lines, position=(W / 2, 262), ip=t0, op=t0 + 10)

    shapes = hand_shapes()
    lines = group([path(bezier([(x, -130), (x, -158)], closed=False)) for x in (-27, 0, 27)] +
                  [stroke(st.ink if st.outline else HAND_EDGE, 5 if st.outline else 4,
                          100 if st.outline else 70)], name="finger-lines")

    def hand(side):
        items = [lines]
        if st.glossy:
            items.append(group([ellipse((50, 20)), fill(WHITE, 45)], position=(-20, -110), rotation=-60))
        items.append(group(shapes + st.paint(st.face, "primary", (-110, -230, 60, -26), sil=True,
                                             under=True, edge=HAND_EDGE), name="hand"))
        if side > 0:
            items += st.shadow(shapes, offset=(10, 8) if st.flat else (8, 8))
        return items

    squash = lambda t: [100 + 5 * hit(t), 100 - 6 * hit(t)]
    # back hand (left, thumb outwards) then front hand (right) drawn on top
    comp.layer("hand-front", hand(1), anchor=(0, -40), position=(PIV + 34, 390),
               scale=sampled(lambda t: [-squash(t)[0], squash(t)[1]], 0, T),
               rotation=sampled(lambda t: -6 - 26 * openness(t), 0, T))
    comp.layer("hand-back", hand(-1) + ([group(hand_shapes() + [fill("#000000", 22)],
                                                position=(6, 8))] if not st.glossy else []),
               anchor=(0, -40), position=(PIV - 18, 390),
               scale=sampled(lambda t: squash(t), 0, T),
               rotation=sampled(lambda t: 10 + 24 * openness(t), 0, T))
    return comp


build3("emoji-clap", "Emoji Clap",
       "Two hands clapping four times a loop, squashing on every clap with a burst of impact lines; "
       "applause for anything. Seamless loop.",
       ["emoji", "clap", "applause", "bravo", "congrats", "hands", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.03, "Classic yellow hands with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.03, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.03, "Cartoon line art with bold black outlines."),
       ])
