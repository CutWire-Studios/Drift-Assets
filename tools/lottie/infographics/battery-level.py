from _common import *

W, H = 780, 340
BC = (290, 170)          # body centre
BW, BH = 420, 196
N = 5
LIT = 4
BOLT = [(12, -62), (-34, 8), (-4, 8), (-14, 62), (34, -10), (4, -10)]


def seg_rects(bc=BC, bw=BW, bh=BH, n=N, pad=20, gap=12, vertical=False):
    out = []
    if vertical:
        sh = (bh - 2 * pad - gap * (n - 1)) / n
        for i in range(n):
            cy = bc[1] + bh / 2 - pad - sh / 2 - i * (sh + gap)
            out.append(((bc[0], cy), (bw - 2 * pad, sh)))
    else:
        sw = (bw - 2 * pad - gap * (n - 1)) / n
        for i in range(n):
            cx = bc[0] - bw / 2 + pad + sw / 2 + i * (sw + gap)
            out.append(((cx, bc[1]), (sw, bh - 2 * pad)))
    return out


def areas():
    x = BC[0] + BW / 2 + 60
    return {"value": (x, BC[1] - 70, W - x - 24, 80), "label": (x, BC[1] + 18, W - x - 24, 48)}


def body(comp, style, bc=BC, bw=BW, bh=BH, vertical=False, t0=0):
    nub = ((bc[0], bc[1] - bh / 2 - 16), (bw * 0.36, 26)) if vertical else ((bc[0] + bw / 2 + 16, bc[1]), (26, bh * 0.36))
    sc = keys((t0, [70, 70], SOFT_SPRING), (t0 + 16, [100, 100]))
    if style == "neon":
        shapes = glow_strokes([rect((bw, bh), bc, 30), rect(nub[1], nub[0], 8)], slot="primary", width=5,
                              widths=(26, 14), ops=(8, 18))
        shapes.append(group([rect((bw, bh), bc, 30), fill(slot="background", opacity=80)], "bg"))
    else:
        shapes = [group([rect((bw, bh), bc, 34), stroke(slot="outline", width=12)], "shell"),
                  group([rect(nub[1], nub[0], 8), fill(slot="outline")], "nub"),
                  group([rect((bw, bh), bc, 34), fill(slot="outline", opacity=8)], "glass")]
    comp.layer("body", shapes, anchor=bc, position=bc, scale=sc, opacity=fade(t0, t0 + 4))


def flat():
    """Rounded battery outline; four of five segments pop in one after another and the last one flashes."""
    F = 75
    comp = Comp("battery-level", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#2ED3A0"}, "primary", "outline")
    for i, (c, sz) in enumerate(seg_rects()):
        if i >= LIT:
            continue
        t = 12 + i * 7
        if i == LIT - 1:
            comp.layer("flash", [group([rect(sz, c, 10), fill("#FFFFFF")], "f")], ip=t + 6, op=t + 20,
                       opacity=keys((t + 6, 80, EASE_IN), (t + 20, 0)))
        comp.layer(f"seg{i}", [group([rect(sz, c, 10), gradient_fill([(0, "#FFFFFF", 0.3), (0.5, "#FFFFFF", 0)],
                                                                     (0, c[1] - sz[1] / 2), (0, c[1]))], "sheen"),
                               group([rect(sz, c, 10), fill(slot="primary")], "f")],
                   anchor=(c[0], c[1] + sz[1] / 2), position=(c[0], c[1] + sz[1] / 2),
                   scale=keys((t, [100, 0], SPRING), (t + 12, [100, 100])), ip=t)
    body(comp, "flat")
    return comp


def charging():
    """Loop: a lightning bolt pulses while the segments fill one by one, blink full and drain."""
    F = 96
    comp = Comp("battery-level--charging", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#2ED3A0", "accent": "#FFC247"}, "primary", "accent", "outline")
    bolt = [(BC[0] + x, BC[1] + y) for x, y in BOLT]
    comp.layer("bolt", [group([polyline(bolt, closed=True), fill(slot="accent"),
                               stroke("#1C1C22", width=6)], "bolt")],
               anchor=BC, position=BC,
               scale=loop(F, [[100, 100], [112, 112], [100, 100], [112, 112], [100, 100], [112, 112]], EASE_IN_OUT))
    for i, (c, sz) in enumerate(seg_rects()):
        t = 8 + i * 12
        comp.layer(f"seg{i}", [group([rect(sz, c, 10), fill(slot="primary")], "f")],
                   anchor=(c[0] - sz[0] / 2, c[1]), position=(c[0] - sz[0] / 2, c[1]),
                   scale=keys((0, [0, 100], HOLD), (t, [0, 100], EXPO_OUT), (t + 10, [100, 100], HOLD), (F, [100, 100])),
                   opacity=keys((0, 0, HOLD), (t, 100, HOLD), (70, 100, HOLD), (72, 30, HOLD), (75, 100, HOLD),
                                (78, 30, HOLD), (81, 100, EASE_IN), (92, 0, HOLD), (F, 0)))
    body(comp, "flat", t0=-40)
    return comp


def neon():
    """Upright neon battery; segments light up bottom to top with a glow and a spark at the top level."""
    F = 75
    Wn, Hn = 560, 600
    bc, bw, bh = (170, 322), 196, 420
    comp = Comp("battery-level--neon", Wn, Hn, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#B6FF3B", "outline": "#B6FF3B"}, "primary", "background", "outline")
    for i, (c, sz) in enumerate(seg_rects(bc, bw, bh, vertical=True)):
        if i >= LIT:
            comp.layer(f"off{i}", [group([rect(sz, c, 8), stroke(slot="primary", width=2, opacity=25)], "o")],
                       opacity=fade(4, 12))
            continue
        t = 12 + i * 7
        comp.layer(f"seg{i}", soft_glow([rect(sz, c, 8)], slot="primary", spread=(12, 28), ops=(26, 10)),
                   opacity=keys((t, 0, HOLD), (t + 1, 100, HOLD), (t + 3, 30, HOLD), (t + 5, 100)), ip=t)
        if i == LIT - 1:
            spark(comp, (c[0] + sz[0] / 2 - 6, c[1] - sz[1] / 2 + 4), t + 6, size=50)
    body(comp, "neon", bc, bw, bh, vertical=True)
    neon_panel(comp, 16, 16, Wn - 32, Hn - 32, r=34)
    return comp, {"value": (320, 250, 210, 84), "label": (320, 344, 210, 48)}


A = areas()
nc, na = neon()
build_asset(CAT, "battery-level", "Battery Level",
            "A battery that fills segment by segment. Put the percentage in the 'value' area beside it and a "
            "caption in 'label'.",
            ["battery", "charge", "level", "power", "energy", "percent", "infographic", "status"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Rounded battery outline; four of five segments pop in and the last one flashes."),
    V("charging", "Charging Loop", charging(), "loop", text_area=A["value"], text_areas=A, thumb_t=0.7,
      description="Looping charge: a lightning bolt pulses while the segments fill, blink full and drain."),
    V("neon", "Neon Upright", nc, "intro-hold", text_area=na["value"], text_areas=na, thumb_t=0.95,
      description="Upright neon battery on a dark panel; segments flicker on from the bottom up."),
])
