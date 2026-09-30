"""Broken heart: a heart pops in and beats, a crack zigzags down it and the halves split apart
with falling shards, then hang (intro-hold)."""

from _reactions2 import *

T = 60
W, H = 460, 440
CX, CY = 230, 214
SC = 2.35
RED = "#FF3B5C"
CRACK_AT, SPLIT = 26, 34

ZIG = [(0, -33), (-8, -19), (7, -6), (-6, 8), (6, 22), (0, 38)]
LEFT_D = ("M 0 38 C -30 20 -54 0 -54 -20 C -54 -39 -40 -51 -25 -51 C -13 -51 -4 -44 0 -33 " +
          " ".join(f"L {x} {y}" for x, y in ZIG[1:]) + " Z")
RIGHT_D = ("M 0 -33 C 4 -44 13 -51 25 -51 C 40 -51 54 -39 54 -20 C 54 0 30 20 0 38 " +
           " ".join(f"L {x} {y}" for x, y in ZIG[-2::-1]) + " Z")
CRACK_D = "M " + " L ".join(f"{x * SC} {y * SC}" for x, y in ZIG)


def pop(t):
    return spring(t / 10, 0.7, 3.4)


def beat(t):
    return 0.12 * bump(t, 12, 17) + 0.07 * bump(t, 17, 22)


def split(t):
    return back_out(clamp((t - SPLIT) / 12), 1.4)


def make(kind):
    st = Style(kind)
    comp = Comp("broken-heart-split", W, H, frames=T)
    comp.slot("primary", RED)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # shards falling out of the break
    r = rng(9)
    for i in range(6):
        x0, y0 = CX + r.uniform(-12, 12), CY + r.uniform(-40, 60)
        vx, sz = r.uniform(-3, 3), r.uniform(0.7, 1.1)

        def fn(u, x0=x0, y0=y0, vx=vx, sz=sz):
            k = u / 24
            return {"position": (x0 + vx * u, y0 + 0.35 * u * u), "rotation": 25 * u * (1 if vx > 0 else -1),
                    "scale": [100 * sz] * 2, "opacity": 100 * (1 - smooth((k - 0.5) / 0.5))}
        particle(comp, f"shard{i}", [group(S("M 0 -22 L 17 11 L -13 16 Z") +
                                           st.paint(RED, "primary", lw=4, sil=not st.flat))],
                 SPLIT + i, 24, T, fn, step=2, wrap=False)

    heart = comp.null("heart", position=(CX, CY),
                      scale=sampled(lambda t: [100 * pop(t) * (1 + beat(t))] * 2, 0, T))

    # crack drawn down the middle before it splits
    comp.layer("crack", [group(S(CRACK_D) + [trim(end=sampled(lambda t: 100 * ease_out((t - CRACK_AT) / 7), CRACK_AT, CRACK_AT + 7)),
                                              stroke(st.ink if not st.flat else "#6E0E24", 8)])],
               parent=heart, ip=CRACK_AT, op=SPLIT + 1)

    for side, d, box in ((-1, LEFT_D, (-54, -51, 0, 38)), (1, RIGHT_D, (0, -51, 54, 38))):
        shapes = S(d, SC)
        box = tuple(v * SC for v in box)
        top = []
        if st.glossy and side < 0:
            top.append(group([ellipse((60, 32)), fill(WHITE, 65)], position=(-80, -84), rotation=-45))
        elif st.outline and side < 0:
            top.append(group(S("M -110 -60 C -104 -90 -80 -110 -56 -108") + [stroke(WHITE, 10)]))
        full_box = (-54 * SC, -51 * SC, 54 * SC, 38 * SC)
        comp.layer(f"half{side}", top + st.body(shapes, RED, "primary", full_box, spec=False),
                   parent=heart, anchor=(0, 38 * SC), position=sampled(
                       lambda t, s=side: (s * 22 * split(t), 38 * SC + 20 * split(t)), 0, T),
                   rotation=sampled(lambda t, s=side: s * 11 * split(t), 0, T))
    return comp


build3("broken-heart-split", "Broken Heart Split",
       "Heart that pops in and beats, then cracks down the middle and splits apart with falling "
       "shards, and holds; for heartbreak and disappointment.",
       ["broken heart", "heartbreak", "sad", "breakup", "heart", "reaction"], make, [
           ("glossy", "Glossy", "intro-hold", 0.75, "Shaded glossy heart with highlights."),
           ("flat", "Flat Sticker", "intro-hold", 0.75, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "intro-hold", 0.75, "Cartoon line art with bold black outlines."),
       ])
