from _sticker import *

W, H = 760, 400
comp = sticker_comp("story-question-sticker", W, H)
comp.slot("accent", "#C13584")
sh = [label("Type something...", W / 2, 322, 34, 500, slot="icon", opacity=45, anchor="c"),
      group([rect_tl(50, 250, W - 100, 100, 28), fill(slot="secondary")], "input"),
      group([rect_tl(0, 0, W, 170), fill(slot="accent")], "header-fill"),
      group(rrect_path(20, 20, W - 40, 150, 40, 40, 0, 0) + [fill(slot="accent")], "header"),
      group([rect_tl(20, 20, W - 40, H - 40, 40), fill(slot="background")], "card")]
# remove stray full-width rect
sh = [s for s in sh if s["nm"] != "header-fill"]
pop_sticker(comp, sh, W, H)
build_asset(CAT, "story-question-sticker", "Story Question Sticker",
            "Story-style 'ask me a question' box: a coloured header for your prompt above a white card with a "
            "'Type something...' field. Put your prompt in the text area.",
            ["question", "ask me", "story", "instagram", "sticker", "q&a", "social", "prompt"], [
    Variant("question", "Question Box", comp, "intro-hold", text_area=(60, 44, W - 120, 110),
            text_areas={"prompt": (60, 44, W - 120, 110), "answer": (80, 262, W - 160, 76)}, thumb_t=0.95, bg="3a5a8a")])
