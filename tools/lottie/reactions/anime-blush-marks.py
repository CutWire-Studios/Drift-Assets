"""Anime blush: a pair of cheek blushes that glow on and pulse; place over a face (loop)."""

from _reactions2 import *

T = 60
W, H = 460, 200
CHEEKS = ((112, 100), (348, 100))
PINK = "#FF6F91"


def pulse(t):
    return 0.5 - 0.5 * math.cos(TAU * t / 30)


def hatch_lines(n, w, h, tilt=0.55):
    xs = [(-w / 2 + w * (i + 0.5) / n) for i in range(n)]
    return [path(bezier([(x - h * tilt / 2, h / 2), (x + h * tilt / 2, -h / 2)], closed=False))
            for x in xs]


def make(style):
    comp = Comp("anime-blush-marks", W, H, frames=T)
    comp.slot("primary", PINK)
    for i, (x, y) in enumerate(CHEEKS):
        if style == "hatch":
            comp.layer(f"hatch{i}", [group(hatch_lines(4, 96, 34) + [stroke(WHITE, 6, 85)])],
                       position=(x, y),
                       opacity=sampled(lambda t, i=i: 60 + 40 * pulse(t + i * 4), 0, T, 2))
            comp.layer(f"blush{i}", [group([ellipse((150, 64)), fill(PINK, 92, slot="primary")]),
                                     group([ellipse((176, 84)), fill(PINK, 35, slot="primary")])],
                       position=(x, y),
                       scale=sampled(lambda t, i=i: [100 + 6 * pulse(t + i * 4), 100 + 8 * pulse(t + i * 4)], 0, T, 2))
        elif style == "soft":
            rings = [group([ellipse((170 - 30 * k, 90 - 16 * k)), fill(PINK, 18 + 6 * k, slot="primary")])
                     for k in range(5)]
            comp.layer(f"glow{i}", rings[::-1], position=(x, y),
                       scale=sampled(lambda t, i=i: [100 + 8 * pulse(t + i * 3)] * 2, 0, T, 2),
                       opacity=sampled(lambda t, i=i: 75 + 25 * pulse(t + i * 3), 0, T, 2))
            # little sparkles twinkling near the cheek
            for j, (dx, dy, ph) in enumerate(((-70, -44, 0.0), (74, -36, 0.5), (60, 40, 0.25))):
                sx = dx if i == 0 else -dx
                comp.layer(f"spark{i}{j}", [group(S(sparkle_d(13)) + [fill("#FFB3C7"), stroke(WHITE, 3)])],
                           position=(x + sx, y + dy),
                           scale=sampled(lambda t, ph=ph: [100 * max(0.0, math.sin(TAU * (t / 30 + ph))) ** 1.4] * 2,
                                         0, T, 2))
        else:  # doodle: marker hatching drawn on, held, redrawn
            lines = hatch_lines(5, 120, 46, 0.6)
            items = []
            for k, ln in enumerate(lines):
                t0 = 2 + k * 2
                items.append(group([ln, trim(end=anim([(t0, 0, SNAP_OUT), (t0 + 6, 100, HOLD),
                                                        (46, 100, EASE_IN), (54, 0)])),
                                    stroke(PINK, 8, slot="primary")], name=f"l{k}"))
            comp.layer(f"doodle{i}", items, position=(x, y),
                       rotation=sampled(lambda t: 2 * math.sin(TAU * t / 15), 0, T, 3))
            comp.layer(f"under{i}", [group([ellipse((140, 56)), fill(PINK, 22, slot="primary")])],
                       position=(x, y + 2),
                       opacity=anim([(0, 0), (8, 100, HOLD), (46, 100), (56, 0)]))
    return comp


build3("anime-blush-marks", "Anime Blush Marks",
       "A pair of anime cheek blushes that glow on and pulse; position them over a face for "
       "flustered, shy or smitten moments. Seamless loop.",
       ["anime", "blush", "shy", "flustered", "cute", "kawaii", "reaction"], make, [
           ("hatch", "Hatched", "loop", 0.5, "Pink ovals with classic white diagonal hatching.", "e8e8ee"),
           ("soft", "Soft Glow", "loop", 0.5, "Soft layered glow with twinkling sparkles.", "e8e8ee"),
           ("doodle", "Doodle", "loop", 0.3, "Marker hatch strokes that draw on and redraw.", "e8e8ee"),
       ])
