from _common import *


def heart_pts(n=48):
    """Classic parametric heart, ~2 units wide, centred on its bounding box middle."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((x / 16, (y + 2.5) / 16))
    return pts


PTS = heart_pts()
HEART = smooth_closed(PTS, tension=1.0)
# the frame sits a little above the heart's middle, where the heart is widest
CENTER = (CX, CY + 60)
SCALE = cover_scale(PTS, CENTER, margin=50)


def flat():
    t = Timing(15, 10, 15)
    comp = base("heart-wipe", t, "cherry", ("primary",))
    grow_open(comp, "primary", t.tm, HEART, SCALE, center=CENTER)
    return comp, t


def stacked():
    t = Timing(16, 10, 16)
    comp = base("heart-wipe--stacked", t, "cherry", ("primary", "secondary", "accent"))
    for s, tm in stack(t, lag=3):
        grow_open(comp, s, tm, HEART, SCALE, center=CENTER, name=s)
    return comp, t


def beat():
    """Heart pops in, beats twice at small size, then fills the frame; the reveal hole has an outline rim."""
    t = Timing(20, 8, 14)
    comp = base("heart-wipe--heartbeat", t, "cherry", ("primary", "accent"))

    def pulse(u):
        # pop to 5%, two beats, then zoom to full
        if u < 0.25:
            return 0.05 * ease_at(POP, u / 0.25)
        if u < 0.55:
            v = (u - 0.25) / 0.3
            return 0.05 * (1 + 0.28 * abs(math.sin(v * 2 * math.pi)))
        return 0.05 * 20 ** ease_at(GENTLE, (u - 0.55) / 0.45)

    # the rim is 0.05 units wide: grow a little further so its inner half clears the notch, same for the hole
    scale = cover_scale(PTS, CENTER, margin=int(50 + 0.05 * SCALE * 0.6))
    grow_open(comp, "primary", t.tm, HEART, scale, curve=pulse, spin=(0, -6), outline="accent", outline_w=0.05,
              center=CENTER, over=1.5)
    return comp, t


VARIANTS = [
    ("flat", "Flat Heart", flat, "A heart grows out of the centre to fill the frame, then a heart-shaped hole opens "
                                 "to reveal."),
    ("stacked", "Stacked Hearts", stacked, "Three hearts in accent, secondary and primary grow one after another "
                                           "and open in reverse."),
    ("heartbeat", "Heartbeat", beat, "The heart pops in, beats at mid size, then fills the frame; an accent rim "
                                     "edges the heart-shaped reveal."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"flat": 0.55, "stacked": 0.7, "heartbeat": 0.68}

build("heart-wipe", "Heart Wipe",
      "Heart-shaped iris transition: a heart grows to cover the shot, holds on solid colour for the cut, then "
      "opens up onto the next clip.",
      ["heart", "love", "valentine", "iris", "transition", "romantic"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
