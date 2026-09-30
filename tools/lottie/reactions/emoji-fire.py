"""Fire: a three-tone flame that licks and flickers while embers float up (loop)."""

from _reactions2 import *

T = 60
W, H = 420, 480
BX, BY = 210, 438          # flame base centre
OUTER, MID, CORE = "#FF4E1F", "#FF9A1F", "#FFE14D"


def flame(t, w, h, ph=0.0, licks=True):
    """Closed flame outline; fixed vertex count so it can morph."""
    s1 = math.sin(TAU * (t / T * 2 + ph))
    s2 = math.sin(TAU * (t / T * 3 + ph + 0.3))
    s3 = math.sin(TAU * (t / T * 4 + ph + 0.6))
    tip = (w * (0.16 * s1 + 0.06 * s3), -h * (1 + 0.05 * s2))
    right = [(w * (0.30 + 0.05 * s2), -h * 0.72), (w * (0.62 + 0.04 * s3), -h * 0.46),
             (w * 0.86, -h * 0.22), (w * 0.72, -h * 0.02), (w * 0.34, h * 0.08)]
    left = [(-w * 0.34, h * 0.08), (-w * 0.74, -h * 0.02), (-w * 0.9, -h * 0.24),
            (-w * (0.66 - 0.04 * s1), -h * 0.5), (-w * (0.3 + 0.05 * s3), -h * 0.74)]
    pts = [tip] + right + left
    if licks:  # side tongues licking up
        rl = (w * (0.74 + 0.06 * s3), -h * (0.62 + 0.06 * s1))
        ll = (-w * (0.8 + 0.05 * s2), -h * (0.7 + 0.07 * s3))
        pts = [tip, (w * (0.34 + 0.04 * s2), -h * 0.6), rl, (w * 0.62, -h * 0.4)] + right[2:] + \
            left[:3] + [(-w * 0.64, -h * 0.46), ll, (-w * (0.34 + 0.04 * s1), -h * 0.66)]
    return smooth_closed(pts, 0.19)


def make(kind):
    st = Style(kind)
    comp = Comp("emoji-fire", W, H, frames=T)
    comp.slot("primary", OUTER)
    comp.slot("secondary", MID)
    comp.slot("accent", CORE)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # embers drifting up
    r = rng(8)
    for i in range(7):
        x0 = r.uniform(-80, 80)
        life = r.uniform(30, 40)
        sz = r.uniform(0.6, 1.1)
        ph = r.uniform(0, 1)

        def fn(u, x0=x0, sz=sz, ph=ph, life=life):
            k = u / life
            s = 100 * sz * (1 - k) * min(1, u / 4)
            return {"position": (BX + x0 + 16 * math.sin(TAU * (k + ph)), BY - 230 - 190 * k),
                    "scale": (s, s), "rotation": 45 + 120 * k, "opacity": 100}

        ember = [group([rect((13, 13), roundness=3)] + st.paint(CORE, "accent", lw=4), name="ember")]
        if st.glossy:
            ember.append(group([ellipse((34, 34)),
                                gradient_fill([(0, CORE, 0.6), (1, CORE, 0)], (0, 0), (17, 0), radial=True)]))
        particle(comp, f"ember{i}", ember, round(i * T / 7, 2), life, T, fn, step=2)

    flicker = comp.null("flicker", position=(BX, BY),
                        scale=sampled(lambda t: [100 + 3 * wave(t, T, 3), 100 - 3 * wave(t, T, 3)], 0, T, 2))
    box = (-150, -360, 150, 30)

    core = [morph(lambda t: flame(t, 58, 150, 0.5, licks=False), 0, T)]
    comp.layer("core", [group(core + st.paint(CORE, "accent", (-58, -150, 58, 12), lw=FLINE,
                                              gloss=0.5))], parent=flicker, position=(0, -14))
    mid = [morph(lambda t: flame(t, 102, 250, 0.25, licks=False), 0, T)]
    comp.layer("mid", [group(mid + st.paint(MID, "secondary", (-102, -250, 102, 20), lw=FLINE,
                                            gloss=0.6))], parent=flicker, position=(0, -6))
    outer = [morph(lambda t: flame(t, 150, 350), 0, T)]
    top = []
    if st.glossy:
        top.append(group([ellipse((30, 70)), fill(WHITE, 30)], position=(-70, -150), rotation=20))
    comp.layer("outer", top + [group(outer + st.paint(OUTER, "primary", box, sil=True, gloss=0.7))] +
               st.shadow(outer), parent=flicker)
    if st.glossy:
        comp.layer("glow", [group([ellipse((380, 300)),
                                   gradient_fill([(0, OUTER, 0.45), (1, OUTER, 0)], (0, 0), (190, 0),
                                                 radial=True)])],
                   position=(BX, BY - 150),
                   opacity=sampled(lambda t: 70 + 30 * wave(t, T, 4), 0, T, 2))
    return comp


build3("emoji-fire", "Emoji Fire",
       "Three-tone flame that licks and flickers while embers drift up; for anything that's lit. "
       "Seamless loop.",
       ["emoji", "fire", "flame", "lit", "hot", "trending", "reaction"], make, [
           ("glossy", "Glossy", "loop", 0.3, "Shaded flame with a warm glow and glowing embers."),
           ("flat", "Flat Sticker", "loop", 0.3, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "loop", 0.3, "Cartoon line art with bold black outlines."),
       ])
