from _common import *
from drift_lottie import Variant, build_asset

W, H = 680, 290
N = 120
Y = 124
IS = 128  # icon size
ICON = (24 + IS / 2, Y)
PL, PW, PH = ICON[0] + IS / 2 + 22, 470, 112
PILL = (PL + PW / 2, Y)
CLICK = 46
OUTRO = 96
TIP = (PILL[0] + 150, Y + 16)
IG_GRADIENT = [(0, "#FEDA75"), (0.22, "#FA7E1E"), (0.48, "#D62976"), (0.74, "#962FBF"), (1, "#4F5BD5")]


def out(keys, t0):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [106, 106], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


def ig_glyph(t0=6):
    """White camera glyph drawing itself on, centred on (0, 0) for a 128 px tile."""
    return [
        group([rect((78, 78), roundness=24), stroke("#FFFFFF", width=9.5),
               trim(end=anim([(t0, 0, SNAP_OUT), (t0 + 16, 100)]), offset=anim([(t0, 90, SNAP_OUT), (t0 + 16, 0)]))],
              "frame"),
        group([ellipse((38, 38)), stroke("#FFFFFF", width=9.5), trim(end=anim([(t0 + 4, 0, SNAP_OUT), (t0 + 18, 100)]))],
              "lens", rotation=-90),
        group([ellipse((12, 12)), fill("#FFFFFF")], "flash", position=(21, -21),
              scale=anim([(t0 + 8, [0, 0], SPRING), (t0 + 18, [100, 100])])),
    ]


def ig_tile(size=IS):
    return group([rect((size, size), roundness=size * 34 / 128),
                  gradient_fill(IG_GRADIENT, (-size * 0.42, size * 0.62), (size * 0.55, -size * 0.75), radial=True)],
                 "tile")


def icon_layer(comp, pos, click, outro, wiggle=True):
    rot = [(0, -18, SNAP_OUT), (16, 0, HOLD)]
    if wiggle:
        rot += [(click + 4, 0, EASE_IN_OUT), (click + 10, -8, EASE_IN_OUT), (click + 18, 4, EASE_IN_OUT), (click + 26, 0)]
    ig = comp.layer("instagram", ig_glyph() + [ig_tile()], position=pos, rotation=anim(rot),
                    scale=anim(out([(0, [0, 0], SPRING), (15, [100, 100], LINEAR), (click + 3, [100, 100], EASE_IN_OUT),
                                    (click + 10, [110, 110], EASE_IN_OUT), (click + 22, [100, 100], LINEAR)], outro + 3)))
    comp.layer("icon-shadow", [rect((IS, IS), roundness=34), fill("#000000", 22)], parent=ig, position=(0, 7))
    return ig


def pointer(comp):
    cursor(comp, [(20, [W + 60, H + 80], DECEL), (40, list(TIP), EASE_IN_OUT), (CLICK + 20, list(TIP), EASE_IN),
                  (CLICK + 36, [W + 60, H + 80])], [CLICK], ip=20, op=CLICK + 38, scale=4.0)


grow = [(6, 0, DECEL), (26, 1, LINEAR)]


def pill_grow():
    """Pill that slides out from behind the icon."""
    return rect(anim([(t, [PH + (PW - PH) * v, PH], e) for t, v, e in grow]), roundness=PH / 2,
                position=anim([(t, [-(PW - PH) * (1 - v) / 2, 0], e) for t, v, e in grow]))


def button_null(comp):
    return comp.null("button", position=PILL, scale=anim(out([
        (CLICK - 3, [100, 100], EASE_IN), (CLICK, [96, 90], SNAP_OUT), (CLICK + 3, [96, 90], OVERSHOOT),
        (CLICK + 15, [100, 100], LINEAR)], OUTRO)))


def base(name):
    comp = Comp(name, W, H, fps=30, frames=N)
    comp.marker("intro", 0, 84)
    comp.marker("outro", OUTRO, N - OUTRO)
    return comp


