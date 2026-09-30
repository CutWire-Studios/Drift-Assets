from _lt2 import *

W, H = 1150, 240


def slots(comp, a="#12131A", b="#FF2E63", c="#08D9D6", d="#1E2130"):
    comp.slot("primary", a)
    comp.slot("accent", b)
    comp.slot("secondary", c)
    comp.slot("background", d)


def badge_shapes(cx, cy, r, color=None):
    """Hex badge with three rank chevrons; `color` forces one flat colour (for glitch ghosts)."""
    f = (lambda slot: fill(color)) if color else (lambda slot: fill(slot=slot))
    s = (lambda slot, w: stroke(color, width=w, join="miter", cap="butt")) if color else \
        (lambda slot, w: stroke(slot=slot, width=w, join="miter", cap="butt"))
    chev = []
    for i in range(3):
        y = cy - r * 0.34 + i * r * 0.3
        chev.append(poly([(cx - r * 0.42, y + r * 0.22), (cx, y), (cx + r * 0.42, y + r * 0.22)], False, f"c{i}"))
    return [group(chev + [s("secondary", r * 0.13)], "chevrons"),
            group([star(6, r * 0.82, None, (cx, cy)), s("accent", 5)], "inner"),
            group([star(6, r, None, (cx, cy)), f("background")], "hex"),
            group([star(6, r + 9, None, (cx, cy)), f("accent")], "rim")]


def plate_shapes(x, y, w, h, c, flip=False, color=None):
    corners = (0, 1, 0, 1) if not flip else (1, 0, 1, 0)
    f = (lambda slot, o=100: fill(color, o)) if color else (lambda slot, o=100: fill(slot=slot, opacity=o))
    ex = x + (c if not flip else 0)
    return [group([rrect(ex + 20, y + h - 8, w * 0.42, 5), f("secondary")], "edge"),
            group([chamfer(x, y, w, h, c, corners), f("primary", 96)], "plate"),
            group([chamfer(x - 5, y - 5, w + 10, h + 10, c + 2, corners), f("accent")], "trim")]


def chamfered():
    comp = base("lower-third-gaming-nameplate", W, H, 36)
    slots(comp)
    cx, cy, r = 130, 120, 88
    x, y, w, h = 200, 58, 880, 124
    for i in range(3):
        lay(comp, f"tick{i}", [para(x + w + 18 + i * 16, y + 20, 8, h - 40, 0.3), fill(slot="accent")],
            opacity=keys((0, 0, HOLD), (20 + 2 * i, 100, HOLD), (126 - 2 * i, 0, HOLD), (127, 0)))
    b = rig(comp, "badge", (cx, cy), scale=pop(0, 16, 128, 142, peak=112),
            rotation=keys((0, -120, EXPO_OUT), (18, 0, HOLD), (128, 0, EXPO_IN), (142, 60)))
    comp.layer("badge", badge_shapes(cx, cy, r), parent=b)
    wipe(comp, "plate", plate_shapes(x, y, w, h, 30), (x - 8, y - 8, w + 16, h + 16), 8, 30, 118, 136, "left")
    return comp, (x + 60, y + 18, w - 120, 58), (x + 60, y + 80, w - 300, 28)


def glitch():
    comp = base("lower-third-gaming-nameplate--glitch", W, H, 26)
    slots(comp, "#0E0F14", "#B8FF3C", "#FF3CAC", "#1A1D24")
    cx, cy, r = 130, 120, 88
    x, y, w, h = 200, 58, 880, 124

    def all_shapes(col=None):
        return badge_shapes(cx, cy, r, col) + plate_shapes(x, y, w, h, 30, color=col)

    lay(comp, "scan", [group([rrect(x, y + 6 + i * 14, w, 4), fill("#FFFFFF", 12)], f"s{i}") for i in range(8)],
        opacity=ghost_vis(0, 120, steps=8))
    lay(comp, "nameplate", all_shapes(), off=glitch_off(0, 120, 60, steps=8), opacity=glitch_vis(0, 120, steps=8))
    glitch_ghosts(comp, lambda col: [group(all_shapes(col), "ghost", opacity=60)], 0, 120, amp=26)
    return comp, (x + 60, y + 18, w - 120, 58), (x + 60, y + 80, w - 300, 28)


def hex_right():
    comp = base("lower-third-gaming-nameplate--hex-right", W, H, 38)
    slots(comp, "#171A2B", "#FFB800", "#7B61FF", "#232845")
    cx, cy, r = 1030, 132, 80
    x, y, w, h = 70, 84, 890, 104
    tx, ty, tw, th = 70, 36, 320, 40
    b = rig(comp, "badge", (cx, cy), scale=pop(0, 16, 128, 142, peak=112),
            rotation=keys((0, 120, EXPO_OUT), (18, 0, HOLD), (128, 0, EXPO_IN), (142, -60)))
    comp.layer("badge", badge_shapes(cx, cy, r), parent=b)
    wipe(comp, "tab", [chamfer(tx, ty, tw, th, 14, (1, 1, 0, 0)), fill(slot="accent")],
         (tx, ty, tw, th + 2), 18, 34, 116, 128, "bottom")
    wipe(comp, "plate", plate_shapes(x, y, w, h, 26, flip=True), (x - 8, y - 8, w + 16, h + 16), 8, 30, 118, 136,
         "right")
    return comp, (x + 50, y + 18, w - 170, 50), (tx + 30, ty + 8, tw - 60, th - 14)


a, ah, asub = chamfered()
g, gh, gs = glitch()
c, chd, cs = hex_right()
build("lower-third-gaming-nameplate", "Gaming Nameplate",
      "Esports-style nameplate with angular cut corners and a hexagonal rank badge of chevrons. Put the "
      "player's gamertag in the plate and a team or rank on the second row.",
      ["lower third", "gaming", "esports", "nameplate", "gamertag", "rank", "stream"], [
          V("chamfered", "Chamfered Plate", a, ah, asub,
            description="The rank badge spins in and the cut-corner plate wipes out from behind it."),
          V("glitch", "Glitch In", g, gh, gs,
            description="Same plate and badge arriving with a digital glitch, RGB-split ghosts and scanlines."),
          V("hex-right", "Badge Right", c, chd, cs,
            description="Mirrored layout: badge on the right, plate wiping leftwards and a team tab on top."),
      ])
