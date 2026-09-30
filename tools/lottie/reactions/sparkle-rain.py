"""Sparkle rain: four-point sparkles, stars and dots drift down, twisting and twinkling (loop)."""

from _reactions2 import *

T = 90
W, H = 420, 520
GOLD, PINK, CYAN = "#FFD66B", "#FF8FD8", "#7FE3FF"
COLS = [("primary", GOLD), ("secondary", PINK), ("accent", CYAN)]


def make(style):
    comp = Comp("sparkle-rain", W, H, frames=T)
    for sid, c in COLS:
        comp.slot(sid, c)

    def shapes(i):
        sid, col = COLS[i % 3] if style != "glow" else COLS[0] if i % 4 else COLS[1]
        kind = i % 5
        r = 30 if kind in (0, 3) else 22 if kind == 1 else 16
        if kind == 4:
            shp = [ellipse((14, 14))]
        elif kind == 2:
            shp = S(star_d(r, 0.48))
        else:
            shp = S(sparkle_d(r))
        if style == "glow":
            return [group(S(sparkle_d(r * 0.4)) + [fill(WHITE, 90)], name="core") if kind != 4 else
                    group([ellipse((6, 6)), fill(WHITE)]),
                    group(shp + [fill(col, slot=sid)]),
                    group([ellipse((r * 2.6, r * 2.6)),
                           gradient_fill([(0, col, 0.55), (0.4, col, 0.18), (1, col, 0)], (0, 0),
                                         (r * 1.3, 0), radial=True)], name="glow")]
        if style == "flat":
            return [group(shp + [fill(col, slot=sid)])]
        # doodle: hand-drawn strokes only, with a little + or ring companion
        extra = []
        if kind in (0, 3):
            extra = [group(S(f"M 0 -{r * 0.35} L 0 {r * 0.35} M -{r * 0.35} 0 L {r * 0.35} 0") +
                           [stroke(col, 4, slot=sid)], position=(r * 1.1, -r * 0.9))]
        body = shp if kind != 4 else [ellipse((16, 16))]
        return extra + [group(body + [stroke(col, 5.5, slot=sid)])]

    n = 22 if style != "doodle" else 18
    rain(comp, "sparkle", n, T, W, H, shapes, seed={"glow": 3, "flat": 5, "doodle": 7}[style],
         life=(0.75, 1.0), size=(0.8, 1.5), sway=22, spin=160, flip=0.0, tumble=0.0)

    # a few in-place twinklers so the rain never looks sparse
    for j, (x, y, ph) in enumerate(((90, 140, 0.0), (330, 250, 0.33), (160, 400, 0.66))):
        sid, col = COLS[j % 3]
        comp.layer(f"twinkle{j}", [group(S(sparkle_d(26)) + ([fill(col, slot=sid)] if style != "doodle"
                                                             else [stroke(col, 5, slot=sid)]))],
                   position=(x, y),
                   scale=sampled(lambda t, ph=ph: [100 * max(0.0, math.sin(TAU * (t / T * 2 + ph))) ** 1.5] * 2,
                                 0, T, 2),
                   rotation=sampled(lambda t: 90 * t / T, 0, T, 5))  # 4-fold symmetric
    return comp


build3("sparkle-rain", "Sparkle Rain",
       "Sparkles, little stars and dots drifting down with a twist and a twinkle; a magical overlay "
       "for reveals and glow-ups. Seamless loop.",
       ["sparkle", "sparkles", "rain", "magic", "glitter", "stars", "reaction"], make, [
           ("glow", "Glow", "loop", 0.5, "Golden sparkles with soft radial glows."),
           ("flat", "Flat Confetti", "loop", 0.5, "Flat multi-colour sparkles, stars and dots."),
           ("doodle", "Doodle", "loop", 0.5, "Hand-drawn line sparkles with little plus marks."),
       ])
