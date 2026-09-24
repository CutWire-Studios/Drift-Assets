"""Shared helpers for the call-to-action Lottie assets."""

import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "lottie"))

from lottie_kit import *  # noqa: E402,F401,F403
from lottie_kit import Comp, anim, bezier, ellipse, fill, group, path, polyline, rect, stroke, trim, \
    EASE_IN, EASE_OUT, EASE_IN_OUT, SNAP_OUT, OVERSHOOT, LINEAR  # noqa: E402

RENDER = os.path.join(REPO, "tools", "skottie-render", "build", "skottie-render")
CATEGORY = "call-to-action"

# Stronger back-out than the kit's OVERSHOOT, for springy pops.
SPRING = (0.3, 1.9, 0.55, 1.0)
DECEL = (0.2, 0.0, 0.1, 1.0)

# ---------------------------------------------------------------- brand glyphs (Simple Icons, 24x24)

YOUTUBE = ("M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505"
           "A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136"
           "c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12"
           "s0-3.93-.502-5.814z")
TIKTOK = ("M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03"
          "c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94"
          "-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1"
          "-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44"
          "-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87"
          " 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z")
X_LOGO = ("M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594"
          "l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z")
TWITCH = ("M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24"
          "l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z")
# Material "thumb_up" (Apache 2.0), 24x24
THUMB = ("M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59"
         "C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z")


def glyph(d, size, center=(0, 0), box=24.0, name="glyph"):
    """svg_shapes() of a path in a `box`-sized viewBox, scaled to `size` px and centred on `center`."""
    from lottie_kit import svg_shapes
    s = size / box
    return svg_shapes(d, s, (center[0] - box * s / 2, center[1] - box * s / 2), name)


# ---------------------------------------------------------------- common parts

def pill(w, h, name="pill"):
    return rect((w, h), roundness=h / 2, name=name)


# Arrow pointer, tip at (0, 0).
_CURSOR = [(0, 0), (0, 17), (4, 13.3), (6.9, 19.8), (9.4, 18.7), (6.6, 12.4), (11.9, 12.4)]


def cursor_shapes(scale=3.6):
    pts = [(x * scale, y * scale) for x, y in _CURSOR]
    return [
        group([polyline(pts, closed=True), fill("#FFFFFF"),
               stroke("#111111", width=scale * 1.25, join="round")], "arrow"),
        group([polyline(pts, closed=True), fill("#000000", 28)], "shadow", position=(3, 6)),
    ]


def cursor(comp, keys, clicks, ip=0, op=None, scale=3.6):
    """Mouse pointer layer. keys: [(frame, (x, y), easing)] for the tip; clicks: frames of presses."""
    sk = [(0, [100, 100], LINEAR)]
    for c in clicks:
        sk += [(c - 3, [100, 100], EASE_IN), (c, [82, 82], EASE_OUT), (c + 7, [100, 100], LINEAR)]
    for c in clicks:
        ripple(comp, _pos_at(keys, c), c)
    return comp.layer("cursor", cursor_shapes(scale), ip=ip, op=op, position=anim(keys),
                      scale=anim(sk) if clicks else (100, 100))


def _pos_at(keys, f):
    last = keys[0][1]
    for k in keys:
        if k[0] <= f:
            last = k[1]
    return last


def ripple(comp, pos, frame, size=90, color="#FFFFFF"):
    comp.layer("ripple", [ellipse(anim([(frame, [8, 8], DECEL), (frame + 14, [size, size])])),
                          stroke(color, width=anim([(frame, 7, EASE_OUT), (frame + 14, 1)]),
                                 opacity=anim([(frame, 90, EASE_IN), (frame + 14, 0)]))],
               ip=frame, op=frame + 15, position=pos)


