from _common import *

W, H = 1080, 220
K = 0.26  # horizontal slant per px of height


def para(x, y, w, h):
    """Parallelogram leaning right; (x, y+h) is the bottom-left corner."""
    s = h * K
    return path(bezier([(x + s, y), (x + w + s, y), (x + w, y + h), (x, y + h)]))


def x_at(x_bottom, y_bottom, y):
    return x_bottom + (y_bottom - y) * K


TOP, MH = 36, 100
SUB_Y, SH = TOP + MH + 6, 44
BOT = SUB_Y + SH
AX, AW = 26, 120                                   # accent block, full height, bottom-left x
MX = x_at(AX + AW + 14, BOT, TOP + MH)
MW = 820
SX = x_at(AX + AW + 14, BOT, BOT)
SW = 540

comp = Comp("lower-third-slant-sports", W, H, fps=FPS, frames=FRAMES)
comp.slot("accent", "#FFD100")
comp.slot("primary", "#12161F")
comp.slot("secondary", "#E4002B")


def wiped(name, x, y, w, h, slot, t_in, t_out, dur_in=14, dur_out=12, slide=70, opacity=100):
    far = -(w + h * K + 140)
    comp.layer(f"{name}-matte", [para(x - 200, y, w + 200, h), fill("#FFFFFF")],
               position=io([far, 0], [0, 0], t_in, t_in + dur_in, t_out, t_out + dur_out, EXPO_OUT, EXPO_IN))
    comp.layer(name, [para(x, y, w, h), fill(slot=slot, opacity=opacity)], matte="alpha",
               position=io([-slide, 0], [0, 0], t_in, t_in + dur_in + 4, t_out, t_out + dur_out,
                           EXPO_OUT, EXPO_IN))


wiped("accent", AX, TOP, AW, BOT - TOP, "accent", 0, 136, 14, 12)

# glint across the name bar
comp.layer("glint-matte", [para(MX, TOP, MW, MH), fill("#FFFFFF")])
comp.layer("glint", [para(0, TOP, 70, MH), para(90, TOP, 16, MH), fill("#FFFFFF", opacity=14)],
           matte="alpha",
           position=keys((16, [MX - 160, 0], (0.45, 0, 0.3, 1)), (42, [MX + MW + 40, 0])))

comp.layer("stripe", [para(MX + MH * K - 6 * K, TOP - 6, 180, 6), fill(slot="accent")],
           anchor=(MX, 0), position=(MX, 0),
           opacity=io(0, 100, 12, 13, 124, 125, HOLD, HOLD),
           scale=io([0, 100], [100, 100], 12, 28, 124, 132, EXPO_OUT, EXPO_IN))

wiped("main", MX, TOP, MW, MH, "primary", 4, 128, 16, 12)
wiped("sub", SX, SUB_Y, SW, SH, "secondary", 9, 122, 16, 12)

build(comp, "lower-third-slant-sports", "Slant Sports Lower Third",
      "Energetic sports lower third: slanted bars slam in with a staggered diagonal wipe and a glint.",
      ["lower third", "sports", "slant", "name", "player", "dynamic", "broadcast"],
      {"name": [MX + 44, TOP + 14, MW - 70, MH - 28], "subtitle": [SX + 30, SUB_Y + 6, SW - 50, SH - 12],
       "badge": [AX + 36, TOP + 30, AW - 36, BOT - TOP - 60]},
      thumb_t=0.5, bg="e8e8ee", intro_end=42)
