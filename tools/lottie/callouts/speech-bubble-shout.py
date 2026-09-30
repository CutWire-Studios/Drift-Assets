"""Spiky shout bubble that slams in with a shake."""
import math
import random

from _callouts2 import *

W, H = 620, 440
N = 36
C = (W / 2, 204)
RX, RY = 222, 150
TIP = (96, 408)
TEXT = (C[0] - 150, C[1] - 70, 300, 140)


def spiky(seed=3, spikes=20, scale=1.0, tail=True, reach=(1.0, 1.14), inner=(0.8, 0.86)):
    """Jagged starburst outline around an ellipse, with one long spike as the tail."""
    rnd = random.Random(seed)
    tail_ang = math.atan2((TIP[1] - C[1]) / RY, (TIP[0] - C[0]) / RX)
    pts = []
    for i in range(spikes):
        a = (i + rnd.uniform(-0.15, 0.15)) / spikes * 2 * math.pi
        b = (i + 0.5 + rnd.uniform(-0.1, 0.1)) / spikes * 2 * math.pi
        ro = rnd.uniform(*reach)
        near_tail = tail and abs((a - tail_ang + math.pi) % (2 * math.pi) - math.pi) < math.pi / spikes
        pts.append(TIP if near_tail else (C[0] + RX * scale * ro * math.cos(a), C[1] + RY * scale * ro * math.sin(a)))
        ri = rnd.uniform(*inner)
        pts.append((C[0] + RX * scale * ri * math.cos(b), C[1] + RY * scale * ri * math.sin(b)))
    return pts


OUT = spiky()


def shake(t0, amp=10, frames=10, seed=2):
    rnd = random.Random(seed)
    keys = [(0, [0, 0], LINEAR), (t0, [0, 0], LINEAR)]
    for k in range(frames):
        a = amp * (1 - k / frames)
        keys.append((t0 + 1 + k, [rnd.uniform(-a, a), rnd.uniform(-a, a)], LINEAR))
    keys.append((t0 + frames + 1, [0, 0]))
    return anim(keys)


def make(style):
    comp = Comp(f"speech-bubble-shout--{style}", W, H, frames=N)
    shaker = comp.null("shake", position=shake(6))
    slam = anim([(0, [150, 150], (0.55, 0.0, 0.9, 0.6)), (6, [90, 90], SETTLE), (10, [105, 105], SETTLE),
                 (15, [100, 100])])
    fade = anim([(0, 0, EASE_OUT), (4, 100)])
    shape = [path(bezier(OUT, closed=True))]
    if style == "bold":
        comp.slot("background", "#FFE14D")
        comp.slot("outline", INK)
        comp.slot("primary", "#FF2D2D")
        back = [path(bezier(spiky(11, 15, 1.0, tail=False, reach=(1.16, 1.32), inner=(0.98, 1.04)), closed=True))]
        comp.layer("bubble", comic(shape, "background", "outline", None, width=9, shadow=None),
                   parent=shaker, anchor=C, position=C, scale=slam, opacity=fade)
        comp.layer("back", comic(back, "primary", "outline", None, width=9, shadow=None),
                   parent=shaker, anchor=C, position=C, rotation=anim([(3, -14, SETTLE), (14, 4)]),
                   scale=anim([(3, [60, 60], SPRING), (15, [100, 100])]), ip=3)
    elif style == "clean":
        comp.slot("background", "#FFFFFF")
        comp.slot("primary", "#FF2D2D")
        comp.layer("bubble", [group(shape + [fill(slot="background")], "b")],
                   parent=shaker, anchor=C, position=C, scale=slam, opacity=fade)
        comp.layer("back", [group(shape + [fill(slot="primary")], "b")], parent=shaker, anchor=C,
                   position=anim([(3, list(C), SETTLE), (12, [C[0] + 14, C[1] + 14]) ]),
                   scale=slam, rotation=anim([(3, 0, SETTLE), (12, 3)]), ip=3)
    else:
        bubble(comp, dense(OUT + [OUT[0]])[:-1], "hand", TIP, t0=0, seed=6, width=11,
               draw_start=(C[0] - RX, C[1]))
        # impact ticks round the outside once the outline is done
        items = []
        for k, ang in enumerate((-150, -115, -40, -10, 20)):
            a = math.radians(ang)
            p0 = (C[0] + (RX + 38) * math.cos(a), C[1] + (RY + 38) * math.sin(a))
            p1 = (C[0] + (RX + 70) * math.cos(a), C[1] + (RY + 70) * math.sin(a))
            items.append(hand_line(dense([p0, p1]), 20 + k, 24 + k, 10, "outline", seed=k, taper=(0.2, 0.4),
                                   mins=(0.6, 0.4), wob=0.03, name=f"tick{k}"))
        emit(comp, items)
    return comp


build_asset(CATEGORY, "speech-bubble-shout", "Shout Speech Bubble",
            "A spiky comic shout bubble that slams in with a shake, for yelling, surprise or big "
            "announcements; type your line in the middle.",
            ["shout", "speech", "bubble", "yell", "comic", "exclaim", "callout"], [
    Variant("bold", "Comic", make("bold"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="e8e8ee",
            description="Yellow spiky bubble with an ink outline over a red burst, slammed in with a shake."),
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Flat white spiky bubble with a red offset echo, no outline."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, text_area=TEXT, bg="e8e8ee",
            description="Marker-drawn jagged bubble with little shout ticks flicked on around it."),
])
