from _common import *

W, H, F = 880, 500, 84
C = (250, 250)
VALS = (0.40, 0.28, 0.20, 0.12)
SEG = ("primary", "secondary", "accent", "icon")
LX = 520          # legend dot x
LY = [134, 212, 290, 368]


def starts():
    a, out = -90.0, []
    for v in VALS:
        out.append((a, a + 360 * v))
        a += 360 * v
    return out


def areas(center=True):
    d = {}
    if center:
        d["value"] = (C[0] - 80, C[1] - 44, 160, 88)
    for i, y in enumerate(LY):
        d[f"label{i + 1}"] = (LX + 34, y - 26, 300, 52)
    return d


def seg_time(i):
    return 8 + i * 7


def legend(comp, style, pal_width=None):
    for i, y in enumerate(LY):
        t = seg_time(i) + 10
        c = (LX, y)
        if style == "flat":
            shapes = [group([ellipse((26, 26), c), fill(slot=SEG[i])], "dot")]
            line = [group([rect((300, 4), (LX + 34 + 150, y + 30), 2), fill(slot="background", opacity=12)], "rule")]
        elif style == "neon":
            shapes = soft_glow([ellipse((16, 16), c)], slot=SEG[i], spread=(10, 22), ops=(30, 12))
            shapes.insert(0, group([ellipse((30, 30), c), stroke(slot=SEG[i], width=2.5)], "ring"))
            line = [group([rect((300, 2), (LX + 34 + 150, y + 30)), fill(slot=SEG[i], opacity=25)], "rule")]
        else:
            shapes = [group([rect((26, 26), c, 6), fill(slot=SEG[i])], "chip"),
                      group([rect((26, 26), (c[0], c[1] + 7), 6), fill("#000000", 35), fill(slot=SEG[i])], "side")]
            line = []
        comp.layer(f"key{i}", shapes, anchor=c, position=c, scale=pop(t, 12))
        if line:
            comp.layer(f"rule{i}", line, anchor=(LX + 34, y), position=(LX + 34, y),
                       scale=keys((t, [0, 100], EXPO_OUT), (t + 18, [100, 100])), opacity=fade(t, t + 4))


def flat():
    """Thick donut whose four segments sweep in one after another, with gaps between; legend dots pop."""
    comp = Comp("donut-chart", W, H, fps=30, frames=F)
    slots(comp, FLAT, *SEG, "background")
    legend(comp, "flat")
    rg = rig(comp, "donut", C, rotation=keys((0, -50, EXPO_OUT), (40, 0)),
             scale=keys((0, [60, 60], SOFT_SPRING), (20, [100, 100])))
    R, w = 150, 64
    for i, (a0, a1) in enumerate(starts()):
        t = seg_time(i)
        comp.layer(f"seg{i}", [group([arc_path(R, a0 + 1.2, a1 - 1.2, C), trim(end=keys((t, 0, EXPO_OUT),
                                                                                         (t + 22, 100))),
                                      stroke(slot=SEG[i], width=w, cap="butt")], "seg")],
                   parent=rg, ip=t)
    comp.layer("inner", [group([ellipse((2 * R - w - 18, 2 * R - w - 18), C), fill(slot="background", opacity=6)],
                               "disc")], parent=rg, opacity=fade(4, 14))
    comp.layer("track", [group([ellipse((2 * R, 2 * R), C), stroke(slot="background", width=w, opacity=10)], "t")],
               parent=rg, opacity=fade(0, 8))
    return comp


