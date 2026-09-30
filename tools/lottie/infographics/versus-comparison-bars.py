from _common import *

W, H, F = 1000, 540, 84
MID = W / 2
GAP = 110                  # half-width of the centre label column
MAXL = 340
BH = 56
ROWS = [214, 324, 434]
VA = (0.82, 0.55, 0.72)
VB = (0.6, 0.86, 0.5)
BOLT = [(8, -30), (-14, 4), (0, 4), (-8, 30), (14, -6), (0, -6)]


def row_t(i):
    return 14 + i * 6


def grow(side, cy, v, t, h=BH, e=EXPO_OUT, r=None):
    """Bar growing outward from the centre column; side -1 = left (A), +1 = right (B)."""
    r = h / 2 if r is None else r
    x0 = MID + side * GAP
    wf = MAXL * v
    size = keys((t, [h, h], e), (t + 26, [wf, h]))
    pos = keys((t, [x0 + side * h / 2, cy], e), (t + 26, [x0 + side * wf / 2, cy]))
    return rect(size, pos, r)


def areas():
    d = {"nameA": (40, 36, 360, 64), "nameB": (W - 400, 36, 360, 64)}
    for i, y in enumerate(ROWS):
        d[f"label{i + 1}"] = (MID - GAP + 12, y - 28, 2 * GAP - 24, 56)
        d[f"valueA{i + 1}"] = (MID - GAP - 140, y - 22, 124, 44)
        d[f"valueB{i + 1}"] = (MID + GAP + 16, y - 22, 124, 44)
    return d


def badge(comp, style):
    c = (MID, 68)
    t = 4
    bolt = [(c[0] + x, c[1] + y) for x, y in BOLT]
    if style == "flat":
        shapes = [group([polyline(bolt, closed=True), fill("#FFFFFF")], "bolt"),
                  group([path(arc(34, -45, 135, c)), polyline([pt(c, 34, 135), pt(c, 34, -45)]), fill(slot="secondary")],
                        "b"),
                  group([ellipse((68, 68), c), fill(slot="primary")], "a")]
    elif style == "neon":
        shapes = glow_strokes([polyline(bolt, closed=True)], slot="accent", width=3, widths=(18, 10), ops=(10, 22)) + \
            glow_strokes([ellipse((72, 72), c)], slot="outline", width=3, core=False, widths=(18,), ops=(12,))
    else:
        shapes = [ink([wobble(bolt + [bolt[0]], 0.6, 2, step=12)], width=4),
                  group([polyline(bolt, closed=True), fill(slot="accent")], "f"),
                  ink([sketch_circle_pts(c, 36, seed=3, amp=0.04, turns=1.1, n=18)], width=4, name="ring")]
    comp.layer("badge", shapes, anchor=c, position=c, scale=keys((t, [0, 0], SPRING), (t + 16, [100, 100])),
               rotation=keys((t, -120, EXPO_OUT), (t + 20, 0)))


def flat():
    """Two teams face off: rounded bars grow outward from a centre column, a split badge spins in on top."""
    comp = Comp("versus-comparison-bars", W, H, fps=30, frames=F)
    slots(comp, FLAT, "primary", "secondary", "background")
    badge(comp, "flat")
    for side, s, x in ((-1, "primary", 40), (1, "secondary", W - 400)):
        comp.layer(f"underline{side}", [box(x, 108, 360, 6, slot=s, r=3)],
                   anchor=(MID + side * 60, 111), position=(MID + side * 60, 111),
                   scale=keys((8, [0, 100], EXPO_OUT), (30, [100, 100])))
    for i, y in enumerate(ROWS):
        t = row_t(i)
        for side, vals, s in ((-1, VA, "primary"), (1, VB, "secondary")):
            win = vals[i] > (VB if side < 0 else VA)[i]
            comp.layer(f"bar{i}{side}", [group([grow(side, y, vals[i], t + (0 if side < 0 else 2)),
                                                fill(slot=s)], "b")],
                       opacity=fade(t, t + 3), ip=t)
            if win:
                edge = (MID + side * (GAP + MAXL * vals[i] - 14), y)
                spark(comp, edge, t + 24, size=44, name=f"spark{i}{side}")
        comp.layer(f"track{i}", [group([rect((2 * (GAP + MAXL), BH), (MID, y), BH / 2), fill(slot="background",
                                                                                          opacity=8)], "t"),
                                 group([rect((2 * GAP - 16, BH), (MID, y), 14), fill(slot="background", opacity=12)],
                                       "mid")],
                   anchor=(MID, y), position=(MID, y), scale=keys((t - 6, [10, 100], EXPO_OUT), (t + 10, [100, 100])),
                   opacity=fade(t - 6, t))
    return comp


def slant(x, cy, w, h, k=14):
    return [(x + k, cy - h / 2), (x + w + k, cy - h / 2), (x + w - k, cy + h / 2), (x - k, cy + h / 2)]


