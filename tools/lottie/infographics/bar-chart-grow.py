from _common import *

W, H, F = 900, 600, 84
BASE = 470
X0 = 150            # first bar centre
STEP = 150
BW = 86
HMAX = 340
VALS = (0.45, 0.7, 0.55, 0.92, 0.74)
TOP = 3             # index of the highlighted (largest) bar


def bar_t(i):
    return 12 + i * 5


def areas(base=BASE, hmax=HMAX, x0=X0, step=STEP, dx=0):
    d = {}
    for i, v in enumerate(VALS):
        cx = x0 + i * step + dx
        d[f"label{i + 1}"] = (cx - 70, base + 16, 140, 44)
        d[f"value{i + 1}"] = (cx - 60, base - hmax * v - 56, 120, 44)
    return d


def axes(comp, style, gl_slot="background"):
    """Baseline, y axis with ticks and faint gridlines."""
    xl, xr = 60, W - 40
    grid = [polyline([(xl + 20, BASE - HMAX * q), (xr, BASE - HMAX * q)]) for q in (0.25, 0.5, 0.75, 1.0)]
    ticks = [polyline([(xl - 8, BASE - HMAX * q), (xl + 6, BASE - HMAX * q)]) for q in (0.25, 0.5, 0.75, 1.0)]
    dash = [6, 10] if style == "neon" else None
    comp.layer("grid", [group(grid + [trim(end=keys((2, 0, EXPO_OUT), (26, 100))),
                                      stroke(slot=gl_slot, width=2, opacity=14 if style != "neon" else 30,
                                             dashes=dash)], "grid")])
    comp.layer("ticks", [group(ticks + [stroke(slot=gl_slot, width=3, opacity=60)], "ticks")], opacity=fade(8, 16))
    comp.layer("yaxis", [group([polyline([(xl, BASE), (xl, BASE - HMAX - 20)]),
                                trim(end=keys((0, 0, EXPO_OUT), (18, 100))),
                                stroke(slot=gl_slot, width=3, opacity=60)], "y")])
    comp.layer("baseline", [group([polyline([(xl - 8, BASE), (xr, BASE)]), trim(end=keys((0, 0, EXPO_OUT), (20, 100))),
                                   stroke(slot=gl_slot, width=4, opacity=80)], "x")])


def flat():
    """Rounded bars spring up from the baseline one after another; the tallest is highlighted."""
    comp = Comp("bar-chart-grow", W, H, fps=30, frames=F)
    slots(comp, FLAT, "primary", "secondary", "background")
    for i, v in enumerate(VALS):
        cx, h, t = X0 + i * STEP, HMAX * v, bar_t(i)
        s = "secondary" if i == TOP else "primary"
        body = path(top_round_bar(cx, BW, BASE - h, BASE, 16))
        lay(comp, f"bar{i}", [group([body, gradient_fill([(0, "#FFFFFF", 0.22), (0.6, "#FFFFFF", 0)],
                                                         (cx - BW / 2, 0), (cx + BW / 2, 0))], "sheen"),
                              group([body, fill(slot=s)], "fill")],
            (cx, BASE), scale=keys((t, [100, 0], SPRING), (t + 20, [100, 100])), ip=t)
        if i == TOP:
            spark(comp, (cx + BW / 2 - 6, BASE - h + 4), t + 14, size=54)
    axes(comp, "flat")
    return comp


