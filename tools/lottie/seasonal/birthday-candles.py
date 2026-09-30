"""Birthday candles: striped candles with flickering flames; a blow-out variant and a cupcake."""

from _common import *

T = 60
COLS = [("primary", "#FF6FA5"), ("secondary", "#63C5FF"), ("accent", "#FFCB3D")]


def candle(comp, name, x, base_y, h, sid, col, w=36, T_=T, parent=None):
    """Candle body with diagonal stripes (matte-clipped), wax drip and wick. Returns top y."""
    top = base_y - h
    body = [rect((w, h), (x, base_y - h / 2), 7)]
    comp.layer(name + "-wick", [group(S(f"M {x} {top + 2} C {x + 1} {top - 6} {x - 2} {top - 10} {x + 1} {top - 16}")
                                      + [stroke("#3A2A22", 4)], "wick")], parent=parent)
    comp.layer(name + "-shade", [group(body + [gradient_fill([(0, WHITE, 0.35), (0.35, WHITE, 0), (0.7, "#000000", 0),
                                                              (1, "#000000", 0.25)], (x - w / 2, 0), (x + w / 2, 0))],
                                       "shade")], parent=parent)
    comp.layer(name + "-drip", [group(S(f"M {x - w / 2} {top + 4} L {x + w / 2} {top + 4} L {x + w / 2} {top + 20} "
                                        f"C {x + w / 2} {top + 30} {x + 6} {top + 30} {x + 6} {top + 20} "
                                        f"C {x + 6} {top + 36} {x - 8} {top + 36} {x - 8} {top + 22} "
                                        f"C {x - 8} {top + 16} {x - w / 2} {top + 18} {x - w / 2} {top + 12} Z")
                                      + [fill(WHITE, 92)], "drip"),
                                group([ellipse((w, 10), (x, top + 4)), fill(WHITE)], "cap")], parent=parent)
    comp.layer(name + "-matte", [group(body + [fill(WHITE)], "m")], parent=parent)
    stripes = []
    for k in range(-2, int(h / 26) + 3):
        y = top + k * 26
        stripes.append(S(f"M {x - w} {y} L {x + w} {y - 26} L {x + w} {y - 14} L {x - w} {y + 12} Z"))
    comp.layer(name + "-stripes", [group(sum(stripes, []) + [fill(WHITE, 90)], "stripes")], parent=parent,
               matte="alpha")
    comp.layer(name + "-body", [group(body + [fill(col, slot=sid)], "body")], parent=parent)
    return top - 14


def classic():
    W, H = 440, 420
    comp = Comp("birthday-candles", W, H, frames=T)
    for sid, c in COLS:
        comp.slot(sid, c)
    spots = [(W / 2 - 110, 150, 0), (W / 2, 190, 1), (W / 2 + 110, 165, 2)]
    tops = []
    for j, (x, h, ci) in enumerate(spots):
        tops.append((x, 380 - h))
    for j, (x, ty) in enumerate(tops):
        flame_layers(comp, f"flame{j}", T, h=62, w=17, seed=j * 7 + 1, position=(x, ty - 12), halo_r=90)
    for j, (x, h, ci) in enumerate(spots):
        sid, col = COLS[ci]
        candle(comp, f"candle{j}", x, 380, h, sid, col)
    comp.layer("plate", [ellipse((380, 34)), fill("#000000", 22)], position=(W / 2, 384))
    return comp


def blowout():
    W, H = 440, 460
    TT = 96
    comp = Comp("birthday-candles--blow-out", W, H, frames=TT)
    for sid, c in COLS:
        comp.slot(sid, c)
    spots = [(W / 2 - 110, 150, 0), (W / 2, 190, 1), (W / 2 + 110, 165, 2)]
    out_t = [44, 40, 47]
    for j, (x, h, ci) in enumerate(spots):
        ty = 420 - h - 12
        t0 = out_t[j]
        # wind: the flame leans away, stretches thin and snuffs out
        lean = comp.null(f"lean{j}", position=(x, ty), rotation=anim([(t0 - 12, 0, EASE_IN), (t0 - 4, 28, EASE_IN_OUT),
                                                                      (t0, 50)]),
                         scale=anim([(t0 - 12, [100, 100], EASE_IN), (t0 - 3, [80, 115], EASE_IN), (t0, [0, 40])]))
        flame_layers(comp, f"flame{j}", TT, h=62, w=17, seed=j * 7 + 1, parent=lean, halo_r=90, op=t0 + 1)
        # ember on the wick after it goes out
        comp.layer(f"ember{j}", [ellipse((7, 7)), fill("#FF6A1A")], position=(x, ty - 2), ip=t0,
                   opacity=anim([(t0, 100, EASE_IN), (t0 + 30, 0)]))
        # smoke curls
        for s in range(3):
            s0 = t0 + s * 5

            def smoke(t, x=x, ty=ty, s=s):
                pts = []
                for i in range(7):
                    k = i / 6
                    pts.append((x + 26 * math.sin(k * 5 + t * 0.12 + s) * k, ty - 10 - k * 150))
                return smooth_open(pts)
            comp.layer(f"smoke{j}-{s}", [group([morph(smoke, s0, s0 + 40, 2),
                                                trim(start=anim([(s0 + 6, 0, EASE_IN_OUT), (s0 + 40, 100)]),
                                                     end=anim([(s0, 0, EASE_OUT), (s0 + 24, 100)])),
                                                stroke("#D8D8E0", 11 - s * 2.5, 60)], "curl")],
                       ip=s0, op=min(TT, s0 + 41), position=(0, -s * 8))
    for j, (x, h, ci) in enumerate(spots):
        sid, col = COLS[ci]
        candle(comp, f"candle{j}", x, 420, h, sid, col, T_=TT)
    comp.layer("plate", [ellipse((380, 34)), fill("#000000", 22)], position=(W / 2, 424))
    return comp


