import math
from _common import *
from _lt2 import rrect, lay, fade, SPRING, BACK_IN
from drift_lottie import Variant, build_asset

W, H = 820, 280
CX, CY = 405, 135
PW, PH, R = 680, 170, 34
OUT = 6
SH = 14

def classic():
    """Chunky plate with an offset shadow pops in with overshoot."""
    comp = Comp("title-plate-bold", W, H, fps=FPS, frames=FRAMES)
    comp.slot("primary", "#FFD23F")
    comp.slot("secondary", "#1B1B2F")
    comp.slot("accent", "#FF5A5F")
    comp.marker("intro", 0, 24)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)

    # sparks off the top-left corner
    corner = (CX - PW / 2 + 6, CY - PH / 2 + 6)
    sparks = []
    for i, ang in enumerate((200, 225, 250)):
        a = math.radians(ang)
        p0 = (corner[0] + math.cos(a) * 24, corner[1] + math.sin(a) * 24)
        p1 = (corner[0] + math.cos(a) * 52, corner[1] + math.sin(a) * 52)
        sparks.append(polyline([p0, p1], name=f"spark{i}"))
    comp.layer("sparks", sparks + [
        stroke(slot="accent", width=7, cap="round"),
        trim(start=keys((0, 0, HOLD), (18, 0, EXPO_OUT), (32, 100, HOLD), (34, 0)),
             end=keys((0, 0, HOLD), (14, 0, EXPO_OUT), (24, 100))),
    ], ip=0, op=34)

    rig = comp.null("rig", anchor=(0, 0), position=(CX, CY),
                    scale=keys((0, [0, 0], (0.3, 0.9, 0.5, 1)), (8, [112, 112], EASE_IN_OUT),
                               (13, [96, 96], EASE_IN_OUT), (18, [101.5, 101.5], EASE_IN_OUT),
                               (23, [100, 100], HOLD), (120, [100, 100], EASE_OUT),
                               (126, [106, 106], (0.6, 0, 0.9, 0.4)), (136, [0, 0])),
                    rotation=keys((0, -7, (0.3, 0.9, 0.4, 1)), (18, 0, HOLD), (126, 0, EASE_IN), (136, 5)))

    plate = [rect((PW, PH), roundness=R), fill(slot="primary"), stroke(slot="secondary", width=OUT, join="round")]
    comp.layer("plate", plate, parent=rig)
    comp.layer("shadow", [rect((PW, PH), roundness=R), fill(slot="secondary"),
                          stroke(slot="secondary", width=OUT, join="round")], parent=rig,
               position=keys((0, [0, 0], HOLD), (9, [0, 0], OVERSHOOT), (20, [SH, SH], HOLD),
                             (120, [SH, SH], EASE_IN), (127, [0, 0])))
    return comp


def slots(comp):
    comp.slot("primary", "#FFD23F")
    comp.slot("secondary", "#1B1B2F")
    comp.slot("accent", "#FF5A5F")


def hang():
    """A sign drops in on two strings from a nail and swings until it settles."""
    comp = Comp("title-plate-bold--hang", W, H, fps=FPS, frames=FRAMES)
    slots(comp)
    comp.marker("intro", 0, 44)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    nail = (CX, 16)
    pw, ph, py = 640, 140, 86
    ex = 230
    holes = [(CX - ex, py + 22), (CX + ex, py + 22)]
    swing = keys((0, 12, EASE_OUT), (12, -6, EASE_IN_OUT), (22, 4, EASE_IN_OUT), (31, -2.5, EASE_IN_OUT),
                 (39, 1.2, EASE_IN_OUT), (46, -0.5, EASE_IN_OUT), (52, 0, HOLD), (118, 0, EASE_IN), (126, -3, EASE_IN),
                 (140, 14))
    rig = comp.null("rig", anchor=nail, position=keys((0, [nail[0], nail[1] - 420], (0.5, 0, 0.8, 0.6)),
                                                     (8, [nail[0], nail[1] + 6], EASE_OUT), (13, list(nail), HOLD),
                                                     (122, list(nail), (0.5, 0, 0.9, 0.4)),
                                                     (140, [nail[0], nail[1] + 320])),
                    rotation=swing)
    comp.layer("nail", [ellipse((20, 20), nail), fill(slot="accent"), stroke(slot="secondary", width=4)],
               scale=keys((6, [0, 0], SPRING), (16, [100, 100], HOLD), (130, [100, 100], EASE_IN), (138, [0, 0])),
               anchor=nail, position=nail)
    comp.layer("holes", [ellipse((16, 16), h) for h in holes] + [fill(slot="secondary")], parent=rig)
    comp.layer("strings", [polyline([holes[0], nail, holes[1]]), stroke(slot="secondary", width=5, join="round")],
               parent=rig)
    comp.layer("plate", [rrect(CX - pw / 2, py, pw, ph, 28), fill(slot="primary"),
                         stroke(slot="secondary", width=OUT, join="round")], parent=rig)
    comp.layer("plate-lip", [rrect(CX - pw / 2, py + 10, pw, ph, 28), fill(slot="secondary"),
                             stroke(slot="secondary", width=OUT, join="round")], parent=rig)
    return comp, {"title": [CX - pw / 2 + 40, py + 40, pw - 80, ph - 64]}


