"""Cartoon skull: punchy pop, then rattles with a chattering jaw (loop)."""

import math

from _common import *
import _reactions2 as r2
from drift_lottie import Variant, build_asset

T = 60
W, H = 460, 460
BONE, DARK = "#F4F1E8", "#2A2233"


def pop(t):
    return 0.2 * math.sin(2 * math.pi * t / 11) * math.exp(-t / 7)


def head_scale(t):
    p = pop(t)
    return (100 * (1 + 0.75 * p), 100 * (1 + 1.25 * p))


def head_rot(t):
    return 3.5 * math.sin(2 * math.pi * t / 12) + 1.8 * math.sin(2 * math.pi * t / 4)


def head_pos(t):
    return (W / 2 + 4 * math.sin(2 * math.pi * t / 6), 238 - 5 * abs(math.sin(math.pi * t / 6)))


def jaw_open(t):
    return 0.5 - 0.5 * math.cos(2 * math.pi * t / 6)


TEETH_X = (-45, -15, 15, 45)
JAW_D = "M -74 112 L 74 112 C 78 146 56 170 0 172 C -56 170 -78 146 -74 112 Z"
CRANIUM_D = ("M -128 0 C -134 -92 -76 -150 0 -150 C 76 -150 134 -92 128 0 "
             "C 126 36 110 50 90 62 C 80 68 76 80 76 108 C 50 112 -50 112 -76 108 "
             "C -76 80 -80 68 -90 62 C -110 50 -126 36 -128 0 Z")
SOCKET_D = "M -44 -26 C -20 -40 30 -34 40 -4 C 48 22 26 42 0 42 C -30 42 -50 18 -50 -4 C -50 -14 -50 -22 -44 -26 Z"


def glossy():
    comp = Comp("emoji-skull", W, H, fps=30, frames=T)
    comp.slot("primary", BONE)
    comp.slot("secondary", DARK)

    head = comp.null("head", anchor=(0, 20), position=sampled(head_pos, 0, T),
                     rotation=sampled(head_rot, 0, T), scale=sampled(head_scale, 0, T))

    # rattle marks either side
    for side in (-1, 1):
        arcs = []
        for k, r in enumerate((26, 44)):
            arcs.append(group(svg_shapes(f"M 0 {-r} A {r} {r} 0 0 1 0 {r}") +
                              [stroke(BONE, 8, slot="primary")], name=f"arc{k}",
                              position=(k * 14, 0)))
        comp.layer(f"rattle{side}", arcs, parent=head, position=(side * 160, 10),
                   scale=(side * 100, 100),
                   opacity=sampled(lambda t: 100 * jaw_open(t) ** 2, 0, T))


    comp.layer("jaw", [
        group([path(bezier([(x, 118), (x, 136)], closed=False)) for x in TEETH_X] +
              [stroke(DARK, 6, slot="secondary")], name="teeth-gaps"),
        group(svg_shapes("M -76 142 C -60 166 60 166 76 142 C 76 156 56 170 0 172 C -56 170 -76 156 -76 142 Z")
              + [fill("#000000", 10)], name="shade"),
        group(svg_shapes(JAW_D) + [fill(BONE, slot="primary")], name="jaw"),
    ], parent=head, anchor=(0, 100), position=(0, 100),
        rotation=sampled(lambda t: 3 * jaw_open(t) * math.sin(2 * math.pi * t / 12), 0, T),
        scale=(100, 100))
    jaw_layer = comp.layers[-1]
    jaw_layer["ks"]["p"] = sampled(lambda t: (0, 100 + 22 * jaw_open(t)), 0, T).lottie()


    comp.layer("cranium", [
        group([path(bezier([(x, 86), (x, 106)], closed=False)) for x in TEETH_X] +
              [stroke(DARK, 6, slot="secondary")], name="teeth-gaps"),
        group(svg_shapes(SOCKET_D) + [fill(DARK, slot="secondary")], name="socket-l",
              position=(-54, -2)),
        group(svg_shapes(SOCKET_D) + [fill(DARK, slot="secondary")], name="socket-r",
              position=(54, -2), scale=(-100, 100)),
        group(svg_shapes("M 0 -18 C 7 -8 18 4 16 13 C 14 21 4 21 0 13 C -4 21 -14 21 -16 13 "
                         "C -18 4 -7 -8 0 -18 Z") + [fill(DARK, slot="secondary")], name="nose",
              position=(0, 60)),
        group(svg_shapes("M 44 -140 L 54 -116 L 40 -102 L 56 -84") + [stroke(DARK, 6, slot="secondary")],
              name="crack"),
        group([ellipse((70, 34)), fill("#FFFFFF", 60)], name="highlight", position=(-66, -108),
              rotation=-38),
        group(svg_shapes("M 60 -130 C 120 -100 140 -30 120 26 C 112 46 96 56 84 66 "
                         "C 70 50 100 -30 60 -130 Z") + [fill("#000000", 9)],
              name="shade"),
        group(svg_shapes(CRANIUM_D) + [fill(BONE, slot="primary")], name="cranium"),
    ], parent=head)

    comp.layer("mouth", [group([rect((136, 70), (0, 130), roundness=24), fill(DARK, slot="secondary")])],
               parent=head)
    return comp


