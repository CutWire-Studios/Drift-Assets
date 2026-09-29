import random

from _broadcast2 import *

W, H = 1920, 1080
F = 60
C = (W / 2, H / 2)


def battery(x, y, w, h, color=None, slot=None, width=5, cells=4, blink_last=True, name="battery"):
    """Battery outline at top-left (x, y) with `cells` bars; returns (outline groups, cell groups)."""
    out = [group([rect_tl(x, y, w, h, 7), stroke(color or "#FFFFFF", width=width, slot=slot)], "case"),
           group([rect_tl(x + w + 3, y + h * 0.3, 8, h * 0.4, 2), fill(color or "#FFFFFF", slot=slot)], "tip")]
    cw = (w - 12 - (cells - 1) * 5) / cells
    cl = [group([rect_tl(x + 6 + i * (cw + 5), y + 6, cw, h - 12, 2), fill(color or "#FFFFFF", slot=slot)],
                f"cell{i}") for i in range(cells)]
    return out, cl


def focus_box(c, w, h, arm, width, color=None, slot=None):
    x0, y0, x1, y1 = c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2
    return [group(corners(x0, y0, x1, y1, arm) + [stroke(color or "#FFFFFF", width=width, slot=slot, cap="butt",
                                                         join="miter")], "focus")]


LOCK = keys((0, [135, 135], EXPO_OUT), (6, [92, 92], SPRING), (16, [100, 100], HOLD), (50, [100, 100], EASE_IN),
            (F, [135, 135]))
LOCK_OP = keys((0, 0, EASE_OUT), (4, 100, HOLD), (52, 100, EASE_IN), (F, 0))
LOCKED = keys((0, 0, HOLD), (15, 0, HOLD), (16, 100, HOLD), (50, 100, EASE_IN), (54, 0, HOLD), (F, 0))


