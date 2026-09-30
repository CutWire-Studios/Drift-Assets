"""Magnifying glass frame with an empty lens for the subject or text."""
import math

from _callouts2 import *

W, H = 440, 440
N = 36
C = (182, 182)
R = 122
ANG = math.radians(45)
H0 = (C[0] + (R + 6) * math.cos(ANG), C[1] + (R + 6) * math.sin(ANG))
H1 = (C[0] + (R + 150) * math.cos(ANG), C[1] + (R + 150) * math.sin(ANG))
LENS = (C[0] - 84, C[1] - 84, 168, 168)
SWOOP = [(0, [C[0] + 90, C[1] + 110], (0.2, 0.0, 0.1, 1.0)), (16, list(C))]


def handle_pts(w0=34, w1=44):
    """Tapered rounded handle from the rim outward, as a closed outline."""
    d = (math.cos(ANG), math.sin(ANG))
    n = (-d[1], d[0])
    a, b = H0, H1
    return [(a[0] + n[0] * w0 / 2, a[1] + n[1] * w0 / 2), (b[0] + n[0] * w1 / 2, b[1] + n[1] * w1 / 2),
            (b[0] - n[0] * w1 / 2, b[1] - n[1] * w1 / 2), (a[0] - n[0] * w0 / 2, a[1] - n[1] * w0 / 2)]


def glare(r):
    return arc((0, 0), r, r, 200, 250)


def make(style):
    comp = Comp(f"magnifier-zoom-ring--{style}", W, H, frames=N)
    rig = comp.null("rig", anchor=C, position=anim(SWOOP),
                    scale=anim([(0, [40, 40], SETTLE), (11, [108, 108], SETTLE), (18, [98, 98], SETTLE),
                                (24, [100, 100])]),
                    rotation=anim([(0, -35, SETTLE), (16, 4, SETTLE), (24, 0)]))
    if style == "clean":
        comp.slot("primary", "#FFFFFF")
        comp.slot("secondary", "#FF4D2E")
        comp.layer("glare", [clean_line(glare(R - 30), 10, color="#FFFFFF", slot=None, opacity=70, t0=14, t1=24)],
                   parent=rig, position=C)
        comp.layer("ring", [group([ellipse((2 * R, 2 * R), C), stroke(slot="primary", width=22)], "r"),
                            group([ellipse((2 * R - 22, 2 * R - 22), C), stroke("#000000", 5, opacity=18)], "in")],
                   parent=rig)
        comp.layer("handle", [group([path(bezier(handle_pts(), closed=True)), round_corners(16),
                                     fill(slot="secondary")], "h"),
                              group([P([lerp(H0, H1, 0.12), lerp(H0, H1, 0.24)]), stroke(slot="primary", width=12)],
                                    "collar")], parent=rig)
        comp.layer("glass", [group([ellipse((2 * R, 2 * R), C), fill("#FFFFFF", 10)], "g")], parent=rig)
    elif style == "hand":
        comp.slot("primary", "#FF2D2D")
        ring = wobble(closed_loop(ellipse_pts(C, R, R - 4, start=150), 0.1, 8), 3, seed=2, freq=2)
        hp = handle_pts(28, 34)
        side1 = dense([lerp(hp[0], hp[1], -0.05), hp[1]])
        side2 = dense([hp[2], lerp(hp[2], hp[3], 1.05)])
        end = dense([hp[1], lerp(hp[1], hp[2], 0.5), hp[2]], smooth=True)
        g = offset(glare(R - 30), *C)
        emit(comp, [hand_line(ring, 1, 16, 16, seed=3, chunks=2, taper=(0.04, 0.1), mins=(0.5, 0.25)),
                    hand_line(side1, 15, 19, 13, seed=4, taper=(0.1, 0.2), mins=(0.7, 0.6), wob=0.04),
                    hand_line(end, 19, 21, 13, seed=5, taper=(0.1, 0.2), mins=(0.8, 0.8), wob=0.02),
                    hand_line(side2, 21, 25, 13, seed=6, taper=(0.1, 0.2), mins=(0.7, 0.4), wob=0.04),
                    hand_line(g, 25, 29, 9, seed=7, taper=(0.3, 0.4), mins=(0.5, 0.3), wob=0.04)], parent=rig)
    else:
        comp.slot("primary", "#29E6FF")
        hp = handle_pts(26, 32)
        comp.layer("handle", [neon_line(hp + [hp[0]], 8, t0=10, t1=20, name="h")], parent=rig,
                   opacity=flicker(12))
        comp.layer("ring", [neon_line(ellipse_pts(C, R, R, start=45), 10, t0=0, t1=16, name="r"),
                            neon_line(offset(glare(R - 30), *C), 6, t0=16, t1=24, name="g")], parent=rig,
                   opacity=flicker(2))
    return comp


build_asset(CATEGORY, "magnifier-zoom-ring", "Magnifier Zoom Ring",
            "A magnifying glass that swoops in with an empty lens; line the lens up over the detail you "
            "want to zoom in on, or put text inside it.",
            ["magnifier", "magnifying glass", "zoom", "search", "detail", "lens", "callout"], [
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99, text_area=LENS,
            description="White rim and orange-red handle with a faint glass tint and a glare that sweeps on."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99, text_area=LENS,
            description="Marker-drawn lens and handle, sketched on stroke by stroke."),
    Variant("neon", "Neon", make("neon"), "intro-hold", thumb_t=0.99, text_area=LENS,
            description="Glowing neon outline that flickers on as it swoops in."),
])
