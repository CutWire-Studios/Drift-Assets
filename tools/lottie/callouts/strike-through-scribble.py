"""Strike-through for crossing something out: messy scratch-out, marker strike or clean line."""
import random

from _callouts2 import *

W, H = 700, 200
N = 30
Y = 100
X0, X1 = 58, 642
TEXT = (X0 + 10, Y - 40, X1 - X0 - 20, 80)
REGION = (X1 - 330, 0, 330, 200)


def scratch(seed=4):
    """Back-and-forth scratch-out: slanted zigzags left to right, then back again over the top."""
    rnd = random.Random(seed)
    pts, x, up = [(X0, Y + 8)], X0, True
    while x < X1 - 20:
        x += rnd.uniform(20, 30)
        pts.append((min(x, X1), Y + (-1 if up else 1) * rnd.uniform(22, 34) + rnd.uniform(-4, 4)))
        up = not up
    while x > X0 + 40:
        x -= rnd.uniform(34, 46)
        pts.append((max(x, X0), Y + (-1 if up else 1) * rnd.uniform(14, 28) + rnd.uniform(-4, 4)))
        up = not up
    return dense(fillet(pts, 8, 5))


def make(style):
    comp = Comp(f"strike-through-scribble--{style}", W, H, frames=N)
    comp.slot("primary", "#FF2D2D")
    if style == "scribble":
        emit(comp, [hand_line(scratch(), 1, 20, 11, seed=2, chunks=14, ease=(0.35, 0.0, 0.5, 1.0),
                              taper=(0.02, 0.05), mins=(0.5, 0.3), wob=0.12)])
    elif style == "marker":
        first = dense([(X0 - 6, Y + 12), (X0 + 180, Y + 2), (X1 - 150, Y - 8), (X1 + 4, Y - 14)], smooth=True)
        second = dense([(X1 - 30, Y + 4), (X1 - 260, Y + 12), (X0 + 60, Y + 20)], smooth=True)
        emit(comp, [hand_line(first, 1, 11, 20, seed=3, taper=(0.04, 0.14), mins=(0.5, 0.2), wob=0.14),
                    hand_line(second, 11, 18, 14, seed=5, taper=(0.06, 0.3), mins=(0.6, 0.1), wob=0.14)])
    else:
        comp.layer("line", [clean_line([(X0, Y + 6), (X1, Y - 6)], 12, t0=2, t1=14, ease=(0.6, 0.0, 0.2, 1.0))],
                   scale=anim([(14, [100, 100], SETTLE), (17, [100, 150], SETTLE), (22, [100, 100])]),
                   anchor=(W / 2, Y), position=(W / 2, Y))
        # a little flash where the line lands
        comp.layer("spark", [group([P([(0, -18), (0, -34)]), stroke(slot="primary", width=6)], "a", rotation=-40),
                             group([P([(0, -18), (0, -38)]), stroke(slot="primary", width=6)], "b"),
                             group([P([(0, -18), (0, -34)]), stroke(slot="primary", width=6)], "c", rotation=40)],
                   position=(X1 + 4, Y - 8), rotation=90, ip=13, op=24,
                   scale=anim([(13, [40, 40], SETTLE), (18, [110, 110], EASE_IN), (23, [130, 130])]),
                   opacity=anim([(13, 100, EASE_IN), (23, 0)]))
    return comp


build_asset(CATEGORY, "strike-through-scribble", "Strike-Through Scribble",
            "Crosses something out: lay it over a word or line of text, which sits in the text area "
            "behind it.",
            ["strike-through", "cross out", "scribble", "wrong", "delete", "edit", "hand-drawn"], [
    Variant("scribble", "Scratch-Out", make("scribble"), "intro-hold", thumb_t=0.99, text_area=TEXT, region=REGION, pad=0.04,
            description="Messy back-and-forth marker scribble that scratches the word out."),
    Variant("marker", "Marker Strike", make("marker"), "intro-hold", thumb_t=0.99, text_area=TEXT, region=REGION, pad=0.04,
            description="One confident marker stroke through the middle with a quick return stroke."),
    Variant("clean", "Clean Line", make("clean"), "intro-hold", thumb_t=0.99, text_area=TEXT, region=REGION, pad=0.04,
            description="Straight vector strike that shoots across and throws a little spark at the end."),
])
