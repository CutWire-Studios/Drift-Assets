from _lt2 import *

CHROME = [(0, "#F4F7FF"), (0.28, "#A9C2FF"), (0.5, "#FFFFFF"), (0.62, "#E2B8FF"), (0.82, "#FF9BE4"),
          (1, "#B69CFF")]


def stadium_pt(s, cx, cy, a, R):
    """Point, outward normal and tangent at arc length s around a stadium (clockwise from top-left)."""
    P = 4 * a + 2 * math.pi * R
    s %= P
    if s < 2 * a:
        return (cx - a + s, cy - R), (0, -1), (1, 0)
    s -= 2 * a
    if s < math.pi * R:
        th = -math.pi / 2 + s / R
        n = (math.cos(th), math.sin(th))
        return (cx + a + R * n[0], cy + R * n[1]), n, (-n[1], n[0])
    s -= math.pi * R
    if s < 2 * a:
        return (cx + a - s, cy + R), (0, 1), (-1, 0)
    s -= 2 * a
    th = math.pi / 2 + s / R
    n = (math.cos(th), math.sin(th))
    return (cx - a + R * n[0], cy + R * n[1]), n, (-n[1], n[0])


def scallop(cx, cy, w, h, bumps, depth, name="scallop"):
    """Bubbly cloud outline: a stadium whose edge is a chain of outward bulges."""
    R = h / 2
    a = w / 2 - R
    P = 4 * a + 2 * math.pi * R
    L = P / bumps
    v, it, ot = [], [], []
    for i in range(bumps):
        p, n, t = stadium_pt(i * L, cx, cy, a, R)
        v.append(p)
        it.append((-t[0] * L * 0.3 + n[0] * depth, -t[1] * L * 0.3 + n[1] * depth))
        ot.append((t[0] * L * 0.3 + n[0] * depth, t[1] * L * 0.3 + n[1] * depth))
    return path(bezier(v, it, ot, True), name)


def twinkle(comp, name, cx, cy, r, t0, t_out, period=36, slot="accent", parent=None):
    k = [(0, [0, 0], HOLD), (t0, [0, 0], SPRING), (t0 + 10, [100, 100], EASE_IN_OUT)]
    t, big = t0 + 10 + period / 2, False
    while t < t_out:
        k.append((t, [100, 100] if big else [55, 55], EASE_IN_OUT))
        big = not big
        t += period / 2
    k += [(t_out, [100, 100], EXPO_IN), (t_out + 10, [0, 0])]
    lay(comp, name, [sparkle(cx, cy, r), fill(slot=slot)], (cx, cy), scale=keys(*k),
        rotation=keys((t0, -90, EXPO_OUT), (t0 + 14, 0)), parent=parent)


def sticker(outline, body, x0, y0, x1, y1, gloss=None):
    """Die-cut sticker: chrome body, glossy highlight, white border and a coloured drop shadow."""
    items = []
    if gloss:
        items.append(group([gloss, fill("#FFFFFF", 55)], "gloss"))
    items += [group([body, gradient_fill(CHROME, (x0, y0), (x1, y1))], "chrome"),
              group([body, stroke(slot="primary", width=3, opacity=70)], "inner-line"),
              group([outline, fill(slot="outline")], "border"),
              group([outline, fill(slot="secondary")], "shadow", position=(8, 10))]
    return items


def slots(comp, sh="#7A3CFF"):
    comp.slot("outline", "#FFFFFF")
    comp.slot("secondary", sh)
    comp.slot("accent", "#FFFFFF")
    comp.slot("primary", "#8A6BFF")


def bubble():
    W, H = 1100, 260
    cx, cy, w, h = 540, 130, 820, 130
    comp = base("lower-third-y2k-sticker", W, H, 30)
    slots(comp)
    for i, (sx, sy, r, t) in enumerate(((cx - w / 2 - 10, cy - 60, 30, 14), (cx + w / 2 + 30, cy - 34, 22, 18),
                                        (cx + w / 2 - 30, cy + 70, 16, 22), (cx - w / 2 + 70, cy + 76, 14, 20))):
        twinkle(comp, f"sparkle{i}", sx, sy, r, t, 118 + i * 2, period=30 + 6 * i)
    rg = rig(comp, "rig", (cx, cy), scale=pop(0, 18, 122, 138, peak=108),
             rotation=keys((0, -10, SPRING), (18, -2, HOLD), (122, -2, EXPO_IN), (138, 8)))
    outline = rect((w + 28, h + 28), (cx, cy), (h + 28) / 2)
    body = rect((w, h), (cx, cy), h / 2)
    gloss = rrect(cx - w / 2 + 40, cy - h / 2 + 12, w - 200, 20, 10)
    comp.layer("sticker", sticker(outline, body, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, gloss), parent=rg)
    return comp, (cx - w / 2 + 70, cy - 30, w - 140, 60)