def stack():
    """Three rounded plates fan out from behind each other; the front plate lands with a squash."""
    comp = Comp("title-plate-bold--stack", W, H, fps=FPS, frames=FRAMES)
    slots(comp)
    comp.marker("intro", 0, 30)
    comp.marker("outro", OUTRO, FRAMES - OUTRO)
    pw, ph = 640, 156
    c = (CX, CY)
    layers = (("front", "primary", 0, 0, 6, 124), ("mid", "accent", -4.5, 0, 12, 120),
              ("back", "secondary", 3.5, 0, 16, 116))
    for nm, slot, rot, _, t0, t2 in layers:
        if nm == "front":
            sc = keys((0, [0, 0], (0.3, 0.9, 0.5, 1)), (8, [110, 110], EASE_IN_OUT), (13, [97, 97], EASE_IN_OUT),
                      (18, [100, 100], HOLD), (t2, [100, 100], EASE_OUT), (t2 + 5, [106, 106], BACK_IN), (t2 + 16, [0, 0]))
            lay(comp, nm, [rrect(CX - pw / 2, CY - ph / 2, pw, ph, 30), fill(slot=slot),
                           stroke(slot="secondary", width=OUT, join="round")], c, scale=sc)
            continue
        lay(comp, nm, [rrect(CX - pw / 2, CY - ph / 2, pw, ph, 30), fill(slot=slot),
                       stroke(slot="secondary", width=OUT, join="round")], c,
            rotation=keys((0, 0, HOLD), (t0, 0, SPRING), (t0 + 16, rot, HOLD), (t2, rot, EASE_IN), (t2 + 10, 0)),
            scale=keys((0, [0, 0], HOLD), (t0 - 6, [0, 0], (0.3, 0.9, 0.5, 1)), (t0 + 2, [100, 100], HOLD),
                       (t2 + 8, [100, 100], EASE_IN), (t2 + 16, [0, 0])))
    return comp, {"title": [CX - pw / 2 + 40, CY - ph / 2 + 30, pw - 80, ph - 60]}


hc, ha = hang()
sc, sa = stack()
build_asset("lower-thirds", "title-plate-bold", "Bold Title Plate",
            "Chunky rounded title plate for section titles, with a bold outline and room for one line of text.",
            ["title", "section", "plate", "bold", "pop", "chapter", "badge"], [
    Variant("classic", "Pop", classic(), "intro-hold-outro",
            text_area=[CX - PW / 2 + 40, CY - PH / 2 + 28, PW - 80, PH - 56],
            thumb_t=0.5, bg="e8e8ee",
            description="Chunky rounded plate with an offset drop shadow that pops in with overshoot and sparks."),
    Variant("hang", "Hanging Sign", hc, "intro-hold-outro", text_area=ha["title"], thumb_t=0.5,
            bg="e8e8ee",
            description="The plate drops in on two strings from a nail and swings until it settles, then falls "
                        "away."),
    Variant("stack", "Fanned Stack", sc, "intro-hold-outro", text_area=sa["title"], thumb_t=0.5,
            bg="e8e8ee",
            description="The plate pops in and two coloured plates fan out from behind it at playful angles."),
])
