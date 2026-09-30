from _broadcast2 import *

F = 300          # 10 s
END = 282        # bar empty here, then refills for a seamless loop
WARN = (195, 225)  # warning colour fades in


def drain(a=100, b=0):
    return keys((0, a, LINEAR), (END, b, EASE_OUT), (F, a))


def warn_op():
    return keys((0, 0, HOLD), (WARN[0], 0, EASE_IN_OUT), (WARN[1], 100, HOLD), (END, 100, EASE_OUT), (F, 0))


def stopwatch(c, r, slot):
    x, y = c
    return [
        group([polyline([(x, y), (x, y - r * 0.62)]), stroke(slot=slot, width=r * 0.16)], "hand",
              anchor=(x, y), position=(x, y), rotation=keys((0, 0, LINEAR), (F, 3600))),
        group([ellipse((r * 0.22, r * 0.22), c), fill(slot=slot)], "hub"),
        group([ellipse((2 * r, 2 * r), c), stroke(slot=slot, width=r * 0.16)], "case"),
        group([rect_tl(x - r * 0.22, y - r * 1.34, r * 0.44, r * 0.2, 3), fill(slot=slot)], "crown"),
        group([polyline([(x, y - r), (x, y - r * 1.18)]), stroke(slot=slot, width=r * 0.14, cap="butt")], "stem"),
    ]


def modern():
    """Rounded pill bar drains right-to-left beside a ticking stopwatch; it turns red for the last seconds."""
    W, H = 1200, 180
    comp = Comp("timer-bar-depleting", W, H, fps=30, frames=F)
    comp.slot("primary", "#22D67A")
    comp.slot("accent", "#FF3B3B")
    comp.slot("icon", "#FFFFFF")
    comp.slot("background", "#23232B")
    cy = H / 2
    x0, x1, bh = 180, W - 40, 60
    pulse = keys((0, [100, 100], HOLD), (WARN[1], [100, 100], EASE_IN_OUT), (WARN[1] + 8, [108, 108], EASE_IN_OUT),
                 (WARN[1] + 16, [100, 100], EASE_IN_OUT), (WARN[1] + 24, [108, 108], EASE_IN_OUT),
                 (WARN[1] + 32, [100, 100], EASE_IN_OUT), (WARN[1] + 40, [108, 108], EASE_IN_OUT),
                 (WARN[1] + 48, [100, 100], HOLD), (F, [100, 100]))
    comp.layer("watch warn", stopwatch((88, cy + 8), 54, "accent"), anchor=(88, cy), position=(88, cy),
               scale=pulse, opacity=warn_op())
    comp.layer("watch", stopwatch((88, cy + 8), 54, "icon"), anchor=(88, cy), position=(88, cy), scale=pulse)
    sx = keys((0, [100, 100], LINEAR), (END, [0, 100], EASE_OUT), (F, [100, 100]))
    pill_ = rect_tl(x0 + 7, cy - bh / 2 + 7, x1 - x0 - 14, bh - 14, (bh - 14) / 2)
    comp.layer("shine", [group([rect_tl(x0 + 24, cy - bh / 2 + 13, x1 - x0 - 48, 8, 4), fill("#FFFFFF", 30)], "s")],
               anchor=(x0, cy), position=(x0, cy), scale=sx)
    comp.layer("fill warn", [group([pill_, fill(slot="accent")], "f")], anchor=(x0, cy), position=(x0, cy),
               scale=sx, opacity=warn_op())
    comp.layer("fill", [group([pill_, fill(slot="primary")], "f")], anchor=(x0, cy), position=(x0, cy), scale=sx)
    comp.layer("track", [group([rect_tl(x0, cy - bh / 2, x1 - x0, bh, bh / 2), fill(slot="background")], "t")])
    return comp


