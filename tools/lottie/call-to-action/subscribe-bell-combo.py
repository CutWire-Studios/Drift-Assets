from _common import *

W, H = 960, 270
N = 150
comp = Comp("subscribe-bell-combo", W, H, fps=30, frames=N)
comp.slot("primary", "#FF0000")
comp.slot("secondary", "#606060")
comp.slot("accent", "#3EA6FF")
comp.slot("icon", "#FFFFFF")

Y = 118
THUMB_C = (126, Y)
PILL_C = (484, Y)
BELL_C = (830, Y)
PW, PH = 440, 116
BS = 0.64  # bell scale

C_THUMB, C_PILL, C_BELL = 36, 66, 94
OUTRO = 128
comp.marker("intro", 0, 124)
comp.marker("outro", OUTRO, N - OUTRO)


def outro(t0, keys):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [108, 108], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


# ---------------------------------------------------------------- cursor
tip_thumb = (THUMB_C[0] + 22, THUMB_C[1] + 18)
pill_local = (120, 16)
tip_pill = (PILL_C[0] + pill_local[0], PILL_C[1] + pill_local[1])
tip_bell = (BELL_C[0] + 10, BELL_C[1] + 22)
cursor(comp, [(14, [40, H + 90], DECEL), (32, list(tip_thumb), EASE_IN_OUT), (C_THUMB + 8, list(tip_thumb), EASE_IN_OUT),
              (C_PILL - 6, list(tip_pill), EASE_IN_OUT), (C_PILL + 8, list(tip_pill), EASE_IN_OUT),
              (C_BELL - 6, list(tip_bell), EASE_IN_OUT), (C_BELL + 16, list(tip_bell), EASE_IN),
              (C_BELL + 32, [W + 40, H + 90])],
       [C_THUMB, C_PILL, C_BELL], ip=14, op=C_BELL + 33, scale=3.9)

# ---------------------------------------------------------------- thumb
TS, TSW = 116, 8.5
t_pivot = (THUMB_C[0] - 30, THUMB_C[1] + 50)
t_local = (THUMB_C[0] - t_pivot[0], THUMB_C[1] - t_pivot[1])
thumb = comp.null("thumb", position=t_pivot, scale=anim(outro(OUTRO, [
    (0, [0, 0], SPRING), (13, [100, 100], EASE_IN_OUT), (C_THUMB - 3, [100, 100], EASE_IN),
    (C_THUMB, [86, 86], SNAP_OUT), (C_THUMB + 6, [124, 124], EASE_IN_OUT), (C_THUMB + 13, [95, 95], EASE_IN_OUT),
    (C_THUMB + 20, [101, 101], EASE_IN_OUT), (C_THUMB + 26, [100, 100], EASE_IN_OUT)])),
    rotation=anim([(0, -25, SNAP_OUT), (13, 0, EASE_IN_OUT), (C_THUMB - 3, 0, EASE_IN), (C_THUMB, 8, SNAP_OUT),
                   (C_THUMB + 6, -16, EASE_IN_OUT), (C_THUMB + 14, 5, EASE_IN_OUT), (C_THUMB + 21, -2, EASE_IN_OUT),
                   (C_THUMB + 28, 0)]))
comp.layer("thumb-matte", [group([ellipse(anim([(C_THUMB, [0, 0], EASE_OUT), (C_THUMB + 9, [300, 300])])), fill()],
                                 "wipe")], parent=thumb)
comp.layer("thumb-fill", [group(glyph(THUMB, TS, t_local) + [fill(slot="accent"), stroke(slot="accent", width=TSW)],
                                "thumb")], parent=thumb, matte="alpha")
comp.layer("thumb-outline", [group(glyph(THUMB, TS, t_local) + [stroke(slot="icon", width=TSW)], "thumb")],
           parent=thumb, op=C_THUMB + 10)
burst(comp, THUMB_C, C_THUMB + 3, 82, 104, count=8, slot="accent", width=7, rotation=22.5)

