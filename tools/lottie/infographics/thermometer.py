from _common import *

W, H, F = 440, 680, 78
TX = 160                 # tube centre x
TT, TB = 90, 480         # tube top / bottom (where it meets the bulb)
TW = 58
BULB = (TX, 548)
BR = 64
LEVEL = 0.7
T0, T1 = 14, 50
TOPY = TB - (TB - TT - 20) * LEVEL


def tube_shape(tw=TW, pad=0):
    """Tube + bulb outline as one closed bezier (tube joins the bulb tangentially enough to read as one)."""
    r = tw / 2 + pad
    br = BR + pad
    k = 0.5523
    top = TT - pad
    # angle where the tube wall meets the bulb circle
    a = math.degrees(math.asin(r / br))
    jl = pt(BULB, br, -90 - a)
    jr = pt(BULB, br, -90 + a)
    v = [(TX - r, top + r), (TX, top), (TX + r, top + r), jr]
    it = [(0, k * r), (-k * r, 0), (0, -k * r), (0, 0)]
    ot = [(0, -k * r), (k * r, 0), (0, k * r), (0, 0)]
    # bulb arc from jr clockwise round the bottom to jl
    arcb = arc(br, -90 + a, 270 - a, BULB)
    for j in range(1, len(arcb["v"])):
        v.append(tuple(arcb["v"][j]))
        it.append(tuple(arcb["i"][j]))
        ot.append(tuple(arcb["o"][j]))
    ot[3] = tuple(arcb["o"][0])
    ot[-1] = (0, 0)
    return bezier(v, it, ot, closed=True)


def mercury_col(e=(0.3, 1.25, 0.5, 1.0), w=TW - 24, t0=T0, t1=T1):
    """Column rising from the bulb to TOPY with a little overshoot."""
    y0 = TB + 10
    size = keys((t0, [w, 1], e), (t1, [w, y0 - TOPY]))
    pos = keys((t0, [TX, y0], e), (t1, [TX, (y0 + TOPY) / 2]))
    return rect(size, pos, w / 2)


def tick_lines(x0, long=26, short=14, n=12):
    out = []
    for k in range(n + 1):
        y = TB - 10 - (TB - TT - 40) * k / n
        out.append(polyline([(x0, y), (x0 + (long if k % 3 == 0 else short), y)]))
    return out


def areas():
    return {"value": (TX + TW / 2 + 56, TOPY - 36, W - TX - TW / 2 - 56 - 16, 72),
            "label": (40, H - 66, W - 80, 48)}


def flat():
    """Glass tube with ticks; the bulb fills and the red column rises to 70% with a small overshoot."""
    comp = Comp("thermometer", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FF4D5E"}, "primary", "outline")
    rg = rig(comp, "thermo", BULB, scale=keys((0, [80, 80], SOFT_SPRING), (16, [100, 100])))
    comp.layer("shine", [group([polyline([(TX - TW / 2 + 12, TT + 30), (TX - TW / 2 + 12, TB - 20)]),
                                stroke("#FFFFFF", width=6, opacity=45)], "s"),
                         group([arc_path(BR - 16, 190, 250, BULB), stroke("#FFFFFF", width=8, opacity=45)], "b")],
               parent=rg, opacity=fade(T1 - 10, T1))
    comp.layer("column", [group([mercury_col(), fill(slot="primary")], "c")], parent=rg, ip=T0)
    comp.layer("bulb", [group([ellipse((2 * BR - 22, 2 * BR - 22), BULB), fill(slot="primary")], "b")], parent=rg,
               anchor=BULB, position=BULB, scale=keys((6, [0, 0], SPRING), (18, [100, 100])), ip=6)
    comp.layer("ticks", [group(tick_lines(TX + TW / 2 + 16) + [trim(end=keys((6, 0, EASE_OUT), (30, 100))),
                                                               stroke(slot="outline", width=4)], "t")], parent=rg)
    comp.layer("glass", [group([path(tube_shape()), stroke(slot="outline", width=8)], "rim"),
                         group([path(tube_shape()), fill(slot="outline", opacity=10)], "glass")], parent=rg,
               opacity=fade(0, 4))
    return comp


def neon():
    """Dark panel; a neon tube with glowing ticks and a column that surges up with a hot core."""
    comp = Comp("thermometer--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#FF3D6E", "outline": "#23E5FF"}, "primary", "background", "outline")
    comp.layer("head", [group([ellipse((TW - 16, 18)), fill("#FFFFFF")], "c"),
                        group([ellipse((TW + 30, 50)), fill(slot="primary", opacity=24)], "g")],
               position=keys((T0, [TX, TB + 10], (0.3, 1.25, 0.5, 1.0)), (T1, [TX, TOPY + 12])), ip=T0,
               opacity=keys((T0, 0, EASE_OUT), (T0 + 3, 100, HOLD), (T1 + 4, 100, EASE_IN), (T1 + 20, 0)))
    comp.layer("column", soft_glow([mercury_col(w=TW - 28)], slot="primary", spread=(14, 30), ops=(26, 10)), ip=T0)
    comp.layer("bulb", soft_glow([ellipse((2 * BR - 28, 2 * BR - 28), BULB)], slot="primary", spread=(16, 36),
                                 ops=(26, 10)),
               anchor=BULB, position=BULB, scale=keys((6, [0, 0], SPRING), (18, [100, 100])), ip=6)
    comp.layer("ticks", glow_strokes(tick_lines(TX + TW / 2 + 18), slot="outline", width=3, core=False,
                                     widths=(14,), ops=(14,), extra=[trim(end=keys((4, 0, EASE_OUT), (28, 100)))]))
    comp.layer("tube", glow_strokes([path(tube_shape())], slot="outline", width=4, widths=(24, 12), ops=(8, 18),
                                    extra=[trim(end=keys((0, 0, EASE_IN_OUT), (20, 100)))]))
    neon_panel(comp, 16, 16, W - 32, H - 32, r=34)
    return comp


