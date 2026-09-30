"""Rounded speech bubble with room for text."""
from _callouts2 import *

W, H = 540, 400
N = 36
C = (W / 2, 172)
BW, BH = 440, 250
TIP = (138, 372)
OUT = with_tail(rrect_pts(C, BW, BH, 112), nearest(rrect_pts(C, BW, BH, 112), (200, C[1] + BH / 2)),
                TIP, 36)
TEXT = (C[0] - 170, C[1] - 78, 340, 156)


def make(style):
    comp = Comp(f"speech-bubble-round--{style}", W, H, frames=N)
    bubble(comp, OUT, style, TIP, t0=1, seed=4, draw_start=(C[0] - BW / 2, C[1]))
    return comp


build_asset(CATEGORY, "speech-bubble-round", "Round Speech Bubble",
            "A rounded speech bubble with a tail at the bottom left that pops in; type your line "
            "inside it.",
            ["speech", "bubble", "talk", "dialogue", "comic", "chat", "callout"], [
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Flat white bubble with a soft shadow that squashes and stretches in from its tail."),
    Variant("bold", "Comic", make("bold"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="e8e8ee",
            description="Comic-book bubble with a thick ink outline and a hard red shadow, springing in."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="e8e8ee",
            description="Marker outline drawn round the bubble while the white fill fades up."),
])
