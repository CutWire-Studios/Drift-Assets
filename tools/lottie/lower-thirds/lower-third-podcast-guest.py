import random
from _lt2 import *


def mic(cx, cy, s, slot="icon"):
    """Studio mic glyph: filled capsule, cradle arc, stem and base (s = icon height)."""
    w = 0.075 * s
    arc = path(bezier([(cx - 0.3 * s, cy - 0.06 * s), (cx + 0.3 * s, cy - 0.06 * s)],
                      [(0, 0), (0, 0.46 * s)], [(0, 0.46 * s), (0, 0)], closed=False), "cradle")
    return [
        group([rrect(cx - 0.17 * s, cy - 0.5 * s, 0.34 * s, 0.6 * s, 0.17 * s), fill(slot=slot)], "capsule"),
        group([arc, poly([(cx, cy + 0.29 * s), (cx, cy + 0.44 * s)], False),
               poly([(cx - 0.17 * s, cy + 0.46 * s), (cx + 0.17 * s, cy + 0.46 * s)], False),
               stroke(slot=slot, width=w)], "stand"),
    ]


def wave_bars(comp, x0, x1, cy, n, bw, hmax, slot, t_in, t_out, seed=1, stagger=1.0, parent=None, name="wave"):
    """Vertical bars that grow in left to right, then bounce like a live audio meter."""
    rng = random.Random(seed)
    step = (x1 - x0) / (n - 1)
    for i in range(n):
        x = x0 + i * step
        env = 0.45 + 0.55 * math.sin(math.pi * (i + 0.5) / n)
        k = [(0, [100, 0], HOLD), (t_in + i * stagger, [100, 0], EXPO_OUT)]
        t = t_in + i * stagger + 8
        while t < t_out:
            k.append((t, [100, round(100 * env * rng.uniform(0.25, 1.0))], EASE_IN_OUT))
            t += rng.choice((5, 6, 7))
        k.append((t_out, [100, 30], EXPO_IN))
        k.append((t_out + 10, [100, 0]))
        lay(comp, f"{name}{i}", [rrect(x - bw / 2, cy - hmax / 2, bw, hmax, bw / 2), fill(slot=slot)], (x, cy),
            scale=keys(*k), parent=parent)


def badge():
    W, H = 1150, 250
    cx, cy, r = 140, 125, 82
    x, y, w, h = cx, 70, 900, 110
    comp = base("lower-third-podcast-guest", W, H, 32)
    comp.slot("primary", "#16161D")
    comp.slot("accent", "#FF4F7B")
    comp.slot("icon", "#FFFFFF")
    comp.slot("secondary", "#2A2A36")
    b = rig(comp, "badge", (cx, cy), scale=pop(0, 16, 124, 136), rotation=keys((0, -25, EXPO_OUT), (18, 0)))
    comp.layer("mic", mic(cx, cy, 86), parent=b)
    comp.layer("disc", [ellipse((r * 2, r * 2), (cx, cy)), fill(slot="accent")], parent=b)
    comp.layer("disc-ring", [ellipse((r * 2 + 16, r * 2 + 16), (cx, cy)), fill(slot="primary")], parent=b)
    for i, t in enumerate((20, 56, 92)):
        lay(comp, f"pulse{i}", [ellipse((r * 2, r * 2), (cx, cy)), stroke(slot="accent", width=4)], (cx, cy),
            scale=keys((t, [100, 100], EASE_OUT), (t + 26, [150, 150])),
            opacity=keys((t, 80, EASE_OUT), (t + 26, 0)), ip=t, op=t + 27)
    wave_bars(comp, x + w - 150, x + w - 34, y + h / 2, 9, 7, 58, "accent", 22, 122, seed=4)
    comp.layer("sub-line", [rect_grow(x + 110, y + 76, 420, 3, 1.5, 18, 36, 118, 130), fill(slot="secondary")])
    comp.layer("bar", [rect_grow(x, y, w, h, 18, 6, 28, 122, 140, "left", start=0), fill(slot="primary")])
    comp.layer("bar-shadow", [rect_grow(x, y + 10, w, h, 18, 6, 28, 122, 140, "left", start=0),
                              fill("#000000", 22)])
    return comp, (x + 110, y + 12, w - 290, 58), (x + 110, y + 82, w - 290, 22)


