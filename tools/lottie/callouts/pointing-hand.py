"""Cartoon hand pointing right that pokes forward twice per loop."""
import math

from _callouts2 import *

W, H = 440, 250
N = 60
ORIGIN = (180, 128)
TIP = (162, -42)  # fingertip in hand space


def parts():
    """Closed outlines, bottom to top: cuff, palm, three curled fingers, thumb, index finger."""
    out = [("cuff", rrect_pts((-132, 8), 46, 120, 16)),
           ("palm", rrect_pts((-46, 10), 150, 128, 46))]
    for i, (cy, w) in enumerate([(-6, 88), (26, 82), (58, 70)]):
        out.append((f"finger{i}", rrect_pts((-24 + w / 2, cy), w, 36, 18, start=0)))
    out.append(("thumb", rotate(rrect_pts((-8, 22), 112, 38, 19), -24, (-60, 22))))
    out.append(("index", rrect_pts((64, -42), 200, 42, 21, start=0)))
    return out


def poke_keys():
    x, y = ORIGIN
    pos, rot = [], []
    for c in (0, 30):
        pos += [(c, [x, y], EASE_IN_OUT), (c + 8, [x - 18, y + 3], (0.6, 0.0, 0.9, 0.4)),
                (c + 12, [x + 26, y - 2], SETTLE), (c + 22, [x, y], EASE_IN_OUT)]
        rot += [(c, 0, EASE_IN_OUT), (c + 8, 5, (0.6, 0.0, 0.9, 0.4)), (c + 12, -4, SETTLE), (c + 22, 0, HOLD)]
    pos.append((N, [x, y]))
    rot.append((N, 0))
    return anim(pos), anim(rot)


def poke_burst(slot, color):
    """Three short lines flicking out from the fingertip on each poke."""
    items = []
    tx, ty = ORIGIN[0] + TIP[0] + 26, ORIGIN[1] + TIP[1] - 2
    for c in (0, 30):
        t = c + 11
        for k, ang in enumerate((-40, 0, 40)):
            a = math.radians(ang)
            p0 = (tx + 22 * math.cos(a), ty + 22 * math.sin(a))
            p1 = (tx + 50 * math.cos(a), ty + 50 * math.sin(a))
            items.append(group([P([p0, p1]), trim(anim([(t + 2, 0, SETTLE), (t + 9, 100)]),
                                                 anim([(t, 0, SETTLE), (t + 5, 100)])),
                                stroke(color, 8, slot=slot)], f"ray{c}{k}"))
    return items


def make(style):
    comp = Comp(f"pointing-hand--{style}", W, H, frames=N)
    pos, rot = poke_keys()
    if style == "glove":
        comp.slot("primary", "#FFFFFF")
        comp.slot("outline", INK)
        comp.slot("accent", "#FFD21F")
        comp.layer("burst", poke_burst("accent", "#FFD21F"))
        holder = comp.null("hand", position=pos, rotation=rot, anchor=(-120, 10))
        stitches = [group([P([(-86 + k * 24, -30), (-80 + k * 24, 0)]), stroke(INK, 5, slot="outline")], f"s{k}")
                    for k in range(3)]
        cuff_lines = [group([P([(-148 + k * 12, -40), (-148 + k * 12, 56)]), stroke(INK, 4, slot="outline",
                                                                                    opacity=60)], f"c{k}")
                      for k in range(2)]
        items = []
        for name, pts in parts()[::-1]:
            if name == "palm":
                items += stitches
            if name == "cuff":
                items += cuff_lines
            items.append(outlined(pts, "clean", "primary", "outline", 7, name=name))
        comp.layer("hand", items, parent=holder, position=(-120, 10))
    elif style == "bold":
        comp.slot("primary", "#FFC83D")
        comp.slot("outline", INK)
        comp.slot("accent", "#FF2D2D")
        comp.layer("burst", poke_burst("accent", "#FF2D2D"))
        holder = comp.null("hand", position=pos, rotation=rot, anchor=(-120, 10))
        mains, shadows = [], []
        for name, pts in parts():
            m, s = comic([P(pts, True)], "primary", width=10, shadow=(8, 10), name=name)
            mains.append(m)
            shadows.append(s)
        shine = group([P([(-10, -52), (110, -52)]), stroke("#FFFFFF", 7, opacity=60)], "shine")
        comp.layer("hand", [shine] + mains[::-1], parent=holder, position=(-120, 10))
        comp.layer("hand-shadow", shadows, parent=holder, position=(-120, 10))
    else:  # hand-drawn doodle with a boiling line
        comp.slot("background", "#FFFFFF")
        comp.slot("outline", INK)
        holder = comp.null("hand", position=pos, rotation=rot, anchor=(-120, 10))
        items = [outlined(pts, "hand", "background", "outline", 7, seed=i + 1, frames=N, name=name)
                 for i, (name, pts) in enumerate(parts())]
        comp.layer("hand", items[::-1], parent=holder, position=(-120, 10))
    return comp


build_asset(CATEGORY, "pointing-hand", "Pointing Hand",
            "Cartoon hand pointing to the right that keeps poking forward; place the fingertip next to "
            "whatever you want to point out (flip it horizontally to point left).",
            ["hand", "pointing", "finger", "point", "look-here", "cartoon", "loop"], [
    Variant("glove", "Cartoon Glove", make("glove"), "loop", thumb_t=0.4, bg="e8e8ee",
            description="White cartoon glove with stitching; little yellow lines flick out on each poke."),
    Variant("bold", "Comic Bold", make("bold"), "loop", thumb_t=0.4, bg="e8e8ee",
            description="Emoji-yellow hand with a thick ink outline and hard shadow."),
    Variant("doodle", "Doodle", make("doodle"), "loop", thumb_t=0.4, bg="e8e8ee",
            description="Marker doodle hand whose outline boils like frame-by-frame animation."),
])
