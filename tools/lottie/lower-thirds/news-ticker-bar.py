from _common import *
from _lt2 import rrect, poly
from drift_lottie import Variant, build_asset

W, H = 1920, 90
N = 120            # 4 s seamless loop
LINE = 3
TAG_W, SLANT = 270, 22
DOT = (34, H / 2 + LINE / 2)
PERIOD = 40


def base(name):
    comp = Comp(name, W, H, fps=FPS, frames=N)
    comp.slot("accent", "#CC0000")
    comp.slot("background", "#101318")
    comp.slot("primary", "#FFFFFF")
    return comp


def live_dot(comp, dot, size=14):
    """White dot that breathes and sends out a ring once per PERIOD (loops over N)."""
    ring_s, ring_o = [], []
    for c in range(0, N, PERIOD):
        ring_s += [(c, [100, 100], EXPO_OUT), (c + PERIOD - 1, [340, 340], HOLD)]
        ring_o += [(c, 70, EASE_OUT), (c + PERIOD - 1, 0, HOLD)]
    ring_s.append((N, [100, 100], HOLD))
    ring_o.append((N, 70, HOLD))
    comp.layer("ring", [ellipse((size, size)), stroke(slot="primary", width=2)], position=dot,
               scale=Anim(ring_s), opacity=Anim(ring_o))
    comp.layer("dot", [ellipse((size, size)), fill(slot="primary")], position=dot,
               opacity=Anim(
                   [(c + d, v, EASE_IN_OUT) for c in range(0, N, PERIOD) for d, v in ((0, 100), (PERIOD / 2, 55))]
                   + [(N, 100, HOLD)]))


def classic():
    """Full-bleed bar with a slanted red tag, pulsing live dot and a looping shine."""
    comp = base("news-ticker-bar")
    tag = bezier([(0, 0), (TAG_W + SLANT, 0), (TAG_W, H), (0, H)])
    live_dot(comp, DOT)

    comp.layer("shine-matte", [path(tag), fill("#FFFFFF")])
    comp.layer("shine", [group([rect((80, 260)),
                                gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.35), (1, "#FFFFFF", 0)],
                                              (-40, 0), (40, 0))], rotation=20)],
               matte="alpha",
               position=keys((0, [-80, H / 2], HOLD), (20, [-80, H / 2], (0.45, 0, 0.35, 1)),
                             (62, [TAG_W + 120, H / 2], HOLD), (N, [TAG_W + 120, H / 2])))

    comp.layer("tag", [path(tag), fill(slot="accent")])
    comp.layer("line", [rect((W, LINE), (W / 2, LINE / 2)), fill(slot="accent")])
    comp.layer("bar", [rect((W, H), (W / 2, H / 2)), fill(slot="background")])
    return comp


def pill():
    """Floating rounded ticker: a capsule bar inset from the edges with a pill-shaped tag and live dot."""
    comp = base("news-ticker-bar--pill")
    m, y0, h = 24, 10, 70
    r = h / 2
    tx, tw = m + 7, 290
    ty, th = y0 + 7, h - 14
    dot = (tx + 34, y0 + h / 2)
    live_dot(comp, dot, 13)
    comp.layer("shine-matte", [rrect(tx, ty, tw, th, th / 2), fill("#FFFFFF")])
    comp.layer("shine", [group([rect((70, 220)),
                                gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.4), (1, "#FFFFFF", 0)],
                                              (-35, 0), (35, 0))], rotation=20)],
               matte="alpha",
               position=keys((0, [tx - 80, H / 2], HOLD), (60, [tx - 80, H / 2], (0.45, 0, 0.35, 1)),
                             (100, [tx + tw + 80, H / 2], HOLD), (N, [tx + tw + 80, H / 2])))
    comp.layer("tag", [rrect(tx, ty, tw, th, th / 2), fill(slot="accent")])
    comp.layer("rim", [rrect(m, y0, W - 2 * m, h, r), stroke(slot="primary", width=1.5, opacity=18)])
    comp.layer("bar", [rrect(m, y0, W - 2 * m, h, r), fill(slot="background", opacity=92)])
    comp.layer("shadow", [rrect(m, y0 + 5, W - 2 * m, h, r), fill("#000000", 22)])
    return comp, {"ticker": [tx + tw + 26, ty + 4, W - m - 30 - (tx + tw + 26), th - 8],
                  "tag": [tx + 58, ty + 8, tw - 80, th - 16]}


