from _common import *
from _cta_actions import body
from drift_lottie import Variant, build_asset

W = H = 440
S = 1.25
N = 60
PIVOT = (220, 110)
CENTER = (220, 228)


def swing():
    return anim([(0, 0, EASE_OUT), (5, 20), (12, -18), (19, 14), (26, -10), (33, 6), (40, -3), (46, 1),
                 (52, 0), (N, 0)])


def bounce():
    return anim([(0, [100, 100], EASE_OUT), (4, [106, 94], EASE_IN_OUT), (12, [100, 100], LINEAR),
                 (N, [100, 100])])


def badge_scale():
    return anim([(0, [0, 0], LINEAR), (4, [0, 0], OVERSHOOT), (16, [100, 100], LINEAR), (48, [100, 100], EASE_IN),
                 (54, [120, 120], EASE_IN), (58, [0, 0], LINEAR), (N, [0, 0])])


def clapper_rot():
    return anim([(0, 0), (3, -7), (9, 9), (16, -8), (23, 6), (30, -4), (37, 3), (43, -1), (50, 0), (N, 0)])


def rays(comp, t, name, slot="primary", width=12):
    items = []
    for side, (a0, a1) in (("r", (-38, -8)), ("l", (188, 218))):
        for i, r in enumerate((160, 188)):
            d = i * 3
            items.append(group([path(arc_pts(r, a0, a1)),
                                trim(start=anim([(t + d, 50, SNAP_OUT), (t + d + 10, 0)]),
                                     end=anim([(t + d, 50, SNAP_OUT), (t + d + 10, 100)])),
                                stroke(slot=slot, width=width,
                                       opacity=anim([(t + d + 22, 100, EASE_IN), (t + d + 34, 0)]))],
                               f"{side}{i}"))
    comp.layer(name, items, ip=t, op=t + 38, position=CENTER,
               scale=anim([(t, [94, 94], SNAP_OUT), (t + 36, [103, 103])]))


def classic():
    """Flat yellow bell swinging with a lagging clapper, sound waves and a badge."""
    comp = Comp("notification-bell-ring", W, H, fps=30, frames=N)
    comp.slot("primary", "#FFC83D")
    comp.slot("accent", "#FF3B30")
    bell = comp.null("bell-pivot", position=PIVOT, rotation=swing(), scale=bounce())
    comp.layer("badge", [group([ellipse((62, 62)), fill(slot="accent")], "dot")],
               parent=bell, position=(74, 42), scale=badge_scale())
    comp.layer("body", [group([polyline([(-50, 80), (-55, 124)]), stroke("#FFFFFF", 13, opacity=40)], "shine"),
                        group(bell_body(S) + [fill(slot="primary")], "bell")],
               parent=bell)
    comp.layer("clapper", [group(bell_clapper(S) + [fill(slot="primary")], "clapper")], parent=bell,
               rotation=clapper_rot())
    rays(comp, 3, "rays")
    return comp


def styled(style):
    """The same swing in 3D-pop or line-art style."""
    comp = Comp(f"notification-bell-ring--{style}", W, H, fps=30, frames=N)
    if style == "outline":
        comp.slot("outline", "#FFFFFF")
    else:
        comp.slot("primary", "#FFC83D")
    comp.slot("accent", "#FF3B30")
    bell = comp.null("bell-pivot", position=PIVOT, rotation=swing(), scale=bounce())
    if style == "outline":
        body(comp, "badge", [ellipse((58, 58))], "outline", parent=bell, position=(74, 42), scale=badge_scale(),
             line=6, line_slot="accent", tint=100, slot="accent")
        body(comp, "bell", bell_body(S), "outline", parent=bell, line=8)
        body(comp, "clapper", bell_clapper(S), "outline", parent=bell, line=8, rotation=clapper_rot())
        rays(comp, 3, "rays", slot="outline", width=9)
    else:
        body(comp, "badge", [ellipse((62, 62))], "3d-pop", slot="accent", parent=bell, position=(74, 42),
             scale=badge_scale(), depth=8, shadow=False)
        body(comp, "bell", bell_body(S), "3d-pop", parent=bell, depth=18)
        body(comp, "clapper", bell_clapper(S), "3d-pop", parent=bell, depth=10, shadow=False,
             rotation=clapper_rot())
        rays(comp, 3, "rays")
    return comp


build_asset("call-to-action", "notification-bell-ring", "Notification Bell Ring",
            "Bell swinging with a lagging clapper, sound waves and a notification badge that pops in. "
            "Seamless loop.",
            ["bell", "notification", "subscribe", "youtube", "alert"], [
    Variant("classic", "Classic", classic(), "loop", thumb_t=0.18,
            description="Flat bell with a shine, a lagging clapper, sound waves and a red badge."),
    Variant("3d-pop", "3D Pop", styled("3d-pop"), "loop", thumb_t=0.18,
            description="Chunky layered 3D bell with a highlight rim and depth, swinging with a 3D badge."),
    Variant("outline", "Line Art", styled("outline"), "loop", thumb_t=0.18,
            description="Line-art bell with clean outer contours, white sound waves and a solid red badge."),
])
