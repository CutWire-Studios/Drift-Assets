"""Helpers for device and window frames: even-odd screen cut-outs, soft shadows, pop-in."""

from ui_kit import *
from os_icons import *

CAT = "devices"


def screen_ring(outer, inner, ro, ri, slot=None, color=None, opacity=100, name="frame"):
    """Filled band between `outer` and `inner` rounded rects (x, y, w, h): the screen is a real hole."""
    f = fill(color, opacity, even_odd=True) if color else fill(slot=slot, opacity=opacity, even_odd=True)
    return group([rect_tl(*outer, ro, "outer"), rect_tl(*inner, ri, "inner"), f], name)


def soft_shadow(x, y, w, h, r, spread=40, dy=22, strength=26, layers=7, hole=None):
    """Stacked translucent rounded rects approximating a blurred drop shadow. `hole` = shape items
    (e.g. rrect_path of the screen) cut out so a transparent window body stays clear."""
    out = []
    for i in range(layers):
        g = spread * (1 - i / layers)
        items = [rect_tl(x - g, y - g + dy, w + 2 * g, h + 2 * g, r + g)] + (hole or [])
        out.append(group(items + [fill("#000000", strength / layers, even_odd=bool(hole))], f"shadow{i}"))
    return out


def pop_layer(comp, name, shapes, cx, cy, delay=0, F_in=16, from_scale=92, dy=24):
    """Layer that scales up from slightly smaller and rises into place."""
    return comp.layer(name, shapes, anchor=(cx, cy), position=Anim([(delay, [cx, cy + dy], EXPO_OUT), (delay + F_in, [cx, cy])]),
                      scale=Anim([(delay, [from_scale, from_scale], EXPO_OUT), (delay + F_in, [100, 100])]),
                      opacity=fade(delay, delay + 8))


def device_comp(name, w, h, F=60):
    return Comp(name, w, h, fps=30, frames=F)


def landscape(comp, pw, ph):
    """Turn a portrait-drawn comp (pw x ph) into a landscape one by rotating every layer's content 90 deg."""
    comp.w, comp.h = ph, pw
    wrap = comp.null("rotate", anchor=(pw / 2, ph / 2), position=(ph / 2, pw / 2), rotation=-90)
    for L in comp.layers:
        if L["ind"] != wrap and "parent" not in L:
            L["parent"] = wrap
    return comp


def window_shell(comp, x, y, w, h, R, tb, chrome, bg_slot="background", solid_slot=None, F_in=16, edge_slot="outline"):
    """Pop-in window: titlebar/toolbar of height tb in `bg_slot`, rounded outer corners, transparent body
    (or a solid body in `solid_slot`), soft shadow. `chrome` = shapes drawn on the bar. Returns the screen rect."""
    screen = (x, y + tb, w, h - tb)
    if solid_slot:
        shell = [group([rect_tl(x, y, w, h, R), fill(slot=solid_slot)], "body"),
                 group(rrect_path(x, y, w, tb + R, tl=R, tr=R) + [fill(slot=bg_slot)], "bar-top"),
                 group([rect_tl(x, y + tb, w, R + 1, 0), fill(slot=solid_slot)], "bar-cover")]
        ring = shell
        hole = None
    else:
        hole = rrect_path(*screen, bl=R - 2, br=R - 2, name="screen")
        ring = [group([rect_tl(x, y, w, h, R)] + hole + [fill(slot=bg_slot, even_odd=True)], "window")]
    sep = [group([polyline([(x, y + tb), (x + w, y + tb)]), stroke(slot=edge_slot, width=1.5)], "sep")]
    pop_layer(comp, "window", chrome[::-1] + sep + ring, comp.w / 2, comp.h / 2, F_in=F_in)
    comp.layer("shadow", soft_shadow(x, y, w, h, R, hole=hole), anchor=(comp.w / 2, comp.h / 2),
               position=(comp.w / 2, comp.h / 2), opacity=fade(0, 14))
    return screen


