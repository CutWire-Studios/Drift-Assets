"""Cartoon skull: punchy pop, then rattles with a chattering jaw (loop)."""

import math

from _common import *

T = 60
W, H = 460, 460
BONE, DARK = "#F4F1E8", "#2A2233"

comp = Comp("emoji-skull", W, H, fps=30, frames=T)
comp.slot("primary", BONE)
comp.slot("secondary", DARK)


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

TEETH_X = (-45, -15, 15, 45)

JAW_D = "M -74 112 L 74 112 C 78 146 56 170 0 172 C -56 170 -78 146 -74 112 Z"
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

CRANIUM_D = ("M -128 0 C -134 -92 -76 -150 0 -150 C 76 -150 134 -92 128 0 "
             "C 126 36 110 50 90 62 C 80 68 76 80 76 108 C 50 112 -50 112 -76 108 "
             "C -76 80 -80 68 -90 62 C -110 50 -126 36 -128 0 Z")
SOCKET_D = "M -44 -26 C -20 -40 30 -34 40 -4 C 48 22 26 42 0 42 C -30 42 -50 18 -50 -4 C -50 -14 -50 -22 -44 -26 Z"

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

build(comp, "reactions", "emoji-skull", "Emoji Skull",
      "Cartoon skull that pops with a squash and stretch, then rattles with a chattering jaw. "
      "Seamless loop.",
      ["emoji", "skull", "dead", "im dead", "funny", "reaction", "spooky"],
      "loop", 0.25)
