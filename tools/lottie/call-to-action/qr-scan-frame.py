from _cta_actions import *

W, H = 440, 560
N = 72
C = (W / 2, 210)  # centre of the square where the user's QR code goes
S = 360  # bracket frame size
Q = 300  # inner square
LY, LW, LH = 492, 360, 88


def corners(arm=92, th=22, r=11):
    """Four L-shaped brackets as filled polygons around an S-sized square."""
    h = S / 2
    base = [(0, 0), (arm, 0), (arm, th), (th, th), (th, arm), (0, arm)]
    out = []
    for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        pts = [(-h * sx + x * sx, -h * sy + y * sy) for x, y in base]
        if sx * sy < 0:
            pts = pts[::-1]
        out.append(shape(pts, [r, th / 2, th / 2, 4, th / 2, th / 2], name=f"corner{i}"))
    return out


def make(style):
    comp = Comp(f"qr-scan-frame--{style}", W, H, fps=30, frames=N)
    comp.slot("primary", "#34E0A1")
    comp.slot("accent", "#34E0A1")
    comp.slot("outline" if style == "outline" else "background", "#FFFFFF")
    # laser sweeping down and back up
    y0, y1 = C[1] - Q / 2 + 6, C[1] + Q / 2 - 6
    sweep = anim([(0, [C[0], y0], EASE_IN_OUT), (N / 2, [C[0], y1], EASE_IN_OUT), (N, [C[0], y0])])
    # the glow trails behind the beam: flip it when the sweep turns
    glow_side = anim([(0, [100, 100], EASE_IN_OUT), (N / 2 - 5, [100, 100], EASE_IN_OUT), (N / 2 + 3, [100, -100], HOLD),
                      (N - 5, [100, -100], EASE_IN_OUT), (N, [100, 100])])
    laser = comp.null("laser", position=sweep)
    comp.layer("beam", [group([rect((Q + 30, 6 if style == "outline" else 8), roundness=4), fill(slot="accent")], "line")],
               parent=laser)
    glow = [group([rect((Q, hh), position=(0, -hh / 2), roundness=6), fill(slot="accent", opacity=13)], f"g{hh}")
            for hh in (16, 34, 56)]
    comp.layer("beam-glow", [group(glow, "glow", scale=glow_side),
                             group([rect((Q + 50, 18), roundness=9), fill(slot="accent", opacity=30)], "halo")],
               parent=laser)
    # brackets breathe in time with the sweep
    breathe = anim([(0, [100, 100], EASE_IN_OUT), (N / 4, [96, 96], EASE_IN_OUT), (N / 2, [100, 100], EASE_IN_OUT),
                    (3 * N / 4, [96, 96], EASE_IN_OUT), (N, [100, 100])])
    if style == "outline":
        h, a = S / 2, 84
        arms = [polyline([(-h * sx, -h * sy + a * sy), (-h * sx, -h * sy), (-h * sx + a * sx, -h * sy)], name=f"c{sx}{sy}")
                for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
        comp.layer("brackets", [group(arms + [stroke(slot="primary", width=10)], "brackets")], position=C, scale=breathe)
        comp.layer("qr-area", [rect((Q, Q), roundness=14), stroke(slot="outline", width=3, opacity=35,
                                                                      dashes=[14, 12])], position=C)
        body(comp, "label", [pill(LW, LH)], style, position=(C[0], LY), line=5)
    else:
        body(comp, "brackets", corners(), style, position=C, scale=breathe, depth=10)
        comp.layer("qr-area", [rect((Q, Q), roundness=14), fill("#FFFFFF", 7)], position=C)
        body(comp, "label", [pill(LW, LH)], style, slot="background", position=(C[0], LY), depth=9)
    return comp


TEXT = text_rect(C[0] - LW / 2, LY, LW, LH)

build_asset(CATEGORY, "qr-scan-frame", "QR Scan Frame",
            f"Scanner corner brackets with a laser line sweeping over an empty {Q}x{Q} px square "
            f"(centred at {C[0]:.0f},{C[1]:.0f}) where you place your own QR code image, plus a label pill "
            "below for \"Scan me\"; seamless loop.",
            ["qr code", "scan", "scanner", "frame", "laser", "loop", "cta"], [
    Variant(s, STYLE_NAMES[s], make(s), "loop", thumb_t=0.3, text_area=TEXT, description=STYLE_DESC[s])
    for s in STYLES])