def styled(kind):
    """Same rattling skull as a flat die-cut sticker or bold outline cartoon."""
    st = r2.Style(kind)
    ink = DARK if st.flat else st.ink
    comp = Comp(f"emoji-skull--{kind}", W, H, fps=30, frames=T)
    comp.slot("primary", BONE)
    comp.slot("secondary", ink)
    comp.slot("outline", r2.WHITE if st.flat else st.ink)
    head = comp.null("head", anchor=(0, 20), position=sampled(head_pos, 0, T),
                     rotation=sampled(head_rot, 0, T), scale=sampled(head_scale, 0, T))
    jaw_rot = sampled(lambda t: 3 * jaw_open(t) * math.sin(2 * math.pi * t / 12), 0, T)
    jaw_pos = sampled(lambda t: (0, 100 + 22 * jaw_open(t)), 0, T)

    for side in (-1, 1):
        arcs = []
        for k, r in enumerate((26, 44)):
            arcs.append(group(svg_shapes(f"M 0 {-r} A {r} {r} 0 0 1 0 {r}") + [stroke(BONE, 8, slot="primary")],
                              name=f"arc{k}", position=(k * 14, 0)))
        for k, r in enumerate((26, 44) if st.outline else ()):
            arcs.append(group(svg_shapes(f"M 0 {-r} A {r} {r} 0 0 1 0 {r}") + [stroke(st.ink, 16, slot="outline")],
                              name=f"arc{k}-edge", position=(k * 14, 0)))
        comp.layer(f"rattle{side}", arcs, parent=head, position=(side * 160, 10), scale=(side * 100, 100),
                   opacity=sampled(lambda t: 100 * jaw_open(t) ** 2, 0, T))

    bone = st.paint(BONE, "primary", lw=r2.LINE if st.outline else 0)
    comp.layer("jaw", [
        group([path(bezier([(x, 118), (x, 136)], closed=False)) for x in TEETH_X] + [stroke(ink, 6, slot="secondary")],
              name="teeth-gaps"),
        group(svg_shapes("M -76 142 C -60 166 60 166 76 142 C 76 156 56 170 0 172 C -56 170 -76 156 -76 142 Z")
              + [fill("#000000", 12)], name="shade"),
        group(svg_shapes(JAW_D) + bone, name="jaw"),
    ], parent=head, anchor=(0, 100), position=jaw_pos, rotation=jaw_rot)

    if st.flat:
        top = [group([ellipse((54, 24)), fill(r2.WHITE, 90)], name="highlight", position=(-70, -104), rotation=-38)]
    else:
        top = [group(svg_shapes(r2.arc_d(116, 212, 242, 0, 4)) + [stroke(r2.WHITE, 11)], name="highlight")]
    comp.layer("cranium", top + [
        group([path(bezier([(x, 86), (x, 106)], closed=False)) for x in TEETH_X] + [stroke(ink, 6, slot="secondary")],
              name="teeth-gaps"),
        group(svg_shapes(SOCKET_D) + [fill(ink, slot="secondary")], name="socket-l", position=(-54, -2)),
        group(svg_shapes(SOCKET_D) + [fill(ink, slot="secondary")], name="socket-r", position=(54, -2),
              scale=(-100, 100)),
        group(svg_shapes("M 0 -18 C 7 -8 18 4 16 13 C 14 21 4 21 0 13 C -4 21 -14 21 -16 13 "
                         "C -18 4 -7 -8 0 -18 Z") + [fill(ink, slot="secondary")], name="nose", position=(0, 60)),
        group(svg_shapes("M 44 -140 L 54 -116 L 40 -102 L 56 -84") + [stroke(ink, 6, slot="secondary")],
              name="crack"),
        group(svg_shapes("M 60 -130 C 120 -100 140 -30 120 26 C 112 46 96 56 84 66 "
                         "C 70 50 100 -30 60 -130 Z") + [fill("#000000", 12 if st.flat else 16)], name="shade"),
        group(svg_shapes(CRANIUM_D) + bone, name="cranium"),
    ], parent=head)
    comp.layer("mouth", [group([rect((136, 70), (0, 130), roundness=24), fill(ink, slot="secondary")])], parent=head)
    # die-cut border / hard shadow behind the whole skull (the jaw part follows the jaw)
    for name, shapes, tr in [("jaw-back", svg_shapes(JAW_D), dict(anchor=(0, 100), position=jaw_pos, rotation=jaw_rot)),
                             ("cranium-back", svg_shapes(CRANIUM_D) + [rect((136, 70), (0, 130), roundness=24)], {})]:
        items = []
        if st.flat:
            items.append(group(list(shapes) + [stroke(r2.WHITE, 2 * r2.BORDER, slot="outline"), fill(r2.WHITE)],
                               name="diecut"))
        items += st.shadow(shapes)
        comp.layer(name, items, parent=head, **tr)
    return comp


build_asset("reactions", "emoji-skull", "Emoji Skull",
            "Cartoon skull that pops with a squash and stretch, then rattles with a chattering jaw. "
            "Seamless loop.",
            ["emoji", "skull", "dead", "im dead", "funny", "reaction", "spooky"], [
    Variant("glossy", "Glossy", glossy(), "loop", thumb_t=0.25,
            description="Softly shaded bone-white skull with a highlight and cracked crown."),
    Variant("flat", "Flat Sticker", styled("flat"), "loop", thumb_t=0.25,
            description="Flat colours with a thick white die-cut border and a soft drop shadow."),
    Variant("outline", "Bold Outline", styled("outline"), "loop", thumb_t=0.25, bg="e8e8ee",
            description="Cartoon line art with bold black outlines and a hard offset shadow."),
])
