from _common import *

S, F = 520, 75
C = (S / 2, S / 2)
R = 176
V70 = 0.7
T0, T1 = 8, 50
END = -90 + 360 * V70


def areas():
    return {"value": (C[0] - 110, C[1] - 62, 220, 92), "label": (C[0] - 100, C[1] + 38, 200, 40)}


def head_rot(t0=T0, t1=T1, e=EXPO_OUT):
    return keys((t0, 0, e), (t1, 360 * V70))


def flat():
    """Thick rounded ring sweeping to 70% with a bright head dot; the centre stays clear for the value."""
    comp = Comp("radial-progress", S, S, fps=30, frames=F)
    slots(comp, FLAT, "primary", "background")
    rg = rig(comp, "ring", C, scale=keys((0, [70, 70], SOFT_SPRING), (18, [100, 100])))
    spark(comp, pt(C, R, END), T1 - 3, size=64, parent=None)
    comp.layer("head", [group([ellipse((16, 16), pt(C, R, -90)), fill("#FFFFFF")], "dot"),
                        group([ellipse((52, 52), pt(C, R, -90)),
                               gradient_fill([(0, "#FFFFFF", 0.5), (1, "#FFFFFF", 0)], pt(C, R, -90),
                                             pt(C, R + 26, -90), radial=True)], "halo")],
               anchor=C, position=C, parent=rg, rotation=head_rot(), opacity=fade(T0, T0 + 4))
    arcs = [arc_path(R, -90, 270, C)]
    comp.layer("arc", [group(arcs + [trim(end=keys((T0, 0, EXPO_OUT), (T1, 100 * V70))),
                                     stroke(slot="primary", width=36)], "arc"),
                       group(arcs + [trim(end=keys((T0, 0, EXPO_OUT), (T1, 100 * V70))),
                                     stroke(slot="primary", width=56, opacity=16)], "halo")],
               parent=rg, opacity=fade(T0, T0 + 2))
    comp.layer("inner", [group([ellipse((R * 2 - 70, R * 2 - 70), C), stroke(slot="background", width=2,
                                                                           opacity=22)], "inner")],
               parent=rg, opacity=fade(6, 16))
    comp.layer("track", [group([ellipse((R * 2, R * 2), C), stroke(slot="background", width=36, opacity=14)], "t")],
               parent=rg, opacity=fade(0, 6))
    return comp


def neon():
    """Dark panel with a ring of tick marks that light up in a glowing sweep; a dashed halo turns slowly."""
    comp = Comp("radial-progress--neon", S, S, fps=30, frames=F)
    slots(comp, NEON, "primary", "secondary", "background", "outline")
    circ = 2 * math.pi * R
    n = 60
    dash = [circ / n * 0.42, circ / n * 0.58]
    ring = [arc_path(R, -90, 270, C)]
    tr = trim(end=keys((T0, 0, EXPO_OUT), (T1, 100 * V70)))
    comp.layer("head", [group([ellipse((14, 22), pt(C, R, -90)), fill("#FFFFFF")], "core"),
                        group([ellipse((34, 56), pt(C, R, -90)), fill(slot="primary", opacity=40)], "g1"),
                        group([ellipse((70, 90), pt(C, R, -90)), fill(slot="primary", opacity=12)], "g2")],
               anchor=C, position=C, rotation=head_rot(), opacity=fade(T0, T0 + 4))
    comp.layer("lit", [group(ring + [tr, stroke("#FFFFFF", width=22, cap="butt", dashes=dash, opacity=60)], "core"),
                       group(ring + [tr, stroke(slot="primary", width=30, cap="butt", dashes=dash)], "tick"),
                       group(ring + [tr, stroke(slot="primary", width=54, opacity=14)], "glow")])
    comp.layer("inner-arc", glow_strokes([arc_path(R - 34, -90, 270, C)], slot="secondary", width=3, core=False,
                                         widths=(16,), ops=(18,),
                                         extra=[trim(end=keys((T0 + 6, 0, EXPO_OUT), (T1 + 8, 100 * V70)))]))
    comp.layer("ticks", [group(ring + [stroke(slot="primary", width=30, cap="butt", dashes=dash, opacity=14)], "t")],
               anchor=C, position=C, opacity=fade(2, 10), rotation=keys((2, -30, EXPO_OUT), (22, 0)))
    comp.layer("halo", [group([ellipse((2 * R + 70, 2 * R + 70), C),
                               stroke(slot="outline", width=2, dashes=[40, 16, 6, 16], opacity=40)], "d")],
                anchor=C, position=C, opacity=fade(4, 16), rotation=keys((0, -60, LINEAR), (F, 30)))
    neon_panel(comp, 14, 14, S - 28, S - 28, r=46)
    return comp


def sketch():
    """Paper card, hand-drawn double circle and a thick marker arc looping round to 70%."""
    comp = Comp("radial-progress--sketch", S, S, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "background", "outline")
    paper = Paper(comp, 18, 18, S - 36, S - 36, tilt=1.2, r=26)
    card = paper.rig
    comp.layer("outline", [ink([sketch_circle_pts(C, R + 22, seed=4, turns=1.05, amp=0.012)], draw=(2, 24)),
                           ink([sketch_circle_pts(C, R - 22, seed=7, turns=1.04, a0=-80, amp=0.012)], width=3, draw=(6, 26),
                               name="inner"),
                           ink([sketch_circle_pts(C, R + 26, seed=11, turns=1.02, a0=-120, amp=0.012)], width=2, opacity=40,
                               draw=(8, 28), name="ghost")], parent=card)
    rnd = random.Random(5)
    m = 40
    pts = [pt(C, R + rnd.uniform(-3, 3), -92 + (360 * V70 + 4) * i / m) for i in range(m + 1)]
    comp.layer("marker", [marker(catmull(pts, 4), 36, draw=(T0 + 6, T1 + 4, EASE_IN_OUT), opacity=90)], parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "radial-progress", "Radial Progress",
            "A progress ring that sweeps to about 70%. Put the percentage in the 'value' area in the centre "
            "and a short caption in the 'label' area under it.",
            ["progress", "ring", "radial", "circle", "percent", "gauge", "infographic", "stat"], [
    V("flat", "Flat Ring", flat(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Thick rounded ring sweeping to 70% with a bright head dot and a sparkle."),
    V("neon", "Neon Ticks", neon(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Dark panel; a ring of tick marks lights up in a glowing sweep with an inner arc and dashed halo."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Paper card with a hand-drawn double circle and a thick marker arc looping to 70%."),
])
