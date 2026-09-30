"""Easter egg crack: a decorated egg wobbles, cracks open and a chick peeks out (intro, then holds)."""

from _common import *

T = 96
W, H = 520, 600
C = (W / 2, 350)     # egg centre
EW, EH = 100, 128    # egg half-width / half-height
Y0 = -8              # horizontal crack height
BASE, PINK, SUN, CHICK = "#8ED8F8", "#FF8CC6", "#FFD75A", "#FFD23F"
POP, WOB0, CRACK0, CRACK1, SPLIT = 0, 14, 28, 46, 56


def egg_xy(th):
    return (EW * math.sin(th) * (1 - 0.1 * math.cos(th)), -EH * math.cos(th))


def egg_arc(a0, a1, n):
    return [egg_xy(lerp(a0, a1, i / n)) for i in range(n + 1)]


def zig_h(n=8, amp=13):
    """Horizontal crack from the left edge to the right edge at Y0."""
    th1 = math.acos(-Y0 / EH)
    xl, xr = egg_xy(TAU - th1)[0], egg_xy(th1)[0]
    return [(lerp(xl, xr, i / n), Y0 + (0 if i in (0, n) else (amp if i % 2 else -amp))) for i in range(n + 1)]


def zig_v(n=10, amp=12):
    """Vertical crack from the top to the bottom."""
    return [((0 if i in (0, n) else (amp if i % 2 else -amp)), lerp(-EH, EH, i / n)) for i in range(n + 1)]


def shells_h():
    th1 = math.acos(-Y0 / EH)
    z = zig_h()
    top = egg_arc(TAU - th1, TAU + th1, 20)[:-1] + list(reversed(z))[:-1]   # left -> over top -> right, zig back
    bot = egg_arc(th1, TAU - th1, 24)[:-1] + z[:-1]                         # right -> under -> left, zig across
    return top, bot


def shells_v():
    z = zig_v()
    left = egg_arc(math.pi, TAU, 24)[:-1] + z[:-1]      # bottom -> up the left side -> top, zig down
    right = egg_arc(0, math.pi, 24)[:-1] + list(reversed(z))[:-1]
    return left, right


def full_egg():
    return egg_arc(0, TAU, 32)[:-1]


def poly(pts):
    return path(bezier(pts, closed=True))


def deco_items(style):
    """Decoration bands for the whole egg (clipped to each shell by a matte)."""
    ink = style == "doodle"
    items = []
    # zigzag band (upper)
    zz = [(-130 + 20 * i, -66 + (-10 if i % 2 else 10)) for i in range(14)]
    items.append(group([path(smooth_open(zz, 0.02)), stroke(PINK, 20, slot="secondary", join="miter", cap="butt")],
                       "zz"))
    if ink:
        items.append(group([path(smooth_open(zz, 0.02)), stroke(INK, 28, slot="outline", join="miter", cap="butt")],
                           "zz-line"))
    # dot row (top)
    items.append(group([ellipse((11, 11), (x, -100)) for x in range(-60, 61, 24)] +
                       [fill(WHITE if not ink else INK, slot=None if not ink else "outline")], "dots-top"))
    # wavy band (lower)
    wv = [(-130 + 10 * i, 50 + 9 * math.sin(i * 0.9)) for i in range(27)]
    items.append(group([path(smooth_open(wv)), stroke(SUN, 22, slot="accent", cap="butt")], "wave"))
    if ink:
        items.append(group([path(smooth_open(wv)), stroke(INK, 30, slot="outline", cap="butt")], "wave-line"))
    # little flowers row (bottom)
    for x in (-54, -18, 18, 54):
        petals = [ellipse((12, 12), rot((0, -8), a)) for a in range(0, 360, 72)]
        items.append(group(petals + [fill(PINK if not ink else WHITE, slot="secondary" if not ink else None)] +
                           ([stroke(INK, 3, slot="outline")] if ink else []), f"flower{x}", position=(x, 94)))
        items.insert(0, group([ellipse((8, 8)), fill(SUN, slot="accent")], f"fc{x}", position=(x, 94)))
    return items


