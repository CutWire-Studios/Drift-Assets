"""Buffering spinner that never finishes: a seamless loop in three looks."""

from _memes2 import *

S = 320
C = (S / 2, S / 2)


def dots():
    """Classic ring of twelve dots with a fading chase that ticks round."""
    F = 72
    comp = base("loading-forever-spinner", S, S, F)
    comp.slot("primary", "#FFFFFF")
    comp.slot("background", "#000000")
    R, n, step = 92, 12, 3
    rk = [(i * step, i * 360 / n, HOLD) for i in range(F // step)] + [(F, 720)]
    comp.layer("dots", [group([ellipse((30, 30), (0, -R)), fill(slot="primary"),
                               repeater(n, rotation=-360 / n, start_opacity=100, end_opacity=12)], "dots")],
               position=C, rotation=keys(*rk))
    comp.layer("pulse", [group([ellipse((276, 276)), fill(slot="background", opacity=45)], "disc")],
               position=C, scale=loop(F, [[100, 100], [103, 103], [100, 100], [103, 103]], SINE))
    return comp


def ring():
    """Material-style arc that grows, chases its tail and spins over a faint track."""
    F = 45
    comp = base("loading-forever-spinner--ring", S, S, F)
    comp.slot("primary", "#4DA3FF")
    comp.slot("secondary", "#FFFFFF")
    R, w = 100, 22
    shift = 71 * 3.6
    comp.layer("arc", [group([arc_path(R, -90, 270),
                              trim(start=keys((0, 0, HOLD), (18, 0, (0.4, 0, 0.2, 1)), (F, 71)),
                                   end=keys((0, 4, (0.4, 0, 0.2, 1)), (26, 75, HOLD), (F, 75))),
                              stroke(slot="primary", width=w)], "arc")],
               position=C, rotation=keys((0, 0, LINEAR), (F, 720 - shift)))
    comp.layer("track", [group([ellipse((2 * R, 2 * R)), stroke(slot="secondary", width=w, opacity=18)], "track")],
               position=C)
    comp.layer("shadow", [group([ellipse((2 * R, 2 * R)), stroke("#000000", width=w + 12, opacity=18)], "sh")],
               position=C)
    return comp


def pixel():
    """Retro 8-bit chase: eight square blocks light up in turn with a stepped trail."""
    F = 64
    comp = base("loading-forever-spinner--pixel", S, S, F)
    comp.slot("primary", "#7CFF6B")
    comp.slot("background", "#101418")
    P, g = 56, 14
    cells = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    step = 4
    trail = [100, 62, 40, 26]
    for i, (cx, cy) in enumerate(cells):
        k = []
        for s in range(F // step):
            d = (s - i) % 8
            k.append((s * step, trail[d] if d < len(trail) else 16, HOLD))
        k.append((F, k[0][1]))
        x, y = C[0] + cx * (P + g), C[1] + cy * (P + g)
        comp.layer(f"block{i}", [group([rect((P, P), (x, y)), fill(slot="primary")], "b"),
                                 group([rect((P, 8), (x, y - P / 2 + 4)), fill("#FFFFFF", 35)], "hi")],
                   opacity=keys(*k))
        comp.layer(f"block{i}-dim", [group([rect((P, P), (x, y)), fill(slot="primary", opacity=14)], "b")])
    comp.layer("panel", [group([rect((3 * P + 2 * g + 44, 3 * P + 2 * g + 44), C), fill(slot="background", opacity=80)],
                               "panel"),
                         group([rect((3 * P + 2 * g + 44, 3 * P + 2 * g + 44), C), stroke(slot="primary", width=6,
                                                                                         opacity=40, join="miter")],
                               "edge")])
    return comp


build_asset(CAT, "loading-forever-spinner", "Loading Forever Spinner",
            "A buffering spinner that loops forever and never finishes loading. Drop it over a frozen moment "
            "for the eternal-buffering joke.",
            ["loading", "buffering", "spinner", "waiting", "meme", "lag", "loop"], [
    Variant("dots", "Dot Ring", dots(), "loop", thumb_t=0.1,
            description="Twelve dots with a fading chase that ticks round on a dim disc."),
    Variant("ring", "Arc Ring", ring(), "loop", thumb_t=0.45,
            description="Modern arc that grows and chases its tail over a faint track."),
    Variant("pixel", "Pixel Blocks", pixel(), "loop", thumb_t=0.2,
            description="Retro 8-bit panel of square blocks lighting up in turn."),
])