def clock():
    """Split ticker: a slanted tag with running chevrons, the crawl bar and a clock box on the right."""
    comp = base("news-ticker-bar--clock")
    tw, sl = 250, 24
    cw = 220                        # clock box on the right
    cx0 = W - cw
    chev_x = tw + sl + 10
    # three chevrons light up in sequence, twice per loop
    for i in range(3):
        x = chev_x + i * 20
        ks = [(0, 25, HOLD)]
        for c in range(0, N, N // 2):
            t = c + 6 + i * 6
            ks += [(t, 25, EASE_OUT), (t + 5, 100, EASE_IN_OUT), (t + 18, 25, HOLD)]
        ks.append((N, 25, HOLD))
        comp.layer(f"chev{i}", [poly([(x, 30), (x + 12, H / 2), (x, H - 30)], closed=False),
                                stroke(slot="accent", width=5, cap="round", join="round")],
                   opacity=Anim(ks))
    # light sweeping along the top edge of the crawl bar
    comp.layer("scan-matte", [rrect(tw, 0, cx0 - tw, 3), fill("#FFFFFF")])
    comp.layer("scan", [rect((260, 3)), gradient_fill([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 1), (1, "#FFFFFF", 0)],
                                                     (-130, 0), (130, 0))],
               matte="alpha", position=keys((0, [tw - 140, 1.5], LINEAR), (N, [cx0 + 140, 1.5])))
    comp.layer("tag", [poly([(0, 0), (tw + sl, 0), (tw, H), (0, H)]), fill(slot="accent")])
    comp.layer("tag-shade", [poly([(tw - 40, 0), (tw + sl, 0), (tw, H), (tw - 40 - sl, H)]), fill("#000000", 18)])
    comp.layer("clock", [poly([(cx0, 0), (W, 0), (W, H), (cx0 - sl, H)]), fill(slot="primary")])
    comp.layer("clock-edge", [poly([(cx0 - 10, 0), (cx0, 0), (cx0 - sl, H), (cx0 - sl - 10, H)]), fill(slot="accent")])
    comp.layer("top", [rect((W, 3), (W / 2, 1.5)), fill(slot="primary", opacity=14)])
    comp.layer("bar", [rect((W, H), (W / 2, H / 2)), fill(slot="background")])
    return comp, {"ticker": [chev_x + 78, 14, cx0 - sl - 30 - (chev_x + 78), H - 28],
                  "tag": [26, 16, tw - 50, H - 32], "time": [cx0 + 14, 18, cw - 40, H - 36]}


pc, pa = pill()
cc, ca = clock()
AREAS = {"ticker": [TAG_W + SLANT + 24, LINE + 12, W - TAG_W - SLANT - 44, H - LINE - 24],
         "tag": [58, LINE + 14, TAG_W - 70, H - LINE - 28]}
build_asset("lower-thirds", "news-ticker-bar", "News Ticker Bar",
            "Full-width news ticker bar with a red tag block and a pulsing live indicator; add scrolling text on "
            "top. Seamless loop.",
            ["news", "ticker", "crawl", "breaking news", "live", "bar", "broadcast"], [
    Variant("classic", "Classic", classic(), "loop", text_area=AREAS["ticker"], text_areas=AREAS, thumb_t=0.28,
            bg="e8e8ee", region=(0, -230, 540, 540), pad=0.03,
            description="Full-width bar with a red tag block, a pulsing live dot and a looping shine."),
    Variant("pill", "Floating Pill", pc, "loop", text_area=pa["ticker"], text_areas=pa, thumb_t=0.7,
            bg="e8e8ee", region=(0, -225, 540, 540), pad=0.03,
            description="Rounded capsule bar inset from the edges, with a pill-shaped tag, live dot and shine."),
    Variant("clock", "Clock Split", cc, "loop", text_area=ca["ticker"], text_areas=ca, thumb_t=0.12,
            bg="e8e8ee", region=(0, -225, 540, 540), pad=0.03,
            description="Slanted tag with running chevrons, a light sweeping along the bar and a white clock box on "
                        "the right for the time or a score."),
])