# ---------------------------------------------------------------- pill
button = comp.null("button", position=PILL_C, scale=anim(outro(OUTRO + 3, [
    (0, [0, 0], HOLD), (5, [0, 0], SPRING), (19, [100, 100], LINEAR), (C_PILL - 4, [100, 100], EASE_IN),
    (C_PILL, [95, 90], SNAP_OUT), (C_PILL + 3, [95, 90], OVERSHOOT), (C_PILL + 16, [100, 100], LINEAR)])))
click_wipe(comp, [pill(PW, PH)], pill_local, C_PILL, "secondary", parent=button)
comp.layer("subscribe", [pill(PW, PH), fill(slot="primary")], parent=button, op=C_PILL + 13)
comp.layer("shadow", [pill(PW, PH), fill("#000000", 22)], parent=button, position=(0, 7))

# ---------------------------------------------------------------- bell
R = C_BELL
bell_pop = comp.null("bell-pop", position=BELL_C, scale=anim(outro(OUTRO + 6, [
    (0, [0, 0], HOLD), (10, [0, 0], SPRING), (23, [100, 100], LINEAR), (R - 3, [100, 100], EASE_IN),
    (R, [88, 88], SNAP_OUT), (R + 8, [108, 108], EASE_IN_OUT), (R + 18, [100, 100], LINEAR)])))
bell = comp.null("bell", parent=bell_pop, position=(0, -88 * BS), rotation=anim([
    (R - 1, 0, EASE_OUT), (R + 4, 22), (R + 10, -19), (R + 16, 15), (R + 22, -11), (R + 28, 7), (R + 34, -4),
    (R + 40, 1.5), (R + 46, 0)]))
body = BELL_BODY
bell_items = svg_shapes(body, BS, name="body")
comp.layer("bell-fill", [group(bell_items + [fill(slot="icon")], "fill")], parent=bell, ip=R + 1,
           opacity=anim([(R + 1, 0, EASE_OUT), (R + 4, 100)]))
comp.layer("bell-outline", [
    group([ellipse((20 * BS, 20 * BS), (0, 3 * BS)), fill(slot="icon")], "knob"),
    group(bell_items + [stroke(slot="icon", width=8.5)], "outline")], parent=bell)
comp.layer("clapper", [group([path(arc_pts(15 * BS, 0, 180, (0, 156 * BS))),
                              stroke(slot="icon", width=8.5)], "clapper")], parent=bell,
           rotation=anim([(R - 1, 0), (R + 2, -8), (R + 8, 10), (R + 14, -8), (R + 20, 6), (R + 26, -4), (R + 32, 3),
                          (R + 38, -1), (R + 44, 0)]))
rays = []
for side, (a0, a1) in (("r", (-40, -8)), ("l", (188, 220))):
    for i, r in enumerate((82, 100)):
        d = i * 3
        rays.append(group([path(arc_pts(r, a0, a1)),
                           trim(start=anim([(R + d, 50, SNAP_OUT), (R + 10 + d, 0)]),
                                end=anim([(R + d, 50, SNAP_OUT), (R + 10 + d, 100)])),
                           stroke(slot="icon", width=7, opacity=anim([(R + 20 + d, 100, EASE_IN), (R + 32 + d, 0)]))],
                          f"{side}{i}"))
comp.layer("rays", rays, ip=R, op=R + 36, position=(BELL_C[0], BELL_C[1] + 6),
           scale=anim([(R, [92, 92], SNAP_OUT), (R + 34, [104, 104])]))

build(comp, "subscribe-bell-combo", "Subscribe Bell Combo",
      "Like, subscribe and bell in a row: a pointer taps the thumb (fills blue), the subscribe pill (turns grey) "
      "and the bell (rings). Put your own \"Subscribe\" text inside the pill.",
      ["subscribe", "like", "bell", "youtube", "cursor", "click"], "intro-hold-outro",
      text_area=(PILL_C[0] - PW / 2 + 40, PILL_C[1] - PH / 2 + 20, PW - 80, PH - 40), thumb_t=0.2)
