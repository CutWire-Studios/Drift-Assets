from _common import *

W, H = 640, 300
N = 120
comp = Comp("subscribe-button-click", W, H, fps=30, frames=N)
comp.slot("primary", "#FF0000")
comp.slot("secondary", "#606060")

PW, PH = 480, 124
CENTER = (W / 2, 128)
CLICK = 38
LOCAL_TIP = (130, 14)
TIP = (CENTER[0] + LOCAL_TIP[0], CENTER[1] + LOCAL_TIP[1])
OUTRO = 96

comp.marker("intro", 0, 80)
comp.marker("outro", OUTRO, N - OUTRO)

cursor(comp, [(12, [W + 60, H + 70], DECEL), (32, list(TIP), EASE_IN_OUT), (CLICK + 22, list(TIP), EASE_IN),
              (CLICK + 38, [W + 60, H + 70])], [CLICK], ip=12, op=CLICK + 40, scale=4.2)

button = comp.null("button", position=CENTER, scale=anim([
    (0, [0, 0], SPRING), (14, [100, 100], LINEAR), (CLICK - 4, [100, 100], EASE_IN), (CLICK, [94, 90], SNAP_OUT),
    (CLICK + 3, [94, 90], OVERSHOOT), (CLICK + 16, [100, 100], LINEAR), (OUTRO, [100, 100], EASE_OUT),
    (OUTRO + 6, [106, 106], EASE_IN), (OUTRO + 18, [0, 0], LINEAR)]))

click_wipe(comp, [pill(PW, PH)], LOCAL_TIP, CLICK, "secondary", parent=button)
comp.layer("subscribe", [pill(PW, PH), fill(slot="primary")], parent=button, op=CLICK + 13)
comp.layer("shadow", [pill(PW, PH), fill("#000000", 22)], parent=button, position=(0, 8))

build(comp, "subscribe-button-click", "Subscribe Button Click",
      "Red subscribe pill that pops in, gets clicked by a mouse pointer and turns grey. "
      "Put your own \"Subscribe\" text inside the pill.",
      ["subscribe", "youtube", "button", "click", "cursor"], "intro-hold-outro",
      text_area=(CENTER[0] - PW / 2 + 44, CENTER[1] - PH / 2 + 22, PW - 88, PH - 44), thumb_t=0.26)
