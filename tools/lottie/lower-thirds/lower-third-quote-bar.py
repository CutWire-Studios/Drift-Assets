from _lt2 import *


def mark(cx, cy, r, name="mark"):
    """One closing quotation mark ('9' shape): round head at (cx, cy), tail sweeping down-left."""
    k = 0.56 * r
    v = [(cx - r, cy), (cx, cy - r), (cx + r, cy), (cx - 0.75 * r, cy + 2.15 * r), (cx - 0.05 * r, cy + r)]
    it = [(0, k), (-k, 0), (0, -k), (0.95 * r, -0.2 * r), (0.2 * r, 0.3 * r)]
    ot = [(0, -k), (k, 0), (0, 1.35 * r), (0.45 * r, -0.28 * r), (-k, 0)]
    return path(bezier(v, it, ot, True), name)


def quotes(cx, cy, r, opening=False):
    """A pair of marks centred on (cx, cy); opening quotes are the closing pair turned upside down."""
    gap = r * 2.5
    shapes = [mark(cx - gap / 2, cy - r * 0.55, r, "a"), mark(cx + gap / 2, cy - r * 0.55, r, "b")]
    return group(shapes + [fill(slot="accent")], "quotes", anchor=(cx, cy), position=(cx, cy),
                 rotation=180 if opening else 0)


def framed():
    W, H = 1150, 250
    comp = base("lower-third-quote-bar", W, H, 36)
    comp.slot("accent", "#FFC53D")
    comp.slot("outline", "#FFFFFF")
    comp.slot("background", "#000000")
    oq, cq = (84, 70), (1066, 150)
    lay(comp, "open", [quotes(*oq, 20, True)], oq, scale=pop(0, 14, 128, 140),
        rotation=keys((0, -30, EXPO_OUT), (16, 0)))
    lay(comp, "close", [quotes(*cq, 20)], cq, scale=pop(10, 24, 124, 136),
        rotation=keys((10, 30, EXPO_OUT), (26, 0)))
    comp.layer("dash", [poly([(150, 206), (190, 206)], False), stroke(slot="accent", width=4),
                        draw(18, 30, 116, 126)])
    comp.layer("rule", [poly([(150, 176), (1010, 176)], False), stroke(slot="outline", width=2, opacity=60),
                        draw(8, 34, 118, 138)])
    lay(comp, "backdrop", [rrect(40, 26, 1070, 206, 18), fill(slot="background", opacity=45)], (575, 129),
        opacity=fade(0, 16, 124, 142), scale=keys((0, [96, 90], EXPO_OUT), (20, [100, 100])))
    return comp, (150, 44, 860, 120), (206, 190, 700, 32)


def side_bar():
    W, H = 1100, 250
    comp = base("lower-third-quote-bar--side", W, H, 34)
    comp.slot("accent", "#4ADE80")
    comp.slot("primary", "#0B1220")
    x, y, h = 60, 30, 190
    q = (x + 60, y + 44)
    lay(comp, "quote", [quotes(*q, 17, True)], q, scale=pop(12, 26, 124, 134))
    lay(comp, "bar", [rrect(x, y, 10, h), fill(slot="accent")], (x, y + h), scale=grow_y(0, 18, 128, 142))
    wipe(comp, "panel", [rrect(x + 10, y, 900, h), fill(slot="primary", opacity=88)], (x + 10, y, 900, h),
         6, 30, 120, 138, "left")
    return comp, (x + 110, y + 26, 770, 100), (x + 110, y + 140, 600, 30)


def card():
    W, H = 1100, 260
    comp = base("lower-third-quote-bar--card", W, H, 34)
    comp.slot("primary", "#FFFFFF")
    comp.slot("accent", "#6366F1")
    comp.slot("secondary", "#1E1B4B")
    x, y, w, h = 60, 34, 940, 178
    c = rig(comp, "card", (x + w / 2, y + h), off=slide(0, 40, 0, 20, 124, 142, EXPO_OUT, EXPO_IN),
            scale=keys((0, [92, 70], EXPO_OUT), (20, [100, 100], HOLD), (124, [100, 100], EXPO_IN), (142, [94, 60])),
            opacity=fade(0, 8, 134, 142))
    wm = (x + w - 110, y + 70)
    comp.layer("watermark", [group([mark(wm[0] - 38, wm[1], 30, "a"), mark(wm[0] + 38, wm[1], 30, "b"),
                                    fill(slot="accent", opacity=18)], "wm")], parent=c)
    q = (x + 56, y + 44)
    lay(comp, "quote", [quotes(*q, 13, True)], q, scale=pop(12, 24, 120, 130), parent=c)
    comp.layer("foot", [rrect(x, y + h - 52, w, 52, 16), rrect(x, y + h - 52, w, 24), fill(slot="secondary")], parent=c)
    comp.layer("face", [rrect(x, y, w, h, 16), fill(slot="primary")], parent=c)
    comp.layer("shadow", shadow(x, y, w, h, 16, dy=10, n=4, spread=5, op=7), parent=c)
    return comp, (x + 100, y + 22, w - 260, h - 90), (x + 40, y + h - 40, w - 80, 28)


a, ah, asub = framed()
b, bh, bs = side_bar()
c, chd, cs = card()
build("lower-third-quote-bar", "Quote Bar Lower Third",
      "Lower third for quotes: big drawn quotation marks frame a quote area, with a smaller row for who said "
      "it. Type the quote in the headline area and the name in the subtitle.",
      ["lower third", "quote", "quotation", "testimonial", "citation", "review", "speech"], [
          V("framed", "Framed Quote", a, ah, asub,
            description="Opening and closing marks spin in at opposite corners over a soft dark backdrop."),
          V("side", "Side Bar", b, bh, bs,
            description="A vertical accent bar grows, an opening mark pops on and a dark panel wipes out."),
          V("card", "Quote Card", c, chd, cs, bg="e8e8ee",
            description="White card with a large faded watermark quote and a coloured footer strip for the name."),
      ])
