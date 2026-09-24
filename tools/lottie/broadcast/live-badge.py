from _common import *

W, H, F = 340, 140, 45
comp = Comp("live-badge", W, H, fps=30, frames=F)
comp.slot("primary", "#E91916")
comp.slot("icon", "#FFFFFF")

cx, cy = W / 2, H / 2
bw, bh, br = 300, 100, 14
dot = (66, cy)

comp.layer("dot", [
    group([ellipse((32, 32)), fill(slot="icon")], "dot", position=dot,
          scale=anim([(0, [100, 100], EASE_IN_OUT), (22, [78, 78], EASE_IN_OUT), (F, [100, 100])]),
          opacity=anim([(0, 100, EASE_IN_OUT), (22, 55, EASE_IN_OUT), (F, 100)])),
])
comp.layer("ring", [
    group([ellipse(anim([(0, [28, 28], EASE_OUT), (32, [84, 84])])), stroke(slot="icon", width=3.5)],
          "ring", position=dot,
          opacity=anim([(0, 0, EASE_OUT), (3, 80, EASE_OUT), (32, 0, HOLD), (F, 0)])),
])
comp.layer("sheen", [
    group([rect((bw, bh), roundness=br),
           gradient_fill([(0, "#FFFFFF", 0.22), (0.5, "#FFFFFF", 0.0), (1, "#000000", 0.12)],
                         (0, -bh / 2), (0, bh / 2))], "sheen", position=(cx, cy)),
])
comp.layer("badge", [
    group([rect((bw, bh), roundness=br), fill(slot="primary")], "badge", position=(cx, cy)),
])

finish(comp, "broadcast", "live-badge", "Live Badge",
       "Red broadcast LIVE badge with a pulsing white dot; add the word LIVE with the text tool.",
       ["live", "badge", "broadcast", "stream", "news"], "loop",
       text_area=[100, 30, 206, 80], thumb_t=0.2)
