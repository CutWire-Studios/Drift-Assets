"""Parameterised follow button shared by the platform follow-button-* assets.

Same motion as follow-button-instagram: the app icon springs in, a pill slides out of it and a
pointer clicks it. Each platform only supplies its icon (Simple Icons glyph + authentic tile shape
and colours) and its button colours:

    from _platforms import Platform, build_platform
    build_platform(Platform("follow-button-facebook", "Facebook", FACEBOOK, kind="knockout", ...))

Icon kinds (everything is drawn centred on (0, 0) for an IS px icon):
  tile      a coloured tile (shape "squircle" / "circle") with the glyph on top in `glyph_color`.
  knockout  the Simple Icons path is the whole icon (e.g. a circle with the logo cut out); it is
            filled with the brand colour over a `backing` shape so the cut-out shows `glyph_color`.
"""

from _common import *  # noqa: F401,F403
from _common import SPRING, DECEL, cursor, burst, click_wipe, pill, glyph
from drift_lottie import Variant, build_asset
from lottie_kit import (Comp, anim, ellipse, fill, gradient_fill, group, polyline, rect, stroke, trim,  # noqa: F401
                        EASE_IN, EASE_OUT, EASE_IN_OUT, SNAP_OUT, OVERSHOOT, LINEAR, HOLD)

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
PILL_TEXT = (PL + 36, Y - PH / 2 + 20, PW - 72, PH - 40)


class Platform:
    """Everything that differs between platforms.

    glyph: Simple Icons path d (24x24 box).
    kind: "tile" or "knockout" (see module doc). shape: "squircle" | "circle" | "custom" (knockout only).
    tile: "#RRGGBB" or gradient (stops, start, end, radial) with start/end as fractions of IS.
    glyph_color / glyph_size (fraction of IS) / glyph_offset (px) / glyph_stroke ((colour, width px)).
    backing: knockout only, [("ellipse", cx, cy, w, h) | ("rect", cx, cy, w, h, r)] in 24-box units.
    path_fill: knockout only, colour or gradient like `tile`.
    rim: faint light rim around dark icons so they read on dark video.
    primary / secondary: pill colour and its clicked ("following") colour.
    done / badge_icon / tick: icon-pop badge colour after the click, the plus colour and the tick colour.
    second: "glass" or "outline". glass_bg: thumbnail backdrop for the glass card.
    bg: thumbnail backdrop for the other variants (None = default dark).
    verb: the word the user will likely type ("Follow", "Subscribe", "Join").
    """

    def __init__(self, asset_id, name, glyph, kind="tile", shape="squircle", roundness=0.265, tile="#000000",
                 glyph_color="#FFFFFF", glyph_size=0.56, glyph_offset=(0, 0), glyph_stroke=None,
                 backing=None, path_fill=None, rim=False, primary="#0095F6", secondary="#363636",
                 done="#2ECC71", badge_icon="#FFFFFF", tick="#FFFFFF", second="glass", glass_bg="2b2f3a", bg=None,
                 verb="Follow", tags=(), badge_at=None, icon_scale=1.0):
        self.id, self.name, self.glyph, self.kind, self.shape = asset_id, name, glyph, kind, shape
        self.roundness, self.tile = roundness, tile
        self.glyph_color, self.glyph_size, self.glyph_offset, self.glyph_stroke = \
            glyph_color, glyph_size, glyph_offset, glyph_stroke
        self.backing, self.path_fill, self.rim = backing or [], path_fill, rim
        self.primary, self.secondary, self.done, self.badge_icon, self.tick = primary, secondary, done, badge_icon, tick
        self.second, self.glass_bg, self.bg, self.verb = second, glass_bg, bg, verb
        self.tags = list(tags)
        self.icon_scale = icon_scale
        if badge_at is None:
            badge_at = (IS / 2 - 14, IS / 2 - 14) if shape == "circle" else (IS / 2 - 6, IS / 2 - 6)
        self.badge_at = badge_at


# ---------------------------------------------------------------- icon

def _paint(spec, size, opacity=100):
    """Solid fill for a hex colour, gradient fill for (stops, start, end, radial)."""
    if isinstance(spec, str):
        return fill(spec, opacity)
    stops, a, b, radial = spec
    return gradient_fill(stops, (a[0] * size, a[1] * size), (b[0] * size, b[1] * size), radial=radial,
                         opacity=opacity)


