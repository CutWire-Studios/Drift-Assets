import math
import random

from _broadcast2 import *

F = 60
W, H = 960, 300
CY = H / 2


def voice(rng, n, steps=8):
    """Per-bar seamless level loops with a speech-like envelope (louder in the middle)."""
    out = []
    for i in range(n):
        x = i / (n - 1)
        env = 0.35 + 0.65 * math.sin(math.pi * x) ** 0.8
        out.append([max(8, 100 * env * rng.uniform(0.2, 1.0)) for _ in range(steps)])
    return out


def modern():
    """Mic in a coloured badge next to rounded voice bars; the badge pulses with the audio."""
    comp = Comp("podcast-mic-waveform", W, H, fps=30, frames=F)
    comp.slot("primary", "#FF6B3D")
    comp.slot("icon", "#FFFFFF")
    rng = random.Random(21)
    mc = (150, CY)
    beat = wave_keys(F, [[100, 100], [106, 106], [101, 101], [104, 104]] * 2)
    comp.layer("mic", mic_icon(1.15, mc[0], mc[1] + 8, slot="icon", width=8), anchor=mc, position=mc, scale=beat)
    comp.layer("badge", [group([ellipse((190, 190), mc), fill(slot="primary")], "badge")],
               anchor=mc, position=mc, scale=beat)
    comp.layer("ring", [group([ellipse((190, 190), mc), stroke(slot="primary", width=4)], "ring")],
               anchor=mc, position=mc,
               scale=keys((0, [100, 100], EASE_OUT), (30, [140, 140], HOLD), (30.5, [100, 100], EASE_OUT),
                          (F, [140, 140])),
               opacity=keys((0, 70, EASE_IN), (30, 0, HOLD), (30.5, 70, EASE_IN), (F, 0)))
    n, x0, x1 = 34, 290, W - 40
    step = (x1 - x0) / (n - 1)
    bars = []
    for i, vals in enumerate(voice(rng, n)):
        x = x0 + i * step
        bars.append(group([polyline([(0, -110), (0, 110)]), stroke(slot="icon", width=12)], f"b{i}",
                          position=(x, CY), scale=wave_keys(F, [[100, v] for v in vals], EASE_IN_OUT)))
    comp.layer("bars", bars)
    return comp


