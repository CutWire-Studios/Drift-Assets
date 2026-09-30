from _common import *
from lottie_kit import svg_shapes

W, H, F = 640, 640, 84
TW, TH = 520, 340
TC = (W / 2, 330)            # tile centre
PIN = (TC[0] + 30, TC[1] + 20)   # landing spot (tip)
TD = 14                      # drop start
TL = TD + 12                 # landing frame
PIN_D = "M0,0 C-8,-18 -30,-36 -30,-60 A30,30 0 1 1 30,-60 C30,-36 8,-18 0,0 Z"


def pin_shapes(scale=1.0, body_slot="primary", hole="#FFFFFF", style="flat"):
    s = scale
    body = svg_shapes(PIN_D, s)
    if style == "neon":
        return (glow_strokes(body, slot=body_slot, width=4, widths=(20, 12), ops=(10, 22))
                + [group([ellipse((22 * s, 22 * s), (0, -60 * s)), stroke(slot=body_slot, width=4)], "hole"),
                   group(body + [fill(slot="background")], "bg")])
    return [group([ellipse((22 * s, 22 * s), (0, -60 * s)), fill(hole)], "hole"),
            group([ellipse((60 * s, 60 * s), (-8 * s, -68 * s)),
                   gradient_fill([(0, "#FFFFFF", 0.35), (1, "#FFFFFF", 0)], (-14 * s, -76 * s), (18 * s, -60 * s),
                                 radial=True)], "shine"),
            group(body + [fill(slot=body_slot)], "body")]


def drop(comp, tip, parent=None, scale=1.0, style="flat", fall=280):
    x, y = tip
    ph = comp.null("pin", parent=parent,
             position=keys((TD, [x, y - fall], EASE_IN), (TL, [x, y], HOLD), (F, [x, y])),
             scale=keys((TD, [90, 110], LINEAR), (TL, [100, 100], EASE_OUT), (TL + 3, [120, 78], EASE_IN_OUT),
                        (TL + 10, [94, 108], EASE_IN_OUT), (TL + 17, [102, 98], EASE_IN_OUT), (TL + 24, [100, 100])))
    comp.layer("pin-body", pin_shapes(scale, style=style), parent=ph, ip=TD,
               opacity=fade(TD, TD + 3))
    return ph


def shadow(comp, tip, parent=None, w=64, h=20):
    comp.layer("pin-shadow", [group([ellipse((w, h), tip), fill("#000000", 35)], "s")], parent=parent,
               anchor=tip, position=tip, ip=TD,
               scale=keys((TD, [20, 20], EASE_IN), (TL, [100, 100], EASE_OUT), (TL + 3, [120, 110], EASE_IN_OUT),
                          (TL + 12, [100, 100])),
               opacity=keys((TD, 0, EASE_IN), (TL, 100)))


def map_content(style):
    """Map tile shapes centred on (0, 0); colours depend on the style."""
    if style == "neon":
        road, minor, water, park, block = None, None, None, None, None
    x0, y0 = -TW / 2, -TH / 2
    river = path(bezier([(x0 - 20, 60), (-90, 30), (40, 120), (TW / 2 + 20, 90)],
                        [(0, 0), (-50, 10), (-60, -10), (-40, 0)], [(40, 0), (50, -10), (60, 10), (0, 0)],
                        closed=False), "river")
    roads = [polyline([(x0, -40), (TW / 2, -60)]), polyline([(-60, y0), (-30, TH / 2)]),
             polyline([(120, y0), (150, TH / 2)])]
    minors = [polyline([(x0, -110), (TW / 2, -120)]), polyline([(-170, y0), (-160, 40)]),
              polyline([(40, y0), (50, 40)]), polyline([(x0, 10), (TW / 2, -2)])]
    blocks = [rect((70, 44), (-210, -78), 8), rect((80, 44), (-110, -78), 8), rect((70, 50), (0, -84), 8),
              rect((90, 44), (86, -90), 8), rect((70, 44), (200, -92), 8), rect((80, 34), (-100, -20), 8),
              rect((60, 40), (210, -30), 8), rect((72, 36), (-205, -142), 8), rect((66, 30), (205, -150), 8)]
    parkb = [ellipse((120, 70), (-10, -140)), ellipse((90, 54), (-40, -130))]
    return river, roads, minors, blocks, parkb


