"""Cartoon mallet swings down and bonks, with an impact burst and dizzy stars."""

from _memes2 import *

W, H = 720, 640
F = 45
GRIP = (600, 596)
L = 300           # grip to head centre
HW = 250          # head length
HIT_R = -66       # rotation at impact
REST_R = HIT_R + 24
HIT = 13
_a = math.radians(HIT_R)
HIT_PT = (GRIP[0] + L * math.sin(_a), GRIP[1] - L * math.cos(_a))
# the head's lower striking face at impact: the bonked spot
TARGET = (HIT_PT[0] - HW / 2 * math.cos(_a), HIT_PT[1] - HW / 2 * math.sin(_a) + 6)

SWING = [(0, -2, EASE_OUT), (8, 7, EXPO_IN), (HIT, HIT_R, EASE_OUT), (19, REST_R + 6, EASE_IN_OUT),
         (25, REST_R - 3, EASE_IN_OUT), (31, REST_R)]


def swing_rig(comp, keys_list=SWING):
    return comp.null("swing", anchor=(0, 0), position=GRIP, rotation=keys(*keys_list),
                     scale=keys((0, [0, 0], SPRING), (6, [100, 100])))


def star_pts(r, n=5, inner=0.45, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180 / n)
        rr = r if i % 2 == 0 else r * inner
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def dizzy_stars(comp, shapes_fn, n=4, rx=140, ry=38, cy_off=-40, t0=HIT + 2, spin=1, spin_self=200):
    """Stars pop out of the impact and orbit in a flat ellipse above it, then hold."""
    cx, cy = TARGET[0], TARGET[1] + cy_off
    for i in range(n):
        a0 = TAU * i / n

        def fn(u, a0=a0):
            p = ease_out(u / 30, 3)
            a = a0 + spin * p * TAU * 0.75
            r = 0.3 + 0.7 * p
            return {"position": [cx + rx * r * math.cos(a), cy + ry * r * math.sin(a) - 40 * (1 - p)],
                    "scale": [100 * min(1, u / 6) * (0.8 + 0.2 * math.sin(a)),
                              100 * min(1, u / 6) * (0.8 + 0.2 * math.sin(a))],
                    "rotation": spin_self * p}
        particle(comp, f"star{i}", shapes_fn(i), t0, F - t0, F, fn, step=2, wrap=False)


def burst_lines(comp, slot, n=10, r0=70, r1=150, width=12, t0=HIT, color=None):
    lines = []
    for i in range(n):
        a = math.radians(-180 + i * 180 / (n - 1))
        lines.append(polyline([(math.cos(a) * r0, math.sin(a) * r0 * 0.8), (math.cos(a) * r1, math.sin(a) * r1 * 0.8)]))
    comp.layer("burst", [group(lines + [trim(start=keys((t0 + 3, 0, EASE_IN), (t0 + 12, 100)),
                                             end=keys((t0, 0, EXPO_OUT), (t0 + 6, 100))),
                                        stroke(color or "#FFFFFF", slot=slot, width=width)], "b")],
               position=(TARGET[0], TARGET[1] - 10), ip=t0, op=t0 + 13)


