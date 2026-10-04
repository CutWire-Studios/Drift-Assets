import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"

W, H = 220, 190
PX, PY = 110, 160


def fan(round_caps, thickness, gap):
    """Three wifi arcs + dot; returns (arcs, dot) as lists of shape groups centred on the pivot."""
    radii = [38 + (thickness + gap) * i for i in range(3)]
    arcs = []
    for i, r in enumerate(radii):
        arcs.append([arc_path(r, 225, 315, (PX, PY)),
                     stroke(slot="icon", width=thickness, cap="round" if round_caps else "butt")])
    dot = [ellipse((thickness * 1.5 if round_caps else thickness * 1.7,) * 2, (PX, PY - (4 if round_caps else 0)))]
    return arcs, dot


def intro(round_caps, thickness, gap, stagger=7):
    comp = Comp("wifi-signal", W, H, frames=75)
    comp.slot("icon", "#FFFFFF")
    arcs, dot = fan(round_caps, thickness, gap)
    layers = []
    for i, a in enumerate(arcs):
        t = 6 + stagger * (i + 1)
        layers.append(group([*a[:1], a[1]], f"arc{i}", opacity=Anim([(0, 0, HOLD), (t, 0, EASE_OUT), (t + 6, 100)]),
                            anchor=(PX, PY), position=(PX, PY),
                            scale=Anim([(t, [70, 70], OVERSHOOT), (t + 8, [100, 100])])))
    layers = layers[::-1]
    comp.layer("arcs", layers)
    comp.layer("dot", [group(dot + [fill(slot="icon")], "dot", anchor=(PX, PY), position=(PX, PY),
                             scale=Anim([(0, [0, 0], OVERSHOOT), (10, [100, 100])]))])
    return comp


def searching():
    F = 60
    comp = Comp("wifi-signal", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    arcs, dot = fan(True, 15, 12)
    for i, a in enumerate(arcs):
        # arc i is lit while the sweep is at level >= i; sweep: 0..3 then all off, loops
        t_on = 8 + 10 * i
        op = Anim([(0, 28, HOLD), (t_on, 100, HOLD), (50, 28, HOLD), (F, 28)])
        comp.layer(f"arc{i}", [group(a, f"arc{i}", opacity=op)])
    comp.layer("dot", [group(dot + [fill(slot="icon")], "dot")])
    return comp


build_asset(CAT, "wifi-signal", "Wi-Fi Signal",
            "Wi-Fi signal icon: arcs light up one by one and hold, in a flat iOS-style cut, with rounded Android "
            "strokes, or a looping 'searching' sweep.",
            ["wifi", "wi-fi", "signal", "internet", "connection", "status bar", "network"], [
    Variant("ios", "iOS Fan", intro(False, 17, 8), "intro-hold", thumb_t=0.95, bg="6a7087"),
    Variant("rounded", "Rounded", intro(True, 15, 12), "intro-hold", thumb_t=0.95, bg="6a7087"),
    Variant("searching", "Searching", searching(), "loop", thumb_t=0.3, bg="6a7087"),
])
