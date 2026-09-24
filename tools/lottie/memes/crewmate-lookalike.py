"""Bean-shaped space crewmate (visor + backpack) waddling in place (loop)."""

import math

from _common import *

T = 30
W, H = 400, 460
RED, VISOR, INK = "#E03A3E", "#A8DDF0", "#1D1B24"
OUT = 10
GROUND = 408

comp = Comp("crewmate-lookalike", W, H, fps=30, frames=T)
comp.slot("primary", RED)
comp.slot("accent", VISOR)


def s1(t):
    return math.sin(2 * math.pi * t / T)


def bob(t):
    return -7 * math.cos(4 * math.pi * t / T)


BODY_D = ("M 106 314 C 104 270 106 216 108 176 C 110 104 150 64 202 64 C 256 64 294 104 296 176 "
          "C 298 216 300 270 298 314 C 297 334 284 344 264 344 L 140 344 C 120 344 107 334 106 314 Z")
VISOR_D = "M 226 118 L 284 118 C 305 118 322 135 322 156 C 322 177 305 194 284 194 L 226 194 C 205 194 188 177 188 156 C 188 135 205 118 226 118 Z"

body = comp.null("body", anchor=(202, GROUND), position=sampled(lambda t: (202, GROUND + bob(t)), 0, T),
                 rotation=sampled(lambda t: 3 * s1(t), 0, T),
                 scale=sampled(lambda t: (100 + 1.8 * math.cos(4 * math.pi * t / T),
                                          100 - 2.2 * math.cos(4 * math.pi * t / T)), 0, T))

comp.layer("visor", [
    group([rect((34, 12), (282, 138), roundness=6), fill("#FFFFFF", 95)], name="glint",
          rotation=0),
    group(svg_shapes("M 190 164 C 196 182 210 194 226 194 L 284 194 C 305 194 320 180 322 164 "
                     "C 300 176 214 178 190 164 Z") + [fill("#000000", 22)], name="shade"),
    group(svg_shapes(VISOR_D) + [stroke(INK, OUT), fill(VISOR, slot="accent")], name="visor"),
], parent=body)

comp.layer("body-matte", [group(svg_shapes(BODY_D) + [fill("#FFFFFF")])], parent=body)
comp.layer("body-shade", [
    group(svg_shapes("M 60 120 C 100 250 170 320 330 320 L 330 380 L 60 380 Z") + [fill("#000000", 22)],
          name="shade"),
    group([ellipse((34, 70), (138, 150)), fill("#FFFFFF", 22)], name="sheen", rotation=0),
], parent=body, matte="alpha")
comp.layer("body", [group(svg_shapes(BODY_D) + [stroke(INK, OUT), fill(RED, slot="primary")])],
           parent=body)

comp.layer("backpack", [
    group([rect((62, 150), (0, 0), roundness=22), stroke(INK, OUT), fill("#000000", 22),
           fill(RED, slot="primary")]),
], parent=body, anchor=(0, 60), position=(100, 312),
    rotation=sampled(lambda t: -2.5 * math.sin(2 * math.pi * t / T - 0.9), 0, T))


def leg(name, x, sign, dark):
    items = [rect((76, 100), (0, 35), roundness=24), stroke(INK, OUT)]
    if dark:
        items.append(fill("#000000", 22))
    items.append(fill(RED, slot="primary"))

    def lift(t):
        return (x, 318 - 12 * max(0.0, sign * math.cos(2 * math.pi * t / T)) ** 2 - bob(t) * 0.6)

    comp.layer(name, [group(items)], parent=body, anchor=(0, 0),
               position=sampled(lift, 0, T),
               rotation=sampled(lambda t: sign * 24 * s1(t), 0, T))


leg("leg-front", 246, 1, False)
leg("leg-back", 158, -1, True)

comp.layer("shadow", [ellipse((230, 26)), fill("#000000", 28)], position=(202, GROUND + 6),
           scale=sampled(lambda t: [100 + 4 * math.cos(4 * math.pi * t / T)] * 2, 0, T))

build(comp, "memes", "crewmate-lookalike", "Space Crewmate",
      "Bean-shaped space crewmate with a visor and backpack waddling in place. Seamless loop.",
      ["crewmate", "space", "impostor", "sus", "character", "meme", "walk"],
      "loop", 0.1)