def underline():
    W, H = 1100, 230
    x, y, w, h = 50, 36, 900, 96
    comp = base("lower-third-podcast-guest--waveform", W, H, 40)
    comp.slot("primary", "#FFFFFF")
    comp.slot("accent", "#7B5CFF")
    comp.slot("icon", "#FFFFFF")
    ix = x + 24
    t = rig(comp, "tile", (ix + 34, y + h / 2), scale=pop(6, 20, 118, 128))
    comp.layer("mic", mic(ix + 34, y + h / 2, 44), parent=t)
    comp.layer("tile-bg", [rrect(ix, y + 14, 68, 68, 16), fill(slot="accent")], parent=t)
    wave_bars(comp, x + 14, x + w - 14, y + h + 44, 48, 6, 54, "accent", 12, 124, seed=9, stagger=0.45)
    comp.layer("bar", [rect_grow(x, y, w, h, 12, 0, 22, 124, 142, "left", start=0), fill(slot="primary")])
    comp.layer("bar-shadow", [rect_grow(x, y + 8, w, h, 12, 0, 22, 124, 142, "left", start=0),
                              fill("#000000", 20)])
    return comp, (x + 120, y + 16, w - 150, h - 32)


def on_air():
    W, H = 1000, 250
    cx, cy, r = 500, 72, 52
    x, y, w, h = 150, 100, 700, 110
    comp = base("lower-third-podcast-guest--on-air", W, H, 34)
    comp.slot("primary", "#FFF4E0")
    comp.slot("accent", "#FF7A1A")
    comp.slot("icon", "#FFFFFF")
    comp.slot("secondary", "#2B1D14")
    b = rig(comp, "badge", (cx, cy), off=slide(0, 60, 0, 18, 124, 138, SPRING, EXPO_IN),
            scale=pop(0, 18, 124, 138))
    comp.layer("mic", mic(cx, cy, 56), parent=b)
    comp.layer("disc", [ellipse((r * 2, r * 2), (cx, cy)), fill(slot="accent"),
                        stroke(slot="primary", width=8)], parent=b)
    wave_bars(comp, cx - 210, cx - 80, cy + 4, 8, 6, 40, "accent", 14, 122, seed=2, name="wl")
    wave_bars(comp, cx + 80, cx + 210, cy + 4, 8, 6, 40, "accent", 14, 122, seed=7, name="wr")
    comp.layer("card", [rect_grow(x, y, w, h, h / 2, 6, 26, 122, 140, "centre", start=0), fill(slot="primary")])
    comp.layer("card-edge", [rect_grow(x, y + 7, w, h, h / 2, 6, 26, 122, 140, "centre", start=0),
                             fill(slot="secondary")])
    return comp, (x + 70, y + 14, w - 140, 50), (x + 110, y + 68, w - 220, 26)


a, ah, asub = badge()
b, bh = underline()
c, ch, cs = on_air()
build("lower-third-podcast-guest", "Podcast Guest Lower Third",
      "Podcast name bar with a microphone badge and a live audio waveform. Put the guest's name on the first "
      "row and their show or role on the second.",
      ["lower third", "podcast", "microphone", "guest", "waveform", "audio", "interview"], [
          V("badge", "Mic Badge", a, ah, asub, bg="e8e8ee",
            description="Round mic badge with pulsing rings; a dark bar extends from it with a waveform on the end."),
          V("waveform", "Waveform Underline", b, bh,
            description="Single-line white bar with a mic tile and a full-width bouncing waveform underneath."),
          V("on-air", "On-Air Card", c, ch, cs,
            description="Centred rounded card with the mic badge perched on top between two waveforms."),
      ])
