from _gaming2 import *

W, H, F = 800, 220, 120
Y = 110
XS = [72, 176, 280, 384]
R = 42
PRESS = [8, 36, 64, 92]
SLOTS = ["primary", "secondary", "accent", "icon"]
COLORS = ["#3DDBB5", "#FF5A6A", "#6AA8FF", "#FF7BD0"]
TA = (452, Y - 32, 330, 64)


def glyph(k, s=17):
    if k == 0:
        return [poly([pt(s * 1.05, a, (0, 2)) for a in (0, 120, 240)])]
    if k == 1:
        return [ellipse((s * 1.9, s * 1.9))]
    if k == 2:
        return [seg((-s * 0.85, -s * 0.85), (s * 0.85, s * 0.85)), seg((-s * 0.85, s * 0.85), (s * 0.85, -s * 0.85))]
    return [rect((s * 1.6, s * 1.6))]


def press_curve(t, p, dur=14):
    """0 -> 1 (fully pressed) -> 0 around press frame p."""
    d = t - p
    if d < 0 or d > dur:
        return 0.0
    if d < 3:
        return ease_out(d / 3)
    return 1 - smooth((d - 3) / (dur - 3))


def press_anim(i, fn, step=1, hold=False):
    return (stepped if hold else sampled)(lambda t: fn(press_curve(t, PRESS[i])), 0, F, step)


def ripple(comp, i, shapes_fn, dur=16, d0=2 * R, d1=2 * R + 70):
    p = PRESS[i]
    comp.layer("ripple", shapes_fn(anim([(p, [d0, d0], DECEL), (p + dur, [d1, d1])])), position=(XS[i], Y), ip=p,
               op=p + dur + 1, opacity=anim([(p, 90, EASE_IN), (p + dur, 0)]))


def idle_bob(i, amp=0):
    return None


# ---------------------------------------------------------------- modern

def modern():
    comp = Comp("controller-button-prompts", W, H, frames=F)
    for s, c in zip(SLOTS, COLORS):
        comp.slot(s, c)
    comp.slot("background", "#1B1E26")
    comp.slot("outline", "#FFFFFF")
    for i, x in enumerate(XS):
        ripple(comp, i, lambda size, i=i: [group([ellipse(size), stroke(slot=SLOTS[i], width=4)], "r")])
        comp.layer("glyph glow", [group(glyph(i) + [stroke(slot=SLOTS[i], width=18, opacity=35)], "g")],
                   position=press_anim(i, lambda v, x=x: [x, Y + 4 * v]), opacity=press_anim(i, lambda v: 100 * v))
        comp.layer("glyph", [group(glyph(i) + [stroke(slot=SLOTS[i], width=5.5, join="miter" if i in (0, 3) else "round")], "g")],
                   position=press_anim(i, lambda v, x=x: [x, Y + 4 * v]),
                   scale=press_anim(i, lambda v: [100 + 12 * v] * 2))
        comp.layer("cap", [
            group([ellipse((2 * R - 8, 2 * R - 8)), stroke(slot="outline", width=1.5, opacity=18)], "inner rim"),
            group([ellipse((2 * R, 2 * R)), gradient_fill([(0, "#FFFFFF", 0.22), (0.5, "#FFFFFF", 0.03), (1, "#000000", 0.25)],
                                                         (0, -R), (0, R))], "gloss"),
            group([ellipse((2 * R, 2 * R)), fill(slot="background")], "face"),
        ], position=press_anim(i, lambda v, x=x: [x, Y + 4 * v]), scale=press_anim(i, lambda v: [100 - 5 * v] * 2))
        comp.layer("well", [group([ellipse((2 * R + 10, 2 * R + 10)), fill("#000000", 45)], "w"),
                            group([ellipse((2 * R + 10, 2 * R + 10), (0, 7)), fill("#000000", 25)], "s")], position=(x, Y + 2))
    comp.layer("divider", [group([seg((432, Y - 34), (432, Y + 34)), stroke(slot="outline", width=2, opacity=35)], "d")])
    return comp


# ---------------------------------------------------------------- pixel

def disc_cells(r):
    n = 2 * r
    return pix_cells(lambda x, y: x * x + y * y <= (r - 0.2) ** 2, n)


def pixel_glyph(k):
    return [
        ["....XX....", "...XXXX...", "...XXXX...", "..XX..XX..", "..XX..XX..", ".XX....XX.", ".XXXXXXXX.", "XXXXXXXXXX"],
        ["..XXXX..", ".XXXXXX.", "XXX..XXX", "XX....XX", "XX....XX", "XXX..XXX", ".XXXXXX.", "..XXXX.."],
        ["XX....XX", "XXX..XXX", ".XXXXXX.", "..XXXX..", "..XXXX..", ".XXXXXX.", "XXX..XXX", "XX....XX"],
        ["XXXXXXXX", "XXXXXXXX", "XX....XX", "XX....XX", "XX....XX", "XX....XX", "XXXXXXXX", "XXXXXXXX"],
    ][k]