def shell(comp, name, pts, style, parent, spec=(-48, -58), **tr):
    """A shell piece: shading/outline, decoration clipped by a matte, base fill. Returns its null."""
    n = comp.null(name, parent=parent, **tr)
    if style == "doodle":
        comp.layer(name + "-line", [group([boil(lambda j: bezier([(x + j(i)[0], y + j(i)[1]) for i, (x, y) in
                                                                  enumerate(pts)], closed=True), T, 4, 1.6,
                                                seed=len(name) + len(pts)), stroke(INK, 6, slot="outline")],
                                          "line")], parent=n)
    else:
        box = (-EW, -EH, EW, EH)
        comp.layer(name + "-shade", [group([poly(pts), shade_overlay(box, 1.0, light=(0.32, 0.22),
                                                                     dark="#1A2A5A")], "shade")], parent=n)
        comp.layer(name + "-spec", [group([ellipse((26, 50)), fill(WHITE, 55)], "spec", position=spec,
                                          rotation=24)], parent=n)
    comp.layer(name + "-matte", [group([poly(pts), fill(WHITE)], "m")], parent=n)
    comp.layer(name + "-deco", deco_items(style), parent=n, matte="alpha",
               position=(6, 5) if style == "doodle" else (0, 0))
    comp.layer(name + "-base", [group([poly(pts), fill(BASE, slot="primary")], "base",
                                      position=(6, 5) if style == "doodle" else (0, 0))], parent=n)
    return n


def chick_layers(comp, parent, style, full=False, flap_t0=None):
    ink = style == "doodle"
    c = comp.null("chick-face", parent=parent)
    blink = Anim([(0, [100, 100], HOLD), (82, [100, 100], EASE_IN), (85, [100, 10], EASE_OUT), (88, [100, 100])])
    eyes = [group([ellipse((7, 7), (-24, -18)), ellipse((7, 7), (30, -18)), fill(WHITE)], "catch"),
            group([ellipse((14, 18), (-22, -14)), ellipse((14, 18), (22, -14)), fill("#2A1A10")], "eyes")]
    comp.layer("eyes", eyes, parent=c, scale=blink, anchor=(0, -14), position=(0, -14))
    comp.layer("face", [
        group(S("M -13 2 L 13 2 L 0 20 Z") + [fill("#FF8A1F")] + ([stroke(INK, 3.5, slot="outline")] if ink else []),
              "beak"),
        group([ellipse((20, 11), (-44, 6)), ellipse((20, 11), (44, 6)), fill("#FF8FA8", 70)], "blush"),
    ], parent=c)
    tuft = S("M -4 -62 C -12 -80 -2 -92 4 -96 C 2 -84 6 -74 4 -62 Z M 4 -62 C 8 -78 20 -84 28 -84 "
             "C 20 -76 14 -68 10 -60 Z")
    body = [ellipse((150, 140), (0, 0))]
    if full:
        body.append(ellipse((170, 150), (0, 70)))
    paint = [stroke(INK, 6, slot="outline")] if ink else []
    comp.layer("tuft", [group(tuft + [fill(CHICK, slot="icon")] + paint, "tuft")], parent=c)
    if full:
        for side in (-1, 1):
            wing = S(f"M {side * 70} 50 C {side * 108} 40 {side * 116} 80 {side * 96} 100 C {side * 86} 90 "
                     f"{side * 76} 80 {side * 66} 70 Z")
            comp.layer(f"wing{side}", [group(wing + [fill("#F5B82A")] + paint, "wing")], parent=parent,
                       anchor=(side * 68, 60), position=(side * 68, 60),
                       rotation=osc_keys(flap_t0, T + 20, 8, 0, -side * 30) if flap_t0 else 0)
        comp.layer("feet", [group(S("M -34 142 L -44 156 M -34 142 L -34 158 M -34 142 L -24 156 "
                                    "M 34 142 L 24 156 M 34 142 L 34 158 M 34 142 L 44 156") +
                                  [stroke("#FF8A1F", 6)], "feet")], parent=parent)
    if not ink:
        comp.layer("chick-shade", [group(body + [shade_overlay((-85, -70, 85, 145 if full else 70), 0.7,
                                                               dark="#8A4A00")], "shade")], parent=parent)
    comp.layer("chick", [group(body + paint + [fill(CHICK, slot="icon")], "body")], parent=parent)


def sparkles(comp, t0, style):
    col = INK if style == "doodle" else "#FFF4B0"
    for j, (p, d) in enumerate((((-150, -150), 0), ((150, -120), 5), ((-120, -20), 9), ((160, 10), 3))):
        comp.layer(f"spark{j}", [group(S(sparkle_d(18)) + [fill(col)], "s")], ip=t0 + d,
                   position=(C[0] + p[0], C[1] + p[1]),
                   scale=Anim([(t0 + d, [0, 0], SPRING), (t0 + d + 10, [100, 100], EASE_IN_OUT),
                               (T, [70, 70])]),
                   rotation=Anim([(t0 + d, -60, SNAP_OUT), (t0 + d + 14, 0)]))


