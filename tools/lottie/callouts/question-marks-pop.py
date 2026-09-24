from _common import (ANTICIPATE, Comp, anim, ellipse, fill, finish, group, stroke, svg_shapes)

W, H = 460, 380
comp = Comp("question-marks-pop", W, H, fps=30, frames=60)
comp.slot("primary", "#FF2D2D")
comp.slot("outline", "#141414")

# '?' as a thick round-capped hook plus a dot, centred so (0, 0) sits at the bottom of the dot
HOOK = "M -34 -112 C -34 -160 34 -166 36 -118 C 38 -84 2 -82 2 -46"
DOT = (2, -12)


def glyph():
    return [
        group(svg_shapes(HOOK, name="hook") + [stroke(slot="primary", width=26)], "hook"),
        group([ellipse((30, 30), DOT), fill(slot="primary")], "dot"),
        group(svg_shapes(HOOK, name="hook-o") + [stroke(slot="outline", width=40)], "hook-outline"),
        group([ellipse((44, 44), DOT), fill(slot="outline")], "dot-outline"),
    ]


POP = (0.2, 0.0, 0.3, 1.0)
WOB = (0.45, 0.0, 0.55, 1.0)
marks = [  # (x, y of the dot bottom, size %, lean in degrees, pop-in frame, pop-out frame)
    (230, 250, 118, 4, 0, 46),
    (106, 318, 82, -22, 6, 49),
    (360, 330, 88, 20, 12, 52),
]
for n, (x, y, size, lean, d, out) in enumerate(marks):
    s = size
    scale = anim([(d, [0, 0], POP), (d + 5, [s * 1.18, s * 1.18], POP),
                  (d + 9, [s * 0.93, s * 0.93], POP), (d + 13, [s, s], WOB),
                  (out, [s, s], ANTICIPATE), (out + 7, [0, 0])])
    rot = [(d, lean - 24, POP), (d + 8, lean + 9, WOB)]
    f, sign = d + 8, -1
    while f + 9 < out:
        f += 9
        rot.append((f, lean + sign * 7, WOB))
        sign = -sign
    rot.append((out + 7, lean + sign * 14))
    pos = anim([(d, [x, y + 26], POP), (d + 7, [x, y], WOB), (out, [x, y - 8], ANTICIPATE),
                (out + 7, [x, y + 10])])
    comp.layer(f"question-{n}", glyph(), position=pos, scale=scale, rotation=anim(rot),
               ip=d, op=out + 7)

finish(comp, "question-marks-pop", "Question Marks Pop",
       "Three chunky question marks pop in one after another and wobble in confusion, then pop "
       "away; loops seamlessly.",
       ["question", "confused", "huh", "reaction", "thinking", "cartoon"], "loop", thumb_t=0.55)
