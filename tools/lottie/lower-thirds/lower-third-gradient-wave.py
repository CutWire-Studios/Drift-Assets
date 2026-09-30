from _lt2 import *

SHADE = [(0, "#FFFFFF", 0.26), (0.5, "#FFFFFF", 0.0), (1, "#000000", 0.28)]


def wave_edge(x0, x1, y, amp, lam, phase=0.0):
    """Points and bezier tangents of a sine edge from x0 to x1 (4 samples per wavelength)."""
    n = max(4, round((x1 - x0) / lam * 4))
    step = (x1 - x0) / n
    v, it, ot = [], [], []
    for i in range(n + 1):
        u = phase + 2 * math.pi * (x0 + i * step) / lam
        d = amp * 2 * math.pi / lam * math.cos(u)
        v.append((x0 + i * step, y + amp * math.sin(u)))
        it.append((-step / 3, -d * step / 3))
        ot.append((step / 3, d * step / 3))
    return v, it, ot


def wave_body(x0, x1, y, bottom, amp, lam, phase=0.0, name="wave"):
    v, it, ot = wave_edge(x0, x1, y, amp, lam, phase)
    it[0], ot[-1] = (0, 0), (0, 0)
    return path(bezier(v + [(x1, bottom), (x0, bottom)], it + [(0, 0)] * 2, ot + [(0, 0)] * 2, True), name)


def wave_line(x0, x1, y, amp, lam, phase=0.0):
    v, it, ot = wave_edge(x0, x1, y, amp, lam, phase)
    return path(bezier(v, it, ot, False), "line")


def ribbon(x0, x1, ytop, ybot, amp, lam, phase=0.0):
    v1, i1, o1 = wave_edge(x0, x1, ytop, amp, lam, phase)
    v2, i2, o2 = wave_edge(x0, x1, ybot, amp, lam, phase + 0.9)
    v2, i2, o2 = v2[::-1], [(-a, -b) for a, b in o2[::-1]], [(-a, -b) for a, b in i2[::-1]]
    i1[0], o1[-1], i2[0], o2[-1] = (0, 0), (0, 0), (0, 0), (0, 0)
    return path(bezier(v1 + v2, i1 + i2, o1 + o2, True), "ribbon")


def drift_x(dist, frames=N):
    """Constant horizontal flow over the whole clip."""
    return keys((0, [0, 0], LINEAR), (frames, [-dist, 0]))


def wave():
    W, H = 1150, 250
    x, w, top, bot, lam, amp = 50, 960, 74, 214, 300, 12
    comp = base("lower-third-gradient-wave", W, H, 30)
    comp.slot("primary", "#6C3BFF")
    comp.slot("accent", "#FF5FA2")
    box = (x, top - 40, w, bot - top + 40)
    flow = 2 * lam
    wipe(comp, "crest", [wave_line(x - 20, x + w + flow + 20, top - 16, amp * 0.8, lam, 1.3),
                         stroke(slot="accent", width=5)],
         box, 6, 30, 120, 140, "left", position=drift_x(flow))
    wipe(comp, "shade", [wave_body(x, x + w + flow, top, bot, amp, lam), gradient_fill(SHADE, (x, 0), (x + w, 0))],
         box, 0, 26, 122, 142, "left", position=drift_x(flow))
    wipe(comp, "body", [wave_body(x, x + w + flow, top, bot, amp, lam), fill(slot="primary")],
         box, 0, 26, 122, 142, "left", position=drift_x(flow))
    return comp, (x + 50, top + 28, w - 100, 62), (x + 50, top + 96, w - 200, 30)


def layered():
    W, H = 1150, 260
    x, w, bot, lam = 50, 960, 230, 360
    comp = base("lower-third-gradient-wave--layered", W, H, 36)
    comp.slot("primary", "#0077B6")
    comp.slot("secondary", "#90E0EF")
    box = (x, 0, w, bot)
    flow = 2 * lam

    def rising(dy, t0, t2):
        return keys((0, [0, dy], HOLD), (t0, [0, dy], EXPO_OUT), (t0 + 24, [-flow * (t0 + 24) / N, 0], LINEAR),
                    (t2, [-flow * t2 / N, 0], EXPO_IN), (t2 + 20, [-flow * (t2 + 20) / N, dy]))

    for nm, top, amp, ph, slot, t0, t2, grad in (("front", 92, 13, 0.0, "primary", 8, 118, True),
                                                 ("back", 56, 16, 2.2, "secondary", 0, 124, False)):
        items = [wave_body(x, x + w + flow, top, bot, amp, lam, ph)]
        if grad:
            wipe(comp, f"{nm}-shade", items + [gradient_fill(SHADE, (x, 0), (x + w, 0))], box, 0, 1, 148, 149,
                 "left", ein=LINEAR, eout=LINEAR, position=rising(bot - top + 30, t0, t2))
        wipe(comp, nm, items + [fill(slot=slot)], box, 0, 1, 148, 149, "left", ein=LINEAR, eout=LINEAR,
             position=rising(bot - top + 30, t0, t2))
    return comp, (x + 50, 122, w - 100, 60), (x + 50, 186, w - 200, 30)


def centred():
    W, H = 1100, 230
    cx, w, lam, amp = 550, 860, 240, 9
    x = cx - w / 2
    ytop, ybot = 62, 176
    comp = base("lower-third-gradient-wave--ribbon", W, H, 30)
    comp.slot("primary", "#FF7B00")
    comp.slot("secondary", "#FFD000")
    flow = 2 * lam
    box = (x, 30, w, 180)
    wipe(comp, "shade", [ribbon(x, x + w + flow, ytop, ybot, amp, lam), gradient_fill(SHADE, (x, 0), (x + w, 0))],
         box, 0, 24, 122, 140, "centre", position=drift_x(flow))
    wipe(comp, "body", [ribbon(x, x + w + flow, ytop, ybot, amp, lam), fill(slot="primary")],
         box, 0, 24, 122, 140, "centre", position=drift_x(flow))
    wipe(comp, "under", [ribbon(x, x + w + flow, ytop + 10, ybot + 10, amp, lam), fill(slot="secondary")],
         box, 4, 28, 118, 136, "centre", position=drift_x(flow))
    return comp, (x + 60, ytop + 22, w - 120, ybot - ytop - 44)


a, ah, asub = wave()
b, bh, bs = layered()
c, chd = centred()
build("lower-third-gradient-wave", "Gradient Wave Lower Third",
      "Lower-third bar whose top edge is a gently flowing wave, shaded with a soft gradient. Put your name in "
      "the bar and a subtitle below it.",
      ["lower third", "wave", "gradient", "flowing", "smooth", "modern", "water"], [
          V("wave", "Wave Bar", a, ah, asub,
            description="Wavy-topped gradient bar wipes in from the left with an accent crest line riding above."),
          V("layered", "Layered Waves", b, bh, bs,
            description="Two wave layers in different colours rise from the bottom and keep flowing."),
          V("ribbon", "Wave Ribbon", c, chd,
            description="Centred single-line ribbon with waves on both edges, opening from the middle."),
      ])
