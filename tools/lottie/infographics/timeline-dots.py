from _common import *

W, H, F = 1100, 380, 90
CY = 186
XA, XB = 70, 1030
XS = [190 + i * 240 for i in range(4)]
T0, T1 = 6, 60
E = (0.4, 0.0, 0.4, 1.0)
DOT_SLOTS = ("primary", "secondary", "accent", "icon")


def reach(x):
    return first_frame(E, T0, T1, (x - XA) / (XB - XA))


def head_x():
    return anim([(f, [XA + (XB - XA) * ease_eval(E, (f - T0) / (T1 - T0)), CY], LINEAR) for f in range(T0, T1 + 1)])


def areas():
    d = {}
    for i, x in enumerate(XS):
        d[f"date{i + 1}"] = (x - 90, 62, 180, 52)
        d[f"label{i + 1}"] = (x - 100, 248, 200, 80)
    return d


def line_trim():
    return trim(end=keys((T0, 0, E), (T1, 100)))


def flat():
    """Line draws across; ringed milestone dots spring up in sequence with a ripple, the last one pulses."""
    comp = Comp("timeline-dots", W, H, fps=30, frames=F)
    slots(comp, FLAT, "primary", "background")
    for i, x in enumerate(XS):
        t = reach(x)
        c = (x, CY)
        ring_pulse(comp, c, t + 2, 22, 54, slot="primary", width=4, name=f"ripple{i}")
        if i == len(XS) - 1:
            for k in range(2):
                tt = t + 20 + k * 30
                ring_pulse(comp, c, tt, 22, 48, slot="primary", width=3, dur=24, name=f"pulse{k}")
        comp.layer(f"dot{i}", [group([ellipse((18, 18), c), fill(slot="background")], "core"),
                               group([ellipse((44, 44), c), fill(slot="primary")], "ring")],
                   anchor=c, position=c, scale=keys((t, [0, 0], SPRING), (t + 14, [100, 100])), ip=t)
        comp.layer(f"card{i}", [group([rect_tl(x - 110, 240, 220, 96, 18), fill(slot="background", opacity=10)], "c"),
                                group([rect_tl(x - 110, 240, 220, 96, 18), stroke(slot="background", width=2,
                                                                                  opacity=16)], "e")],
                   anchor=(x, 240), position=(x, 240), scale=keys((t + 6, [60, 0], EXPO_OUT), (t + 20, [100, 100])),
                   opacity=fade(t + 6, t + 10), ip=t + 6)
        comp.layer(f"pill{i}", [group([rect_tl(x - 90, 62, 180, 52, 26), fill(slot="primary", opacity=24)], "p")],
                   anchor=(x, 114), position=(x, 114), scale=keys((t + 8, [60, 0], EXPO_OUT), (t + 22, [100, 100])),
                   opacity=fade(t + 8, t + 12), ip=t + 8)
        comp.layer(f"stem{i}", [group([polyline([(x, CY + 30), (x, CY + 50)]), stroke(slot="primary", width=4)], "s"),
                                group([polyline([(x, CY - 30), (x, CY - 50)]), stroke(slot="primary", width=4)], "s2")],
                   anchor=c, position=c, scale=keys((t + 4, [100, 0], EXPO_OUT), (t + 16, [100, 100])), ip=t + 4)
    comp.layer("line", [group([polyline([(XA, CY), (XB, CY)]), line_trim(), stroke(slot="primary", width=8)], "l")])
    comp.layer("track", [group([polyline([(XA, CY), (XB, CY)]), trim(end=keys((0, 0, EXPO_OUT), (20, 100))),
                                stroke(slot="background", width=8, opacity=16)], "t")])
    return comp


