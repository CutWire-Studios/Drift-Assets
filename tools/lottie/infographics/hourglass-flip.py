from _common import *

W, H, F = 440, 680, 120
C = (W / 2, 316)
HY = 180                 # interior half height
FLOW = 84                # sand runs 0..FLOW
FL0, FL1 = 90, 112       # flip


def hw(y):
    u = min(1.0, abs(y) / HY)
    return 11 + 84 * math.sin(math.pi / 2 * min(1.0, u / 0.82)) ** 1.25


def interior(pad=0, n=48):
    right = [(C[0] + hw(HY * (i / n * 2 - 1)) + pad, C[1] + HY * (i / n * 2 - 1)) for i in range(n + 1)]
    left = [(C[0] - hw(HY * (1 - i / n * 2)) - pad, C[1] + HY * (1 - i / n * 2)) for i in range(n + 1)]
    right[0] = (right[0][0], right[0][1] - pad)
    right[-1] = (right[-1][0], right[-1][1] + pad)
    left[0] = (left[0][0], left[0][1] + pad)
    left[-1] = (left[-1][0], left[-1][1] - pad)
    return right + left


def glass_path(pad=0):
    return path(bezier(interior(pad), closed=True), "glass")


def flip_rig(comp):
    return rig(comp, "hourglass", C,
               rotation=keys((0, 0, HOLD), (FL0, 0, (0.6, -0.3, 0.3, 1.25)), (FL1, 180, HOLD), (F, 180)),
               scale=keys((0, [100, 100], HOLD), (FL0, [100, 100], EASE_IN_OUT), (FL0 + 10, [84, 84], EASE_IN_OUT),
                          (FL1 + 2, [100, 100], HOLD), (F, [100, 100])))


def sand_layers(comp, parent, slot="primary", glow=False, stream_w=6):
    x, y = C
    big = 240
    te = (0.35, 0.0, 0.75, 0.8)
    top = rect(keys((0, [big, HY + 10], te), (FLOW, [big, 0], HOLD), (F, [big, 0])),
               keys((0, [x, y - (HY + 10) / 2], te), (FLOW, [x, y], HOLD), (F, [x, y])))
    # the bottom pile rises from the base to the pinch; a mound sits on top of it
    bk = keys((0, [x, y + HY + big / 2], (0.2, 0.0, 0.6, 1.0)), (FLOW, [x, y + big / 2], HOLD), (F, [x, y + big / 2]))
    bot = rect((big, big), bk)
    mk = []
    for i in range(9):
        f = FLOW * i / 8
        u = ease_eval((0.2, 0.0, 0.6, 1.0), i / 8)
        lvl = y + HY - HY * u
        h = 34 * math.sin(math.pi * min(1, u * 1.15)) if i < 8 else 0
        mk.append((f, bezier([(x - 120, lvl + 1), (x, lvl - h), (x + 120, lvl + 1)]), LINEAR))
    mk.append((F, mk[-1][1], LINEAR))
    mound = path(anim(mk), "mound")
    stream = rect((stream_w, HY), (x, y + HY / 2))
    shapes = [group([top, bot, mound, fill(slot=slot)], "piles"),
              group([stream, fill(slot=slot)], "stream",
                    opacity=keys((0, 0, HOLD), (2, 100, HOLD), (FLOW - 3, 100, EASE_IN), (FLOW, 0, HOLD), (F, 0)))]
    if glow:
        shapes.insert(0, group([top, bot, mound, gradient_fill([(0, "#FFFFFF", 0.35), (1, "#FFFFFF", 0)],
                                                               (x, y - 40), (x, y + 60), radial=True)], "hot"))
    comp.layer("sand-matte", [group([glass_path(-1), fill()], "m")], parent=parent)
    comp.layer("sand", shapes, parent=parent, matte="alpha")


def areas():
    return {"label": (60, H - 70, W - 120, 48)}


def caps(comp, parent, col, dark, r=12, w=260, h=26, name="caps"):
    x, y = C
    items = []
    for sgn in (-1, 1):
        cy = y + sgn * (HY + 8 + h / 2)
        items += [group([rect((w, h), (x, cy), r), fill(slot=col)], f"cap{sgn}"),
                  group([rect((w, 8), (x, cy + sgn * (h / 2 - 4)), 4), fill(dark, 30)], f"edge{sgn}")]
    # darker edge on top of the fill
    items = [items[1], items[0], items[3], items[2]]
    comp.layer(name, items, parent=parent)


