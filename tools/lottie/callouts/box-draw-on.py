"""A rectangle that draws itself around content."""
from _callouts2 import *

W, H = 660, 300
N = 36
C = (W / 2, H / 2)
BW, BH = 580, 220
TEXT = (C[0] - BW / 2 + 34, C[1] - BH / 2 + 30, BW - 68, BH - 60)


def make(style):
    comp = Comp(f"box-draw-on--{style}", W, H, frames=N)
    comp.slot("primary", {"hand": "#FF2D2D", "clean": "#FFFFFF", "select": "#2D8CFF"}[style])
    if style == "hand":
        pts = rrect_pts(C, BW, BH, 10, start=180)
        # start a little into the left side and run past the start, drifting out like a quick pen
        k = len(pts) // 40
        pts = pts[-k:] + pts[:-k]
        pts = wobble(closed_loop(pts, 0.07, 9), 3.5, seed=3, freq=2)
        emit(comp, [hand_line(pts, 1, 22, 16, seed=5, chunks=3, taper=(0.03, 0.08), mins=(0.5, 0.3), wob=0.12)])
    elif style == "clean":
        pts = rrect_pts(C, BW, BH, 22, start=180)
        comp.layer("box", [clean_line(pts + [pts[0]], 10, t0=1, t1=20, mid=True, ease=(0.5, 0.0, 0.2, 1.0))])
        comp.layer("tint", [group([rect((BW, BH), C, 22), fill(slot="primary", opacity=10)], "t")],
                   opacity=anim([(12, 0, EASE_OUT), (24, 100)]))
    else:  # selection box: dashed outline with handles
        comp.slot("background", "#FFFFFF")
        pts = rrect_pts(C, BW, BH, 1, start=-90, n=2)
        corners = [(C[0] + sx * BW / 2, C[1] + sy * BH / 2) for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        mids = [(C[0], C[1] - BH / 2), (C[0] + BW / 2, C[1]), (C[0], C[1] + BH / 2), (C[0] - BW / 2, C[1])]
        for i, p in enumerate(corners + mids):
            t = 14 + i * 1 if i < 4 else 20 + (i - 4)
            s = 22 if i < 4 else 16
            comp.layer(f"handle{i}", [group([rect((s, s)), stroke(slot="primary", width=4),
                                             fill(slot="background")], "h")],
                       position=p, scale=pop(t, 10, 135), ip=t)
        comp.layer("box", [clean_line(pts + [pts[0]], 4, t0=1, t1=18, mid=True, cap="butt",
                                      dashes=[14, 9], ease=(0.5, 0.0, 0.2, 1.0))])
        comp.layer("tint", [group([rect((BW, BH), C), fill(slot="primary", opacity=12)], "t")],
                   opacity=anim([(10, 0, EASE_OUT), (22, 100)]))
    return comp


build_asset(CATEGORY, "box-draw-on", "Box Draw-On",
            "A rectangle that draws itself around content to box it in; put your text inside or frame "
            "part of the video with it.",
            ["box", "rectangle", "frame", "outline", "highlight", "draw-on", "callout"], [
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Quick marker box that overshoots its starting corner."),
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Rounded white box that draws out both ways from the right, with a faint tint."),
    Variant("select", "Selection Box", make("select"), "intro-hold", thumb_t=0.99, text_area=TEXT,
            description="Design-tool style dashed selection box with handles popping on at the corners and edges."),
])
