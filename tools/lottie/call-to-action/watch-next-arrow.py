from _cta_actions import *

W, H = 820, 290
N = 120
OUT = 96
A = (112, 140)  # arrow centre
CX, CY, CW, CH = 504, 140, 560, 210
TB = (CX - CW / 2 + 26 + 100, CY)  # thumbnail placeholder centre (200x112)
TEXT = (TB[0] + 100 + 26, CY - 52, CX + CW / 2 - 28 - (TB[0] + 126), 104)


def arrow():
    return [shape([(-72, -26), (8, -26), (8, -64), (78, 0), (8, 64), (8, 26), (-72, 26)], [8, 3, 10, 14, 10, 3, 8],
                  name="arrow")]


def play(k=1.0):
    return [shape([(-14 * k, -18 * k), (20 * k, 0), (-14 * k, 18 * k)], 5 * k, name="play")]


def make(style):
    comp = Comp(f"watch-next-arrow--{style}", W, H, fps=30, frames=N)
    comp.marker("intro", 0, 56)
    comp.marker("outro", OUT, N - OUT)
    comp.slot("primary", "#FF5A36")
    comp.slot("outline" if style == "outline" else "background", "#FFFFFF")
    if style != "outline":
        comp.slot("secondary", "#2B2B36")
    # card slides in from the right, and back out
    card = comp.null("card", position=anim([(6, [CX + 340, CY], DECEL), (26, [CX, CY], HOLD), (OUT + 4, [CX, CY], ANTICIPATE),
                                            (N - 2, [CX + 620, CY])]))
    rel = (TB[0] - CX, 0)
    cop = anim([(6, 0, EASE_OUT), (12, 100, HOLD), (N - 8, 100, EASE_IN), (N - 2, 0)])
    if style == "outline":
        draw = trim(end=anim([(8, 0, EASE_IN_OUT), (30, 100)]), offset=anim([(8, -25, EASE_IN_OUT), (30, 0)]))
        comp.layer("play", [group(play() + [stroke(slot="outline", width=4)], "p")], parent=card, position=rel,
                   scale=pop(22, 14))
        comp.layer("thumb", [rect((200, 112), roundness=14), draw, stroke(slot="primary", width=4)], parent=card,
                   position=rel)
        comp.layer("card-line", [rect((CW, CH), roundness=34), draw, stroke(slot="outline", width=5)], parent=card)
    else:
        body(comp, "play", play(), "classic", slot="background", parent=card, position=rel, shadow=False,
             scale=pop(22, 14), opacity=cop)
        body(comp, "thumb", [rect((200, 112), roundness=14)], "classic", slot="secondary", parent=card, position=rel,
             shadow=False, opacity=cop)
        body(comp, "card-body", [rect((CW, CH), roundness=34)], style, slot="background", parent=card, depth=12,
             opacity=cop)
    # arrow: springs in, nudges twice towards the card
    nudge = [(0, [A[0], A[1]], HOLD)]
    for t in (30, 42):
        nudge += [(t, [A[0], A[1]], EASE_OUT), (t + 4, [A[0] + 22, A[1]], EASE_IN_OUT), (t + 11, [A[0], A[1]], LINEAR)]
    nudge.append((N, [A[0], A[1]]))
    body(comp, "arrow", arrow(), style, slot="primary", position=anim(nudge), depth=12, line=6, line_slot="primary",
         scale=pop(0, 16, out_at=OUT, out_dur=12), rotation=anim([(0, -30, SNAP_OUT), (18, 0)]))
    return comp


build_asset(CATEGORY, "watch-next-arrow", "Watch Next Arrow",
            "Arrow that springs in and nudges towards a video card sliding in from the right; the card has a "
            "thumbnail placeholder and room for a title. Type \"Watch next\" or the video title in the card.",
            ["watch next", "next video", "arrow", "card", "up next", "end screen"], [
    Variant(s, STYLE_NAMES[s], make(s), "intro-hold-outro", thumb_t=0.6, text_area=TEXT, text_areas={"title": TEXT},
            description=STYLE_DESC[s]) for s in STYLES])
