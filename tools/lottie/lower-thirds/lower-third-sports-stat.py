from _lt2 import *

K = 0.26
W, H = 1250, 250
NX, NY, NW, NH = 70, 44, 780, 100      # name bar (bottom-left x)
SX, SY, SW, SH = 50, NY + NH + 8, 520, 44
BX, BY, BW, BH = 880, 26, 210, 170      # stat box


def slanted_wipe(comp, name, x, y, w, h, slot, t_in, t_out, dur_in=16, dur_out=12, slide_px=70, parent=None):
    far = -(w + h * K + 160)
    comp.layer(f"{name}-matte", [para(x - 220, y, w + 220, h, K), fill("#FFFFFF")], parent=parent,
               position=io([far, 0], [0, 0], t_in, t_in + dur_in, t_out, t_out + dur_out, EXPO_OUT, EXPO_IN))
    return comp.layer(name, [para(x, y, w, h, K), fill(slot=slot)], matte="alpha", parent=parent,
                      position=io([-slide_px, 0], [0, 0], t_in, t_in + dur_in + 4, t_out, t_out + dur_out,
                                  EXPO_OUT, EXPO_IN))


def slots(comp, a="#101820", b="#E4002B", c="#FFD100", d="#FFFFFF"):
    comp.slot("primary", a)
    comp.slot("secondary", b)
    comp.slot("accent", c)
    comp.slot("background", d)


def glint(comp, x, y, w, h, t0):
    comp.layer("glint-matte", [para(x, y, w, h, K), fill("#FFFFFF")])
    comp.layer("glint", [para(0, y, 70, h, K), para(90, y, 16, h, K), fill("#FFFFFF", opacity=16)], matte="alpha",
               position=keys((t0, [x - 180, 0], (0.45, 0, 0.3, 1)), (t0 + 26, [x + w + 60, 0])))


def slam():
    comp = base("lower-third-sports-stat", W, H, 38)
    slots(comp)
    box = rig(comp, "stat", (BX + BW / 2, BY + BH / 2),
              off=keys((12, [0, -120], (0.5, 0, 0.7, 1)), (22, [0, 12], EASE_OUT), (27, [0, -4], EASE_IN_OUT),
                       (31, [0, 0], HOLD), (122, [0, 0], EXPO_IN), (136, [0, -120])),
              rotation=keys((12, -8, EASE_OUT), (22, 2, EASE_IN_OUT), (30, 0)),
              opacity=keys((0, 0, HOLD), (12, 0, EASE_OUT), (17, 100, HOLD), (128, 100, EASE_IN), (136, 0)))
    comp.layer("stat-top", [para(BX + (BH - 28) * K + 14, BY + 14, BW - 40, 10, K), fill(slot="primary", opacity=90)], parent=box)
    comp.layer("stat-box", [para(BX, BY, BW, BH, K), fill(slot="accent")], parent=box)
    comp.layer("stat-shadow", [para(BX + 10, BY + 12, BW, BH, K), fill("#000000", 28)], parent=box)
    glint(comp, NX, NY, NW, NH, 22)
    slanted_wipe(comp, "name", NX, NY, NW, NH, "primary", 0, 124)
    slanted_wipe(comp, "sub", SX, SY, SW, SH, "secondary", 6, 118)
    return comp


def wipe_two_row():
    comp = base("lower-third-sports-stat--wipe", W, H, 40)
    slots(comp, "#0B1F4B", "#00A3E0", "#FFFFFF", "#0B1F4B")
    by = BY
    # label strip at the bottom of the stat box
    slanted_wipe(comp, "stat-label", BX, by + BH - 44, BW, 44, "secondary", 22, 118, slide_px=30)
    comp.layer("stat-div", [para(BX + 14, by + BH - 50, BW - 20, 4, K), fill(slot="background")],
               opacity=fade(24, 26, 118, 120))
    slanted_wipe(comp, "stat-value", BX, by, BW, BH - 46, "accent", 16, 120, slide_px=30)
    for i in range(3):
        comp.layer(f"tick{i}", [para(NX + NW + 10 + i * 18, NY, 8, NH, K), fill(slot="secondary")],
                   opacity=keys((0, 0, HOLD), (10 + 2 * i, 100, HOLD), (124 - 2 * i, 0, HOLD), (125, 0)))
    glint(comp, NX, NY, NW, NH, 24)
    slanted_wipe(comp, "name", NX, NY, NW, NH, "primary", 0, 124)
    slanted_wipe(comp, "sub", SX, SY, SW, SH, "secondary", 6, 118)
    return comp


def twin():
    comp = base("lower-third-sports-stat--twin", W, H, 40)
    slots(comp, "#1B1B1B", "#7ED957", "#FF7A00", "#FFFFFF")
    bw = 150
    for i in range(2):
        x = 870 + i * (bw + 16)
        piv = (x + bw / 2, BY + BH / 2)
        b = rig(comp, f"stat{i}", piv, scale=pop(16 + 5 * i, 30 + 5 * i, 116 - 4 * i, 130 - 4 * i, peak=106))
        comp.layer(f"stat{i}-bar", [para(x + 12, BY + BH - 22, bw - 36, 6, K), fill(slot="background")],
                   parent=b)
        comp.layer(f"stat{i}", [para(x, BY, bw, BH, K), fill(slot="accent" if i == 0 else "primary")], parent=b)
        comp.layer(f"stat{i}-edge", [para(x + 6, BY + 6, bw, BH, K), fill(slot="secondary")], parent=b)
    glint(comp, NX, NY, NW, NH, 22)
    slanted_wipe(comp, "name", NX, NY, NW, NH, "primary", 0, 124)
    slanted_wipe(comp, "sub", SX, SY, SW, SH, "secondary", 6, 118)
    return comp


head = (NX + 40, NY + 18, NW - 60, NH - 36)
sub = (SX + 30, SY + 8, SW - 50, SH - 16)
build("lower-third-sports-stat", "Sports Stat Lower Third",
      "Angled sports lower third with a player name bar, a team subtitle strip and a stat box on the right. "
      "Put the player in the headline, the team in the subtitle and a number in the stat box.",
      ["lower third", "sports", "stats", "score", "player", "broadcast", "slant"], [
          V("slam", "Stat Slam", slam(), head, sub, {"stat": (BX + 40, BY + 36, BW - 60, BH - 72)}, bg="e8e8ee",
            description="Bars slash in diagonally and the stat box slams down from above with a bounce."),
          V("wipe", "Two-Row Stat", wipe_two_row(), head, sub,
            {"stat": (BX + 34, BY + 20, BW - 50, BH - 80), "stat_label": (BX + 20, BY + BH - 38, BW - 40, 32)},
            bg="e8e8ee", description="Stat box split into a value block and a label strip, wiped in with speed ticks."),
          V("twin", "Twin Stats", twin(), head, sub,
            {"stat": (900, BY + 36, 100, BH - 80), "stat_2": (1066, BY + 36, 100, BH - 80)}, bg="e8e8ee",
            description="Two smaller stat boxes pop in side by side for comparing numbers."),
      ])