def cupcake():
    W, H = 420, 520
    comp = Comp("birthday-candles--cupcake", W, H, frames=T)
    comp.slot("primary", "#FF8FC0")
    comp.slot("secondary", "#8E5A3C")
    comp.slot("accent", "#63C5FF")
    cx = W / 2
    flame_layers(comp, "flame", T, h=66, w=18, seed=5, position=(cx, 166), halo_r=100)
    candle(comp, "candle", cx, 266, 90, "accent", "#63C5FF", w=30)
    r = rng(6)
    sprinkles = []
    cols = ["#FFE14A", "#5BE0A0", "#63C5FF", "#FFFFFF", "#FF5A7A"]
    for i in range(22):
        a = r.uniform(0, TAU)
        rr = r.uniform(0.2, 1)
        p = (cx + 125 * rr * math.cos(a), 312 + 30 * rr * math.sin(a))
        sprinkles.append(group([rect((14, 5), roundness=2.5), fill(cols[i % 5])], f"s{i}", position=p,
                               rotation=r.uniform(0, 180)))
    comp.layer("sprinkles", sprinkles)
    frost = S("M 60 360 C 30 356 40 316 74 318 C 60 290 100 262 130 282 C 140 250 190 238 210 258 "
              "C 230 238 280 250 290 282 C 320 262 360 290 346 318 C 380 316 390 356 360 360 Z")
    swirl = S("M 110 300 C 160 318 260 318 310 300 M 150 270 C 190 282 240 282 270 270")
    comp.layer("frosting", [group(swirl + [stroke("#C9457F", 5, 45)], "swirl"),
                            group(frost + [shade_overlay((40, 240, 380, 360), 0.8, dark="#6A0030")], "shade"),
                            group(frost + [fill("#FF8FC0", slot="primary")], "cream")],
               scale=looped(lambda t: [100 + 1.2 * wave(t, T, 1), 100 - 1.2 * wave(t, T, 1)], T, 3),
               anchor=(cx, 360), position=(cx, 360))
    liner = S("M 70 356 L 350 356 L 318 480 L 102 480 Z")
    pleats = S(" ".join(f"M {70 + 280 * k / 8} 356 L {102 + 216 * k / 8} 480" for k in range(1, 8)))
    comp.layer("liner", [group(pleats + [stroke("#000000", 4, 22)], "pleats"),
                         group(liner + [gradient_fill([(0, WHITE, 0.25), (0.4, WHITE, 0), (1, "#000000", 0.25)],
                                                      (70, 0), (350, 0))], "shade"),
                         group(liner + [fill("#8E5A3C", slot="secondary")], "cup")])
    comp.layer("shadow", [ellipse((260, 26)), fill("#000000", 24)], position=(cx, 484))
    return comp


build("birthday-candles", "Birthday Candles",
      "Striped birthday candles with softly flickering flames; also a blow-out moment and a cupcake. "
      "Great next to a birthday message.",
      ["birthday", "candles", "cake", "party", "celebration", "flame", "cupcake"], [
          Variant("classic", "Three Candles", classic(), "loop", thumb_t=0.3,
                  description="Three striped candles of different heights with flickering flames and a warm glow."),
          Variant("blow-out", "Blow Out", blowout(), "intro-hold", thumb_t=0.4,
                  description="The flames lean in a puff of breath and go out, leaving curling smoke and embers."),
          Variant("cupcake", "Cupcake", cupcake(), "loop", thumb_t=0.3,
                  description="A frosted cupcake with sprinkles and a single flickering candle."),
      ])
