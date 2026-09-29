"""Thumbs down: the fist drops in from above, slams down with a squash, puffs of dust and
impact lines, then settles and holds (intro-hold)."""

from _reactions2 import *

T = 45
W, H = 400, 440
X, Y = 206, 214          # resting fist centre
HIT = 10
HAND_EDGE = "#C27A00"
DUST = "#E9E3F5"


def fall(t):
    """Vertical offset: drop, hit, small rebound, settle."""
    if t < HIT:
        return -300 * (1 - ease_in(t / HIT, 2.2))
    return -26 * bump(t, HIT + 1, HIT + 11) - 6 * bump(t, HIT + 11, HIT + 18)


def squash(t):
    return bump(t, HIT - 1, HIT + 6) - 0.4 * bump(t, HIT + 6, HIT + 14)


def hand_shapes():
    fist = [rect((136, 128), (0, 0), roundness=50)]
    curls = []
    for y in (-42, -14, 14, 42):
        curls += capsule((10, y), (74 - abs(y) * 0.15, y), 15)
    thumb = capsule((-40, 30), (-44, 128), 27)
    wrist = [rect((96, 60), (4, -78), roundness=20)]
    return fist + curls + thumb + wrist


SLEEVE_D = [rect((112, 46), (4, -112), roundness=12)]


def make(kind):
    st = Style(kind)
    comp = Comp("thumbs-down-drop", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("accent", "#FF4D4D")
    comp.slot("secondary", "#4C7DFF")
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    tip = (X - 44, Y + 155)
    # impact lines fanning out below
    lines = []
    for k, a in enumerate((200, 230, 310, 340)):
        p0, p1 = rot((50, 0), a), rot((96, 0), a)
        p0, p1 = (p0[0], -p0[1] * 0.6), (p1[0], -p1[1] * 0.6)
        lines.append(group([path(bezier([p0, p1], closed=False)),
                            trim(start=anim([(HIT, 0, EASE_IN), (HIT + 12, 100)]),
                                 end=anim([(HIT, 0, SNAP_OUT), (HIT + 6, 100)])),
                            stroke("#FF4D4D", 10, slot="accent")] +
                           ([stroke(st.ink, 19)] if st.outline else []), name=f"line{k}"))
    comp.layer("impact", lines, position=tip, ip=HIT, op=HIT + 13)

    # dust puffs rolling out to both sides
    for i, (dx, s0) in enumerate(((-1, 1.0), (1, 1.0), (-1, 0.7), (1, 0.7))):
        def fn(u, dx=dx, s0=s0, i=i):
            k = u / 22
            s = 100 * s0 * (0.4 + 0.8 * ease_out(k)) * (1 - 0.3 * k)
            return {"position": (tip[0] + dx * (30 + 70 * ease_out(k) * (1.3 if i > 1 else 1)),
                                 tip[1] + 12 - 18 * k - (12 if i > 1 else 0)),
                    "scale": (s, s), "opacity": 100 * (1 - smooth((k - 0.4) / 0.6))}
        particle(comp, f"dust{i}", [group([ellipse((46, 34)), ellipse((34, 28), (18, -8)),
                                           ellipse((30, 24), (-16, -4))] +
                                          st.paint(DUST, under=True, sil=True))],
                 HIT, 22, T, fn, step=2, wrap=False)

    shapes = hand_shapes()
    lines_ = group([path(bezier([(20, y), (62, y)], closed=False)) for y in (-28, 0, 28)] +
                   [stroke(st.ink if st.outline else HAND_EDGE, 5 if st.outline else 4,
                           100 if st.outline else 70)], name="curl-lines")
    top = [lines_]
    if st.glossy:
        top.append(group([ellipse((60, 22)), fill(WHITE, 45)], position=(-26, -30), rotation=-30))
    # anchor at the thumb tip so the squash plants on the ground
    sleeve = [group(SLEEVE_D + st.paint("#4C7DFF", "secondary", (-52, -135, 60, -89), sil=True))]
    comp.layer("hand", top + sleeve + st.body(shapes, st.face, "primary", (-70, -108, 90, 155),
                                              under=True, edge=HAND_EDGE, spec=False),
               anchor=(-44, 155), position=sampled(lambda t: (tip[0], tip[1] + fall(t)), 0, T),
               rotation=sampled(lambda t: 8 * (1 - ease_out(t / HIT)) if t < HIT else
                                -4 * bump(t, HIT, HIT + 12) + 2 * bump(t, HIT + 12, HIT + 22), 0, T),
               scale=sampled(lambda t: [100 + 14 * squash(t), 100 - 16 * squash(t)], 0, T))
    return comp


build3("thumbs-down-drop", "Thumbs Down Drop",
       "Thumbs-down fist that drops in from above and slams down with a squash, dust puffs and "
       "impact lines, then holds; for dislikes, fails and hard nos.",
       ["thumbs down", "dislike", "no", "fail", "boo", "reaction"], make, [
           ("glossy", "Glossy", "intro-hold", 0.95, "Classic yellow hand with soft shading and highlights."),
           ("flat", "Flat Sticker", "intro-hold", 0.95, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "intro-hold", 0.95, "Cartoon line art with bold black outlines."),
       ])
