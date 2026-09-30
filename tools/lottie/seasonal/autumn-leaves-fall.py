"""Autumn leaves fall: maple, oak and elm leaves tumbling down over the frame (seamless loop)."""

from _common import *

W, H = 1920, 1080
T = 120
RED, ORANGE, GOLD = "#D63A26", "#F07A1C", "#F2B43A"
COLORS = [("primary", RED), ("secondary", ORANGE), ("accent", GOLD)]
REGION = (610, 190, 700, 700)


def maple_pts(L=50):
    """Five pointed lobes with small side teeth; short stem notch at the bottom. ~100 px at L=50."""
    lobes = [(-195, L * 0.6), (-140, L * 0.92), (-90, L), (-40, L * 0.92), (15, L * 0.6)]
    pts = [rot((L * 0.3, 0), 150)]
    prev = None
    for a, l in lobes:
        if prev is not None:
            pts.append(rot((L * 0.4, 0), (prev + a) / 2))
        pts += [rot((l * 0.6, 0), a - 17), rot((l * 0.74, 0), a - 13), rot((l * 0.66, 0), a - 6), rot((l, 0), a),
                rot((l * 0.66, 0), a + 6), rot((l * 0.74, 0), a + 13), rot((l * 0.6, 0), a + 17)]
        prev = a
    pts += [rot((L * 0.3, 0), 30), (0, L * 0.16)]
    return pts


def oak_pts(n=36):
    pts = []
    for i in range(n):
        t = TAU * i / n
        base_w, base_h = 24, 48
        lobe = 1 + 0.2 * math.cos(7 * t) if 0.12 < (i / n) < 0.88 or True else 1
        x = base_w * math.sin(t) * lobe * (0.8 + 0.3 * (1 - math.cos(t)) / 2)
        y = -base_h * math.cos(t) * (1 if math.cos(t) > 0 else 0.92)
        pts.append((x, y))
    return pts


STEM_D = "M 0 40 C 1 50 3 58 7 66"


def elm_pts(n=24):
    pts = []
    for i in range(n):
        t = TAU * i / n
        x = 27 * math.sin(t) * (0.75 + 0.25 * math.cos(t)) ** 0.6 if math.cos(t) > -1 else 0
        y = -48 * math.cos(t) + 4 * math.sin(t) ** 2
        pts.append((x, y))
    return pts


def leaf_poly(kind):
    """Dense outline polygon + vein strokes (SVG) for leaf kind 0 maple, 1 oak, 2 elm."""
    if kind == 0:
        return bezier(maple_pts(60), closed=True), ("M 0 9 L 0 -50 M 0 9 L -40 -34 M 0 9 L 40 -34 "
                                                   "M 0 9 L -28 -2 M 0 9 L 28 -2")
    if kind == 1:
        return smooth_closed(oak_pts()), ("M 0 42 L 0 -40 M 0 -14 L -14 -24 M 0 -14 L 14 -24 "
                                                          "M 0 8 L -16 0 M 0 8 L 16 0 M 0 26 L -12 22 M 0 26 L 12 22")
    return smooth_closed(elm_pts()), ("M 0 42 L 0 -44 M 0 -20 L -14 -32 M 0 -20 L 14 -32 "
                                                      "M 0 0 L -18 -14 M 0 0 L 18 -14 M 0 20 L -16 8 M 0 20 L 16 8")


def leaf(i, style):
    kind = i % 3
    sid, col = COLORS[(i * 7 // 3) % 3]
    bez, veins = leaf_poly(kind)
    outline = [path(bez)]
    poly = sample_bez(bez, 3) if kind else bez["v"]
    stem = S(STEM_D, 0.8, (0, -23)) if kind == 0 else S(STEM_D)
    items = []
    if style == "shaded":
        items.append(group(S(veins) + [stroke("#5A1A08", 3.2, 45)], "veins"))
        items.append(group(outline + [shade_overlay((-50, -52, 50, 50), 0.9, dark="#4A1200")], "shade"))
        items.append(group(outline + [fill(col, slot=sid)], "leaf"))
        items.append(group(stem + [stroke("#6B3414", 5)], "stem"))
    elif style == "flat":
        # modern two-tone: the right half a shade darker, clean midrib
        items.append(group(S("M 0 9 L 0 -50" if kind == 0 else "M 0 38 L 0 -44") + [stroke(WHITE, 3, 50)], "rib"))
        items.append(group([path(bezier(clip_half(poly), closed=True)), fill("#4A1000", 24)], "half"))
        items.append(group(outline + [fill(col, slot=sid)], "leaf"))
        items.append(group(stem + [stroke(col, 5, slot=sid)], "stem"))
    else:  # doodle: ink line with an off-register colour fill
        items.append(group(S(veins) + [stroke(INK, 3, slot="outline")], "veins"))
        items.append(group(outline + [stroke(INK, 5.5, slot="outline")], "line"))
        items.append(group(stem + [stroke(INK, 5.5, slot="outline")], "stem"))
        items.append(group(outline + [fill(col, slot=sid)], "leaf", position=(6, 5), scale=(94, 94)))
    return items


def slots(comp, outline=False):
    for sid, col in COLORS:
        comp.slot(sid, col)
    if outline:
        comp.slot("outline", INK)


def mixed():
    comp = Comp("autumn-leaves-fall", W, H, frames=T)
    slots(comp)
    fall(comp, "leaf", 36, T, W, H, lambda i, d: leaf(i, "shaded"), seed=3, speed=(3.4, 5.6),
         sway=(30, 80), sway_period=(60, 120), spin=(30, 120), flip=0.75, flip_period=(30, 60),
         size=(0.8, 1.5), opacity=(80, 100), margin=110)
    return comp


def gust():
    comp = Comp("autumn-leaves-fall--gust", W, H, frames=T)
    slots(comp)
    fall(comp, "leaf", 50, T, W, H, lambda i, d: leaf(i + 1, "flat"), seed=8, speed=(5.6, 8.0),
         sway=(40, 110), sway_period=(40, 60), spin=(160, 320), flip=0.7, flip_period=(20, 40), wind=-6.0,
         size=(0.75, 1.4), opacity=(85, 100), margin=110)
    return comp


def doodle():
    comp = Comp("autumn-leaves-fall--doodle", W, H, frames=T)
    slots(comp, outline=True)
    fall(comp, "leaf", 32, T, W, H, lambda i, d: leaf(i + 2, "doodle"), seed=17, speed=(3.2, 5.4),
         sway=(30, 70), sway_period=(60, 120), spin=(30, 100), flip=0.6, flip_period=(30, 60),
         size=(0.85, 1.5), margin=110)
    return comp


build("autumn-leaves-fall", "Autumn Leaves Fall",
      "Maple, oak and elm leaves tumbling down over the whole frame in a seamless loop; a transparent "
      "overlay for autumn, harvest and Thanksgiving edits.",
      ["autumn", "fall", "leaves", "maple", "thanksgiving", "overlay", "seasonal"], [
          Variant("mixed", "Tumbling Leaves", mixed(), "loop", thumb_t=0.5, region=REGION, pad=0,
                  description="Softly shaded leaves with veins, flipping and swaying as they fall."),
          Variant("gust", "Wind Gust", gust(), "loop", thumb_t=0.5, region=REGION, pad=0,
                  description="Flat two-tone leaves blown sideways by a strong gust, spinning fast."),
          Variant("doodle", "Doodle", doodle(), "loop", thumb_t=0.5, region=REGION, pad=0, bg="f3ece0",
                  description="Hand-drawn ink leaves with off-register colour fills."),
      ])