def tile_layers(comp, style, parent=None, off=(0, 0)):
    c = (TC[0] + off[0], TC[1] + off[1])
    river, roads, minors, blocks, parkb = map_content(style)
    if style == "neon":
        items = [group(roads + [stroke(slot="primary", width=3)], "roads"),
                 group(roads + [stroke(slot="primary", width=14, opacity=14)], "roads-glow"),
                 group(minors + [stroke(slot="outline", width=1.5, opacity=45)], "minor"),
                 group([river, stroke(slot="secondary", width=3, opacity=80)], "river"),
                 group([river, stroke(slot="secondary", width=26, opacity=10)], "river-glow"),
                 group(blocks + [stroke(slot="outline", width=1.5, opacity=30)], "blocks")]
    else:
        items = [group(roads + [stroke("#FFFFFF", width=16)], "roads"),
                 group(roads + [stroke("#C9D1DE", width=20)], "road-edge"),
                 group(minors + [stroke("#FFFFFF", width=8)], "minor"),
                 group(parkb + [fill("#B9E3B2")], "park"),
                 group([river, stroke("#9CCBF5", width=34)], "river"),
                 group(blocks + [fill("#DCE2EC")], "blocks")]
    comp.layer("map-matte", [group([rect((TW, TH), c, 26), fill()], "m")], parent=parent)
    comp.layer("map", [group(items, "content", position=c)], parent=parent, matte="alpha", opacity=fade(2, 8))


def label_chip(comp, t, style):
    c = (W / 2, 578)
    if style == "neon":
        shapes = glow_strokes([rect((400, 64), c, 12)], slot="primary", width=2.5, core=False, widths=(14,),
                              ops=(14,)) + [group([rect((400, 64), c, 12), fill(slot="background", opacity=90)], "b")]
    else:
        shapes = [group([rect((400, 64), c, 32), fill(slot="primary")], "chip"),
                  group([rect((400, 64), (c[0], c[1] + 6), 32), fill("#000000", 22)], "sh")]
    comp.layer("chip", shapes, anchor=(c[0], c[1] - 32), position=(c[0], c[1] - 32),
               scale=keys((t, [0, 0], SPRING), (t + 14, [100, 100])), ip=t)


def areas():
    return {"label": (W / 2 - 180, 552, 360, 52)}


