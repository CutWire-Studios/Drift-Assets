import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 75
W = 1000


def card(hearted, F=F):
    H = 420 if not hearted else 470
    comp = Comp("youtube-comment-card", W, H, frames=F)
    comp.slot("background", "#0F0F0F")
    comp.slot("icon", "#F1F1F1")
    comp.slot("outline", "#AAAAAA")
    comp.slot("secondary", "#3A3A3A")
    comp.slot("primary", "#FF0000")
    top = 40 if not hearted else 90
    sh = []
    ay = H - 62
    sh += [glyph("more", 32, W - 50, top + 18, slot="outline"),
           label("Reply", 380, ay + 10, 30, 600, slot="outline"),
           glyph("thumb", 36, 272, ay, slot="outline", rotation=180), glyph("thumb", 36, 70, ay, slot="outline")]
    liked = group([glyph("thumb", 36, 70, ay, slot="icon")], "liked", opacity=Anim([(0, 0, HOLD), (30, 100, HOLD), (F, 100)]),
                  anchor=(70, ay), position=(70, ay), scale=Anim([(30, [0, 0], OVERSHOOT), (42, [100, 100])]))
    sh = [liked] + sh
    if hearted:
        sh += [glyph("heart", 26, 118, top - 50 + 12 - 12, slot="primary") if False else group([], "n"),
               glyph("heart", 26, 56, 52, slot="primary"), label("Hearted by creator", 84, 60, 26, 500, slot="outline")]
    sh += [avatar(70, top + 46, 76, slot="secondary", fg="outline", fg_opacity=100)]
    if hearted:
        sh += [group([ellipse((38, 38), (96, top + 76)), fill(slot="primary")], "badge-bg"), glyph("heart", 22, 96, top + 76, slot="icon")]
        sh = sh[:-1] + [sh[-1]]
    sh += [group([rect_tl(0, 0, W, H, 28), fill(slot="background")], "card")]
    comp.layer("card", sh, position=Anim([(0, [0, 40], EXPO_OUT), (14, [0, 0])]), opacity=fade(0, 8))
    areas = {"username": (130, top + 10, 500, 36), "time": (640, top + 10, 200, 36), "comment": (130, top + 56, W - 190, H - top - 170)}
    return comp, areas


vs = []
for vid, h, nm, desc in (("comment", False, "Comment", "Dark-mode comment with avatar, @name, time, comment text, like / dislike and Reply; the like lights up."),
                         ("hearted", True, "Hearted by Creator", "Same comment with the 'Hearted by creator' row and a red heart badge on the avatar.")):
    c, a = card(h)
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["comment"], text_areas=a, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "youtube-comment-card", "Video Comment Card",
            "Comment card in the style of YouTube's dark mode: avatar, @username, time and comment text areas, a like that "
            "lights up, dislike and Reply. Great for reading out viewer comments.",
            ["youtube", "comment", "comments", "reply", "social", "like", "card", "viewer", "reaction"], vs)
