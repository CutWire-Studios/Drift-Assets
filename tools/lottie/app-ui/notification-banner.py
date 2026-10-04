import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 105


def ios():
    W, H = 1000, 230
    comp = Comp("notification-banner", W, H, frames=F)
    comp.slot("background", "#2C2C2E")
    comp.slot("icon", "#FFFFFF")
    comp.slot("primary", "#34C759")
    comp.slot("outline", "#A0A0A8")
    sh = [label("now", W - 40, 70, 26, 400, slot="outline", anchor="r"),
          glyph("send", 40, 70, 110, slot="icon") if False else group([], "n"),
          group([rect_tl(30, 36, 100, 100, 24), fill(slot="primary")], "app-icon"),
          group([rect_tl(0, 0, W, H, 54), fill(slot="background", opacity=94)], "card")]
    sh[1] = glyph("comment", 54, 80, 86, slot="icon")
    sh = [sh[0], sh[1], sh[2], sh[3]]
    comp.layer("banner", sh, position=Anim([(0, [0, -260], EXPO_OUT), (16, [0, 0], HOLD), (F - 24, [0, 0], EXPO_IN), (F, [0, -260])]) if False else
               Anim([(0, [0, -260], EXPO_OUT), (18, [0, 0])]), opacity=fade(0, 8))
    return comp, {"title": (156, 36, 600, 44), "message": (156, 88, 800, 100)}


def android():
    W, H = 1000, 260
    comp = Comp("notification-banner", W, H, frames=F)
    comp.slot("background", "#F2F2F7")
    comp.slot("icon", "#1B1B1F")
    comp.slot("primary", "#1A73E8")
    comp.slot("outline", "#5F6368")
    sh = [label("now", 220, 56, 26, 500, slot="outline"), group([ellipse((8, 8), (190, 48)), fill(slot="outline")], "dot"),
          glyph("comment", 30, 62, 46, slot="primary"), glyph("more", 30, W - 54, 48, slot="outline"),
          group([ellipse((90, 90), (W - 100, 160)), fill(slot="primary", opacity=18)], "avatar"),
          group([rect_tl(0, 0, W, H, 40), fill(slot="background")], "card")]
    comp.layer("banner", sh, position=Anim([(0, [0, -300], EXPO_OUT), (18, [0, 0])]), opacity=fade(0, 8))
    return comp, {"title": (50, 84, 740, 44), "message": (50, 134, 740, 90)}


def macos():
    W, H = 760, 190
    comp = Comp("notification-banner", W, H, frames=F)
    comp.slot("background", "#F3F3F3")
    comp.slot("icon", "#1D1D1F")
    comp.slot("primary", "#34C759")
    comp.slot("outline", "#6E6E73")
    sh = [label("now", W - 28, 52, 22, 400, slot="outline", anchor="r"),
          glyph("comment", 40, 68, 96, slot="icon"),
          group([rect_tl(24, 36, 88, 88, 22), fill(slot="primary")], "app-icon"),
          group([rect_tl(0, 0, W, H, 34), fill(slot="background", opacity=96)], "card")]
    sh[1] = glyph("comment", 46, 68, 80, slot="icon")
    sh = [sh[0], sh[1], sh[2], sh[3]]
    comp.layer("banner", sh, position=Anim([(0, [380, 0], EXPO_OUT), (18, [0, 0])]), opacity=fade(0, 8))
    return comp, {"title": (136, 32, 480, 38), "message": (136, 78, 590, 84)}


vs = []
for vid, nm, fn, desc in (("ios", "iPhone Banner", ios, "Rounded dark push-notification banner drops from the top with an app icon, 'now' and title / message areas."),
                          ("android", "Android Card", android, "Material-style notification card with app glyph, 'now', avatar and text areas."),
                          ("macos", "macOS Banner", macos, "macOS notification banner sliding in from the right.")):
    c, a = fn()
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["message"], text_areas=a, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "notification-banner", "Notification Banner",
            "Push-notification banners that slide in: iPhone, Android and macOS styles with an app-icon tile. Type the "
            "title and message in the text areas.",
            ["notification", "push", "banner", "alert", "ios", "android", "macos", "message", "toast"], vs)