def neon():
    """Dark panel; slanted neon bars shoot out from the centre in two glowing colours."""
    comp = Comp("versus-comparison-bars--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, "primary", "secondary", "accent", "background", "outline")
    badge(comp, "neon")
    for i, y in enumerate(ROWS):
        t = row_t(i)
        for side, vals, s in ((-1, VA, "primary"), (1, VB, "secondary")):
            wf = MAXL * vals[i]
            x0 = MID + side * GAP
            p0 = slant(x0 if side > 0 else x0 - 20, y, 20, BH - 8)
            p1 = slant(x0 if side > 0 else x0 - wf, y, wf, BH - 8)
            shp = path(keys((t, bezier(p0), EXPO_OUT), (t + 26, bezier(p1))))
            comp.layer(f"bar{i}{side}", soft_glow([shp], slot=s, spread=(12, 28), ops=(26, 10), body_opacity=80),
                       opacity=fade(t, t + 3), ip=t)
            tip = x0 + side * wf
            comp.layer(f"tip{i}{side}", [group([polyline([(tip + 14, y - BH / 2 + 4), (tip - 14, y + BH / 2 - 4)]),
                                                stroke("#FFFFFF", width=4)], "t")],
                       position=keys((t, [-side * (wf - 20), 0], EXPO_OUT), (t + 26, [0, 0])),
                       opacity=keys((t, 0, HOLD), (t + 1, 100, HOLD), (t + 26, 100, EASE_IN), (t + 40, 30)), ip=t)
        comp.layer(f"track{i}", [group([polyline(slant(MID - GAP - MAXL, y, MAXL, BH - 8), closed=True),
                                        polyline(slant(MID + GAP, y, MAXL, BH - 8), closed=True),
                                        stroke(slot="outline", width=2, opacity=25)], "t")],
                   opacity=fade(t - 6, t + 2))
        comp.layer(f"mid{i}", [group([polyline([(MID - GAP + 20, y + BH / 2), (MID + GAP - 20, y + BH / 2)]),
                                      stroke(slot="outline", width=2, opacity=40)], "m")],
                   opacity=fade(t, t + 8))
    for side, s, x in ((-1, "primary", 40), (1, "secondary", W - 400)):
        comp.layer(f"underline{side}", glow_strokes([polyline([(x, 110), (x + 360, 110)])], slot=s, width=3,
                                                    core=False, widths=(14,), ops=(16,),
                                                    extra=[trim(end=keys((6, 0, EXPO_OUT), (28, 100)))]))
    neon_panel(comp, 14, 14, W - 28, H - 28, r=32)
    return comp


def sketch():
    """Paper card; hand-drawn bars get scribbled in from the centre in two marker colours."""
    comp = Comp("versus-comparison-bars--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "secondary", "accent", "background", "outline")
    paper = Paper(comp, 20, 16, W - 40, H - 32, tilt=0.6, r=16)
    card = paper.rig
    badge(comp, "sketch")
    comp.layers[-1]["parent"] = card
    for side, s, x in ((-1, "primary", 40), (1, "secondary", W - 400)):
        comp.layer(f"underline{side}", [ink([wobble([(x + 10, 108), (x + 350, 106)], 1.5, side + 5)], width=9, slot=s,
                                             color="#FF5A4E", opacity=90, draw=(6, 24))], parent=card)
    for i, y in enumerate(ROWS):
        t = row_t(i)
        for side, vals, s in ((-1, VA, "primary"), (1, VB, "secondary")):
            wf = MAXL * vals[i]
            x0 = MID + side * GAP
            xl = x0 if side > 0 else x0 - wf
            comp.layer(f"box{i}{side}", [ink([sketch_rect_pts(xl, y - BH / 2, wf, BH, seed=i * 3 + side, amp=1.6)],
                                             width=4, draw=(t - 4, t + 10))], parent=card)
            pts = scribble_pts(xl + 10, y - BH / 2 + 10, wf - 20, BH - 20, spacing=12, slant=16, seed=i + side)
            if side < 0:
                pts = pts[::-1]
            comp.layer(f"fill{i}{side}", [marker(pts, 15, slot=s, draw=(t + 6, t + 30))], parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "versus-comparison-bars", "Versus Comparison Bars",
            "Head-to-head comparison: two sets of bars grow outward from a centre column across three rows. Put the "
            "two names in 'nameA'/'nameB', the row topics in 'label1'-'label3' and the numbers in "
            "'valueA1'-'valueA3' and 'valueB1'-'valueB3'.",
            ["versus", "comparison", "vs", "compare", "bars", "stats", "infographic", "head-to-head"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Rounded bars grow outward from a centre column under a spinning split badge."),
    V("neon", "Neon Slant", neon(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Dark panel; slanted neon bars shoot out in two glowing colours with white-hot tips."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Paper card; hand-drawn bars scribbled in from the centre in two marker colours."),
])
