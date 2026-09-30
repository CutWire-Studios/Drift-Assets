from _common import *

W, H, F = 520, 600, 120
C = (W / 2, 262)
R = 206
HOUR_A, MIN_A = -60 + 0, 60      # 10:10 pose (degrees from 12 o'clock)


def hand(c, length, width, back=0, cap="round"):
    return polyline([(c[0], c[1] + back), (c[0], c[1] - length)])


def tick_rot():
    """Second hand: 12 springy ticks of 30 degrees over the loop."""
    step = F / 12
    out = [(0, 0, HOLD)]
    for i in range(12):
        t0 = round(i * step + step - 5)
        out += [(t0, i * 30, (0.3, 1.9, 0.5, 1.0)), (t0 + 5, (i + 1) * 30, HOLD)]
    if out[-1][0] != F:
        out.append((F, 360, HOLD))
    return anim(out)


def dial_ticks(r0, long=26, short=12, n=60):
    majors, minors = [], []
    for k in range(n):
        a = -90 + k * 360 / n
        if k % (n // 12) == 0:
            majors.append(polyline([pt(C, r0, a), pt(C, r0 - long, a)]))
        else:
            minors.append(polyline([pt(C, r0, a), pt(C, r0 - short, a)]))
    return majors, minors


def areas():
    return {"label": (W / 2 - 200, H - 90, 400, 60)}


def flat():
    """Classic wall clock: the red second hand ticks round in springy steps."""
    comp = Comp("clock-tick", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FF4D5E", "background": "#FFFFFF", "outline": "#1F2233", "secondary": "#5B6CFF"},
          "primary", "secondary", "background", "outline")
    comp.layer("cap", [group([ellipse((10, 10), C), fill("#FFFFFF")], "d"),
                       group([ellipse((26, 26), C), fill(slot="primary")], "c")])
    comp.layer("second", [group([hand(C, R - 30, 4, 40), stroke(slot="primary", width=4)], "h"),
                          group([ellipse((18, 18), (C[0], C[1] + 44)), fill(slot="primary")], "tail")],
               anchor=C, position=C, rotation=tick_rot())
    comp.layer("minute", [group([hand(C, R - 44, 12, 18), stroke(slot="outline", width=12)], "h")],
               anchor=C, position=C, rotation=MIN_A)
    comp.layer("hour", [group([hand(C, R - 96, 16, 16), stroke(slot="outline", width=16)], "h")],
               anchor=C, position=C, rotation=HOUR_A)
    comp.layer("hand-shadow", [group([hand(C, R - 44, 12, 18), stroke("#000000", width=12, opacity=14)], "m",
                                     rotation=MIN_A, anchor=C, position=C),
                               group([hand(C, R - 96, 16, 16), stroke("#000000", width=16, opacity=14)], "h",
                                     rotation=HOUR_A, anchor=C, position=C)], position=(4, 8))
    majors, minors = dial_ticks(R - 26)
    comp.layer("ticks", [group(majors + [stroke(slot="outline", width=7, cap="butt")], "maj"),
                         group(minors + [stroke(slot="outline", width=2.5, opacity=45, cap="butt")], "min")])
    comp.layer("face", [group([ellipse((2 * R - 26, 2 * R - 26), C), gradient_fill(
                            [(0, "#000000", 0), (0.8, "#000000", 0), (1, "#000000", 0.1)], C, (C[0] + R, C[1]),
                            radial=True)], "vig"),
                        group([ellipse((2 * R - 26, 2 * R - 26), C), fill(slot="background")], "f"),
                        group([ellipse((2 * R, 2 * R), C), fill(slot="secondary")], "rim"),
                        group([ellipse((2 * R, 2 * R), (C[0], C[1] + 12)), fill("#000000", 24)], "sh")])
    return comp


def neon():
    """Dark panel; glowing dial ring and a second hand sweeping smoothly with a comet trail."""
    comp = Comp("clock-tick--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#FF3DCB", "outline": "#23E5FF"}, "primary", "background", "outline")
    trail = []
    for k, (a0, op) in enumerate(((-150, 10), (-120, 22), (-104, 40))):
        trail.append(group([arc_path(R - 44, a0, -90, C), stroke(slot="primary", width=10, opacity=op, cap="butt")],
                           f"trail{k}"))
    sweep = anim([(0, 0, LINEAR), (F, 360)])
    comp.layer("cap", soft_glow([ellipse((20, 20), C)], slot="primary", spread=(12, 26), ops=(30, 12)))
    comp.layer("second", glow_strokes([hand(C, R - 34, 4, 30)], slot="primary", width=4, widths=(20, 12),
                                      ops=(10, 20)) + trail,
               anchor=C, position=C, rotation=sweep)
    comp.layer("minute", glow_strokes([hand(C, R - 56, 6, 0)], slot="outline", width=6, widths=(22,), ops=(14,)),
               anchor=C, position=C, rotation=MIN_A)
    comp.layer("hour", glow_strokes([hand(C, R - 104, 8, 0)], slot="outline", width=8, widths=(22,), ops=(14,)),
               anchor=C, position=C, rotation=HOUR_A)
    majors, minors = dial_ticks(R - 18, 22, 8)
    comp.layer("ticks", glow_strokes(majors, slot="outline", width=4, core=False, widths=(16,), ops=(16,), cap="butt")
               + [group(minors + [stroke(slot="outline", width=2, opacity=40, cap="butt")], "min")])
    comp.layer("ring", glow_strokes([ellipse((2 * R, 2 * R), C)], slot="outline", width=4, widths=(28, 14),
                                    ops=(8, 18)))
    comp.layer("orbit", [group([ellipse((2 * R + 30, 2 * R + 30), C), stroke(slot="primary", width=2,
                                                                          dashes=[30, 20, 4, 20], opacity=45)], "d")],
               anchor=C, position=C, rotation=anim([(0, 0, LINEAR), (F, -90)]))
    neon_panel(comp, 16, 16, W - 32, H - 32, r=36)
    return comp


