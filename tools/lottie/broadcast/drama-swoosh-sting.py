import math
import random

from _broadcast2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 40
PEAK = 15          # flash peak; the intro ends here
OUT = 19           # outro starts


def base(name):
    c = Comp(name, W, H, fps=30, frames=F)
    c.marker("intro", 0, PEAK)
    c.marker("outro", OUT, F - OUT)
    return c


def flash(comp, peak=85, color="#FFFFFF", slot=None):
    comp.layer("flash", [box(0, 0, W, H, color, slot=slot)],
               opacity=keys((PEAK - 3, 0, EASE_IN), (PEAK, peak, HOLD), (OUT - 1, peak, EASE_OUT), (OUT + 12, 0)))


def curve(y0, y1, bend, x0=-300, x1=W + 300):
    """Gentle S-curve across the frame."""
    return path(bezier([(x0, y0), (x1, y1)], [(0, 0), (-(x1 - x0) * 0.4, -bend)], [((x1 - x0) * 0.4, bend), (0, 0)],
                       closed=False))


def swoosh():
    """Curved light streaks whip across the frame into a white flash, then fade."""
    comp = base("drama-swoosh-sting")
    comp.slot("primary", "#FFFFFF")
    comp.slot("accent", "#FFB02E")
    rng = random.Random(12)
    flash(comp, 80)
    streaks = [(620, 380, 260, 44, "primary"), (700, 460, 200, 18, "accent"), (540, 300, 320, 10, "primary"),
               (820, 560, 140, 26, "accent"), (440, 260, 280, 8, "primary"), (760, 500, 240, 6, "primary")]
    for i, (y0, y1, bend, w_, slot) in enumerate(streaks):
        t0 = rng.uniform(0, 5)
        t1 = t0 + rng.uniform(11, 14)
        cv = curve(y0, y1, bend)
        tr = trim(start=keys((t0 + 3, 0, EASE_IN), (t1 + 6, 100)), end=keys((t0, 0, EXPO_OUT), (t1, 100)))
        comp.layer(f"streak{i}", [group([cv, tr, stroke("#FFFFFF", width=w_ * 0.35, opacity=90)], "core"),
                                  group([cv, tr, stroke(slot=slot, width=w_)], "body"),
                                  group([cv, tr, stroke(slot=slot, width=w_ * 3, opacity=18)], "glow")],
                   opacity=keys((t0, 100, HOLD), (t1, 100, EASE_OUT), (t1 + 8, 0)))
    comp.layer("sheen", [group([rect((W * 3, 520)), gradient_fill(
        [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.35), (1, "#FFFFFF", 0)], (0, -260), (0, 260))], "band", rotation=-12)],
        position=keys((2, [-W, C[1] - 60], EASE_IN), (PEAK + 2, [W * 1.6, C[1] + 60])),
        opacity=keys((2, 0, EASE_OUT), (6, 100, HOLD), (PEAK, 100, EASE_OUT), (PEAK + 4, 0)))
    return comp


def zoom():
    """Radial speed lines rush into the centre, a flash hits and a shockwave ring blows out."""
    comp = base("drama-swoosh-sting--zoom")
    comp.slot("primary", "#FFFFFF")
    comp.slot("accent", "#FF2E4D")
    rng = random.Random(4)
    flash(comp, 75)
    comp.layer("shockwave", [group([ellipse(keys((PEAK, [120, 120], EXPO_OUT), (PEAK + 16, [2600, 2600])), C),
                                    stroke(slot="accent", width=keys((PEAK, 50, EASE_OUT), (PEAK + 16, 6)))], "ring")],
               ip=PEAK, op=PEAK + 17, opacity=keys((PEAK, 100, EASE_IN), (PEAK + 16, 0)))
    lines = []
    for i in range(46):
        a = math.radians(i * 360 / 46 + rng.uniform(-3, 3))
        r0 = rng.uniform(1150, 1300)
        r1 = rng.uniform(170, 360)
        p0 = (C[0] + math.cos(a) * r0, C[1] + math.sin(a) * r0)
        p1 = (C[0] + math.cos(a) * r1, C[1] + math.sin(a) * r1)
        t0 = rng.uniform(0, 5)
        lines.append(group([polyline([p0, p1]),
                            trim(start=keys((t0 + 4, 0, EASE_IN), (PEAK + 2, 100)), end=keys((t0, 0, EXPO_OUT), (PEAK - 2, 100))),
                            stroke(slot="primary" if i % 3 else "accent", width=rng.uniform(4, 16), cap="round")],
                           f"l{i}"))
    comp.layer("lines", lines, ip=0, op=PEAK + 3)
    comp.layer("vignette", [vignette(W, H, 0.6, 0.4)], opacity=keys((0, 0, EASE_OUT), (PEAK, 100, HOLD),
                                                                     (OUT, 100, EASE_IN), (F - 2, 0)))
    return comp


