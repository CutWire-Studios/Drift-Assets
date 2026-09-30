"""Lunar New Year lanterns: red lanterns with gold caps and tassels swaying on their strings (loops)."""

from _common import *

T = 90
RED, GOLD, DEEP = "#E0231C", "#FFC23D", "#9E0F0B"


def lantern_items(t_ph, amp, style="classic", w=150, h=124):
    """Lantern centred on its body; string attach at the top cap. Tassel lags the swing."""
    glow_style = style == "glow"
    cap_w = w * 0.46
    items = []
    # tassel: knot + fringe, swinging opposite to the body's sway
    fringe = group([
        group([rect((10, 12), (0, 8), 3), fill(GOLD, slot="accent")], "knot"),
        group(S("M 0 0 L 0 16") + [stroke(GOLD, 3, slot="accent")], "cord"),
        group(S("M -9 16 L 9 16 L 12 72 L -12 72 Z") + [fill(RED, slot="primary")], "fringe"),
        group(S("M -5 20 L -6 70 M 0 20 L 0 71 M 5 20 L 6 70") + [stroke(DEEP, 2)], "strands"),
        group([rect((22, 8), (0, 18), 3), fill(GOLD, slot="accent")], "band"),
    ], "tassel")
    fringe["it"][-1] = transform(shape=True, position=(0, h / 2 + 12),
                                 rotation=looped(lambda t: -amp * 0.8 * math.sin(TAU * (t / T + t_ph - 0.12)), T, 3))
    items.append(fringe)
    items.append(group([rect((cap_w, 16), (0, h / 2 + 4), 4), fill(GOLD, slot="accent")], "bottom-cap"))
    items.append(group([rect((cap_w, 16), (0, -h / 2 - 4), 4), fill(GOLD, slot="accent")], "top-cap"))
    items.append(group([rect((cap_w * 0.6, 8), (0, -h / 2 - 14), 3), fill("#E0A020")], "top-ring"))
    ribs = []
    for k in (-0.62, -0.3, 0, 0.3, 0.62):
        x = k * w / 2
        ribs += S(f"M {x * 0.55:.1f} {-h / 2 + 2} C {x * 1.25:.1f} {-h / 4} {x * 1.25:.1f} {h / 4} "
                  f"{x * 0.55:.1f} {h / 2 - 2}")
    items.append(group(ribs + [stroke(GOLD if glow_style else DEEP, 3 if glow_style else 4,
                                      60 if glow_style else 55)], "ribs"))
    if glow_style:
        items.append(group([ellipse((w, h)), gradient_fill([(0, "#FFF2B0"), (0.35, "#FF9A3A"), (1, RED)],
                                                           (0, 6), (w * 0.55, 6), radial=True)], "light"))
    else:
        items.append(group([ellipse((w, h)), shade_overlay((-w / 2, -h / 2, w / 2, h / 2), 0.9, dark="#3A0000")],
                           "shade"))
        items.append(group([ellipse((w, h)), fill(RED, slot="primary")], "body"))
    return items


def hanging(comp, name, top, length, t_ph, amp, style, scale=100, T_=T):
    string = comp.null(name, position=top, scale=(scale, scale),
                       rotation=looped(lambda t: amp * math.sin(TAU * (t / T_ + t_ph)), T_, 2))
    h = 124
    if style == "glow":
        comp.layer(name + "-halo", [glow(140, "#FF7A2A", 100, falloff=((0, 0.55), (0.5, 0.2), (1, 0)))],
                   parent=string, position=(0, length + h / 2 + 14),
                   opacity=looped(lambda t: 70 + 20 * flicker(t, T_, len(name)), T_, 2))
    comp.layer(name + "-lantern", lantern_items(t_ph, amp, style), parent=string, position=(0, length + h / 2 + 14))
    comp.layer(name + "-string", [group(S(f"M 0 0 L 0 {length}") + [stroke(GOLD if style == "glow" else DEEP, 3,
                                                                          slot="accent" if style == "glow" else None)],
                                        "s")], parent=string)
    return string


def classic():
    W, H = 900, 560
    comp = Comp("lunar-new-year-lanterns", W, H, frames=T)
    comp.slot("primary", RED)
    comp.slot("accent", GOLD)
    for i, (x, L, ph, s) in enumerate(((170, 110, 0.0, 125), (450, 50, 0.33, 160), (730, 150, 0.66, 120))):
        hanging(comp, f"l{i}", (x, 0), L, ph, 6, "classic", s)
    return comp


def glowing():
    W, H = 900, 600
    comp = Comp("lunar-new-year-lanterns--glow", W, H, frames=T)
    comp.slot("primary", RED)
    comp.slot("accent", GOLD)
    for i, (x, L, ph, s) in enumerate(((180, 150, 0.1, 120), (450, 110, 0.45, 150), (720, 180, 0.8, 115))):
        hanging(comp, f"l{i}", (x, 0), L, ph, 4, "glow", s)
    return comp


def border():
    W, H = 1920, 420
    comp = Comp("lunar-new-year-lanterns--border", W, H, frames=T)
    comp.slot("primary", RED)
    comp.slot("accent", GOLD)
    segs = [((-20 + 490 * i, 24), (-20 + 490 * (i + 1), 24), 70) for i in range(4)]
    items = []
    for j, (p0, p1, sag) in enumerate(segs):
        items.append(group([path(smooth_open(sag_pts(p0, p1, sag, 20))), stroke(DEEP, 5)], f"rope{j}"))
    for j, (p0, p1, sag) in enumerate(segs):
        for k, L in ((0.3, 40), (0.7, 110)):
            p = sag_at(p0, p1, sag, k)
            hanging(comp, f"l{j}-{k}", p, L, (j * 0.27 + k) % 1, 5, "classic", 72)
    comp.layer("rope", items)
    return comp


build("lunar-new-year-lanterns", "Lunar New Year Lanterns",
      "Red Lunar New Year lanterns with gold caps and tassels swaying gently on their strings; seamless loops "
      "that hang from the top of the frame.",
      ["lunar new year", "chinese new year", "lantern", "spring festival", "red", "gold", "festive"], [
          Variant("classic", "Classic Trio", classic(), "loop", thumb_t=0.2,
                  description="Three shaded red lanterns on strings of different lengths, swaying with lagging tassels."),
          Variant("glow", "Glowing", glowing(), "loop", thumb_t=0.2,
                  description="Lanterns lit from within with a warm gradient and a softly flickering halo."),
          Variant("border", "Top Border", border(), "loop", thumb_t=0.2, region=(470, 0, 520, 330),
                  description="A swagged rope across the top of the frame with eight small hanging lanterns."),
      ])