def sketch():
    """Paper card with a hand-drawn clock; the minute hand whizzes round in a time-lapse with motion arcs."""
    comp = Comp("clock-tick--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "background", "outline", "accent")
    paper = Paper(comp, 20, 20, W - 40, H - 40, tilt=-1.0, r=18, t0=-30)
    card = paper.rig
    e = (0.55, 0.0, 0.45, 1.0)
    spin = anim([(0, 0, e), (F / 2, 180, e), (F, 360)])
    comp.layer("cap", [group([ellipse((20, 20), C), fill(slot="outline")], "c")], parent=card)
    arcs = [group([sk_path(catmull([pt(C, R - 70 - k * 18, -90 - a) for a in range(8, 70, 10)], 3)),
                   stroke(slot="primary", width=4, opacity=70 - k * 20)], f"arc{k}") for k in range(2)]
    comp.layer("minute", [ink([wobble([(C[0], C[1] + 14), (C[0], C[1] - R + 60)], 1.0, 4, step=30)], width=8,
                              slot="primary", color="#FF5A4E")] + arcs,
               parent=card, anchor=C, position=C, rotation=spin)
    comp.layer("hour", [ink([wobble([(C[0], C[1] + 10), (C[0], C[1] - R + 110)], 1.0, 2, step=30)], width=11)],
               parent=card, anchor=C, position=C, rotation=HOUR_A)
    majors = [wobble([pt(C, R - 30, -90 + k * 30), pt(C, R - 52, -90 + k * 30)], 1.0, k, step=10) for k in range(12)]
    comp.layer("ticks", [ink(majors, width=5)], parent=card)
    comp.layer("face", [ink([sketch_circle_pts(C, R - 6, seed=2, amp=0.012, turns=1.06)], width=6),
                        ink([sketch_circle_pts(C, R - 14, seed=5, amp=0.012, turns=1.02, a0=-40)], width=2,
                            opacity=40, name="ghost"),
                        group([ellipse((2 * R - 12, 2 * R - 12), C), fill(slot="accent", opacity=30)], "wash")],
               parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "clock-tick", "Clock Tick",
            "Looping analog clock with a moving hand. Put a caption such as a time, deadline or duration in the "
            "'label' area under the clock.",
            ["clock", "time", "watch", "timer", "deadline", "schedule", "hours", "loop"], [
    V("flat", "Wall Clock", flat(), "loop", text_area=A["label"], text_areas=A, thumb_t=0.2,
      description="Classic wall clock; the red second hand ticks round in springy steps."),
    V("neon", "Neon", neon(), "loop", text_area=A["label"], text_areas=A, thumb_t=0.2,
      description="Dark panel with a glowing dial; the second hand sweeps smoothly with a comet trail."),
    V("sketch", "Sketch Time-lapse", sketch(), "loop", text_area=A["label"], text_areas=A, thumb_t=0.3,
      description="Paper card with a hand-drawn clock; the minute hand whizzes round with motion arcs."),
])