def flare():
    """Anamorphic lens flare streaks across horizontally with a hot core, blooms into a flash and fades."""
    comp = base("drama-swoosh-sting--flare")
    comp.slot("primary", "#6FD8FF")
    comp.slot("accent", "#FFFFFF")
    flash(comp, 70, slot="accent")
    fx = keys((0, [-500, C[1]], (0.3, 0, 0.2, 1)), (PEAK, [C[0], C[1]], HOLD), (OUT, [C[0], C[1]], EASE_IN),
              (F, [W + 600, C[1]]))
    grow = keys((0, [40, 100], EXPO_OUT), (PEAK, [140, 100], HOLD), (OUT, [140, 100], EASE_IN), (F, [60, 100]))
    comp.layer("core", [group([ellipse((260, 260)), gradient_fill([(0, "#FFFFFF", 1), (0.4, "#FFFFFF", 0.5),
                                                                   (1, "#FFFFFF", 0)], (0, 0), (130, 0), radial=True)],
                              "hot")],
               position=fx, scale=keys((0, [40, 40], EXPO_OUT), (PEAK, [160, 160], HOLD), (OUT, [160, 160], EASE_IN),
                                       (F, [30, 30])),
               opacity=keys((0, 100, HOLD), (OUT, 100, EASE_IN), (F - 4, 0)))
    streak = [group([ellipse((2600, 16)), fill("#FFFFFF", 95)], "line"),
              group([ellipse((2400, 54)), fill(slot="primary", opacity=45)], "blue"),
              group([ellipse((2200, 150)), fill(slot="primary", opacity=14)], "haze"),
              group([ellipse((1600, 300)), fill(slot="primary", opacity=6)], "haze2")]
    comp.layer("streak", streak, position=fx, scale=grow, opacity=keys((0, 100, HOLD), (OUT, 100, EASE_IN), (F - 4, 0)))
    ghosts = []
    for k, (d, s, o) in enumerate(((-420, 90, 30), (-760, 50, 22), (380, 140, 18), (640, 70, 26))):
        ghosts.append(group([ellipse((s, s)), stroke(slot="primary", width=4, opacity=o)], f"g{k}", position=(d, 0)))
        ghosts.append(group([ellipse((s, s)), fill(slot="primary", opacity=o / 3)], f"gf{k}", position=(d, 0)))
    comp.layer("ghosts", ghosts, position=keys((0, [W + 300, C[1]], (0.3, 0, 0.2, 1)), (PEAK, [C[0], C[1]], HOLD),
                                               (OUT, [C[0], C[1]], EASE_IN), (F, [-700, C[1]])),
               opacity=keys((0, 0, EASE_OUT), (8, 100, HOLD), (OUT, 100, EASE_IN), (F - 6, 0)))
    return comp


build_asset(CAT, "drama-swoosh-sting", "Drama Swoosh Sting",
            "Reality-TV style dramatic sting: a whoosh of light into a white flash that fades out, for punching "
            "into a reveal or a confessional cut. Empty at the start and end; the flash can be held.",
            ["drama", "reality tv", "swoosh", "whoosh", "flash", "sting", "transition", "reveal"], [
    V("swoosh", "Swoosh", swoosh(), "intro-hold-outro", thumb_t=0.28, bg="4b5366",
      description="Curved white and amber light streaks whip across into a white flash."),
    V("zoom", "Zoom Lines", zoom(), "intro-hold-outro", thumb_t=0.25, bg="4b5366",
      description="Radial speed lines rush into the centre, then a flash and a red shockwave ring."),
    V("flare", "Lens Flare", flare(), "intro-hold-outro", thumb_t=0.3, bg="2a2f3d",
      description="An anamorphic blue lens flare streaks across, blooms into a flash and slides away."),
])