def _outline_shape(p, size):
    if p.shape == "circle":
        return ellipse((size, size))
    return rect((size, size), roundness=size * p.roundness)


def _backing(p, size):
    s = size / 24
    items = []
    for b in p.backing:
        if b[0] == "ellipse":
            items.append(ellipse((b[3] * s, b[4] * s), ((b[1] - 12) * s, (b[2] - 12) * s)))
        else:
            items.append(rect((b[3] * s, b[4] * s), ((b[1] - 12) * s, (b[2] - 12) * s), roundness=b[5] * s))
    return items


def icon_shapes(p, size=IS, t0=6):
    """The platform icon, centred on (0, 0); the glyph pops in at t0."""
    size = size * p.icon_scale
    pop = dict(scale=anim([(t0, [0, 0], SPRING), (t0 + 14, [100, 100])]),
               rotation=anim([(t0, -30, SNAP_OUT), (t0 + 16, 0)]))
    if p.kind == "tile":
        gs = size * p.glyph_size
        paint = [fill(p.glyph_color)]
        if p.glyph_stroke:
            paint = [stroke(p.glyph_stroke[0], width=p.glyph_stroke[1] * size / 128)] + paint
        items = [group(glyph(p.glyph, gs, (p.glyph_offset[0] * size / 128, p.glyph_offset[1] * size / 128))
                       + paint, "glyph", **pop)]
        tile = [_outline_shape(p, size), _paint(p.tile, size)]
        if p.rim:
            tile.insert(1, stroke("#FFFFFF", width=3, opacity=26))
        return items + [group(tile, "tile")]
    # knockout: the brand path over a backing that fills the cut-out glyph
    items = [group(glyph(p.glyph, size) + [_paint(p.path_fill, size)], "logo")]
    if p.rim:
        items.insert(0, group([_outline_shape(p, size), stroke("#FFFFFF", width=3, opacity=26)], "rim"))
    items.append(group(_backing(p, size) + [fill(p.glyph_color)], "cutout",
                       scale=anim([(t0, [0, 0], DECEL), (t0 + 12, [100, 100])])))
    return items


def icon_shadow(p, size=IS):
    size = size * p.icon_scale
    if p.kind == "tile":
        return [_outline_shape(p, size), fill("#000000", 22)]
    return glyph(p.glyph, size) + [fill("#000000", 22)]


def out(keys, t0):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [106, 106], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


def icon_layer(comp, p, pos, click, outro, wiggle=True):
    rot = [(0, -18, SNAP_OUT), (16, 0, HOLD)]
    if wiggle:
        rot += [(click + 4, 0, EASE_IN_OUT), (click + 10, -8, EASE_IN_OUT), (click + 18, 4, EASE_IN_OUT), (click + 26, 0)]
    ic = comp.layer(p.id.replace("follow-button-", ""), icon_shapes(p), position=pos, rotation=anim(rot),
                    scale=anim(out([(0, [0, 0], SPRING), (15, [100, 100], LINEAR), (click + 3, [100, 100], EASE_IN_OUT),
                                    (click + 10, [110, 110], EASE_IN_OUT), (click + 22, [100, 100], LINEAR)], outro + 3)))
    comp.layer("icon-shadow", icon_shadow(p), parent=ic, position=(0, 7))
    return ic


# ---------------------------------------------------------------- button parts

def pointer(comp):
    cursor(comp, [(20, [W + 60, H + 80], DECEL), (40, list(TIP), EASE_IN_OUT), (CLICK + 20, list(TIP), EASE_IN),
                  (CLICK + 36, [W + 60, H + 80])], [CLICK], ip=20, op=CLICK + 38, scale=4.0)


_GROW = [(6, 0, DECEL), (26, 1, LINEAR)]


def pill_grow():
    """Pill that slides out from behind the icon."""
    return rect(anim([(t, [PH + (PW - PH) * v, PH], e) for t, v, e in _GROW]), roundness=PH / 2,
                position=anim([(t, [-(PW - PH) * (1 - v) / 2, 0], e) for t, v, e in _GROW]))