def retro():
    """Vintage broadcast mic in a ring mount beside a green oscilloscope screen with a live trace."""
    comp = Comp("podcast-mic-waveform--retro", W, H, fps=30, frames=F)
    comp.slot("primary", "#52FF8F")
    comp.slot("background", "#0E1A12")
    comp.slot("outline", "#C9B48A")
    mc = (140, CY - 6)
    # mic: chrome grille capsule inside a spring ring, on a stand
    grille = [group([polyline([(mc[0] - 44, mc[1] - 40 + i * 11), (mc[0] + 44, mc[1] - 40 + i * 11)])], f"g{i}")
              for i in range(8)]
    comp.layer("grille matte", [group([rect((92, 112), mc, 46), fill("#FFFFFF")], "m")])
    comp.layer("grille", [group(grille + [stroke("#2B2B2B", 3.5, opacity=70, cap="butt")], "lines")], matte="alpha")
    comp.layer("capsule", [group([rect((92, 112), mc, 46), gradient_fill(
        [(0, "#F4F4F4"), (0.45, "#B9BCC2"), (1, "#5B5E66")], (mc[0] - 46, mc[1] - 40), (mc[0] + 46, mc[1] + 50))],
        "cap"), group([rect((100, 120), mc, 50), fill("#2A2A2E")], "rim")])
    comp.layer("mount", [group([ellipse((150, 150), mc), stroke(slot="outline", width=8)], "ring"),
                         group([polyline([(mc[0], mc[1] + 75), (mc[0], H - 30)]), stroke(slot="outline", width=10)],
                               "stem"),
                         group([rect((110, 16), (mc[0], H - 26), 8), fill(slot="outline")], "foot")])
    # scope screen
    sx0, sx1, sy0, sy1 = 270, W - 30, 40, H - 40
    scy = (sy0 + sy1) / 2
    n = 90
    rng = random.Random(4)

    def trace(ph):
        pts = []
        for i in range(n):
            u = i / (n - 1)
            env = math.sin(math.pi * u) ** 1.5
            y = (math.sin(u * 30 + ph) * 0.6 + math.sin(u * 71 + ph * 2.3) * 0.3 +
                 math.sin(u * 13 - ph * 1.7) * 0.5) * env * 78
            pts.append((sx0 + 20 + u * (sx1 - sx0 - 40), scy + y))
        return bezier(pts, closed=False)
    ks = [(f, trace(f / F * 2 * math.pi * 2), LINEAR) for f in range(0, F + 1, 2)]
    tr = path(Anim(ks), "trace")
    comp.layer("trace", glow_strokes([tr], slot="primary", width=4, widths=(26, 12), ops=(8, 20), core=True))
    grid = [polyline([(sx0 + 20 + i * (sx1 - sx0 - 40) / 10, sy0 + 12), (sx0 + 20 + i * (sx1 - sx0 - 40) / 10,
                                                                         sy1 - 12)]) for i in range(11)]
    grid += [polyline([(sx0 + 12, sy0 + 20 + j * (sy1 - sy0 - 40) / 4), (sx1 - 12, sy0 + 20 + j * (sy1 - sy0 - 40) / 4)])
             for j in range(5)]
    comp.layer("grid", [group(grid + [stroke(slot="primary", width=1.5, opacity=18, cap="butt")], "grid")])
    comp.layer("glass", [group([rect((sx1 - sx0, sy1 - sy0), ((sx0 + sx1) / 2, scy), 22), gradient_fill(
        [(0, "#FFFFFF", 0.10), (0.5, "#FFFFFF", 0.0)], (0, sy0), (0, scy))], "glass")])
    comp.layer("screen", [group([rect((sx1 - sx0, sy1 - sy0), ((sx0 + sx1) / 2, scy), 22), fill(slot="background")],
                                "screen"),
                          group([rect((sx1 - sx0 + 16, sy1 - sy0 + 16), ((sx0 + sx1) / 2, scy), 30),
                                 fill(slot="outline")], "bezel")])
    return comp


def neon():
    """Neon-outlined mic with glowing mirrored bars that pulse out from the centre."""
    comp = Comp("podcast-mic-waveform--neon", W, H, fps=30, frames=F)
    comp.slot("primary", "#FF3FD2")
    comp.slot("secondary", "#3FE7FF")
    rng = random.Random(8)
    mc = (140, CY + 6)
    capsule, rest = mic_shapes(1.9, mc[0], mc[1] - 6)
    comp.layer("mic", glow_strokes([capsule] + rest, slot="primary", width=8))
    n, x0, x1 = 30, 270, W - 40
    step = (x1 - x0) / (n - 1)
    bars = []
    for i, vals in enumerate(voice(rng, n)):
        x = x0 + i * step
        d = abs(i - n / 2) / (n / 2)
        vals = [max(8, v * (1.1 - 0.5 * d)) for v in vals]
        sk = wave_keys(F, [[100, min(v, 100)] for v in vals], EASE_IN_OUT)
        line = polyline([(0, -105), (0, 105)])
        bars.append(group([group([line, stroke("#FFFFFF", width=4, opacity=85)], "core"),
                           group([line, stroke(slot="secondary", width=10)], "tube"),
                           group([line, stroke(slot="secondary", width=24, opacity=18)], "glow")],
                          f"b{i}", position=(x, CY), scale=sk))
    comp.layer("bars", bars)
    return comp


build_asset(CAT, "podcast-mic-waveform", "Podcast Mic Waveform",
            "Podcast microphone with a live, looping voice waveform, for audiograms, podcast clips and "
            "radio segments.",
            ["podcast", "microphone", "waveform", "audio", "voice", "audiogram", "radio", "mic"], [
    V("modern", "Modern Badge", modern(), "loop", thumb_t=0.25,
            description="Mic in a pulsing coloured badge next to rounded voice bars."),
    V("retro", "Oscilloscope", retro(), "loop", thumb_t=0.25,
            description="Vintage ring-mounted mic beside a green oscilloscope screen with a live trace."),
    V("neon", "Neon", neon(), "loop", thumb_t=0.25,
            description="Glowing neon mic outline with mirrored neon bars pulsing from the centre."),
])