def segmented():
    """Chunky arcade bar of twenty blocks that switch off one by one, ending on blinking red."""
    W, H = 1160, 150
    comp = Comp("timer-bar-depleting--segmented", W, H, fps=30, frames=F)
    comp.slot("primary", "#3CE05A")
    comp.slot("secondary", "#FFD23C")
    comp.slot("accent", "#FF3B3B")
    comp.slot("outline", "#FFFFFF")
    comp.slot("background", "#101014")
    n = 20
    x0, y0, bw, bh, gap = 60, 45, 46, 60, 6
    per = END / n
    for i in range(n):
        slot = "accent" if i < 4 else "secondary" if i < 9 else "primary"
        x = x0 + i * (bw + gap)
        off = round(END - (i + 1) * per + per)  # rightmost block goes first
        back = END + 1 + i * 0.8
        if i == 0:
            op = keys((0, 100, HOLD), (off - 60, 100, HOLD), (off - 52, 30, HOLD), (off - 44, 100, HOLD),
                      (off - 36, 30, HOLD), (off - 28, 100, HOLD), (off - 20, 30, HOLD), (off - 12, 100, HOLD),
                      (off, 0, HOLD), (back, 100, HOLD), (F, 100))
        else:
            op = keys((0, 100, HOLD), (off, 0, HOLD), (back, 100, HOLD), (F, 100))
        comp.layer(f"block{i}", [box(x + 6, y0 + 6, bw - 12, 10, "#FFFFFF", opacity=40, name="hi"),
                                 box(x, y0, bw, bh, slot=slot)], opacity=op)
    comp.layer("slots", [box(x0 + i * (bw + gap), y0, bw, bh, "#FFFFFF", opacity=7, name=f"s{i}") for i in range(n)])
    fx0, fx1 = x0 - 16, x0 + n * (bw + gap) - gap + 16
    comp.layer("frame", [
        group([rect_tl(fx0, y0 - 16, fx1 - fx0, bh + 32), stroke(slot="outline", width=8, join="miter", cap="butt")],
              "frame"),
        box(fx0, y0 - 16, fx1 - fx0, bh + 32, slot="background")])
    comp.layer("frame shadow", [box(fx0 - 4 + 10, y0 - 20 + 10, fx1 - fx0 + 8, bh + 40, "#000000", opacity=45)])
    return comp


def neon():
    """Thin neon line burns down with a bright spark at its head; it shifts to the warning colour at the end."""
    W, H = 1200, 120
    comp = Comp("timer-bar-depleting--neon", W, H, fps=30, frames=F)
    comp.slot("primary", "#2EF2FF")
    comp.slot("accent", "#FF2E88")
    cy = H / 2
    x0, x1 = 50, W - 50
    line = polyline([(x0, cy), (x1, cy)])
    tr = [trim(end=drain())]
    comp.layer("spark", [group([sparkle(46, 0, 0, 0.14), fill("#FFFFFF")], "star",
                               rotation=keys((0, 0, LINEAR), (F, 720))),
                         group([ellipse((16, 16)), fill("#FFFFFF")], "dot"),
                         group([ellipse((44, 44)), fill(slot="primary", opacity=35)], "halo")],
               position=keys((0, [x1, cy], LINEAR), (END, [x0, cy], EASE_OUT), (F, [x1, cy])),
               scale=wave_keys(F, [[100, 100], [80, 80]] * 15, EASE_IN_OUT))
    comp.layer("warn", glow_strokes([line], slot="accent", width=8, extra=tr), opacity=warn_op())
    comp.layer("line", glow_strokes([line], slot="primary", width=8, extra=tr))
    comp.layer("track", [group([line, stroke(slot="primary", width=8, opacity=16)], "track"),
                         group([polyline([(x0, cy - 22), (x0, cy + 22)]), polyline([(x1, cy - 22), (x1, cy + 22)]),
                                stroke(slot="primary", width=4, opacity=60)], "ends")])
    return comp


build_asset(CAT, "timer-bar-depleting", "Timer Bar Depleting",
            "Ten-second countdown bar that drains and turns to a warning colour near the end, then refills so "
            "it loops. Good for quizzes, challenges and giveaways.",
            ["timer", "countdown", "progress", "bar", "quiz", "time", "game show", "seconds"], [
    V("modern", "Modern Pill", modern(), "loop", thumb_t=0.45,
            description="Rounded pill bar with a ticking stopwatch; turns red and pulses in the last seconds."),
    V("segmented", "Arcade Blocks", segmented(), "loop", thumb_t=0.55,
            description="Chunky pixel-style frame of twenty blocks that switch off one by one, ending on blinking red."),
    V("neon", "Neon Fuse", neon(), "loop", thumb_t=0.45,
            description="Thin neon line that burns down like a fuse with a spark at its head."),
])
