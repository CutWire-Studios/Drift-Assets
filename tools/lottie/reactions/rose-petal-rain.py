"""Rose petal rain: petals flutter, tumble and drift down in a soft romantic shower (loop)."""

from _reactions2 import *

T = 120
W, H = 460, 560
PETAL, PETAL2 = "#E8264F", "#FF7A9C"
PETAL_D = ("M 0 34 C -18 30 -30 12 -28 -8 C -26 -24 -16 -34 -8 -34 C -4 -30 -2 -26 0 -24 "
           "C 2 -26 4 -30 8 -34 C 16 -34 26 -24 28 -8 C 30 12 18 30 0 34 Z")


def make(kind):
    st = Style(kind)
    comp = Comp("rose-petal-rain", W, H, frames=T)
    comp.slot("primary", PETAL)
    comp.slot("secondary", PETAL2)
    if st.outline:
        comp.slot("outline", st.ink)

    def shapes(i):
        sid, col = ("primary", PETAL) if i % 3 else ("secondary", PETAL2)
        vein = group(S("M 0 28 C -2 14 -2 0 0 -16") + [stroke(st.ink if st.outline else "#7A0A26",
                                                               3 if st.outline else 2.5,
                                                               100 if st.outline else 35)], name="vein")
        top = [vein]
        if st.glossy:
            top.append(group([ellipse((12, 26)), fill(WHITE, 40)], position=(-12, -4), rotation=16))
            return top + [group(S(PETAL_D) + [
                gradient_fill([(0, "#FFFFFF", 0.35), (0.5, "#FFFFFF", 0), (1, "#5A0018", 0.35)],
                              (-10, -30), (14, 34)), fill(col, slot=sid)])]
        if st.flat:
            return top + [group(S(PETAL_D) + [fill(col, slot=sid)]),
                          group(S(PETAL_D) + [fill("#000000", 16)], position=(3, 5))]
        return top + [group(S(PETAL_D) + [stroke(st.ink, 5, slot="outline"), fill(col, slot=sid)])]

    rain(comp, "petal", 24, T, W, H, shapes, seed=44, life=(0.7, 1.0), size=(0.75, 1.3), sway=46,
         spin=260, flip=0.85, tumble=0.4, margin=50, fade=0.1)
    return comp


build3("rose-petal-rain", "Rose Petal Rain",
       "Rose petals fluttering, flipping and drifting down in a soft shower; for romance, "
       "anniversaries and weddings. Seamless loop.",
       ["rose", "petals", "romantic", "love", "wedding", "valentine", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.5, "Velvety shaded petals with soft highlights."),
           ("flat", "Flat", "loop", 0.5, "Flat two-tone petals with soft drop shadows."),
           ("outline", "Bold Outline", "loop", 0.5, "Cartoon petals with bold black outlines."),
       ])
