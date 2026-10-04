from _sticker import *

W, H = 560, 190


def mention(style):
    comp = sticker_comp("story-mention-sticker", W, H)
    comp.slot("accent", "#C13584")
    sh = []
    if style == "white":
        sh += [label("@", 54, 118, 70, 700, slot="accent"), group([rect_tl(20, 20, W - 40, H - 40, 48), fill(slot="background")], "pill")]
    else:
        sh += [label("@", 54, 118, 70, 700, slot="background"), group([rect_tl(20, 20, W - 40, H - 40, 48), fill(slot="accent")], "pill")]
    pop_sticker(comp, sh, W, H)
    return comp


build_asset(CAT, "story-mention-sticker", "Story Mention Sticker",
            "Story @mention sticker: a rounded pill with a big @ sign, in white or solid colour. Type the username in "
            "the text area.",
            ["mention", "story", "instagram", "sticker", "tag", "username", "at sign", "social"], [
    Variant("white", "White Pill", mention("white"), "intro-hold", text_area=(120, 62, 400, 66), thumb_t=0.95, bg="3a5a8a"),
    Variant("solid", "Solid Pill", mention("solid"), "intro-hold", text_area=(120, 62, 400, 66), thumb_t=0.95, bg="3a5a8a")])
