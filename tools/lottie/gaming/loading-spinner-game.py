from _gaming2 import *

W, H, F = 320, 400, 60
C = (W / 2, 168)
TA = (40, 318, 240, 52)


def spin(deg, step=None):
    return anim([(0, 0, LINEAR), (F, deg)])


# ---------------------------------------------------------------- rune ring (fantasy)

def rune_mark(k):
    """Abstract geometric glyphs (dots, bars, chevrons); deliberately not letters."""
    kinds = [
        [poly([(0, -8), (7, 0), (0, 8), (-7, 0)])],
        [ellipse((9, 9))],
        [poly([(0, -8), (8, 6), (-8, 6)])],
        [seg((-7, -3), (7, -3)), seg((-7, 4), (7, 4))],
    ]
    return kinds[k % len(kinds)]


def rune():
    comp = Comp("loading-spinner-game", W, H, frames=F)
    comp.slot("primary", GOLD)
    comp.slot("secondary", "#9B5CFF")
    comp.slot("accent", "#E7D2FF")
    R = 110
    marks = [group(rune_mark(k), f"m{k}", position=pt(R - 22, k * 30), rotation=k * 30) for k in range(12)]
    comp.layer("chaser", [group([ellipse((2 * R, 2 * R)), trim(start=0, end=22, offset=anim([(0, 0, EASE_IN_OUT), (F, 360)])),
                                stroke("#FFFFFF", width=5)], "c"),
                          group([ellipse((2 * R, 2 * R)), trim(start=0, end=22, offset=anim([(0, 0, EASE_IN_OUT), (F, 360)])),
                                 stroke(slot="accent", width=16, opacity=35)], "g")], position=C)
    comp.layer("gem", [group([ngon(4, 20, 0), fill(slot="secondary"), stroke(slot="primary", width=3)], "g"),
                       group([ngon(4, 8, 0, (-4, -4)), fill("#FFFFFF", 60)], "hi"), glow(90, "#B98CFF", 0.7)],
               position=C, scale=loop(F, [[100, 100], [118, 118]] * 2))
    comp.layer("hexagram", [group([ngon(3, 56, 0), ngon(3, 56, 180), stroke(slot="secondary", width=3, join="miter")], "h"),
                            group([ellipse((112, 112)), stroke(slot="secondary", width=2, opacity=60)], "c")],
               position=C, rotation=spin(-120))
    comp.layer("runes", [group(marks + [stroke(slot="primary", width=3, join="miter")], "marks")], position=C, rotation=spin(120))
    comp.layer("rings", [group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=4)], "outer"),
                         group([ellipse((2 * R - 44, 2 * R - 44)), stroke(slot="primary", width=2)], "inner"),
                         group([ellipse((2 * R, 2 * R)), stroke(slot="secondary", width=14, opacity=18)], "glow")], position=C)
    comp.layer("plate", [glow(2 * R + 60, "#2A1650", 0.8)], position=C)
    return comp


# ---------------------------------------------------------------- diamond (modern)

