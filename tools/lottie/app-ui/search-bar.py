import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 90


def google():
    W, H = 1100, 150
    comp = Comp("search-bar", W, H, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("icon", "#5F6368")
    comp.slot("outline", "#DFE1E5")
    comp.slot("primary", "#4285F4")
    sh = [glyph("mic", 44, W - 150, 75, slot="primary"), group([ellipse((40, 40), (W - 80, 75)), stroke(slot="icon", width=4)], "lens"),
          group([rect_tl(112, 45, 3, 60, 1), fill(slot="icon")], "caret", opacity=Anim([(0, 100, HOLD), (22, 0, HOLD), (44, 100, HOLD), (66, 0, HOLD), (F, 100)])),
          magnifier(64, 75, 22, slot="icon", w=5),
          group([rect_tl(20, 20, W - 40, 110, 55), stroke(slot="outline", width=2)], "edge"),
          group([rect_tl(20, 20, W - 40, 110, 55), fill(slot="background")], "pill")]
    comp.layer("bar", sh, anchor=(W / 2, 75), position=(W / 2, 75), scale=Anim([(0, [90, 90], EXPO_OUT), (14, [100, 100])]), opacity=fade(0, 8))
    comp.layer("shadow", soft_shadow(20, 20, W - 40, 110, 55, spread=16, dy=8, strength=20), opacity=fade(0, 8))
    return comp, {"query": (130, 40, 700, 70)}


def suggestions():
    W, H = 1100, 560
    comp = Comp("search-bar", W, H, frames=F)
    comp.slot("background", "#FFFFFF")
    comp.slot("icon", "#5F6368")
    comp.slot("outline", "#DFE1E5")
    comp.slot("primary", "#4285F4")
    sh = []
    areas = {"query": (130, 40, 700, 70)}
    for i in range(3):
        y = 190 + i * 110
        t = 14 + i * 5
        sh.append(group([magnifier(64, y, 20, slot="icon", w=4.5)], f"s{i}", opacity=fade(t, t + 8)))
        areas[f"suggestion{i + 1}"] = (130, y - 32, 780, 64)
    sh += [glyph("mic", 44, W - 150, 75, slot="primary"), group([ellipse((40, 40), (W - 80, 75)), stroke(slot="icon", width=4)], "lens"),
           magnifier(64, 75, 22, slot="icon", w=5),
           group([polyline([(60, 150), (W - 60, 150)]), stroke(slot="outline", width=2)], "div"),
           group([rect_tl(112, 45, 3, 60, 1), fill(slot="icon")], "caret", opacity=Anim([(0, 100, HOLD), (22, 0, HOLD), (44, 100, HOLD), (66, 0, HOLD), (F, 100)])),
           group([rect_tl(20, 20, W - 40, 520, 55), fill(slot="background")], "card")]
    comp.layer("bar", sh, anchor=(W / 2, 75), position=(W / 2, 75), scale=Anim([(0, [90, 90], EXPO_OUT), (14, [100, 100])]), opacity=fade(0, 8))
    comp.layer("shadow", soft_shadow(20, 20, W - 40, 520, 55, spread=16, dy=8, strength=20), opacity=fade(0, 8))
    return comp, areas


def spotlight():
    W, H = 1100, 190
    comp = Comp("search-bar", W, H, frames=F)
    comp.slot("background", "#ECECEC")
    comp.slot("icon", "#6E6E73")
    comp.slot("outline", "#C7C7CC")
    sh = [group([rect_tl(112, 55, 3, 80, 1.5), fill(slot="icon")], "caret", opacity=Anim([(0, 100, HOLD), (22, 0, HOLD), (44, 100, HOLD), (66, 0, HOLD), (F, 100)])),
          magnifier(78, 95, 30, slot="icon", w=6),
          group([rect_tl(24, 24, W - 48, 142, 40), stroke(slot="outline", width=2)], "edge"),
          group([rect_tl(24, 24, W - 48, 142, 40), fill(slot="background", opacity=96)], "box")]
    comp.layer("bar", sh, anchor=(W / 2, 95), position=(W / 2, 95), scale=Anim([(0, [90, 90], EXPO_OUT), (14, [100, 100])]), opacity=fade(0, 8))
    comp.layer("shadow", soft_shadow(24, 24, W - 48, 142, 40, spread=22, dy=12, strength=24), opacity=fade(0, 8))
    return comp, {"query": (140, 52, 880, 86)}


vs = []
for vid, nm, fn, desc in (("pill", "Search Pill", google, "Rounded search pill with a magnifier, blinking caret, mic and lens icons."),
                          ("suggestions", "With Suggestions", suggestions, "Search pill that drops a three-row suggestion list below it."),
                          ("spotlight", "Desktop Spotlight", spotlight, "Large desktop launcher search field with a magnifier and caret.")):
    c, a = fn()
    vs.append(Variant(vid, nm, c, "intro-hold", text_area=a["query"], text_areas=a, thumb_t=0.95, bg="6a7087", description=desc))
build_asset(CAT, "search-bar", "Search Bar",
            "Search box UI with a blinking caret: Google-style pill, one with a suggestions dropdown, and a desktop "
            "Spotlight-style launcher. Type the query (and suggestions) in the text areas.",
            ["search", "google", "query", "search bar", "spotlight", "typing", "input", "web", "meme"], vs)
