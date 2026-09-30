"""Full-frame "NPC glitch" overlay: RGB-split outlines, scanlines and glitch slices on a seamless loop."""

from _memes2 import *

W, H = 1920, 1080
C = (W / 2, H / 2)
F = 60
BURSTS = [(8, 4), (22, 2), (37, 5), (51, 3)]  # (frame, length) of glitch bursts


def glitch_keys(seed, amp, burst=BURSTS, base=(0, 0), axis=(1, 0.25)):
    """Hold-stepped [dx, dy] offsets: still, then random jumps during each burst; loops."""
    rng = random.Random(seed)
    k = [(0, list(base), HOLD)]
    for t0, n in burst:
        for j in range(n):
            k.append((t0 + j, [base[0] + rng.uniform(-amp, amp) * axis[0], base[1] + rng.uniform(-amp, amp) * axis[1]],
                      HOLD))
        k.append((t0 + n, list(base), HOLD))
    k.append((F, list(base)))
    return keys(*k)


def burst_opacity(on=100, off=0, burst=BURSTS):
    k = [(0, off, HOLD)]
    for t0, n in burst:
        k += [(t0, on, HOLD), (t0 + n, off, HOLD)]
    k.append((F, off))
    return keys(*k)


def scanlines(comp, period=6, thick=2, opacity=16):
    comp.layer("scanlines", [group([rect((W, thick), (W / 2, -period)), fill("#000000"),
                                    repeater(int(H // period) + 3, position=(0, period))], "lines")],
               position=keys((0, [0, 0], LINEAR), (F, [0, period * 4])), opacity=opacity)


def rgb_split(comp, name, shapes, width, seed, amp=22, slots=("primary", "secondary"), base_amp=6):
    """White element with red/cyan copies that sit a few px apart and jump during bursts."""
    comp.layer(name, [group(shapes + [stroke("#FFFFFF", width=width, cap="butt", join="miter")], "w")],
               position=glitch_keys(seed, amp * 0.4))
    comp.layer(name + "-r", [group(shapes + [stroke(slot=slots[0], width=width, cap="butt", join="miter")], "r")],
               position=glitch_keys(seed + 1, amp, base=(-base_amp, 0)), blend=2)
    comp.layer(name + "-c", [group(shapes + [stroke(slot=slots[1], width=width, cap="butt", join="miter")], "c")],
               position=glitch_keys(seed + 2, amp, base=(base_amp, 0)), blend=2)


def slices(comp, seed, n=5, slots=("primary", "secondary")):
    rng = random.Random(seed)
    for i in range(n):
        t0, ln = BURSTS[i % len(BURSTS)]
        y, h = rng.uniform(80, H - 80), rng.uniform(14, 70)
        dx = rng.uniform(-260, 260)
        comp.layer(f"slice{i}", [group([rect((rng.uniform(300, 900), h), (W / 2 + dx, y)),
                                        fill(slot=slots[i % 2], opacity=55)], "s"),
                                 group([rect((rng.uniform(200, 600), h * 0.4), (W / 2 - dx, y + h)),
                                        fill("#FFFFFF", 50)], "w")],
                   opacity=burst_opacity(100, 0, [(t0, ln)]))


def frame_rect(inset, r=24):
    return [rect((W - 2 * inset, H - 2 * inset), C, r)]


def rgb():
    """A thin screen outline split into red and cyan that jolts during glitch bursts, with scanlines."""
    comp = base("npc-glitch", W, H, F)
    comp.slot("primary", "#FF2A4D")
    comp.slot("secondary", "#1FE6FF")
    slices(comp, 3)
    rgb_split(comp, "outline", frame_rect(56), 8, 10)
    scanlines(comp)
    comp.layer("tint", [group([rect((W, H), C), fill(slot="secondary", opacity=10)], "t")],
               opacity=burst_opacity(100, 0))
    return comp


def marker():
    """A game-style NPC diamond marker bobs above the subject inside glitching target brackets."""
    comp = base("npc-glitch--marker", W, H, F)
    comp.slot("primary", "#FF2A4D")
    comp.slot("secondary", "#1FE6FF")
    comp.slot("accent", "#FFD83D")
    MY = 160
    bob = loop(F, [[0, 0], [0, -18]], SINE)
    dia = lambda s: polyline([(C[0], MY - 95 * s), (C[0] + 62 * s, MY), (C[0], MY + 95 * s), (C[0] - 62 * s, MY)],
                             closed=True)
    shape = [group([dia(0.55), fill("#FFFFFF", 70)], "core"), group([dia(1), fill(slot="accent")], "gem"),
             group([dia(1), stroke("#000000", width=16, opacity=45)], "edge")]
    comp.layer("marker", shape, position=at((C[0], MY), bob), anchor=(C[0], MY),
               scale=loop(F, [[100, 100], [92, 106]], SINE))
    comp.layer("marker-r", [group([dia(1), fill(slot="primary")], "r")],
               position=glitch_keys(4, 30, base=(-8, 0)), blend=2, opacity=burst_opacity(90, 0))
    comp.layer("marker-c", [group([dia(1), fill(slot="secondary")], "c")],
               position=glitch_keys(5, 30, base=(8, 0)), blend=2, opacity=burst_opacity(90, 0))
    x0, y0, x1, y1 = C[0] - 380, 300, C[0] + 380, H - 80
    arm = 90
    br = [polyline([(x0, y0 + arm), (x0, y0), (x0 + arm, y0)]), polyline([(x1 - arm, y0), (x1, y0), (x1, y0 + arm)]),
          polyline([(x1, y1 - arm), (x1, y1), (x1 - arm, y1)]), polyline([(x0 + arm, y1), (x0, y1), (x0, y1 - arm)])]
    rgb_split(comp, "brackets", br, 10, 20, amp=26)
    slices(comp, 7, n=4)
    scanlines(comp, opacity=12)
    return comp


def vhs():
    """Tape-style: heavy scanlines, a rolling tracking-noise band and colour fringes down the edges."""
    comp = base("npc-glitch--vhs", W, H, F)
    comp.slot("primary", "#FF2A4D")
    comp.slot("secondary", "#1FE6FF")
    rng = random.Random(8)
    rows = []
    for i in range(14):
        y = i * 7
        d = []
        for _ in range(10):
            d += [rng.uniform(4, 40), rng.uniform(10, 120)]
        rows.append(group([polyline([(-100, y), (W + 100, y)]),
                           stroke("#FFFFFF", width=4, cap="butt", dashes=d + [rng.uniform(0, 200)],
                                  opacity=rng.uniform(40, 80))], f"r{i}"))
    comp.layer("tracking", rows, position=keys((0, [0, -140], LINEAR), (F, [0, H + 40])))
    comp.layer("tracking-2", rows[:6], position=keys((0, [0, H / 2 - 60], LINEAR), (F / 2, [0, H + 40], HOLD),
                                                      (F / 2 + 1, [0, -140], LINEAR), (F, [0, H / 2 - 60])))
    slices(comp, 11, n=4)
    comp.layer("fringe-l", [group([rect((260, H), (50, C[1])),
                                   gradient_fill([(0, "#FF2A4D", 0.55), (1, "#FF2A4D", 0)], (0, 0), (160, 0))], "f")],
               position=glitch_keys(30, 20, axis=(1, 0)))
    comp.layer("fringe-r", [group([rect((260, H), (W - 50, C[1])),
                                   gradient_fill([(0, "#1FE6FF", 0), (1, "#1FE6FF", 0.55)], (W - 160, 0), (W, 0))], "f")],
               position=glitch_keys(31, 20, axis=(1, 0)))
    scanlines(comp, period=5, thick=2, opacity=30)
    comp.layer("vig", [vignette(W, H, 0.5, 0.45)])
    return comp


build_asset(CAT, "npc-glitch", "NPC Glitch",
            "Full-frame glitch overlay for \"NPC moment\" edits: RGB-split outlines, scanlines and glitch slices "
            "that jolt in bursts on a seamless loop. The middle stays clear for your subject.",
            ["npc", "glitch", "rgb split", "scanlines", "error", "meme", "loop"], [
    Variant("rgb", "RGB Outline", rgb(), "loop", thumb_t=0.14,
            description="Thin screen outline split into red and cyan that jolts in bursts, with scanlines."),
    Variant("marker", "NPC Marker", marker(), "loop", thumb_t=0.14, region=(420, 0, 1080, 1080),
            description="Game-style diamond marker bobbing above the subject inside glitching target brackets."),
    Variant("vhs", "Tape Tracking", vhs(), "loop", thumb_t=0.14,
            description="Heavy scanlines, a rolling tracking-noise band and colour fringes down the edges."),
])