def button_null(comp):
    return comp.null("button", position=PILL, scale=anim(out([
        (CLICK - 3, [100, 100], EASE_IN), (CLICK, [96, 90], SNAP_OUT), (CLICK + 3, [96, 90], OVERSHOOT),
        (CLICK + 15, [100, 100], LINEAR)], OUTRO)))


def base(name):
    comp = Comp(name, W, H, fps=30, frames=N)
    comp.marker("intro", 0, 84)
    comp.marker("outro", OUTRO, N - OUTRO)
    return comp


# ---------------------------------------------------------------- variants

def classic(p):
    """Solid brand pill slides out of the app icon; the click turns it to the 'following' colour."""
    comp = base(p.id)
    comp.slot("primary", p.primary)
    comp.slot("secondary", p.secondary)
    pointer(comp)
    icon_layer(comp, p, ICON, CLICK, OUTRO)
    button = button_null(comp)
    click_wipe(comp, [pill(PW, PH)], (TIP[0] - PILL[0], TIP[1] - PILL[1]), CLICK, "secondary", parent=button)
    comp.layer("pill", [group([pill_grow(), fill(slot="primary")], "pill")], parent=button, op=CLICK + 13,
               opacity=anim([(6, 0, EASE_OUT), (9, 100)]))
    comp.layer("shadow", [group([pill_grow(), fill("#000000", 20)], "pill")], parent=button, position=(0, 7),
               opacity=anim([(6, 0, EASE_OUT), (9, 100)]))
    return comp


def outline(p):
    """Outlined pill draws on around the text; the click floods it with the brand colour."""
    comp = base(p.id + "--outline")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", p.primary)
    pointer(comp)
    icon_layer(comp, p, ICON, CLICK, OUTRO)
    button = button_null(comp)
    click_wipe(comp, [pill(PW, PH)], (TIP[0] - PILL[0], TIP[1] - PILL[1]), CLICK, "primary", parent=button)
    comp.layer("ring", [pill(PW, PH), trim(end=anim([(8, 0, EASE_IN_OUT), (30, 100)]),
                                           offset=anim([(8, -40, EASE_IN_OUT), (30, 0)])),
                        stroke(slot="outline", width=6)], parent=button)
    comp.layer("tint", [pill(PW, PH), fill("#000000", 30)], parent=button,
               opacity=anim([(14, 0, EASE_OUT), (30, 100)]))
    return comp


def glass(p):
    """Frosted glass card holding the icon; a sheen sweeps it, the click pulses a ring and pops a check."""
    comp = base(p.id + "--glass")
    comp.slot("outline", "#FFFFFF")
    comp.slot("primary", "#FFFFFF")
    comp.slot("accent", p.primary)
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
    ix = -cw / 2 + 24 + IS / 2
    bx, by = p.badge_at
    comp.layer("check", [group([polyline([(-10, 0), (-3, 8), (11, -8)]), stroke(p.badge_icon, width=6),
                                trim(end=anim([(CLICK + 6, 0, EASE_OUT), (CLICK + 14, 100)]))], "tick"),
                         group([ellipse((40, 40)), fill(slot="accent"), stroke("#FFFFFF", width=3)], "dot")],
               parent=card, position=(ix + bx + 2, by + 2),
               scale=anim([(CLICK + 2, [0, 0], SPRING), (CLICK + 14, [100, 100])]), ip=CLICK + 2)
    comp.layer("icon", icon_shapes(p, t0=8), parent=card, position=(ix, 0),
               scale=anim([(4, [0, 0], SPRING), (18, [100, 100], LINEAR), (CLICK + 3, [100, 100], EASE_IN_OUT),
                           (CLICK + 10, [112, 112], EASE_IN_OUT), (CLICK + 22, [100, 100])]))
    comp.layer("sheen-matte", [rect((cw, ch), roundness=44), fill()], parent=card)
    comp.layer("sheen", [group([rect((70, ch * 2)), fill("#FFFFFF", 22)], "band", rotation=20)], parent=card,
               matte="alpha", position=anim([(10, [-cw, 0], EASE_IN_OUT), (40, [cw, 0])]))
    comp.layer("rim", [rect((cw, ch), roundness=44), stroke(slot="outline", width=3, opacity=70)], parent=card)
    comp.layer("glass", [rect((cw, ch), roundness=44), fill(slot="primary", opacity=16)], parent=card)
    comp.layer("glass-shadow", [rect((cw, ch), roundness=44), fill("#000000", 18)], parent=card, position=(0, 9))
    return comp


