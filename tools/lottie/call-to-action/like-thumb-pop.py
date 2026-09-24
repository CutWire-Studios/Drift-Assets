from _common import *

W = H = 440
N = 60
comp = Comp("like-thumb-pop", W, H, fps=30, frames=N)
comp.slot("primary", "#3EA6FF")
comp.slot("outline", "#FFFFFF")
comp.slot("accent", "#9AD2FF")

SIZE = 230
CENTER = (W / 2, H / 2 + 4)
PIVOT = (CENTER[0] - 60, CENTER[1] + 100)  # near the cuff, so the thumb rocks from the wrist
LOCAL = (CENTER[0] - PIVOT[0], CENTER[1] - PIVOT[1])
SW = 15

HIT = 20  # frame the fill starts

thumb = comp.null("thumb", position=PIVOT, scale=anim([
    (0, [0, 0], SPRING), (12, [100, 100], EASE_IN_OUT), (HIT - 5, [100, 100], EASE_IN),
    (HIT, [88, 88], SNAP_OUT), (HIT + 6, [122, 122], EASE_IN_OUT), (HIT + 13, [95, 95], EASE_IN_OUT),
    (HIT + 20, [102, 102], EASE_IN_OUT), (HIT + 27, [100, 100])]),
    rotation=anim([(0, -25, SNAP_OUT), (12, 0, EASE_IN_OUT), (HIT - 5, 0, EASE_IN), (HIT, 8, SNAP_OUT),
                   (HIT + 6, -16, EASE_IN_OUT), (HIT + 14, 5, EASE_IN_OUT), (HIT + 21, -2, EASE_IN_OUT),
                   (HIT + 28, 0)]))


def thumb_shape(paint):
    return [group(glyph(THUMB, SIZE, LOCAL, name="thumb") + paint, "thumb")]


# fill revealed by a circle growing from the cuff
comp.layer("fill-matte", [group([ellipse(anim([(HIT, [0, 0], EASE_OUT), (HIT + 9, [560, 560])])), fill()],
                                "wipe", position=(0, 0))], parent=thumb)
comp.layer("thumb-fill", thumb_shape([fill(slot="primary"), stroke(slot="primary", width=SW)]),
           parent=thumb, matte="alpha")
comp.layer("thumb-outline", thumb_shape([stroke(slot="outline", width=SW)]), parent=thumb,
           op=HIT + 10)

burst(comp, CENTER, HIT + 3, 160, 204, count=8, slot="accent", width=11, rotation=22.5)

build(comp, "like-thumb-pop", "Like Thumb Pop",
      "Outlined thumbs-up that pops in, fills with colour and bounces with a particle burst.",
      ["like", "thumbs up", "youtube", "reaction"], "intro-hold", thumb_t=0.48)
