from _broadcast2 import *

W, H = 800, 380
C = (W / 2, H / 2)
F = 60
FLICK = keys((0, 0, HOLD), (8, 0, HOLD), (9, 100, HOLD), (11, 15, HOLD), (14, 100, HOLD), (16, 35, HOLD),
             (19, 100, HOLD), (F, 100))
HUM = keys((19, 100, SINE), (34, 88, SINE), (49, 100, HOLD), (F, 100))


def lit_glow(shape, slot, spread=(16, 36, 64), ops=(40, 18, 8)):
    return [group([shape, stroke(slot=slot, width=s, opacity=o)], f"glow{s}") for s, o in zip(spread, ops)]


def classic():
    """Brushed-metal studio lamp box with screws; the red glass flickers on and hums."""
    comp = Comp("on-air-light", W, H, fps=30, frames=F)
    comp.slot("primary", "#FF2B2B")
    comp.slot("outline", "#2A2B30")
    fw, fh = 620, 200
    face = rect((fw, fh), C, 14)
    pl = rig(comp, "lamp", C, scale=keys((0, [70, 70], SPRING), (10, [100, 100])),
             opacity=keys((0, 0, EASE_OUT), (4, 100)))
    # hot spot + glass highlight on the lit face
    comp.layer("glass shine", [group([rect((fw - 30, 36), (C[0], C[1] - fh / 2 + 30), 12),
                                      fill("#FFFFFF", 16)], "shine")], parent=pl, opacity=FLICK)
    comp.layer("hotspot", [group([face, gradient_fill([(0, "#FFFFFF", 0.55), (0.45, "#FFFFFF", 0.12),
                                                       (1, "#FFFFFF", 0)], C, (C[0] + fw * 0.55, C[1]),
                                                      radial=True)], "hot")],
               parent=pl, opacity=keys((0, 0, HOLD), (8, 0, HOLD), (9, 100, HOLD), (11, 15, HOLD), (14, 100, HOLD),
                                       (16, 35, HOLD), (19, 100, SINE), (34, 70, SINE), (49, 100, HOLD), (F, 100)))
    comp.layer("lit", [group([face, fill(slot="primary")], "lit")], parent=pl, opacity=FLICK)
    comp.layer("unlit", [group([face, fill("#3B1113")], "unlit"),
                         group([face, gradient_fill([(0, "#FFFFFF", 0.10), (1, "#000000", 0.25)],
                                                    (0, C[1] - fh / 2), (0, C[1] + fh / 2))], "shade")],
               parent=pl)
    comp.layer("bezel", [group([rect((fw + 20, fh + 20), C, 20), fill("#0D0D10")], "bezel")], parent=pl)
    screws = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = (C[0] + sx * 330, C[1] + sy * 118)
            screws += [group([polyline([(p[0] - 5, p[1] - 5), (p[0] + 5, p[1] + 5)]), stroke("#55565C", 2.5)],
                             "slot"),
                       group([ellipse((16, 16), p), fill("#C9CBD1")], "screw")]
    comp.layer("screws", screws, parent=pl)
    comp.layer("housing", [
        group([rect((700, 280), C, 30), gradient_fill([(0, "#6B6D75"), (0.08, "#9FA1A8"), (0.5, "#56585F"),
                                                       (1, "#2B2C31")], (0, C[1] - 140), (0, C[1] + 140))],
              "metal"),
        group([rect((704, 284), C, 32), fill(slot="outline")], "rim")], parent=pl)
    comp.layer("halo", lit_glow(rect((704, 284), C, 32), "primary"), parent=pl,
               opacity=keys((0, 0, HOLD), (8, 0, HOLD), (9, 100, HOLD), (11, 15, HOLD), (14, 100, HOLD),
                             (16, 35, HOLD), (19, 100, SINE), (34, 75, SINE), (49, 100, HOLD), (F, 100)))
    return comp, (C[0] - fw / 2 + 40, C[1] - fh / 2 + 30, fw - 80, fh - 60)