def egg_null(comp, squash_at):
    wob = [(0, 0, HOLD), (WOB0, 0, EASE_IN_OUT), (WOB0 + 5, -5, EASE_IN_OUT), (WOB0 + 10, 5, EASE_IN_OUT),
           (WOB0 + 16, -8, EASE_IN_OUT), (WOB0 + 22, 8, EASE_IN_OUT), (WOB0 + 28, -10, EASE_IN_OUT),
           (WOB0 + 34, 10, EASE_IN_OUT), (WOB0 + 40, 0)]
    sc = [(0, [0, 0], SPRING), (12, [100, 100], HOLD), (squash_at - 6, [100, 100], EASE_IN_OUT),
          (squash_at - 1, [108, 92], SNAP_OUT), (squash_at + 3, [96, 105], EASE_IN_OUT), (squash_at + 10, [100, 100])]
    return comp.null("egg", position=(C[0], C[1] + EH), anchor=(0, EH), rotation=anim(wob), scale=anim(sc))


def crack_layer(comp, pts, parent, style):
    comp.layer("crack", [group([path(bezier(pts, closed=False)), trim(end=anim([(CRACK0, 0, EASE_IN_OUT),
                                                                               (CRACK1, 100)])),
                                stroke(INK if style == "doodle" else "#3A2A50", 5, join="miter")], "crack")],
               parent=parent, op=SPLIT + 1)


def fragments(comp, style, t0):
    col = INK if style == "doodle" else BASE
    r = rng(5)
    for j in range(6):
        a = math.radians(-160 + j * 28 + r.uniform(-8, 8))
        dist = r.uniform(140, 210)
        p0 = (C[0] + 90 * math.cos(a), C[1] + Y0 + 40 * math.sin(a))
        p1 = (p0[0] + dist * math.cos(a), p0[1] + dist * math.sin(a) + 60)
        comp.layer(f"frag{j}", [group(S("M -9 -7 L 10 -4 L 2 9 Z") + [fill(col, slot="primary" if style != "doodle"
                                                                              else "outline")], "f")],
                   ip=t0, op=t0 + 20, position=anim([(t0, list(p0), DECEL), (t0 + 20, list(p1))]),
                   rotation=anim([(t0, 0), (t0 + 20, r.uniform(-300, 300))]),
                   opacity=anim([(t0 + 10, 100), (t0 + 20, 0)]))


def top_pop(style):
    """The top of the shell pops off; the chick rises and wears it like a hat."""
    comp = Comp("easter-egg-crack" + ("" if style == "classic" else f"--{style}"), W, H, frames=T)
    comp.slot("primary", BASE)
    comp.slot("secondary", PINK)
    comp.slot("accent", SUN)
    comp.slot("icon", CHICK)
    if style == "doodle":
        comp.slot("outline", INK)
    sparkles(comp, 74, style)
    fragments(comp, style, SPLIT)
    egg = egg_null(comp, SPLIT - 2)
    top, bot = shells_h()
    shell(comp, "top", top, style, egg, position=anim([
        (SPLIT, [0, 0], DECEL), (SPLIT + 9, [-24, -200], EASE_IN), (SPLIT + 18, [12, -98], SNAP_OUT),
        (SPLIT + 22, [12, -106], EASE_IN_OUT), (SPLIT + 27, [12, -98])]),
          rotation=anim([(SPLIT, 0, DECEL), (SPLIT + 9, -40, EASE_IN), (SPLIT + 18, 14, SNAP_OUT),
                         (SPLIT + 22, 8, EASE_IN_OUT), (SPLIT + 27, 12)]))
    crack_layer(comp, zig_h(), egg, style)
    shell(comp, "bottom", bot, style, egg, spec=(-62, 40))
    head = comp.null("chick", parent=egg, position=anim([(SPLIT + 2, [0, 90], SNAP_OUT), (SPLIT + 14, [0, -36], EASE_IN_OUT),
                                                         (SPLIT + 22, [0, -22], EASE_IN_OUT), (SPLIT + 30, [0, -26])]),
                     rotation=anim([(SPLIT + 26, 0, EASE_IN_OUT), (SPLIT + 32, -6, EASE_IN_OUT),
                                    (SPLIT + 38, 4, EASE_IN_OUT), (T, 0)]))
    comp.layer("inner", [group([poly(full_egg()), fill("#000000", 0)], "none")], parent=egg, ip=0, op=1, opacity=0)
    chick_layers(comp, head, style)
    comp.layer("shadow", [ellipse((230, 30)), fill("#000000", 24)], position=(C[0], C[1] + EH + 6),
               scale=anim([(0, [0, 0], SPRING), (12, [100, 100])]))
    return comp