def blob():
    W, H = 1100, 280
    cx, cy, w, h = 540, 140, 820, 150
    comp = base("lower-third-y2k-sticker--blob", W, H, 34)
    slots(comp, "#FF4FB8")
    for i, (sx, sy, r, t) in enumerate(((cx - w / 2 + 10, cy - 78, 28, 16), (cx + w / 2 + 16, cy + 50, 26, 20),
                                        (cx + 140, cy - 92, 16, 24))):
        twinkle(comp, f"sparkle{i}", sx, sy, r, t, 118 + i * 2, period=28 + 8 * i)
    rg = rig(comp, "rig", (cx, cy + h / 2),
             scale=keys((0, [20, 20], (0.3, 1.4, 0.6, 1)), (10, [112, 88], EASE_IN_OUT), (17, [94, 108], EASE_IN_OUT),
                        (24, [103, 97], EASE_IN_OUT), (30, [100, 100], HOLD), (120, [100, 100], EASE_IN_OUT),
                        (126, [110, 90], EXPO_IN), (138, [0, 0])),
             opacity=keys((0, 0, HOLD), (1, 100, HOLD), (137, 100, HOLD), (138, 0)))
    outline = scallop(cx, cy, w + 34, h + 34, 30, 16)
    body = scallop(cx, cy, w, h, 30, 12)
    gloss = rrect(cx - w / 2 + 70, cy - h / 2 + 18, 260, 18, 9)
    comp.layer("sticker", sticker(outline, body, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, gloss), parent=rg)
    return comp, (cx - w / 2 + 90, cy - 36, w - 180, 72)


def tilt_stack():
    W, H = 1100, 300
    comp = base("lower-third-y2k-sticker--stack", W, H, 36)
    slots(comp, "#00B3FF")
    a = (500, 110, 800, 120, -4)
    b = (350, 222, 460, 64, 3)
    twinkle(comp, "sparkle0", 100, 44, 30, 12, 118)
    twinkle(comp, "sparkle1", 930, 196, 24, 20, 120, period=40)
    twinkle(comp, "sparkle2", 610, 218, 14, 26, 116, period=30)
    for nm, (cx, cy, w, h, rot), t0, t2 in (("sub", b, 10, 118), ("head", a, 0, 124)):
        rg = rig(comp, f"{nm}-rig", (cx, cy), scale=pop(t0, t0 + 16, t2, t2 + 14, peak=108),
                 rotation=keys((t0, rot * 4, SPRING), (t0 + 16, rot, HOLD), (t2, rot, EXPO_IN), (t2 + 14, rot * -3)))
        outline = rect((w + 24, h + 24), (cx, cy), (h + 24) / 2)
        body = rect((w, h), (cx, cy), h / 2)
        gloss = rrect(cx - w / 2 + 34, cy - h / 2 + 10, w * 0.5, h * 0.14, h * 0.07)
        comp.layer(nm, sticker(outline, body, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, gloss), parent=rg)
    # text areas are axis-aligned boxes inside the tilted stickers
    return comp, (a[0] - a[2] / 2 + 70, a[1] - 34, a[2] - 140, 64), (b[0] - b[2] / 2 + 50, b[1] - 18, b[2] - 100, 36)


a, ah = bubble()
b, bh = blob()
c, chd, cs = tilt_stack()
build("lower-third-y2k-sticker", "Y2K Sticker Lower Third",
      "Bubbly Y2K die-cut sticker with a chrome gradient, a glossy highlight and twinkling sparkles. Type your "
      "name or title across the sticker.",
      ["lower third", "y2k", "sticker", "chrome", "sparkle", "bubbly", "retro", "cute"], [
          V("bubble", "Chrome Bubble", a, ah, bg="e8e8ee",
            description="Chrome pill sticker that bounces in tilted, with sparkles twinkling around it."),
          V("blob", "Cloud Blob", b, bh, bg="e8e8ee",
            description="Scalloped cloud-shaped sticker that squashes and stretches as it lands."),
          V("stack", "Tilted Stack", c, chd, cs, bg="e8e8ee",
            description="Two stickers, headline and subtitle, slapped on at opposite tilts."),
      ])
