"""A pair of suspicious cartoon side-eyes that punch in and dart left and right before settling."""

from _memes2 import *

W, H = 640, 360
C = (W / 2, H / 2 + 10)
F = 60
GAP = 150  # half distance between eye centres

# pupil x offsets (fraction of max travel) and zoom punches
DARTS = [(0, 0, HOLD), (10, 0, EXPO_OUT), (14, -1, HOLD), (24, -1, EXPO_OUT), (28, 1, HOLD), (36, 1, EXPO_OUT),
         (40, -1, HOLD), (46, -1, EXPO_OUT), (50, 0.9, LINEAR)]
ZOOM = [(0, [0, 0], SPRING), (9, [100, 100], HOLD), (38, [100, 100], EXPO_OUT), (41, [116, 116], EASE_IN_OUT),
        (52, [108, 108])]
SQUINT = [(0, 0, HOLD), (36, 0, EXPO_OUT), (41, 1, EASE_IN_OUT), (52, 0.8, LINEAR)]


def dart_pos(travel, dy=0):
    return keys(*[(t, [v * travel, dy], e) for t, v, e in DARTS])


def lid_pos(open_y, closed_y):
    return keys(*[(t, [0, open_y + (closed_y - open_y) * v], e) for t, v, e in SQUINT])


def eyes(comp, ew, eh, pupil, travel, lid_open, lid_closed, lid_slot, draw_pupil, outline=None, lid_line=None,
         brow=None, shape=None, rig_parent=None, pupil_y=0.08):
    """Adds the eye layers: inner (pupils + lids, matted to the eyes), then whites and outline."""
    xs = (C[0] - GAP, C[0] + GAP)
    eye_shape = shape or (lambda x: ellipse((ew, eh), (x, C[1])))
    if brow:
        comp.layer("brows", brow(xs), parent=rig_parent)
    inner = []
    for x in xs:
        lid_items = [rect((ew + 40, eh), (x, C[1] - eh / 2)), fill(slot=lid_slot)]
        if lid_line:
            inner.append(group([polyline([(x - ew / 2 - 10, C[1]), (x + ew / 2 + 10, C[1])]),
                                stroke(slot=lid_line, width=10)], "lid-line",
                               position=lid_pos(lid_open, lid_closed)))
        inner.append(group(lid_items, "lid", position=lid_pos(lid_open, lid_closed)))
    for x in xs:
        inner.append(group(draw_pupil(x, C[1] + eh * pupil_y), "pupil", position=dart_pos(travel)))
    comp.layer("matte", [group([eye_shape(x) for x in xs] + [fill("#000000")], "m")], parent=rig_parent)
    comp.layer("inner", inner, parent=rig_parent, matte="alpha")
    if outline:
        comp.layer("outline", [group([eye_shape(x) for x in xs] + [stroke(slot=outline[0], width=outline[1])], "o")],
                   parent=rig_parent)
    comp.layer("whites", [group([eye_shape(x) for x in xs] + [fill("#FFFFFF")], "w")], parent=rig_parent)


def cartoon():
    """Big round cartoon eyes with heavy lids and angled brows; black pupils dart side to side."""
    comp = base("suspicious-eyes-zoom", W, H, F)
    comp.slot("outline", INK)
    comp.slot("primary", "#F0B98E")
    rg = rig(comp, "rig", C, scale=keys(*ZOOM))

    def pupil(x, y):
        return [group([ellipse((20, 20), (x + 14, y - 16)), fill("#FFFFFF")], "glint"),
                group([ellipse((80, 88), (x, y)), fill(INK)], "p")]

    def brow(xs):
        return [group([polyline([(xs[0] - 100, C[1] - 132), (xs[0] + 90, C[1] - 104)]),
                       polyline([(xs[1] + 100, C[1] - 150), (xs[1] - 90, C[1] - 116)]),
                       stroke(slot="outline", width=22)], "brows",
                      position=keys(*[(t, [0, 12 * v], e) for t, v, e in SQUINT]))]
    eyes(comp, 224, 206, 80, 56, -50, -8, "primary", pupil, outline=("outline", 12), lid_line="outline",
         brow=brow, rig_parent=rg, pupil_y=0.2)
    return comp


