"""Ramadan crescent and lanterns: a crescent moon with a star and hanging fanous lanterns (seamless loops)."""

from _common import *

T = 90
GOLD, GOLD_DK, GLASS, GLASS2, NIGHT = "#F2C14E", "#B9861F", "#FF9F3A", "#2FB6A8", "#16213E"


def crescent_pts(R=120, r=100, off=(46, -30), n=48):
    """Crescent = outer disc minus an offset disc, as one closed outline with sharp horns."""
    d = math.hypot(*off)
    phi = math.atan2(off[1], off[0])
    al = math.acos((R * R + d * d - r * r) / (2 * R * d))
    a0, a1 = phi + al, phi + TAU - al               # outer arc, away from the offset disc
    outer = [(R * math.cos(lerp(a0, a1, i / n)), R * math.sin(lerp(a0, a1, i / n))) for i in range(n + 1)]
    q0, q1 = outer[-1], outer[0]
    b0 = math.atan2(q0[1] - off[1], q0[0] - off[0])
    b1 = math.atan2(q1[1] - off[1], q1[0] - off[0])
    # inner arc goes the way that passes closest to the origin (the side facing the outer disc centre)
    towards = math.atan2(-off[1], -off[0])
    db = (b1 - b0) % TAU
    mid = b0 + db / 2
    if math.cos(mid - towards) < 0:
        db -= TAU
    inner = [(off[0] + r * math.cos(b0 + db * i / n), off[1] + r * math.sin(b0 + db * i / n)) for i in range(1, n)]
    return outer + inner


def crescent_path(R=120, r=100, off=(46, -30)):
    return path(bezier(crescent_pts(R, r, off), closed=True))


def fanous_shapes():
    """Parts of an Egyptian fanous lantern, front view, hanging point at (0, -132)."""
    return {
        "ring": [ellipse((18, 18), (0, -132))],
        "spike": S("M -3 -122 L 3 -122 L 4 -108 L -4 -108 Z"),
        "dome": S("M -36 -62 C -36 -86 -10 -98 0 -110 C 10 -98 36 -86 36 -62 Z"),
        "brim": [rect((96, 14), (0, -56), 4)],
        "body": S("M -40 -48 L 40 -48 L 32 42 L -32 42 Z"),
        "panes": S("M -34 -42 L -13 -42 L -11 36 L -27 36 Z M -9 -42 L 9 -42 L 8 36 L -8 36 Z "
                   "M 13 -42 L 34 -42 L 27 36 L 11 36 Z"),
        "arches": S("M -31 -20 C -31 -34 -16 -34 -16 -20 M -8 -20 C -8 -34 8 -34 8 -20 "
                    "M 16 -20 C 16 -34 31 -34 31 -20"),
        "band": [rect((74, 10), (0, 48), 3)],
        "cone": S("M -32 54 L 32 54 L 0 94 Z"),
        "tip": [ellipse((10, 10), (0, 98))],
        "dome-dots": [ellipse((6, 6), (x, -74 + 0.01 * x * x)) for x in (-20, -10, 0, 10, 20)],
    }


def fanous_items(t_ph, style="classic", pane=GLASS, pane_slot="accent"):
    f = fanous_shapes()
    gold = [fill(GOLD, slot="primary")]
    if style == "line":
        line = [stroke(GOLD, 4, slot="primary")]
        return [group(f["arches"] + [stroke(GOLD, 3, 80, slot="primary")], "arches"),
                group(f["panes"] + line, "panes"),
                group(f["ring"] + f["dome"] + f["brim"] + f["body"] + f["band"] + f["cone"] + line, "frame"),
                group(f["panes"] + [fill(pane, 35, slot=pane_slot)], "glass",
                      opacity=looped(lambda t: 60 + 40 * clamp(0.5 + 0.5 * flicker(t, T, int(t_ph * 97))), T, 2)),
                glow(90, pane, 40, position=(0, 0))]
    return [
        group(f["dome-dots"] + [fill("#FFF3C8")], "dots"),
        group(f["arches"] + [stroke(GOLD_DK, 3)], "arches"),
        group(f["panes"] + [gradient_fill([(0, "#FFF6CF"), (0.45, pane), (1, "#8A2A10")], (0, -10), (0, 60),
                                          opacity=100)], "glass-light",
              opacity=looped(lambda t: 55 + 45 * clamp(0.5 + 0.5 * flicker(t, T, int(t_ph * 97))), T, 2)),
        group(f["panes"] + [fill(pane, slot=pane_slot)], "glass"),
        group(f["ring"] + [stroke(GOLD, 4, slot="primary")], "ring"),
        group(f["spike"] + f["dome"] + f["brim"] + f["band"] + f["cone"] + f["tip"] +
              [gradient_fill([(0, WHITE, 0.3), (0.5, WHITE, 0), (1, "#000000", 0.3)], (-40, 0), (40, 0))], "shine"),
        group(f["spike"] + f["dome"] + f["brim"] + f["band"] + f["cone"] + f["tip"] + gold, "metal"),
        group(f["body"] + gold, "frame"),
    ]


def hang(comp, name, top, length, t_ph, amp, style, scale=100, pane=GLASS, pane_slot="accent"):
    n = comp.null(name, position=top, scale=(scale, scale),
                  rotation=looped(lambda t: amp * math.sin(TAU * (t / T + t_ph)), T, 2))
    if style != "line":
        comp.layer(name + "-halo", [glow(110, "#FFB347", 100, falloff=((0, 0.5), (0.5, 0.18), (1, 0)))], parent=n,
                   position=(0, length + 132), opacity=looped(lambda t: 60 + 30 * flicker(t, T, int(t_ph * 31) + 2),
                                                              T, 2))
    comp.layer(name + "-lantern", fanous_items(t_ph, style, pane, pane_slot), parent=n, position=(0, length + 132))
    chain = S(f"M 0 0 L 0 {length}")
    comp.layer(name + "-chain", [group(chain + [stroke(GOLD, 3, slot="primary", dashes=[6, 4])], "c")], parent=n)
    return n


