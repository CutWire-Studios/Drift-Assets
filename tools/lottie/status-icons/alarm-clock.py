import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ui_kit import *

CAT = "status-icons"

CX, CY, R = 150, 168, 92


def hands(slot, w=12):
    return [group([polyline([(CX, CY), (CX, CY - 52)]), stroke(slot=slot, width=w)], "minute"),
            group([polyline([(CX, CY), (CX + 38, CY + 22)]), stroke(slot=slot, width=w)], "hour")]


def ring_waves(frames, slot, side):
    out = []
    for k in range(2):
        t = k * 6
        sx = CX + side * (R + 30 + k * 22)
        a0, a1 = (-32, 32) if side > 0 else (148, 212)
        out.append(group([arc_path(R + 30 + k * 22, a0, a1, (CX, CY)), stroke(slot=slot, width=9)], f"wave{k}",
                         opacity=Anim([(0, 0, HOLD), (t + 2, 100, EASE_IN_OUT), (t + 8, 0, HOLD), (frames // 2, 0, HOLD),
                                       (frames // 2 + t + 2, 100, EASE_IN_OUT), (frames // 2 + t + 8, 0)]),
                         ))
    return out


def classic():
    F = 60
    comp = Comp("alarm-clock", 300, 300, frames=F)
    comp.slot("primary", "#FF3B30")
    comp.slot("secondary", "#2C2C34")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FFD60A")
    shake = Anim([(0, 0, EASE_IN_OUT), (3, -9, EASE_IN_OUT), (6, 9, EASE_IN_OUT), (9, -9, EASE_IN_OUT), (12, 9, EASE_IN_OUT),
                  (15, -9, EASE_IN_OUT), (18, 9, EASE_IN_OUT), (21, 0, EASE_IN_OUT), (30, 0, HOLD), (33, -9, EASE_IN_OUT),
                  (36, 9, EASE_IN_OUT), (39, -9, EASE_IN_OUT), (42, 9, EASE_IN_OUT), (45, -9, EASE_IN_OUT), (48, 9, EASE_IN_OUT),
                  (51, 0, EASE_IN_OUT), (F, 0)])
    body = [
        *hands("secondary"),
        group([ellipse((16, 16), (CX, CY)), fill(slot="secondary")], "pin"),
        *[group([polyline([(CX + 68 * math.sin(math.radians(a)), CY - 68 * math.cos(math.radians(a))),
                           (CX + 77 * math.sin(math.radians(a)), CY - 77 * math.cos(math.radians(a)))]),
                 stroke(slot="secondary", width=7, opacity=70)], f"tick{a}") for a in range(0, 360, 90)],
        group([ellipse((2 * R - 40, 2 * R - 40), (CX, CY)), fill(slot="icon")], "face"),
        group([ellipse((2 * R, 2 * R), (CX, CY)), fill(slot="primary")], "body"),
        group([polyline([(CX - 62, CY + R - 6), (CX - 82, CY + R + 26)]), stroke(slot="secondary", width=14)], "leg-l"),
        group([polyline([(CX + 62, CY + R - 6), (CX + 82, CY + R + 26)]), stroke(slot="secondary", width=14)], "leg-r"),
        group([polyline([(CX, CY - R - 26), (CX, CY - R - 4)]), stroke(slot="secondary", width=12)], "hammer-stem"),
        group([ellipse((30, 20), (CX, CY - R - 30)), fill(slot="secondary")], "hammer"),
    ]
    bells = []
    for s in (-1, 1):
        ang = s * 48
        bx, by = CX + (R + 4) * math.sin(math.radians(ang)), CY - (R + 4) * math.cos(math.radians(ang))
        bells.append(group([arc_path(40, 180, 360, (0, 0)), fill(slot="secondary")], "bell",
                           anchor=(0, 0), position=(bx, by), rotation=ang))
    comp.layer("clock", bells + body, anchor=(CX, CY + R), position=(CX, CY + R), rotation=shake)
    comp.layer("waves-r", ring_waves(F, "accent", 1))
    comp.layer("waves-l", ring_waves(F, "accent", -1))
    return comp


def minimal():
    F = 60
    comp = Comp("alarm-clock", 300, 300, frames=F)
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#FF9F0A")
    shake = Anim([(0, 0, EASE_IN_OUT), (4, -7, EASE_IN_OUT), (8, 7, EASE_IN_OUT), (12, -7, EASE_IN_OUT), (16, 7, EASE_IN_OUT),
                  (20, 0, EASE_IN_OUT), (30, 0, HOLD), (34, -7, EASE_IN_OUT), (38, 7, EASE_IN_OUT), (42, -7, EASE_IN_OUT),
                  (46, 7, EASE_IN_OUT), (50, 0, EASE_IN_OUT), (F, 0)])
    sh = [
        *[group([arc_path(R + 24, a0, a1, (CX, CY)), stroke(slot="accent", width=12)], f"ear{a0}")
          for a0, a1 in ((190, 240), (300, 350))],
        *hands("icon", 12),
        group([ellipse((2 * R - 8, 2 * R - 8), (CX, CY)), stroke(slot="icon", width=14)], "ring"),
    ]
    comp.layer("alarm", sh, anchor=(CX, CY), position=(CX, CY), rotation=shake)
    return comp


build_asset(CAT, "alarm-clock", "Alarm Clock",
            "Ringing alarm clock icon that shakes with ring waves around it, as a chunky twin-bell clock or a "
            "minimal outlined clock with alarm arcs.",
            ["alarm", "clock", "wake up", "time", "morning", "ring", "timer", "reminder"], [
    Variant("classic", "Twin Bell", classic(), "loop", thumb_t=0.1, bg="6a7087"),
    Variant("minimal", "Outline", minimal(), "loop", thumb_t=0.1, bg="6a7087"),
])
