from _lt2 import *

W, H = 1160, 250
X, Y, WA, HA = 60, 44, 860, 96     # top (headline) block
HB, WB = 56, 600                   # bottom (subtitle) block
YB = Y + HA


def slots(comp, a="#1D2B53", b="#FF6B35", acc="#FFFFFF"):
    comp.slot("primary", a)
    comp.slot("secondary", b)
    comp.slot("accent", acc)


def slide_in():
    comp = base("lower-third-split-two-tone", W, H, 30)
    slots(comp)
    # accent square where the blocks meet
    lay(comp, "joint", [rrect(X - 16, YB - 16, 32, 32), fill(slot="accent")], (X, YB),
        scale=pop(18, 30, 116, 126), rotation=keys((18, -90, EXPO_OUT), (32, 0)))
    lay(comp, "top", [rrect(X, Y, WA, HA), fill(slot="primary")],
        off=slide(-(X + WA + 40), 0, 0, 24, 122, 142, EXPO_OUT, EXPO_IN), opacity=fade(0, 8, 132, 142))
    lay(comp, "bottom", [rrect(X, YB, WB, HB), fill(slot="secondary")],
        off=slide(W - X + 40, 0, 4, 28, 118, 138, EXPO_OUT, EXPO_IN), opacity=fade(4, 12, 128, 138))
    lay(comp, "shadow", [rrect(X + 8, Y + 10, WA, HA), rrect(X + 8, YB + 10, WB, HB), fill("#000000", 22)],
        opacity=fade(20, 30, 116, 122))
    return comp


def wipes():
    comp = base("lower-third-split-two-tone--wipe", W, H, 34)
    slots(comp, "#0F0F14", "#F5C518", "#F5C518")
    # leading edge lines that race ahead of each wipe
    lay(comp, "edge-a", [rrect(0, Y, 8, HA), fill(slot="accent")],
        off=keys((0, [X - 10, 0], EXPO_OUT), (24, [X + WA, 0], HOLD), (26, [X + WA, 0], EASE_IN), (30, [X + WA + 30, 0])),
        opacity=keys((0, 100, HOLD), (26, 100, EASE_IN), (30, 0)))
    lay(comp, "edge-b", [rrect(0, YB, 8, HB), fill(slot="primary")],
        off=keys((4, [X + WB, 0], EXPO_OUT), (28, [X - 8, 0], HOLD), (30, [X - 8, 0], EASE_IN), (34, [X - 36, 0])),
        opacity=keys((0, 0, HOLD), (4, 100, HOLD), (30, 100, EASE_IN), (34, 0)))
    wipe(comp, "top", [rrect(X, Y, WA, HA), fill(slot="primary")], (X, Y, WA, HA), 0, 24, 122, 140, "left")
    wipe(comp, "bottom", [rrect(X, YB, WB, HB), fill(slot="secondary")], (X, YB, WB, HB), 4, 28, 118, 136, "right")
    return comp


def diagonal():
    comp = base("lower-third-split-two-tone--diagonal", W, H, 30)
    slots(comp, "#5B2EFF", "#00D1B2", "#FFFFFF")
    k = 0.3
    lay(comp, "stripe", [para(X + WA - 220, Y - 14, 200, 8, k), fill(slot="accent")],
        off=slide(200, -60, 14, 32, 116, 132), opacity=fade(14, 18, 124, 132))
    lay(comp, "top", [para(X + 20, Y, WA, HA, k), fill(slot="primary")],
        off=slide(-300, -90, 0, 22, 122, 140), opacity=fade(0, 6, 132, 140))
    lay(comp, "bottom", [para(X, YB, WB, HB, k), fill(slot="secondary")],
        off=slide(300, 90, 4, 26, 118, 136), opacity=fade(4, 10, 128, 136))
    return comp


build("lower-third-split-two-tone", "Split Two-Tone Lower Third",
      "Two stacked colour blocks that fly in from opposite sides and lock together. The top block holds your "
      "name, the bottom block a role or caption.",
      ["lower third", "two tone", "split", "blocks", "bold", "name", "title"], [
          V("slide", "Slide Lock", slide_in(), (X + 30, Y + 16, WA - 60, HA - 32), (X + 30, YB + 12, WB - 60, HB - 24),
            description="Solid blocks slide in from left and right with a spinning accent square at the joint."),
          V("wipe", "Edge Wipe", wipes(), (X + 30, Y + 16, WA - 60, HA - 32), (X + 30, YB + 12, WB - 60, HB - 24),
            bg="e8e8ee", description="Blocks are wiped on in opposite directions behind racing edge lines."),
          V("diagonal", "Diagonal", diagonal(), (X + 70, Y + 16, WA - 110, HA - 32),
            (X + 40, YB + 12, WB - 80, HB - 24),
            description="Slanted parallelogram blocks that fly in diagonally from opposite corners."),
      ])