def neon():
    """Dark panel; thin glowing arcs trace the four segments around a dashed inner ring."""
    comp = Comp("donut-chart--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, *SEG, "background", "outline")
    legend(comp, "neon")
    R = 146
    for i, (a0, a1) in enumerate(starts()):
        t = seg_time(i)
        comp.layer(f"seg{i}", glow_strokes([arc_path(R, a0 + 4, a1 - 4, C)], slot=SEG[i], width=16,
                                           widths=(40, 26), ops=(8, 18),
                                           extra=[trim(end=keys((t, 0, EXPO_OUT), (t + 24, 100)))]), ip=t)
    comp.layer("inner", [group([ellipse((2 * R - 60, 2 * R - 60), C),
                                stroke(slot="outline", width=2, dashes=[4, 10], opacity=45)], "d")],
               anchor=C, position=C, rotation=keys((0, -90, EXPO_OUT), (50, 0)), opacity=fade(4, 14))
    comp.layer("track", [group([ellipse((2 * R, 2 * R), C), stroke(slot="outline", width=16, opacity=8)], "t")],
               opacity=fade(2, 10))
    neon_panel(comp, 14, 14, W - 28, H - 28, r=36)
    return comp


def solid3d():
    """Tilted, extruded donut; the segments sweep in and the largest slice lifts out of the ring."""
    comp = Comp("donut-chart--3d", W, H, fps=30, frames=F)
    slots(comp, FLAT, *SEG)
    legend(comp, "3d")
    c3 = (C[0], C[1] - 12)
    tilt = rig(comp, "tilt", c3, scale=keys((0, [70, 40], SOFT_SPRING), (20, [100, 56])),
               rotation=0)
    R, w, depth, step = 150, 84, 54, 4.5
    for i, (a0, a1) in enumerate(starts()):
        t = seg_time(i)
        tr = trim(end=keys((t, 0, EXPO_OUT), (t + 22, 100)))
        a = arc_path(R, a0 + 0.8, a1 - 0.8, c3)
        items = [group([a, tr, stroke("#FFFFFF", width=w, cap="butt", opacity=10),
                        stroke(slot=SEG[i], width=w, cap="butt")], "top")]
        k = step
        while k <= depth:
            items.append(group([a, tr, stroke("#000000", width=w, cap="butt", opacity=30),
                                stroke(slot=SEG[i], width=w, cap="butt")], f"side{int(k)}", position=(0, k)))
            k += step
        m = (a0 + a1) / 2
        lift = 22 if i == 0 else 0
        off = keys((t + 26, [0, 0], SPRING), (t + 40, [lift * math.cos(math.radians(m)),
                                                       lift * math.sin(math.radians(m))])) if lift else None
        lay(comp, f"seg{i}", items, (0, 0), off=off, parent=tilt, ip=t)
    comp.layer("shadow", [group([ellipse((2 * R + w + 40, 2 * R + w + 40), (c3[0], c3[1] + depth + 30)),
                                 gradient_fill([(0, "#000000", 0.35), (0.7, "#000000", 0.15), (1, "#000000", 0)],
                                               (c3[0], c3[1] + depth + 30), (c3[0] + R + w / 2 + 20, c3[1] + depth + 30),
                                               radial=True)], "s")],
               parent=tilt, opacity=fade(0, 14))
    return comp


build_asset(CAT, "donut-chart", "Donut Chart",
            "A four-part donut chart whose segments sweep in one after another, with a colour-keyed legend. "
            "Put a total in the centre 'value' area and each segment's name in 'label1'-'label4'.",
            ["donut", "pie", "chart", "percent", "share", "legend", "infographic", "data"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=areas()["value"], text_areas=areas(), thumb_t=0.95,
      description="Thick donut with gaps between segments; legend dots pop as each segment lands."),
    V("neon", "Neon", neon(), "intro-hold", text_area=areas()["value"], text_areas=areas(), thumb_t=0.95,
      description="Dark panel with thin glowing arcs, tick marks and a dashed inner ring."),
    V("3d", "3D Tilted", solid3d(), "intro-hold", text_area=areas(False)["label1"], text_areas=areas(False),
      thumb_t=0.95, description="Tilted, extruded pie ring; the largest slice lifts out. The centre is left open "
                                "(no value area); labels sit beside cube-shaped keys."),
])
