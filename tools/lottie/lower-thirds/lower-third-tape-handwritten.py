from _lt2 import *


def torn_tape(cx, cy, w, h, seed=1, teeth=7, jag=9):
    """Masking-tape outline centred on (cx, cy): straight long edges, ragged torn ends."""
    rng = random.Random(seed)
    x0, x1, y0 = cx - w / 2, cx + w / 2, cy - h / 2
    pts = [(x0 + rng.uniform(0, jag), y0), (x1 - rng.uniform(0, jag), y0)]
    for i in range(1, teeth):
        pts.append((x1 + (jag if i % 2 else -jag) * rng.uniform(0.3, 1), y0 + h * i / teeth))
    pts.append((x1 - rng.uniform(0, jag), y0 + h))
    pts.append((x0 + rng.uniform(0, jag), y0 + h))
    for i in range(teeth - 1, 0, -1):
        pts.append((x0 + (jag if i % 2 else -jag) * rng.uniform(0.3, 1), y0 + h * i / teeth))
    return poly(pts, name="tape")


def tape_items(cx, cy, w, h, slot, seed=1, stripes=True):
    shape = torn_tape(cx, cy, w, h, seed)
    items = []
    if stripes:  # faint crepe texture running along the tape
        lines = [rrect(cx - w / 2 + 6, cy - h / 2 + h * f, w - 12, 1.6) for f in (0.2, 0.37, 0.61, 0.8)]
        items.append(group(lines + [fill("#FFFFFF", 16)], "crepe"))
    items += [group([rrect(cx - w / 2 + 12, cy - h / 2 + 3, w - 24, h * 0.28, 2), fill("#FFFFFF", 16)], "sheen"),
              group([shape, fill(slot=slot, opacity=92)], "tape"),
              group([shape, fill("#000000", 18)], "shadow", position=(3, 6))]
    return items


def slap(t0, t_out, rot):
    """Scale and rotation for a strip being slapped down: comes in big, squashes, settles."""
    sc = keys((0, [0, 0], HOLD), (t0, [128, 128], EXPO_IN), (t0 + 5, [96, 96], EASE_OUT), (t0 + 10, [101, 101], EASE_IN_OUT),
              (t0 + 14, [100, 100], HOLD), (t_out, [100, 100], BACK_IN), (t_out + 12, [110, 0]))
    ro = keys((t0, rot - 6, EXPO_IN), (t0 + 5, rot + 0.8, EASE_OUT), (t0 + 12, rot, HOLD), (t_out, rot, BACK_IN),
              (t_out + 12, rot + 8))
    op = keys((0, 0, HOLD), (t0, 0, EASE_OUT), (t0 + 3, 100, HOLD), (t_out + 10, 100, EASE_IN), (t_out + 12, 0))
    return dict(scale=sc, rotation=ro, opacity=op)


def strip():
    W, H = 1100, 250
    comp = base("lower-third-tape-handwritten", W, H, 30)
    comp.slot("primary", "#F1DFA6")
    comp.slot("secondary", "#FFB3C7")
    a = (500, 92, 880, 104, -1.6)
    b = (320, 190, 500, 50, 2.2)
    for nm, (cx, cy, w, h, rot), slot, t0, t2, seed in (("sub", b, "secondary", 12, 116, 5),
                                                        ("head", a, "primary", 2, 122, 2)):
        lay(comp, nm, tape_items(cx, cy, w, h, slot, seed), (cx, cy), **slap(t0, t2, rot))
    return comp, (a[0] - a[2] / 2 + 50, a[1] - 34, a[2] - 100, 68), (b[0] - b[2] / 2 + 40, b[1] - 16, b[2] - 80, 32)


def single():
    W, H = 1050, 220
    cx, cy, w, h, rot = 520, 112, 900, 112, -2.4
    comp = base("lower-third-tape-handwritten--single", W, H, 30)
    comp.slot("primary", "#CFE8FF")
    s = slap(8, 122, rot)
    s["position"] = keys((0, [cx - 60, cy - 160], EXPO_IN), (8, [cx, cy], HOLD), (122, [cx, cy]))
    comp.layer("tape", tape_items(cx, cy, w, h, "primary", 9), anchor=(cx, cy), **s)
    return comp, (cx - w / 2 + 50, cy - h / 2 + 20, w - 100, h - 40)


def card():
    W, H = 1050, 290
    cx, cy, w, h = 500, 160, 820, 170
    comp = base("lower-third-tape-handwritten--card", W, H, 40)
    comp.slot("background", "#FFFDF6")
    comp.slot("primary", "#F1DFA6")
    comp.slot("accent", "#E9C9A3")
    for i, (tx, ty, rot, t0) in enumerate(((cx - w / 2 + 30, cy - h / 2 + 4, -32, 22),
                                           (cx + w / 2 - 30, cy - h / 2 + 4, 30, 28))):
        lay(comp, f"tape{i}", tape_items(tx, ty, 170, 46, "primary", 20 + i, stripes=False), (tx, ty),
            **slap(t0, 118 - 4 * i, rot))
    lay(comp, "rule", [rrect(cx - w / 2 + 50, cy + 18, w - 100, 2), fill(slot="accent")], (cx - w / 2 + 50, 0),
        scale=grow_x(26, 44, 114, 124))
    rg = rig(comp, "card-rig", (cx, cy + h / 2), off=slide(0, 60, 0, 20, 124, 142, EXPO_OUT, EXPO_IN, ody=60), opacity=fade(0, 8, 134, 142),
             rotation=keys((0, 5, EXPO_OUT), (22, -1, HOLD), (124, -1, EXPO_IN), (142, -6)))
    comp.layer("card", [rect((w, h), (cx, cy), 4), fill(slot="background")], parent=rg)
    comp.layer("card-shadow", shadow(cx - w / 2, cy - h / 2, w, h, 4, dy=8, n=4, spread=4, op=8), parent=rg)
    return comp, (cx - w / 2 + 50, cy - h / 2 + 34, w - 100, 64), (cx - w / 2 + 50, cy + 30, w - 100, 34)


a, ah, asub = strip()
b, bh = single()
c, chd, cs = card()
build("lower-third-tape-handwritten", "Masking Tape Lower Third",
      "Crafty lower third made from strips of masking tape with torn ends, slapped on at a slight angle. "
      "Write your name on the tape, ideally with a handwritten font.",
      ["lower third", "tape", "masking tape", "handwritten", "scrapbook", "craft", "diy"], [
          V("strip", "Two Strips", a, ah, asub,
            description="A long tape strip for the name and a shorter washi strip for the subtitle, slapped on in turn."),
          V("single", "Single Strip", b, bh,
            description="One wide tape strip that drops in from above and slaps down."),
          V("card", "Taped Card", c, chd, cs,
            description="A paper card slides up and two tape pieces pin its top corners."),
      ])