def moon(comp, pos, style, scale=100, T_=T):
    n = comp.null("moon", position=pos, scale=(scale, scale),
                  rotation=looped(lambda t: 4 * wave(t, T_, 1), T_, 3))
    cp = crescent_path()
    star_pos = (58, -18)
    if style == "line":
        comp.layer("star", [group(S(star_d(26, 0.45)) + [stroke(GOLD, 4, slot="primary")], "s")], parent=n,
                   position=star_pos, scale=looped(lambda t: [100 + 10 * wave(t, T_, 2)] * 2, T_, 3))
        comp.layer("crescent", [group([cp, stroke(GOLD, 5, slot="primary")], "c")], parent=n)
        comp.layer("crescent-glow", [group([cp, stroke(GOLD, 16, 18, slot="primary")], "g")], parent=n,
                   opacity=looped(lambda t: 60 + 40 * wave(t, T_, 1), T_, 3))
        return n
    comp.layer("star", [group(S(star_d(28, 0.45)) + [fill(GOLD, slot="primary")], "s")], parent=n,
               position=star_pos, rotation=looped(lambda t: 8 * wave(t, T_, 1), T_, 3),
               scale=looped(lambda t: [100 + 8 * wave(t, T_, 2)] * 2, T_, 3))
    comp.layer("crescent-shade", [group([cp, gradient_fill([(0, WHITE, 0.45), (0.5, WHITE, 0), (1, "#6A4000", 0.35)],
                                                           (-100, -80), (60, 110))], "s")], parent=n)
    comp.layer("crescent", [group([cp, fill(GOLD, slot="primary")], "c")], parent=n)
    comp.layer("moon-glow", [glow(150, "#FFD98A", 100, falloff=((0, 0.35), (0.5, 0.14), (1, 0)))], parent=n,
               opacity=looped(lambda t: 60 + 25 * wave(t, T_, 1), T_, 3))
    return n


def twinkles(comp, pts, style):
    for j, (p, r) in enumerate(pts):
        sparkle(comp, f"tw{j}", p, T, r, GOLD if style != "line" else "#FFE6A8", t0=j * 17, period=45)


def classic(style="classic"):
    W, H = 900, 540
    comp = Comp("ramadan-crescent-lanterns" + ("" if style == "classic" else "--line"), W, H, frames=T)
    comp.slot("primary", GOLD)
    comp.slot("accent", GLASS)
    comp.slot("secondary", GLASS2)
    twinkles(comp, [((90, 80), 18), ((850, 110), 20), ((420, 60), 15), ((860, 450), 17), ((440, 470), 18)], style)
    hang(comp, "f1", (560, 0), 120, 0.2, 5, style, 130)
    hang(comp, "f2", (760, 0), 40, 0.6, 6, style, 110, GLASS2, "secondary")
    moon(comp, (240, 290), style, 150)
    return comp


def border():
    W, H = 1920, 440
    comp = Comp("ramadan-crescent-lanterns--border", W, H, frames=T)
    comp.slot("primary", GOLD)
    comp.slot("accent", GLASS)
    comp.slot("secondary", GLASS2)
    r = rng(3)
    xs = [120 + i * 210 for i in range(9)]
    for i, x in enumerate(xs):
        L = [40, 130, 70, 160, 50][i % 5]
        ph = r.random()
        if i % 2 == 0:
            pane, sid = (GLASS, "accent") if i % 4 == 0 else (GLASS2, "secondary")
            hang(comp, f"f{i}", (x, 0), L / 0.8, ph, 5, "classic", 80, pane, sid)
        else:
            n = comp.null(f"m{i}", position=(x, 0), rotation=looped(lambda t, ph=ph: 6 * math.sin(TAU * (t / T + ph)),
                                                                      T, 2))
            item = [group(S(star_d(34, 0.45)) + [fill(GOLD, slot="primary")], "star")] if i % 4 == 1 else \
                [group([crescent_path(40, 34, (16, -10)), fill(GOLD, slot="primary")], "moon", rotation=-30)]
            comp.layer(f"m{i}-shape", item, parent=n, position=(0, L + (36 if i % 4 == 1 else 22)))
            comp.layer(f"m{i}-chain", [group(S(f"M 0 0 L 0 {L}") + [stroke(GOLD, 3, slot="primary",
                                                                           dashes=[6, 4])], "c")], parent=n)
    comp.layer("rail", [group(S(f"M 0 3 L {W} 3") + [stroke(GOLD, 6, slot="primary")], "r")])
    return comp


build("ramadan-crescent-lanterns", "Ramadan Crescent Lanterns",
      "A golden crescent moon with a star and glowing fanous lanterns swaying on their chains for Ramadan "
      "and Eid greetings; seamless loops.",
      ["ramadan", "eid", "crescent", "moon", "fanous", "lantern", "ramadan kareem"], [
          Variant("classic", "Crescent & Fanous", classic("classic"), "loop", thumb_t=0.2,
                  description="Glowing gold crescent and star beside two hanging fanous lanterns with flickering glass."),
          Variant("line", "Line Art", classic("line"), "loop", thumb_t=0.2,
                  description="Elegant gold line-art version with softly pulsing glow and twinkling stars."),
          Variant("border", "Top Border", border(), "loop", thumb_t=0.2, region=(420, 0, 660, 420),
                  description="A gold rail across the top of the frame hung with fanous lanterns, crescents and stars."),
      ])
