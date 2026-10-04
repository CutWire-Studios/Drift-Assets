import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app_kit import *

F = 150


def slots(comp):
    comp.slot("background", "#181818")
    comp.slot("primary", "#1DB954")
    comp.slot("secondary", "#3A3A3A")
    comp.slot("icon", "#FFFFFF")
    comp.slot("outline", "#5A5A5A")


def art(x, y, s, r):
    return [glyph("music", s * 0.38, x + s / 2, y + s / 2, slot="icon", opacity=45),
            group([rect_tl(x, y, s, s, r), fill(slot="secondary")], "art")]


def card():
    W, H = 760, 1010
    comp = Comp("spotify-now-playing", W, H, frames=F)
    slots(comp)
    px, pw = 60, 640
    py = 800
    sh = []
    # controls
    cy = 930
    sh += [glyph("repeat", 46, 650, cy, slot="icon", opacity=70), glyph("skip-next", 70, 540, cy),
           glyph("pause", 54, 380, cy, slot="background"), group([ellipse((116, 116), (380, cy)), fill(slot="icon")], "play-bg"),
           glyph("skip-prev", 70, 220, cy), glyph("shuffle", 46, 110, cy, slot="primary")]
    # progress
    sh += [label("1:12", px, py + 56, 26, 500, opacity=70), label("3:45", px + pw, py + 56, 26, 500, anchor="r", opacity=70),
           group([ellipse((22, 22), (0, py)), fill(slot="icon")], "scrub",
                 position=Anim([(14, [px, 0], LINEAR), (F, [px + pw * 0.62, 0])])),
           group([grow_rect(px, py - 3, pw * 0.62, 6, 14, F, 3), fill(slot="icon")], "progress"),
           group([rect_tl(px, py - 3, pw, 6, 3), fill(slot="outline")], "track")]
    # title row (text areas for title/artist), heart
    sh += [glyph("heart", 56, px + pw - 28, 720, slot="primary")]
    sh += art(px, 40, pw, 20)
    sh += [group([rect_tl(0, 0, W, H, 46), fill(slot="background")], "card")]
    slide_up(comp, "card", sh, 60, 0, 18)
    return comp, {"title": (px, 676, 540, 52), "artist": (px, 738, 540, 40)}


def mini():
    W, H = 1060, 190
    comp = Comp("spotify-now-playing", W, H, frames=F)
    slots(comp)
    sh = [glyph("pause", 54, 970, 82, slot="icon"), glyph("heart", 50, 868, 82, slot="primary")]
    sh += [group([grow_rect(32, H - 28, W - 64, 4, 10, F, 2), fill(slot="icon")], "progress"),
           group([rect_tl(32, H - 28, W - 64, 4, 2), fill(slot="outline")], "track")]
    sh += art(30, 30, 122, 12)
    sh += [group([rect_tl(0, 0, W, H, 26), fill(slot="background")], "card")]
    slide_up(comp, "mini", sh, 50, 0, 16)
    return comp, {"title": (178, 40, 600, 46), "artist": (178, 94, 600, 38)}


def sticker():
    W, H = 880, 220
    comp = Comp("spotify-now-playing", W, H, frames=60)
    slots(comp)
    sh = []
    amps = [0.35, 1.0, 0.55, 0.85, 0.4, 0.95, 0.5, 0.35]
    for i in range(4):
        rot = amps[i * 2:] + amps[:i * 2]
        ks = [(k * 8, [100, max(a * 100, 20)], EASE_IN_OUT) for k, a in enumerate(rot)] + [(64, [100, max(rot[0] * 100, 20)], EASE_IN_OUT)]
        ks = ks[:7] + [(60, ks[-1][1], EASE_IN_OUT)]
        sh.append(group([rect_tl(0, -50, 12, 100, 6), fill(slot="primary")], f"eq{i}", anchor=(6, 50), position=(226 + i * 22, 118),
                        scale=Anim(ks)))
    sh += [label("Now Playing", 332, 104, 34, 700)]
    sh += art(30, 30, 160, 16)
    sh += [group([rect_tl(0, 0, W, H, 40), fill(slot="background")], "pill")]
    pop_from(comp, "sticker", sh, (W / 2, H / 2), 0, 16)
    return comp, {"title": (226, 124, 620, 44), "artist": (226, 170, 620, 36)}


vs = []
for vid, nm, fn, desc in (("card", "Player Card", card, "Full 'now playing' card: album art, title and artist, heart, a progress bar that fills with times, and transport controls."),
                          ("mini", "Mini Player", mini, "The bar at the bottom of the app: small album art, title and artist, heart, pause and a thin progress line."),
                          ("sticker", "Equalizer Sticker", sticker, "A compact 'Now Playing' pill with album art and dancing equalizer bars for music callouts.")):
    c, a = fn()
    vs.append(Variant(vid, nm, c, "loop" if vid == "sticker" else "intro-hold", text_area=a["title"], text_areas=a, thumb_t=0.95 if vid != "sticker" else 0.3,
                      bg="6a7087", description=desc))
build_asset(CAT, "spotify-now-playing", "Music Player Now Playing",
            "Spotify-style music player in dark mode: a full now-playing card, the mini player bar, and an "
            "equalizer sticker. Add the song title and artist in the text areas; album art is a placeholder tile.",
            ["spotify", "music", "now playing", "player", "song", "audio", "playlist", "album", "streaming"], vs)