def diamond():
    comp = Comp("loading-spinner-game--diamond", W, H, frames=F)
    comp.slot("primary", "#35E0FF")
    comp.slot("secondary", "#FFFFFF")
    comp.slot("background", PANEL)
    # orbiting squares (4-fold, so a quarter turn per loop is seamless)
    for k in range(4):
        comp.layer("orbit", [group([rect((14, 14), (0, 0), 2), fill(slot="primary" if k % 2 else "secondary")], "s")],
                   position=sampled(lambda t, k=k: list(pt(92 + 10 * math.sin(TAU * t / F * 2), k * 90 + 180 * t / F, C)), 0, F, 1),
                   rotation=spin(360))
    # diamond flipping on its vertical axis, twice per loop
    comp.layer("diamond", [group([poly([(0, -46), (32, 0), (0, 46), (-32, 0)]), fill(slot="primary")], "d"),
                           group([poly([(0, -46), (32, 0), (0, 0)]), fill("#FFFFFF", 45)], "facet"),
                           group([poly([(0, 46), (-32, 0), (0, 0)]), fill("#000000", 25)], "shade")],
               position=C, scale=sampled(lambda t: [100 * math.cos(TAU * t / F), 100], 0, F, 1))
    comp.layer("arc", [group([ellipse((150, 150)), trim(start=anim([(0, 0, EASE_IN), (F / 2, 0, EASE_IN_OUT), (F, 100)]),
                                                        end=anim([(0, 0, EASE_IN_OUT), (F / 2, 100, HOLD), (F, 100)])),
                              stroke(slot="primary", width=6, cap="round")], "a")], position=C, rotation=spin(360))
    comp.layer("track", [group([ellipse((150, 150)), stroke(slot="secondary", width=6, opacity=12)], "t"),
                         group([ellipse((190, 190)), stroke(slot="secondary", width=1.5, opacity=25, dashes=[3, 9])], "d")], position=C)
    comp.layer("pill", [group([rect((200, 44), (0, 0), 22), fill(slot="background", opacity=80), stroke(slot="secondary", width=1.5, opacity=25)],
                              "p")], position=(TA[0] + TA[2] / 2, TA[1] + TA[3] / 2))
    return comp


# ---------------------------------------------------------------- pixel

def pixel():
    comp = Comp("loading-spinner-game--pixel", W, H, frames=F)
    comp.slot("primary", "#4DFF7A")
    comp.slot("outline", INK)
    comp.slot("background", "#2B2140")
    P = 8
    N = 8
    for k in range(N):
        a = k * 360 / N
        p = pt(80, a, C)
        p = (snap(p[0], P), snap(p[1], P))
        # head moves one block every F/N frames; blocks behind it fade in steps
        def op(t, k=k):
            head = int(t / (F / N)) % N
            d = (head - k) % N
            return [100, 70, 45, 25, 12, 12, 12, 12][d]

        def sc(t, k=k):
            head = int(t / (F / N)) % N
            return [125, 125] if head == k else [100, 100]
        comp.layer("block", [box(-2 * P, -2 * P, 4 * P, P, "#FFFFFF", opacity=40), box(-2 * P, -2 * P, 4 * P, 4 * P, slot="primary")],
                   position=p, opacity=stepped(op, 0, F, 1), scale=stepped(sc, 0, F, 1))
        comp.layer("socket", [box(-2 * P, -2 * P, 4 * P, 4 * P, slot="background"), box(-3 * P, -3 * P, 6 * P, 6 * P, slot="outline")],
                   position=p)
    # blinking dots under the spinner for the label line
    for i in range(3):
        comp.layer("dot", [box(-P, -P, 2 * P, 2 * P, slot="primary")], position=(C[0] - 3 * P + i * 3 * P, 290),
                   opacity=stepped(lambda t, i=i: 100 if int(t // 10) % 3 >= i else 0, 0, F, 2))
    return comp


build_asset(CAT, "loading-spinner-game", "Loading Spinner Game",
            "Stylised game loading spinner on a loop, with room for a \"Loading\" label underneath.",
            ["loading", "spinner", "loader", "wait", "rune", "gaming", "hud", "progress"], [
    Variant("rune", "Rune Ring", rune(), "loop", thumb_t=0.3, text_area=TA,
            description="Fantasy rune circle: a ring of geometric glyphs and a hexagram counter-rotate around a pulsing gem."),
    Variant("diamond", "Diamond", diamond(), "loop", thumb_t=0.15, text_area=TA,
            description="Modern flipping diamond with orbiting squares and a chasing arc, over a label pill."),
    Variant("pixel", "Pixel", pixel(), "loop", thumb_t=0.3, bg="e8e8ee", text_area=TA,
            description="Classic 8-bit ring of blocks with a bright head and a stepped fading trail."),
])
