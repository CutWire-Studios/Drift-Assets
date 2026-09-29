"""Loudly crying face: sobs in shuddering hops with rivers of tears pouring down both cheeks and
droplets spilling off the chin (loop)."""

from _reactions2 import *

T = 60
BEAT = 15
W, H = 460, 500
R = 150
CX, CY = 230, 222


def sob(t):
    return abs(math.sin(math.pi * (t % BEAT) / BEAT)) ** 1.5


def stream(side, t):
    """Tear river from under the eye to past the chin, wobbling (fixed vertex count)."""
    pts_l, pts_r = [], []
    n = 7
    for i in range(n):
        k = i / (n - 1)
        x = side * (58 + 40 * k ** 1.2) + 3 * math.sin(TAU * (t / 20 - k * 1.5))
        y = -10 + (R + 24) * k
        w = 11 + 11 * k + 2 * math.sin(TAU * (t / 15 + k))
        pts_l.append((x - w, y))
        pts_r.append((x + w, y))
    x, y = (pts_l[-1][0] + pts_r[-1][0]) / 2, pts_l[-1][1]
    w = (pts_r[-1][0] - pts_l[-1][0]) / 2
    bulb = [(x + w * 0.75, y + w * 0.8), (x, y + w * 1.15), (x - w * 0.75, y + w * 0.8)]
    return smooth_closed([(side * 54, -22)] + pts_r[1:] + bulb + pts_l[:0:-1])


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-crying", W, H, frames=T)
    comp.slot("primary", st.face)
    comp.slot("accent", TEAR)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (4 * wave(t, T), -14 * sob(t)),
                     drot=lambda t: 3 * wave(t, T) + 1.5 * wave(t, BEAT / 2),
                     dscale=lambda t: (100 + 3 * sob(t), 100 - 3 * sob(t)))

    # droplets spilling off the bottom of the streams
    r = rng(5)
    for i in range(8):
        side = -1 if i % 2 else 1
        t0 = i * T / 8
        vx = side * r.uniform(1.2, 3.0)
        vy = r.uniform(-4, -1.5)
        s0 = r.uniform(0.55, 0.85)
        life = 18

        def fn(u, side=side, vx=vx, vy=vy, s0=s0):
            x = CX + side * 98 + vx * u
            y = CY + R + 60 + vy * u + 0.3 * u * u
            s = 100 * s0 * min(1, u / 5)
            return {"position": (x, y), "rotation": math.degrees(math.atan2(-vx, vy + 0.6 * u)),
                    "scale": (s, s), "opacity": 100 if u < life - 8 else 100 * (life - u) / 8}

        particle(comp, f"drop{i}", st.body(S(TEAR_D), TEAR, "accent", (-13, -24, 13, 17),
                                           shadow=False, spec=False) +
                 ([group([ellipse((6, 9)), fill(WHITE, 70)], position=(-4, 3))] if not st.outline else []),
                 round(t0, 2), life, T, fn, step=1)

    # rivers of tears
    for side in (-1, 1):
        shine = [group([path(bezier([(side * 48, 4), (side * 62, 70)], closed=False)),
                        stroke(WHITE, 5, 55)], name="shine")]
        comp.layer(f"stream{side}", shine + [
            group([morph(lambda t, s=side: stream(s, t), 0, T, 2)] +
                  st.paint(TEAR, "accent", (-120, -20, 120, 190), sil=True, gloss=0.6),
                  name="river")], parent=face)

    # squeezed-shut eyes and sad brows
    for side in (-1, 1):
        comp.layer(f"eye{side}", st.brow("M -30 8 C -18 -12 18 -12 30 8", 13), parent=face,
                   position=(side * 54, -30),
                   scale=sampled(lambda t: [100 + 6 * sob(t), 100 - 30 * sob(t)], 0, T))
        comp.layer(f"brow{side}", st.brow("M -24 8 C -12 -2 10 -6 26 -10", 10), parent=face,
                   rotation=side * -4, scale=(side * -100, 100),
                   position=sampled(lambda t, s=side: (s * 60, -84 - 8 * sob(t)), 0, T))

    wail_d = ("M -58 64 C -42 26 42 26 58 64 C 64 86 44 104 0 104 C -44 104 -64 86 -58 64 Z")
    add_mouth(comp, st, wail_d, face, tongue=((84, 40), (0, 100)),
              teeth="M -80 20 C -40 36 40 36 80 20 L 80 46 C 40 40 -40 40 -80 46 Z",
              anchor=(0, 40), position=(0, 40),
              scale=sampled(lambda t: [100 - 4 * sob(t), 88 + 18 * sob(t)], 0, T))

    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-crying", "Emoji Crying",
       "Loudly crying face that sobs in shuddering hops while rivers of tears pour down both cheeks "
       "and spill off the chin. Seamless loop.",
       ["emoji", "crying", "sob", "sad", "tears", "bawling", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.3, "Classic yellow emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.3, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.3, "Cartoon line art with bold black outlines."),
       ])
