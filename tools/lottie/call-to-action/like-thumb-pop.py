from _common import *
from _cta_actions import body
from drift_lottie import Variant, build_asset

W = H = 440
N = 60
SIZE = 230
CENTER = (W / 2, H / 2 + 4)
PIVOT = (CENTER[0] - 60, CENTER[1] + 100)  # near the cuff, so the thumb rocks from the wrist
LOCAL = (CENTER[0] - PIVOT[0], CENTER[1] - PIVOT[1])
SW = 15
HIT = 20  # frame the fill starts


def rock(hit):
    scale = anim([
        (0, [0, 0], SPRING), (12, [100, 100], EASE_IN_OUT), (hit - 5, [100, 100], EASE_IN),
        (hit, [88, 88], SNAP_OUT), (hit + 6, [122, 122], EASE_IN_OUT), (hit + 13, [95, 95], EASE_IN_OUT),
        (hit + 20, [102, 102], EASE_IN_OUT), (hit + 27, [100, 100])])
    rot = anim([(0, -25, SNAP_OUT), (12, 0, EASE_IN_OUT), (hit - 5, 0, EASE_IN), (hit, 8, SNAP_OUT),
                (hit + 6, -16, EASE_IN_OUT), (hit + 14, 5, EASE_IN_OUT), (hit + 21, -2, EASE_IN_OUT),
                (hit + 28, 0)])
    return scale, rot


def classic():
    """Outlined thumb pops in, fills with colour from the cuff and bounces with a burst."""
    comp = Comp("like-thumb-pop", W, H, fps=30, frames=N)
    comp.slot("primary", "#3EA6FF")
    comp.slot("outline", "#FFFFFF")
    comp.slot("accent", "#9AD2FF")
    scale, rot = rock(HIT)
    thumb = comp.null("thumb", position=PIVOT, scale=scale, rotation=rot)

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
    return comp


def pop3d():
    """Chunky layered 3D thumb springs in and rocks on its wrist with a burst."""
    comp = Comp("like-thumb-pop--3d-pop", W, H, fps=30, frames=N)
    comp.slot("primary", "#3EA6FF")
    comp.slot("accent", "#9AD2FF")
    hit = 16
    scale, rot = rock(hit)
    size = 214
    c = (W / 2, H / 2 - 4)
    piv = (c[0] - 56, c[1] + 94)
    local = (c[0] - piv[0], c[1] - piv[1])
    thumb = comp.null("thumb", position=piv, scale=scale, rotation=rot)
    body(comp, "like", glyph(THUMB, size, local, name="thumb"), "3d-pop", slot="primary", parent=thumb, depth=20)
    burst(comp, (c[0], c[1] + 8), hit + 3, 156, 200, count=10, slot="accent", width=11, rotation=18)
    return comp


def badge():
    """A round badge pops and a white thumb flicks up inside it; a ring pulses out."""
    comp = Comp("like-thumb-pop--badge", W, H, fps=30, frames=N)
    comp.slot("primary", "#3EA6FF")
    comp.slot("icon", "#FFFFFF")
    comp.slot("accent", "#9AD2FF")
    c = (W / 2, H / 2)
    d = 250
    hit = 18
    comp.layer("ring", [ellipse(anim([(hit, [d, d], DECEL), (hit + 20, [d + 150, d + 150])])),
                        stroke(slot="accent", width=anim([(hit, 12, EASE_OUT), (hit + 20, 2)]),
                               opacity=anim([(hit, 100, EASE_IN), (hit + 20, 0)]))],
               position=c, ip=hit, op=hit + 21)
    burst(comp, c, hit + 2, 150, 196, count=12, slot="accent", width=9, rotation=15, dots=False)
    circle = comp.null("badge", position=c, scale=anim([
        (0, [0, 0], SPRING), (14, [100, 100], EASE_IN_OUT), (hit - 3, [100, 100], EASE_IN), (hit, [92, 92], SNAP_OUT),
        (hit + 8, [110, 110], EASE_IN_OUT), (hit + 16, [98, 98], EASE_IN_OUT), (hit + 24, [100, 100])]))
    size = 144
    piv = (-34, 52)
    comp.layer("thumb", [group(glyph(THUMB, size, (-piv[0] - 6, -piv[1] + 2)) + [fill(slot="icon")], "thumb")],
               parent=circle, position=piv,
               rotation=anim([(4, -70, SNAP_OUT), (hit, -8, EASE_IN), (hit + 3, 0, SPRING), (hit + 14, -12, EASE_IN_OUT),
                              (hit + 22, 3, EASE_IN_OUT), (hit + 30, 0)]),
               scale=anim([(4, [0, 0], SPRING), (16, [100, 100])]))
    comp.layer("shine", [group([path(arc_pts(d / 2 - 22, 200, 250)), stroke("#FFFFFF", width=10, opacity=45)], "arc")],
               parent=circle)
    comp.layer("disc", [ellipse((d, d)), fill(slot="primary")], parent=circle)
    comp.layer("disc-shadow", [ellipse((d, d)), fill("#000000", 22)], parent=circle, position=(0, 9))
    return comp


build_asset("call-to-action", "like-thumb-pop", "Like Thumb Pop",
            "Thumbs-up like reaction that pops in and bounces with a particle burst.",
            ["like", "thumbs up", "youtube", "reaction"], [
    Variant("classic", "Outline Fill", classic(), "intro-hold", thumb_t=0.48,
            description="Outlined thumbs-up that pops in, fills with colour and bounces with a particle burst."),
    Variant("3d-pop", "3D Pop", pop3d(), "intro-hold", thumb_t=0.5,
            description="Chunky layered 3D thumb with a highlight rim and depth that springs in and rocks on its "
                        "wrist."),
    Variant("badge", "Round Badge", badge(), "intro-hold", thumb_t=0.4,
            description="A round badge pops and a white thumb flicks up inside it while a ring pulses out."),
])
