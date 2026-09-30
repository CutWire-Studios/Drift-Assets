from _common import *

W, H, F = 900, 240, 75
X0, BW, CY, BH = 60, 780, 160, 48
V70 = 0.7
T0, T1 = 8, 46


def areas(y=34):
    return {"label": (X0, y, 500, 64), "value": (X0 + BW - 220, y, 220, 64)}


def grow(x, cy, wf, h, t0, t1, e=EXPO_OUT, r=None):
    r = h / 2 if r is None else r
    size = keys((t0, [h, h], e), (t1, [wf, h]))
    pos = keys((t0, [x + h / 2, cy], e), (t1, [x + wf / 2, cy]))
    return rect(size, pos, r)


def flat():
    """Soft track, primary fill easing to 70% with a glowing leading edge and a glint sweep."""
    comp = Comp("progress-bar", W, H, fps=30, frames=F)
    slots(comp, FLAT, "primary", "background")
    wf = BW * V70
    # leading edge glow + spark
    edge = keys((T0, [X0 + BH / 2, CY], EXPO_OUT), (T1, [X0 + wf - BH / 2, CY]))
    spark(comp, (X0 + wf - BH / 2 + 4, CY - 2), T1 - 4, size=58, name="edge-spark")
    comp.layer("edge", [group([ellipse((BH * 0.5, BH * 0.5)), fill("#FFFFFF", 95)], "core"),
                        group([ellipse((BH * 1.8, BH * 1.8)),
                               gradient_fill([(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)], (0, 0), (BH * 0.9, 0),
                                             radial=True)], "halo")],
               position=edge, opacity=keys((T0, 0, EASE_OUT), (T0 + 4, 100, HOLD), (T1 + 6, 100, EASE_IN),
                                            (T1 + 22, 55)),
               scale=keys((T0, [60, 60], EASE_OUT), (T1 - 2, [100, 100], EASE_OUT), (T1 + 4, [150, 150], EASE_IN_OUT),
                          (T1 + 18, [100, 100])))
    glint_band(comp, [group([grow(X0, CY, wf, BH, T0, T1), fill()], "m")], X0 - 60, X0 + wf + 60, CY, BH,
               T1 + 4, T1 + 24, width=46, opacity=60)
    comp.layer("fill-sheen", [group([grow(X0, CY, wf, BH, T0, T1),
                                     gradient_fill([(0, "#FFFFFF", 0.28), (0.55, "#FFFFFF", 0), (1, "#000000", 0.12)],
                                                   (0, CY - BH / 2), (0, CY + BH / 2))], "sheen")],
               opacity=fade(T0, T0 + 3))
    comp.layer("fill", [group([grow(X0, CY, wf, BH, T0, T1), fill(slot="primary")], "fill"),
                        group([grow(X0, CY + 5, wf, BH, T0, T1), fill(slot="primary", opacity=30)], "drop")],
               opacity=fade(T0, T0 + 3))
    # quarter ticks under the bar
    ticks = [polyline([(X0 + BW * q, CY + BH / 2 + 12), (X0 + BW * q, CY + BH / 2 + 22)]) for q in (0.25, 0.5, 0.75)]
    comp.layer("ticks", [group(ticks + [stroke(slot="background", width=3, opacity=55)], "t")],
               opacity=fade(4, 14))
    comp.layer("track", [group([rect((BW, BH), (X0 + BW / 2, CY), BH / 2), fill(slot="background", opacity=16)], "t"),
                         group([rect((BW, BH), (X0 + BW / 2, CY), BH / 2), stroke(slot="background", width=2,
                                                                                    opacity=22)], "e")],
               anchor=(X0, CY), position=(X0, CY), scale=keys((0, [8, 100], EXPO_OUT), (16, [100, 100])),
               opacity=fade(0, 4))
    return comp


