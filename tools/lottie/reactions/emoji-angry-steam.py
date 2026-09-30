"""Fuming face: flushes red, swells and blasts puffs of steam from both sides of the head, shaking
with rage (loop)."""

from _reactions2 import *

T = 60
PUFF = 30
W, H = 560, 460
R = 145
CX, CY = 280, 248
STEAM = "#F4F6FA"


def build_up(t):
    """Pressure: rises through each half-cycle, released at the puff."""
    u = (t % PUFF) / PUFF
    return smooth(u / 0.7) if u < 0.7 else 1 - smooth((u - 0.7) / 0.15)


def blast(t):
    u = t % PUFF
    return bump(u, 20, 30)


def shake(t):
    return math.sin(TAU * t / 5) * (0.4 + 0.6 * build_up(t))


def cloud_shapes(s=1.0):
    return [ellipse((52 * s, 46 * s), (-16 * s, 6 * s)), ellipse((60 * s, 56 * s), (10 * s, -6 * s)),
            ellipse((44 * s, 40 * s), (28 * s, 12 * s)), ellipse((40 * s, 36 * s), (-2 * s, 16 * s))]


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-angry-steam", W, H, frames=T)
    comp.slot("primary", st.face)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # steam puffs: two bursts per loop, three clouds per side each
    for burst in range(2):
        for side in (-1, 1):
            for j in range(3):
                t0 = burst * PUFF + 20 + j * 3
                life = 26
                ang = math.radians(-35 - j * 14)
                d = (side * math.cos(ang), math.sin(ang))
                base = (CX + side * (R - 6), CY - 34)

                def fn(u, d=d, base=base, j=j, side=side):
                    k = u / life
                    dist = 118 * ease_out(k, 2.4) + 10
                    s = 100 * (0.35 + 0.9 * ease_out(k, 2)) * (1 - 0.15 * j)
                    return {"position": (base[0] + d[0] * dist, base[1] + d[1] * dist - 20 * k),
                            "scale": (s, s), "rotation": side * 40 * k,
                            "opacity": 100 if k < 0.45 else 100 * (1 - (k - 0.45) / 0.55) ** 1.4}

                items = cloud_shapes()
                sh = [group(cloud_shapes() + [fill("#9AA4B8", 45)], position=(4, 6))] if st.glossy else []
                body = [group(items + st.paint(STEAM, under=True, sil=True))]
                particle(comp, f"steam{burst}{side}{j}", body + sh, t0 % T, life, T, fn, step=2)

    face = face_null(comp, T, R, CX, CY,
                     dpos=lambda t: (2.5 * shake(t), -10 * blast(t)),
                     drot=lambda t: 1.5 * shake(t),
                     dscale=lambda t: (100 + 6 * build_up(t) - 4 * blast(t),
                                       100 + 3 * build_up(t) + 6 * blast(t)))

    # angry V brows and narrowed eyes
    for side in (-1, 1):
        comp.layer(f"brow{side}", st.brow("M -30 -12 L 28 14", 14), parent=face,
                   scale=(side * -100, 100), position=(side * 56, -60))
        eye_d = "M -22 -6 L 22 6 C 22 22 12 30 0 30 C -14 30 -24 20 -22 -6 Z"
        comp.layer(f"eye{side}", [group(S(eye_d) + [fill(st.ink)])], parent=face,
                   scale=(side * -100, 100), position=(side * 52, -30))

    # clenched teeth
    teeth = [group([path(bezier([(x, 50), (x, 90)], closed=False)) for x in (-33, -11, 11, 33)] +
                   [path(bezier([(-54, 70), (54, 70)], closed=False)),
                    stroke(st.ink if st.outline else "#C9B8A6", 4 if st.outline else 3.5)], name="gaps"),
             group([rect((116, 44), (0, 70), roundness=18)] + st.paint(WHITE, lw=FLINE), name="teeth")]
    if not st.outline:
        teeth.append(group([rect((124, 52), (0, 70), roundness=22), fill(CAVITY)], name="lips"))
    comp.layer("mouth", teeth, parent=face,
               scale=sampled(lambda t: [100 + 6 * build_up(t), 100 - 8 * build_up(t)], 0, T),
               anchor=(0, 70), position=(0, 70))

    # red flush rising up the face as the pressure builds
    gr = R - (LINE / 2 if st.outline else 0)
    comp.layer("flush", [group([ellipse((2 * gr, 2 * gr)),
                                gradient_fill([(0, "#FF2A1F", 0.85), (0.6, "#FF2A1F", 0.55),
                                               (1, "#FF2A1F", 0.0)], (0, R), (0, -R))])],
               parent=face, opacity=sampled(lambda t: 55 + 45 * build_up(t), 0, T))
    comp.layer("face-base", st.face_disc(R), parent=face)
    return comp


build3("emoji-angry-steam", "Emoji Angry Steam",
       "Fuming face that flushes red, swells up and blasts puffs of steam from both sides of its "
       "head while shaking with rage. Seamless loop.",
       ["emoji", "angry", "mad", "rage", "furious", "steam", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.42, "Classic emoji with soft shading and highlights."),
           ("flat", "Flat Sticker", "loop", 0.42, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.42, "Cartoon line art with bold black outlines."),
       ])
