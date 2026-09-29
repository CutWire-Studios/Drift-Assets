"""Full-frame "you failed" game-over look: a grey washed-out overlay and a dark banner stripe for text."""

from _memes2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 60


def grey_wash(comp, op=55, t1=18, color_slot="secondary", color="#7C7C80"):
    comp.layer("wash", [group([rect((W, H), C), fill(color, slot=color_slot)], "grey")],
               opacity=keys((0, 0, (0.3, 0, 0.3, 1)), (t1, op)))


def classic():
    """Grey wash fades in slowly while a translucent black stripe opens from the centre line."""
    comp = base("wasted-stripe", W, H, F)
    comp.slot("background", "#000000")
    comp.slot("secondary", "#7C7C80")
    SH = 220
    comp.layer("stripe", [group([rect(keys((10, [W + 40, 0], (0.3, 0, 0.1, 1)), (26, [W + 40, SH])), C),
                                 fill(slot="background", opacity=68)], "stripe")],
               opacity=keys((10, 0, EASE_OUT), (16, 100)))
    comp.layer("vig", [vignette(W, H, 0.45, 0.35)], opacity=keys((0, 0, EASE_OUT), (24, 100)))
    grey_wash(comp, 58, 24)
    return comp, (160, C[1] - SH / 2 + 30, W - 320, SH - 60)


def slide():
    """A skewed dark banner whips in from the left with red edge lines, over a flat grey wash."""
    comp = base("wasted-stripe--slide", W, H, F)
    comp.slot("background", "#101014")
    comp.slot("primary", "#E0322B")
    comp.slot("secondary", "#6E6E74")
    SH = 190
    x = keys((6, [-W * 1.3, 0], (0.1, 0.9, 0.2, 1)), (20, [30, 0], EASE_IN_OUT), (28, [0, 0]))
    sk = keys((6, -22, EASE_OUT), (20, 8, EASE_IN_OUT), (28, 0))
    comp.layer("edge-top", [group([rect((W * 1.1, 12), (C[0], C[1] - SH / 2 - 12)), fill(slot="primary")], "l")],
               anchor=C, position=keys((9, [W * 1.3 + C[0], C[1]], (0.1, 0.9, 0.2, 1)), (24, list(C))))
    comp.layer("edge-bot", [group([rect((W * 1.1, 12), (C[0], C[1] + SH / 2 + 12)), fill(slot="primary")], "l")],
               anchor=C, position=keys((11, [-W * 1.3 + C[0], C[1]], (0.1, 0.9, 0.2, 1)), (26, list(C))))
    comp.layer("stripe", [group([rect((W * 1.1, SH), C), fill(slot="background", opacity=86)], "s")],
               anchor=C, position=at(C, x), skew=sk, skew_axis=0)
    grey_wash(comp, 50, 10)
    return comp, (160, C[1] - SH / 2 + 25, W - 320, SH - 50)


def cinematic():
    """Heavy vignette closes in, then gold hairlines draw out from the centre to frame a thin fading stripe."""
    comp = base("wasted-stripe--cinematic", W, H, F)
    comp.slot("background", "#000000")
    comp.slot("accent", "#D9B25B")
    comp.slot("secondary", "#5C5C62")
    SH = 170
    for i, y in enumerate((C[1] - SH / 2, C[1] + SH / 2)):
        comp.layer(f"line{i}", [group([polyline([(C[0], y), (C[0] - W * 0.42, y)]),
                                       polyline([(C[0], y), (C[0] + W * 0.42, y)]),
                                       trim(end=keys((14 + i * 3, 0, (0.3, 0, 0.1, 1)), (40 + i * 3, 100))),
                                       stroke(slot="accent", width=4)], "l")])
    comp.layer("stripe", [group([rect((W, SH), C),
                                 gradient_fill([(0, "#000000", 0), (0.25, "#000000", 0.7), (0.75, "#000000", 0.7),
                                                (1, "#000000", 0)], (0, C[1]), (W, C[1]))], "s")],
               opacity=keys((18, 0, EASE_OUT), (40, 100)))
    comp.layer("vig", [vignette(W, H, 0.9, 0.25, mid=(0.6, "#000000", 0.45))],
               anchor=C, position=C, scale=keys((0, [150, 150], (0.3, 0, 0.1, 1)), (30, [100, 100])),
               opacity=keys((0, 0, EASE_OUT), (12, 100)))
    grey_wash(comp, 44, 26)
    return comp, (360, C[1] - SH / 2 + 25, W - 720, SH - 50)


c1, a1 = classic()
c2, a2 = slide()
c3, a3 = cinematic()
build_asset(CAT, "wasted-stripe", "Game Over Stripe",
            "Full-frame game-over overlay: the picture washes out grey and a dark banner stripe settles across the "
            "middle. Type your verdict inside the stripe.",
            ["wasted", "game over", "fail", "banner", "grey", "meme", "death screen"], [
    Variant("classic", "Classic", c1, "intro-hold", thumb_t=1.0, text_area=a1,
            description="Grey wash with a soft vignette; a translucent black stripe opens from the centre line."),
    Variant("slide", "Slide In", c2, "intro-hold", thumb_t=1.0, text_area=a2,
            description="A skewed dark banner whips in from the left between red edge lines."),
    Variant("cinematic", "Cinematic", c3, "intro-hold", thumb_t=1.0, text_area=a3,
            description="Heavy vignette closes in and gold hairlines draw out to frame a thin fading stripe."),
])
