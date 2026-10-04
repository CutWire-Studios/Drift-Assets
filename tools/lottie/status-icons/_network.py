import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"
F = 60


def make(tech, style):
    size = 56 if style == "ios" else 50
    tw = text_width(tech, size, 700)
    W, H = (round(tw + 50 + 60 + 22), 120) if style == "ios" else (round(tw + 56 + 70), 120)
    comp = Comp(f"network-{tech.lower()}", W, H, fps=30, frames=F)
    comp.slot("icon", "#FFFFFF")
    if style == "filled":
        comp.slot("primary", "#2F6BFF")
        comp.slot("background", "#FFFFFF")
    shapes = []
    if style == "ios":
        bars = 4
        bw = bars * 10 + (bars - 1) * 5
        total = bw + 22 + tw
        x0 = (W - total) / 2
        shapes += signal_bars(x0, H / 2 + 24, t0=2)
        shapes += [group(text(tech, x0 + bw + 22, H / 2 + 20, size, 700) + [fill(slot="icon")], "tech",
                         anchor=(x0 + bw + 22 + tw / 2, H / 2), position=(x0 + bw + 22 + tw / 2, H / 2),
                         scale=Anim([(10, [0, 0], OVERSHOOT), (24, [100, 100])]))]
    else:
        pw, ph = tw + 56, 72
        px, py = (W - pw) / 2, (H - ph) / 2
        pop_s = Anim([(0, [0, 0], OVERSHOOT), (16, [100, 100])])
        if style == "boxed":
            shapes += [group(text(tech, W / 2 - tw / 2, H / 2 + size * 0.36, size, 700) + [fill(slot="icon")], "tech"),
                       group([rect_tl(px, py, pw, ph, 16), stroke(slot="icon", width=6)], "box")]
        else:
            shapes += [group(text(tech, W / 2 - tw / 2, H / 2 + size * 0.36, size, 700) + [fill(slot="background")], "tech"),
                       group([rect_tl(px, py, pw, ph, 36), fill(slot="primary")], "pill")]
        shapes = [group(shapes, "badge", anchor=(W / 2, H / 2), position=(W / 2, H / 2), scale=pop_s)]
    comp.layer("network", shapes)
    return comp


def build(tech, name, extra_tags):
    build_asset(CAT, f"network-{tech.lower()}", name,
                f"{tech} mobile network indicator in three looks: iOS-style signal bars with the label, an outlined "
                "box and a filled pill. Pops in and holds; no text needed.",
                [tech.lower(), "network", "mobile", "signal", "status bar", "cellular", "phone"] + extra_tags, [
        Variant("ios", "Bars + Label", make(tech, "ios"), "intro-hold", thumb_t=0.95, bg="6a7087"),
        Variant("boxed", "Outlined Box", make(tech, "boxed"), "intro-hold", thumb_t=0.95, bg="6a7087"),
        Variant("filled", "Filled Pill", make(tech, "filled"), "intro-hold", thumb_t=0.95, bg="6a7087"),
    ])