def classic():
    """Solid blue pill slides out of the app icon; the click turns it grey."""
    comp = base("follow-button-instagram")
    comp.slot("primary", "#0095F6")
    comp.slot("secondary", "#363636")
    pointer(comp)
    icon_layer(comp, ICON, CLICK, OUTRO)
    button = button_null(comp)
    click_wipe(comp, [pill(PW, PH)], (TIP[0] - PILL[0], TIP[1] - PILL[1]), CLICK, "secondary", parent=button)
    comp.layer("pill", [group([pill_grow(), fill(slot="primary")], "pill")], parent=button, op=CLICK + 13,
               opacity=anim([(6, 0, EASE_OUT), (9, 100)]))
    comp.layer("shadow", [group([pill_grow(), fill("#000000", 20)], "pill")], parent=button, position=(0, 7),
               opacity=anim([(6, 0, EASE_OUT), (9, 100)]))
    return comp


def outline():
    """Outlined pill that draws on around the text; the click fills it solid."""
    comp = base("follow-button-instagram--outline")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", "#D62976")
    pointer(comp)
    icon_layer(comp, ICON, CLICK, OUTRO)
    button = button_null(comp)
    click_wipe(comp, [pill(PW, PH)], (TIP[0] - PILL[0], TIP[1] - PILL[1]), CLICK, "primary", parent=button)
    comp.layer("ring", [pill(PW, PH), trim(end=anim([(8, 0, EASE_IN_OUT), (30, 100)]),
                                           offset=anim([(8, -40, EASE_IN_OUT), (30, 0)])),
                        stroke(slot="outline", width=6)], parent=button)
    comp.layer("tint", [pill(PW, PH), fill("#000000", 30)], parent=button,
               opacity=anim([(14, 0, EASE_OUT), (30, 100)]))
    return comp


def glass():
    """Frosted glass card holding the icon; a gradient sheen sweeps it and the click pulses a ring."""
    comp = base("follow-button-instagram--glass")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", "#FFFFFF")
    pointer(comp)
    cw, ch = W - 40, 176
    card = comp.null("card", position=(W / 2, Y), scale=anim(out([
        (0, [0, 0], SPRING), (16, [100, 100], LINEAR), (CLICK - 3, [100, 100], EASE_IN), (CLICK, [97, 94], SNAP_OUT),
        (CLICK + 3, [97, 94], OVERSHOOT), (CLICK + 15, [100, 100], LINEAR)], OUTRO)))
    comp.layer("pulse", [rect(anim([(CLICK, [cw, ch], DECEL), (CLICK + 18, [cw + 60, ch + 60])]),
                              roundness=anim([(CLICK, 44, DECEL), (CLICK + 18, 74)])),
                         stroke(slot="outline", width=anim([(CLICK, 5, EASE_OUT), (CLICK + 18, 1)]),
                                opacity=anim([(CLICK, 90, EASE_IN), (CLICK + 18, 0)]))],
               parent=card, ip=CLICK, op=CLICK + 19)
    comp.layer("icon", ig_glyph(8) + [ig_tile()], parent=card, position=(-cw / 2 + 24 + IS / 2, 0),
                      scale=anim([(4, [0, 0], SPRING), (18, [100, 100], LINEAR), (CLICK + 3, [100, 100], EASE_IN_OUT),
                                  (CLICK + 10, [112, 112], EASE_IN_OUT), (CLICK + 22, [100, 100])]))
    # a check dot appears after the click, tucked on the icon's corner
    comp.layer("check", [group([polyline([(-10, 0), (-3, 8), (11, -8)]), stroke("#FFFFFF", width=6),
                                trim(end=anim([(CLICK + 6, 0, EASE_OUT), (CLICK + 14, 100)]))], "tick"),
                         group([ellipse((40, 40)), fill("#0095F6")], "dot")],
               parent=card, position=(-cw / 2 + 24 + IS - 8, 44),
               scale=anim([(CLICK + 2, [0, 0], SPRING), (CLICK + 14, [100, 100])]), ip=CLICK + 2)
    # sheen: a soft diagonal band clipped to the card
    comp.layer("sheen-matte", [rect((cw, ch), roundness=44), fill()], parent=card)
    comp.layer("sheen", [group([rect((70, ch * 2)), fill("#FFFFFF", 22)], "band", rotation=20)], parent=card,
               matte="alpha", position=anim([(10, [-cw, 0], EASE_IN_OUT), (40, [cw, 0])]))
    comp.layer("rim", [rect((cw, ch), roundness=44), stroke(slot="outline", width=3, opacity=70)], parent=card)
    comp.layer("glass", [rect((cw, ch), roundness=44), fill(slot="primary", opacity=16)], parent=card)
    comp.layer("glass-shadow", [rect((cw, ch), roundness=44), fill("#000000", 18)], parent=card, position=(0, 9))
    return comp