def flat():
    """Minimal hourglass: sand pours into the bottom bulb, then the glass flips with a springy spin."""
    comp = Comp("hourglass-flip", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FFC247", "secondary": "#5B6CFF"}, "primary", "secondary", "outline")
    rg = flip_rig(comp)
    caps(comp, rg, "secondary", "#000000")
    comp.layer("shine", [group([polyline([(C[0] - 70, C[1] - 150), (C[0] - 78, C[1] - 60)]),
                                polyline([(C[0] - 70, C[1] + 150), (C[0] - 78, C[1] + 60)]),
                                stroke("#FFFFFF", width=7, opacity=50)], "s")], parent=rg)
    comp.layer("glass", [group([glass_path(4), stroke(slot="outline", width=7)], "rim")], parent=rg)
    sand_layers(comp, rg)
    comp.layer("glass-fill", [group([glass_path(4), fill(slot="outline", opacity=10)], "f")], parent=rg)
    return comp


def classic():
    """Wooden hourglass with turned pillars and glossy glass; sand runs through, then it flips over."""
    comp = Comp("hourglass-flip--classic", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#E9B872", "secondary": "#8A5530", "outline": "#FFFFFF"},
          "primary", "secondary", "outline")
    rg = flip_rig(comp)
    x, y = C
    # pillars in front
    pil = []
    for sx in (-1, 1):
        px = x + sx * 112
        pil.append(group([rect((16, 2 * HY + 16), (px, y), 8), fill(slot="secondary")], f"p{sx}"))
        for k in (-1, 0, 1):
            pil.insert(0, group([ellipse((26, 16), (px, y + k * 120)), fill(slot="secondary")], f"bead{sx}{k}"))
            pil.insert(0, group([ellipse((26, 16), (px, y + k * 120)), fill("#000000", 22)], f"bs{sx}{k}"))
    comp.layer("pillars", pil, parent=rg)
    caps(comp, rg, "secondary", "#000000", r=8, w=280, h=34)
    comp.layer("knobs", [group([ellipse((28, 16), (x + sx * 118, y + sy * (HY + 52))) for sx in (-1, 1)
                                for sy in (-1, 1)] + [fill(slot="secondary")], "k")], parent=rg)
    comp.layer("shine", [group([polyline([(x - 66, y - 150), (x - 76, y - 70)]),
                                polyline([(x - 66, y + 150), (x - 76, y + 70)]),
                                stroke("#FFFFFF", width=9, opacity=55)], "s"),
                         group([polyline([(x + 62, y - 150), (x + 68, y - 110)]),
                                stroke("#FFFFFF", width=5, opacity=40)], "s2")], parent=rg)
    comp.layer("glass", [group([glass_path(4), stroke(slot="outline", width=5, opacity=80)], "rim")], parent=rg)
    sand_layers(comp, rg)
    comp.layer("glass-fill", [group([glass_path(4), fill("#BFE3FF", 16)], "f")], parent=rg)
    comp.layer("back-pillar", [group([rect((14, 2 * HY + 16), (x, y), 7), fill(slot="secondary")], "bp"), group([rect((14, 2 * HY + 16), (x, y), 7), fill("#000000", 35)],
                                                       "bps")], parent=rg)
    return comp


def neon():
    """Dark panel; a neon hourglass drains glowing sand and spins over."""
    comp = Comp("hourglass-flip--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#FFB23D", "outline": "#23E5FF"}, "primary", "background", "outline")
    rg = flip_rig(comp)
    x, y = C
    capl = [polyline([(x - 125, y + s * (HY + 22)), (x + 125, y + s * (HY + 22))]) for s in (-1, 1)]
    comp.layer("caps", glow_strokes(capl, slot="outline", width=6, widths=(26, 14), ops=(8, 18)), parent=rg)
    comp.layer("glass", glow_strokes([glass_path(5)], slot="outline", width=3.5, widths=(22, 12), ops=(8, 16)),
               parent=rg)
    sand_layers(comp, rg, glow=True, stream_w=5)
    comp.layer("sand-glow", [group([ellipse((150, 60), (x, y + HY - 20)), fill(slot="primary", opacity=10)], "g")],
               parent=rg, opacity=keys((0, 30, LINEAR), (FLOW, 100, HOLD), (FL0, 100, EASE_IN), (FL0 + 8, 0, HOLD),
                                       (F - 10, 0, EASE_OUT), (F, 30)))
    neon_panel(comp, 16, 16, W - 32, H - 32, r=34)
    return comp


A = areas()
build_asset(CAT, "hourglass-flip", "Hourglass Flip",
            "Looping hourglass: the sand pours into the bottom bulb, then the glass flips over and it starts again. "
            "Put a caption such as a countdown or deadline in the 'label' area underneath.",
            ["hourglass", "timer", "time", "wait", "sand", "countdown", "deadline", "loading"], [
    V("flat", "Flat", flat(), "loop", text_area=A["label"], text_areas=A, thumb_t=0.4,
      description="Minimal hourglass with coloured caps; flips with a springy spin."),
    V("classic", "Classic Wood", classic(), "loop", text_area=A["label"], text_areas=A, thumb_t=0.4,
      description="Wooden hourglass with turned pillars and glossy glass."),
    V("neon", "Neon", neon(), "loop", text_area=A["label"], text_areas=A, thumb_t=0.4,
      description="Dark panel; a neon hourglass drains glowing sand and spins over."),
])
