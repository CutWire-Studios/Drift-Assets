"""Cluster of four-point sparkles twinkling on staggered beats (loop)."""

import math

from _common import *
import _reactions2 as r2
from drift_lottie import Variant, build_asset

T = 60
W, H = 400, 400
GOLD = "#FFF1B8"


def sparkle_d(r, pinch=0.16):
    """Four-point star with concave sides; tips on the axes."""
    tips = [(0, -r), (r, 0), (0, r), (-r, 0)]
    d = f"M 0 {-r} "
    for a, b in zip(tips, tips[1:] + tips[:1]):
        c1 = (a[0] * 0.25 + b[0] * pinch, a[1] * 0.25 + b[1] * pinch)
        c2 = (b[0] * 0.25 + a[0] * pinch, b[1] * 0.25 + a[1] * pinch)
        d += f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {b[0]} {b[1]} "
    return d + "Z"


def sparkle(r):
    return [
        group(svg_shapes(sparkle_d(r * 0.42)) + [fill("#FFFFFF", 85)], name="core"),
        group(svg_shapes(sparkle_d(r)) + [fill(GOLD, slot="primary")], name="star"),
        group([ellipse((r * 1.5, r * 1.5)),
               gradient_fill([(0, "#FFFFFF", 0.3), (0.45, "#FFFFFF", 0.1), (1, "#FFFFFF", 0)],
                             (0, 0), (r * 0.75, 0), radial=True)], name="glow"),
    ]


def glossy(sparkle=sparkle, name="sparkles-twinkle", slots=None):
    comp = Comp(name, W, H, fps=30, frames=T)
    comp.slot("primary", GOLD)
    for sid, col in (slots or {}).items():
        comp.slot(sid, col)

    # (x, y, radius, period, phase, min_scale)
    STARS = [
        (178, 214, 110, 60, 0.00, 0.72),
        (300, 108, 52, 30, 0.35, 0.0),
        (92, 96, 38, 60, 0.55, 0.0),
        (318, 290, 40, 60, 0.15, 0.0),
        (80, 320, 28, 30, 0.8, 0.0),
        (228, 58, 24, 60, 0.75, 0.0),
        (340, 196, 20, 30, 0.1, 0.0),
    ]

    for i, (x, y, r, per, ph, lo) in enumerate(STARS):
        def sc(t, per=per, ph=ph, lo=lo):
            c = (t / per + ph) % 1
            if lo:
                v = lo + (1 - lo) * (0.5 - 0.5 * math.cos(2 * math.pi * c)) ** 1.5
            else:
                v = max(0.0, math.sin(2 * math.pi * c)) ** 1.6
            return [100 * v, 100 * v]

        def rot(t, per=per, ph=ph, lo=lo):
            if lo:
                return 8 * math.sin(2 * math.pi * t / T)
            return 90 * ((t / per + ph) % 1) - 45

        # rotation keys restart each cycle; the star is four-fold symmetric so the wrap is invisible
        keys = []
        for t in range(0, T + 1, 2):
            keys.append((t, sc(t)))
        rkeys = []
        if lo:
            rkeys = sampled(rot, 0, T, 2)
        else:
            for c in range(-1, T // per + 1):
                t0 = (c - ph) * per
                rkeys += [(t0, -45, LINEAR), (t0 + per - 0.01, 45, HOLD)]
            rkeys = anim(rkeys)
        comp.layer(f"sparkle{i}", sparkle(r), position=(x, y),
                   scale=anim([(t, v, LINEAR) for t, v in keys]), rotation=rkeys)

    for i, (x, y, per, ph) in enumerate([(130, 150, 30, 0.6), (262, 256, 30, 0.2), (250, 150, 60, 0.4),
                                        (140, 360, 60, 0.9)]):
        comp.layer(f"dot{i}", [ellipse((12, 12)), fill(GOLD, slot="primary")], position=(x, y),
                   scale=sampled(lambda t, per=per, ph=ph: [100 * max(0.0, math.sin(
                       2 * math.pi * ((t / per + ph) % 1))) ** 1.2] * 2, 0, T, 2))
    return comp


def styled(kind):
    """Same twinkle, drawn as flat die-cut stickers or bold outlined cartoon sparkles."""
    st = r2.Style(kind)
    gold = "#FFD84A"

    def sticker(r):
        top = []
        if st.flat:
            top.append(group(svg_shapes(sparkle_d(r * 0.34)) + [fill("#FFFFFF", 70)], name="core"))
        else:
            top.append(group(svg_shapes(f"M {-r * 0.08} {-r * 0.62} L {-r * 0.05} {-r * 0.3}") +
                             [stroke("#FFFFFF", max(3, r * 0.08))], name="shine"))
        lw = max(4, min(r2.LINE, r * 0.14))
        body = [group(svg_shapes(sparkle_d(r)) + st.paint(gold, "primary", lw=lw if st.outline else None,
                                                             sil=True), name="star")]
        if st.flat:
            body[0]["it"][-2] = stroke("#FFFFFF", max(8, r * 0.2), slot="outline", name="diecut")
            body.append(group(svg_shapes(sparkle_d(r)) + [fill("#000000", 22), stroke("#000000", max(8, r * 0.2), 22)],
                              name="shadow", position=(0, max(3, r * 0.08))))
        else:
            off = max(3, r * 0.07)
            body.append(group(svg_shapes(sparkle_d(r)) + [fill(st.ink), stroke(st.ink, lw)], name="shadow",
                              position=(off * 0.8, off)))
        return top + body

    comp = glossy(sticker, f"sparkles-twinkle--{kind}", {"outline": r2.WHITE if st.flat else st.ink})
    comp.slots["primary"] = {"p": {"a": 0, "k": hex_color(gold)}}
    for L in comp.layers:
        if L["nm"].startswith("dot"):
            L["shapes"] = [ellipse((14, 14)), fill(gold, slot="primary"),
                           stroke(r2.WHITE if st.flat else st.ink, 5, slot="outline")]
    return comp


build_asset("reactions", "sparkles-twinkle", "Sparkles Twinkle",
            "Cluster of four-point sparkles that twinkle with a scale and twist on staggered beats. "
            "Seamless loop.",
            ["sparkle", "sparkles", "twinkle", "stars", "shine", "magic", "reaction"], [
    Variant("glossy", "Glowing", glossy(), "loop", thumb_t=0.47,
            description="Soft cream sparkles with white-hot cores and a faint glow."),
    Variant("flat", "Flat Sticker", styled("flat"), "loop", thumb_t=0.47,
            description="Golden sparkles as flat die-cut stickers with white borders and soft shadows."),
    Variant("outline", "Bold Outline", styled("outline"), "loop", thumb_t=0.47, bg="e8e8ee",
            description="Cartoon sparkles with bold black outlines and hard offset shadows."),
])
