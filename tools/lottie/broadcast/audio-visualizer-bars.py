import math
import random

from _broadcast2 import *

F = 60  # 2 s loop


def levels(rng, n, i, lo=12, hi=100, env=None, steps=8, spread=0.25):
    """Seamless loop of `steps` random levels (percent) for bar i, shaped by an envelope 0..1."""
    e = 1.0 if env is None else env
    vals = [max(lo, min(hi, lo + (hi - lo) * e * rng.uniform(spread, 1.0))) for _ in range(steps)]
    return vals


def scale_keys(vals, axis="y", phase=0):
    vals = vals[phase:] + vals[:phase]
    return wave_keys(F, [[100, v] if axis == "y" else [v, 100] for v in vals], EASE_IN_OUT)


def env_at(x):
    """Bell-ish envelope over 0..1 with a bit of spread."""
    return 0.45 + 0.55 * math.exp(-((x - 0.45) ** 2) / 0.12)


def linear():
    """Classic equalizer: square-topped bars rising from a baseline with falling peak caps."""
    W, H = 1040, 340
    comp = Comp("audio-visualizer-bars", W, H, fps=30, frames=F)
    comp.slot("primary", "#35E0A1")
    comp.slot("accent", "#FFFFFF")
    rng = random.Random(11)
    n, gap = 28, 8
    bw = (W - 80 - gap * (n - 1)) / n
    base = H - 40
    top = 280
    caps, bars, ghosts = [], [], []
    for i in range(n):
        x = 40 + i * (bw + gap)
        vals = levels(rng, n, i, 8, 100, 1.0 - 0.55 * (i / (n - 1)) ** 1.3, spread=0.15)
        cap_vals = [max(v, vals[j - 1]) for j, v in enumerate(vals)]  # caps hang on the higher level
        bars.append(group([rect_tl(x, base - top, bw, top, 3), fill(slot="primary")], f"bar{i}",
                          anchor=(x + bw / 2, base), position=(x + bw / 2, base), scale=scale_keys(vals)))
        ghosts.append(group([rect_tl(x, base - top, bw, top, 3), fill(slot="primary", opacity=10)], f"g{i}"))
        caps.append(group([rect_tl(x, -9, bw, 7, 2), fill(slot="accent")], f"cap{i}",
                          position=wave_keys(F, [[0, base - top * v / 100 - 6] for v in cap_vals], EASE_IN_OUT)))
    comp.layer("caps", caps)
    comp.layer("sheen matte", [group(bars, "bars")])
    comp.layer("sheen", [group([rect_tl(40, base - top, W - 80, top), gradient_fill(
        [(0, "#FFFFFF", 0.45), (0.6, "#FFFFFF", 0.0)], (0, base - top), (0, base))], "sheen")], matte="alpha")
    comp.layer("bars", bars)
    comp.layer("ghosts", ghosts)
    comp.layer("baseline", [box(30, base + 6, W - 60, 4, slot="primary", opacity=60)])
    return comp


def mirrored():
    """Rounded pill bars mirrored around a centre line, like a voice waveform."""
    W, H = 1040, 400
    comp = Comp("audio-visualizer-bars--mirrored", W, H, fps=30, frames=F)
    comp.slot("primary", "#7C5CFF")
    comp.slot("secondary", "#FF5CA8")
    rng = random.Random(5)
    n, gap = 40, 9
    bw = (W - 80 - gap * (n - 1)) / n
    cy = H / 2
    full = 320
    top, bot = [], []
    for i in range(n):
        x = 40 + i * (bw + gap) + bw / 2
        vals = levels(rng, n, i, 10, 100, env_at(i / (n - 1)), spread=0.35)
        sk = scale_keys(vals)
        top.append(group([rect((bw, full), (0, 0), bw / 2), fill(slot="primary")], f"t{i}", position=(x, cy),
                         scale=sk))
        bot.append(group([rect((bw, full), (0, 0), bw / 2), fill(slot="secondary")], f"b{i}", position=(x, cy),
                         scale=sk))
    comp.layer("top half matte", [box(0, 0, W, cy)])
    comp.layer("top half", top, matte="alpha")
    comp.layer("bottom half", bot)
    comp.layer("centre line", [box(24, cy - 1, W - 48, 2, "#FFFFFF", opacity=35)])
    return comp


def circular():
    """Bars radiating around a disc, like a circular spectrum, with a pulsing core."""
    S = 660
    C = (S / 2, S / 2)
    comp = Comp("audio-visualizer-bars--circular", S, S, fps=30, frames=F)
    comp.slot("primary", "#27D7FF")
    comp.slot("accent", "#FF4FD8")
    comp.slot("background", "#101018")
    rng = random.Random(9)
    n = 56
    R, L = 172, 118
    bars = []
    for i in range(n):
        a = i * 360 / n
        e = 0.55 + 0.45 * abs(math.sin(math.radians(a * 1.5)))
        vals = levels(rng, n, i, 10, 100, e)
        inner = group([rect((9, L), (0, -R - L / 2), 4.5), fill(slot="primary")], "bar",
                      anchor=(0, -R), position=(0, -R), scale=scale_keys(vals))
        bars.append(group([inner], f"b{i}", position=C, rotation=a))
    beat = wave_keys(F, [[100, 100], [106, 106], [100, 100], [103, 103]] * 2, EASE_IN_OUT)
    comp.layer("ring", [group([ellipse((2 * R - 22, 2 * R - 22), C), stroke(slot="accent", width=6)], "ring")],
               anchor=C, position=C, scale=beat)
    comp.layer("core", [group([ellipse((2 * R - 40, 2 * R - 40), C), fill(slot="background")], "core"),
                        group([ellipse((2 * R - 40, 2 * R - 40), C), gradient_fill(
                            [(0, "#FFFFFF", 0.14), (1, "#FFFFFF", 0.0)], (C[0], C[1] - R), (C[0], C[1] + R * 0.4))],
                              "sheen")],
               anchor=C, position=C, scale=beat)
    comp.layer("bars", bars)
    comp.layer("bar glow", [group([ellipse((2 * R + 70, 2 * R + 70), C), stroke(slot="primary", width=90,
                                                                                   opacity=10)], "glow")])
    return comp, (C[0] - 110, C[1] - 60, 220, 120)


circ, circ_text = circular()
build_asset(CAT, "audio-visualizer-bars", "Audio Visualizer Bars",
            "Looping music equalizer bars for podcasts, music clips and audiograms. The circular variant "
            "leaves room in the centre for a name or logo.",
            ["equalizer", "audio", "visualizer", "music", "spectrum", "bars", "sound", "podcast"], [
    V("linear", "Linear EQ", linear(), "loop", thumb_t=0.3,
            description="Classic equalizer bars rising from a baseline with falling peak caps."),
    V("mirrored", "Mirrored Wave", mirrored(), "loop", thumb_t=0.3,
            description="Rounded pill bars mirrored around a centre line in two colours, like a voice waveform."),
    V("circular", "Circular Spectrum", circ, "loop", text_area=circ_text, thumb_t=0.3,
            description="Bars radiate around a dark disc with a beating ring; text area in the centre."),
])
