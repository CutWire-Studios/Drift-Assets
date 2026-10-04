import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

W, H = 900, 1240
F = 120
YEL = "#E4A400"


def note(kind):
    comp = Comp("apple-notes", W, H, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("secondary", "#F7F7F7")
    comp.slot("icon", "#1C1C1E")
    comp.slot("primary", YEL)
    comp.slot("outline", "#8E8E93")
    top = 120
    sh = []
    # toolbar (bottom)
    ty = H - 70
    sh += [glyph("image", 0, 0, 0, slot="outline", opacity=0) if False else group([], "n")]
    sh += [group([polyline([(W - 110, ty + 22), (W - 70, ty - 22), (W - 50, ty - 2), (W - 90, ty + 42)], closed=True), stroke(slot="primary", width=4, join="round")], "pencil"),
           glyph("camera", 46, W - 250, ty, slot="primary"),
           group([rect_tl(W - 500, ty - 24, 52, 48, 8), stroke(slot="primary", width=4)], "table"),
           label("Aa", 140, ty + 14, 42, 600, slot="primary", anchor="c")]
    sh += [group([ellipse((40, 40), (W - 640 + 0, ty)), stroke(slot="primary", width=4)], "check-circle") if False else group([ellipse((40, 40), (360, ty)), stroke(slot="primary", width=4)], "list"),
           group([polyline([(350, ty), (358, ty + 9), (373, ty - 9)]), stroke(slot="primary", width=4, join="round")], "list-check")]
    if kind == "checklist":
        for i in range(4):
            ry = 360 + i * 120
            t = 20 + i * 22
            sh += [group([ellipse((46, 46), (86, ry)), stroke(slot="outline", width=4)], f"ring{i}"),
                   group([ellipse((46, 46), (86, ry)), fill(slot="primary")], f"done{i}", anchor=(86, ry), position=(86, ry),
                         scale=Anim([(t, [0, 0], OVERSHOOT), (t + 10, [100, 100])]), opacity=Anim([(0, 0, HOLD), (t, 100, HOLD), (F, 100)])),
                   group([polyline([(74, ry), (83, ry + 10), (99, ry - 10)]), stroke(slot="background", width=5, join="round"),
                          trim(0, Anim([(t + 4, 0, EASE_OUT), (t + 12, 100)]))], f"tick{i}"),
                   group([polyline([(140, ry + 36), (W - 70, ry + 36)]), stroke(slot="outline", width=1.5, opacity=45)], f"rule{i}")]
        areas = {"title": (70, 150, W - 140, 80)}
        areas.update({f"item{i + 1}": (140, 336 + i * 120, W - 210, 52) for i in range(4)})
    else:
        sh += [group([rect_tl(76, 388, 4, 56, 2), fill(slot="primary")], "cursor",
                     opacity=Anim([(0, 100, HOLD), (30, 0, HOLD), (60, 100, HOLD), (90, 0, HOLD), (F, 100)]))]
        areas = {"title": (70, 150, W - 140, 80), "body": (70, 260, W - 140, 880)}
    # header
    sh += [glyph("more", 40, W - 54, 56, slot="primary"), glyph("share", 40, W - 140, 56, slot="primary"),
           group([polyline([(52, 38), (36, 56), (52, 74)]), stroke(slot="primary", width=5)], "back"),
           label("Notes", 70, 66, 34, 500, slot="primary")]
    sh += [group(rrect_path(0, 0, W, H, 40, 40, 40, 40, "card") + [fill(slot="background")], "page")]
    comp.layer("notes", sh, position=Anim([(0, [0, 60], EXPO_OUT), (16, [0, 0])]), opacity=fade(0, 8))
    return comp, areas


vs = []
for vid, nm, desc in (("note", "Blank Note", "Blank note page with a blinking yellow cursor and the Notes toolbar."),
                      ("checklist", "Checklist", "Checklist note: four yellow circles tick off one after another.")):
    c, a = note(vid)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["title"], text_areas=a, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "apple-notes", "Notes App",
            "Apple Notes-style page with a back button, share and more icons, the formatting toolbar and either a "
            "blinking cursor or a checklist that ticks off. Type the title and body in the text areas.",
            ["notes", "apple notes", "checklist", "to do", "list", "ios", "app", "text", "memo"], vs)
