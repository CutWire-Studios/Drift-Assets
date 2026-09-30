from _common import *


def star_pts(points=5, inner=0.5, rot=-90):
    pts = []
    for i in range(points * 2):
        a = math.radians(rot + 180 * i / points)
        r = 1.0 if i % 2 == 0 else inner
        pts.append((math.cos(a) * r, math.sin(a) * r))
    return pts


PTS = star_pts()
STAR = bezier(PTS, closed=True)
CENTER = (CX, CY + 30)
SCALE = cover_scale(PTS, CENTER, margin=50)


def sparkle(comp, pos, t0, size, slot="accent", name="sparkle"):
    """Four-point twinkle that pops and fades."""
    pts = []
    for i in range(8):
        a = math.radians(45 * i - 90)
        r = 1.0 if i % 2 == 0 else 0.22
        pts.append((math.cos(a) * r * size, math.sin(a) * r * size))
    comp.layer(name, [group([path(bezier(pts, closed=True)), fill(slot=slot)], "twinkle")], position=pos,
               scale=anim([(t0, [0, 0], POP), (t0 + 5, [100, 100], EASE_IN), (t0 + 9, [0, 0])]),
               rotation=anim([(t0, -45, EASE_OUT), (t0 + 9, 45)]), ip=t0, op=t0 + 10)


def flat():
    t = Timing(15, 10, 15)
    comp = base("star-wipe", t, {"primary": "#FFC93C"})
    grow_open(comp, "primary", t.tm, STAR, SCALE, spin=(144, 72), center=CENTER)
    return comp, t


def stacked():
    t = Timing(16, 10, 16)
    comp = base("star-wipe--stacked", t, "violet", ("primary", "secondary", "accent"))
    for i, (s, tm) in enumerate(stack(t, lag=3)):
        grow_open(comp, s, tm, STAR, SCALE, spin=(144 + 36 * i, -72), center=CENTER, name=s)
    return comp, t


def twinkle():
    t = Timing(14, 8, 12)
    comp = base("star-wipe--twinkle", t, "violet", ("primary", "accent"))
    a0, a1, b0, b1 = t.tm
    for k, (x, y, f, sz) in enumerate([(-420, -250, 1, 90), (380, -300, 3, 70), (480, 220, 2, 110),
                                       (-360, 260, 4, 80), (40, -420, 5, 60)]):
        sparkle(comp, (CX + x, CY + y), a0 + f, sz, name=f"sparkle{k}")
    for k, (x, y, f, sz) in enumerate([(-520, -200, 0, 120), (560, 260, 1, 100), (-300, 330, 2, 90)]):
        sparkle(comp, (CX + x, CY + y), b0 + f, sz, name=f"sparkle-out{k}")
    scale = cover_scale(PTS, CENTER, margin=int(50 + 0.06 * SCALE * 0.6))
    grow_open(comp, "primary", t.tm, STAR, scale, spin=(216, 36), outline="accent", outline_w=0.06,
              center=CENTER, over=1.5, curve=zoom_curve(POP, 5.0))
    return comp, t


VARIANTS = [
    ("spin", "Spinning Star", flat, "A star spins as it zooms out of the centre to fill the frame, then a star-shaped "
                                    "hole spins open."),
    ("stacked", "Stacked Stars", stacked, "Three stars in accent, secondary and primary spin in one after another "
                                          "and open in reverse."),
    ("twinkle", "Twinkle", twinkle, "Sparkles twinkle round a star with an accent rim that zooms in with a little "
                                    "overshoot."),
]

# thumbnail moment, as a fraction of the intro (frame part-covered so the shape reads)
THUMB = {"spin": 0.62, "stacked": 0.55, "twinkle": 0.5}

build("star-wipe", "Star Wipe",
      "Star-shaped iris transition: a spinning star zooms in to cover the shot, holds for the cut, then opens "
      "onto the next clip.",
      ["star", "iris", "spin", "retro", "transition", "fun"],
      [V(v, n, *f(), d, thumb=THUMB[v], **(k[0] if k else {})) for v, n, f, d, *k in VARIANTS])
