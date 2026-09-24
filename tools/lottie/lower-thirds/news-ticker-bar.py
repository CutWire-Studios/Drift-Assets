from _common import *

W, H = 1920, 90
N = 120            # 4 s seamless loop
LINE = 3
TAG_W, SLANT = 270, 22
DOT = (34, H / 2 + LINE / 2)
PERIOD = 40

comp = Comp("news-ticker-bar", W, H, fps=FPS, frames=N)
comp.slot("accent", "#CC0000")
comp.slot("background", "#101318")
comp.slot("primary", "#FFFFFF")

tag = bezier([(0, 0), (TAG_W + SLANT, 0), (TAG_W, H), (0, H)])

ring_s, ring_o = [], []
for c in range(0, N, PERIOD):
    ring_s += [(c, [100, 100], EXPO_OUT), (c + PERIOD - 1, [340, 340], HOLD)]
    ring_o += [(c, 70, EASE_OUT), (c + PERIOD - 1, 0, HOLD)]
ring_s.append((N, [100, 100], HOLD))
ring_o.append((N, 70, HOLD))

comp.layer("ring", [ellipse((14, 14)), stroke(slot="primary", width=2)], position=DOT,
           scale=Anim(ring_s), opacity=Anim(ring_o))
comp.layer("dot", [ellipse((14, 14)), fill(slot="primary")], position=DOT,
           opacity=Anim(
               [(c + d, v, EASE_IN_OUT) for c in range(0, N, PERIOD) for d, v in ((0, 100), (PERIOD / 2, 55))]
               + [(N, 100, HOLD)]))

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

build(comp, "news-ticker-bar", "News Ticker Bar",
      "Full-width news ticker bar with a red tag block, a pulsing live dot and a looping shine; add scrolling text on top.",
      ["news", "ticker", "crawl", "breaking news", "live", "bar", "broadcast"],
      {"ticker": [TAG_W + SLANT + 24, LINE + 12, W - TAG_W - SLANT - 44, H - LINE - 24],
       "tag": [58, LINE + 14, TAG_W - 70, H - LINE - 28]},
      thumb_t=0.28, bg="e8e8ee", playback="loop",
      region=(0, -230, 540, 540))
