"""A tiny personal rain cloud that hovers and drizzles: seamless loop in three looks."""

from _memes2 import *

W, H = 440, 480
F = 72
CX, CY = W / 2, 150
PUFFS = [(-92, 22, 104), (-40, -26, 124), (38, -38, 138), (98, 12, 108), (0, 30, 150), (-52, 40, 100),
         (58, 42, 100)]


def puffs(dx=0, dy=0, grow=0, sx=1.0):
    return [ellipse((d + grow, d + grow), (CX + x * sx + dx, CY + y + dy)) for x, y, d in PUFFS]


def drop(size=1.0):
    s = size
    return path(bezier([(0, -16 * s), (9 * s, 2 * s), (0, 11 * s), (-9 * s, 2 * s)],
                       [(0, 0), (0, -6 * s), (6 * s, 0), (0, 6 * s)],
                       [(0, 0), (0, 6 * s), (-6 * s, 0), (0, -6 * s)]), "drop")


def rain(comp, shapes_fn, xs, period, life, y0, y1, seed, slant=0.0, fade_out=True):
    rng = random.Random(seed)
    for i, x in enumerate(xs):
        t0 = (i * period * 0.618 * 7) % F + rng.uniform(0, 3)
        for rep in range(int(F // period)):
            s = (t0 + rep * period) % F

            def fn(u, x=x):
                p = u / life
                yy = y0 + (y1 - y0) * p ** 1.25
                return {"position": [x + slant * (yy - y0), yy],
                        "opacity": 100 * clamp(p * 6) * (clamp((1 - p) * 4) if fade_out else 1)}
            particle(comp, f"drop{i}-{rep}", shapes_fn(), s, life, F, fn, step=3)


def cartoon():
    """Chunky outlined cloud with a glum little face, bobbing while fat drops fall."""
    comp = base("sad-rain-cloud", W, H, F)
    comp.slot("primary", "#B9C3D4")
    comp.slot("accent", "#4FA8FF")
    comp.slot("outline", INK)
    bob = loop(F, [[0, 0], [0, -8]], SINE)
    squash = loop(F, [[100, 100], [103, 97]], SINE)
    face = [group([ellipse((6, 7), (CX - 30, CY + 21)), ellipse((6, 7), (CX + 38, CY + 21)), fill("#FFFFFF")], "glint"),
            group([ellipse((16, 20), (CX - 34, CY + 26)), ellipse((16, 20), (CX + 34, CY + 26)), fill(INK)], "eyes"),
            group([polyline([(CX - 52, CY + 10), (CX - 22, CY - 2)]), polyline([(CX + 52, CY + 10), (CX + 22, CY - 2)]),
                   stroke(INK, width=6)], "brows"),
            group([arc_path(20, 200, 340, (CX, CY + 66)), stroke(INK, width=6)], "mouth"),
            group([ellipse((30, 14), (CX - 62, CY + 50)), ellipse((30, 14), (CX + 62, CY + 50)),
                   fill("#FF8FA3", 45)], "cheeks")]
    comp.layer("face", face, anchor=(CX, CY + 60), position=at((CX, CY + 60), bob), scale=squash)
    shade = [group(puffs(0, 18, -8) + [fill("#000000", 10)], "shade")]
    hi = [group([ellipse((60, 26), (CX - 50, CY - 58)), fill("#FFFFFF", 55)], "hi")]
    comp.layer("cloud", hi + [group(puffs() + [fill(slot="primary")], "body")] + shade,
               anchor=(CX, CY + 60), position=at((CX, CY + 60), bob), scale=squash)
    comp.layer("cloud-line", [group(puffs() + [stroke(slot="outline", width=18), fill(slot="outline")], "ink")],
               anchor=(CX, CY + 60), position=at((CX, CY + 60), bob), scale=squash)
    xs = [CX - 90, CX - 45, CX, CX + 45, CX + 90, CX - 68, CX + 22, CX + 68]
    rain(comp, lambda: [group([drop(1.1)], "d"),
                        group([drop(1.1), fill(slot="accent"), stroke(slot="outline", width=5)], "d2")],
         xs[:6], 24, 26, CY + 90, H - 30, 7)
    comp.layer("shadow", [group([ellipse((260, 26), (CX, H - 22)), fill("#000000", 22)], "sh")],
               anchor=(CX, H - 22), position=(CX, H - 22),
               scale=loop(F, [[100, 100], [92, 92]], SINE))
    return comp


def minimal():
    """Line-art cloud outline with streaky dashed rain; no face, very clean."""
    comp = base("sad-rain-cloud--line", W, H, F)
    comp.slot("outline", "#FFFFFF")
    comp.slot("accent", "#8CC8FF")
    bob = loop(F, [[0, 0], [0, -6]], SINE)
    # clean union outline: every puff stroked, the inside knocked out by the puffs themselves
    face = [group([ellipse((13, 13), (CX - 32, CY + 22)), ellipse((13, 13), (CX + 32, CY + 22)),
                   fill(slot="outline")], "eyes"),
            group([arc_path(18, 205, 335, (CX, CY + 62)), stroke(slot="outline", width=7)], "mouth")]
    comp.layer("face", face, position=bob)
    comp.layer("knockout", [group(puffs() + [fill("#000000")], "k")], position=bob)
    comp.layer("cloud", [group(puffs() + [stroke(slot="outline", width=20)], "line")], position=bob,
               matte="alpha_inverted")
    comp.layer("tint", [group(puffs() + [fill(slot="outline", opacity=8)], "tint")], position=bob)
    xs = [CX - 110, CX - 66, CX - 22, CX + 22, CX + 66, CX + 110]
    rng = random.Random(4)
    for i, x in enumerate(xs):
        for rep in range(3):
            s = (i * 7 + rep * 24) % F

            def fn(u, x=x):
                p = u / 22
                return {"position": [x - 18 * p, CY + 130 + 230 * p], "opacity": 100 * clamp(p * 5) * clamp((1 - p) * 3)}
            particle(comp, f"streak{i}-{rep}", [group([polyline([(0, -26), (6, 26)]),
                                                       stroke(slot="accent", width=7)], "s")], s, 22, F, fn, step=2)
    return comp


def storm():
    """Dark storm cloud that rumbles, with slanted heavy rain and a lightning flash each loop."""
    comp = base("sad-rain-cloud--storm", W, H, F)
    comp.slot("primary", "#4A5163")
    comp.slot("accent", "#FFE14D")
    comp.slot("secondary", "#9FD0FF")
    FL = 40
    sh = keys(*shake_keys(FL, FL + 12, 6, 11, pivot=(0, 0)))
    bolt = [(CX + 14, CY + 30), (CX - 40, CY + 150), (CX + 2, CY + 144), (CX - 30, CY + 280), (CX + 64, CY + 124),
            (CX + 20, CY + 130), (CX + 54, CY + 30)]
    comp.layer("bolt", [group([polyline(bolt, closed=True), fill(slot="accent"), stroke("#FFFFFF", width=4)], "b")],
               opacity=keys((0, 0, HOLD), (FL, 100, HOLD), (FL + 3, 0, HOLD), (FL + 5, 100, HOLD), (FL + 10, 0, HOLD),
                            (F, 0)))
    comp.layer("lit", [group(puffs() + [fill("#FFFFFF", 22)], "glow")],
               position=sh,
               opacity=keys((0, 0, HOLD), (FL, 100, HOLD), (FL + 3, 0, HOLD), (FL + 5, 100, EASE_OUT),
                            (FL + 14, 0, HOLD), (F, 0)))
    comp.layer("cloud-hi", [group([ellipse((70, 26), (CX - 48, CY - 60)), fill("#FFFFFF", 22)], "hi")], position=sh)
    comp.layer("cloud", [group(puffs(0, 24, -6) + [fill("#000000", 22)], "under"),
                         group(puffs() + [fill(slot="primary")], "body")], position=sh)
    comp.layer("flash", [group(puffs() + [stroke(slot="accent", width=w, opacity=o)], f"glow{w}") for w, o in ((30, 30), (60, 16), (100, 8))],
               position=sh,
               opacity=keys((0, 0, HOLD), (FL, 100, HOLD), (FL + 3, 0, HOLD), (FL + 5, 100, EASE_OUT),
                            (FL + 14, 0, HOLD), (F, 0)))
    xs = [CX - 120 + i * 24 for i in range(11)]
    for i, x in enumerate(xs):
        for rep in range(4):
            s = (i * 5 + rep * 18) % F

            def fn(u, x=x):
                p = u / 14
                return {"position": [x - 60 * p + 20, CY + 70 + 300 * p], "opacity": 90 * clamp(p * 5) * clamp((1 - p) * 3)}
            particle(comp, f"rain{i}-{rep}", [group([polyline([(0, -22), (8, 22)]),
                                                     stroke(slot="secondary", width=6)], "s")], s, 14, F, fn, step=2)
    return comp


build_asset(CAT, "sad-rain-cloud", "Sad Rain Cloud",
            "A tiny personal rain cloud that hovers and drizzles on a loop. Place it over someone's head for "
            "instant gloom.",
            ["rain", "cloud", "sad", "gloomy", "meme", "weather", "loop"], [
    Variant("cartoon", "Cartoon", cartoon(), "loop", thumb_t=0.3,
            description="Outlined cartoon cloud with a glum face, bobbing while fat drops fall."),
    Variant("line", "Line Art", minimal(), "loop", thumb_t=0.3,
            description="Clean white outline cloud with a simple line face and streaky rain."),
    Variant("storm", "Storm", storm(), "loop", thumb_t=0.57,
            description="Dark rumbling cloud with heavy slanted rain and a lightning flash each loop."),
])
