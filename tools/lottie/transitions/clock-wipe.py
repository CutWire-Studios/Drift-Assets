from _common import *

R = 610  # stroke radius; a stroke 2R wide fills the disc out to 2R (> the corner distance)


def sweep(comp, slot, tm, ease=SMOOTH, start_angle=0, name="sweep"):
    """Pie that sweeps clockwise round the centre to cover, then keeps going to uncover."""
    a0, a1, b0, b1 = tm
    comp.layer(name, [group([ellipse((2 * R, 2 * R)), stroke(slot=slot, width=2 * R + 4, cap="butt"),
                             trim(end=anim([(a0, 0, ease), (a1, 100)]), start=anim([(b0, 0, ease), (b1, 100)]))],
                            "pie", rotation=start_angle)], position=C)
    # a solid disc while the pie is closed hides the hairline where the stroke's two ends meet
    comp.layer(name + "-hold", [group([ellipse((4 * R, 4 * R)), fill(slot=slot)], "disc")], position=C,
               ip=a1, op=b0 + 1)


def flat():
    t = Timing(15, 10, 15)
    comp = base("clock-wipe", t, "ocean", ("primary",))
    sweep(comp, "primary", t.tm)
    return comp, t


def stacked():
    t = Timing(16, 10, 16)
    comp = base("clock-wipe--stacked", t, "ocean", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        sweep(comp, s, tm, name=s)
    return comp, t


def radar():
    """A clock hand leads the sweep in and drags it out, with a pivot dot; snappy tick-like timing."""
    t = Timing(14, 8, 14)
    comp = base("clock-wipe--hand", t, "mint", ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    ease = SNAPPY
    hand = [rect((26, 1400), position=(0, -700 + 60), roundness=13), fill(slot="accent")]
    dot = [ellipse((74, 74)), fill(slot="accent"), stroke(slot="primary", width=12)]
    for k, (t0, t1) in enumerate(((a0, a1), (b0, b1))):
        comp.layer(f"pivot{k}", [group(dot, "dot")], position=C, ip=max(t0, 1), op=t1,
                   scale=anim([(t0, [0, 0], OVERSHOOT), (t0 + 4, [100, 100], LINEAR), (t1 - 3, [100, 100], EASE_IN),
                               (t1, [0, 0])]))
        comp.layer(f"hand{k}", [group(hand, "hand")], position=C, ip=max(t0, 1), op=t1,
                   rotation=anim([(t0, 0, ease), (t1, 360)]),
                   scale=anim([(t0, [100, 30], EASE_OUT), (t0 + 4, [100, 100], LINEAR), (t1 - 3, [100, 100], EASE_IN),
                               (t1, [100, 0])]))
    sweep(comp, "primary", t.tm, ease)
    return comp, t


VARIANTS = [
    ("sweep", "Clock Sweep", flat, "A pie slice sweeps clockwise round the centre to cover, then sweeps on round "
                                   "to reveal."),
    ("stacked", "Stacked Sweep", stacked, "Accent, secondary and primary sweeps chase each other round the clock."),
    ("hand", "Clock Hand", radar, "A clock hand with a pivot dot leads a snappy sweep in and drags it back out.",
     {"bg": "e8e8ee"}),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"sweep": 0.52, "stacked": 0.55, "hand": 0.52}

build("clock-wipe", "Clock Wipe",
      "Radial clock wipe: a pie slice sweeps round the centre to cover the shot, holds for the cut, then sweeps "
      "on round to reveal the next clip.",
      ["clock", "radial", "sweep", "wipe", "transition", "timer"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
