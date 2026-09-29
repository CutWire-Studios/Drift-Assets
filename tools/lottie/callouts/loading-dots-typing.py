"""Typing indicator: three dots rippling inside a chat bubble (seamless loop)."""
from _callouts2 import *

W, H = 300, 170
N = 72
CYCLE = 36
C = (W / 2 + 6, 76)
BW, BH = 210, 104
TIP = (62, 160)
XS = [-44, 0, 44]


def wave(k, lo, hi):
    """Per-dot keys: rise to `hi` and back, offset by dot index, twice per loop."""
    keys = []
    d = k * 6
    for c in range(0, N, CYCLE):
        keys += [(c + d, lo, EASE_IN_OUT), (c + d + 9, hi, EASE_IN_OUT), (c + d + 18, lo, HOLD)]
    # wrap: every dot is at rest at frame 0 and N
    keys = [(0, lo, HOLD)] + [k_ for k_ in keys if 0 < k_[0] < N] + [(N, lo, HOLD)]
    return keys


def dots(comp, style, parent=None):
    for k, x in enumerate(XS):
        y = [(t, [C[0] + x, C[1] + v], e) for t, v, e in wave(k, 0, -13)]
        sc = [(t, [v, v], e) for t, v, e in wave(k, 88, 112)]
        op = wave(k, 45, 100)
        if style == "bold":
            shape = comic([ellipse((30, 30))], "primary", "outline", None, width=5, shadow=None)
        else:
            shape = [group([ellipse((26, 26)), fill(slot="primary")], "d")]
        comp.layer(f"dot{k}", shape, parent=parent, position=anim(y), scale=anim(sc),
                   opacity=anim(op) if style != "bold" else 100)


def make(style):
    comp = Comp(f"loading-dots-typing--{style}", W, H, frames=N)
    if style == "bubble":
        comp.slot("primary", "#8E8E93")
        comp.slot("background", "#E9E9EB")
        dots(comp, style)
        out = with_tail(rrect_pts(C, BW, BH, BH / 2), nearest(rrect_pts(C, BW, BH, BH / 2),
                                                              (C[0] - 70, C[1] + BH / 2)), TIP, 18, bend=0.15)
        comp.layer("bubble", [group([P(out, True), fill(slot="background")], "b")])
    elif style == "minimal":
        comp.slot("primary", "#FFFFFF")
        dots(comp, style)
    else:
        comp.slot("primary", "#FFD21F")
        comp.slot("outline", INK)
        comp.slot("background", "#FFFFFF")
        dots(comp, style)
        out = with_tail(rrect_pts(C, BW, BH, 30), nearest(rrect_pts(C, BW, BH, 30), (C[0] - 70, C[1] + BH / 2)),
                        TIP, 26, bend=0.12)
        comp.layer("bubble", comic([P(out, True)], "background", "outline", "outline", width=6, shadow=(8, 8)))
    return comp


build_asset(CATEGORY, "loading-dots-typing", "Typing Dots",
            "A chat \"someone is typing\" indicator: three dots ripple inside a message bubble, looping "
            "seamlessly.",
            ["typing", "loading", "dots", "chat", "message", "waiting", "loop"], [
    Variant("bubble", "Chat Bubble", make("bubble"), "loop", thumb_t=0.2,
            description="Soft grey messenger bubble with dots rising and brightening in turn."),
    Variant("minimal", "Dots Only", make("minimal"), "loop", thumb_t=0.2, region=(76, 16, 160, 120),
            description="Just the three dots, no bubble, for putting on your own background."),
    Variant("bold", "Comic", make("bold"), "loop", thumb_t=0.2, bg="e8e8ee",
            description="Squarer comic bubble with an ink outline and hard shadow, and outlined yellow dots."),
])
