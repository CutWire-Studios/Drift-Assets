"""Star pop: a big star springs in with a spin, a shockwave ring and a spray of mini stars and
sparkles, then settles and holds (intro-hold)."""

from _reactions2 import *

T = 45
W, H = 440, 440
CX, CY = 220, 224
GOLD, RING, MINI = "#FFC93C", "#FFE58A", "#FF7AB6"
STAR_D = star_d(118, 0.5)


def make(kind):
    st = Style(kind)
    comp = Comp("star-pop-burst", W, H, frames=T)
    comp.slot("primary", GOLD)
    comp.slot("secondary", RING)
    comp.slot("accent", MINI)
    if not st.glossy:
        comp.slot("outline", WHITE if st.flat else st.ink)

    # mini stars and sparkles flying out
    r = rng(4)
    for i in range(10):
        a = math.radians(i * 36 + r.uniform(-10, 10))
        dist = r.uniform(150, 195)
        sz = r.uniform(0.7, 1.1)
        t0 = 3 + r.uniform(0, 2)
        spark = i % 2 == 1

        def fn(u, a=a, dist=dist, sz=sz):
            k = u / 26
            d = 60 + (dist - 60) * ease_out(k, 3)
            s = 100 * sz * (back_out(clamp(u / 6)) if u < 6 else 1 - smooth((k - 0.5) / 0.5))
            return {"position": (CX + math.cos(a) * d, CY + math.sin(a) * d),
                    "rotation": 140 * k, "scale": (s, s)}
        shp = S(sparkle_d(18)) if spark else S(star_d(17, 0.5))
        col, sid = (RING, "secondary") if spark else (MINI, "accent")
        particle(comp, f"mini{i}", [group(shp + st.paint(col, sid, (-17, -17, 17, 17), sil=not st.flat, lw=4,
                                                         gloss=0.6))],
                 t0, 26, T, fn, step=2, wrap=False)

    # shockwave ring
    comp.layer("ring", [group([ellipse((300, 300)),
                               stroke(RING, 1, slot="secondary")], name="ring")] +
               ([group([ellipse((300, 300)), stroke(st.ink, 1)])] if st.outline else []),
               position=(CX, CY), ip=2, op=24,
               scale=anim([(2, [20, 20], SNAP_OUT), (22, [120, 120])]))
    ring = comp.layers[-1]
    ring["shapes"][0]["it"][1]["w"] = anim([(2, 26, EASE_OUT), (22, 0)]).lottie()
    if st.outline:
        ring["shapes"][1]["it"][1]["w"] = anim([(2, 38, EASE_OUT), (22, 0)]).lottie()

    star = S(STAR_D)
    top = []
    if st.glossy:
        top.append(group(S(star_d(70, 0.5)) + [fill(WHITE, 22)], position=(-10, -14), name="inner"))
    elif st.flat:
        top.append(group(S(star_d(64, 0.5)) + [fill("#FFFFFF", 25)], position=(0, 4), name="inner"))
    else:
        top.append(group(S("M -60 -30 L -30 -34") + [stroke(WHITE, 9)], name="shine"))
    comp.layer("star", top + st.body(star, GOLD, "primary", (-118, -118, 118, 100), spec=False,
                                     shade=[path(bezier([(0, 0), (112, -36), (56, 18), (69, 95)]))]),
               position=(CX, CY + 8),
               scale=sampled(lambda t: [100 * spring(t / 10, 0.75, 3.2)] * 2, 0, T),
               rotation=sampled(lambda t: -60 * (1 - spring(t / 10, 0.6, 3.5)), 0, T))
    return comp


build3("star-pop-burst", "Star Pop Burst",
       "Big star that springs in with a spin, a shockwave ring and a spray of mini stars and "
       "sparkles, then holds; for wins, favourites and top picks.",
       ["star", "pop", "burst", "favorite", "win", "award", "reaction"], make, [
           ("glossy", "Glossy", "intro-hold", 0.4, "Shaded golden star with soft highlights."),
           ("flat", "Flat Sticker", "intro-hold", 0.4, "Flat colours with a thick white die-cut border."),
           ("outline", "Bold Outline", "intro-hold", 0.4, "Cartoon line art with bold black outlines."),
       ])
