from _common import *

W, H = 680, 300
N = 120
comp = Comp("follow-button-twitch", W, H, fps=30, frames=N)
comp.slot("primary", "#9146FF")
comp.slot("icon", "#FFFFFF")

PW, PH = 540, 132
CENTER = (W / 2, 130)
LOGO_X = -PW / 2 + 76
HEART_X = PW / 2 - 74
CLICK = 42
OUTRO = 96
comp.marker("intro", 0, 80)
comp.marker("outro", OUTRO, N - OUTRO)

HEART = ("M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09"
         "C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z")

tip = (CENTER[0] + HEART_X + 8, CENTER[1] + 14)
cursor(comp, [(16, [W + 60, H + 80], DECEL), (36, list(tip), EASE_IN_OUT), (CLICK + 20, list(tip), EASE_IN),
              (CLICK + 36, [W + 60, H + 80])], [CLICK], ip=16, op=CLICK + 38, scale=4.0)


def out(keys, t0):
    return keys + [(t0, [100, 100], EASE_OUT), (t0 + 5, [106, 106], EASE_IN), (t0 + 15, [0, 0], LINEAR)]


button = comp.null("button", position=CENTER, scale=anim(out([
    (0, [0, 0], SPRING), (14, [100, 100], LINEAR), (CLICK - 3, [100, 100], EASE_IN), (CLICK, [96, 92], SNAP_OUT),
    (CLICK + 3, [96, 92], OVERSHOOT), (CLICK + 15, [100, 100], LINEAR)], OUTRO + 6)))

# ---------------------------------------------------------------- heart
HS = 64
heart = comp.null("heart", parent=button, position=(HEART_X, 0), scale=anim(out([
    (0, [0, 0], HOLD), (10, [0, 0], SPRING), (24, [100, 100], LINEAR), (CLICK - 2, [100, 100], EASE_IN),
    (CLICK + 1, [78, 78], SNAP_OUT), (CLICK + 8, [124, 124], EASE_IN_OUT), (CLICK + 15, [94, 94], EASE_IN_OUT),
    (CLICK + 22, [100, 100], LINEAR)], OUTRO)))
comp.layer("heart-fill", [group(glyph(HEART, HS) + [fill(slot="icon")], "heart", anchor=(0, 4), position=(0, 4),
                                scale=anim([(CLICK + 1, [0, 0], SNAP_OUT), (CLICK + 9, [100, 100])]))],
           parent=heart, ip=CLICK + 1)
comp.layer("heart-outline", [group(glyph(HEART, HS) + [stroke(slot="icon", width=6)], "heart")], parent=heart)
burst(comp, (HEART_X, 2), CLICK + 3, 50, 70, count=8, slot="icon", width=6, parent=button)

# ---------------------------------------------------------------- Twitch glitch, eyes blink
LS = 70
s = LS / 24
parts = glyph(TWITCH, LS)
eye_y = (7.286 - 12) * s
logo = comp.null("logo", parent=button, position=(LOGO_X, 0), scale=anim(out([
    (0, [0, 0], HOLD), (5, [0, 0], SPRING), (19, [100, 100], LINEAR)], OUTRO + 3)),
    rotation=anim([(5, -20, SNAP_OUT), (19, 0)]))
blink = anim([(0, [100, 100], HOLD), (26, [100, 100], EASE_IN), (29, [100, 10], EASE_OUT), (33, [100, 100], HOLD),
              (CLICK + 2, [100, 100], EASE_IN), (CLICK + 5, [100, 10], EASE_OUT), (CLICK + 9, [100, 100])])
comp.layer("glitch", [
    group(parts[:2] + [fill("#FFFFFF")], "eyes", anchor=(0, eye_y), position=(0, eye_y), scale=blink),
    group(parts[2:] + [fill("#FFFFFF")], "body"),
], parent=logo)

comp.layer("pill", [pill(PW, PH), fill(slot="primary")], parent=button)
comp.layer("shadow", [pill(PW, PH), fill("#000000", 22)], parent=button, position=(0, 8))

build(comp, "follow-button-twitch", "Follow Button Twitch",
      "Purple follow pill with a blinking Twitch glitch logo; a pointer clicks the heart, which fills with a burst. "
      "Put your own \"Follow\" text inside the pill.",
      ["follow", "twitch", "button", "click", "cursor", "heart", "social", "stream"], "intro-hold-outro",
      text_area=(CENTER[0] + LOGO_X + 54, CENTER[1] - PH / 2 + 24, HEART_X - LOGO_X - 104, PH - 48), thumb_t=0.5)