def cartoon():
    """Wooden mallet with a thick ink outline; burst lines and yellow dizzy stars."""
    comp = base("bonk-mallet", W, H, F)
    comp.slot("primary", "#C98A4B")
    comp.slot("secondary", "#8A5A2E")
    comp.slot("accent", "#FFD23F")
    comp.slot("outline", INK)
    dizzy_stars(comp, lambda i: [group([polyline(star_pts(36), closed=True), round_corners(5),
                                         fill(slot="accent"), stroke(slot="outline", width=6)], "s")])
    burst_lines(comp, "accent")
    sw = swing_rig(comp)
    hw, hh = HW, 132
    squash = keys((HIT - 1, [100, 100], EASE_OUT), (HIT, [114, 84], EASE_OUT), (HIT + 5, [96, 104], EASE_IN_OUT),
                  (HIT + 10, [100, 100]))
    head = [group([rect((hw * 0.5, 16), (-hw * 0.12, -hh * 0.3), 8), fill("#FFFFFF", 45)], "shine"),
            group([rect((26, hh - 10), (-hw / 2 + 34, 0)), rect((26, hh - 10), (hw / 2 - 34, 0)),
                   fill(slot="secondary")], "bands"),
            group([rect((hw, hh * 0.3), (0, hh * 0.28), 0), fill("#000000", 16)], "shade"),
            group([rect((hw, hh), (0, 0), 30), fill(slot="primary"), stroke(slot="outline", width=10)], "head")]
    comp.layer("head", head, parent=sw, position=(0, -L), scale=squash)
    comp.layer("handle", [group([rect((24, L - 40), (-4, -L / 2 - 20), 10), fill("#FFFFFF", 22)], "hi"),
                          group([rect((44, L + 20), (0, -L / 2 + 10), 22), fill(slot="secondary"),
                                 stroke(slot="outline", width=10)], "h")], parent=sw)
    comp.layer("smear", [group([path(arc(L, -90 + 7, -90 + HIT_R + 6, (0, 0))),
                                trim(start=keys((9, 0, EASE_IN), (HIT + 3, 100)), end=keys((8, 0, EASE_OUT), (HIT, 100))),
                                stroke("#FFFFFF", width=90, opacity=22)], "arc")],
               position=GRIP, ip=8, op=HIT + 4)
    return comp


def toy():
    """Red squeaky toy hammer with yellow bumpers: big squash and stretch, a pastel pop cloud and hearts."""
    comp = base("bonk-mallet--toy", W, H, F)
    comp.slot("primary", "#FF3B4E")
    comp.slot("secondary", "#FFD23F")
    comp.slot("accent", "#7FD4FF")
    heart = path(bezier([(0, 12), (-22, -6), (-11, -20), (0, -10), (11, -20), (22, -6)],
                        [(0, 0), (-4, 8), (-8, 0), (0, -8), (-6, 0), (0, -8)],
                        [(0, 0), (0, -8), (6, 0), (0, -8), (8, 0), (-4, 8)]), "heart")
    dizzy_stars(comp, lambda i: [group([heart, fill("#FF8FB8")], "h", scale=(170, 170))] if i % 2 else
                [group([polyline(star_pts(34, inner=0.5), closed=True), round_corners(7), fill(slot="accent")], "s")],
                n=5, rx=120, spin=-1)
    # soft pop cloud
    puff = [ellipse((d, d), (x, y)) for x, y, d in ((-60, 0, 90), (0, -24, 110), (60, 0, 90), (0, 18, 100))]
    comp.layer("pop", [group(puff + [fill("#FFFFFF", 80)], "c")], position=TARGET,
               scale=keys((HIT, [30, 30], EXPO_OUT), (HIT + 10, [130, 130])),
               opacity=keys((HIT, 100, EASE_IN), (HIT + 12, 0)), ip=HIT, op=HIT + 13)
    sw = swing_rig(comp)
    hw, hh = HW + 10, 140
    squash = keys((HIT - 1, [104, 96], EASE_OUT), (HIT, [128, 70], EASE_OUT), (HIT + 4, [90, 112], EASE_IN_OUT),
                  (HIT + 9, [104, 96], EASE_IN_OUT), (HIT + 14, [100, 100]))
    head = [group([ellipse((hw * 0.45, 26), (-hw * 0.05, -hh * 0.28)), fill("#FFFFFF", 55)], "shine"),
            group([rect((40, hh + 16), (-hw / 2 + 4, 0), 18), rect((40, hh + 16), (hw / 2 - 4, 0), 18),
                   fill(slot="secondary")], "bumpers"),
            group([rect((hw - 40, 18), (0, -hh * 0.18), 9), rect((hw - 40, 18), (0, hh * 0.18), 9),
                   fill("#000000", 12)], "ribs"),
            group([rect((hw - 30, hh), (0, 0), 50), fill(slot="primary")], "head")]
    comp.layer("head", head, parent=sw, position=(0, -L), scale=squash)
    comp.layer("handle", [group([rect((46, L), (0, -L / 2), 23), fill(slot="secondary")], "h"),
                          group([rect((60, 60), (0, -18), 20), fill(slot="primary")], "grip-cap")], parent=sw,
               scale=keys((HIT, [100, 100], EASE_OUT), (HIT + 3, [110, 92], EASE_IN_OUT), (HIT + 10, [100, 100])))
    return comp