def neon():
    """Dark panel; a spark races along a neon line and each milestone ring flares as it passes."""
    comp = Comp("timeline-dots--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, "primary", "secondary", "background", "outline")
    comp.layer("head", [group([ellipse((16, 16)), fill("#FFFFFF")], "c"),
                        group([ellipse((46, 46)), fill(slot="primary", opacity=30)], "g"),
                        group([rect((120, 6), (-60, 0), 3),
                               gradient_fill([(0, "#FFFFFF", 0), (1, "#FFFFFF", 0.8)], (-120, 0), (0, 0))], "trail")],
               position=head_x(), ip=T0, op=T1 + 1, opacity=keys((T1 - 6, 100, EASE_IN), (T1, 0)))
    for i, x in enumerate(XS):
        t = reach(x)
        c = (x, CY)
        s = "secondary" if i == len(XS) - 1 else "primary"
        ring_pulse(comp, c, t, 20, 64, slot=s, width=3, dur=16, name=f"flare{i}")
        comp.layer(f"core{i}", soft_glow([ellipse((14, 14), c)], slot=s, spread=(12, 24), ops=(30, 12)),
                   anchor=c, position=c, scale=keys((t + 2, [0, 0], SPRING), (t + 14, [100, 100])), ip=t + 2)
        comp.layer(f"ring{i}", glow_strokes([ellipse((40, 40), c)], slot=s, width=4, widths=(20, 12), ops=(10, 20))
                   + [group([ellipse((40, 40), c), fill(slot="background")], "bg")],
                   anchor=c, position=c, scale=keys((t, [40, 40], SPRING), (t + 12, [100, 100])),
                   opacity=keys((t, 0, HOLD), (t + 1, 100, HOLD), (t + 3, 30, HOLD), (t + 5, 100)), ip=t)
        comp.layer(f"card{i}", glow_strokes([rect_tl(x - 108, 244, 216, 88, 10)], slot=s, width=2, core=False,
                                            widths=(12,), ops=(10,),
                                            extra=[trim(end=keys((t + 4, 0, EASE_IN_OUT), (t + 22, 100)))])
                   + [group([rect_tl(x - 108, 244, 216, 88, 10), fill(slot=s, opacity=6)], "f")], ip=t + 4)
        comp.layer(f"tick{i}", [group([polyline([(x, CY - 34), (x, CY - 52)]), polyline([(x, CY + 34), (x, CY + 52)]),
                                       stroke(slot="outline", width=2, opacity=60)], "t")], opacity=fade(t, t + 8))
    comp.layer("line", glow_strokes([polyline([(XA, CY), (XB, CY)])], slot="primary", width=4, widths=(22, 12),
                                    ops=(8, 18), extra=[line_trim()]))
    comp.layer("track", [group([polyline([(XA, CY), (XB, CY)]), stroke(slot="outline", width=2, opacity=25,
                                                                         dashes=[6, 10])], "t")], opacity=fade(0, 10))
    neon_panel(comp, 16, 16, W - 32, H - 32, r=32)
    return comp


def sketch():
    """Paper strip: an ink arrow scrawls across, milestones get circled and coloured in, a flag on the last."""
    comp = Comp("timeline-dots--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, *DOT_SLOTS, "background", "outline")
    paper = Paper(comp, 24, 22, W - 48, H - 44, tilt=-0.6, r=14)
    card = paper.rig
    last = XS[-1]
    tf = reach(last) + 10
    flag = [wobble([(last, CY - 22), (last + 2, CY - 92)], 0.8, 3, step=20)]
    comp.layer("flag", [ink(flag, width=4, draw=(tf, tf + 6)),
                        group([polyline([(last + 2, CY - 92), (last + 50, CY - 80), (last + 2, CY - 66)], closed=True),
                               fill(slot="primary")], "cloth")],
               parent=card, anchor=(last, CY - 92), position=(last, CY - 92),
               scale=keys((tf, [0, 0], SPRING), (tf + 12, [100, 100])), ip=tf)
    for i, x in enumerate(XS):
        t = reach(x)
        c = (x, CY)
        comp.layer(f"circle{i}", [ink([sketch_circle_pts(c, 22, seed=i, amp=0.05, turns=1.12, n=16)], width=4.5,
                                      draw=(t, t + 8))], parent=card, ip=t)
        comp.layer(f"fill{i}", [group([ellipse((40, 40), c), fill(slot=DOT_SLOTS[i])], "f")], parent=card,
                   anchor=c, position=c, scale=keys((t + 4, [0, 0], SPRING), (t + 14, [100, 100])), ip=t + 4)
    ln = wobble([(XA, CY), (XB, CY)], 1.6, 7, step=60)
    comp.layer("line", [ink([ln, arrow_head((XB, CY), (XB - 20, CY), 18)], width=5, draw=(T0, T1, E))], parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "timeline-dots", "Timeline Dots",
            "Horizontal timeline whose line draws across and four milestone dots pop in sequence. Put the dates "
            "in 'date1'-'date4' above the dots and the milestone names in 'label1'-'label4' below.",
            ["timeline", "milestones", "roadmap", "history", "steps", "dates", "infographic", "process"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Line draws across; ringed milestone dots spring up with ripples and the last one pulses."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Dark panel; a spark races along the neon line and each milestone ring flares as it passes."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Paper strip with an ink arrow, circled milestones coloured in and a flag on the last one."),
])
