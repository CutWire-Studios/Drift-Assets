"""Target brackets that swing in and lock onto a point."""
import math

from _callouts2 import *

W = H = 420
N = 45
C = (W / 2, H / 2)
LOCK = 16  # frame the brackets land


def bracket(sx, sy, arm=40, r=6):
    return fillet([(-sx * arm, 0), (0, 0), (0, -sy * arm)], r)


def blink(t):
    return anim([(t, 100, HOLD), (t + 2, 30, HOLD), (t + 4, 100, HOLD), (t + 6, 30, HOLD), (t + 8, 100)])


def make(style):
    comp = Comp(f"crosshair-target-lock--{style}", W, H, frames=N)
    comp.slot("primary", {"clean": "#FF2D2D", "hud": "#39FF88", "hand": "#FF2D2D"}[style])
    if style in ("clean", "hud"):
        line = clean_line if style == "clean" else neon_line
        wd = 9 if style == "clean" else 6
        rig = comp.null("rig", position=C, rotation=anim([(0, -90, (0.3, 0.0, 0.2, 1.0)), (LOCK, 0)]),
                        scale=anim([(0, [230, 230], (0.3, 0.0, 0.2, 1.0)), (LOCK, [92, 92], SETTLE),
                                    (LOCK + 5, [100, 100])]))
        for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]):
            comp.layer(f"bracket{i}", [line(bracket(sx, sy), wd)], parent=rig, position=(sx * 96, sy * 96),
                       opacity=blink(LOCK + 2) if style == "clean" else flicker(0))
        # centre dot + ticks
        comp.layer("dot", [group([ellipse((18, 18)), fill(slot="primary")], "d")], position=C,
                   scale=pop(LOCK, 10, 160), ip=LOCK)
        ticks = []
        for k in range(4):
            a = math.radians(k * 90)
            p0 = (math.cos(a) * 30, math.sin(a) * 30)
            p1 = (math.cos(a) * 62, math.sin(a) * 62)
            ticks.append(line([p1, p0], wd * 0.8, t0=LOCK - 2, t1=LOCK + 6, name=f"t{k}"))
        comp.layer("ticks", ticks, position=C, ip=LOCK - 2)
        ring_t = 4
        if style == "clean":
            comp.layer("ring", [group([ellipse((170, 170)), trim(0, draw(ring_t, LOCK + 2)),
                                       stroke(slot="primary", width=4, opacity=80)], "r")],
                       position=C, rotation=anim([(ring_t, -200, SETTLE), (LOCK + 2, -90)]))
        else:
            segs = []
            for k in range(4):
                pts = arc((0, 0), 150, 150, k * 90 - 30, k * 90 + 30)
                segs.append(neon_line(pts, 5, t0=ring_t, t1=LOCK, name=f"s{k}"))
            comp.layer("ring", segs, position=C, opacity=flicker(ring_t),
                       rotation=anim([(ring_t, -120, SETTLE), (LOCK + 4, 0, EASE_IN_OUT), (N, 20)]))
        # lock flash
        comp.layer("flash", [group([ellipse((190, 190)), stroke(slot="primary", width=anim(
            [(LOCK, 8, EASE_OUT), (LOCK + 12, 1)]))], "f")], position=C, ip=LOCK, op=LOCK + 13,
            scale=anim([(LOCK, [60, 60], DECEL), (LOCK + 12, [150, 150])]),
            opacity=anim([(LOCK, 90, EASE_IN), (LOCK + 12, 0)]))
    else:
        circle = wobble(closed_loop(ellipse_pts(C, 112, 106, start=-150), 0.12, 8), 3, seed=2, freq=2)
        h = dense([(C[0] - 168, C[1] + 6), (C[0] + 164, C[1] - 4)])
        v = dense([(C[0] - 4, C[1] - 166), (C[0] + 6, C[1] + 164)])
        dot = closed_loop(ellipse_pts(C, 16, 15, start=-60), 0.15, 3)
        emit(comp, [hand_line(circle, 1, 16, 16, seed=3, chunks=2, taper=(0.04, 0.1), mins=(0.5, 0.3)),
                    hand_line(h, 15, 21, 12, seed=4, taper=(0.1, 0.2), mins=(0.6, 0.3), wob=0.08),
                    hand_line(v, 20, 26, 12, seed=5, taper=(0.1, 0.2), mins=(0.6, 0.3), wob=0.08),
                    hand_line(dot, 27, 33, 11, seed=6, chunks=2, taper=(0.1, 0.2), mins=(0.7, 0.5), wob=0.04)])
    return comp


build_asset(CATEGORY, "crosshair-target-lock", "Crosshair Target Lock",
            "Target brackets that swing in and lock onto a point, with a flash on lock; centre it on the "
            "thing you are targeting.",
            ["crosshair", "target", "lock-on", "aim", "focus", "hud", "gaming"], [
    Variant("clean", "Clean", make("clean"), "intro-hold", thumb_t=0.99,
            description="Red brackets spin down onto a ring and blink twice when they lock."),
    Variant("hud", "Neon HUD", make("hud"), "intro-hold", thumb_t=0.99,
            description="Glowing sci-fi HUD: segmented ring keeps turning slowly after the lock."),
    Variant("hand", "Hand-Drawn", make("hand"), "intro-hold", thumb_t=0.99,
            description="Marker circle and crosshair lines scribbled on, with a little ring on the spot."),
])
