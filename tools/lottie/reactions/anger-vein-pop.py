"""Anger vein: the manga anger mark pops on and throbs with rising pressure (loop)."""

from _reactions2 import *

T = 60
W, H = 400, 400
C = 200
VEIN = "#FF2E3F"
ARC_D = "M 26 -80 C 28 -42 40 -28 80 -26"   # one quadrant bracket, bowing toward the centre


def throb(t):
    u = t % 30
    return bump(u, 0, 6) + 0.55 * bump(u, 6, 13)


def make(kind):
    st = Style(kind)
    comp = Comp("anger-vein-pop", W, H, frames=T)
    comp.slot("primary", VEIN)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    wid = 30
    root = comp.null("vein", position=(C, C),
                     rotation=sampled(lambda t: 6 * wave(t, T) + 3 * throb(t), 0, T),
                     scale=sampled(lambda t: [100 + 16 * throb(t)] * 2, 0, T))
    for q in range(4):
        items = []
        if st.glossy:
            items.append(group(S("M 34 -70 C 36 -50 44 -40 58 -36") + [stroke(WHITE, 7, 70)], name="shine"))
            items.append(group(S(ARC_D) + [stroke("#A8001A", wid, 45)], position=(3, 4), name="shade"))
        items.append(group(S(ARC_D) + [stroke(VEIN, wid, slot="primary")], name="vein"))
        if st.flat:
            items.append(group(S(ARC_D) + [stroke(WHITE, wid + 2 * BORDER, slot="outline")], name="diecut"))
            items.append(group(S(ARC_D) + [stroke("#000000", wid + 2 * BORDER, 22)], position=(0, 8)))
        elif st.outline:
            items.append(group(S(ARC_D) + [stroke(st.ink, wid + 2 * LINE, slot="outline")], name="ink"))
            items.append(group(S(ARC_D) + [stroke(st.ink, wid + 2 * LINE)], position=(5, 7)))
        # each bracket also breathes outward on the throb
        comp.layer(f"q{q}", items, parent=root, rotation=q * 90,
                   position=sampled(lambda t, q=q: rot((8 * throb(t), -8 * throb(t)), q * 90), 0, T))

    return comp


build3("anger-vein-pop", "Anger Vein Pop",
       "Manga anger mark that throbs with rising pressure; stick it on a head or next to your text "
       "for irritation and rage. Seamless loop.",
       ["anger", "angry", "vein", "manga", "anime", "mad", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.05, "Shaded glossy mark with highlights."),
           ("flat", "Flat Sticker", "loop", 0.05, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.05, "Cartoon line art with bold black outlines."),
       ])
