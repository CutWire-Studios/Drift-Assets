from _common import *

W = H = 440
S = 1.25
N = 60
comp = Comp("notification-bell-ring", W, H, fps=30, frames=N)
comp.slot("primary", "#FFC83D")
comp.slot("accent", "#FF3B30")

PIVOT = (220, 110)
CENTER = (220, 228)

swing = anim([(0, 0, EASE_OUT), (5, 20), (12, -18), (19, 14), (26, -10), (33, 6), (40, -3), (46, 1),
              (52, 0), (N, 0)])
bounce = anim([(0, [100, 100], EASE_OUT), (4, [106, 94], EASE_IN_OUT), (12, [100, 100], LINEAR),
               (N, [100, 100])])

badge_scale = anim([(0, [0, 0], LINEAR), (4, [0, 0], OVERSHOOT), (16, [100, 100], LINEAR), (48, [100, 100], EASE_IN),
                    (54, [120, 120], EASE_IN), (58, [0, 0], LINEAR), (N, [0, 0])])

bell = comp.null("bell-pivot", position=PIVOT, rotation=swing, scale=bounce)
comp.layer("badge", [group([ellipse((62, 62)), fill(slot="accent")], "dot")],
           parent=bell, position=(74, 42), scale=badge_scale)
comp.layer("body", [group([polyline([(-50, 80), (-55, 124)]), stroke("#FFFFFF", 13, opacity=40)], "shine"),
                    group(bell_body(S) + [fill(slot="primary")], "bell")],
           parent=bell)
comp.layer("clapper", [group(bell_clapper(S) + [fill(slot="primary")], "clapper")], parent=bell,
           rotation=anim([(0, 0), (3, -7), (9, 9), (16, -8), (23, 6), (30, -4), (37, 3), (43, -1), (50, 0),
                          (N, 0)]))


def rays(t, name):
    items = []
    for side, (a0, a1) in (("r", (-38, -8)), ("l", (188, 218))):
        for i, r in enumerate((160, 188)):
            d = i * 3
            items.append(group([path(arc_pts(r, a0, a1)),
                                trim(start=anim([(t + d, 50, SNAP_OUT), (t + d + 10, 0)]),
                                     end=anim([(t + d, 50, SNAP_OUT), (t + d + 10, 100)])),
                                stroke(slot="primary", width=12,
                                       opacity=anim([(t + d + 22, 100, EASE_IN), (t + d + 34, 0)]))],
                               f"{side}{i}"))
    comp.layer(name, items, ip=t, op=t + 38, position=CENTER,
               scale=anim([(t, [94, 94], SNAP_OUT), (t + 36, [103, 103])]))


rays(3, "rays")

build(comp, "notification-bell-ring", "Notification Bell Ring",
      "Bell swinging with a lagging clapper, sound waves and a notification badge that pops in. "
      "Seamless loop.",
      ["bell", "notification", "subscribe", "youtube", "alert"], "loop", thumb_t=0.18)