def modern():
    """Clean viewfinder: thin corner marks, blinking REC dot, battery, thirds grid and a focus square that locks."""
    comp = Comp("camcorder-viewfinder", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF2D2D")
    comp.slot("accent", "#3DFF7A")
    M, ARM = 80, 110
    comp.layer("rec", [group([ellipse((34, 34), (M + 44, M + 46)), fill(slot="primary")], "dot")],
               opacity=blink(F, 30, 3))
    comp.layer("focus locked", focus_box(C, 260, 190, 40, 5, slot="accent"), anchor=C, position=C, scale=LOCK,
               opacity=LOCKED)
    comp.layer("focus", focus_box(C, 260, 190, 40, 5, slot="icon"), anchor=C, position=C, scale=LOCK,
               opacity=LOCK_OP)
    case, cells = battery(W - M - 150, M + 26, 106, 44, slot="icon")
    comp.layer("battery", case + cells)
    # zoom slider bottom centre with a drifting indicator
    zx0, zx1, zy = C[0] - 220, C[0] + 220, H - M - 30
    comp.layer("zoom knob", [group([rect_tl(-5, zy - 18, 10, 36, 3), fill(slot="icon")], "knob")],
               position=wave_keys(F, [[zx0 + 150, 0], [zx0 + 185, 0]], SINE))
    comp.layer("zoom", [group([polyline([(zx0, zy), (zx1, zy)])] +
                              [polyline([(zx0 + i * 44, zy - 8), (zx0 + i * 44, zy + 8)]) for i in range(11)] +
                              [stroke(slot="icon", width=3, opacity=80, cap="butt")], "zoom")])
    comp.layer("marks", [group(corners(M, M, W - M, H - M, ARM) + [stroke(slot="icon", width=5, cap="butt",
                                                                       join="miter")], "corners"),
                         group([polyline([(C[0] - 26, C[1]), (C[0] + 26, C[1])]),
                                polyline([(C[0], C[1] - 26), (C[0], C[1] + 26)]),
                                stroke(slot="icon", width=3, opacity=80)], "cross")])
    grid = [polyline([(W / 3, M + 40), (W / 3, H - M - 40)]), polyline([(2 * W / 3, M + 40), (2 * W / 3, H - M - 40)]),
            polyline([(M + 40, H / 3), (W - M - 40, H / 3)]), polyline([(M + 40, 2 * H / 3), (W - M - 40, 2 * H / 3)])]
    comp.layer("thirds", [group(grid + [stroke(slot="icon", width=2, opacity=22, cap="butt")], "grid")])
    comp.layer("shadow", [group(corners(M, M, W - M, H - M, ARM) + [stroke("#000000", width=9, opacity=25,
                                                                         cap="butt", join="miter")], "c")],
               position=(2, 3))
    areas = {"rec": (M + 80, M + 18, 340, 56), "timecode": (M + 20, H - M - 90, 460, 60),
             "battery": (W - M - 460, M + 18, 290, 56)}
    return comp, areas


def retro():
    """90s camcorder: chunky shadowed marks, draining blinking battery, spinning tape reels and scanlines."""
    comp = Comp("camcorder-viewfinder--retro", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF2A2A")
    M, ARM, SW = 100, 150, 12
    jit = keys((0, [0, 0], HOLD), (23, [2, 0], HOLD), (25, [0, 0], HOLD), (47, [-2, 1], HOLD), (48, [0, 0], HOLD),
               (F, [0, 0]))

    def ui(color, slot=None):
        case, cells = battery(W - M - 180, M + 20, 130, 58, color=color, slot=slot, width=8, cells=3)
        tape_c = (W - M - 118, M + 150)
        tape = [group([rect_tl(tape_c[0] - 62, tape_c[1] - 34, 124, 68, 10), stroke(color, width=7, slot=slot)],
                      "cassette"),
                group([rect_tl(tape_c[0] - 30, tape_c[1] + 14, 60, 20, 4), stroke(color, width=5, slot=slot)],
                      "window")]
        reels = []
        for dx in (-28, 28):
            rc = (tape_c[0] + dx, tape_c[1] - 6)
            reels.append(group([ellipse((30, 30), rc), stroke(color, width=5, slot=slot),
                                ], f"reel{dx}"))
            reels.append(group([polyline([(rc[0] - 10, rc[1]), (rc[0] + 10, rc[1])]),
                                polyline([(rc[0], rc[1] - 10), (rc[0], rc[1] + 10)]),
                                stroke(color, width=4, slot=slot, cap="butt")], f"spokes{dx}",
                               anchor=rc, position=rc, rotation=keys((0, 0, LINEAR), (F, 360))))
        return case, cells, tape + reels

    for color, slot, off, name, op in (("#FFFFFF", "icon", (0, 0), "", 100), ("#000000", None, (5, 5), " shadow", 55)):
        case, cells, tape = ui(color, slot)
        cell_ops = [100, 100, keys((0, 100, HOLD), (15, 0, HOLD), (30, 100, HOLD), (45, 0, HOLD), (F, 100))]
        for i, cgrp in enumerate(cells):
            comp.layer(f"cell{i}{name}", [cgrp], position=at(off, jit), opacity=cell_ops[i] if op == 100 else
                       (keys((0, op, HOLD), (15, 0, HOLD), (30, op, HOLD), (45, 0, HOLD), (F, op)) if i == 2 else op))
        comp.layer(f"ui{name}", case + tape + [
            group(corners(M, M, W - M, H - M, ARM) + [stroke(color, width=SW, slot=slot, cap="butt", join="miter")],
                  "corners")], position=at(off, jit), opacity=op)
        comp.layer(f"rec{name}", [group([ellipse((46, 46), (M + 52, M + 50)), fill(
            "#FF2A2A" if slot else color, slot="primary" if slot else None)], "dot")], position=at(off, jit),
            opacity=keys((0, op, HOLD), (30, 0, HOLD), (F, op)))
    scanlines(comp, W, H, 5, 2, 12)
    comp.layer("vignette", [vignette(W, H, 0.45, 0.6)])
    areas = {"rec": (M + 100, M + 16, 340, 70), "timecode": (M + 10, H - M - 100, 520, 76),
             "date": (W - M - 530, H - M - 100, 520, 76)}
    return comp, areas


def pro():
    """Cinema-camera monitor: red record border, 2.39 frame guides, audio meters and a focus square."""
    comp = Comp("camcorder-viewfinder--pro", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF2D2D")
    comp.slot("accent", "#3DFF7A")
    comp.slot("background", "#000000")
    bar = 72
    comp.layer("rec border", [group([rect_tl(6, bar + 6, W - 12, H - 2 * bar - 12), stroke(slot="primary", width=8,
                                                                                               join="miter")], "b")],
               opacity=keys((0, 100, HOLD), (40, 100, EASE_IN_OUT), (44, 25, HOLD), (56, 25, EASE_IN_OUT), (F, 100)))
    comp.layer("rec", [group([ellipse((26, 26), (46, bar / 2)), fill(slot="primary")], "dot")],
               opacity=blink(F, 40, 3))
    # audio meters: two segmented bars bouncing at the left edge
    rng = random.Random(2)
    mx, my0, my1 = 40, H - bar - 40, H - bar - 330
    segs = []
    for ch in range(2):
        x = mx + ch * 22
        lv = [rng.uniform(35, 95) for _ in range(6)]
        comp.layer(f"meter mask {ch}", [group([rect_tl(x, my1, 16, my0 - my1), fill("#FFFFFF")], "m")],
                   anchor=(x, my0), position=(x, my0), scale=wave_keys(F, [[100, v] for v in lv], EASE_IN_OUT))
        n = 24
        sh = []
        for i in range(n):
            y = my0 - (i + 1) * (my0 - my1) / n
            c = "#FF3B3B" if i >= n - 3 else "#FFD23C" if i >= n - 8 else None
            sh.append(group([rect_tl(x, y + 2, 16, (my0 - my1) / n - 3), fill(c or "#3DFF7A", slot=None if c else "accent")],
                            f"s{i}"))
        comp.layer(f"meter {ch}", sh, matte="alpha")
        segs.append(group([rect_tl(x, my1, 16, my0 - my1), fill("#FFFFFF", 12)], f"t{ch}"))
    comp.layer("meter tracks", segs)
    comp.layer("focus locked", focus_box(C, 200, 200, 26, 4, slot="accent"), anchor=C, position=C, scale=LOCK,
               opacity=LOCKED)
    comp.layer("focus", focus_box(C, 200, 200, 26, 4, slot="icon"), anchor=C, position=C, scale=LOCK, opacity=LOCK_OP)
    gh = W / 2.39
    comp.layer("guides", [group([rect_tl(0, C[1] - gh / 2, W, gh), stroke(slot="icon", width=2, opacity=55,
                                                                          dashes=[18, 12])], "239"),
                          group([rect_tl(W * 0.05, H * 0.05 + bar * 0.6, W * 0.9, H * 0.9 - bar * 1.2),
                                 stroke(slot="icon", width=2, opacity=25)], "safe"),
                          group([polyline([(C[0] - 16, C[1]), (C[0] + 16, C[1])]),
                                 polyline([(C[0], C[1] - 16), (C[0], C[1] + 16)]),
                                 stroke(slot="icon", width=2, opacity=70)], "cross")])
    case, cells = battery(W - 110, bar / 2 - 15, 60, 30, slot="icon", width=3, cells=3)
    comp.layer("battery", case + cells)
    comp.layer("bars", [box(0, 0, W, bar, slot="background", opacity=70), box(0, H - bar, W, bar, slot="background",
                                                                              opacity=70)])
    areas = {"top": (80, 12, W - 220, bar - 24), "bottom": (120, H - bar + 12, W - 240, bar - 24)}
    return comp, areas


m, ma = modern()
r, ra = retro()
p, pa = pro()
build_asset(CAT, "camcorder-viewfinder", "Camcorder Viewfinder",
            "Full-frame camera viewfinder overlay with a transparent centre: corner marks, blinking record dot, "
            "battery and a focus square that locks on. Text areas for REC, timecode and other readouts.",
            ["camcorder", "viewfinder", "camera", "rec", "recording", "focus", "overlay", "vlog"], [
    V("modern", "Modern", m, "loop", text_area=ma["rec"], text_areas=ma, thumb_t=0.4, bg="4f5a6e",
            description="Thin corner marks, thirds grid, zoom slider and a focus square that locks green."),
    V("retro", "90s Camcorder", r, "loop", text_area=ra["rec"], text_areas=ra, thumb_t=0.2, bg="4f5a6e",
            description="Chunky shadowed marks, a blinking low battery, spinning tape reels, scanlines and jitter."),
    V("pro", "Cinema Monitor", p, "loop", text_area=pa["top"], text_areas=pa, thumb_t=0.4, bg="4f5a6e",
            description="Cinema-camera monitor: red record border, info bars, 2.39 guides, audio meters and focus box."),
])
