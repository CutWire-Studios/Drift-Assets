import random

from _broadcast2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)

BARS = ["#C0C0C0", "#C0C000", "#00C0C0", "#00C000", "#C000C0", "#C00000", "#0000C0"]
REV = ["#0000C0", "#131313", "#C000C0", "#131313", "#00C0C0", "#131313", "#C0C0C0"]


def static_layers(comp, frames, seeds, row, alpha, every=1, ip=0, op=None, parent_off=None, dens=0.5):
    """Old-TV snow: noise layers (white and grey) jumping to random offsets on every `every` frames."""
    rng = random.Random(seeds[0] * 31)
    for k, s in enumerate(seeds):
        pos, ops = [], []
        for i, f in enumerate(range(0, frames, every)):
            pos.append((f, [rng.randrange(-180, 180), rng.randrange(-4, 4) * row], HOLD))
            ops.append((f, 100 if (i + k) % len(seeds) == 0 else 0, HOLD))
        pos.append((frames, pos[0][1]))
        ops.append((frames, ops[0][1]))
        color = "#FFFFFF" if k % 2 == 0 else "#9A9A9A"
        items = noise_rows(W, H + 60, s, row=row, color=color, density=dens, min_len=4, max_len=34, n_dash=8)
        comp.layer(f"snow{k}", [group(items, "rows", opacity=alpha, position=(0, -30))], position=Anim(pos),
                   opacity=Anim(ops), ip=ip, op=op)