def neon():
    """Dark panel; outlined glowing bars shoot up with a white-hot cap and a soft fill."""
    comp = Comp("bar-chart-grow--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, "primary", "secondary", "background", "outline")
    for i, v in enumerate(VALS):
        cx, h, t = X0 + i * STEP, HMAX * v, bar_t(i)
        s = "secondary" if i == TOP else "primary"
        shape = rect((BW - 14, h), (cx, BASE - h / 2), 6)
        sc = keys((t, [100, 0], SPRING), (t + 20, [100, 100]))
        lay(comp, f"cap{i}", [group([polyline([(cx - BW / 2 + 12, BASE - h), (cx + BW / 2 - 12, BASE - h)]),
                                     stroke("#FFFFFF", width=5)], "cap"),
                              group([polyline([(cx - BW / 2 + 12, BASE - h), (cx + BW / 2 - 12, BASE - h)]),
                                     stroke(slot=s, width=22, opacity=35)], "g")],
            (cx, BASE), scale=sc, ip=t)
        lay(comp, f"bar{i}", glow_strokes([shape], slot=s, width=4, core=False, widths=(22, 12), ops=(8, 16))
            + [group([shape, fill(slot=s, opacity=22)], "fill")],
            (cx, BASE), scale=sc, ip=t)
        lay(comp, f"floor{i}", [group([ellipse((BW + 20, 18), (cx, BASE)), fill(slot=s, opacity=30)], "pool")],
            (cx, BASE), scale=keys((t, [0, 0], EXPO_OUT), (t + 14, [100, 100])), ip=t)
    axes(comp, "neon", gl_slot="outline")
    neon_panel(comp, 14, 14, W - 28, H - 28, r=34)
    return comp


def iso():
    """Isometric blocks rise out of a floor plate with staggered overshoot."""
    comp = Comp("bar-chart-grow--3d", W, H, fps=30, frames=F)
    slots(comp, FLAT, "primary", "secondary", "background")
    d, k = 34, 0.5          # side depth, slope
    base, x0, step, bw, hmax = BASE + 10, X0 - 20, STEP, 84, HMAX - 10
    for i, v in enumerate(VALS):
        x, h, t = x0 + i * step - bw / 2, hmax * v, bar_t(i)
        s = "secondary" if i == TOP else "primary"

        def faces(top):
            return ([(x, top), (x + bw, top), (x + bw, base), (x, base)],
                    [(x + bw, top), (x + bw + d, top - d * k), (x + bw + d, base - d * k), (x + bw, base)],
                    [(x, top), (x + d, top - d * k), (x + bw + d, top - d * k), (x + bw, top)])

        f0, f1 = faces(base - 2), faces(base - h)
        sp = lambda j: path(keys((t, bezier(f0[j]), SPRING), (t + 20, bezier(f1[j]))))
        comp.layer(f"top{i}", [group([sp(2), fill("#FFFFFF", 38), fill(slot=s)], "top")], ip=t)
        comp.layer(f"side{i}", [group([sp(1), fill("#000000", 30), fill(slot=s)], "side")], ip=t)
        comp.layer(f"front{i}", [group([sp(0), fill(slot=s)], "front"),
                                 group([sp(0), gradient_fill([(0, "#FFFFFF", 0.0), (1, "#FFFFFF", 0.14)],
                                                             (x, 0), (x + bw, 0))], "sheen")], ip=t)
    # floor plate
    px0, px1 = 40, W - 60
    plate = [(px0, base), (px1, base), (px1 + d, base - d * k), (px0 + d, base - d * k)]
    lip = [(px0, base), (px1, base), (px1, base + 16), (px0, base + 16)]
    lipr = [(px1, base), (px1 + d, base - d * k), (px1 + d, base - d * k + 16), (px1, base + 16)]
    sc = keys((0, [0, 100], EXPO_OUT), (18, [100, 100]))
    lay(comp, "plate", [group([polyline(plate, closed=True), fill(slot="background", opacity=22)], "p"),
                        group([polyline(lip, closed=True), fill(slot="background", opacity=12)], "l"),
                        group([polyline(lipr, closed=True), fill(slot="background", opacity=8)], "lr")],
        (W / 2, base), scale=sc, opacity=fade(0, 6))
    # back wall grid
    gl = [polyline([(px0 + d, base - d * k - hmax * q), (px1 + d, base - d * k - hmax * q)])
          for q in (0.25, 0.5, 0.75, 1.0)]
    comp.layer("grid", [group(gl + [trim(end=keys((4, 0, EXPO_OUT), (28, 100))),
                                    stroke(slot="background", width=2, opacity=16, dashes=[8, 8])], "g")])
    return comp


A = areas()
AI = areas(BASE + 26, HMAX - 10, X0 - 20, STEP, 0)
build_asset(CAT, "bar-chart-grow", "Bar Chart Grow",
            "Five-bar chart whose bars grow from the baseline with a staggered overshoot. Put the category "
            "names in 'label1'-'label5' under the bars and the numbers in 'value1'-'value5' above them.",
            ["bar", "chart", "graph", "column", "growth", "stats", "infographic", "data"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Rounded bars spring up in turn over a light grid; the tallest bar is highlighted."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["label1"], text_areas=A, thumb_t=0.95,
      description="Dark panel with dashed gridlines; glowing outlined bars shoot up with white-hot caps."),
    V("3d", "Isometric Blocks", iso(), "intro-hold", text_area=AI["label1"], text_areas=AI, thumb_t=0.95,
      description="Isometric blocks rise out of a floor plate with staggered overshoot."),
])