def phone(name, spec, F=60, status=None):
    """Portrait phone frame with a real screen cut-out. spec keys: sw, sh (screen), rs (screen radius),
    bt, bs, bb (black bezel top/side/bottom), band (metal rim), cam: island|notch|punch|home|pixel.
    Returns (comp, screen_rect, (pw, ph)) in portrait canvas coordinates; call landscape() afterwards for sideways."""
    M = 34
    sw, sh, rs = spec["sw"], spec["sh"], spec["rs"]
    bt, bs, bb, band = spec["bt"], spec["bs"], spec["bb"], spec["band"]
    pw = sw + 2 * (bs + band) + 2 * M
    ph = sh + bt + bb + 2 * band + 2 * M
    comp = device_comp(name, pw, ph, F)
    comp.slot("primary", spec.get("rim", "#2A2A2E"))
    comp.slot("secondary", "#0A0A0C")
    comp.slot("icon", "#FFFFFF")
    sx, sy = M + band + bs, M + band + bt
    r_bez, r_body = rs + min(bs, bt), rs + min(bs, bt) + band
    screen = rrect_path(sx, sy, sw, sh, rs, rs, rs, rs, "screen")
    bez_out = (sx - bs, sy - bt, sw + 2 * bs, sh + bt + bb)
    body_out = (M, M, pw - 2 * M, ph - 2 * M)
    cx = sx + sw / 2
    shapes = []
    cam = spec["cam"]
    if cam == "island":
        shapes += [group([rect_tl(cx - 95, sy + 22, 190, 56, 28), fill(slot="secondary")], "island")]
    elif cam == "notch":
        shapes += [group(rrect_path(cx - 190, sy, 380, 56, br=30, bl=30) + [fill(slot="secondary")], "notch")]
    elif cam == "punch":
        shapes += [group([ellipse((spec.get("hole", 30),) * 2, (cx, sy + spec.get("hole_y", 34))), fill(slot="secondary")], "punch")]
    elif cam == "home":
        shapes += [group([rect_tl(cx - 60, sy - bt / 2 - 5, 120, 10, 5), fill("#2F2F34")], "speaker"),
                   group([ellipse((16, 16), (cx - 110, sy - bt / 2)), fill("#2F2F34")], "camera"),
                   group([ellipse((74, 74), (cx, sy + sh + bb / 2)), stroke("#3A3A40", 3.5)], "home-button")]
    if status:
        shapes = status(sx, sy, sw, sh) + shapes
    # side buttons
    for (y0, hgt, side) in spec.get("buttons", []):
        bx = M - 7 if side == "l" else pw - M
        shapes.append(group([rect_tl(bx, M + y0, 7, hgt, 3), fill(slot="primary")], "button"))
    shapes += [group(rrect_path(*bez_out, r_bez, r_bez, r_bez, r_bez, "bez-out") + screen + [fill(slot="secondary", even_odd=True)], "bezel"),
               group(rrect_path(*body_out, r_body, r_body, r_body, r_body, "body-out") +
                     rrect_path(*bez_out, r_bez, r_bez, r_bez, r_bez, "body-in") + [fill(slot="primary", even_odd=True)], "rim")]
    pop_layer(comp, "phone", shapes, pw / 2, ph / 2)
    comp.layer("shadow", soft_shadow(*body_out, r_body, spread=34, dy=24, hole=screen), anchor=(pw / 2, ph / 2),
               position=(pw / 2, ph / 2), opacity=fade(0, 14))
    return comp, (sx, sy, sw, sh), (pw, ph)


def phone_variant(name, spec, orient, status=None, F=60):
    comp, scr, (pw, ph) = phone(name, spec, F, status)
    if orient == "landscape":
        comp = landscape(comp, pw, ph)
        x, y, w, h = scr
        # rotate the portrait rect -90 deg about the canvas centre
        cx, cy = pw / 2, ph / 2
        nx = ph / 2 + (y - cy)
        ny = pw / 2 - (x + w - cx)
        scr = (nx, ny, h, w)
    return comp, scr


def finish_device(comp, shapes, body, r_body, hole, spread=34, dy=24):
    """Pop-in layer for `shapes` plus a shadow under `body` (x, y, w, h) that keeps `hole` clear."""
    cx, cy = comp.w / 2, comp.h / 2
    pop_layer(comp, "device", shapes, cx, cy)
    comp.layer("shadow", soft_shadow(*body, r_body, spread=spread, dy=dy, hole=hole), anchor=(cx, cy), position=(cx, cy),
               opacity=fade(0, 14))