def anime():
    """Tall glossy anime eyes with a thick lash line and coloured irises that glance sideways."""
    comp = base("suspicious-eyes-zoom--anime", W, H, F)
    comp.slot("outline", "#1A1420")
    comp.slot("accent", "#7A4BE0")
    comp.slot("primary", "#F4D1B5")
    rg = rig(comp, "rig", C, scale=keys(*ZOOM))
    ew, eh = 190, 150

    def shape(x):
        y = C[1]
        return path(bezier([(x - ew / 2, y + 4), (x, y - eh / 2), (x + ew / 2, y - 10), (x, y + eh / 2)],
                           [(0, 22), (-60, 0), (0, -30), (60, 0)],
                           [(0, -30), (60, 0), (0, 26), (-60, 0)]), "eye")

    def pupil(x, y):
        return [group([ellipse((26, 34), (x + 18, y - 22)), fill("#FFFFFF")], "hi"),
                group([ellipse((12, 12), (x - 20, y + 20)), fill("#FFFFFF", 80)], "hi2"),
                group([ellipse((44, 70), (x, y)), fill("#120A18")], "pupil"),
                group([ellipse((96, 118), (x, y)), gradient_fill([(0, "#FFFFFF", 0), (1, "#000000", 0.35)],
                                                               (x, y + 50), (x, y - 60))], "shade"),
                group([ellipse((96, 118), (x, y)), fill(slot="accent")], "iris")]

    def brow(xs):
        return [group([path(arc(120, 200, 300, (xs[0] + 20, C[1] + 20))),
                       path(arc(120, 240, 340, (xs[1] - 20, C[1] + 20))),
                       stroke(slot="outline", width=9)], "brows",
                      position=keys(*[(t, [0, 20 + 14 * v], e) for t, v, e in SQUINT]))]
    lash = [group([shape(C[0] - GAP), shape(C[0] + GAP)] + [trim(start=0, end=50),
                                                          stroke(slot="outline", width=16)], "lash")]
    comp.layer("lash", lash, parent=rg)
    eyes(comp, ew, eh, 96, 44, -34, -6, "primary", pupil, outline=("outline", 5), lid_line="outline",
         shape=shape, rig_parent=rg)
    return comp


def pixel():
    """Pixel-art eyes: chunky square pupils jump in whole pixels and the lids step down."""
    comp = base("suspicious-eyes-zoom--pixel", W, H, F)
    comp.slot("outline", "#101010")
    comp.slot("primary", "#3A2A4A")
    P = 20
    rg = rig(comp, "rig", C, scale=keys((0, [0, 0], HOLD), (2, [60, 60], HOLD), (4, [100, 100], HOLD),
                                         (38, [100, 100], HOLD), (40, [115, 115], HOLD), (52, [108, 108])))
    grid = ["  ######  ",
            " #......# ",
            "#........#",
            "#........#",
            " #......# ",
            "  ######  "]

    def cells(ch):
        return pixel_outline(grid, lambda c: c in ch, P, (-5 * P, -3 * P))

    xs = (C[0] - GAP, C[0] + GAP)
    darts = [(t, [round(v * 2) * P, 0], HOLD) for t, v, e in DARTS]
    lids = [(t, [0, (-2 + round(v * 2)) * P], HOLD) for t, v, e in SQUINT]
    for i, x in enumerate(xs):
        comp.layer(f"matte{i}", [group(cells(".") + [fill("#000000")], "m")], parent=rg, position=(x, C[1]))
        comp.layer(f"inner{i}", [group([rect((P * 10, P * 3), (0, -P * 1.5)), fill(slot="primary")], "lid",
                                       position=keys(*lids)),
                                 group([rect((P, P), (P * 0.5, -P * 0.5)), fill("#FFFFFF")], "glint",
                                       position=keys(*darts)),
                                 group([rect((P * 2, P * 3), (0, P * 0.5)), fill(slot="outline")], "pupil",
                                       position=keys(*darts))],
                   parent=rg, position=(x, C[1]), matte="alpha")
        comp.layer(f"eye{i}", [group(cells("#") + [fill(slot="outline")], "rim"),
                               group(cells(".") + [fill("#FFFFFF")], "white")], parent=rg, position=(x, C[1]))
        ys = (-2 * P, -P, 0) if i == 0 else (0, -P, -2 * P)  # inner ends lower: a frown
        steps = [rect((P * 2, P), (dx * 2 * P, y)) for dx, y in zip((-1, 0, 1), ys)]
        comp.layer(f"brow{i}", [group(steps + [fill(slot="outline")], "b")], parent=rg,
                   position=(x + (P if i == 0 else -P), C[1] - 3.5 * P))
    return comp


build_asset(CAT, "suspicious-eyes-zoom", "Suspicious Side Eyes",
            "A pair of suspicious cartoon eyes that punch in, dart left and right, squint with a zoom punch and "
            "settle on a side-eye. Place over a face or next to the suspect.",
            ["eyes", "suspicious", "side eye", "sus", "zoom", "meme", "look"], [
    Variant("cartoon", "Cartoon", cartoon(), "intro-hold", thumb_t=1.0, bg="e8e8ee",
            description="Round cartoon eyes with heavy lids and angled brows; black pupils dart side to side."),
    Variant("anime", "Anime", anime(), "intro-hold", thumb_t=1.0, bg="e8e8ee",
            description="Tall glossy eyes with a thick lash line and coloured irises."),
    Variant("pixel", "Pixel", pixel(), "intro-hold", thumb_t=1.0, bg="e8e8ee",
            description="Pixel-art eyes whose square pupils jump in whole pixels while the lids step down."),
])
