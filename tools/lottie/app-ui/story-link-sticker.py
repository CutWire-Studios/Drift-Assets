from _sticker import *

W, H = 560, 190


def link_sticker(style):
    comp = sticker_comp("story-link-sticker", W, H)
    comp.slot("accent", "#3897F0")
    L = ("M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z")
    sh = []
    if style == "classic":
        sh += [label("LINK", 190, 112, 46, 800, slot="accent"), group(svg_shapes(L, 56 / 24, (88 - 28, 95 - 28)) + [fill(slot="accent")], "link"),
               group([rect_tl(20, 20, W - 40, H - 40, 48), fill(slot="background")], "pill")]
    else:
        sh += [group(svg_shapes(L, 56 / 24, (60 - 28, 95 - 28)) + [fill(slot="background")], "link"),
               group([rect_tl(20, 20, W - 40, H - 40, 48), fill(slot="accent")], "pill")]
    pop_sticker(comp, sh, W, H)
    return comp


area = (170, 62, 330, 66)
build_asset(CAT, "story-link-sticker", "Story Link Sticker",
            "Story link sticker: a white pill with a chain icon and the word LINK, or a solid blue pill with the chain; "
            "the pill pops in with a rotation and a gentle pulse. Type the link text in the text area.",
            ["link", "story", "instagram", "sticker", "swipe up", "url", "bio", "social"], [
    Variant("classic", "White Pill", link_sticker("classic"), "intro-hold", text_area=(300, 62, 220, 66), thumb_t=0.95, bg="3a5a8a"),
    Variant("solid", "Blue Pill", link_sticker("solid"), "intro-hold", text_area=area, thumb_t=0.95, bg="3a5a8a")])