def icon_pop():
    """No pill: the app icon bounces in, a plus badge pops on its corner and the click flips it to a check."""
    s = 330
    comp = Comp("follow-button-instagram--icon-pop", s, s, fps=30, frames=N)
    comp.marker("intro", 0, 70)
    comp.marker("outro", OUTRO, N - OUTRO)
    comp.slot("primary", "#0095F6")
    comp.slot("secondary", "#2ECC71")
    c = (s / 2 - 10, s / 2 + 6)
    click = 50
    tip = (c[0] + 74, c[1] + 70)
    cursor(comp, [(22, [s + 60, s + 80], DECEL), (40, list(tip), EASE_IN_OUT), (click + 18, list(tip), EASE_IN),
                  (click + 32, [s + 60, s + 80])], [click], ip=22, op=click + 34, scale=3.4)
    badge = comp.null("badge", position=(c[0] + IS / 2 - 6, c[1] + IS / 2 - 6),
                      scale=anim(out([(16, [0, 0], SPRING), (28, [100, 100], LINEAR), (click, [100, 100], EASE_IN),
                                      (click + 4, [80, 80], SPRING), (click + 14, [100, 100], LINEAR)], OUTRO)))
    comp.layer("plus", [group([polyline([(-13, 0), (13, 0)]), polyline([(0, -13), (0, 13)]),
                               stroke("#FFFFFF", width=7)], "plus")], parent=badge, op=click + 4,
               rotation=anim([(16, -90, SNAP_OUT), (30, 0)]))
    comp.layer("tick", [group([polyline([(-12, 1), (-3, 10), (13, -9)]), stroke("#FFFFFF", width=7),
                               trim(end=anim([(click + 4, 0, EASE_OUT), (click + 12, 100)]))], "tick")],
               parent=badge, ip=click + 4)
    click_wipe(comp, [ellipse((52, 52))], (0, 0), click + 1, "secondary", parent=badge, dur=8, reach=120)
    comp.layer("dot", [ellipse((52, 52)), fill(slot="primary"), stroke("#FFFFFF", width=5)], parent=badge)
    burst(comp, c, click + 2, 92, 134, count=10, width=7, rotation=18)
    icon_layer(comp, c, click, OUTRO)
    return comp


build_asset("call-to-action", "follow-button-instagram", "Follow Button Instagram",
            "Instagram app icon with a follow button; a pointer clicks it. Put your own \"Follow\" text "
            "inside the button.",
            ["follow", "instagram", "button", "click", "cursor", "social"], [
    Variant("classic", "Classic Pill", classic(), "intro-hold-outro", thumb_t=0.34,
            text_area=(PL + 36, Y - PH / 2 + 20, PW - 72, PH - 40),
            description="Blue follow pill slides out of the app icon; the click turns it grey."),
    Variant("outline", "Outline", outline(), "intro-hold-outro", thumb_t=0.3,
            text_area=(PL + 36, Y - PH / 2 + 20, PW - 72, PH - 40),
            description="White outline draws on around the pill; the click floods it with colour."),
    Variant("glass", "Glass Card", glass(), "intro-hold-outro", thumb_t=0.3, bg="3b2a55",
            text_area=(ICON[0] + IS / 2 + 30, Y - 50, W - 40 - IS - 90, 100),
            description="Frosted glass card with the app icon; a sheen sweeps across and a check pops after the click."),
    Variant("icon-pop", "Icon Pop", icon_pop(), "intro-hold-outro", thumb_t=0.8,
            description="Just the app icon with a plus badge that flips to a green check when clicked; no text area."),
])