def neon():
    """Neon tube frame on a dark acrylic plate, flickering on like a sign."""
    comp = Comp("on-air-light--neon", W, H, fps=30, frames=F)
    comp.slot("primary", "#FF2E4D")
    comp.slot("background", "#120A10")
    outer = rect((640, 230), C, 115)
    inner = rect((600, 190), C, 95)
    pl = rig(comp, "sign", C, opacity=keys((0, 0, EASE_OUT), (6, 100)),
             scale=keys((0, [92, 92], EXPO_OUT), (14, [100, 100])))
    comp.layer("tube", glow_strokes([outer], slot="primary", width=9), parent=pl, opacity=FLICK)
    comp.layer("tube2", glow_strokes([inner], slot="primary", width=4, core=False, widths=(18, 10), ops=(12, 22)),
               parent=pl, opacity=keys((0, 0, HOLD), (12, 0, HOLD), (13, 100, HOLD), (15, 20, HOLD), (21, 100, HOLD),
                                       (F, 100)))
    comp.layer("tube off", [group([outer, stroke("#5A2A33", 9)], "o"), group([inner, stroke("#4A2530", 4)], "i")],
               parent=pl)
    comp.layer("wash", [group([rect((620, 210), C, 105), fill(slot="primary", opacity=14)], "wash")],
               parent=pl, opacity=keys((0, 0, HOLD), (8, 0, HOLD), (9, 100, HOLD), (11, 15, HOLD), (14, 100, HOLD),
                                       (16, 35, HOLD), (19, 100, SINE), (34, 70, SINE), (49, 100, HOLD), (F, 100)))
    bolts = [group([ellipse((12, 12), (C[0] + sx * 336, C[1] + sy * 130)), fill("#8C8C96")], "bolt")
             for sx in (-1, 1) for sy in (-1, 1)]
    comp.layer("bolts", bolts, parent=pl)
    comp.layer("plate", [group([rect((712, 300), C, 22), fill(slot="background", opacity=88)], "plate"),
                         group([rect((712, 300), C, 22), stroke("#FFFFFF", 2, opacity=18)], "edge")], parent=pl)
    return comp, (C[0] - 250, C[1] - 70, 500, 140)


def retro():
    """Vintage stadium-shaped lamp with chrome rim and grille, mounted on a bracket, warming up."""
    comp = Comp("on-air-light--retro", W, H, fps=30, frames=F)
    comp.slot("primary", "#FF5A1F")
    comp.slot("secondary", "#6E1405")
    cy = C[1] - 10
    face = rect((600, 190), (C[0], cy), 95)
    warm = keys((0, 0, HOLD), (6, 0, EASE_IN), (22, 100, HOLD), (F, 100))
    pl = rig(comp, "lamp", (C[0], H - 10), rotation=keys((0, -4, SPRING), (18, 0)),
             opacity=keys((0, 0, EASE_OUT), (5, 100)))
    grille = [group([polyline([(C[0] - 300, cy - 60 + i * 20), (C[0] + 300, cy - 60 + i * 20)])], f"l{i}")
              for i in range(7)]
    comp.layer("grille matte", [group([face, fill("#FFFFFF")], "m")], parent=pl)
    comp.layer("grille", [group(grille + [stroke("#000000", 3, opacity=20, cap="butt")], "grille")], parent=pl,
               matte="alpha")
    comp.layer("shine", [group([rect((520, 40), (C[0], cy - 62), 20), fill("#FFFFFF", 22)], "shine")], parent=pl)
    comp.layer("hot", [group([face, gradient_fill([(0, "#FFF2C0", 0.85), (0.5, "#FFD27A", 0.25), (1, "#FFFFFF", 0)],
                                                  (C[0], cy), (C[0] + 330, cy), radial=True)], "hot")],
               parent=pl, opacity=keys((0, 0, HOLD), (6, 0, EASE_IN), (22, 100, SINE), (40, 80, SINE), (F, 100)))
    comp.layer("lit", [group([face, fill(slot="primary")], "lit")], parent=pl, opacity=warm)
    comp.layer("glass", [group([face, fill(slot="secondary")], "glass")], parent=pl)
    comp.layer("chrome", [
        group([rect((624, 214), (C[0], cy), 107), stroke("#1A1A1A", 3)], "line"),
        group([rect((636, 226), (C[0], cy), 113), gradient_fill(
            [(0, "#FFFFFF"), (0.35, "#B8BCC4"), (0.55, "#6E727B"), (0.8, "#D9DCE2"), (1, "#8D9199")],
            (0, cy - 113), (0, cy + 113))], "rim")], parent=pl)
    comp.layer("bracket", [group([polyline([(C[0] - 60, cy + 110), (C[0] - 30, H - 14), (C[0] + 30, H - 14),
                                            (C[0] + 60, cy + 110)], closed=True),
                                  fill("#3C3E44")], "bracket")], parent=pl)
    comp.layer("halo", lit_glow(rect((636, 226), (C[0], cy), 113), "primary", ops=(34, 16, 7)), parent=pl,
               opacity=warm)
    return comp, (C[0] - 230, cy - 60, 460, 120)


c1, t1 = classic()
c2, t2 = neon()
c3, t3 = retro()
build_asset(CAT, "on-air-light", "On Air Light",
            "Studio ON AIR lamp that flickers on and glows. Type ON AIR (or LIVE, RECORDING...) inside the "
            "lit face with the text tool.",
            ["on air", "studio", "live", "radio", "podcast", "lamp", "sign", "recording"], [
    V("classic", "Studio Box", c1, "intro-hold", text_area=t1, thumb_t=0.9,
            description="Brushed-metal lamp box with screws and a red glass face that flickers on and hums."),
    V("neon", "Neon Sign", c2, "intro-hold", text_area=t2, thumb_t=0.9, bg="e8e8ee",
            description="Double neon tube on a dark acrylic plate that stutters on like a sign."),
    V("retro", "Vintage Lamp", c3, "intro-hold", text_area=t3, thumb_t=0.9,
            description="Stadium-shaped vintage lamp with chrome rim and grille on a bracket; the glass warms up slowly."),
])
