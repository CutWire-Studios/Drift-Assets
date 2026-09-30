from _common import *

W, H, F = 900, 560, 90
XL, XR = 100, 840
BASE, TOPY = 450, 110
VALS = (0.22, 0.42, 0.34, 0.62, 0.55, 0.86)
T0, T1 = 10, 58
E = (0.45, 0.0, 0.3, 1.0)
N_AREA = 48


def points(dy=0):
    n = len(VALS)
    return [(XL + 40 + i * (XR - XL - 80) / (n - 1), BASE - (BASE - TOPY) * v + dy) for i, v in enumerate(VALS)]


class Curve:
    def __init__(self, pts, smooth=True, seed=None):
        self.pts = pts
        d = catmull(pts, 14) if smooth else densify(pts, 6)
        if seed is not None:
            d = wobble(pts, 2.2, seed, step=30, samples=6)
        self.dense = d
        self.cum = [0.0]
        for a, b in zip(d, d[1:]):
            self.cum.append(self.cum[-1] + math.dist(a, b))
        self.L = self.cum[-1]

    def at(self, s):
        s = max(0.0, min(self.L, s))
        for j in range(len(self.cum) - 1):
            if self.cum[j + 1] >= s:
                u = (s - self.cum[j]) / ((self.cum[j + 1] - self.cum[j]) or 1)
                a, b = self.dense[j], self.dense[j + 1]
                return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
        return self.dense[-1]

    def frac_of(self, p):
        j = min(range(len(self.dense)), key=lambda k: math.dist(self.dense[k], p))
        return self.cum[j] / self.L

    def progress(self, f, t0=T0, t1=T1):
        return ease_eval(E, (f - t0) / (t1 - t0))

    def trim(self, t0=T0, t1=T1):
        return trim(end=keys((t0, 0, E), (t1, 100)))

    def head(self, t0=T0, t1=T1):
        return anim([(f, list(self.at(self.progress(f, t0, t1) * self.L)), LINEAR) for f in range(t0, t1 + 1)])

    def area(self, base, t0=T0, t1=T1):
        ks = []
        for f in range(t0, t1 + 1):
            p = max(0.002, self.progress(f, t0, t1))
            top = [self.at(p * self.L * i / (N_AREA - 1)) for i in range(N_AREA)]
            poly = [(top[0][0], base)] + top + [(top[-1][0], base)]
            ks.append((f, bezier(poly), LINEAR))
        return path(anim(ks), "area")

    def dot_frame(self, i, t0=T0, t1=T1):
        return first_frame(E, t0, t1, self.frac_of(self.pts[i]))


def areas():
    p = points()
    d = {"title": (XL, 24, 480, 56)}
    lx, ly = p[-1]
    d["value"] = (lx - 150, ly - 96, 136, 52)
    for i, (x, _) in enumerate(p):
        d[f"label{i + 1}"] = (x - 55, BASE + 16, 110, 40)
    return d


def grid_lines(comp, slot, opacity, dashes=None, width=2):
    ls = [polyline([(XL, BASE - (BASE - TOPY) * q), (XR, BASE - (BASE - TOPY) * q)]) for q in (0.25, 0.5, 0.75, 1.0)]
    comp.layer("grid", [group(ls + [trim(end=keys((0, 0, EXPO_OUT), (24, 100))),
                                    stroke(slot=slot, width=width, opacity=opacity, dashes=dashes)], "g")])
    comp.layer("baseline", [group([polyline([(XL - 10, BASE), (XR, BASE)]), trim(end=keys((0, 0, EXPO_OUT), (20, 100))),
                                   stroke(slot=slot, width=4, opacity=70)], "b")])


def value_chip(comp, c, t, slot, style="flat"):
    lx, ly = c
    cx, cy = lx - 82, ly - 70
    shapes = [group([rect((150, 56), (cx, cy), 28), fill(slot=slot)], "chip"),
              group([polyline([(cx + 44, cy + 24), (lx - 6, ly - 12), (cx + 64, cy + 20)], closed=True),
                     fill(slot=slot)], "tail")]
    if style == "neon":
        shapes = [group([rect((150, 56), (cx, cy), 12), stroke(slot=slot, width=3)], "chip"),
                  group([rect((150, 56), (cx, cy), 12), stroke(slot=slot, width=16, opacity=15)], "glow"),
                  group([rect((150, 56), (cx, cy), 12), fill(slot="background", opacity=90)], "bg"),
                  group([polyline([(cx + 50, cy + 28), (lx - 6, ly - 12)]), stroke(slot=slot, width=3)], "leader")]
    comp.layer("chip", shapes, anchor=(lx, ly), position=(lx, ly), scale=pop(t, 14), ip=t)


def flat():
    """Smooth line draws across a light grid, dots pop at each point and the area fills beneath."""
    comp = Comp("line-chart-draw", W, H, fps=30, frames=F)
    slots(comp, FLAT, "primary", "secondary", "background")
    cv = Curve(points())
    p = points()
    value_chip(comp, p[-1], T1 + 2, "secondary")
    for i, c in enumerate(p):
        t = cv.dot_frame(i)
        comp.layer(f"dot{i}", [group([ellipse((14, 14), c), fill(slot="primary")], "in"),
                               group([ellipse((30, 30), c), fill("#FFFFFF")], "out")],
                   anchor=c, position=c, scale=pop(t, 12), ip=t)
    ring_pulse(comp, p[-1], T1, 18, 46, slot="primary", width=4)
    line = [path(bezier(cv.dense, closed=False), "line")]
    comp.layer("line", [group(line + [cv.trim(), stroke(slot="primary", width=8)], "line")])
    comp.layer("line-shadow", [group(line + [cv.trim(), stroke("#000000", width=8, opacity=18)], "s")],
               position=(0, 8))
    comp.layer("area", [group([cv.area(BASE), fill(slot="primary", opacity=22)], "a")], ip=T0)
    grid_lines(comp, "background", 14)
    return comp


