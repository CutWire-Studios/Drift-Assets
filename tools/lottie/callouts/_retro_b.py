"""Extra designs for the retrofitted first-batch callouts (clean / hand / neon looks).

Built on `_callouts2` so they match the second-batch callouts.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _callouts2 as c2  # noqa: E402
from _callouts2 import (DECEL, DRAW, INK, SETTLE, SPRING, P, clean_line, closed_loop, dense, draw,  # noqa: E402,F401
                        ellipse_pts, emit, flicker, hand_line, hand_static, neon_line, pop, wobble)
from lottie_kit import (EASE_IN, EASE_OUT, LINEAR, anim, ellipse, fill, group, stroke, trim)  # noqa: E402,F401


# ---------------------------------------------------------------- stamps (check / cross)

def badge_stamp(comp, strokes, tilt=0, t_mark=8):
    """Clean badge: a flat disc pops in with a twist, a white symbol draws on stroke by stroke, a
    thin inner ring traces round and a ripple plus short rays flick out. strokes: point lists
    centred on (0, 0) sized for a ~300 px disc. Slots: primary (disc), icon (symbol)."""
    comp.slot("icon", "#FFFFFF")
    c = (comp.w / 2, comp.h / 2)
    R = 150
    holder = comp.null("badge", position=c, scale=pop(0, 13, 114),
                       rotation=anim([(0, tilt - 30, SETTLE), (10, tilt + 4, SETTLE), (16, tilt)]))
    per = 7
    for k, pts in enumerate(strokes):
        t0 = t_mark + k * (per - 1)
        comp.layer(f"mark{k}", [clean_line(pts, 36, "icon", t0=t0, t1=t0 + per, ease=(0.5, 0.0, 0.25, 1.0))],
                   parent=holder, ip=t0)
    comp.layer("inner-ring", [group([ellipse((2 * R - 36, 2 * R - 36)),
                                     trim(0, draw(4, 20, (0.4, 0.0, 0.2, 1.0))),
                                     stroke(slot="icon", width=5, opacity=45)], "ring", rotation=-90)],
               parent=holder, ip=4)
    comp.layer("disc", [group([ellipse((2 * R, 2 * R)), fill(slot="primary")], "disc")], parent=holder)
    comp.layer("disc-shadow", [group([ellipse((2 * R, 2 * R)), fill("#000000", 22)], "s")], parent=holder,
               position=(0, 10))
    # ripple and rays once the mark lands
    hit = t_mark + len(strokes) * (per - 1) + 1
    comp.layer("ripple", [group([ellipse((2 * R, 2 * R)), stroke(slot="primary", width=anim([(hit, 10, EASE_OUT),
                                                                                             (hit + 14, 1)]))], "r")],
               position=c, ip=hit, op=hit + 15, scale=anim([(hit, [100, 100], DECEL), (hit + 14, [138, 138])]),
               opacity=anim([(hit, 80, EASE_IN), (hit + 14, 0)]))
    rays = []
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        p0 = (math.cos(a) * (R + 22), math.sin(a) * (R + 22))
        p1 = (math.cos(a) * (R + 52), math.sin(a) * (R + 52))
        rays.append(group([P([p0, p1]), trim(anim([(hit + 3, 0, EASE_OUT), (hit + 11, 100)]),
                                             anim([(hit, 0, EASE_OUT), (hit + 7, 100)])),
                           stroke(slot="primary", width=9)], f"ray{i}"))
    comp.layer("rays", rays, position=c, ip=hit, op=hit + 12)


def marker_stamp(comp, strokes, seed=3, start=-120, tilt=-8, taper=(0.1, 0.35), mins=(0.6, 0.3)):
    """Hand-drawn mark: a marker circle scribbled round, then the symbol flicked on with a thick
    marker. strokes: point lists (tail -> tip) around (0, 0) in canvas-centred coords."""
    c = (comp.w / 2, comp.h / 2)
    ring = ellipse_pts((0, 0), 168, 158, start=start)
    ring = c2.rotate(ring, tilt)
    ring = wobble(closed_loop(ring, 0.1, 12), 3.2, seed=seed, freq=2)
    ring = [(x + c[0], y + c[1]) for x, y in ring]
    brushes = [hand_line(ring, 1, 17, 15, seed=seed, chunks=3, taper=(0.04, 0.12), mins=(0.5, 0.25), wob=0.12,
                         name="ring")]
    t = 17
    for k, pts in enumerate(strokes):
        pts = dense([(x + c[0], y + c[1]) for x, y in pts], smooth=True)
        brushes.append(hand_line(pts, t, t + 6, 30, seed=seed + 5 + k, taper=taper, mins=mins, wob=0.08,
                                 name=f"mark{k}"))
        t += 6
    emit(comp, brushes)
    return t
