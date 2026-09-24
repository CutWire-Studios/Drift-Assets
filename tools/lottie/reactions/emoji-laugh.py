"""Crying-laughing face: hops on every "ha", shakes, and flings tears from both eyes (loop)."""

import math

from _common import *

T, BEAT = 45, 15
W, H = 600, 500
R = 150
CX, CY = 300, 262
FACE, TEAR = "#FFC83D", "#4FC3F7"
DARK = "#5B3312"
MOUTH = "#6E2412"

comp = Comp("emoji-laugh", W, H, fps=30, frames=T)
comp.slot("primary", FACE)
comp.slot("accent", TEAR)


def phase(t):
    return (t % BEAT) / BEAT


def hop(t):
    return abs(math.sin(math.pi * phase(t)))


def face_pos(t):
    x = CX + 5 * math.sin(2 * math.pi * t / T)
    return (x, CY + R - 26 * hop(t))


def face_rot(t):
    return 6 * math.sin(2 * math.pi * t / T) + 2.5 * math.sin(2 * math.pi * t / (BEAT / 2))


def face_scale(t):
    c = math.cos(2 * math.pi * phase(t))
    sq = 0.07 * max(c, 0) ** 3 - 0.035 * max(-c, 0)
    return (100 * (1 + sq), 100 * (1 - sq))


def to_world(t, p):
    sx, sy = face_scale(t)
    x, y = p[0] * sx / 100, (p[1] - R) * sy / 100
    a = math.radians(face_rot(t))
    px, py = face_pos(t)
    return (px + x * math.cos(a) - y * math.sin(a), py + x * math.sin(a) + y * math.cos(a))


def drop_rot(dx, dy):
    return math.degrees(math.atan2(-dx, dy))


TEAR_D = "M 0 -24 C 4 -14 13 -6 13 4 A 13 13 0 0 1 -13 4 C -13 -6 -4 -14 0 -24 Z"


def teardrop(scale=1.0):
    return [
        group([ellipse((7 * scale, 11 * scale), (-5 * scale, 2 * scale)), fill("#FFFFFF", 70)],
              name="shine", rotation=20),
        group(svg_shapes(TEAR_D, scale) + [fill(TEAR, slot="accent")], name="drop"),
    ]


face = comp.null("face", anchor=(0, R),
                 position=sampled(face_pos, 0, T), rotation=sampled(face_rot, 0, T),
                 scale=sampled(face_scale, 0, T))

# flying tears, alternating eyes
CORNER = (112, -22)
n = 9
for i in range(n):
    t0 = i * T / n
    side = -1 if i % 2 == 0 else 1
    start = to_world(t0, (side * CORNER[0], CORNER[1]))
    vx = side * (7.5 + 2.5 * ((i * 7) % 5) / 4)
    vy = -7.5 - 1.5 * ((i * 3) % 4) / 3
    g = 0.85
    life = 21

    def fn(u, start=start, vx=vx, vy=vy):
        x, y = start[0] + vx * u, start[1] + vy * u + 0.5 * g * u * u
        s = min(1, 0.35 + u / 4) * (1 - 0.35 * u / life) * 100
        return {"position": (x, y), "rotation": drop_rot(vx, vy + g * u),
                "scale": (s, s), "opacity": 100 if u < life - 6 else 100 * (life - u) / 6}

    particle(comp, f"tear{i}", teardrop(1.2), round(t0, 2), life, T, fn, step=1)

# tear pools hanging at the eye corners, swelling with each laugh
for side in (-1, 1):
    swell = sampled(lambda t: [100 + 18 * hop(t + 3)] * 2, 0, T)
    comp.layer(f"pool{side}", teardrop(1.45), parent=face,
               position=(side * 112, -4), rotation=drop_rot(side * 0.75, 0.66),
               scale=swell)

# eyes: squeezed-shut arcs
EYE_D = "M -34 6 C -24 -26 24 -26 34 6"
for side in (-1, 1):
    squeeze = sampled(lambda t: [100 + 6 * hop(t), 100 - 22 * hop(t)], 0, T)
    comp.layer(f"eye{side}", [group(svg_shapes(EYE_D) + [stroke(DARK, 17)], rotation=side * 12)],
               parent=face, position=(side * 56, -38), scale=squeeze)
    comp.layer(f"brow{side}",
               [group(svg_shapes("M -26 4 C -14 -8 14 -8 26 4") + [stroke(DARK, 10)],
                      rotation=side * 16)],
               parent=face, position=sampled(lambda t, s=side: (s * 60, -86 - 8 * hop(t)), 0, T))

# mouth: wide open grin with teeth and tongue, opening on each "ha"
MOUTH_D = "M -98 14 C -40 30 40 30 98 14 C 96 78 52 120 0 120 C -52 120 -96 78 -98 14 Z"
mouth = comp.null("mouth", parent=face, position=(0, 12), anchor=(0, 14),
                  scale=sampled(lambda t: [100 + 4 * hop(t), 86 + 18 * hop(t)], 0, T))
comp.layer("mouth-matte", [group(svg_shapes(MOUTH_D) + [fill("#FFFFFF")])], parent=mouth)
comp.layer("mouth-inside", [
    group(svg_shapes("M -110 0 L 110 0 L 110 34 C 40 52 -40 52 -110 34 Z") + [fill("#FFFFFF")],
          name="teeth"),
    group([ellipse((130, 90), (0, 128)), fill("#F2677A")], name="tongue"),
    group(svg_shapes(MOUTH_D) + [fill(MOUTH)], name="cavity"),
], parent=mouth, matte="alpha")

comp.layer("face-base", [
    group([ellipse((62, 30)), fill("#FFFFFF", 45)], position=(-92, -84), rotation=-48,
          name="highlight"),
    group(svg_shapes(f"M {-R} 0 A {R} {R} 0 0 0 {R} 0 A 162 162 0 0 1 {-R} 0 Z") +
          [fill("#B35C00", 22)], name="shade"),
    group([ellipse((2 * R, 2 * R)), fill(FACE, slot="primary")], name="face"),
], parent=face)

build(comp, "reactions", "emoji-laugh", "Emoji Laugh",
      "Crying-laughing face that hops and shakes on every laugh while tears fly from both eyes. "
      "Seamless loop.",
      ["emoji", "laugh", "lol", "crying laughing", "funny", "reaction", "tears"],
      "loop", 0.2)