def neon():
    """Dark panel; a glowing line races across with a spark at its head, dots flare and the area glows."""
    comp = Comp("line-chart-draw--neon", W, H, fps=30, frames=F)
    slots(comp, NEON, "primary", "secondary", "background", "outline")
    cv = Curve(points(), smooth=False)
    p = points()
    value_chip(comp, p[-1], T1 + 2, "secondary", "neon")
    comp.layer("head", [group([ellipse((14, 14)), fill("#FFFFFF")], "c"),
                        group([ellipse((40, 40)), fill(slot="primary", opacity=35)], "g")],
               position=cv.head(), ip=T0, op=T1 + 1)
    for i, c in enumerate(p):
        t = cv.dot_frame(i)
        comp.layer(f"dot{i}", [group([ellipse((10, 10), c), fill("#FFFFFF")], "core"),
                               group([ellipse((24, 24), c), stroke(slot="primary", width=4)], "ring"),
                               group([ellipse((24, 24), c), stroke(slot="primary", width=16, opacity=18)], "glow"),
                               group([ellipse((24, 24), c), fill(slot="background")], "bg")],
                   anchor=c, position=c, scale=pop(t, 12), ip=t)
        ring_pulse(comp, c, t, 12, 36, slot="primary", width=3, dur=14, name=f"flare{i}")
    line = [path(bezier(cv.dense, closed=False), "line")]
    comp.layer("line", glow_strokes(line, slot="primary", width=5, extra=[cv.trim()]))
    comp.layer("area", [group([cv.area(BASE), gradient_fill([(0, "#23E5FF", 0.32), (1, "#23E5FF", 0)],
                                                            (0, TOPY), (0, BASE))], "a")], ip=T0)
    ticks = [polyline([(x, BASE), (x, BASE + 10)]) for x, _ in p]
    comp.layer("xticks", [group(ticks + [stroke(slot="outline", width=2, opacity=50)], "t")], opacity=fade(10, 20))
    grid_lines(comp, "outline", 22, dashes=[5, 9])
    neon_panel(comp, 14, 14, W - 28, H - 28, r=34, grid=None)
    return comp


def sketch():
    """Paper card with hand-drawn axes; an ink line scrawls across, points get circled and the area is hatched."""
    comp = Comp("line-chart-draw--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH, "primary", "secondary", "background", "outline")
    paper = Paper(comp, 24, 16, W - 48, H - 32, tilt=-0.8, r=20)
    card = paper.rig
    p = points()
    cv = Curve(p, seed=4)
    for i, c in enumerate(p):
        t = cv.dot_frame(i)
        comp.layer(f"dot{i}", [ink([sketch_circle_pts(c, 11, seed=i, turns=1.15, amp=0.06, n=14)], width=4,
                                   draw=(t, t + 6)),
                               group([ellipse((20, 20), c), fill(slot="background")], "bg")],
                   parent=card, ip=t)
    comp.layer("line", [ink([cv.dense], width=6, draw=(T0, T1, E), slot="primary", color="#FF5A4E")], parent=card)
    # hatched area: diagonal lines clipped to the growing area polygon
    comp.layer("area-matte", [group([cv.area(BASE), fill("#FFFFFF")], "m")], parent=card, ip=T0)
    hatch = [polyline([(x, BASE + 10), (x + 180, TOPY - 40)]) for x in range(XL - 200, XR + 40, 16)]
    comp.layer("hatch", [group(hatch + [stroke(slot="secondary", width=3, opacity=70)], "h")], parent=card,
               matte="alpha", ip=T0)
    ax = [wobble([(XL - 10, BASE), (XR + 10, BASE)], 1.4, 1), wobble([(XL - 10, BASE), (XL - 12, TOPY - 40)], 1.4, 2),
          arrow_head((XR + 12, BASE), (XR - 10, BASE), 16), arrow_head((XL - 12, TOPY - 42), (XL - 12, TOPY), 16)]
    comp.layer("axes", [ink(ax, width=4.5, draw=(2, 22))], parent=card)
    gl = [wobble([(XL + 10, BASE - (BASE - TOPY) * q), (XR - 10, BASE - (BASE - TOPY) * q)], 1.2, 10 + k)
          for k, q in enumerate((0.33, 0.66, 1.0))]
    comp.layer("grid", [ink(gl, width=2, opacity=25, draw=(8, 26))], parent=card)
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "line-chart-draw", "Line Chart Draw",
            "A line chart that draws itself across a grid with points popping in and the area filling beneath. "
            "Put the chart title in 'title', the highlight number in 'value' and the axis labels in "
            "'label1'-'label6'.",
            ["line", "chart", "graph", "trend", "growth", "stats", "infographic", "data"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["title"], text_areas=A, thumb_t=0.95,
      description="Smooth line with white dots and a soft area fill; a value chip pops at the last point."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["title"], text_areas=A, thumb_t=0.95,
      description="Dark panel; a glowing line races across with a spark head, flaring dots and a glowing area."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=A["title"], text_areas=A, thumb_t=0.95,
      description="Paper card with hand-drawn axes, an ink line scrawled across, circled points and hatching."),
])
