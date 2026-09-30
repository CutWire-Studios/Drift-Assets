"""Four corner brackets that snap in around a subject."""
from _callouts2 import *

W, H = 580, 400
N = 36
C = (W / 2, H / 2)
BW, BH = 480, 300  # bracket frame
ARM = 78
CORNERS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]


def corner_pts(sx, sy, arm=ARM, r=12):
    """L relative to its corner point: arm along x, corner, arm along y."""
    return dense(fillet([(-sx * arm, 0), (0, 0), (0, -sy * arm)], r))


def make(style):
    comp = Comp(f"focus-corner-brackets--{style}", W, H, frames=N)
    comp.slot("primary", {"clean": "#FFFFFF", "hand": "#FFD21F", "neon": "#39FF88"}[style])
    for i, (sx, sy) in enumerate(CORNERS):
        cx, cy = C[0] + sx * BW / 2, C[1] + sy * BH / 2
        d = i * 2
        if style == "clean":
            comp.layer(f"corner{i}", [clean_line(corner_pts(sx, sy), 14)],
                       position=anim([(d, [cx + sx * 70, cy + sy * 70], SPRING), (d + 14, [cx, cy])]),
                       opacity=anim([(d, 0, EASE_OUT), (d + 4, 100)]),
                       scale=anim([(d, [60, 60], SPRING), (d + 14, [100, 100])]))
        elif style == "neon":
            comp.layer(f"corner{i}", [neon_line(corner_pts(sx, sy), 9)],
                       position=anim([(d, [cx + sx * 36, cy + sy * 36], SETTLE), (d + 10, [cx, cy])]),
                       opacity=flicker(d + 1))
        else:
            pts = wobble(corner_pts(sx, sy, ARM + 6, 6), 1.5, seed=i)
            if i % 2:
                pts = pts[::-1]
            emit(comp, [hand_line(pts, i * 5 + 1, i * 5 + 8, 17, seed=i + 2, taper=(0.1, 0.25),
                                  mins=(0.6, 0.35), wob=0.08, name=f"corner{i}")],
                 position=(cx, cy))
    return comp


build_asset(CATEGORY, "focus-corner-brackets", "Focus Corner Brackets",
            "Four corner brackets that snap in to frame a subject, like a camera focusing; stretch it "
            "to fit what you want to highlight.",
            ["focus", "brackets", "frame", "corners", "highlight", "camera", "callout"], [
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99,
            description="White round-capped corners that spring in from outside the frame."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Marker corners flicked on one after another."),
    Variant("neon", "Neon", make("neon"), "intro-hold", thumb_t=0.99,
            description="Glowing neon corners that slide in and flicker on."),
])
