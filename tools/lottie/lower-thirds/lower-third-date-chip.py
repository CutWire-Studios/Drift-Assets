from _lt2 import *


def calendar(x, y, s, hi=(2, 1), rings=True, grid=True, name="cal"):
    """Calendar icon with its top-left at (x, y), s px square. hi = highlighted grid cell (col, row)."""
    hb = s * 0.3
    items = []
    if rings:
        for rx in (x + s * 0.28, x + s * 0.72):
            items.append(group([rrect(rx - s * 0.045, y - s * 0.09, s * 0.09, s * 0.2, s * 0.045),
                                fill(slot="secondary")], "ring"))
    if grid:
        cw, ch = s * 0.16, s * 0.12
        gx, gy = x + s * 0.14, y + hb + s * 0.12
        cells = []
        for r in range(3):
            for c in range(4):
                if (c, r) == hi:
                    continue
                cells.append(rrect(gx + c * cw * 1.25, gy + r * ch * 1.45, cw, ch, 2))
        cx, cy = gx + hi[0] * cw * 1.25, gy + hi[1] * ch * 1.45
        items.append(group([rrect(cx - 3, cy - 3, cw + 6, ch + 6, 4), fill(slot="accent")], "today"))
        items.append(group(cells + [fill(slot="secondary", opacity=35)], "grid"))
    items += [group([rrect(x, y, s, hb + s * 0.12, s * 0.16), fill(slot="accent")], "header"),
              group([rrect(x, y, s, s, s * 0.16), fill(slot="background")], "page"),
              group([rrect(x, y + 6, s, s, s * 0.16), fill("#000000", 22)], "shade")]
    return items


def slots(comp, bar="#FFFFFF", acc="#E53935", page="#FFFFFF", ink="#1F2933"):
    comp.slot("primary", bar)
    comp.slot("accent", acc)
    comp.slot("background", page)
    comp.slot("secondary", ink)


def chip():
    W, H = 1100, 240
    comp = base("lower-third-date-chip", W, H, 34)
    slots(comp, "#1F2933", "#E53935", "#FFFFFF", "#1F2933")
    s, x, y = 124, 50, 66
    c = rig(comp, "chip", (x + s / 2, y + s), scale=keys((0, [100, 0], SPRING), (16, [100, 100], HOLD),
                                                         (126, [100, 100], EXPO_IN), (140, [100, 0])),
            rotation=keys((0, -12, EXPO_OUT), (18, 0)))
    comp.layer("calendar", calendar(x, y, s), parent=c)
    bx, by, bw, bh = x + s - 20, y + 10, 900, s - 20
    wipe(comp, "bar", [rrect(bx, by, bw, bh, 14), fill(slot="primary")], (bx, by, bw, bh), 8, 30, 118, 136, "left")
    return comp, (bx + 60, by + 12, bw - 100, 50), (bx + 60, by + 66, bw - 240, 24)


def hand(cx, cy, length, width, slot="secondary"):
    return group([rrect(cx - width / 2, cy - length, width, length + width / 2, width / 2), fill(slot=slot)], "hand")


def clock():
    W, H = 1100, 230
    comp = base("lower-third-date-chip--clock", W, H, 36)
    slots(comp, "#FFFFFF", "#7C3AED", "#FFFFFF", "#111827")
    cx, cy, R = 118, 115, 70
    c = rig(comp, "clock", (cx, cy), scale=pop(0, 16, 126, 140), rotation=keys((0, -90, EXPO_OUT), (18, 0)))
    lay(comp, "minute", [hand(cx, cy, R * 0.72, 7)], (cx, cy), parent=c,
        rotation=keys((0, -360, (0.3, 0, 0.2, 1)), (36, 60, HOLD), (120, 60, LINEAR), (150, 90)))
    lay(comp, "hour", [hand(cx, cy, R * 0.46, 9, "accent")], (cx, cy), parent=c,
        rotation=keys((0, -120, (0.3, 0, 0.2, 1)), (36, 300, HOLD), (120, 300, LINEAR), (150, 303)))
    ticks = []
    for i in range(12):
        a = math.radians(i * 30)
        l = 12 if i % 3 == 0 else 6
        p0 = (cx + math.sin(a) * (R - 10), cy - math.cos(a) * (R - 10))
        p1 = (cx + math.sin(a) * (R - 10 - l), cy - math.cos(a) * (R - 10 - l))
        ticks.append(poly([p0, p1], False, f"t{i}"))
    comp.layer("face", [group([ellipse((14, 14), (cx, cy)), fill(slot="secondary")], "pivot"),
                        group(ticks + [stroke(slot="secondary", width=4)], "ticks"),
                        group([ellipse((R * 2, R * 2), (cx, cy)), fill(slot="background")], "face"),
                        group([ellipse((R * 2 + 16, R * 2 + 16), (cx, cy)), fill(slot="accent")], "bezel")], parent=c)
    x, y, w, h = cx, cy - 46, 920, 92
    comp.layer("bar", [rect_grow(x, y, w, h, h / 2, 8, 30, 120, 138, "left", start=0), fill(slot="primary")])
    return comp, (cx + R + 30, y + 14, w - R - 80, 40), (cx + R + 30, y + 58, w - R - 200, 22)


def flip():
    W, H = 1100, 250
    comp = base("lower-third-date-chip--flip", W, H, 44)
    slots(comp, "#FDF2E9", "#FF7A00", "#FFFFFF", "#3D2C1E")
    s, x, y = 136, 60, 58
    bx, by, bw, bh = x + s / 2, y + 30, 920, 100
    c = rig(comp, "chip", (x + s / 2, y + s / 2), scale=pop(0, 16, 126, 140),
            rotation=keys((0, 15, SPRING), (16, -4, HOLD), (126, -4, EXPO_IN), (140, 10)))
    hb = s * 0.3 + s * 0.12
    # the front page tears up and away, revealing the next day
    comp.layer("page-off", calendar(x, y, s, hi=(1, 1), rings=False)[:-3] +
               [group([rrect(x, y + hb - 20, s, s - hb + 20, s * 0.16), fill(slot="background")], "page")],
               parent=c, ip=0, op=34, anchor=(x + s / 2, y + hb), position=(x + s / 2, y + hb),
               scale=keys((16, [100, 100], EASE_IN), (30, [100, -10])),
               opacity=keys((22, 100, EASE_IN), (33, 0)))
    comp.layer("calendar", calendar(x, y, s, hi=(2, 1)), parent=c)
    wipe(comp, "bar", [rrect(bx, by, bw, bh, 10), fill(slot="primary")], (bx, by, bw, bh), 6, 28, 118, 136, "left")
    return comp, (x + s + 30, by + 10, bw - s / 2 - 60, 50), (x + s + 30, by + 64, bw - s / 2 - 200, 24)


a, ah, asub = chip()
b, bh, bs = clock()
c, chd, cs = flip()
build("lower-third-date-chip", "Date Chip Lower Third",
      "Small calendar-chip icon with a bar for a date, time or event. Type the date in the headline row and the "
      "time or event name beneath it.",
      ["lower third", "date", "calendar", "time", "event", "schedule", "clock"], [
          V("chip", "Calendar Chip", a, ah, asub,
            description="The calendar chip flips up into place and a bar wipes out from behind it."),
          V("clock", "Clock Chip", b, bh, bs,
            description="A clock face spins in with its hands whirling to a time; a capsule bar extends behind it."),
          V("flip", "Page Flip", c, chd, cs,
            description="The calendar's top page tears away to reveal the next day as the bar wipes on."),
      ])
