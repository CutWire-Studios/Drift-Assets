"""Nervous sweat drop: a big anime sweat drop beads up, trembles and slides down, with small
droplets flicking off (loop)."""

from _reactions2 import *

T = 60
W, H = 320, 420
DROP = "#7CCBFF"
X0, Y0 = 160, 104
BIG_D = "M 0 -80 C 10 -54 50 -10 50 26 A 50 50 0 0 1 -50 26 C -50 -10 -10 -54 0 -80 Z"


def slide(t):
    """0 beading at the top -> 1 slid down; resets through a fade."""
    return smooth((t - 14) / 34) ** 1.3


def appear(t):
    return back_out(clamp(t / 10), 2.2) * (1 - smooth((t - 50) / 10))


def make(kind):
    st = Style(kind)
    comp = Comp("sweat-drop-nervous", W, H, frames=T)
    comp.slot("primary", DROP)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # small droplets flicking off to the side
    for i, (t0, dx, sz) in enumerate(((20, 1, 0.34), (30, -1, 0.26), (40, 1, 0.22))):
        def fn(u, dx=dx, sz=sz, t0=t0):
            k = u / 18
            y = Y0 + 110 * slide(t0)
            return {"position": (X0 + dx * (56 + 50 * ease_out(k)), y - 30 - 40 * k + 110 * k * k),
                    "rotation": dx * 30, "scale": [100 * sz * (1 - 0.4 * k)] * 2,
                    "opacity": 100 * (1 - smooth((k - 0.5) / 0.5))}
        particle(comp, f"drip{i}", st.body(S(BIG_D), DROP, "primary", (-50, -80, 50, 76), spec=False),
                 t0, 18, T, fn, step=2, wrap=False)

    top = []
    if st.glossy:
        top.append(group([ellipse((22, 44)), fill(WHITE, 80)], position=(-22, 12), rotation=18))
        top.append(group([ellipse((10, 10)), fill(WHITE, 80)], position=(-8, -18)))
    elif st.flat:
        top.append(group([ellipse((16, 34)), fill(WHITE, 85)], position=(-22, 14), rotation=18))
    else:
        top.append(group(S("M -30 10 C -32 26 -26 40 -14 48") + [stroke(WHITE, 8)]))
    comp.layer("drop", top + st.body(S(BIG_D), DROP, "primary", (-50, -80, 50, 76), spec=False),
               position=sampled(lambda t: (X0 + 3 * math.sin(TAU * t / 5) * (1 - slide(t)) * (t > 8),
                                           Y0 + 110 * slide(t)), 0, T),
               scale=sampled(lambda t: [100 * appear(t) * (1 - 0.1 * bump(slide(t), 0.05, 0.6)),
                                        100 * appear(t) * (1 + 0.16 * bump(slide(t), 0.05, 0.6))], 0, T),
               anchor=(0, -80), rotation=sampled(lambda t: -4 + 3 * math.sin(TAU * t / 7), 0, T))
    return comp


build3("sweat-drop-nervous", "Sweat Drop Nervous",
       "Big anime sweat drop that beads up, trembles and slides down with droplets flicking off; "
       "place it by a face for nervous, awkward moments. Seamless loop.",
       ["sweat", "nervous", "awkward", "anime", "drop", "yikes", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.3, "Glassy drop with bright highlights."),
           ("flat", "Flat Sticker", "loop", 0.3, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.3, "Cartoon line art with bold black outlines."),
       ])
