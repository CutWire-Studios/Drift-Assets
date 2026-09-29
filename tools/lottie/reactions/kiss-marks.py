"""Kiss marks: lipstick prints stamp on one after another with a squash and a little heart, then
fade to make room for the next round (loop)."""

from _reactions2 import *

T = 90
W, H = 460, 420
LIP = "#E8264F"

UPPER_D = ("M -62 0 C -44 -8 -32 -36 -15 -36 C -6 -36 -2 -30 0 -25 C 2 -30 6 -36 15 -36 "
           "C 32 -36 44 -8 62 0 C 34 -2 12 3 0 5 C -12 3 -34 -2 -62 0 Z")
LOWER_D = ("M -62 5 C -32 6 -12 10 0 10 C 12 10 32 6 62 5 C 46 32 24 44 0 44 "
           "C -24 44 -46 32 -62 5 Z")
# (x, y, rotation, scale, stamp frame)
PRINTS = [(150, 176, -18, 1.25, 4), (322, 220, 14, 1.05, 22), (200, 318, -6, 0.95, 40)]


def make(kind):
    st = Style(kind)
    comp = Comp("kiss-marks", W, H, frames=T)
    comp.slot("primary", LIP)
    comp.slot("accent", "#FF8FB1")
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    lips = S(UPPER_D) + S(LOWER_D)
    creases = group([path(bezier([(x, 18), (x * 0.9, 34)], closed=False)) for x in (-30, -12, 12, 30)] +
                    [path(bezier([(x, -6), (x * 0.9, -22)], closed=False)) for x in (-34, -18, 18, 34)] +
                    [stroke(st.ink if st.outline else "#9E0F32", 3.5, 100 if st.outline else 55)],
                    name="creases")
    for i, (x, y, r, s, t0) in enumerate(PRINTS):
        def sc(t, t0=t0, s=s):
            u = t - t0
            if u < 0:
                return [0, 0]
            if u < 3:
                k = 1.5 - 0.5 * u / 3
                return [100 * s * k, 100 * s * k]
            v = 100 * s * (1 + 0.14 * bump(u, 3, 9) * -1)
            return [v * (1 + 0.1 * bump(u, 3, 9)), v]

        fade = lambda t, t0=t0: 100 * clamp((t - t0) / 2) * (1 - smooth((t - 72) / 14))
        top = [creases]
        if st.glossy:
            top.append(group([ellipse((30, 10)), fill(WHITE, 55)], position=(-26, -20), rotation=-20))
            top.append(group([ellipse((34, 10)), fill(WHITE, 45)], position=(8, 28), rotation=-4))
        comp.layer(f"print{i}", top + st.body(lips, LIP, "primary", (-62, -36, 62, 44), spec=False),
                   position=(x, y), rotation=r, scale=sampled(sc, t0, t0 + 10),
                   opacity=sampled(fade, 0, T, 2), ip=t0, op=T)
        # a tiny heart popping off each print
        def hfn(u, x=x, y=y, i=i):
            k = u / 26
            sc_ = 100 * 0.32 * (back_out(clamp(u / 6)) if u < 6 else 1) * (1 - 0.3 * k)
            side = 1 if i % 2 == 0 else -1
            return {"position": (x + side * (60 + 18 * k), y - 50 - 60 * ease_out(k)),
                    "scale": (sc_, sc_), "rotation": side * 14,
                    "opacity": 100 * (1 - smooth((k - 0.5) / 0.5))}
        particle(comp, f"heart{i}", st.body(S(HEART_D), "#FF8FB1", "accent", (-54, -51, 54, 38),
                                            spec=False), t0 + 3, 26, T, hfn, step=2, wrap=False)
    return comp


build3("kiss-marks", "Kiss Marks",
       "Lipstick kiss prints that stamp on one after another with a squash and a little heart, then "
       "fade out for the next round. Seamless loop.",
       ["kiss", "lipstick", "love", "mwah", "lips", "flirty", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.62, "Shiny lip-gloss prints with highlights."),
           ("flat", "Flat Sticker", "loop", 0.62, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.62, "Cartoon line art with bold black outlines."),
       ])
