from _common import *

W, H, F = 920, 250, 45
comp = Comp("to-be-continued-arrow", W, H, fps=30, frames=F)
comp.slot("primary", "#6B5A2E")
comp.slot("outline", "#000000")

CY = H / 2
TIP, NECK, END = 40, 196, 872
HEAD, BODY = 98, 50
PTS = [(TIP, CY), (NECK, CY - HEAD), (NECK, CY - BODY), (END, CY - BODY), (END, CY + BODY),
       (NECK, CY + BODY), (NECK, CY + HEAD)]


def arrow():
    return polyline(PTS, closed=True)


slide = anim([(0, [-420, 0], (0.2, 0.9, 0.4, 1)), (13, [16, 0], EASE_IN_OUT), (20, [-5, 0], EASE_IN_OUT),
              (26, [0, 0])])
comp.layer("arrow", [
    group([arrow(), stroke(slot="outline", width=9, join="miter")], "outline"),
    group([arrow(), gradient_fill([(0, "#FFFFFF", 0.16), (0.5, "#FFFFFF", 0.0), (1, "#000000", 0.18)],
                                  (0, CY - HEAD), (0, CY + HEAD))], "shade"),
    group([arrow(), fill(slot="primary")], "fill"),
    group([arrow(), stroke("#000000", 9, 35, join="miter"), fill("#000000", 35)], "shadow",
          position=(7, 7)),
], anchor=(W / 2, CY), position=anim([(t, [W / 2 + v[0], CY], e) for t, v, e in slide.keys]),
    skew=anim([(0, 14, EASE_OUT), (13, -3, EASE_IN_OUT), (22, 0)]), skew_axis=0,
    opacity=anim([(0, 0, EASE_OUT), (5, 100)]))

build(comp, "memes", "to-be-continued-arrow", "To Be Continued Arrow",
       "Olive 'to be continued' meme arrow with a black outline that slides in from the left and "
       "settles; type your caption inside it.",
       ["to be continued", "jojo", "meme", "arrow", "ending", "cliffhanger"], "intro-hold",
       thumb_t=1.0, bg="e8e8ee", text_area=[206, 83, 656, 84])