def flat():
    """Top-down map tile; a pin drops, squashes on landing and sends out ripples, then the label chip pops."""
    comp = Comp("map-pin-drop", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FF4D5E", "background": "#EEF2F7"}, "primary", "background")
    label_chip(comp, TL + 8, "flat")
    drop(comp, PIN)
    for k in range(2):
        ring_pulse(comp, PIN, TL + k * 6, 16, 90, slot="primary", width=5 - k, dur=22, name=f"ripple{k}", yscale=100)
    shadow(comp, PIN)
    rg = rig(comp, "tile", TC, scale=keys((0, [80, 80], SOFT_SPRING), (18, [100, 100])))
    tile_layers(comp, "flat", parent=rg)
    comp.layer("tile", [group([rect((TW, TH), TC, 26), fill(slot="background")], "land"),
                        group([rect((TW, TH), (TC[0], TC[1] + 12), 26), fill("#000000", 22)], "sh")],
               parent=rg, opacity=fade(0, 5))
    return comp


def iso():
    """Isometric map slab; the pin drops onto it with a squash and flat ripples spread over the ground."""
    comp = Comp("map-pin-drop--3d", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FF4D5E", "background": "#EEF2F7"}, "primary", "background")
    label_chip(comp, TL + 8, "flat")
    cc = (TC[0], TC[1] - 10)
    # screen position of the landing spot after the iso transform
    dx, dy = PIN[0] - TC[0], PIN[1] - TC[1]
    a = math.radians(45)
    sx, sy = dx * math.cos(a) - dy * math.sin(a), (dx * math.sin(a) + dy * math.cos(a)) * 0.58
    tip = (cc[0] + sx, cc[1] + sy)
    drop(comp, tip, scale=1.15, fall=300)
    for k in range(2):
        ring_pulse(comp, tip, TL + k * 6, 16, 100, slot="primary", width=5 - k, dur=22, name=f"ripple{k}", yscale=58)
    shadow(comp, tip, w=70, h=24)
    intro = keys((0, [0, 40], EXPO_OUT), (22, [0, 0]))
    op = fade(0, 6)
    for name, off in (("top", 0), ("slab", 22)):
        squash = comp.null(f"{name}-squash", position=at((cc[0], cc[1] + off), intro), scale=(100, 58))
        spin = comp.null(f"{name}-spin", parent=squash, anchor=TC, rotation=keys((0, 20, EXPO_OUT), (26, 45)))
        if name == "top":
            tile_layers(comp, "flat", parent=spin)
            comp.layer("tile", [group([rect((TW, TH), TC, 26), fill(slot="background")], "land")], parent=spin,
                       opacity=op)
        else:
            comp.layer("slab", [group([rect((TW, TH), TC, 26), fill("#000000", 30), fill(slot="background")], "s")],
                        parent=spin, opacity=op)
            comp.layer("fill-between", [group([rect((TW, TH), TC, 26), fill("#000000", 30), fill(slot="background")],
                                              "s")], parent=spin, position=(0, -11), opacity=op)
            comp.layer("ground", [group([rect((TW + 60, TH + 60), TC, 50), fill("#000000", 9)], "g")], parent=spin,
                       position=(0, 30), opacity=op)
    return comp


def neon():
    """Dark holo-map with glowing streets; a neon pin drops in and radar rings sweep out."""
    comp = Comp("map-pin-drop--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#FF3DCB", "secondary": "#23E5FF", "outline": "#23E5FF"},
          "primary", "secondary", "background", "outline")
    label_chip(comp, TL + 8, "neon")
    drop(comp, PIN, style="neon")
    for k in range(3):
        ring_pulse(comp, PIN, TL + k * 8, 14, 110, slot="primary", width=3, dur=26, name=f"radar{k}")
    comp.layer("glow-spot", soft_glow([ellipse((40, 14), PIN)], slot="primary", spread=(16, 34), ops=(20, 8)),
               anchor=PIN, position=PIN, scale=keys((TL, [0, 0], EXPO_OUT), (TL + 10, [100, 100])), ip=TL)
    rg = rig(comp, "tile", TC, scale=keys((0, [90, 90], EXPO_OUT), (18, [100, 100])))
    tile_layers(comp, "neon", parent=rg)
    comp.layer("tile", glow_strokes([rect((TW, TH), TC, 22)], slot="outline", width=2.5, core=False, widths=(16,),
                                    ops=(12,), extra=[trim(end=keys((0, 0, EASE_IN_OUT), (20, 100)))])
               + [group([rect((TW, TH), TC, 22), fill(slot="background", opacity=92)], "bg")], parent=rg)
    return comp


A = areas()
build_asset(CAT, "map-pin-drop", "Map Pin Drop",
            "A location pin drops onto an abstract map tile with a squash and ripple, then a label chip pops under "
            "the map. Put the place name in the 'label' area.",
            ["map", "pin", "location", "place", "travel", "gps", "marker", "infographic"], [
    V("flat", "Flat Map", flat(), "intro-hold", text_area=A["label"], text_areas=A, thumb_t=0.95,
      description="Top-down map tile with roads, a river and a park; the pin drops and ripples."),
    V("3d", "Isometric", iso(), "intro-hold", text_area=A["label"], text_areas=A, thumb_t=0.95,
      description="Isometric map slab that swings into place; the pin drops onto it with flat ripples."),
    V("neon", "Neon Holo-map", neon(), "intro-hold", text_area=A["label"], text_areas=A, thumb_t=0.95,
      description="Dark holo-map with glowing streets; a neon pin drops in and radar rings sweep out."),
])