def split(style="flat"):
    """The egg cracks down the middle; the halves fall apart and the chick hops out flapping."""
    comp = Comp("easter-egg-crack--" + style, W, H, frames=T)
    comp.slot("primary", BASE)
    comp.slot("secondary", PINK)
    comp.slot("accent", SUN)
    comp.slot("icon", CHICK)
    comp.slot("outline", WHITE)
    sparkles(comp, 72, style)
    egg = egg_null(comp, SPLIT - 2)
    left, right = shells_v()
    for name, pts, side in (("left", left, -1), ("right", right, 1)):
        n = comp.null(name + "-hinge", parent=egg, position=(side * EW * 0.8, EH), anchor=(side * EW * 0.8, EH),
                      rotation=anim([(SPLIT, 0, EASE_IN), (SPLIT + 8, side * 44, SNAP_OUT), (SPLIT + 12, side * 36,
                                                                                               EASE_IN_OUT),
                                     (SPLIT + 16, side * 40)]))
        m = comp.null(name + "-slide", parent=n, position=anim([(SPLIT, [0, 0], DECEL), (SPLIT + 10, [side * 22, 0])]))
        # white die-cut outline behind each half
        comp.layer(name + "-cut", [group([poly(pts), stroke(WHITE, 16, slot="outline", join="round")], "cut")],
                   parent=m)
        comp.layer(name + "-matte", [group([poly(pts), fill(WHITE)], "m")], parent=m)
        comp.layer(name + "-deco", deco_items("flat"), parent=m, matte="alpha")
        comp.layer(name + "-base", [group([poly(pts), fill(BASE, slot="primary")], "base")], parent=m)
        comp.layer(name + "-diecut", [group([poly(pts), stroke(WHITE, 16, slot="outline"), fill(WHITE, slot="outline")],
                                            "d")], parent=m)
    crack_layer(comp, zig_v(), egg, "flat")
    hop = comp.null("chick", parent=egg, position=anim([
        (SPLIT, [0, 40], DECEL), (SPLIT + 10, [0, -70], EASE_IN), (SPLIT + 20, [0, -10], SNAP_OUT),
        (SPLIT + 26, [0, -26], EASE_IN), (SPLIT + 32, [0, -10])]),
        scale=anim([(SPLIT + 19, [100, 100], EASE_OUT), (SPLIT + 21, [110, 90], EASE_IN_OUT), (SPLIT + 27, [100, 100])]),
        anchor=(0, 150))
    hop2 = comp.null("chick-pos", parent=hop, position=(0, 150 - 60), scale=(78, 78))
    chick_layers(comp, hop2, "flat", full=True, flap_t0=SPLIT + 4)
    comp.layer("shadow", [ellipse((260, 30)), fill("#000000", 24)], position=(C[0], C[1] + EH + 6),
               scale=anim([(0, [0, 0], SPRING), (12, [100, 100], HOLD), (SPLIT, [100, 100], EASE_OUT),
                           (SPLIT + 10, [150, 100])]))
    return comp


build("easter-egg-crack", "Easter Egg Crack",
      "A decorated Easter egg wobbles, cracks open and a fluffy chick pops out, then holds on the final pose.",
      ["easter", "egg", "chick", "spring", "hatch", "cute"], [
          Variant("classic", "Shell Hat", top_pop("classic"), "intro-hold", thumb_t=1.0,
                  description="Glossy painted egg; the top pops off and lands on the peeking chick like a hat."),
          Variant("flat", "Split Open", split("flat"), "intro-hold", thumb_t=1.0,
                  description="Flat sticker egg with a white die-cut edge that splits in two; the chick hops out flapping."),
          Variant("doodle", "Doodle", top_pop("doodle"), "intro-hold", thumb_t=1.0, bg="f3ece0",
                  description="Hand-drawn ink egg with boiling lines and off-register colour, same shell-hat reveal."),
      ])
