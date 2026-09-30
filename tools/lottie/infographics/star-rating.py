from _common import *

W, H, F = 700, 330, 66
CY = 124
R, RI = 50, 22
XS = [W / 2 + (i - 2) * 124 for i in range(5)]
FILL = (1, 1, 1, 1, 0.5)


def star_t(i):
    return 6 + i * 6


def star_pts(c, r=R, ri=RI, rot=-90):
    return [pt(c, r if k % 2 == 0 else ri, rot + k * 36) for k in range(10)]


def clip_left(poly, xc):
    """Sutherland-Hodgman clip of a polygon to x <= xc."""
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        ina, inb = a[0] <= xc, b[0] <= xc
        if ina:
            out.append(a)
        if ina != inb:
            u = (xc - a[0]) / (b[0] - a[0])
            out.append((xc, lerp(a[1], b[1], u)))
    return out


def areas():
    return {"value": (W / 2 - 160, CY + R + 36, 320, 84)}


def pop_rig(comp, i, c):
    t = star_t(i)
    return rig(comp, f"star{i}", c, scale=keys((t, [0, 0], SPRING), (t + 14, [100, 100])),
               rotation=keys((t, -40, EXPO_OUT), (t + 16, 0)))


def flat():
    """Rounded gold stars pop in one by one with a little burst; the fifth fills halfway."""
    comp = Comp("star-rating", W, H, fps=30, frames=F)
    slots(comp, FLAT | {"primary": "#FFC247"}, "primary", "background")
    for i, x in enumerate(XS):
        c = (x, CY)
        t = star_t(i)
        burst_lines(comp, c, t + 4, R + 8, R + 30, n=5, slot="primary", width=5, rot=-54, name=f"burst{i}")
        rg = pop_rig(comp, i, c)
        st = star(5, R, RI, c, -0, outer_roundness=18, inner_roundness=8)
        if FILL[i] < 1:
            comp.layer(f"half-m{i}", [box(x - R - 6, CY - R - 6, R + 6, 2 * R + 12)], parent=rg)
        comp.layer(f"fill{i}", [group([st, gradient_fill([(0, "#FFFFFF", 0.3), (0.5, "#FFFFFF", 0)],
                                                         (x, CY - R), (x, CY + R))], "sheen"),
                                group([st, fill(slot="primary")], "f")], parent=rg,
                   matte="alpha" if FILL[i] < 1 else None)
        comp.layer(f"track{i}", [group([st, fill(slot="background", opacity=18)], "t")], parent=rg)
    return comp


def neon():
    """Neon outlined stars flicker on in sequence and fill with a soft glow; the fifth glows halfway."""
    comp = Comp("star-rating--neon", W, H, fps=30, frames=F)
    slots(comp, NEON | {"primary": "#FFD23D"}, "primary", "background", "outline")
    for i, x in enumerate(XS):
        c = (x, CY)
        t = star_t(i)
        poly = star_pts(c, R - 2, RI)
        outline = [polyline(poly, closed=True)]
        flick = keys((t, 0, HOLD), (t + 2, 100, HOLD), (t + 4, 30, HOLD), (t + 6, 100, HOLD), (F, 100))
        comp.layer(f"tube{i}", glow_strokes(outline, slot="primary", width=4, widths=(26, 14), ops=(8, 18)),
                   opacity=flick, ip=t)
        fp = poly if FILL[i] == 1 else clip_left(poly, x)
        comp.layer(f"fill{i}", soft_glow([polyline(fp, closed=True)], slot="primary", body_opacity=85,
                                         spread=(16, 34), ops=(14, 6)),
                   anchor=c, position=c, scale=keys((t + 6, [40, 40], SPRING), (t + 18, [100, 100])),
                   opacity=fade(t + 6, t + 9), ip=t + 6)
        comp.layer(f"ghost{i}", [group(outline + [stroke(slot="primary", width=3, opacity=14)], "g")],
                   opacity=fade(0, 8))
    neon_panel(comp, 14, 14, W - 28, H - 28, r=32)
    return comp


def sketch():
    """Paper card with hand-drawn stars; marker scribbles colour them in and the last one half-way."""
    comp = Comp("star-rating--sketch", W, H, fps=30, frames=F)
    slots(comp, SKETCH | {"primary": "#FFC83D"}, "primary", "background", "outline")
    paper = Paper(comp, 20, 18, W - 40, H - 36, tilt=0.8)
    card = paper.rig
    for i, x in enumerate(XS):
        c = (x, CY)
        t = star_t(i) + 4
        poly = star_pts(c, R, RI + 2, -90 + (i % 2) * 3)
        comp.layer(f"outline{i}", [ink([wobble(poly + [poly[0], poly[1]], 1.4, i, step=30)], width=4.5,
                                       draw=(t - 6, t + 6))], parent=card)
        fp = poly if FILL[i] == 1 else clip_left(poly, x)
        comp.layer(f"m{i}", [group([polyline(fp, closed=True), fill()], "m")], parent=card)
        comp.layer(f"scribble{i}", [marker(scribble_pts(x - R, CY - R, 2 * R * (FILL[i] if FILL[i] < 1 else 1) +
                                                        (6 if FILL[i] < 1 else 0), 2 * R, spacing=11, slant=16,
                                                        seed=i), 16, draw=(t + 2, t + 14), opacity=95)],
                   parent=card, matte="alpha")
    paper.sheet()
    return comp


A = areas()
build_asset(CAT, "star-rating", "Star Rating",
            "Five rating stars that pop in one by one, the last one half filled for a 4.5 score. Put the score "
            "in the 'value' area to the right.",
            ["rating", "stars", "review", "score", "feedback", "infographic", "stat"], [
    V("flat", "Flat", flat(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Rounded gold stars pop in with little bursts over soft star tracks."),
    V("neon", "Neon", neon(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Dark panel; neon star outlines flicker on and fill with a soft glow."),
    V("sketch", "Sketch", sketch(), "intro-hold", text_area=A["value"], text_areas=A, thumb_t=0.95,
      description="Paper card with hand-drawn stars coloured in by marker scribbles."),
])
