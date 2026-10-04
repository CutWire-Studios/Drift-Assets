from _sticker import *

W, H = 760, 420
comp = sticker_comp("story-poll-sticker", W, H)
comp.slot("accent", "#FF3B6B")
sh = []
# two option halves; the left one wins and fills
sh += [label("YES", 190, 330, 40, 800, slot="icon", anchor="c"), label("NO", 570, 330, 40, 800, slot="icon", anchor="c")] if False else []
ox, oy, ow, oh = 50, 220, 330, 130
for i, (x, nm) in enumerate(((ox, "left"), (ox + ow + 20, "right"))):
    pct = 0.68 if i == 0 else 0.32
    sh += [group([grow_rect(x, oy, ow * pct, oh, 24, 50, 26, EXPO_OUT), fill(slot="primary" if i == 0 else "secondary", opacity=100 if i == 0 else 100)], f"fill-{nm}"),
           group([rect_tl(x, oy, ow, oh, 26), fill(slot="secondary")], f"opt-{nm}")]
sh += [group([ellipse((44, 44), (W / 2, oy + oh / 2)), fill(slot="background")], "vs") if False else group([], "n")]
sh += [group([rect_tl(20, 20, W - 40, H - 40, 40), fill(slot="background")], "card")]
pop_sticker(comp, sh, W, H)
build_asset(CAT, "story-poll-sticker", "Story Poll Sticker",
            "Story-style poll sticker: a white card with a question area and two answer pills; the winning pill fills "
            "with colour. Type the question and the two answers in the text areas.",
            ["poll", "story", "instagram", "sticker", "vote", "question", "yes no", "social"], [
    Variant("poll", "Poll", comp, "intro-hold", text_area=(60, 56, W - 120, 120),
            text_areas={"question": (60, 56, W - 120, 120), "answer1": (ox + 20, oy + 40, ow - 40, 50), "answer2": (ox + ow + 40, oy + 40, ow - 40, 50)},
            thumb_t=0.95, bg="3a5a8a")])
