"""Balloons: a bunch of party balloons floats up past the frame, swaying on their strings (loop)."""

from _reactions2 import *

T = 120
W, H = 440, 560
COLS = [("primary", "#FF4D6D"), ("secondary", "#4D9BFF"), ("accent", "#FFC93C"), (None, "#9B6BFF"),
        (None, "#2EC4B6")]
BAL_D = ("M 0 -76 C 42 -76 64 -42 64 -6 C 64 36 32 68 0 74 C -32 68 -64 36 -64 -6 "
         "C -64 -42 -42 -76 0 -76 Z")
KNOT_D = "M 0 70 L 10 86 L -10 86 Z"
STRING_D = "M 0 86 C 10 104 -10 124 0 144 C 8 160 -6 176 2 192"


def make(kind):
    st = Style(kind)
    comp = Comp("balloons-rise", W, H, frames=T)
    for sid, c in COLS:
        if sid:
            comp.slot(sid, c)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    def shapes(i):
        sid, col = COLS[(i * 3) % len(COLS)]
        top = []
        if st.glossy:
            top += [group([ellipse((24, 44)), fill(WHITE, 60)], position=(-30, -32), rotation=24),
                    group([ellipse((9, 9)), fill(WHITE, 70)], position=(-16, -60))]
        elif st.flat:
            top.append(group([ellipse((16, 30)), fill(WHITE, 70)], position=(-32, -28), rotation=24))
        else:
            top.append(group(S("M -44 -30 C -42 -46 -34 -58 -20 -64") + [stroke(WHITE, 8)]))
        bal = S(BAL_D) + S(KNOT_D)
        string = [group(S(STRING_D) + ([stroke("#F4F4F8", 3), stroke(st.ink, 8)] if st.outline else
                                       [stroke("#E6E6EE", 3.5)]))]
        return top + st.body(bal, col, sid, (-64, -76, 64, 80), spec=False, under=True) + string

    # each balloon pops up (inflates) low in the frame, rises with a sway and fades near the top,
    # so nothing is ever clipped by the canvas edge
    r = rng(12)
    lanes = [96, 330, 190, 260, 120, 350]
    n, life = 6, 96
    for i in range(n):
        x0, sz = lanes[i] + r.uniform(-10, 10), r.uniform(0.74, 0.95)
        amp, ph = r.uniform(10, 18) * r.choice((-1, 1)), r.uniform(0, 1)

        def fn(u, x0=x0, sz=sz, amp=amp, ph=ph):
            k = u / life
            y = (H - 190) - 330 * k - 40 * k * k
            pop = back_out(clamp(u / 12), 2.0)
            s = 100 * sz * pop
            return {"position": (x0 + amp * math.sin(TAU * (k * 1.2 + ph)), y),
                    "rotation": 0.5 * amp * math.cos(TAU * (k * 1.2 + ph)),
                    "scale": (s * (1 + 0.04 * math.sin(TAU * k * 3)), s),
                    "opacity": 100 * (1 - smooth((k - 0.8) / 0.2))}

        particle(comp, f"balloon{i}", shapes(i), round(i * T / n, 2), life, T, fn, step=2)
    return comp


build3("balloons-rise", "Balloons Rise",
       "Party balloons floating up past the frame, swaying on their strings; for birthdays and "
       "celebrations. Seamless loop.",
       ["balloons", "birthday", "party", "celebration", "float", "congrats", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.3, "Shiny latex balloons with highlights."),
           ("flat", "Flat Sticker", "loop", 0.3, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.3, "Cartoon line art with bold black outlines."),
       ])
