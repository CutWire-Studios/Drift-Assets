import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"
W, H = 360, 120
BX, BY, BW, BH = 190, 33, 130, 54          # battery body
PAD = 6


def battery(comp, level_stops, t_cross=None, charge=False, pct=False, F=90, pulse=False):
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF453A")      # low-charge red
    comp.slot("accent", "#30D158")       # charging green
    ix, iy, iw, ih = BX + PAD, BY + PAD, BW - 2 * PAD, BH - 2 * PAD
    lvl = level_rect(ix, iy, iw, ih, level_stops, 9)
    fill_shape = lambda sl, op=None: group([lvl, fill(slot=sl, opacity=op if op is not None else 100)], "level")
    body = []
    if charge:
        # bolt on the body
        bolt = svg_shapes("M13 2L4.5 13.5H11L10 22L19.5 10H13z", 2.2, (BX + BW / 2 - 26.4, BY + BH / 2 - 26.4), "bolt")
        body.append(group(bolt + [fill("#FFFFFF")], "bolt", opacity=fade(36, 44)))
    body.append(fill_shape("accent") if charge else None)
    body = [b for b in body if b]
    if not charge:
        if t_cross is None:
            body.append(fill_shape("icon"))
        else:
            body.append(group([lvl, fill(slot="primary")], "level-low", opacity=Anim([(0, 0, HOLD), (t_cross, 100, HOLD)])))
            body.append(group([lvl, fill(slot="icon")], "level", opacity=Anim([(0, 100, HOLD), (t_cross, 0, HOLD)])))
    cap = group([rect_tl(BX + BW + 6, BY + BH / 2 - 10, 8, 20, 4), fill(slot="icon", opacity=45)], "cap")
    tray = group([rect_tl(BX, BY, BW, BH, 17), stroke(slot="icon", width=4, opacity=45)], "tray")
    shapes = body + [cap, tray]
    comp.layer("battery", shapes, anchor=(BX + BW / 2, 60), position=(BX + BW / 2, 60),
               scale=Anim([(0, [0, 0], OVERSHOOT), (12, [100, 100])]) if not pulse else [100, 100])
    return comp


def percent_ticks(comp, t_start, t_end, F, start=100, end=10, step=10, slot_after=None):
    n = (start - end) // step
    out = []
    for i in range(n + 1):
        v = start - i * step
        a = t_start + (t_end - t_start) * i / (n + 1) if i else 0
        b = t_start + (t_end - t_start) * (i + 1) / (n + 1) if i < n else F
        out.append(group(text(f"{v}%", BX - 24, 78, 52, 700, "r") + [fill(slot="icon")], f"pct{v}",
                         opacity=hold_on(a, b, F)))
    comp.layer("percent", out)


def drain():
    F = 120
    comp = Comp("battery-ios", W, H, frames=F)
    t0, t1 = 14, 100
    cross = t0 + (t1 - t0) * (100 - 20) / 90
    stops = [(0, 1.0), (t0, 1.0), (t1, 0.1), (F, 0.1)]
    battery(comp, stops, t_cross=cross, F=F)
    percent_ticks(comp, t0, t1, F)
    return comp


def charge():
    F = 90
    comp = Comp("battery-ios", W, H, frames=F)
    battery(comp, [(0, 0.12), (14, 0.12), (80, 1.0), (F, 1.0)], charge=True, F=F)
    percent_ticks(comp, 14, 80, F, start=100, end=10)
    return comp


def low():
    F = 60
    comp = Comp("battery-ios", W, H, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#FF453A")
    ix, iy, iw, ih = BX + PAD, BY + PAD, BW - 2 * PAD, BH - 2 * PAD
    sh = [group([rect_tl(ix, iy, iw * 0.14, ih, 9), fill(slot="primary")], "level"),
          group([rect_tl(BX + BW + 6, BY + BH / 2 - 10, 8, 20, 4), fill(slot="icon", opacity=45)], "cap"),
          group([rect_tl(BX, BY, BW, BH, 17), stroke(slot="primary", width=4)], "tray")]
    comp.layer("battery", sh, anchor=(BX + BW / 2, 60), position=(BX + BW / 2, 60),
               scale=Anim([(0, [100, 100], EASE_IN_OUT), (15, [112, 112], EASE_IN_OUT), (30, [100, 100], EASE_IN_OUT),
                           (45, [112, 112], EASE_IN_OUT), (60, [100, 100])]),
               opacity=Anim([(0, 100, EASE_IN_OUT), (15, 100, EASE_IN_OUT), (30, 100)]))
    comp.layer("percent", [group(text("14%", BX - 24, 78, 52, 700, "r") + [fill(slot="primary")], "pct")])
    return comp


build_asset(CAT, "battery-ios", "iOS Battery",
            "iPhone-style battery indicator: it drains with a counting percentage and turns red at 20%, charges "
            "up with a green bolt, or pulses at low charge. The percentage is part of the animation.",
            ["battery", "ios", "iphone", "charge", "low battery", "status bar", "percent", "power"], [
    Variant("drain", "Draining", drain(), "intro-hold", thumb_t=0.4, bg="6a7087"),
    Variant("charge", "Charging", charge(), "intro-hold", thumb_t=0.7, bg="6a7087"),
    Variant("low", "Low Battery", low(), "loop", thumb_t=0.0, bg="6a7087"),
])