def sketch():
    """Paper card; an ink thermometer draws itself and a marker scribble climbs up the tube."""
    comp = Comp("thermometer--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "background", "outline")
    paper = Paper(comp, 20, 20, W - 40, H - 40, tilt=1.2, r=16)
    card = paper.rig
    ts = tube_shape()
    outline = [(v[0], v[1]) for v in ts["v"]]
    dense = []
    for j in range(len(outline)):
        a, b = ts["v"][j], ts["v"][(j + 1) % len(outline)]
        oa, ib = ts["o"][j], ts["i"][(j + 1) % len(outline)]
        for s in range(8):
            u = s / 8
            p0, p1 = a, (a[0] + oa[0], a[1] + oa[1])
            p2, p3 = (b[0] + ib[0], b[1] + ib[1]), b
            dense.append(tuple((1 - u) ** 3 * p0[k] + 3 * (1 - u) ** 2 * u * p1[k] + 3 * (1 - u) * u * u * p2[k]
                               + u ** 3 * p3[k] for k in (0, 1)))
    dense += dense[:4]
    rnd = random.Random(3)
    dense = [(x + rnd.uniform(-1.5, 1.5), y + rnd.uniform(-1.5, 1.5)) for x, y in dense]
    ticks = [wobble([(TX + TW / 2 + 18, y), (TX + TW / 2 + 18 + ln, y + 1)], 0.8, k, step=12)
             for k, (y, ln) in enumerate((TB - 10 - (TB - TT - 40) * q / 12, 26 if q % 3 == 0 else 14)
                                         for q in range(13))]
    comp.layer("ticks", [ink(ticks, width=3.5, draw=(10, 30))], parent=card)
    comp.layer("outline", [ink([catmull(dense, 2)], width=5, draw=(2, 26))], parent=card)
    comp.layer("bulb", [marker(catmull([pt(BULB, BR - 18 - k * 9, a) for k in range(5) for a in range(0, 360, 40)], 3),
                               22, draw=(8, 18), opacity=92)], parent=card)
    col = scribble_v_pts(TX - TW / 2 + 14, TOPY, TW - 28, TB + 10 - TOPY, spacing=10, slant=6, seed=2, over=2)
    comp.layer("column", [marker(col, 14, draw=(T0 + 4, T1 + 4, EASE_IN_OUT), opacity=92)], parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "thermometer", "Thermometer",
            "A thermometer whose column rises to about 70% against a tick scale. Put the reading in the 'value' area "
            "beside the top of the column and a caption in 'label' underneath.",
            ["thermometer", "temperature", "gauge", "heat", "level", "weather", "infographic", "meter"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Glass tube with ticks; the bulb fills and the red column rises with a small overshoot."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Dark panel with a neon tube; the column surges up behind a white-hot head."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Paper card; an ink thermometer draws itself and a marker scribble climbs the tube."),
])