def neon():
    """Dark panel, twenty glowing segments light up in turn behind a white-hot spark."""
    comp = Comp("progress-bar--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, "primary", "background", "outline")
    n, lit = 20, 14
    gap = 8
    sw = (BW - gap * (n - 1)) / n
    sh = BH - 10
    t0, t1 = T0 + 4, T1 + 6
    spark_x = []
    for i in range(lit):
        f = first_frame(EXPO_OUT, t0, t1, (i + 1) / lit)
        x = X0 + i * (sw + gap)
        spark_x.append(x + sw)
        seg = rect((sw, sh), (x + sw / 2, CY), 5)
        comp.layer(f"flash{i}", [group([seg, fill("#FFFFFF")], "f")], ip=f, op=f + 7,
                   opacity=keys((f, 90, EASE_IN), (f + 6, 0)))
        comp.layer(f"seg{i}", soft_glow([seg], slot="primary", spread=(10, 22), ops=(28, 10)),
                   opacity=keys((f - 1, 0, EASE_OUT), (f, 100)), ip=f - 1)
    for i in range(n):
        x = X0 + i * (sw + gap)
        comp.layer(f"slot{i}", [group([rect((sw, sh), (x + sw / 2, CY), 5), fill(slot="primary", opacity=10)], "s")],
                   opacity=fade(2 + i // 2, 8 + i // 2))
    head = keys((t0, [X0 + 4, CY], EXPO_OUT), (t1, [spark_x[-1] + gap / 2, CY]))
    comp.layer("head", [group([ellipse((10, BH + 14)), fill("#FFFFFF")], "core"),
                        group([ellipse((26, BH + 30)), fill(slot="primary", opacity=45)], "g1"),
                        group([ellipse((60, BH + 60)), fill(slot="primary", opacity=14)], "g2")],
               position=head, opacity=keys((t0 - 2, 0, EASE_OUT), (t0 + 2, 100, HOLD), (t1, 100, EASE_IN_OUT),
                                           (t1 + 20, 0, HOLD), (t1 + 26, 0, EASE_IN_OUT), (t1 + 40, 70)),
               scale=keys((t1 - 2, [100, 100], EASE_OUT), (t1 + 4, [140, 120], EASE_IN), (t1 + 20, [60, 60])))
    comp.layer("frame", glow_strokes([rect((BW + 26, BH + 22), (X0 + BW / 2, CY), (BH + 22) / 2)], slot="primary",
                                     width=3, core=False, widths=(18, 9), ops=(6, 14),
                                     extra=[trim(end=keys((0, 0, EASE_IN_OUT), (22, 100)))]))
    neon_panel(comp, 20, 14, W - 40, H - 28, t0=0, r=30)
    return comp


def sketch():
    """Paper card with a hand-drawn bar; a marker scribble fills it and an ink arrow marks the spot."""
    comp = Comp("progress-bar--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "background", "outline")
    paper = Paper(comp, 22, 14, W - 44, H - 28, t0=0, tilt=-0.8)
    card = paper.rig
    wf = BW * V70
    tx = X0 + wf
    # arrow pointing at the fill end
    a0, a1 = (tx + 44, CY - 96), (tx + 3, CY - 34)
    comp.layer("arrow", [ink([wobble([a0, (tx + 30, CY - 58), a1], 1.0, 3), arrow_head(a1, (tx + 14, CY - 52), 18)],
                             width=4.5, draw=(T1 + 6, T1 + 18))], parent=card)
    comp.layer("outline", [ink([sketch_rect_pts(X0, CY - BH / 2, BW, BH, seed=5)], width=INK_W, draw=(4, 26)),
                           ink([sketch_rect_pts(X0 + 2, CY - BH / 2 + 1, BW - 3, BH - 1, seed=9, amp=2.6)],
                               width=2, opacity=45, draw=(8, 28), name="ink2")], parent=card)
    ticks = [sketch_line_pts((X0 + BW * q, CY + BH / 2 + 12), (X0 + BW * q + 1, CY + BH / 2 + 24), seed=q * 10)
             for q in (0.25, 0.5, 0.75)]
    comp.layer("ticks", [ink(ticks, width=3.5, draw=(20, 30))], parent=card)
    comp.layer("scribble", [marker(scribble_pts(X0 + 8, CY - BH / 2 + 6, wf - 12, BH - 12, spacing=13, seed=2),
                                   19, draw=(T0 + 12, T1 + 4, EASE_IN_OUT))], parent=card)
    paper.sheet()
    return comp


build_asset(CAT, "progress-bar", "Progress Bar",
            "A progress bar that fills to about 70% with a glinting leading edge. Put the label in the "
            "'label' area and the percentage in the 'value' area above the bar.",
            ["progress", "bar", "percent", "loading", "infographic", "stat", "goal"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=areas()["label"], text_areas=areas(), thumb_t=0.95,
      description="Soft rounded track; the fill eases in with a glowing leading edge and a glint sweep."),
    V("neon", "Neon Segments", neon(), "intro-hold", text_area=areas()["label"], text_areas=areas(), thumb_t=0.95,
      description="Dark glass panel; twenty glowing segments light up behind a white-hot spark."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=areas(40)["label"], text_areas=areas(40), thumb_t=0.95,
      description="Paper card with a hand-drawn bar, marker scribble fill and an ink arrow at the end."),
])