def icon_pop(p):
    """No pill: the app icon bounces in, a plus badge pops on its corner and the click flips it to a check."""
    s = 330
    comp = Comp(p.id + "--icon-pop", s, s, fps=30, frames=N)
    comp.marker("intro", 0, 70)
    comp.marker("outro", OUTRO, N - OUTRO)
    comp.slot("primary", p.primary)
    comp.slot("secondary", p.done)
    c = (s / 2 - 10, s / 2 + 6)
    click = 50
    bx, by = p.badge_at
    tip = (c[0] + bx + 16, c[1] + by + 12)
    cursor(comp, [(22, [s + 60, s + 80], DECEL), (40, list(tip), EASE_IN_OUT), (click + 18, list(tip), EASE_IN),
                  (click + 32, [s + 60, s + 80])], [click], ip=22, op=click + 34, scale=3.4)
    badge = comp.null("badge", position=(c[0] + bx, c[1] + by),
                      scale=anim(out([(16, [0, 0], SPRING), (28, [100, 100], LINEAR), (click, [100, 100], EASE_IN),
                                      (click + 4, [80, 80], SPRING), (click + 14, [100, 100], LINEAR)], OUTRO)))
    comp.layer("plus", [group([polyline([(-13, 0), (13, 0)]), polyline([(0, -13), (0, 13)]),
                               stroke(p.badge_icon, width=7)], "plus")], parent=badge, op=click + 4,
               rotation=anim([(16, -90, SNAP_OUT), (30, 0)]))
    comp.layer("tick", [group([polyline([(-12, 1), (-3, 10), (13, -9)]), stroke(p.tick, width=7),
                               trim(end=anim([(click + 4, 0, EASE_OUT), (click + 12, 100)]))], "tick")],
               parent=badge, ip=click + 4)
    click_wipe(comp, [ellipse((52, 52))], (0, 0), click + 1, "secondary", parent=badge, dur=8, reach=120)
    comp.layer("dot", [ellipse((52, 52)), fill(slot="primary"), stroke("#FFFFFF", width=5)], parent=badge)
    burst(comp, c, click + 2, 92, 134, count=10, width=7, rotation=18)
    icon_layer(comp, p, c, click, OUTRO)
    return comp


# ---------------------------------------------------------------- asset

def build_platform(p):
    verb = p.verb
    second = {
        "glass": Variant("glass", "Glass Card", glass(p), "intro-hold-outro", thumb_t=0.3, bg=p.glass_bg,
                         text_area=(ICON[0] + IS / 2 + 30, Y - 50, W - 40 - IS - 90, 100),
                         description="Frosted glass card with the app icon; a sheen sweeps across and a check "
                                     "pops on the icon after the click."),
        "outline": Variant("outline", "Outline", outline(p), "intro-hold-outro", thumb_t=0.3, bg=p.bg,
                           text_area=PILL_TEXT,
                           description="White outline draws on around the pill; the click floods it with the "
                                       "brand colour."),
    }[p.second]
    build_asset("call-to-action", p.id, f"Follow Button {p.name}",
                f"{p.name} app icon with a {verb.lower()} button; a pointer clicks it. Put your own "
                f"\"{verb}\" text inside the button.",
                [p.name.lower(), "follow", "button", "social"] + p.tags + ["click"], [
        Variant("classic", "Classic Pill", classic(p), "intro-hold-outro", thumb_t=0.34, bg=p.bg,
                text_area=PILL_TEXT,
                description=f"{p.name}-coloured pill slides out of the app icon; the click switches it to "
                            "the followed colour."),
        second,
        Variant("icon-pop", "Icon Pop", icon_pop(p), "intro-hold-outro", thumb_t=0.8, bg=p.bg,
                description="Just the app icon with a plus badge that flips to a check when clicked; no text area."),
    ])
