import random

from _common import *

W, H, F = 1920, 1080, 90
comp = Comp("vhs-hud", W, H, fps=30, frames=F)
comp.slot("icon", "#FFFFFF")

TRI = [(140, 108), (140, 212), (230, 160)]


def tri(color, slot=None, opacity=100):
    return [group([polyline(TRI, closed=True), fill(color, opacity, slot=slot)], "play")]


# slight horizontal jitter of the on-screen display, returning to rest for the loop
jit = anim([(0, [0, 0], HOLD), (19, [3, 0], HOLD), (21, [0, 0], HOLD), (52, [-2, 0], HOLD),
            (53, [2, 0], HOLD), (55, [0, 0], HOLD), (F, [0, 0])])
flick = anim([(0, 100, HOLD), (20, 82, HOLD), (22, 100, HOLD), (53, 88, HOLD), (55, 100, HOLD), (F, 100)])

comp.layer("play", tri("#FFFFFF", "icon"), position=jit, opacity=flick)
comp.layer("play red", tri("#FF2A4F", opacity=70), position=anim(
    [(t, [v[0] - 5, 0], e) for t, v, e in jit.keys]), opacity=flick)
comp.layer("play cyan", tri("#29E8FF", opacity=70), position=anim(
    [(t, [v[0] + 5, 0], e) for t, v, e in jit.keys]), opacity=flick)
comp.layer("play shadow", tri("#000000", opacity=40), position=(4, 5))

# tracking-noise band rolling down the picture once per loop
rng = random.Random(7)
streaks = []
for i in range(26):
    w = rng.uniform(40, 420)
    x = rng.uniform(-100, W)
    y = rng.uniform(-38, 38)
    h = rng.choice([2, 2, 3, 4])
    streaks.append(box(x, y, w, h, "#FFFFFF", opacity=rng.uniform(25, 70), name=f"streak{i}"))
band = streaks + [
    group([rect((W, 120), (W / 2, 0)), gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.10), (1, "#FFFFFF", 0)],
                                        (0, -60), (0, 60))], "glow"),
]
comp.layer("tracking band", band, position=anim([(0, [W / 2 - W / 2, -140], LINEAR), (F, [0, H + 140])]),
           anchor=(0, 0))
comp.layer("tracking band 2", [
    group([rect((W, 40)), gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.07), (1, "#FFFFFF", 0)],
                                       (0, -20), (0, 20))], "glow")],
    position=anim([(0, [W / 2, H * 0.55], LINEAR), (F * 0.45, [W / 2, H + 40], HOLD),
                   (F * 0.45 + 1, [W / 2, -40], LINEAR), (F, [W / 2, H * 0.55])]))

# fine scanlines drifting down by one period over the loop
P = 6
comp.layer("scanlines", [
    group([rect((W, 2), (W / 2, -P * 4)), fill("#000000", 100),
           repeater(H // P + 6, position=(0, P))], "lines"),
], position=anim([(0, [0, 0], LINEAR), (F, [0, P * 3])]), opacity=16)

finish(comp, "broadcast", "vhs-hud", "VHS HUD",
       "Retro VHS on-screen display: RGB-split play triangle, drifting scanlines and a rolling "
       "tracking band. Add PLAY next to the triangle and a timestamp bottom-left.",
       ["vhs", "retro", "80s", "90s", "tape", "play", "camcorder", "overlay"], "loop",
       text_area=[262, 100, 440, 120], thumb_t=0.3, region=(40, 40, 640, 640))
