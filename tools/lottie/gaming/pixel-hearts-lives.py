from _common import *

PX = 10
HEART = [
    "..KKK.KKK..",
    ".KRRRKRRRK.",
    "KRWWRRRRRRK",
    "KRWRRRRRRRK",
    "KRRRRRRRRDK",
    ".KRRRRRRDK.",
    "..KRRRRDK..",
    "...KRRDK...",
    "....KDK....",
    ".....K.....",
]
GW, GH = len(HEART[0]), len(HEART)
ORIGIN = (-GW * PX / 2, -GH * PX / 2)
CRACK = [5, 5, 4, 5, 6, 5, 4, 5, 5, 5]  # first column of the right half, per row

W, H, F = 430, 180, 45
comp = Comp("pixel-hearts-lives", W, H, fps=30, frames=F)
comp.slot("primary", "#E8283C")
comp.slot("outline", "#1B0B12")
comp.slot("background", "#4E4356")

XS = [85, 215, 345]
Y = 75
BREAK = 26


def cells(ch, keep=lambda c, r: True):
    return [(c, r) for c, r in grid_cells(HEART, ch) if keep(c, r)] if len(ch) == 1 else \
        [cell for k in ch for cell in cells(k, keep)]


def heart(keep=lambda c, r: True, flash=None):
    """Layered so each colour sits on the union of the colours above it: no seams."""
    g = []
    if flash is not None:
        g.append(group([*pixel_paths(cells("KRDW", keep), PX, ORIGIN), fill("#FFFFFF")], "flash",
                       opacity=flash))
    g += [
        group([*pixel_paths(cells("W", keep), PX, ORIGIN), fill("#FFFFFF", opacity=90)], "highlight"),
        group([*pixel_paths(cells("D", keep), PX, ORIGIN), fill("#000000", opacity=28)], "shade"),
        group([*pixel_paths(cells("RDW", keep), PX, ORIGIN), fill(slot="primary")], "fill"),
        group([*pixel_paths(cells("KRDW", keep), PX, ORIGIN), fill(slot="outline")], "outline"),
    ]
    return g


def pop(t):
    return anim([(t, [0, 0], OVERSHOOT), (t + 10, [100, 100])])


# shards thrown from the crack
for i, (dx, dy, t) in enumerate(((-38, -30, 0), (34, -40, 1), (-22, 30, 2), (40, 12, 0), (6, -48, 2),
                                 (-46, 4, 1))):
    x0, y0 = XS[2] + (CRACK[3] - GW / 2) * PX, Y + (3 - GH / 2) * PX
    s = t + BREAK
    comp.layer(f"shard {i}", [box(-PX / 2 * (0.6 + 0.2 * (i % 2)), -PX / 2 * (0.6 + 0.2 * (i % 2)),
                                  PX * (0.6 + 0.2 * (i % 2)), PX * (0.6 + 0.2 * (i % 2)),
                                  slot="primary" if i % 3 else None)],
               ip=s, op=s + 14,
               position=anim([(s, [x0, y0], EASE_OUT), (s + 14, [x0 + dx, y0 + dy + 20])]),
               opacity=anim([(s, 100, HOLD), (s + 7, 100, EASE_IN), (s + 14, 0)]))

# broken halves
half_flash = anim([(BREAK, 100, EASE_OUT), (BREAK + 6, 0)])
for side, sgn in (("left", -1), ("right", 1)):
    keep = (lambda c, r: c < CRACK[r]) if sgn < 0 else (lambda c, r: c >= CRACK[r])
    comp.layer(f"half {side}", heart(keep, half_flash), ip=BREAK,
               position=anim([(BREAK, [XS[2], Y], EASE_OUT), (BREAK + 4, [XS[2] + sgn * 10, Y - 6], EASE_IN),
                              (F - 1, [XS[2] + sgn * 26, Y + 60])]),
               rotation=anim([(BREAK, 0, EASE_OUT), (F - 1, sgn * 28)]),
               opacity=anim([(BREAK, 100, HOLD), (BREAK + 8, 100, EASE_IN), (F - 3, 0)]))

# intact hearts
shake = [(15, [XS[2], Y], LINEAR)]
for k, (dx, dy) in enumerate(((-3, 0), (4, -1), (-5, 1), (6, 0), (-6, -1), (7, 1), (-7, 0), (5, 0))):
    shake.append((16 + k, [XS[2] + dx, Y + dy], LINEAR))
shake.append((BREAK, [XS[2], Y], LINEAR))
comp.layer("heart 3", heart(flash=anim([(19, 0, EASE_IN), (BREAK - 1, 100)])), op=BREAK,
           position=anim(shake), scale=anim([(8, [0, 0], OVERSHOOT), (18, [100, 100], EASE_IN_OUT),
                                             (BREAK - 1, [110, 110])]),
           rotation=anim([(15, 0, LINEAR), (18, -6, LINEAR), (21, 6, LINEAR), (24, -8, LINEAR), (BREAK, 0)]))
for i in (1, 0):
    comp.layer(f"heart {i + 1}", heart(), position=(XS[i], Y), scale=pop(i * 4))

# empty container left behind
comp.layer("empty heart", [
    group([*pixel_paths(cells("RDW"), PX, ORIGIN), fill(slot="background")], "inside"),
    group([*pixel_paths(cells("KRDW"), PX, ORIGIN), fill(slot="outline")], "outline"),
], ip=BREAK, position=(XS[2], Y), scale=anim([(BREAK, [80, 80], OVERSHOOT), (BREAK + 8, [100, 100])]))

finish(comp, "pixel-hearts-lives", "Pixel Hearts Lives",
       "Three pixel-art hearts; the last one shakes, flashes and shatters, leaving an empty heart "
       "(losing a life).",
       ["hearts", "lives", "life", "pixel", "retro", "8-bit", "gaming", "damage"], "intro-hold",
       thumb_t=1.0, bg="e8e8ee", region=(20, 10, 390, 130))