def pixel():
    comp = Comp("controller-button-prompts--pixel", W, H, frames=F)
    for s, c in zip(SLOTS, ["#39E5A0", "#FF4D5E", "#4D8CFF", "#FF6FD8"]):
        comp.slot(s, c)
    comp.slot("background", "#3A3150")
    comp.slot("outline", INK)
    P = 6
    r = 6
    for i, x in enumerate(XS):
        down = lambda v: [0, P] if v > 0.3 else [0, 0]
        pos = press_anim(i, lambda v, x=x: [x, Y + (P if v > 0.3 else 0)], hold=True)
        rows = pixel_glyph(i)
        comp.layer("glyph", pix(rows, {"X": ("slot", SLOTS[i])}, 4), position=pos)
        comp.layer("flash", [pix_group(disc_cells(r - 1), P, (-(r - 1) * P, -(r - 1) * P), "#FFFFFF", "f")], position=pos,
                   opacity=press_anim(i, lambda v: 60 if 0.3 < v < 0.95 else 0, hold=True))
        top = disc_cells(r)
        o = (-r * P, -r * P)
        comp.layer("cap", [
            pix_group([(3, 2), (4, 2), (2, 3), (2, 4)], P, o, ("#FFFFFF", 45), "hi"),
            pix_group(disc_cells(r), P, o, ("slot", "background"), "face"),
            pix_group(pix_cells(lambda x_, y_: x_ * x_ + y_ * y_ <= (r + 1 - 0.2) ** 2, 2 * r + 2), P, (-(r + 1) * P, -(r + 1) * P),
                      ("slot", "outline"), "rim"),
        ], position=pos)
        comp.layer("base", [pix_group(pix_cells(lambda x_, y_: x_ * x_ + y_ * y_ <= (r + 1 - 0.2) ** 2, 2 * r + 2), P,
                                      (-(r + 1) * P, -(r + 1) * P), ("slot", "outline"), "b"),
                            pix_group(disc_cells(r), P, o, "#000000", "d")], position=(x, Y + P))
        # pixel ripple: square ring expanding in steps
        p = PRESS[i]
        for k in range(3):
            s = 2 * (r + 2 + k * 1.5) * P
            comp.layer("ring", [box(-s / 2, -s / 2, s, P, slot=SLOTS[i]), box(-s / 2, s / 2 - P, s, P, slot=SLOTS[i]),
                                box(-s / 2, -s / 2, P, s, slot=SLOTS[i]), box(s / 2 - P, -s / 2, P, s, slot=SLOTS[i])],
                       position=(x, Y), ip=p + 1 + k * 3, op=p + 4 + k * 3, opacity=100 - k * 30)
    comp.layer("divider", [box(430 + (k % 2) * 0, Y - 30 + k * 12, 6, 6, slot="background") for k in range(6)])
    return comp


# ---------------------------------------------------------------- neon

def neon_v():
    comp = Comp("controller-button-prompts--neon", W, H, frames=F)
    for s, c in zip(SLOTS, ["#2BFFC6", "#FF2B6A", "#2BB8FF", "#FF2BD6"]):
        comp.slot(s, c)
    comp.slot("outline", "#B9B3FF")
    for i, x in enumerate(XS):
        ripple(comp, i, lambda size, i=i: [group([ellipse(size), stroke(slot=SLOTS[i], width=3)], "r"),
                                           group([ellipse(size), stroke(slot=SLOTS[i], width=12, opacity=25)], "g")])
        comp.layer("glyph", neon(glyph(i, 16), slot=SLOTS[i], w=3.5), position=(x, Y),
                   opacity=press_anim(i, lambda v: 70 + 30 * v), scale=press_anim(i, lambda v: [100 + 14 * v] * 2))
        comp.layer("fill", [group([ellipse((2 * R - 8, 2 * R - 8)), fill(slot=SLOTS[i], opacity=40)], "f")], position=(x, Y),
                   opacity=press_anim(i, lambda v: 100 * v))
        comp.layer("ring", neon([ellipse((2 * R, 2 * R))], slot="outline", w=3, glow_a=0.8), position=(x, Y),
                   scale=press_anim(i, lambda v: [100 - 6 * v] * 2))
    comp.layer("divider", neon([seg((432, Y - 30), (432, Y + 30))], slot="outline", w=2.5, core=False))
    return comp


build_asset(CAT, "controller-button-prompts", "Controller Button Prompts",
            "A row of four face-button prompts with triangle, circle, cross and square glyphs; each one is pressed in "
            "turn on a loop. Put the action label to the right.",
            ["controller", "buttons", "prompt", "gamepad", "tutorial", "input", "gaming", "hud"], [
    Variant("modern", "Modern", modern(), "loop", thumb_t=0.1, region=(16, 30, 440, 160), text_area=TA,
            description="Glossy dark keycaps with coloured glyphs that sink and glow when pressed."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.1, region=(16, 30, 440, 160), bg="e8e8ee", text_area=TA,
            description="8-bit round buttons with pixel glyphs that drop a pixel on press, with stepped ripples."),
    Variant("neon", "Neon", neon_v(), "loop", thumb_t=0.1, region=(16, 30, 440, 160), text_area=TA,
            description="Neon outline rings and glyphs that flood with colour when pressed."),
])