def burst(comp, center, frame, r0, r1, count=8, color=None, slot=None, width=8, rotation=0, ip_pad=0,
          parent=None, dots=True, name="burst"):
    """Radial line burst (+ optional dots between lines) starting at `frame`."""
    items = []
    for i in range(count):
        a = math.radians(rotation + i * 360 / count - 90)
        p0 = (math.cos(a) * r0, math.sin(a) * r0)
        p1 = (math.cos(a) * r1, math.sin(a) * r1)
        items.append(group([polyline([p0, p1]),
                            trim(start=anim([(frame + 2, 0, EASE_OUT), (frame + 13, 100)]),
                                 end=anim([(frame, 0, SNAP_OUT), (frame + 9, 100)])),
                            stroke(color or "#FFFFFF", width=width, slot=slot)], f"ray{i}"))
        if dots:
            b = a + math.pi / count
            d0 = (math.cos(b) * r0 * 0.95, math.sin(b) * r0 * 0.95)
            d1 = (math.cos(b) * r1 * 0.8, math.sin(b) * r1 * 0.8)
            items.append(group([ellipse((width * 1.1, width * 1.1)), fill(color or "#FFFFFF", slot=slot)],
                               f"dot{i}",
                               position=anim([(frame, list(d0), SNAP_OUT), (frame + 14, list(d1))]),
                               scale=anim([(frame, [0, 0], EASE_OUT), (frame + 4, [100, 100], EASE_IN),
                                           (frame + 15, [0, 0])])))
    return comp.layer(name, items, ip=frame, op=frame + 16, position=center, parent=parent)


def click_wipe(comp, shapes, point, frame, slot, parent=None, dur=12, reach=800, name="wipe"):
    """Colour `slot` spreading from `point` across `shapes` (which act as an alpha matte)."""
    comp.layer(name + "-matte", [group(list(shapes) + [fill()], "matte")], parent=parent, ip=frame)
    comp.layer(name, [group([ellipse(anim([(frame, [0, 0], DECEL), (frame + dur, [reach, reach])])),
                             fill(slot=slot)], "spread", position=point)],
               parent=parent, ip=frame, matte="alpha")


def pop_scale(t0, dur=14, to=100, spring=SPRING):
    return [(t0, [0, 0], spring), (t0 + dur, [to, to], LINEAR)]


# ---------------------------------------------------------------- output

def _hex(c):
    return "#" + "".join(f"{round(v * 255):02X}" for v in c[:3])


def build(comp, asset_id, name, description, tags, playback, text_area=None, thumb_t=0.5, bg=None):
    out = os.path.join(REPO, "lottie", CATEGORY, asset_id)
    os.makedirs(out, exist_ok=True)
    jpath = os.path.join(out, f"{asset_id}.json")
    comp.save(jpath)
    cmd = [RENDER, jpath, os.path.join(out, "thumbnail.png"), "--size", "512", "--t", str(thumb_t), "--strict"]
    if bg:
        cmd += ["--bg", bg]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    meta = {
        "schema": 1, "id": asset_id, "name": name, "type": "lottie", "category": CATEGORY,
        "file": f"{asset_id}.json", "thumbnail": "thumbnail.png", "license": "CC-BY-NC-SA-4.0",
        "description": description, "tags": tags, "width": comp.w, "height": comp.h, "fps": comp.fps,
        "duration": round(comp.frames / comp.fps, 3), "playback": playback,
        "slots": {k: _hex(v["p"]["k"]) for k, v in comp.slots.items()},
        "textArea": [round(v) for v in text_area] if text_area else None,
    }
    with open(os.path.join(out, "asset.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    print(jpath)


# Bell, pivot (top of knob) at (0, 0); body ~164 wide, ~150 tall at s=1.
BELL_BODY = ("M0 10 C40 10 62 40 62 80 L62 106 C62 116 68 124 78 130 C87 136 85 146 76 146 "
             "L-76 146 C-85 146 -87 136 -78 130 C-68 124 -62 116 -62 106 L-62 80 C-62 40 -40 10 0 10 Z")
BELL_CLAPPER = "M-19 156 A19 19 0 0 0 19 156 Z"


def bell_body(s=1.0):
    from lottie_kit import svg_shapes
    return svg_shapes(BELL_BODY, s, name="body") + [ellipse((26 * s, 26 * s), (0, 10 * s), name="knob")]


def bell_clapper(s=1.0):
    from lottie_kit import svg_shapes
    return svg_shapes(BELL_CLAPPER, s, name="clapper")


def arc_pts(r, a0, a1, center=(0, 0)):
    """Circular arc (degrees, 0 = right, clockwise with y down) as an open bezier()."""
    n = max(1, math.ceil(abs(a1 - a0) / 90))
    d = math.radians(a1 - a0) / n
    k = 4 / 3 * math.tan(d / 4)
    v, it, ot = [], [], []
    for i in range(n + 1):
        a = math.radians(a0) + i * d
        x, y = center[0] + r * math.cos(a), center[1] + r * math.sin(a)
        tx, ty = -math.sin(a) * r * k, math.cos(a) * r * k
        v.append((x, y))
        it.append((-tx, -ty))
        ot.append((tx, ty))
    return bezier(v, it, ot, closed=False)