def pixel():
    """Chunky pixel-art mallet swinging in stepped frames with blocky stars."""
    comp = base("bonk-mallet--pixel", W, H, F)
    comp.slot("primary", "#B0703A")
    comp.slot("secondary", "#6B4020")
    comp.slot("accent", "#FFE14D")
    comp.slot("outline", "#161616")
    P = 12
    star = ["   #   ", "   #   ", "  ###  ", "#######", "  ###  ", "   #   ", "   #   "]
    sparks = pixel_outline(star, lambda c: c == "#", P, (-3.5 * P, -3.5 * P))
    dizzy_stars(comp, lambda i: [group(sparks + [fill(slot="accent")], "s")], n=3, rx=130, ry=34, spin_self=0)
    # stepped swing: hold keys only
    steps = [(0, -2), (3, 3), (6, 7), (9, -14), (11, -40), (HIT, HIT_R), (17, REST_R + 8), (21, REST_R - 3),
             (25, REST_R)]
    sw = swing_rig(comp, [(t, r, HOLD) for t, r in steps] + [(F, REST_R)])
    comp.layers[-1]["ks"]["s"] = keys((0, [0, 0], HOLD), (2, [100, 100])).lottie()
    head = ["###################",
            "#ppppppppppppppppp#",
            "#s#ppppppppppppp#s#",
            "#s#ppppppppppppp#s#",
            "#s#ppppppppppppp#s#",
            "#s#ppppppppppppp#s#",
            "#s#ppppppppppppp#s#",
            "#ddddddddddddddddd#",
            "###################"]
    o = (-len(head[0]) * P / 2, -len(head) * P / 2)
    comp.layer("head", [group(pixel_outline(head, lambda c: c == "#", P, o) + [fill(slot="outline")], "ink"),
                        group(pixel_outline(head, lambda c: c == "p", P, o) + [fill(slot="primary")], "wood"),
                        group(pixel_outline(head, lambda c: c in "sd", P, o) + [fill(slot="secondary")], "bands")],
               parent=sw, position=(0, -L))
    n = int(L / P) - 3
    handle = ["#ss#"] * n
    comp.layer("handle", [group(pixel_outline(handle, lambda c: c == "#", P, (-2 * P, -n * P + 2 * P)) +
                                [fill(slot="outline")], "ink"),
                          group(pixel_outline(handle, lambda c: c == "s", P, (-2 * P, -n * P + 2 * P)) +
                                [fill(slot="secondary")], "wood")], parent=sw)
    # blocky impact sparks
    for i, (dx, dy) in enumerate(((-1, -1), (1, -1), (-1.4, 0), (1.4, 0))):
        comp.layer(f"spark{i}", [group([rect((P * 2, P * 2)), fill("#FFFFFF")], "s")],
                   position=keys((HIT, [TARGET[0] + dx * 40, TARGET[1] + dy * 40 - 10], HOLD),
                                 (HIT + 3, [TARGET[0] + dx * 80, TARGET[1] + dy * 80 - 10], HOLD),
                                 (HIT + 6, [TARGET[0] + dx * 110, TARGET[1] + dy * 110 - 10])),
                   ip=HIT, op=HIT + 8)
    return comp


build_asset(CAT, "bonk-mallet", "Bonk Mallet",
            "A cartoon mallet winds up, swings down and bonks, with an impact burst and dizzy stars circling "
            "the spot. Line the bottom-left of the swing up with the head you are bonking.",
            ["bonk", "mallet", "hammer", "hit", "cartoon", "meme", "dizzy"], [
    Variant("cartoon", "Wooden Mallet", cartoon(), "intro-hold", thumb_t=0.8,
            description="Wooden mallet with a thick ink outline, burst lines and yellow dizzy stars."),
    Variant("toy", "Squeaky Toy", toy(), "intro-hold", thumb_t=0.8,
            description="Red squeaky toy hammer with big squash and stretch, a pop cloud, stars and hearts."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=0.8,
            description="Chunky pixel-art mallet swinging in stepped frames with blocky stars."),
])