def roll(comp, frames, op=14, h=260):
    comp.layer("roll", [group([rect((W, h)), gradient_fill(
        [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", op / 100), (1, "#FFFFFF", 0)], (0, -h / 2), (0, h / 2))], "band")],
        position=keys((0, [W / 2, -h], LINEAR), (frames, [W / 2, H + h])))


def crt(comp):
    comp.layer("crt vignette", [vignette(W, H, 0.7, 0.55)])
    scanlines(comp, W, H, 4, 2, 25, drift=False)


def static():
    """Full-screen analogue snow with a rolling bright band and CRT scanlines."""
    F = 30
    comp = Comp("tv-static-card", W, H, fps=30, frames=F)
    comp.slot("background", "#161616")
    crt(comp)
    roll(comp, F, 16)
    static_layers(comp, F, (1, 2, 3, 4), 6, 85)
    comp.layer("tear", [box(0, 0, W, 10, "#FFFFFF", opacity=45)], position=keys(
        (0, [0, 300], HOLD), (7, [0, 820], HOLD), (13, [0, 140], HOLD), (21, [0, 620], HOLD), (F, [0, 300])),
        opacity=keys((0, 100, HOLD), (3, 0, HOLD), (7, 100, HOLD), (9, 0, HOLD), (21, 100, HOLD), (23, 0, HOLD),
                     (F, 100)))
    comp.layer("base", [box(0, 0, W, H, slot="background")])
    return comp


def bars():
    """SMPTE-style colour-bar test card with a centre circle and ID box, gently flickering with static."""
    F = 60
    comp = Comp("tv-static-card--bars", W, H, fps=30, frames=F)
    comp.slot("background", "#101010")
    comp.slot("icon", "#FFFFFF")
    crt(comp)
    roll(comp, F, 8)
    static_layers(comp, F, (5, 6), 5, 10, every=2)
    bw = W / 7
    top_h, mid_h = H * 0.67, H * 0.08
    bot_y = top_h + mid_h
    # centre ID plate
    comp.layer("plate", [group([rect((620, 150), C, 18), fill(slot="background", opacity=92)], "plate"),
                         group([rect((620, 150), C, 18), stroke(slot="icon", width=4)], "rim")])
    comp.layer("circle", [group([ellipse((760, 760), C), stroke(slot="icon", width=6, opacity=85)], "circle"),
                          group([polyline([(C[0] - 380, C[1]), (C[0] + 380, C[1])]),
                                 polyline([(C[0], C[1] - 380), (C[0], C[1] + 380)]),
                                 stroke(slot="icon", width=3, opacity=60)], "cross")])
    items = [box(i * bw, 0, bw + 1, top_h, c, name=f"bar{i}") for i, c in enumerate(BARS)]
    items += [box(i * bw, top_h, bw + 1, mid_h, c, name=f"rev{i}") for i, c in enumerate(REV)]
    bottom = [("#00214C", 1.25), ("#FFFFFF", 1.25), ("#32006A", 1.25), ("#131313", 1.25), ("#090909", 0.33),
              ("#131313", 0.33), ("#1D1D1D", 0.34), ("#131313", 1)]
    x = 0
    for i, (c, wmul) in enumerate(bottom):
        items.append(box(x, bot_y, bw * wmul + 1, H - bot_y, c, name=f"bot{i}"))
        x += bw * wmul
    flick = keys((0, 100, HOLD), (17, 90, HOLD), (18, 100, HOLD), (41, 93, HOLD), (43, 100, HOLD), (F, 100))
    comp.layer("bars", items, opacity=flick)
    comp.layer("base", [box(0, 0, W, H, "#000000")])
    return comp, (C[0] - 280, C[1] - 55, 560, 110)


def no_signal():
    """Deep-blue no-signal screen with a small bars ident; a burst of static glitches it once per loop."""
    F = 75
    comp = Comp("tv-static-card--no-signal", W, H, fps=30, frames=F)
    comp.slot("background", "#0B2FA8")
    comp.slot("icon", "#FFFFFF")
    crt(comp)
    g0, g1 = 44, 54
    static_layers(comp, F, (7, 8), 6, 80, ip=g0, op=g1)
    shake = keys((0, [0, 0], HOLD), (g0, [36, 0], HOLD), (g0 + 2, [-22, 6], HOLD), (g0 + 4, [60, -4], HOLD),
                 (g0 + 6, [-10, 0], HOLD), (g1, [0, 0], HOLD), (F, [0, 0]))
    iw, ih = 460, 250
    ix, iy = C[0] - iw / 2, C[1] - ih / 2 - 90
    ident = [box(ix + i * iw / 7, iy, iw / 7 + 1, ih, c, name=f"b{i}") for i, c in enumerate(BARS)]
    comp.layer("ident frame", [group([rect_tl(ix - 10, iy - 10, iw + 20, ih + 20, 8), stroke(slot="icon", width=6)],
                                     "frame")], position=shake)
    comp.layer("ident", ident, position=shake)
    comp.layer("ident red", [box(ix, iy, iw, ih, "#FF2050", opacity=40)], position=keys(
        (0, [0, 0], HOLD), (g0, [-14, 0], HOLD), (g1, [0, 0], HOLD), (F, [0, 0])), ip=g0, op=g1)
    comp.layer("roll", [group([rect((W, 60)), fill("#FFFFFF", 14)], "band")],
               position=keys((0, [W / 2, -60], LINEAR), (F, [W / 2, H + 60])))
    comp.layer("base", [box(0, 0, W, H, slot="background")])
    return comp, (C[0] - 400, iy + ih + 50, 800, 110)


b, bt = bars()
n, nt = no_signal()
build_asset(CAT, "tv-static-card", "TV Static Card",
            "Full-screen old-TV card: analogue snow, a colour-bar test pattern or a blue no-signal screen, "
            "with CRT scanlines. Use as a cutaway or to fake a lost signal; the test card has a text area in its "
            "ID box.",
            ["tv static", "noise", "test pattern", "color bars", "no signal", "retro", "crt", "glitch"], [
    V("static", "Snow", static(), "loop", thumb_t=0.3,
      description="Full-screen analogue snow with a rolling band, tear lines and CRT scanlines."),
    V("bars", "Test Card", b, "loop", text_area=bt, thumb_t=0.3,
      description="SMPTE-style colour bars with a centre circle and an ID box for your text."),
    V("no-signal", "No Signal", n, "loop", text_area=nt, thumb_t=0.2,
      description="Deep-blue no-signal screen with a small bars ident; a burst of static glitches it once per loop."),
])
